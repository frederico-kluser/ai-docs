# Running Local LLMs in Electron.js with Bundled Model Distribution

**node-llama-cpp running in Electron's UtilityProcess with models distributed via extraResources is the optimal production architecture.** This combination delivers native inference speed (14-150 tokens/sec depending on hardware), automatic GPU acceleration (CUDA, Metal, Vulkan), and reliable cross-platform distribution. For Qwen3, use the 4B or 8B model with Q4_K_M quantization—this balances 95%+ quality retention with 5-6GB file sizes that fit consumer GPUs.

The critical architectural insight: **never run inference in the main process**. Electron's UtilityProcess API provides process isolation, Mojo IPC for efficient streaming, and full Node.js access—exactly what LLM inference requires. Bundle a small starter model (~600MB) for offline capability while downloading larger models on first run.

---

## Runtime comparison reveals one clear winner

After evaluating six runtime options, **node-llama-cpp** stands out as the production-ready choice for Electron applications. The library (v3.14.x as of late 2025) provides pre-built binaries for all major platforms, automatic GPU detection, and native streaming support.

| Runtime | Integration | Performance | GPU Support | Maintenance | Production-Ready |
|---------|-------------|-------------|-------------|-------------|------------------|
| **node-llama-cpp** | Easy (2/5) | Native speed | CUDA/Metal/Vulkan | ✅ Very active | ✅ Yes |
| WebLLM | Moderate (3/5) | 80-85% native | WebGPU | ✅ Active | ⚠️ Medium |
| transformers.js | Easy (2/5) | Variable | WebGPU/WASM | ✅ Active | ✅ For smaller models |
| Ollama | Easiest (1/5) | Native (IPC overhead) | CUDA/Metal/ROCm | ✅ Active | ✅ Yes |
| llamafile | Moderate (3/5) | Native speed | CUDA/Metal/Vulkan | ✅ Active | ⚠️ Medium |
| llama-node | N/A | CPU only | ❌ None | ❌ Abandoned | ❌ No |

**node-llama-cpp advantages**: Pre-built binaries eliminate compilation headaches. The `getLlama()` function auto-detects available GPU backends—no manual configuration needed. Streaming works through async iterators that integrate naturally with Electron IPC. The experimental **@electron/llm** package from Electron maintainers uses node-llama-cpp internally, validating this as the recommended approach.

**When to consider alternatives**: Use **Ollama** if you prefer REST API simplicity and don't mind bundling its binary (~2GB). Consider **WebLLM** for web-first architectures requiring browser compatibility—it achieves 80-85% of native performance through optimized WebGPU kernels.

---

## Qwen3 model selection for desktop deployment

Qwen3's model lineup ranges from 0.6B to 235B parameters. For desktop Electron apps, **Qwen3-4B and Qwen3-8B** hit the sweet spot between capability and resource requirements.

| Model | Q4_K_M Size | Min VRAM | Recommended VRAM | RAM (CPU-only) |
|-------|-------------|----------|------------------|----------------|
| Qwen3-0.6B | ~0.4 GB | 2 GB | 4 GB | 4 GB |
| Qwen3-1.7B | ~1.1 GB | 4 GB | 6 GB | 8 GB |
| **Qwen3-4B** | **2.5 GB** | **4 GB** | **6 GB** | **8 GB** |
| **Qwen3-8B** | **5.0 GB** | **6 GB** | **8 GB** | **16 GB** |
| Qwen3-14B | 9.0 GB | 12 GB | 16 GB | 24 GB |
| Qwen3-32B | 19.8 GB | 24 GB | 32 GB | 48 GB |

**Quantization recommendation**: Q4_K_M provides the optimal tradeoff—**95%+ quality retention** with the fastest inference speed and smallest file size. Only use Q8_0 for quality-critical applications like coding assistance where syntax precision matters. The K-quant variants (Q4_K_M, Q5_K_M) use adaptive precision per block, outperforming older uniform quantization.

Official GGUF files are available from `Qwen/Qwen3-*-GGUF` on Hugging Face. For extended quantization options including IQ and Q2_K variants, use `unsloth/Qwen3-*-GGUF` repositories.

---

## The UtilityProcess architecture pattern

Electron's **UtilityProcess** API is purpose-built for CPU-intensive operations like LLM inference. Unlike worker threads, utility processes run in completely separate V8 instances with Chromium's Mojo IPC for efficient binary streaming.

```
┌─────────────────────────────────────────────────────────────┐
│                      RENDERER PROCESS                        │
│    React/Vue UI → window.llmAPI (contextBridge)             │
└─────────────────────────────│────────────────────────────────┘
                              │ MessagePort (direct streaming)
┌─────────────────────────────▼────────────────────────────────┐
│                       MAIN PROCESS                           │
│    Creates UtilityProcess, routes MessagePorts               │
└─────────────────────────────│────────────────────────────────┘
                              │ MessagePort
┌─────────────────────────────▼────────────────────────────────┐
│                    UTILITY PROCESS                           │
│    node-llama-cpp loads GGUF model via mmap                 │
│    Runs inference on GPU/CPU, streams tokens                 │
│    Flags: --max-old-space-size=8192                         │
└──────────────────────────────────────────────────────────────┘
```

**Why not the main process?** CPU-intensive work in main blocks all renderer processes, causing the dreaded "beachball" on macOS and frozen UI on all platforms. The utility process crashes without affecting the rest of the app.

**Why not worker threads?** Worker threads share the main process memory space and V8 instance. Native addons designed for single-threaded environments can conflict. Utility processes provide true isolation.

---

## Implementation guide with working code

### Project setup and dependencies

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

### Native binding installation

node-llama-cpp ships pre-built binaries for most configurations. After installing, rebuild for Electron's Node version:

```bash
npx electron-rebuild -w node-llama-cpp
```

Verify GPU support:
```bash
npx --no node-llama-cpp inspect gpu
```

### Main process setup (src/main.js)

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
  // Spawn utility process for LLM inference
  llmProcess = utilityProcess.fork(path.join(__dirname, 'llm-worker.js'), [], {
    serviceName: 'LLM Inference',
    execArgv: ['--max-old-space-size=8192']
  });

  // Initialize model once process spawns
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

// Create MessagePort channel for direct renderer-utility communication
ipcMain.handle('llm:get-channel', (event) => {
  const { port1, port2 } = new MessageChannelMain();
  llmProcess.postMessage({ type: 'new-client' }, [port1]);
  event.sender.postMessage('llm:port', null, [port2]);
});
```

### Utility process worker (src/llm-worker.js)

```javascript
import { getLlama, LlamaChatSession } from 'node-llama-cpp';

let llama, model, context;

process.parentPort.on('message', async (e) => {
  const { type, modelPath } = e.data;
  const [port] = e.ports;

  if (type === 'init') {
    try {
      llama = await getLlama(); // Auto-detects GPU
      model = await llama.loadModel({ 
        modelPath,
        gpuLayers: 99 // Offload all layers to GPU
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
        
        // Stream tokens back through MessagePort
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

### Secure preload script (src/preload.js)

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

### Renderer usage (src/renderer.js)

```javascript
const llm = await window.llmAPI.connect();
const stream = llm.prompt('Explain quantum computing in simple terms');

const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  document.getElementById('output').textContent += value;
}
```

---

## Bundling configuration for multi-GB models

The key insight: **ASAR archives cannot efficiently handle multi-GB model files**. Use `extraResources` to place models outside the archive where they can be memory-mapped directly.

### Complete electron-builder.yml

```yaml
appId: com.example.llm-desktop
productName: LLM Desktop

# ASAR for source code, but unpack native modules
asar: true
asarUnpack:
  - "node_modules/**/*.node"
  - "node_modules/**/build/Release/*.node"

# Models and native binaries outside ASAR
extraResources:
  # Bundled starter model
  - from: "models/starter"
    to: "models"
    filter:
      - "*.gguf"
  
  # Platform-specific native binaries
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

# macOS with Apple Silicon and Intel support
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
  # Sign bundled native binaries
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
  differentialPackage: false  # Disable delta updates for large apps

# Linux
linux:
  target:
    - AppImage
    - deb
  category: Development

# Notarization
afterSign: scripts/notarize.js

# Auto-update (separate from model updates)
publish:
  provider: github
  owner: your-org
  repo: your-app
```

### macOS entitlements for LLM inference

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

### Recommended distribution strategy

**Bundle a small starter model** (~600MB TinyLlama or Qwen3-0.6B) for immediate offline functionality. Download larger models on first run:

```javascript
// Hybrid model resolution
function getModelPath() {
  const userModels = path.join(app.getPath('userData'), 'models');
  const largeModel = path.join(userModels, 'qwen3-8b-q4_k_m.gguf');
  
  if (fs.existsSync(largeModel)) return largeModel;
  
  // Fall back to bundled starter
  return path.join(process.resourcesPath, 'models', 'qwen3-0.6b-q4_k_m.gguf');
}
```

This approach keeps installer size under 1GB while enabling full capability after download.

---

## Performance optimization delivers 2-5x improvements

Hardware acceleration is the single most impactful optimization. Full GPU offload transforms token generation from **2-5 t/s (CPU)** to **14-150 t/s (GPU)** depending on hardware.

### Benchmark data by hardware

| Hardware | Prompt Processing | Token Generation |
|----------|-------------------|------------------|
| M1 MacBook Pro | 266 t/s | 36 t/s |
| M3 Max MacBook Pro | 760 t/s | 66 t/s |
| M4 Max MacBook Pro | 886 t/s | 83 t/s |
| RTX 3080 | 780-900 t/s | 70-80 t/s |
| RTX 4090 | 1400-1800 t/s | 130-150 t/s |
| CPU-only (modern Intel/AMD) | 15-35 t/s | 8-18 t/s |

**Token generation is memory-bandwidth bound**, not compute-bound. This explains why M-series chips with unified memory often match dedicated GPUs—they have excellent memory bandwidth to weight ratios.

### High-impact optimizations checklist

1. **Enable GPU acceleration** (+200-500%): `gpuLayers: 99` offloads all layers
2. **Enable Flash Attention** (+5-15%): `flashAttention: true` reduces KV cache memory
3. **Use Q4_K_M quantization** (+40-60% vs F16): Fastest inference with excellent quality
4. **Quantize KV cache** (+10-20% context capacity): `--cache-type-k q8_0`
5. **Tune thread count**: Use 1-2 threads when GPU handles inference; physical core count for CPU-only

### Optimal configuration for NVIDIA GPUs

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
  threads: 2  // Low thread count with GPU
});
```

### Optimal configuration for Apple Silicon

```javascript
const context = await model.createContext({
  contextSize: 'auto',  // Maximize based on unified memory
  flashAttention: true,
  threads: 6  // Physical performance cores only
});
```

---

## Known limitations and practical workarounds

### Native addon compatibility

**Issue**: node-llama-cpp requires matching Node.js ABI with Electron's Node version.

**Solution**: Always run `npx electron-rebuild` after installing. For CI/CD:
```bash
npx electron-rebuild -v 31.0.0 -a x64 -w node-llama-cpp
```

### Windows code signing and SmartScreen

**Issue**: EV certificates no longer provide instant SmartScreen reputation (changed March 2024).

**Solution**: Use **Azure Trusted Signing** for US/Canada organizations, or accept that reputation builds over time with download volume.

### macOS notarization with native binaries

**Issue**: Unsigned `.node` files and external binaries cause notarization failures.

**Solution**: Use `asarUnpack` for `.node` files (auto-signed) and `mac.binaries` array for external executables.

### Large model updates

**Issue**: electron-updater differential updates don't work effectively for binary model files.

**Solution**: Manage model updates separately from app updates. Store user-downloaded models in `app.getPath('userData')` and implement a model manager with resume support.

### WebGPU in Electron (for WebLLM)

**Issue**: WebGPU requires explicit enabling in some Electron versions.

**Solution**:
```javascript
app.commandLine.appendSwitch('enable-unsafe-webgpu');
// Linux additionally needs:
app.commandLine.appendSwitch('enable-features', 'Vulkan,VulkanFromANGLE');
```

---

## When to consider alternative architectures

The node-llama-cpp + UtilityProcess architecture is optimal for most cases, but alternatives make sense in specific scenarios:

- **Ollama subprocess**: When you want model management UI, model library access, and REST API simplicity. Trade-off: +2GB for Ollama binary, slight IPC overhead.

- **Local server mode**: For applications needing multiple concurrent users or microservice architecture. Run llama.cpp server as subprocess, communicate via HTTP.

- **WebLLM/WebGPU**: For web-first applications where browser compatibility matters more than maximum performance. Achieves 80-85% native speed.

- **Cloud hybrid**: When model size exceeds local resources. Run small model locally for quick responses, route complex queries to cloud API. Implement with fallback logic based on prompt complexity.

- **llamafile distribution**: For maximum portability with zero dependencies. Single executable runs on six operating systems. Best for tools distributed to non-technical users who can't install dependencies.

---

## Conclusion

Building a production Electron app with bundled LLM inference is now practical thanks to **node-llama-cpp's mature bindings** and **Electron's UtilityProcess API**. The winning combination: Qwen3-4B or 8B with Q4_K_M quantization, running in an isolated utility process, with models distributed via extraResources. This delivers native inference speed across platforms while maintaining Electron's familiar development model.

For new projects, start with the @electron/llm experimental package as a reference implementation, then customize as needed. The hybrid bundling strategy—small model bundled, large models downloaded—keeps installer sizes reasonable while providing full offline capability. Focus optimization efforts on GPU acceleration first; everything else provides incremental gains compared to the 5-10x improvement from proper hardware utilization.