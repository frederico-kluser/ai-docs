# Executando LLMs Locais em Electron.js com Distribuição de Modelos Empacotados

**node-llama-cpp rodando no UtilityProcess do Electron com modelos distribuídos via extraResources é a arquitetura de produção ideal.** Essa combinação oferece velocidade de inferência nativa (14-150 tokens/seg dependendo do hardware), aceleração automática de GPU (CUDA, Metal, Vulkan) e distribuição confiável multiplataforma. Para Qwen3, use o modelo 4B ou 8B com quantização Q4_K_M—isso equilibra retenção de qualidade acima de 95% com arquivos de 5-6GB que cabem em GPUs de consumo.

O insight arquitetural crítico: **nunca execute inferência no processo principal**. A API UtilityProcess do Electron fornece isolamento de processo, IPC Mojo para streaming eficiente e acesso completo ao Node.js—exatamente o que a inferência de LLM requer. Empacote um modelo inicial pequeno (~600MB) para capacidade offline enquanto baixa modelos maiores na primeira execução.

---

## Comparação de runtimes revela um vencedor claro

Após avaliar seis opções de runtime, **node-llama-cpp** se destaca como a escolha pronta para produção em aplicações Electron. A biblioteca (v3.14.x no final de 2025) fornece binários pré-compilados para todas as principais plataformas, detecção automática de GPU e suporte nativo a streaming.

| Runtime | Integração | Performance | Suporte GPU | Manutenção | Pronto p/ Produção |
|---------|------------|-------------|-------------|------------|---------------------|
| **node-llama-cpp** | Fácil (2/5) | Velocidade nativa | CUDA/Metal/Vulkan | ✅ Muito ativo | ✅ Sim |
| WebLLM | Moderada (3/5) | 80-85% nativo | WebGPU | ✅ Ativo | ⚠️ Médio |
| transformers.js | Fácil (2/5) | Variável | WebGPU/WASM | ✅ Ativo | ✅ Para modelos menores |
| Ollama | Mais fácil (1/5) | Nativa (overhead IPC) | CUDA/Metal/ROCm | ✅ Ativo | ✅ Sim |
| llamafile | Moderada (3/5) | Velocidade nativa | CUDA/Metal/Vulkan | ✅ Ativo | ⚠️ Médio |
| llama-node | N/A | Apenas CPU | ❌ Nenhum | ❌ Abandonado | ❌ Não |

**Vantagens do node-llama-cpp**: Binários pré-compilados eliminam dores de cabeça com compilação. A função `getLlama()` detecta automaticamente backends de GPU disponíveis—sem configuração manual necessária. Streaming funciona através de iteradores assíncronos que se integram naturalmente com IPC do Electron. O pacote experimental **@electron/llm** dos mantenedores do Electron usa node-llama-cpp internamente, validando esta como a abordagem recomendada.

**Quando considerar alternativas**: Use **Ollama** se preferir a simplicidade de API REST e não se importar em empacotar seu binário (~2GB). Considere **WebLLM** para arquiteturas web-first que requerem compatibilidade com navegador—ele atinge 80-85% da performance nativa através de kernels WebGPU otimizados.

---

## Seleção de modelo Qwen3 para deploy em desktop

A linha de modelos Qwen3 varia de 0.6B a 235B parâmetros. Para apps Electron desktop, **Qwen3-4B e Qwen3-8B** atingem o ponto ideal entre capacidade e requisitos de recursos.

| Modelo | Tamanho Q4_K_M | VRAM Mín | VRAM Recomendada | RAM (só CPU) |
|--------|----------------|----------|------------------|--------------|
| Qwen3-0.6B | ~0.4 GB | 2 GB | 4 GB | 4 GB |
| Qwen3-1.7B | ~1.1 GB | 4 GB | 6 GB | 8 GB |
| **Qwen3-4B** | **2.5 GB** | **4 GB** | **6 GB** | **8 GB** |
| **Qwen3-8B** | **5.0 GB** | **6 GB** | **8 GB** | **16 GB** |
| Qwen3-14B | 9.0 GB | 12 GB | 16 GB | 24 GB |
| Qwen3-32B | 19.8 GB | 24 GB | 32 GB | 48 GB |

**Recomendação de quantização**: Q4_K_M oferece o melhor custo-benefício—**retenção de qualidade acima de 95%** com a velocidade de inferência mais rápida e menor tamanho de arquivo. Use Q8_0 apenas para aplicações críticas de qualidade como assistência em código onde precisão de sintaxe importa. As variantes K-quant (Q4_K_M, Q5_K_M) usam precisão adaptativa por bloco, superando quantizações uniformes mais antigas.

Arquivos GGUF oficiais estão disponíveis em `Qwen/Qwen3-*-GGUF` no Hugging Face. Para opções de quantização estendidas incluindo variantes IQ e Q2_K, use os repositórios `unsloth/Qwen3-*-GGUF`.

---

## O padrão de arquitetura UtilityProcess

A API **UtilityProcess** do Electron é feita sob medida para operações intensivas de CPU como inferência de LLM. Diferente de worker threads, utility processes rodam em instâncias V8 completamente separadas com IPC Mojo do Chromium para streaming binário eficiente.

```
┌─────────────────────────────────────────────────────────────┐
│                    PROCESSO RENDERER                         │
│    UI React/Vue → window.llmAPI (contextBridge)             │
└─────────────────────────────│────────────────────────────────┘
                              │ MessagePort (streaming direto)
┌─────────────────────────────▼────────────────────────────────┐
│                     PROCESSO PRINCIPAL                       │
│    Cria UtilityProcess, roteia MessagePorts                 │
└─────────────────────────────│────────────────────────────────┘
                              │ MessagePort
┌─────────────────────────────▼────────────────────────────────┐
│                    UTILITY PROCESS                           │
│    node-llama-cpp carrega modelo GGUF via mmap              │
│    Executa inferência em GPU/CPU, faz streaming de tokens   │
│    Flags: --max-old-space-size=8192                         │
└──────────────────────────────────────────────────────────────┘
```

**Por que não o processo principal?** Trabalho intensivo de CPU no main bloqueia todos os processos renderer, causando a temida "bolinha giratória" no macOS e UI congelada em todas as plataformas. O utility process pode crashar sem afetar o resto do app.

**Por que não worker threads?** Worker threads compartilham o espaço de memória e instância V8 do processo principal. Addons nativos projetados para ambientes single-threaded podem conflitar. Utility processes fornecem isolamento real.

---

## Guia de implementação com código funcional

### Setup do projeto e dependências

```bash
npm init -y
npm install electron node-llama-cpp
npm install --save-dev @electron/rebuild electron-builder
```

```json
{
  "main": "src/main.js",
  "type": "module",
  "scripts": {
    "start": "electron .",
    "rebuild": "electron-rebuild",
    "build": "electron-builder"
  }
}
```

### Instalação de bindings nativos

node-llama-cpp já vem com binários pré-compilados para a maioria das configurações. Após instalar, reconstrua para a versão Node do Electron:

```bash
npx electron-rebuild -w node-llama-cpp
```

Verifique suporte a GPU:
```bash
npx --no node-llama-cpp inspect gpu
```

### Setup do processo principal (src/main.js)

```javascript
import { app, BrowserWindow, utilityProcess, MessageChannelMain, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
let llmProcess;
let mainWindow;

function getModelPath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, 'models', 'qwen3-4b-q4_k_m.gguf');
  }
  return path.join(__dirname, '..', 'models', 'qwen3-4b-q4_k_m.gguf');
}

app.whenReady().then(() => {
  // Spawna utility process para inferência LLM
  llmProcess = utilityProcess.fork(path.join(__dirname, 'llm-worker.js'), [], {
    serviceName: 'LLM Inference',
    execArgv: ['--max-old-space-size=8192']
  });

  // Inicializa modelo quando processo spawna
  llmProcess.on('spawn', () => {
    llmProcess.postMessage({ type: 'init', modelPath: getModelPath() });
  });

  createWindow();
});

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  mainWindow.loadFile('src/index.html');
}

// Cria canal MessagePort para comunicação direta renderer-utility
ipcMain.handle('llm:get-channel', (event) => {
  const { port1, port2 } = new MessageChannelMain();
  llmProcess.postMessage({ type: 'new-client' }, [port1]);
  event.sender.postMessage('llm:port', null, [port2]);
});
```

### Worker do utility process (src/llm-worker.js)

```javascript
import { getLlama, LlamaChatSession } from 'node-llama-cpp';

let llama, model, context;

process.parentPort.on('message', async (e) => {
  const { type, modelPath } = e.data;
  const [port] = e.ports;

  if (type === 'init') {
    try {
      llama = await getLlama(); // Detecta GPU automaticamente
      model = await llama.loadModel({ 
        modelPath,
        gpuLayers: 99 // Transfere todas as camadas para GPU
      });
      context = await model.createContext({
        contextSize: 8192,
        flashAttention: true,
        batchSize: 512
      });
      process.parentPort.postMessage({ type: 'ready' });
    } catch (error) {
      process.parentPort.postMessage({ type: 'error', error: error.message });
    }
  }

  if (type === 'new-client' && port) {
    handleClientConnection(port);
  }
});

function handleClientConnection(port) {
  port.on('message', async (event) => {
    const { type, prompt, requestId } = event.data;

    if (type === 'prompt') {
      try {
        const session = new LlamaChatSession({ 
          contextSequence: context.getSequence() 
        });
        
        // Faz streaming de tokens de volta através do MessagePort
        for await (const token of session.promptStream(prompt)) {
          port.postMessage({ type: 'token', requestId, content: token });
        }
        port.postMessage({ type: 'done', requestId });
      } catch (error) {
        port.postMessage({ type: 'error', requestId, error: error.message });
      }
    }
  });

  port.start();
}
```

### Script preload seguro (src/preload.js)

```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('llmAPI', {
  connect: () => new Promise((resolve) => {
    ipcRenderer.invoke('llm:get-channel');
    ipcRenderer.once('llm:port', (event) => {
      const port = event.ports[0];
      port.start();

      resolve({
        prompt: (text) => {
          const requestId = crypto.randomUUID();
          return new ReadableStream({
            start(controller) {
              port.postMessage({ type: 'prompt', prompt: text, requestId });
              
              const handler = (e) => {
                if (e.data.requestId !== requestId) return;
                if (e.data.type === 'token') {
                  controller.enqueue(e.data.content);
                } else if (e.data.type === 'done') {
                  controller.close();
                  port.removeEventListener('message', handler);
                } else if (e.data.type === 'error') {
                  controller.error(new Error(e.data.error));
                  port.removeEventListener('message', handler);
                }
              };
              port.addEventListener('message', handler);
            }
          });
        }
      });
    });
  })
});
```

### Uso no renderer (src/renderer.js)

```javascript
const llm = await window.llmAPI.connect();
const stream = llm.prompt('Explique computação quântica em termos simples');

const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  document.getElementById('output').textContent += value;
}
```

---

## Configuração de empacotamento para modelos de vários GB

O insight principal: **arquivos ASAR não conseguem lidar eficientemente com arquivos de modelo de vários GB**. Use `extraResources` para colocar modelos fora do arquivo onde podem ser mapeados em memória diretamente.

### electron-builder.yml completo

```yaml
appId: com.example.llm-desktop
productName: LLM Desktop

# ASAR para código fonte, mas desempacota módulos nativos
asar: true
asarUnpack:
  - "node_modules/**/*.node"
  - "node_modules/**/build/Release/*.node"

# Modelos e binários nativos fora do ASAR
extraResources:
  # Modelo inicial empacotado
  - from: "models/starter"
    to: "models"
    filter:
      - "*.gguf"
  
  # Binários nativos específicos da plataforma
  - from: "native/${os}/${arch}"
    to: "native"
    filter:
      - "**/*"
      - "!*.pdb"
      - "!*.dSYM/**"

files:
  - "dist/**/*"
  - "package.json"
  - "!native/**"
  - "!models/**"

# macOS com suporte para Apple Silicon e Intel
mac:
  category: public.app-category.developer-tools
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
  target:
    - target: dmg
      arch: [x64, arm64]
    - target: zip
      arch: [x64, arm64]
  # Assina binários nativos empacotados
  binaries:
    - Contents/Resources/native/**/*

# Windows
win:
  target:
    - target: nsis
      arch: [x64]
  sign: ./scripts/sign-windows.js

nsis:
  oneClick: false
  perMachine: true
  allowToChangeInstallationDirectory: true
  differentialPackage: false  # Desativa delta updates para apps grandes

# Linux
linux:
  target:
    - AppImage
    - deb
  category: Development

# Notarização
afterSign: scripts/notarize.js

# Auto-update (separado de updates de modelo)
publish:
  provider: github
  owner: sua-org
  repo: seu-app
```

### Entitlements macOS para inferência LLM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```

### Estratégia de distribuição recomendada

**Empacote um modelo inicial pequeno** (~600MB TinyLlama ou Qwen3-0.6B) para funcionalidade offline imediata. Baixe modelos maiores na primeira execução:

```javascript
// Resolução híbrida de modelo
function getModelPath() {
  const userModels = path.join(app.getPath('userData'), 'models');
  const largeModel = path.join(userModels, 'qwen3-8b-q4_k_m.gguf');
  
  if (fs.existsSync(largeModel)) return largeModel;
  
  // Fallback para modelo inicial empacotado
  return path.join(process.resourcesPath, 'models', 'qwen3-0.6b-q4_k_m.gguf');
}
```

Esta abordagem mantém o tamanho do instalador abaixo de 1GB enquanto habilita capacidade completa após download.

---

## Otimização de performance entrega melhorias de 2-5x

Aceleração de hardware é a otimização de maior impacto. Offload completo para GPU transforma geração de tokens de **2-5 t/s (CPU)** para **14-150 t/s (GPU)** dependendo do hardware.

### Dados de benchmark por hardware

| Hardware | Processamento de Prompt | Geração de Tokens |
|----------|-------------------------|-------------------|
| M1 MacBook Pro | 266 t/s | 36 t/s |
| M3 Max MacBook Pro | 760 t/s | 66 t/s |
| M4 Max MacBook Pro | 886 t/s | 83 t/s |
| RTX 3080 | 780-900 t/s | 70-80 t/s |
| RTX 4090 | 1400-1800 t/s | 130-150 t/s |
| Apenas CPU (Intel/AMD moderno) | 15-35 t/s | 8-18 t/s |

**Geração de tokens é limitada por bandwidth de memória**, não por computação. Isso explica por que chips da série M com memória unificada frequentemente igualam GPUs dedicadas—eles têm excelente proporção de bandwidth de memória para pesos.

### Checklist de otimizações de alto impacto

1. **Habilitar aceleração GPU** (+200-500%): `gpuLayers: 99` transfere todas as camadas
2. **Habilitar Flash Attention** (+5-15%): `flashAttention: true` reduz memória do KV cache
3. **Usar quantização Q4_K_M** (+40-60% vs F16): Inferência mais rápida com excelente qualidade
4. **Quantizar KV cache** (+10-20% capacidade de contexto): `--cache-type-k q8_0`
5. **Ajustar contagem de threads**: Use 1-2 threads quando GPU lida com inferência; contagem de núcleos físicos para apenas CPU

### Configuração ideal para GPUs NVIDIA

```javascript
const llama = await getLlama();
const model = await llama.loadModel({
  modelPath: 'qwen3-8b-q4_k_m.gguf',
  gpuLayers: 99
});

const context = await model.createContext({
  contextSize: 8192,
  flashAttention: true,
  batchSize: 512,
  threads: 2  // Baixa contagem de threads com GPU
});
```

### Configuração ideal para Apple Silicon

```javascript
const context = await model.createContext({
  contextSize: 'auto',  // Maximiza baseado na memória unificada
  flashAttention: true,
  threads: 6  // Apenas núcleos de performance físicos
});
```

---

## Limitações conhecidas e soluções práticas

### Compatibilidade de addon nativo

**Problema**: node-llama-cpp requer ABI Node.js correspondente à versão Node do Electron.

**Solução**: Sempre execute `npx electron-rebuild` após instalar. Para CI/CD:
```bash
npx electron-rebuild -v 31.0.0 -a x64 -w node-llama-cpp
```

### Assinatura de código Windows e SmartScreen

**Problema**: Certificados EV não fornecem mais reputação SmartScreen instantânea (mudou em março de 2024).

**Solução**: Use **Azure Trusted Signing** para organizações nos EUA/Canadá, ou aceite que reputação se constrói ao longo do tempo com volume de downloads.

### Notarização macOS com binários nativos

**Problema**: Arquivos `.node` não assinados e binários externos causam falhas de notarização.

**Solução**: Use `asarUnpack` para arquivos `.node` (auto-assinados) e array `mac.binaries` para executáveis externos.

### Atualizações de modelos grandes

**Problema**: Updates diferenciais do electron-updater não funcionam efetivamente para arquivos binários de modelo.

**Solução**: Gerencie atualizações de modelo separadamente das atualizações do app. Armazene modelos baixados pelo usuário em `app.getPath('userData')` e implemente um gerenciador de modelos com suporte a retomada.

### WebGPU no Electron (para WebLLM)

**Problema**: WebGPU requer habilitação explícita em algumas versões do Electron.

**Solução**:
```javascript
app.commandLine.appendSwitch('enable-unsafe-webgpu');
// Linux adicionalmente precisa de:
app.commandLine.appendSwitch('enable-features', 'Vulkan,VulkanFromANGLE');
```

---

## Quando considerar arquiteturas alternativas

A arquitetura node-llama-cpp + UtilityProcess é ideal para a maioria dos casos, mas alternativas fazem sentido em cenários específicos:

- **Subprocesso Ollama**: Quando você quer UI de gerenciamento de modelos, acesso a biblioteca de modelos e simplicidade de API REST. Trade-off: +2GB para binário Ollama, leve overhead de IPC.

- **Modo servidor local**: Para aplicações que precisam de múltiplos usuários simultâneos ou arquitetura de microsserviços. Execute servidor llama.cpp como subprocesso, comunique via HTTP.

- **WebLLM/WebGPU**: Para aplicações web-first onde compatibilidade com navegador importa mais que performance máxima. Atinge 80-85% da velocidade nativa.

- **Híbrido cloud**: Quando tamanho do modelo excede recursos locais. Execute modelo pequeno localmente para respostas rápidas, roteie queries complexas para API cloud. Implemente com lógica de fallback baseada em complexidade do prompt.

- **Distribuição llamafile**: Para máxima portabilidade com zero dependências. Executável único roda em seis sistemas operacionais. Melhor para ferramentas distribuídas para usuários não-técnicos que não podem instalar dependências.

---

## Conclusão

Construir um app Electron de produção com inferência LLM empacotada agora é prático graças aos **bindings maduros do node-llama-cpp** e à **API UtilityProcess do Electron**. A combinação vencedora: Qwen3-4B ou 8B com quantização Q4_K_M, rodando em um utility process isolado, com modelos distribuídos via extraResources. Isso entrega velocidade de inferência nativa em todas as plataformas mantendo o modelo de desenvolvimento familiar do Electron.

Para novos projetos, comece com o pacote experimental @electron/llm como implementação de referência, depois customize conforme necessário. A estratégia de empacotamento híbrido—modelo pequeno empacotado, modelos grandes baixados—mantém tamanhos de instalador razoáveis enquanto fornece capacidade offline completa. Foque esforços de otimização em aceleração GPU primeiro; todo o resto fornece ganhos incrementais comparado à melhoria de 5-10x da utilização adequada de hardware.
