# Paralelismo inteligente no Node.js: controlando instâncias do Claude Code

O controle eficiente de múltiplas instâncias do Claude Code via Node.js requer um sistema adaptativo que balanceie desempenho e recursos disponíveis. Este guia apresenta duas abordagens completas - uma com PM2 e outra customizada - para executar 15 tarefas paralelizáveis enquanto monitora recursos, implementa filas de prioridade e adiciona tarefas dinamicamente quando outras são concluídas.

## Comparação: PM2 vs. solução customizada

| Aspecto | PM2 | Solução Customizada |
|---------|-----|---------------------|
| **Facilidade de uso** | Interface CLI intuitiva, zero configuração inicial | Requer implementação de todos os componentes |
| **Balanceamento de carga** | Integrado, automático entre processos | Necessita implementação manual |
| **Monitoramento** | Ferramentas básicas incluídas, dashboard web (PM2.io) | Total controle sobre métricas e visualização |
| **Recuperação de falhas** | Automática, com retentativas configuráveis | Necessita implementação manual |
| **Controle granular** | Limitado às opções disponíveis | Controle total sobre comportamento |
| **Recursos avançados** | Alguns recursos premium (PM2.io) | Sem custos adicionais |
| **Overhead** | Pequeno impacto no desempenho | Potencialmente menor consumo |
| **Manutenção** | Gerenciada pela comunidade e equipe | Responsabilidade total da equipe |

### Quando escolher PM2
- Aplicações de produção que precisam de estabilidade comprovada
- Equipes com limitação de tempo para implementação
- Necessidade de recursos prontos como balanceamento de carga e zero-downtime reloads

### Quando escolher solução customizada
- Necessidade de controle granular sobre cada aspecto do sistema
- Requisitos muito específicos não cobertos pelo PM2
- Projetos onde a compreensão profunda do sistema é essencial

## Métricas importantes para monitoramento

### Métricas críticas

1. **CPU**
   - **Utilização média**: Porcentagem geral de uso de CPU
   - **Utilização por núcleo**: Identifica gargalos em núcleos específicos
   - **Event Loop Utilization (ELU)**: Indica quão ocupado está o loop de eventos
   - **Event Loop Delay (ELD)**: Medida crítica para detecção de bloqueios

2. **Memória**
   - **Heap Total/Usado**: Para detectar crescimento descontrolado de memória
   - **RSS (Resident Set Size)**: Memória total alocada pelo processo
   - **External**: Memória usada por objetos C++ vinculados a JavaScript
   - **Tendência de uso**: Crescimento consistente indica vazamento de memória

3. **Recursos de Sistema**
   - **Load Average**: Carga do sistema nos últimos 1, 5 e 15 minutos
   - **Disco I/O**: Para tarefas com operações intensivas de arquivo
   - **Rede**: Importante para comunicações entre instâncias

4. **Métricas específicas**
   - **Tamanho da fila**: Número de tarefas pendentes
   - **Taxa de sucesso/falha**: Porcentagem de tarefas concluídas com êxito
   - **Tempo de execução**: Duração média, mínima e máxima das tarefas

### Bibliotecas recomendadas para monitoramento

```javascript
// Monitoramento de CPU e memória usando systeminformation
const si = require('systeminformation');

async function collectMetrics() {
  const cpuLoad = await si.currentLoad();
  const memoryInfo = await si.mem();
  
  return {
    cpuLoad: {
      average: cpuLoad.currentLoad.toFixed(2) + '%',
      coreUsage: cpuLoad.cpus.map(core => core.load.toFixed(2) + '%')
    },
    memory: {
      total: (memoryInfo.total / 1024 / 1024 / 1024).toFixed(2) + ' GB',
      used: (memoryInfo.used / 1024 / 1024 / 1024).toFixed(2) + ' GB',
      usedPercent: (memoryInfo.used / memoryInfo.total * 100).toFixed(2) + '%'
    }
  };
}
```

## Implementação com PM2

### 1. Configuração básica do ecosystem.config.js

```javascript
module.exports = {
  apps: [
    // Aplicação principal que gerencia as tarefas
    {
      name: "claude-manager",
      script: "./manager.js",
      instances: 1, // Apenas uma instância do gerenciador
      exec_mode: "fork",
      watch: false,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "production"
      }
    },
    
    // Workers que processarão as chamadas do Claude Code
    {
      name: "claude-workers",
      script: "./worker.js",
      instances: "max", // Usar todos os núcleos disponíveis
      exec_mode: "cluster",
      watch: false,
      max_memory_restart: "800M",
      exp_backoff_restart_delay: 100,
      env: {
        NODE_ENV: "production"
      }
    }
  ]
};
```

### 2. Implementação do gerenciador de tarefas (manager.js)

```javascript
const { Queue } = require('bull');
const express = require('express');
const os = require('os');
const pm2 = require('pm2');

const app = express();
app.use(express.json());

// Fila de tarefas com prioridade
const taskQueue = new Queue('claude-tasks', {
  redis: { host: 'localhost', port: 6379 }
});

// Rota para adicionar tarefas
app.post('/task', async (req, res) => {
  const { prompt, priority = 5 } = req.body;
  
  if (!prompt) {
    return res.status(400).json({ error: 'Prompt é obrigatório' });
  }
  
  const job = await taskQueue.add(
    { prompt },
    { 
      priority: 10 - priority, // Inverter para Bull (menor número = maior prioridade)
      attempts: 3,
      removeOnComplete: true
    }
  );
  
  res.json({ jobId: job.id, message: 'Tarefa adicionada com sucesso' });
});

// Rota para status de tarefas
app.get('/task/:id', async (req, res) => {
  const job = await taskQueue.getJob(req.params.id);
  
  if (!job) {
    return res.status(404).json({ error: 'Tarefa não encontrada' });
  }
  
  const state = await job.getState();
  const progress = job._progress;
  
  res.json({
    id: job.id,
    state,
    progress,
    data: job.data,
    returnValue: job.returnvalue
  });
});

// Monitoramento de recursos
app.get('/status', async (req, res) => {
  pm2.connect(async (err) => {
    if (err) {
      res.status(500).json({ error: 'Erro ao conectar com PM2' });
      return;
    }
    
    pm2.list(async (err, list) => {
      if (err) {
        res.status(500).json({ error: 'Erro ao obter lista de processos' });
        pm2.disconnect();
        return;
      }
      
      const workerData = list.filter(p => p.name === 'claude-workers');
      const queueStatus = await getQueueStatus();
      const systemLoad = getSystemLoad();
      
      res.json({
        workers: {
          count: workerData.length,
          status: workerData.map(p => ({
            id: p.pm_id,
            status: p.pm2_env.status,
            cpu: p.monit.cpu,
            memory: `${Math.round(p.monit.memory / 1024 / 1024)} MB`
          }))
        },
        queue: queueStatus,
        system: systemLoad
      });
      
      pm2.disconnect();
    });
  });
});

// Obter status da fila
async function getQueueStatus() {
  const [waiting, active, completed, failed] = await Promise.all([
    taskQueue.getWaitingCount(),
    taskQueue.getActiveCount(),
    taskQueue.getCompletedCount(),
    taskQueue.getFailedCount()
  ]);
  
  return {
    waiting,
    active,
    completed,
    failed,
    total: waiting + active + completed + failed
  };
}

// Obter carga do sistema
function getSystemLoad() {
  const cpus = os.cpus();
  const loadAvg = os.loadavg();
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  
  return {
    cpuCount: cpus.length,
    loadAverage: {
      '1m': loadAvg[0].toFixed(2),
      '5m': loadAvg[1].toFixed(2),
      '15m': loadAvg[2].toFixed(2),
      perCore: (loadAvg[0] / cpus.length).toFixed(2)
    },
    memory: {
      total: `${(totalMem / 1024 / 1024 / 1024).toFixed(2)} GB`,
      free: `${(freeMem / 1024 / 1024 / 1024).toFixed(2)} GB`,
      used: `${((totalMem - freeMem) / 1024 / 1024 / 1024).toFixed(2)} GB`,
      usedPercent: `${(((totalMem - freeMem) / totalMem) * 100).toFixed(2)}%`
    }
  };
}

// Ajuste dinâmico de workers baseado na carga
setInterval(() => {
  const load = getSystemLoad();
  const loadPerCore = parseFloat(load.loadAverage.perCore);
  
  pm2.connect(function(err) {
    if (err) {
      console.error('Erro ao conectar com PM2:', err);
      return;
    }
    
    pm2.list((err, list) => {
      if (err) {
        console.error('Erro ao listar processos:', err);
        pm2.disconnect();
        return;
      }
      
      const workerCount = list.filter(p => p.name === 'claude-workers').length;
      const cpuCount = os.cpus().length;
      
      // Escalar com base na carga
      if (loadPerCore > 0.7 && workerCount < cpuCount) {
        console.log(`Carga alta (${loadPerCore}), aumentando workers...`);
        pm2.scale('claude-workers', workerCount + 1, (err) => {
          if (err) console.error('Erro ao escalar:', err);
          pm2.disconnect();
        });
      } else if (loadPerCore < 0.3 && workerCount > 2) {
        console.log(`Carga baixa (${loadPerCore}), reduzindo workers...`);
        pm2.scale('claude-workers', workerCount - 1, (err) => {
          if (err) console.error('Erro ao escalar:', err);
          pm2.disconnect();
        });
      } else {
        pm2.disconnect();
      }
    });
  });
}, 60000); // Verificar a cada minuto

// Iniciar servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Gerenciador iniciado na porta ${PORT}`);
});
```

### 3. Implementação do worker (worker.js)

```javascript
const { Queue, QueueScheduler } = require('bull');
const Anthropic = require('@anthropic-ai/sdk');

// Assegurar processamento ordenado mesmo com múltiplos workers
new QueueScheduler('claude-tasks');

// Configurar cliente Claude
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Conectar à fila de tarefas
const taskQueue = new Queue('claude-tasks', {
  redis: { host: 'localhost', port: 6379 }
});

// Processar tarefas
taskQueue.process(async (job) => {
  const { prompt } = job.data;
  
  job.progress(10);
  
  try {
    // Reportar início da tarefa
    console.log(`[Worker ${process.pid}] Processando tarefa ${job.id}`);
    
    // Chamar a API Claude
    const startTime = Date.now();
    
    const response = await anthropic.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 4000,
      messages: [{ role: "user", content: prompt }],
    });
    
    const duration = Date.now() - startTime;
    
    job.progress(100);
    
    // Reportar conclusão
    console.log(`[Worker ${process.pid}] Tarefa ${job.id} concluída em ${duration}ms`);
    
    // Retornar resultado
    return {
      content: response.content[0].text,
      usage: response.usage,
      processingTime: duration
    };
  } catch (error) {
    console.error(`[Worker ${process.pid}] Erro na tarefa ${job.id}:`, error.message);
    throw error; // Permitir que o Bull gerencie retentativas
  }
});

// Evento para registrar o início do worker
console.log(`[Worker ${process.pid}] Iniciado e pronto para processar tarefas`);

// Monitoramento de memória para auto-recuperação
setInterval(() => {
  const memoryUsage = process.memoryUsage();
  const heapUsed = Math.round(memoryUsage.heapUsed / 1024 / 1024);
  
  // Auto-recover se uso de memória for muito alto
  if (heapUsed > 700) { // 700MB
    console.warn(`[Worker ${process.pid}] Uso de memória alto (${heapUsed}MB), iniciando limpeza`);
    global.gc && global.gc(); // Forçar garbage collection se disponível
  }
}, 30000);
```

### 4. Scripts de implantação

```bash
# Iniciar o sistema completo
npm install -g pm2
pm2 start ecosystem.config.js

# Monitoramento em tempo real
pm2 monit

# Escalar manualmente workers
pm2 scale claude-workers +2

# Reiniciar com zero downtime
pm2 reload claude-workers

# Verificar logs
pm2 logs claude-workers
```

## Implementação com solução customizada

### 1. Estrutura de arquivos

```
project/
├── src/
│   ├── index.js           # Ponto de entrada principal
│   ├── taskManager.js     # Gerenciador de tarefas e recursos
│   ├── priorityQueue.js   # Implementação da fila de prioridade
│   ├── monitorService.js  # Sistema de monitoramento  
│   ├── claudeService.js   # Integração com Claude API
│   └── workers/
│       └── workerPool.js  # Pool de worker threads
└── config.js              # Configurações do sistema
```

### 2. Implementação da fila de prioridade (priorityQueue.js)

```javascript
class PriorityQueue {
  constructor(comparator = (a, b) => a.priority - b.priority) {
    this.heap = [];
    this.comparator = comparator;
  }

  get size() {
    return this.heap.length;
  }

  isEmpty() {
    return this.size === 0;
  }

  peek() {
    return this.heap[0];
  }

  enqueue(item, priority) {
    this.heap.push({ item, priority });
    this._siftUp();
    return this.size;
  }

  dequeue() {
    if (this.isEmpty()) {
      return null;
    }
    
    const top = this.heap[0];
    const bottom = this.heap.pop();
    
    if (this.size > 0) {
      this.heap[0] = bottom;
      this._siftDown();
    }
    
    return top.item;
  }

  _parent(idx) {
    return Math.floor((idx - 1) / 2);
  }

  _leftChild(idx) {
    return 2 * idx + 1;
  }

  _rightChild(idx) {
    return 2 * idx + 2;
  }

  _swap(i, j) {
    [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
  }

  _siftUp() {
    let idx = this.size - 1;
    while (idx > 0) {
      const parentIdx = this._parent(idx);
      if (this.comparator(this.heap[idx], this.heap[parentIdx]) >= 0) break;
      this._swap(idx, parentIdx);
      idx = parentIdx;
    }
  }

  _siftDown() {
    let idx = 0;
    const length = this.size;
    
    while (true) {
      const leftIdx = this._leftChild(idx);
      const rightIdx = this._rightChild(idx);
      let smallest = idx;
      
      if (leftIdx < length && this.comparator(this.heap[leftIdx], this.heap[smallest]) < 0) {
        smallest = leftIdx;
      }
      
      if (rightIdx < length && this.comparator(this.heap[rightIdx], this.heap[smallest]) < 0) {
        smallest = rightIdx;
      }
      
      if (smallest === idx) break;
      
      this._swap(idx, smallest);
      idx = smallest;
    }
  }
}

module.exports = PriorityQueue;
```

### 3. Serviço de monitoramento (monitorService.js)

```javascript
const os = require('os');
const EventEmitter = require('events');

class MonitorService extends EventEmitter {
  constructor(options = {}) {
    super();
    this.interval = options.interval || 5000; // 5 segundos
    this.cpuThresholds = {
      high: options.highCpuThreshold || 0.7,  // 70%
      low: options.lowCpuThreshold || 0.3     // 30%
    };
    this.memoryThresholds = {
      high: options.highMemoryThreshold || 0.8,  // 80%
      low: options.lowMemoryThreshold || 0.4     // 40%
    };
    this.metrics = {
      cpu: {},
      memory: {},
      system: {},
      tasks: {
        active: 0,
        queued: 0,
        completed: 0,
        failed: 0
      }
    };
    this.history = {
      cpu: [],
      memory: [],
      tasks: []
    };
    this.historyMaxLength = options.historyLength || 60; // 5 minutos com intervalo de 5s
    this.monitorTimer = null;
  }

  start() {
    if (this.monitorTimer) return;
    
    this.gatherMetrics();
    this.monitorTimer = setInterval(() => this.gatherMetrics(), this.interval);
    console.log(`Monitor iniciado com intervalo de ${this.interval}ms`);
  }

  stop() {
    if (this.monitorTimer) {
      clearInterval(this.monitorTimer);
      this.monitorTimer = null;
      console.log('Monitor parado');
    }
  }
  
  updateTaskMetrics(metrics) {
    this.metrics.tasks = {
      ...this.metrics.tasks,
      ...metrics
    };
  }

  gatherMetrics() {
    // Métricas de CPU
    const cpuUsage = this.getCpuUsage();
    this.metrics.cpu = cpuUsage;
    this.history.cpu.push({
      timestamp: Date.now(),
      average: cpuUsage.loadPerCore
    });
    
    // Métricas de memória
    const memoryUsage = this.getMemoryUsage();
    this.metrics.memory = memoryUsage;
    this.history.memory.push({
      timestamp: Date.now(),
      usedPercent: memoryUsage.usedPercent
    });
    
    // Métricas de tarefas
    this.history.tasks.push({
      timestamp: Date.now(),
      ...this.metrics.tasks
    });
    
    // Limitar tamanho do histórico
    if (this.history.cpu.length > this.historyMaxLength) {
      this.history.cpu.shift();
      this.history.memory.shift();
      this.history.tasks.shift();
    }
    
    // Event Loop Delay (ELD)
    this.checkEventLoopDelay();
    
    // Emitir evento com métricas atualizadas
    this.emit('metrics', this.getMetrics());
    
    // Verificar limites
    this.checkThresholds();
  }
  
  checkEventLoopDelay() {
    const start = Date.now();
    
    setTimeout(() => {
      const delay = Date.now() - start - 0; // 0ms é o delay esperado
      this.metrics.system.eventLoopDelay = delay;
      
      if (delay > 100) { // 100ms é considerado alto para o loop de eventos
        this.emit('highEventLoopDelay', delay);
      }
    }, 0);
  }
  
  checkThresholds() {
    const cpuLoad = this.metrics.cpu.loadPerCore;
    const memUsage = this.metrics.memory.usedPercent / 100;
    
    // Verificar CPU
    if (cpuLoad > this.cpuThresholds.high) {
      this.emit('highCpu', cpuLoad);
    } else if (cpuLoad < this.cpuThresholds.low) {
      this.emit('lowCpu', cpuLoad);
    }
    
    // Verificar memória
    if (memUsage > this.memoryThresholds.high) {
      this.emit('highMemory', memUsage);
    } else if (memUsage < this.memoryThresholds.low) {
      this.emit('lowMemory', memUsage);
    }
  }
  
  getCpuUsage() {
    const cpus = os.cpus();
    const loadAvg = os.loadavg();
    
    return {
      cores: cpus.length,
      load: {
        '1m': loadAvg[0],
        '5m': loadAvg[1],
        '15m': loadAvg[2]
      },
      loadPerCore: loadAvg[0] / cpus.length
    };
  }
  
  getMemoryUsage() {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    
    return {
      total: Math.round(totalMem / (1024 * 1024)),
      used: Math.round(usedMem / (1024 * 1024)),
      free: Math.round(freeMem / (1024 * 1024)),
      usedPercent: Math.round((usedMem / totalMem) * 100)
    };
  }
  
  getMetrics() {
    return {
      timestamp: Date.now(),
      cpu: this.metrics.cpu,
      memory: this.metrics.memory,
      system: this.metrics.system,
      tasks: this.metrics.tasks,
      history: this.history
    };
  }
  
  canAcceptMoreTasks() {
    const cpuLoad = this.metrics.cpu.loadPerCore;
    const memUsage = this.metrics.memory.usedPercent / 100;
    const eventLoopDelay = this.metrics.system?.eventLoopDelay || 0;
    
    // Algoritmo para determinar capacidade
    // Retorna um score de 0 a 1, onde 1 é capacidade total
    const cpuScore = Math.max(0, 1 - (cpuLoad / this.cpuThresholds.high));
    const memScore = Math.max(0, 1 - (memUsage / this.memoryThresholds.high));
    const eldScore = Math.max(0, 1 - (eventLoopDelay / 100));
    
    const overallScore = (cpuScore * 0.4) + (memScore * 0.4) + (eldScore * 0.2);
    
    return {
      canAccept: overallScore > 0.3, // 30% de capacidade mínima
      capacityScore: overallScore,
      recommendedBatch: Math.ceil(overallScore * 10) // 0-10 tarefas baseado na capacidade
    };
  }
}

module.exports = MonitorService;
```

### 4. Pool de Worker Threads (workers/workerPool.js)

```javascript
const { Worker } = require('worker_threads');
const os = require('os');
const path = require('path');
const { EventEmitter } = require('events');

class WorkerPool extends EventEmitter {
  constructor(options = {}) {
    super();
    this.workerScript = options.workerScript || path.resolve(__dirname, './worker.js');
    this.minWorkers = options.minWorkers || 2;
    this.maxWorkers = options.maxWorkers || os.cpus().length;
    this.workerOptions = options.workerOptions || {};
    this.workerTimeout = options.workerTimeout || 60000; // 1 minuto
    
    this.workers = [];
    this.idleWorkers = [];
    this.activeWorkers = new Map();
    this.taskQueue = [];
    this.pendingTasks = new Map();
    
    this.initialize();
  }
  
  initialize() {
    // Criar workers iniciais
    for (let i = 0; i < this.minWorkers; i++) {
      this.addWorker();
    }
    
    // Verificar workers inativos periodicamente
    setInterval(() => this.checkInactiveWorkers(), 30000);
  }
  
  addWorker() {
    const worker = new Worker(this.workerScript, this.workerOptions);
    const workerId = this.workers.length;
    
    worker.on('message', (message) => this.handleWorkerMessage(workerId, message));
    worker.on('error', (error) => this.handleWorkerError(workerId, error));
    worker.on('exit', (code) => this.handleWorkerExit(workerId, code));
    
    this.workers.push(worker);
    this.idleWorkers.push(workerId);
    
    console.log(`Worker #${workerId} adicionado ao pool`);
    this.emit('workerAdded', { workerId, poolSize: this.workers.length });
    
    return workerId;
  }
  
  removeWorker(workerId) {
    if (workerId >= this.workers.length || !this.workers[workerId]) return false;
    
    console.log(`Removendo worker #${workerId}`);
    
    const worker = this.workers[workerId];
    
    // Verificar se worker está processando tarefa
    if (this.activeWorkers.has(workerId)) {
      const taskId = this.activeWorkers.get(workerId);
      console.log(`Worker #${workerId} estava processando tarefa ${taskId}, requibando...`);
      this.requeueTask(taskId);
    }
    
    // Remover das listas
    this.idleWorkers = this.idleWorkers.filter(id => id !== workerId);
    this.activeWorkers.delete(workerId);
    
    // Terminar worker
    worker.terminate()
      .then(() => {
        console.log(`Worker #${workerId} terminado com sucesso`);
        this.workers[workerId] = null;
        this.emit('workerRemoved', { workerId, poolSize: this.getActiveWorkerCount() });
        this.processQueue();
      })
      .catch(err => {
        console.error(`Erro ao terminar worker #${workerId}:`, err);
      });
    
    return true;
  }
  
  handleWorkerMessage(workerId, message) {
    if (!message || typeof message !== 'object') return;
    
    switch (message.type) {
      case 'ready':
        console.log(`Worker #${workerId} está pronto`);
        this.makeWorkerIdle(workerId);
        break;
        
      case 'result':
        console.log(`Worker #${workerId} completou tarefa ${message.taskId}`);
        this.completeTask(message.taskId, message.result);
        this.makeWorkerIdle(workerId);
        break;
        
      case 'error':
        console.error(`Worker #${workerId} reportou erro:`, message.error);
        this.failTask(message.taskId, new Error(message.error));
        this.makeWorkerIdle(workerId);
        break;
        
      case 'status':
        // Atualizar status do worker
        this.emit('workerStatus', { workerId, status: message.status });
        break;
    }
  }
  
  handleWorkerError(workerId, error) {
    console.error(`Erro no worker #${workerId}:`, error);
    
    // Obter taskId se worker estiver ativo
    let taskId = null;
    if (this.activeWorkers.has(workerId)) {
      taskId = this.activeWorkers.get(workerId);
    }
    
    // Recriar worker
    this.removeWorker(workerId);
    this.addWorker();
    
    // Falhar a tarefa se necessário
    if (taskId) {
      this.failTask(taskId, error);
    }
  }
  
  handleWorkerExit(workerId, code) {
    console.log(`Worker #${workerId} encerrou com código ${code}`);
    
    // Se não foi uma terminação solicitada, recriar worker
    if (this.workers[workerId] !== null && this.getActiveWorkerCount() < this.minWorkers) {
      console.log(`Recriando worker #${workerId} após saída inesperada`);
      this.addWorker();
    }
  }
  
  makeWorkerIdle(workerId) {
    // Remover de workers ativos
    if (this.activeWorkers.has(workerId)) {
      this.activeWorkers.delete(workerId);
    }
    
    // Adicionar à lista de inativos se ainda não estiver
    if (!this.idleWorkers.includes(workerId)) {
      this.idleWorkers.push(workerId);
    }
    
    // Processar fila
    this.processQueue();
  }
  
  queueTask(task) {
    const taskId = Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    
    this.taskQueue.push({
      id: taskId,
      task,
      timestamp: Date.now(),
      retries: 0
    });
    
    this.emit('taskQueued', { taskId, queueSize: this.taskQueue.length });
    
    // Tentar processar imediatamente
    setImmediate(() => this.processQueue());
    
    return taskId;
  }
  
  completeTask(taskId, result) {
    if (!this.pendingTasks.has(taskId)) return;
    
    const { resolve } = this.pendingTasks.get(taskId);
    this.pendingTasks.delete(taskId);
    
    resolve(result);
    
    this.emit('taskCompleted', { taskId, result });
  }
  
  failTask(taskId, error) {
    if (!this.pendingTasks.has(taskId)) return;
    
    const { reject } = this.pendingTasks.get(taskId);
    this.pendingTasks.delete(taskId);
    
    reject(error);
    
    this.emit('taskFailed', { taskId, error });
  }
  
  requeueTask(taskId) {
    if (!this.pendingTasks.has(taskId)) return;
    
    const { task, retries } = this.pendingTasks.get(taskId);
    this.pendingTasks.delete(taskId);
    
    // Limitar número de retentativas
    if (retries >= 3) {
      this.emit('taskFailed', { 
        taskId, 
        error: new Error('Excedido número máximo de retentativas') 
      });
      return;
    }
    
    // Adicionar à fila com prioridade
    this.taskQueue.unshift({
      id: taskId,
      task,
      timestamp: Date.now(),
      retries: retries + 1
    });
    
    this.emit('taskRequeued', { taskId, retries: retries + 1 });
  }
  
  processQueue() {
    // Verificar se há tarefas e workers disponíveis
    if (this.taskQueue.length === 0 || this.idleWorkers.length === 0) {
      return;
    }
    
    // Obter próxima tarefa
    const { id: taskId, task, retries } = this.taskQueue.shift();
    
    // Obter worker disponível
    const workerId = this.idleWorkers.shift();
    
    // Registrar como ativo
    this.activeWorkers.set(workerId, taskId);
    
    // Criar promise para retorno da tarefa
    const taskPromise = new Promise((resolve, reject) => {
      // Adicionar timeout
      const timeoutId = setTimeout(() => {
        console.warn(`Tarefa ${taskId} no worker #${workerId} atingiu timeout`);
        this.removeWorker(workerId); // Recriar worker
        reject(new Error('Timeout excedido'));
      }, this.workerTimeout);
      
      // Armazenar referências
      this.pendingTasks.set(taskId, { 
        resolve, 
        reject, 
        task, 
        workerId, 
        retries,
        timeoutId 
      });
    });
    
    // Limpar timeout quando tarefa concluir
    taskPromise
      .finally(() => {
        if (this.pendingTasks.has(taskId)) {
          clearTimeout(this.pendingTasks.get(taskId).timeoutId);
        }
      });
    
    // Enviar tarefa para o worker
    this.workers[workerId].postMessage({
      type: 'task',
      taskId,
      payload: task
    });
    
    this.emit('taskStarted', { taskId, workerId });
    
    return taskPromise;
  }
  
  executeTask(task) {
    const taskId = this.queueTask(task);
    
    return new Promise((resolve, reject) => {
      this.pendingTasks.set(taskId, { 
        resolve, 
        reject, 
        task, 
        retries: 0 
      });
    });
  }
  
  checkInactiveWorkers() {
    // Reduzir workers se houver mais que o mínimo e alguns inativos
    const excessIdleWorkers = Math.max(0, this.idleWorkers.length - 1);
    const workersToRemove = Math.min(
      excessIdleWorkers,
      this.getActiveWorkerCount() - this.minWorkers
    );
    
    if (workersToRemove > 0) {
      console.log(`Removendo ${workersToRemove} workers inativos`);
      
      for (let i = 0; i < workersToRemove; i++) {
        if (this.idleWorkers.length > 0) {
          const workerId = this.idleWorkers.pop();
          this.removeWorker(workerId);
        }
      }
    }
  }
  
  getActiveWorkerCount() {
    return this.workers.filter(w => w !== null).length;
  }
  
  getStats() {
    return {
      workers: {
        total: this.getActiveWorkerCount(),
        idle: this.idleWorkers.length,
        active: this.activeWorkers.size,
        min: this.minWorkers,
        max: this.maxWorkers
      },
      tasks: {
        queued: this.taskQueue.length,
        pending: this.pendingTasks.size
      }
    };
  }
  
  resize(size) {
    const targetSize = Math.min(Math.max(size, this.minWorkers), this.maxWorkers);
    const currentSize = this.getActiveWorkerCount();
    
    if (targetSize === currentSize) return;
    
    if (targetSize > currentSize) {
      // Adicionar workers
      for (let i = 0; i < targetSize - currentSize; i++) {
        this.addWorker();
      }
    } else {
      // Remover workers (apenas inativos)
      const workersToRemove = currentSize - targetSize;
      let removed = 0;
      
      while (removed < workersToRemove && this.idleWorkers.length > 0) {
        const workerId = this.idleWorkers.pop();
        if (this.removeWorker(workerId)) {
          removed++;
        }
      }
    }
  }
}

module.exports = WorkerPool;
```

### 5. Worker Thread (workers/worker.js)

```javascript
const { parentPort } = require('worker_threads');
const Anthropic = require('@anthropic-ai/sdk');

// Inicializar cliente Claude
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Reportar que o worker está pronto
parentPort.postMessage({ type: 'ready' });

// Monitoramento de recursos
function getMemoryUsage() {
  const memoryUsage = process.memoryUsage();
  
  return {
    rss: Math.round(memoryUsage.rss / 1024 / 1024),
    heapTotal: Math.round(memoryUsage.heapTotal / 1024 / 1024),
    heapUsed: Math.round(memoryUsage.heapUsed / 1024 / 1024),
    external: Math.round(memoryUsage.external / 1024 / 1024)
  };
}

// Enviar status periodicamente
setInterval(() => {
  parentPort.postMessage({
    type: 'status',
    status: {
      memory: getMemoryUsage(),
      timestamp: Date.now()
    }
  });
}, 10000);

// Receber mensagens do pool
parentPort.on('message', async (message) => {
  if (message.type !== 'task') return;
  
  const { taskId, payload } = message;
  
  try {
    console.log(`Worker processando tarefa ${taskId}`);
    
    // Chamar a API Claude
    const startTime = Date.now();
    
    const response = await anthropic.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 4000,
      messages: [{ role: "user", content: payload.prompt }],
    });
    
    const duration = Date.now() - startTime;
    
    // Enviar resultado
    parentPort.postMessage({
      type: 'result',
      taskId,
      result: {
        content: response.content[0].text,
        usage: response.usage,
        processingTime: duration
      }
    });
  } catch (error) {
    console.error(`Erro ao processar tarefa ${taskId}:`, error);
    
    // Enviar erro
    parentPort.postMessage({
      type: 'error',
      taskId,
      error: error.message
    });
  }
});

// Tratamento de encerramento
process.on('unhandledRejection', (error) => {
  console.error('Unhandled Rejection:', error);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Registrar erro e encerrar worker (será recriado pelo pool)
  parentPort.postMessage({
    type: 'error',
    error: `Worker crash: ${error.message}`
  });
  
  process.exit(1);
});
```

### 6. Serviço de integração com Claude (claudeService.js)

```javascript
class ClaudeService {
  constructor(workerPool, options = {}) {
    this.workerPool = workerPool;
    this.modelOptions = {
      defaultModel: options.defaultModel || 'claude-3-opus-20240229',
      maxTokens: options.maxTokens || 4000
    };
    
    // Estatísticas
    this.stats = {
      totalRequests: 0,
      totalTokensInput: 0,
      totalTokensOutput: 0,
      totalErrors: 0,
      averageResponseTime: 0,
      responseTimeHistory: []
    };
  }
  
  async processPrompt(prompt, options = {}) {
    const startTime = Date.now();
    this.stats.totalRequests++;
    
    try {
      const task = {
        prompt,
        model: options.model || this.modelOptions.defaultModel,
        maxTokens: options.maxTokens || this.modelOptions.maxTokens,
        options
      };
      
      // Executar tarefa no pool
      const result = await this.workerPool.executeTask(task);
      
      // Atualizar estatísticas
      const duration = Date.now() - startTime;
      this.updateStats(duration, result.usage);
      
      return {
        content: result.content,
        usage: result.usage,
        processingTime: duration
      };
    } catch (error) {
      this.stats.totalErrors++;
      throw error;
    }
  }
  
  updateStats(duration, usage) {
    // Atualizar histórico de tempo de resposta
    this.stats.responseTimeHistory.push(duration);
    
    // Limitar tamanho do histórico
    if (this.stats.responseTimeHistory.length > 100) {
      this.stats.responseTimeHistory.shift();
    }
    
    // Recalcular média
    this.stats.averageResponseTime = this.stats.responseTimeHistory.reduce(
      (a, b) => a + b, 0
    ) / this.stats.responseTimeHistory.length;
    
    // Atualizar tokens
    if (usage) {
      this.stats.totalTokensInput += usage.input_tokens || 0;
      this.stats.totalTokensOutput += usage.output_tokens || 0;
    }
  }
  
  getStats() {
    return {
      ...this.stats,
      currentTime: Date.now()
    };
  }
}

module.exports = ClaudeService;
```

### 7. Gerenciador de tarefas (taskManager.js)

```javascript
const PriorityQueue = require('./priorityQueue');
const EventEmitter = require('events');

class TaskManager extends EventEmitter {
  constructor(claudeService, monitorService, options = {}) {
    super();
    this.claudeService = claudeService;
    this.monitorService = monitorService;
    this.taskQueue = new PriorityQueue();
    this.activeTasksCount = 0;
    this.maxConcurrentTasks = options.maxConcurrentTasks || 10;
    this.completedTasks = [];
    this.failedTasks = [];
    this.maxHistorySize = options.maxHistorySize || 100;
    this.adaptiveConcurrency = options.adaptiveConcurrency !== false;
    
    // Iniciar processamento
    setImmediate(() => this.processQueue());
    
    // Ajustar concorrência com base em recursos
    if (this.adaptiveConcurrency) {
      this.monitorService.on('metrics', () => this.adjustConcurrency());
    }
  }
  
  addTask(prompt, options = {}) {
    const taskId = Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    const priority = options.priority || 5; // 1 = mais alta, 10 = mais baixa
    
    const task = {
      id: taskId,
      prompt,
      options,
      priority,
      status: 'queued',
      timestamp: Date.now()
    };
    
    return new Promise((resolve, reject) => {
      // Adicionar callbacks
      task.resolve = resolve;
      task.reject = reject;
      
      // Adicionar à fila
      this.taskQueue.enqueue(task, priority);
      
      // Atualizar métricas
      this.monitorService.updateTaskMetrics({
        queued: this.taskQueue.size,
        active: this.activeTasksCount
      });
      
      // Notificar
      this.emit('taskAdded', {
        taskId,
        priority,
        queueSize: this.taskQueue.size
      });
      
      // Tentar processar imediatamente
      setImmediate(() => this.processQueue());
    });
  }
  
  async processQueue() {
    // Verificar se podemos processar mais tarefas
    if (this.activeTasksCount >= this.maxConcurrentTasks || this.taskQueue.isEmpty()) {
      return;
    }
    
    // Verificar disponibilidade de recursos
    if (this.adaptiveConcurrency) {
      const resourceStatus = this.monitorService.canAcceptMoreTasks();
      if (!resourceStatus.canAccept) {
        console.log('Recursos insuficientes, pausando processamento');
        return;
      }
    }
    
    // Obter próxima tarefa
    const task = this.taskQueue.dequeue();
    this.activeTasksCount++;
    
    // Atualizar status
    task.status = 'processing';
    task.startTime = Date.now();
    
    // Atualizar métricas
    this.monitorService.updateTaskMetrics({
      queued: this.taskQueue.size,
      active: this.activeTasksCount
    });
    
    // Notificar
    this.emit('taskStarted', {
      taskId: task.id,
      activeTasksCount: this.activeTasksCount
    });
    
    try {
      // Processar tarefa
      const result = await this.claudeService.processPrompt(task.prompt, task.options);
      
      // Atualizar status
      task.status = 'completed';
      task.endTime = Date.now();
      task.duration = task.endTime - task.startTime;
      task.result = result;
      
      // Adicionar ao histórico
      this.addToCompletedHistory(task);
      
      // Resolver promise
      task.resolve(result);
      
      // Notificar
      this.emit('taskCompleted', {
        taskId: task.id,
        duration: task.duration
      });
    } catch (error) {
      // Atualizar status
      task.status = 'failed';
      task.endTime = Date.now();
      task.duration = task.endTime - task.startTime;
      task.error = error.message;
      
      // Adicionar ao histórico
      this.addToFailedHistory(task);
      
      // Rejeitar promise
      task.reject(error);
      
      // Notificar
      this.emit('taskFailed', {
        taskId: task.id,
        error: error.message
      });
    } finally {
      // Diminuir contador
      this.activeTasksCount--;
      
      // Atualizar métricas
      this.monitorService.updateTaskMetrics({
        queued: this.taskQueue.size,
        active: this.activeTasksCount,
        completed: this.completedTasks.length,
        failed: this.failedTasks.length
      });
      
      // Processar próxima tarefa
      setImmediate(() => this.processQueue());
    }
  }
  
  addToCompletedHistory(task) {
    // Remover detalhes para economizar memória
    const historyItem = {
      id: task.id,
      prompt: task.prompt.substring(0, 100) + '...',
      priority: task.priority,
      startTime: task.startTime,
      endTime: task.endTime,
      duration: task.duration,
      usage: task.result.usage
    };
    
    this.completedTasks.unshift(historyItem);
    
    // Limitar tamanho
    if (this.completedTasks.length > this.maxHistorySize) {
      this.completedTasks.pop();
    }
  }
  
  addToFailedHistory(task) {
    // Remover detalhes para economizar memória
    const historyItem = {
      id: task.id,
      prompt: task.prompt.substring(0, 100) + '...',
      priority: task.priority,
      startTime: task.startTime,
      endTime: task.endTime,
      duration: task.duration,
      error: task.error
    };
    
    this.failedTasks.unshift(historyItem);
    
    // Limitar tamanho
    if (this.failedTasks.length > this.maxHistorySize) {
      this.failedTasks.pop();
    }
  }
  
  adjustConcurrency() {
    if (!this.adaptiveConcurrency) return;
    
    const resourceStatus = this.monitorService.canAcceptMoreTasks();
    const newConcurrency = Math.max(
      1,
      Math.min(20, Math.ceil(resourceStatus.recommendedBatch))
    );
    
    if (newConcurrency !== this.maxConcurrentTasks) {
      console.log(`Ajustando concorrência de ${this.maxConcurrentTasks} para ${newConcurrency}`);
      this.maxConcurrentTasks = newConcurrency;
      
      // Se aumentou a concorrência, tentar processar mais tarefas
      if (newConcurrency > this.activeTasksCount) {
        setImmediate(() => this.processQueue());
      }
    }
  }
  
  getStats() {
    return {
      queued: this.taskQueue.size,
      active: this.activeTasksCount,
      maxConcurrent: this.maxConcurrentTasks,
      completed: this.completedTasks.length,
      failed: this.failedTasks.length,
      recentTasks: {
        completed: this.completedTasks.slice(0, 10),
        failed: this.failedTasks.slice(0, 10)
      }
    };
  }
}

module.exports = TaskManager;
```

### 8. Aplicação principal (index.js)

```javascript
require('dotenv').config();
const express = require('express');
const path = require('path');
const WorkerPool = require('./workers/workerPool');
const MonitorService = require('./monitorService');
const ClaudeService = require('./claudeService');
const TaskManager = require('./taskManager');

// Configurar serviços
const monitorService = new MonitorService({
  interval: 5000,
  highCpuThreshold: 0.7,
  lowCpuThreshold: 0.3
});

const workerPool = new WorkerPool({
  workerScript: path.resolve(__dirname, './workers/worker.js'),
  minWorkers: 2,
  maxWorkers: 15
});

const claudeService = new ClaudeService(workerPool, {
  defaultModel: 'claude-3-opus-20240229'
});

const taskManager = new TaskManager(claudeService, monitorService, {
  maxConcurrentTasks: 5,
  adaptiveConcurrency: true
});

// Iniciar monitoramento
monitorService.start();

// Configurar API
const app = express();
app.use(express.json());

// API para submeter tarefas
app.post('/api/tasks', async (req, res) => {
  try {
    const { prompt, priority = 5, options = {} } = req.body;
    
    if (!prompt) {
      return res.status(400).json({ error: 'Prompt é obrigatório' });
    }
    
    // Adicionar tarefa
    const result = await taskManager.addTask(prompt, { 
      priority: parseInt(priority, 10), 
      ...options 
    });
    
    res.json({
      success: true,
      content: result.content,
      usage: result.usage,
      processingTime: result.processingTime
    });
  } catch (error) {
    console.error('Erro ao processar tarefa:', error);
    res.status(500).json({ error: error.message });
  }
});

// API para verificar status
app.get('/api/status', (req, res) => {
  const stats = {
    taskManager: taskManager.getStats(),
    workerPool: workerPool.getStats(),
    claudeService: claudeService.getStats(),
    system: monitorService.getMetrics()
  };
  
  res.json(stats);
});

// Iniciar servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor iniciado na porta ${PORT}`);
});

// Tratamento de encerramento
process.on('SIGINT', async () => {
  console.log('Encerrando aplicação graciosamente...');
  
  monitorService.stop();
  
  // Dar tempo para concluir tarefas em andamento
  setTimeout(() => {
    process.exit(0);
  }, 5000);
});
```

## Considerações finais

Ambas as implementações oferecem soluções robustas para executar múltiplas instâncias do Claude Code em Node.js com controle de recursos. A escolha entre PM2 e uma solução customizada depende das necessidades específicas do projeto:

1. **Use PM2 quando:**
   - Precisar de uma solução pronta para produção rapidamente
   - Equipe tiver experiência limitada com desenvolvimento de sistemas concorrentes
   - Aplicação precisar de integração fácil com sistemas de monitoramento existentes

2. **Use solução customizada quando:**
   - Necessitar de controle granular sobre comportamento do sistema
   - Precisar de lógica de priorização complexa
   - Requisitos específicos de integração com Claude Code
   - Equipe tiver experiência com worker threads e controle de concorrência

Independentemente da abordagem escolhida, lembre-se de:

- Monitorar métricas críticas de CPU, memória e Event Loop
- Implementar thresholds dinâmicos baseados na carga do sistema
- Usar estratégias de backoff exponencial para falhas
- Incluir mecanismos de recuperação automática
- Manter logs detalhados para depuração

Ambas as implementações são adaptativas, escalando automaticamente o número de tarefas em execução com base na disponibilidade de recursos, garantindo estabilidade e eficiência mesmo com variações na carga de trabalho.