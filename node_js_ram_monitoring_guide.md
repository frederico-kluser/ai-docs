# Monitoring RAM em Node.js: guia definitivo para performance e estabilidade

O monitoramento e gerenciamento de memória RAM é crucial para aplicações Node.js de longa execução, especialmente em produção. Este relatório apresenta métodos eficazes para monitorar e otimizar o consumo de memória em aplicações Node.js, com foco especial em soluções multiplataforma e otimizações para macOS, priorizando versões modernas do Node.js (v20+) com suporte nativo para TypeScript.

## Bibliotecas e APIs: as melhores opções para monitoramento

A escolha da ferramenta certa para monitoramento de RAM pode definir o sucesso da sua estratégia de gerenciamento de memória. Após análise detalhada das opções disponíveis nos últimos três anos, identificamos as soluções mais eficazes, balanceando precisão, overhead e compatibilidade.

### APIs nativas do Node.js

O Node.js oferece ferramentas nativas poderosas que servem como base para qualquer estratégia de monitoramento:

```typescript
// Monitoramento básico com process.memoryUsage()
function monitorarMemoria(): void {
  const memUsage = process.memoryUsage();
  console.log({
    rss: `${Math.round(memUsage.rss / 1024 / 1024)} MB`,        // Memória total alocada
    heapTotal: `${Math.round(memUsage.heapTotal / 1024 / 1024)} MB`, // Total do heap
    heapUsed: `${Math.round(memUsage.heapUsed / 1024 / 1024)} MB`,  // Memória realmente usada
    external: `${Math.round(memUsage.external / 1024 / 1024)} MB`,  // Memória C++
    arrayBuffers: `${Math.round(memUsage.arrayBuffers / 1024 / 1024)} MB` // Buffers
  });
}

// Estatísticas detalhadas do V8
import * as v8 from 'v8';

function monitorHeap(): void {
  const stats = v8.getHeapStatistics();
  console.log({
    totalHeapSize: `${stats.total_heap_size / 1024 / 1024} MB`,
    usedHeapSize: `${stats.used_heap_size / 1024 / 1024} MB`,
    heapSizeLimit: `${stats.heap_size_limit / 1024 / 1024} MB`
    // Outras métricas disponíveis...
  });
}
```

**Vantagens**: Zero dependências externas, overhead mínimo, compatibilidade garantida com todas as versões do Node.js, incluindo v20+, e suporte completo para TypeScript.

**Limitações**: Métricas básicas sem visualizações ou análises avançadas, requer implementação manual de lógica para rastreamento ao longo do tempo.

### prom-client para monitoramento em produção

Para aplicações de produção, o `prom-client` emerge como solução líder, oferecendo integração com o ecossistema Prometheus:

```typescript
// Exemplo com TypeScript e Express
import express from 'express';
import * as client from 'prom-client';

const app = express();
const register = new client.Registry();
register.setDefaultLabels({ app: 'minha-aplicacao-nodejs' });

// Coletar métricas padrão do Node.js
client.collectDefaultMetrics({ register });

// Métrica personalizada para monitorar heap
const heapSizeGauge = new client.Gauge({
  name: 'node_heap_size_used_bytes',
  help: 'Heap size usado pela aplicação em bytes',
  collect() {
    this.set(process.memoryUsage().heapUsed);
  }
});
register.registerMetric(heapSizeGauge);

// Endpoint para o Prometheus coletar métricas
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.send(await register.metrics());
});
```

**Vantagens**: Suporte completo para TypeScript e Node.js v20+, baixo overhead, integração com Prometheus/Grafana para visualizações avançadas e alertas, manutenção ativa com atualizações recentes.

### Ferramentas de diagnóstico: Clinic.js

Para análise detalhada durante desenvolvimento e diagnóstico de problemas:

```typescript
// Uso com TypeScript
import ClinicHeapProfiler from '@clinic/heap-profiler';

const heapProfiler = new ClinicHeapProfiler();
heapProfiler.collect(['node', './seu-script.js'], function (err, filepath) {
  if (err) throw err;
  heapProfiler.visualize(filepath, filepath + '.html', function (err) {
    if (err) throw err;
    console.log(`Relatório gerado em ${filepath}.html`);
  });
});
```

**Vantagens**: Visualizações detalhadas do uso de memória, suporte para Node.js v20+, ideal para diagnóstico de vazamentos de memória.

## Detecção de picos: implementando sistemas de alerta eficientes

A capacidade de detectar anomalias no consumo de memória antes que causem problemas é essencial para aplicações estáveis. Existem duas abordagens principais para definição de limiares:

### Limiares estáticos vs. dinâmicos

**Limiares estáticos**: Valores predefinidos que, quando ultrapassados, disparam alertas.

```typescript
class StaticThresholdMemoryWatcher implements MemoryWatcher {
  private thresholdBytes: number;
  private checkIntervalMs: number;
  private intervalId: NodeJS.Timeout | null = null;
  private handlers: Array<(usage: NodeJS.MemoryUsage) => void> = [];

  constructor(thresholdMB: number, checkIntervalMs = 5000) {
    this.thresholdBytes = thresholdMB * 1024 * 1024;
    this.checkIntervalMs = checkIntervalMs;
  }

  start(): void {
    if (this.intervalId) return;
    
    this.intervalId = setInterval(() => {
      const memoryUsage = process.memoryUsage();
      
      if (memoryUsage.heapUsed > this.thresholdBytes) {
        this.handlers.forEach(handler => handler(memoryUsage));
      }
    }, this.checkIntervalMs);
  }

  // Outros métodos...
}
```

**Limiares dinâmicos**: Adaptam-se automaticamente aos padrões de uso de memória, usando técnicas estatísticas:

```typescript
class DynamicThresholdMemoryWatcher implements MemoryWatcher {
  private memoryHistory: number[] = [];
  private readonly historySize: number;
  private readonly deviationFactor: number;

  constructor(historySize = 10, deviationFactor = 2.0, checkIntervalMs = 5000) {
    this.historySize = historySize;
    this.deviationFactor = deviationFactor;
    // Inicialização...
  }

  start(): void {
    this.intervalId = setInterval(() => {
      const memoryUsage = process.memoryUsage();
      const currentHeapUsed = memoryUsage.heapUsed;
      
      // Atualiza histórico e calcula estatísticas
      this.memoryHistory.push(currentHeapUsed);
      if (this.memoryHistory.length > this.historySize) {
        this.memoryHistory.shift();
      }
      
      if (this.memoryHistory.length < this.historySize) return;
      
      // Calcula média e desvio padrão
      const mean = this.calculateMean(this.memoryHistory);
      const stdDev = this.calculateStdDev(this.memoryHistory, mean);
      
      // Define limiar dinâmico baseado nas estatísticas
      const threshold = mean + (stdDev * this.deviationFactor);
      
      if (currentHeapUsed > threshold) {
        this.handlers.forEach(handler => handler(memoryUsage, threshold));
      }
    }, this.checkIntervalMs);
  }

  // Implementação dos métodos de cálculo...
}
```

Os **limiares dinâmicos** são preferíveis para a maioria das aplicações com carga variável, pois adaptam-se ao comportamento normal da aplicação e reduzem falsos positivos.

### Polling vs. event-driven

**Polling**: Verificações periódicas do uso de memória em intervalos predefinidos:

```typescript
function startMemoryPolling(intervalMs: number, thresholdMB: number): void {
  const thresholdBytes = thresholdMB * 1024 * 1024;
  
  setInterval(() => {
    const memUsage = process.memoryUsage();
    if (memUsage.heapUsed > thresholdBytes) {
      console.warn('ALERTA: Consumo de memória acima do limiar!');
      // Lógica de alerta
    }
  }, intervalMs);
}
```

**Event-driven**: Responde a eventos específicos do sistema, como coletas de lixo:

```typescript
import { PerformanceObserver } from 'node:perf_hooks';

const obs = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  entries.forEach((entry) => {
    // Observar eventos de GC pode ajudar a identificar
    // padrões problemáticos nas coletas de lixo
    console.log(`GC: ${entry.kind === 1 ? 'Minor' : 'Major'}, Duração: ${entry.duration.toFixed(2)}ms`);
    
    // Verificar memória após GC para identificar vazamentos
    const memoryUsage = process.memoryUsage();
    if (memoryUsage.heapUsed > THRESHOLD) {
      // Lógica de alerta
    }
  });
});

obs.observe({ entryTypes: ['gc'] });
```

### Análise estatística para identificar anomalias

Para diferenciar entre uso normal e anômalo de memória, as técnicas estatísticas oferecem a melhor precisão:

```typescript
class StatisticalMemoryWatcher {
  private readonly memoryReadings: number[] = [];
  private readonly maxReadings: number;
  private readonly outlierThreshold: number;

  constructor(maxReadings = 60, outlierThreshold = 3.0) {
    this.maxReadings = maxReadings;
    this.outlierThreshold = outlierThreshold;
  }

  addReading(heapUsedBytes: number): boolean {
    this.memoryReadings.push(heapUsedBytes);
    
    if (this.memoryReadings.length > this.maxReadings) {
      this.memoryReadings.shift();
    }
    
    if (this.memoryReadings.length < 10) return false;
    
    // Calcular estatísticas para detectar outliers
    const mean = this.memoryReadings.reduce((sum, val) => sum + val, 0) / this.memoryReadings.length;
    const variance = this.memoryReadings.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / this.memoryReadings.length;
    const stdDev = Math.sqrt(variance);
    
    // Z-score para determinar se é anomalia
    const currentReading = this.memoryReadings[this.memoryReadings.length - 1];
    const zScore = Math.abs((currentReading - mean) / stdDev);
    
    return zScore > this.outlierThreshold;
  }
}
```

**Análise de tendências** para detectar vazamentos de memória graduais:

```typescript
class TrendAnalysisMemoryWatcher {
  // ... inicialização

  private detectAbnormalGrowthRate(): boolean {
    // Normalizar tempos para valores em minutos
    const points = this.memoryReadings.map(reading => ({
      x: (reading.timestamp - this.firstTimestamp) / 60000,
      y: reading.bytes
    }));
    
    // Cálculos para regressão linear
    // ... cálculos de sumX, sumY, etc.
    
    // Calcular inclinação da reta (taxa de crescimento)
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    
    // Taxa de crescimento relativa ao valor médio
    const avgMemory = sumY / n;
    const growthRatePerMinute = slope / avgMemory;
    
    // Se a taxa exceder o limiar, é considerado anômalo
    return growthRatePerMinute > this.growthRateThreshold;
  }
}
```

## Otimização de memória: liberando recursos não utilizados

A otimização e liberação de memória não utilizada são fundamentais para manter aplicações Node.js executando de forma eficiente, especialmente em ambientes de longa duração.

### Forçando o garbage collector (global.gc())

Uma das técnicas mais diretas para liberar memória é forçar o garbage collector:

```typescript
// Executar Node.js com a flag --expose-gc
// node --expose-gc script.js

if (global.gc) {
  console.log("Memória antes da GC:", process.memoryUsage().heapUsed / 1024 / 1024, "MB");
  global.gc();
  console.log("Memória após a GC:", process.memoryUsage().heapUsed / 1024 / 1024, "MB");
}
```

**Importante**: Forçar o GC frequentemente pode afetar negativamente a performance. Use esta técnica apenas em momentos estratégicos, como após operações que manipulam grandes quantidades de dados.

### Estratégias para processamento de dados grandes com streams

Em vez de carregar grandes conjuntos de dados na memória, utilize streams:

```typescript
import fs from 'fs';

// Abordagem eficiente usando streams
function processarArquivoEficiente(arquivo: string): Promise<number> {
  return new Promise((resolve, reject) => {
    let total = 0;
    const stream = fs.createReadStream(arquivo, { encoding: 'utf8' });
    let restante = '';
    
    stream.on('data', (chunk: string) => {
      const linhas = (restante + chunk).split('\n');
      restante = linhas.pop() || '';
      
      for (const linha of linhas) {
        total += parseInt(linha, 10) || 0;
      }
    });
    
    stream.on('end', () => {
      if (restante) {
        total += parseInt(restante, 10) || 0;
      }
      resolve(total);
    });
    
    stream.on('error', reject);
  });
}
```

### Buffer pools para reduzir alocações repetitivas

Implementar pool de buffers para reutilizar recursos e evitar alocações frequentes:

```typescript
class BufferPool {
  private pool: Buffer[] = [];
  private readonly bufferSize: number;
  private readonly maxBuffers: number;
  
  constructor(bufferSize: number = 8192, maxBuffers: number = 100) {
    this.bufferSize = bufferSize;
    this.maxBuffers = maxBuffers;
  }
  
  getBuffer(): Buffer {
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }
    return Buffer.allocUnsafe(this.bufferSize);
  }
  
  releaseBuffer(buffer: Buffer): void {
    if (buffer.length !== this.bufferSize) return;
    
    if (this.pool.length < this.maxBuffers) {
      buffer.fill(0); // Limpar para prevenir vazamento de dados
      this.pool.push(buffer);
    }
  }
}
```

### WeakRef e FinalizationRegistry para recursos externos

Para Node.js v14+ e TypeScript com ES2021+, utilize WeakRef e FinalizationRegistry para gerenciar recursos externos:

```typescript
class ResourceManager {
  private registry = new FinalizationRegistry((resource: { close: () => void }) => {
    try {
      resource.close();
      console.log('Recurso liberado pelo garbage collector');
    } catch (err) {
      console.error('Erro ao fechar recurso:', err);
    }
  });
  
  private resources = new Set<{ resource: any, ref: WeakRef<any> }>();
  
  registerResource<T extends { close: () => void }>(resource: T, owner: object): T {
    const ref = new WeakRef(owner);
    this.resources.add({ resource, ref });
    this.registry.register(owner, resource);
    return resource;
  }
  
  cleanup(): void {
    for (const entry of this.resources) {
      const owner = entry.ref.deref();
      if (!owner) {
        try {
          entry.resource.close();
          this.resources.delete(entry);
        } catch (err) {
          console.error('Erro ao fechar recurso:', err);
        }
      }
    }
  }
}
```

### Detecção e mitigação de memory leaks

Classe para detectar vazamentos de memória:

```typescript
class MemoryLeakDetector {
  private snapshots: { timestamp: number, usage: NodeJS.MemoryUsage }[] = [];
  private readonly interval: NodeJS.Timeout;
  private readonly threshold: number; // em MB
  
  constructor(intervalMs: number = 60000, thresholdMB: number = 10) {
    this.threshold = thresholdMB;
    this.interval = setInterval(() => this.takeSnapshot(), intervalMs);
  }
  
  private takeSnapshot(): void {
    const usage = process.memoryUsage();
    const timestamp = Date.now();
    this.snapshots.push({ timestamp, usage });
    
    // Manter apenas as últimas 60 snapshots
    if (this.snapshots.length > 60) {
      this.snapshots.shift();
    }
    
    this.analyzeGrowth();
  }
  
  private analyzeGrowth(): void {
    if (this.snapshots.length < 5) return;
    
    const first = this.snapshots[0];
    const last = this.snapshots[this.snapshots.length - 1];
    
    // Calcular taxa de crescimento por hora
    const heapGrowthMB = (last.usage.heapUsed - first.usage.heapUsed) / (1024 * 1024);
    const timeDiffMinutes = (last.timestamp - first.timestamp) / (1000 * 60);
    const growthRatePerHour = (heapGrowthMB / timeDiffMinutes) * 60;
    
    if (growthRatePerHour > this.threshold) {
      console.warn(`[ALERTA] Possível memory leak detectado: ${growthRatePerHour.toFixed(2)} MB/hora`);
      this.dumpMemoryProfile();
    }
  }
  
  async dumpMemoryProfile(): Promise<void> {
    // Implementação para salvar perfil de memória
  }
}
```

## Otimizações específicas para macOS

O macOS possui características específicas de gerenciamento de memória que precisam ser consideradas.

### Comportamento de compressão de memória no macOS

O macOS comprime páginas de memória não utilizadas ativamente, o que pode fazer com que o Node.js reporte alto uso de RSS mesmo sem vazamentos reais. Monitorar a memória no macOS requer compreender este comportamento:

```typescript
import os from 'os';

function monitorarMemoriaMacOS() {
  const memoriaTotal = os.totalmem() / 1024 / 1024; // MB
  const memoriaLivre = os.freemem() / 1024 / 1024;  // MB
  const memoriaUsada = memoriaTotal - memoriaLivre;
  
  console.log(`Memória total: ${memoriaTotal.toFixed(2)} MB`);
  console.log(`Memória livre: ${memoriaLivre.toFixed(2)} MB`);
  console.log(`Memória usada: ${memoriaUsada.toFixed(2)} MB`);
  console.log(`Percentual usado: ${((memoriaUsada / memoriaTotal) * 100).toFixed(2)}%`);
}
```

### Otimização para Apple Silicon (M1/M2/M3)

Para obter o melhor desempenho em chips Apple Silicon:

```bash
# Usar a versão correta do Node.js para o chip M1/M2/M3
nvm install 20
nvm use 20

# Aumentar o limite de heap para aplicações em M1/M2/M3
node --max-old-space-size=4096 seu-script.js
```

### Configurações de heapBaseSize e otimização específica

Para ambientes macOS, considere ajustar as configurações do V8:

```bash
# Otimização para usar menos memória
node --optimize-for-size --max-old-space-size=2048 app.js

# Aumentar o tamanho do "new space" para reduzir frequência de GC
node --max-semi-space-size=128 app.js

# Configuração equilibrada para macOS com 8GB+ de RAM
node --max-old-space-size=4096 --max-semi-space-size=64 app.js
```

## Arquitetura de sistema completo de monitoramento

Com base nas pesquisas realizadas, recomendamos uma arquitetura de três camadas para monitoramento e otimização de RAM:

### 1. Camada interna (na aplicação)

```typescript
// monitor-memory.ts
import { PerformanceObserver } from 'node:perf_hooks';
import EventEmitter from 'events';

export class MemoryMonitor extends EventEmitter {
  private readonly pollingIntervalMs: number;
  private readonly heapThresholdMB: number;
  private readonly growthThresholdMBPerHour: number;
  private pollingInterval: NodeJS.Timer | null = null;
  private memoryHistory: Array<{timestamp: number, heap: number}> = [];
  private gcObserver: PerformanceObserver | null = null;
  
  constructor(options: {
    pollingIntervalMs?: number,
    heapThresholdMB?: number,
    growthThresholdMBPerHour?: number,
    enableGCMonitoring?: boolean
  } = {}) {
    super();
    this.pollingIntervalMs = options.pollingIntervalMs || 60000; // 1 minuto
    this.heapThresholdMB = options.heapThresholdMB || 0; // 0 = desativado
    this.growthThresholdMBPerHour = options.growthThresholdMBPerHour || 10; // 10MB/hora
    
    if (options.enableGCMonitoring) {
      this.setupGCMonitoring();
    }
  }
  
  start(): this {
    if (this.pollingInterval) return this;
    
    this.pollingInterval = setInterval(() => {
      this.checkMemory();
    }, this.pollingIntervalMs);
    
    return this;
  }
  
  stop(): this {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
    
    if (this.gcObserver) {
      this.gcObserver.disconnect();
      this.gcObserver = null;
    }
    
    return this;
  }
  
  private checkMemory(): void {
    const memUsage = process.memoryUsage();
    const heapUsedMB = memUsage.heapUsed / 1024 / 1024;
    const timestamp = Date.now();
    
    // Emitir evento com dados atuais
    this.emit('memory', { 
      timestamp,
      heap: {
        used: heapUsedMB,
        total: memUsage.heapTotal / 1024 / 1024,
        percentage: (memUsage.heapUsed / memUsage.heapTotal) * 100
      },
      rss: memUsage.rss / 1024 / 1024,
      external: memUsage.external / 1024 / 1024,
      arrayBuffers: memUsage.arrayBuffers ? memUsage.arrayBuffers / 1024 / 1024 : 0
    });
    
    // Verificar limiar de heap
    if (this.heapThresholdMB > 0 && heapUsedMB > this.heapThresholdMB) {
      this.emit('threshold-exceeded', { 
        current: heapUsedMB, 
        threshold: this.heapThresholdMB 
      });
    }
    
    // Atualizar histórico para detecção de crescimento
    this.memoryHistory.push({ timestamp, heap: heapUsedMB });
    
    // Manter apenas 60 pontos no histórico (1 hora se intervalo = 1 min)
    if (this.memoryHistory.length > 60) {
      this.memoryHistory.shift();
    }
    
    // Analisar tendência de crescimento
    this.analyzeGrowthTrend();
  }
  
  private analyzeGrowthTrend(): void {
    if (this.memoryHistory.length < 10) return; // Precisa de dados suficientes
    
    const oldest = this.memoryHistory[0];
    const newest = this.memoryHistory[this.memoryHistory.length - 1];
    
    const heapGrowthMB = newest.heap - oldest.heap;
    const timeDiffHours = (newest.timestamp - oldest.timestamp) / (1000 * 60 * 60);
    
    // Taxa de crescimento por hora
    const growthRateMBPerHour = heapGrowthMB / timeDiffHours;
    
    if (growthRateMBPerHour > this.growthThresholdMBPerHour) {
      this.emit('growth-rate-exceeded', {
        rate: growthRateMBPerHour,
        threshold: this.growthThresholdMBPerHour,
        period: { start: oldest.timestamp, end: newest.timestamp }
      });
    }
  }
  
  private setupGCMonitoring(): void {
    try {
      this.gcObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          this.emit('gc', {
            kind: entry.kind === 1 ? 'minor' : 'major',
            duration: entry.duration,
            startTime: entry.startTime
          });
          
          // Verificar memória após GC
          this.checkMemory();
        });
      });
      
      this.gcObserver.observe({ entryTypes: ['gc'] });
    } catch (e) {
      console.warn('GC monitoring not available:', e);
    }
  }
  
  // Método para forçar GC (requer --expose-gc)
  forceGC(): boolean {
    if (global.gc) {
      global.gc();
      return true;
    }
    return false;
  }
}
```

### 2. Camada de exportação (métricas e integração)

```typescript
// metrics-exporter.ts
import express from 'express';
import * as client from 'prom-client';
import { MemoryMonitor } from './monitor-memory';

export class MetricsExporter {
  private readonly app: express.Application;
  private readonly port: number;
  private readonly register: client.Registry;
  private server: ReturnType<express.Application['listen']> | null = null;
  
  // Métricas do Prometheus
  private heapGauge: client.Gauge<string>;
  private heapTotalGauge: client.Gauge<string>;
  private rssGauge: client.Gauge<string>;
  private gcDurationHistogram: client.Histogram<string>;
  private memoryGrowthGauge: client.Gauge<string>;
  
  constructor(
    private readonly memoryMonitor: MemoryMonitor,
    options: { port?: number, prefix?: string } = {}
  ) {
    this.app = express();
    this.port = options.port || 9090;
    const metricPrefix = options.prefix || 'nodejs_app';
    
    // Criar registro do Prometheus
    this.register = new client.Registry();
    
    // Definir métricas
    this.heapGauge = new client.Gauge({
      name: `${metricPrefix}_heap_used_bytes`,
      help: 'Memory used in the heap in bytes',
      registers: [this.register]
    });
    
    this.heapTotalGauge = new client.Gauge({
      name: `${metricPrefix}_heap_total_bytes`,
      help: 'Total heap size in bytes',
      registers: [this.register]
    });
    
    this.rssGauge = new client.Gauge({
      name: `${metricPrefix}_rss_bytes`,
      help: 'RSS (Resident Set Size) in bytes',
      registers: [this.register]
    });
    
    this.gcDurationHistogram = new client.Histogram({
      name: `${metricPrefix}_gc_duration_seconds`,
      help: 'Duration of GC operations in seconds',
      labelNames: ['kind'],
      buckets: [0.001, 0.01, 0.1, 0.5, 1, 2, 5],
      registers: [this.register]
    });
    
    this.memoryGrowthGauge = new client.Gauge({
      name: `${metricPrefix}_memory_growth_mb_per_hour`,
      help: 'Memory growth rate in MB per hour',
      registers: [this.register]
    });
    
    // Configurar endpoints
    this.setupEndpoints();
    this.setupEventListeners();
  }
  
  private setupEndpoints(): void {
    // Endpoint para métricas do Prometheus
    this.app.get('/metrics', async (_req, res) => {
      res.set('Content-Type', this.register.contentType);
      res.send(await this.register.metrics());
    });
    
    // Endpoint para informações de memória atual
    this.app.get('/memory', (_req, res) => {
      const memUsage = process.memoryUsage();
      res.json({
        heap: {
          used: memUsage.heapUsed / 1024 / 1024,
          total: memUsage.heapTotal / 1024 / 1024,
          percentage: (memUsage.heapUsed / memUsage.heapTotal) * 100
        },
        rss: memUsage.rss / 1024 / 1024,
        external: memUsage.external / 1024 / 1024,
        arrayBuffers: memUsage.arrayBuffers ? memUsage.arrayBuffers / 1024 / 1024 : 0
      });
    });
    
    // Endpoint para forçar GC (apenas com --expose-gc)
    this.app.post('/gc', (_req, res) => {
      const success = this.memoryMonitor.forceGC();
      if (success) {
        res.status(200).json({ success: true, message: 'Garbage collection executed' });
      } else {
        res.status(400).json({ 
          success: false, 
          message: 'Garbage collection not available. Run with --expose-gc flag.' 
        });
      }
    });
  }
  
  private setupEventListeners(): void {
    // Atualizar métricas quando o monitor emitir eventos
    this.memoryMonitor.on('memory', (data) => {
      this.heapGauge.set(data.heap.used * 1024 * 1024);
      this.heapTotalGauge.set(data.heap.total * 1024 * 1024);
      this.rssGauge.set(data.rss * 1024 * 1024);
    });
    
    this.memoryMonitor.on('gc', (data) => {
      this.gcDurationHistogram.observe({ kind: data.kind }, data.duration / 1000);
    });
    
    this.memoryMonitor.on('growth-rate-exceeded', (data) => {
      this.memoryGrowthGauge.set(data.rate);
    });
  }
  
  start(): this {
    if (this.server) return this;
    
    this.server = this.app.listen(this.port, () => {
      console.log(`Metrics server running at http://localhost:${this.port}`);
    });
    
    return this;
  }
  
  stop(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.server) {
        resolve();
        return;
      }
      
      this.server.close((err) => {
        if (err) reject(err);
        else {
          this.server = null;
          resolve();
        }
      });
    });
  }
}
```

### 3. Camada de diagnóstico e ação automatizada

```typescript
// memory-optimizer.ts
import { MemoryMonitor } from './monitor-memory';
import fs from 'fs';
import { promisify } from 'util';
import path from 'path';

const writeFile = promisify(fs.writeFile);
const mkdir = promisify(fs.mkdir);

export class MemoryOptimizer {
  private lowMemoryActionExecuted: boolean = false;
  private readonly lowMemoryThresholdMB: number;
  private readonly criticalMemoryThresholdMB: number;
  private readonly heapDumpPath: string;
  
  constructor(
    private readonly memoryMonitor: MemoryMonitor,
    options: {
      lowMemoryThresholdMB?: number,
      criticalMemoryThresholdMB?: number,
      heapDumpPath?: string,
      autoOptimize?: boolean
    } = {}
  ) {
    this.lowMemoryThresholdMB = options.lowMemoryThresholdMB || 0; // 0 = desativado
    this.criticalMemoryThresholdMB = options.criticalMemoryThresholdMB || 0; // 0 = desativado
    this.heapDumpPath = options.heapDumpPath || './memory-dumps';
    
    if (options.autoOptimize) {
      this.setupAutoOptimization();
    }
  }
  
  private setupAutoOptimization(): void {
    // Monitorar eventos de memória
    this.memoryMonitor.on('memory', async (data) => {
      const heapUsedMB = data.heap.used;
      
      // Ações para limiar de memória baixa
      if (this.lowMemoryThresholdMB > 0 && 
          heapUsedMB > this.lowMemoryThresholdMB &&
          !this.lowMemoryActionExecuted) {
        await this.handleLowMemory(heapUsedMB);
      }
      
      // Ações para limiar de memória crítica
      if (this.criticalMemoryThresholdMB > 0 && 
          heapUsedMB > this.criticalMemoryThresholdMB) {
        await this.handleCriticalMemory(heapUsedMB);
      }
    });
    
    // Monitorar crescimento sustentado (possível vazamento)
    this.memoryMonitor.on('growth-rate-exceeded', async (data) => {
      await this.handleMemoryLeak(data.rate);
    });
  }
  
  async handleLowMemory(heapUsedMB: number): Promise<void> {
    console.warn(`[MEMORY] Low memory threshold reached: ${heapUsedMB.toFixed(2)}MB`);
    
    // Executar GC
    const gcSuccess = this.memoryMonitor.forceGC();
    if (gcSuccess) {
      console.log('[MEMORY] Executed garbage collection');
    }
    
    // Adicionar lógica para limpar caches internos, fechar conexões inativas, etc.
    
    this.lowMemoryActionExecuted = true;
    
    // Resetar flag após algum tempo para permitir novas ações se necessário
    setTimeout(() => {
      this.lowMemoryActionExecuted = false;
    }, 5 * 60 * 1000); // 5 minutos
  }
  
  async handleCriticalMemory(heapUsedMB: number): Promise<void> {
    console.error(`[MEMORY] CRITICAL memory level: ${heapUsedMB.toFixed(2)}MB`);
    
    // Criar dump de heap para análise
    await this.createHeapDump('critical');
    
    // Medidas extremas: forçar GC múltiplas vezes
    for (let i = 0; i < 3; i++) {
      this.memoryMonitor.forceGC();
    }
    
    // Lógica adicional para lidar com situação crítica
    // Por exemplo: fechar conexões, rejeitar novas requisições, etc.
  }
  
  async handleMemoryLeak(growthRateMBPerHour: number): Promise<void> {
    console.warn(`[MEMORY] Potential memory leak detected: ${growthRateMBPerHour.toFixed(2)}MB/hour`);
    
    // Criar dump de heap para análise posterior
    await this.createHeapDump('leak');
  }
  
  async createHeapDump(reason: string): Promise<string | null> {
    try {
      // Garantir que o diretório existe
      await mkdir(this.heapDumpPath, { recursive: true });
      
      const filename = `heap-${reason}-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
      const filepath = path.join(this.heapDumpPath, filename);
      
      // Node.js não tem API nativa para criar heap dumps programaticamente
      // Em uma implementação real, você usaria uma biblioteca como heapdump
      // ou v8-profiler-next
      
      // Aqui, estamos apenas salvando informações básicas de memória
      const memoryInfo = process.memoryUsage();
      await writeFile(filepath, JSON.stringify(memoryInfo, null, 2));
      
      console.log(`[MEMORY] Created memory snapshot: ${filepath}`);
      return filepath;
    } catch (error) {
      console.error('[MEMORY] Failed to create heap dump:', error);
      return null;
    }
  }
}
```

### Implementação do sistema completo

```typescript
// index.ts
import { MemoryMonitor } from './monitor-memory';
import { MetricsExporter } from './metrics-exporter';
import { MemoryOptimizer } from './memory-optimizer';

// Criar uma instância do monitor de memória
const memoryMonitor = new MemoryMonitor({
  pollingIntervalMs: 30000, // 30 segundos
  heapThresholdMB: 500,     // 500 MB
  growthThresholdMBPerHour: 10, // 10 MB/hora
  enableGCMonitoring: true
});

// Iniciar exportador de métricas
const metricsExporter = new MetricsExporter(memoryMonitor, {
  port: 9090,
  prefix: 'myapp'
});

// Configurar otimizador de memória
const memoryOptimizer = new MemoryOptimizer(memoryMonitor, {
  lowMemoryThresholdMB: 400,
  criticalMemoryThresholdMB: 600,
  heapDumpPath: './memory-dumps',
  autoOptimize: true
});

// Iniciar todos os componentes
memoryMonitor.start();
metricsExporter.start();

// Configurar monitoramento de memória para macOS
if (process.platform === 'darwin') {
  console.log('Detected macOS, applying platform-specific optimizations');
  // Aqui você poderia adicionar configurações específicas para macOS
}

// Graceful shutdown
process.once('SIGINT', async () => {
  console.log('Shutting down...');
  memoryMonitor.stop();
  await metricsExporter.stop();
  process.exit(0);
});
```

## Configurações para ambientes containerizados (Docker/Kubernetes)

Para ambientes containerizados, a otimização de memória é ainda mais crítica:

```dockerfile
FROM node:20-alpine

# Definir ambiente de produção
ENV NODE_ENV production

# Configurar limite de memória consistente com os recursos do container
ENV NODE_OPTIONS="--max-old-space-size=300 --max-semi-space-size=32"

WORKDIR /app

# Copiar apenas arquivos necessários (pequena imagem = menos RAM)
COPY package*.json ./
RUN npm ci --only=production

COPY dist/ ./dist/

# Usar usuário não-root
USER node

# Healthcheck para memória
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "dist/index.js"]
```

Em Kubernetes, configure recursos consistentes:

```yaml
# Kubernetes exemplo
resources:
  limits:
    memory: "512Mi"
  requests:
    memory: "256Mi"
env:
  - name: NODE_OPTIONS
    value: "--max-old-space-size=400"  # 80% do limite do contêiner
```

## Conclusão

O gerenciamento eficiente de memória em Node.js requer uma combinação de técnicas de monitoramento, detecção de anomalias e otimização. As abordagens nativas combinadas com ferramentas especializadas como prom-client oferecem a melhor solução para aplicações de produção.

Para o monitoramento, a análise estatística de uso de memória com detecção de anomalias proporciona a maior precisão na detecção precoce de problemas. Para otimização, o uso de streams, pools de objetos e estratégias cuidadosas de alocação de recursos são fundamentais para aplicações de longa duração.

O sistema de três camadas proposto (monitoramento interno, exportação de métricas e diagnóstico/otimização) oferece uma solução completa e robusta para gerenciar memória em aplicações Node.js modernas, garantindo estabilidade e performance mesmo sob carga intensa.