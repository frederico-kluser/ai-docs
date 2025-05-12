# Guia Completo do Claude Code: Controle, Integração e Configuração

O Claude Code é uma ferramenta de codificação baseada em IA que opera diretamente no terminal, lançada em fevereiro de 2025 pela Anthropic junto com o modelo Claude 3.7 Sonnet. Este guia aborda todos os aspectos solicitados sobre sua execução via Node.js, captura de dados em tempo real, flags disponíveis e técnicas avançadas.

## Execução do Claude Code via Node.js

O Claude Code pode ser executado via Node.js de várias maneiras eficientes, sem depender apenas do terminal:

### Instalação via NPM

```bash
npm install -g @anthropic-ai/claude-code
```

### Método 1: Execução via Child Process

```javascript
const { spawn, exec } = require('child_process');

// Função para executar Claude Code e obter resultado
function runClaudeCode(command) {
  return new Promise((resolve, reject) => {
    const claudeProcess = spawn('claude', [command], {
      shell: true,
      stdio: 'pipe'
    });
    
    let output = '';
    claudeProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    claudeProcess.stderr.on('data', (data) => {
      console.error(`Claude Code error: ${data}`);
    });
    
    claudeProcess.on('close', (code) => {
      if (code === 0) {
        resolve(output);
      } else {
        reject(new Error(`Claude Code process exited with code ${code}`));
      }
    });
  });
}

// Exemplo de uso
async function main() {
  try {
    const result = await runClaudeCode('explain the authentication.js file');
    console.log('Claude Code output:', result);
  } catch (error) {
    console.error('Error running Claude Code:', error);
  }
}

main();
```

### Método 2: Uso Programático do Pacote Claude Code

```javascript
const claudeCode = require('@anthropic-ai/claude-code');

async function main() {
  try {
    // Inicializa Claude Code
    await claudeCode.initialize();
    
    // Envia comando para Claude Code
    const response = await claudeCode.executeCommand('explain the authentication.js file');
    
    console.log('Claude Code response:', response);
  } catch (error) {
    console.error('Error using Claude Code:', error);
  }
}

main();
```

### Método 3: Sessão Interativa em Aplicação Node.js

```javascript
const { spawn } = require('child_process');
const readline = require('readline');

function startInteractiveClaudeSession() {
  // Inicia Claude Code em modo interativo
  const claude = spawn('claude', [], {
    stdio: ['pipe', process.stdout, process.stderr]
  });

  // Interface para leitura de input do usuário
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: 'You: '
  });

  // Encaminha input do usuário para Claude Code
  rl.prompt();
  rl.on('line', (line) => {
    if (line.toLowerCase() === 'exit') {
      claude.kill();
      rl.close();
      return;
    }
    
    claude.stdin.write(line + '\n');
    rl.prompt();
  });

  // Lida com a saída do Claude Code
  claude.on('close', (code) => {
    console.log(`Claude Code exited with code ${code}`);
    rl.close();
  });
}

startInteractiveClaudeSession();
```

## Técnicas para Captura de Dados/Outputs em Tempo Real

### 1. Mecanismos de Pipe

O Claude Code suporta mecanismos padrão de pipe Unix para capturar e redirecionar saídas:

```bash
# Pipe da saída para outro comando
claude "explain this function" | grep "important"

# Redirecionamento para arquivo
claude "generate a test for this function" > test_output.txt
```

Para automação mais confiável, o modo headless é preferível:

```bash
# Uso básico do modo headless com prompt
claude -p "explain this function" --output-format stream-json

# Pipe do conteúdo do arquivo para Claude e captura da saída
cat myfile.js | claude -p "explain this code" > explanation.md
```

### 2. Streaming via Server-Sent Events (SSE)

#### Implementação em Node.js:

```javascript
import { Anthropic } from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function streamResponse() {
  const stream = await anthropic.messages.stream({
    model: 'claude-3-7-sonnet-20250219',
    max_tokens: 1024,
    messages: [
      { role: 'user', content: 'Analyze this code snippet: [code]' }
    ],
  });

  // Processa o stream em tempo real
  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta') {
      process.stdout.write(chunk.delta.text);
      // Opcionalmente processa ou armazena os chunks
      // processChunk(chunk.delta.text);
    }
  }
}

streamResponse();
```

### 3. Comunicação Inter-Processo (IPC)

#### Model Context Protocol (MCP)

Um dos métodos mais poderosos para IPC com Claude Code é através do Model Context Protocol (MCP):

```javascript
// Exemplo de implementação de servidor MCP para interagir com Claude Code
import { createServer } from '@anthropic-ai/mcp';

// Cria um servidor MCP para interagir com Claude Code
const server = createServer({
  name: 'custom-data-processor',
  version: '1.0.0',
  tools: [
    {
      name: 'process_data',
      description: 'Process data and return results',
      execute: async (params) => {
        // Processa dados e retorna resultados
        const result = processData(params.data);
        return { result };
      },
    },
  ],
});

// Começa a ouvir conexões do Claude Code
server.listen(3000);
```

Configuração do Claude Code para conectar ao servidor MCP:

```bash
# Adiciona o servidor MCP ao Claude Code
claude mcp add custom-processor http://localhost:3000

# Usa a ferramenta em uma conversa
claude "process this data using the custom-processor"
```

### 4. Arquitetura Orientada a Eventos

```javascript
// Usando Node.js EventEmitter
import { EventEmitter } from 'events';
import { exec } from 'child_process';

class ClaudeCodeHandler extends EventEmitter {
  runClaudeCode(prompt) {
    const claudeProcess = exec(`claude -p "${prompt}" --output-format stream-json`);
    
    claudeProcess.stdout.on('data', (data) => {
      this.emit('output', data.toString());
    });
    
    claudeProcess.stderr.on('data', (data) => {
      this.emit('error', data.toString());
    });
    
    claudeProcess.on('close', (code) => {
      this.emit('complete', code);
    });
  }
}

// Uso
const handler = new ClaudeCodeHandler();

handler.on('output', (chunk) => {
  console.log('Received output:', chunk);
  // Processa ou armazena a saída
});

handler.on('error', (error) => {
  console.error('Error:', error);
});

handler.on('complete', (code) => {
  console.log('Process complete with code:', code);
});

handler.runClaudeCode('Explain this function and suggest improvements');
```

## Lista Completa de Flags, Configurações e Argumentos

### Flags de Modo de Impressão

| Flag | Descrição | Exemplo |
|------|-------------|---------| 
| `-p, --print` | Habilita modo não-interativo, permitindo pipe de entrada/saída para uso programático | `claude -p "Explain this code"` |
| `--output-format` | Especifica o formato de saída no modo de impressão (text, json, stream-json) | `claude -p --output-format json "Fix bugs"` |
| `--verbose` | Inclui transcrição completa da conversa na saída JSON (deve ser usado com --output-format json ou stream-json) | `claude -p --verbose --output-format json "Debug this"` |

### Flags de Controle de Sessão

| Flag | Descrição | Exemplo |
|------|-------------|---------| 
| `--continue` | Continua automaticamente a conversa mais recente | `claude --continue` |
| `--resume` | Mostra um seletor de conversas para escolher uma sessão específica para retomar | `claude --resume` |
| `--resume <session-id>` | Retoma uma sessão específica por ID | `claude --resume abc123 "Continue work"` |
| `--max-turns <number>` | Limita o número de turnos de agente no modo não-interativo | `claude -p --max-turns 5 "Fix bugs"` |

### Flags MCP (Model Context Protocol)

| Flag | Descrição | Exemplo |
|------|-------------|---------| 
| `--mcp-debug` | Habilita depuração para conexões de servidor MCP | `claude --mcp-debug` |
| `-e, --env <KEY=value>` | Define variáveis de ambiente para a sessão | `claude -e API_KEY=123` |
| `--permission-prompt-tool <tool>` | Especifica uma ferramenta MCP para lidar com solicitações de permissão no modo não-interativo | `claude -p --permission-prompt-tool mcp_auth_tool "Create a file"` |
| `--dangerously-skip-permissions` | Ignora todas as verificações de permissão (use com cautela em ambientes controlados) | `claude --dangerously-skip-permissions` |

### Flags de Segurança e Permissões

| Flag | Descrição | Exemplo |
|------|-------------|---------| 
| `--allowedTools` | Especifica permissões específicas da sessão para ferramentas | `claude --allowedTools` |
| `--allowed-domains` | Especifica domínios que podem ser acessados sem solicitar permissão | `claude --allowed-domains github.com,example.com` |

### Flags Diversas

| Flag | Descrição | Exemplo |
|------|-------------|---------| 
| `--help, -h` | Exibe informações de ajuda sobre comandos e flags disponíveis | `claude --help` |
| `--version` | Exibe a versão atual do Claude Code | `claude --version` |

### Formatos de Saída

Quando usando a flag `--output-format` com o modo de impressão (`-p`), três formatos são suportados:

1. **Text (padrão)**: Exibe apenas o texto da resposta final
   ```bash
   claude -p "Explain this function"
   ```

2. **JSON**: Retorna um objeto JSON com metadados e a resposta
   ```bash
   claude -p --output-format json "Explain how to use JSON output"
   ```
   Exemplo de saída:
   ```json
   {
     "cost_usd": 0.003,
     "duration_ms": 1234,
     "duration_api_ms": 800,
     "result": "The response text here...",
     "session_id": "abc123"
   }
   ```

3. **Stream JSON**: Exibe objetos JSON em tempo real conforme as mensagens são recebidas
   ```bash
   claude -p --output-format stream-json "Create a Python script"
   ```

### Comandos MCP

O Claude Code pode ser usado para gerenciar servidores Model Context Protocol (MCP):

```bash
# Adiciona um servidor de escopo local (padrão)
claude mcp add my-private-server /path/to/server

# Especifica explicitamente escopo local
claude mcp add my-private-server -s local /path/to/server

# Adiciona um servidor de escopo de projeto
claude mcp add shared-server -s project /path/to/server

# Adiciona um servidor SSE
claude mcp add --transport sse sse-server https://example.com/sse-endpoint

# Lista todos os servidores configurados
claude mcp list

# Obtém detalhes de um servidor específico
claude mcp get my-server

# Remove um servidor
claude mcp remove my-server
```

### Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-------------|---------| 
| `MCP_TIMEOUT` | Configura o timeout de inicialização do servidor MCP (em milissegundos) | `MCP_TIMEOUT=10000 claude` |
| `ANTHROPIC_API_KEY` | Sua chave de API Anthropic (geralmente definida durante a configuração) | `export ANTHROPIC_API_KEY=your_key_here` |

## Técnicas Avançadas com Claude Code 3.7

### Controle de Modo de Pensamento Flexível

O Claude Code 3.7 introduz um sistema sofisticado de controle de modo de pensamento que permite aos desenvolvedores especificar quão profundamente Claude deve pensar antes de responder:

- **Modo padrão**: Modo padrão para respostas rápidas
- **Modo de pensamento estendido**: Acionado por palavras-chave específicas:
  - `think` (aloca 4.000 tokens)
  - `think hard` (aloca mais tokens)
  - `think harder` (aloca ainda mais tokens)
  - `ultrathink` (aloca até 31.999 tokens)

### Fluxos de Trabalho de Comando Especializados

Desenvolvedores experientes usam as capacidades de comando do Claude Code para criar fluxos de trabalho reutilizáveis:

- **Comandos slash personalizados**: Armazenados no diretório `.claude/commands/` e acessíveis através do menu slash (`/`)
- **Templates parametrizados**: Comandos podem incluir o placeholder `$ARGUMENTS` para entradas dinâmicas
- **Compactação de sessão**: Comando `/compact` para liberar espaço na janela de contexto para bases de código maiores
- **Conhecimento específico do projeto**: Mantido em arquivos CLAUDE.md para compartilhamento em equipe

### Análise Profunda de Base de Código

O Claude Code vai além da simples assistência de código com:

- **Raciocínio multi-arquivo**: Compreensão contextual em bases de código inteiras
- **Análise de arquitetura**: Entendimento do design geral do sistema e interações de componentes
- **Mapeamento de dependências**: Rastreamento de dependências e compreensão de relações de bibliotecas
- **Estratégias de refatoração**: Desenvolvimento de planos abrangentes de refatoração baseados em padrões da base de código

## APIs e Interfaces Programáticas

### 1. Modo Headless CLI

O método oficial mais direto para controle programático do Claude Code é através do seu modo headless:

- **Formato do comando**: `claude -p "<prompt>" [options]`
- **Formatos de saída**:
  - Padrão (texto simples): `claude -p "Generate a Python function that..."`
  - JSON: `claude -p --output-format json "Generate a Python function that..."`
  - Streaming JSON: `claude -p --output-format stream-json "Generate a Python function that..."`

### 2. Gerenciamento de Sessão

O Claude Code fornece flags CLI para gerenciar sessões programaticamente:
- **Continuar sessão anterior**: `claude --continue` (continua automaticamente a sessão mais recente)
- **Retomar sessão específica**: `claude --resume <session_id> "Resume prompt"`
- **Modo não-interativo com sessão anterior**: `claude --continue --print "Continue working on..."`

### 3. AgentAPI (Interface HTTP Não-Oficial)

[AgentAPI](https://github.com/coder/agentapi) é uma ferramenta popular de terceiros que fornece uma interface de API HTTP para controlar o Claude Code:

- **Configuração**: `agentapi server -- claude [--allowedTools "..."]`
- **Endpoints HTTP**:
  - `GET /messages` - Lista todas as mensagens de conversação
  - `POST /message` - Envia uma mensagem para o Claude Code
  - `GET /status` - Obtém o status atual (stable/running)
  - `GET /events` - Stream SSE de eventos do agente

Exemplo de uso:
```bash
curl -X POST localhost:3284/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Generate a React component", "type": "user"}'
```

### 4. Model Context Protocol (MCP)

O Claude Code pode integrar-se com o Model Context Protocol (MCP) da Anthropic, que fornece uma maneira padronizada de estender capacidades:

```javascript
// Exemplo de implementação de servidor MCP que pode interagir com Claude Code
import { createServer } from '@anthropic-ai/mcp';

// Cria um servidor MCP para interagir com Claude Code
const server = createServer({
  name: 'custom-data-processor',
  version: '1.0.0',
  tools: [
    {
      name: 'process_data',
      description: 'Process data and return results',
      execute: async (params) => {
        // Processa dados e retorna resultados
        const result = processData(params.data);
        return { result };
      },
    },
  ],
});

// Começa a ouvir conexões do Claude Code
server.listen(3000);
```

## Métodos para Intercomunicação entre Claude Code e Aplicações Node.js

### 1. Integração Direta de API

O SDK oficial JavaScript da Anthropic (`@anthropic-ai/sdk`) fornece uma interface robusta para aplicações Node.js se comunicarem com modelos Claude:

```javascript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env['ANTHROPIC_API_KEY'],
});

async function generateCode(prompt) {
  const message = await client.messages.create({
    max_tokens: 4096,
    messages: [{ role: 'user', content: prompt }],
    model: 'claude-3-7-sonnet-20250219',
  });
  
  return message.content[0].text;
}
```

### 2. Padrão de Event Emitter

```javascript
const EventEmitter = require('events');
const claudeEvents = new EventEmitter();

// Na sua aplicação Node.js
claudeEvents.on('code-review-requested', async (data) => {
  const review = await runClaudeCode(`Review this code: ${data.code}`);
  claudeEvents.emit('code-review-completed', review);
});

// Dispara eventos de diferentes partes da sua aplicação
claudeEvents.emit('code-review-requested', { code: 'function sum(a, b) { return a + b; }' });
```

### 3. WebSockets para Comunicação em Tempo Real

```javascript
const WebSocket = require('ws');
const server = new WebSocket.Server({ port: 8080 });

server.on('connection', (socket) => {
  socket.on('message', async (message) => {
    const data = JSON.parse(message);
    
    if (data.type === 'claude-request') {
      const response = await runClaudeCode(data.prompt);
      socket.send(JSON.stringify({
        type: 'claude-response',
        data: response
      }));
    }
  });
});
```

### 4. Sistemas de Passagem de Mensagens

Redis Pub/Sub para Sistemas Distribuídos:

```javascript
const Redis = require('ioredis');
const publisher = new Redis();
const subscriber = new Redis();

// Inscreve-se para tarefas do Claude Code
subscriber.subscribe('claude-tasks');
subscriber.on('message', async (channel, message) => {
  const task = JSON.parse(message);
  const result = await runClaudeCode(task.prompt);
  
  // Publica o resultado de volta
  publisher.publish('claude-results', JSON.stringify({
    id: task.id,
    result
  }));
});

// Submete uma tarefa
function submitClaudeTask(prompt) {
  const taskId = generateUniqueId();
  publisher.publish('claude-tasks', JSON.stringify({
    id: taskId,
    prompt
  }));
  return taskId;
}
```

## Conclusão

O Claude Code oferece uma ampla gama de capacidades para integração com Node.js, captura de dados em tempo real e controle programático. Através das técnicas, flags, e métodos de intercomunicação descritos neste guia, desenvolvedores podem criar fluxos de trabalho sofisticados que integram o Claude Code em seus aplicativos e pipelines de desenvolvimento.

As principais forças do Claude Code incluem sua arquitetura baseada em terminal que facilita a automação, capacidades de raciocínio profundo com modos de pensamento personalizáveis, e várias opções para integração com ambientes Node.js. Seja usando processos filho simples, a API Anthropic direta, ou protocolos mais avançados como MCP, há múltiplas maneiras de aproveitar o Claude Code em aplicações Node.js modernas.