# RIFE v4.26: Guia técnico completo para interpolação de frames

O **RIFE v4.26** (Real-Time Intermediate Flow Estimation) da Megvii Research representa o estado da arte em interpolação de frames em tempo real, alcançando **828 FPS em 720p** com TensorRT e qualidade superior em benchmarks padrão (Vimeo90K PSNR 35.615, UCF101 PSNR 35.282). Esta análise abrangente cobre arquitetura, integração com ComfyUI, otimização de performance, e comparações práticas com alternativas.

---

## A arquitetura IFNet revoluciona a estimação de fluxo óptico

O diferencial técnico do RIFE está no **IFNet (Intermediate Flow Network)**, que estima diretamente o fluxo intermediário sem depender de modelos pré-treinados de fluxo óptico. Enquanto métodos tradicionais como SuperSlomo e DAIN calculam fluxos bidirecionais e depois os revertem (causando o problema de "object shift" nas bordas de movimento), o RIFE aprende end-to-end a produzir os fluxos F_(t→0) e F_(t→1) diretamente.

A estrutura utiliza **3 IFBlocks** em cascata coarse-to-fine com parâmetros de resolução **(K₀, K₁, K₂) = (4, 2, 1)**. O primeiro bloco opera em 1/4 da resolução para capturar movimentos grandes, o segundo em 1/2, e o terceiro em resolução completa para refinamento final. Cada IFBlock contém camadas convolucionais 3×3, TransposeConv para upsampling, e ativação PReLU, totalizando apenas **~9.8 milhões de parâmetros**.

**Fórmula de atualização iterativa:**
```
[F^i, M^i] = [F^(i-1), M^(i-1)] + IFB_i([F^(i-1), M^(i-1)], t, Î^(i-1))
```

A reconstrução final combina os frames warped usando uma máscara de fusão M:
```
Î_t = M ⊙ Î_(t←0) + (1-M) ⊙ Î_(t←1)
```

O treinamento emprega **privileged distillation** com um bloco "professor" que tem acesso ao frame ground-truth, gerando supervisão mais estável para os fluxos intermediários. Isso permite convergência mais rápida e qualidade superior comparado a usar apenas loss de reconstrução.

---

## Instalação completa no ComfyUI

### Método 1: ComfyUI Manager (recomendado)
```
1. Abrir ComfyUI → Menu Manager → "Install Custom Nodes"
2. Buscar "ComfyUI-Frame-Interpolation"
3. Instalar e reiniciar ComfyUI
```

### Método 2: Instalação manual
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git
cd ComfyUI-Frame-Interpolation

# Windows
install.bat

# Linux/Mac
source ../../../venv/bin/activate
python install.py
```

### Download dos checkpoints RIFE v4.26
Os modelos devem ser colocados em `ComfyUI/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/`:

| Versão | Data | Link (Google Drive) | Uso recomendado |
|--------|------|---------------------|-----------------|
| **v4.26** | 2024.09.21 | `1gViYvvQrtETBgU1w8axZSsr7YUuw31uy` | Recursos ilimitados |
| **v4.25** | 2024.09.19 | `1ZKjcbmt1hypiFprJPIKW0Tt0lr_2i7bg` | **Padrão para maioria das cenas** |
| **v4.25.lite** | 2024.10.20 | `1zlKblGuKNatulJNFf5jdB-emp9AqGK05` | Recursos limitados |

Para GPUs não-NVIDIA (AMD/Intel), edite `config.yaml`:
```yaml
ops_backend: taichi  # ao invés de 'cupy'
```

---

## Parâmetros do node RIFE VFI no ComfyUI

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `ckpt_name` | String | rife47.pth | Arquivo do modelo |
| `multiplier` | INT | 2 | Fator de multiplicação (2, 4, 8, 16) |
| `ensemble` | BOOL | True | Melhor qualidade, mais lento |
| `scale_factor` | FLOAT | 1.0 | Escala de processamento (0.5 para 4K) |
| `fast_mode` | BOOL | True | Modo rápido (sem efeito v4.5+) |
| `clear_cache_after_n_frames` | INT | 10 | Limpeza de cache CUDA |

### Configurações por caso de uso

**Processamento rápido (preview):**
```yaml
ckpt_name: rife47.pth
multiplier: 2
fast_mode: true
ensemble: false
scale_factor: 0.5
```

**Alta qualidade para anime:**
```yaml
ckpt_name: rife49.pth
multiplier: 2
ensemble: true
scale_factor: 1.0
```

**Vídeo 4K com memória limitada:**
```yaml
ckpt_name: rife47.pth
multiplier: 2
scale_factor: 0.5
clear_cache_after_n_frames: 3
```

---

## Workflow JSON completo para slow-motion

```json
{
  "last_node_id": 5,
  "last_link_id": 4,
  "nodes": [
    {
      "id": 1,
      "type": "VHS_LoadVideo",
      "pos": [100, 200],
      "size": [315, 178],
      "outputs": [
        {"name": "IMAGE", "type": "IMAGE", "links": [1]},
        {"name": "frame_count", "type": "INT", "links": []},
        {"name": "audio", "type": "VHS_AUDIO", "links": [3]},
        {"name": "video_info", "type": "VHS_VIDEOINFO", "links": []}
      ],
      "widgets_values": ["input_video.mp4", 0, false, true, 0, null, false]
    },
    {
      "id": 2,
      "type": "RIFE VFI",
      "pos": [500, 200],
      "size": [315, 250],
      "inputs": [
        {"name": "frames", "type": "IMAGE", "link": 1},
        {"name": "optional_interpolation_states", "type": "INTERPOLATION_STATES", "link": null}
      ],
      "outputs": [
        {"name": "IMAGE", "type": "IMAGE", "links": [2]}
      ],
      "widgets_values": ["rife49.pth", 10, 8, false, true, 1.0]
    },
    {
      "id": 3,
      "type": "VHS_VideoCombine",
      "pos": [900, 200],
      "size": [315, 300],
      "inputs": [
        {"name": "images", "type": "IMAGE", "link": 2},
        {"name": "audio", "type": "VHS_AUDIO", "link": 3}
      ],
      "widgets_values": [30, 0, "slowmo_output", "video/h264-mp4", false, true, false, null, null]
    }
  ],
  "links": [
    [1, 1, 0, 2, 0, "IMAGE"],
    [2, 2, 0, 3, 0, "IMAGE"],
    [3, 1, 2, 3, 1, "VHS_AUDIO"]
  ]
}
```

**Para slow-motion 8x:** Configure `multiplier: 8` no RIFE VFI e mantenha o frame_rate original (30) no VHS_VideoCombine. O vídeo de 30fps original terá 240 frames por segundo de conteúdo original, reproduzidos a 30fps = 8x mais lento.

---

## Performance e consumo de VRAM detalhados

### Benchmarks RTX 4090 com TensorRT (Linux, TRT 10.9)

| Modelo | Resolução | FPS | VRAM |
|--------|-----------|-----|------|
| **RIFE v4.26** | 720p | **828.65** | 1.9GB |
| **RIFE v4.26** | 1080p | **409.53** | 2.3GB |
| RIFE v4.26.heavy | 720p | 567.59 | 2.4GB |
| RIFE v4.26.heavy | 1080p | 278.55 | 3.5GB |

### Requisitos de VRAM por resolução

| Resolução | VRAM Necessária | Recomendação |
|-----------|-----------------|--------------|
| 720p | **1.9 - 2.4 GB** | Qualquer GPU moderna |
| 1080p | **2.3 - 3.5 GB** | GTX 1060 6GB+ |
| 1440p | 6-8 GB | RTX 3060+ |
| 4K | **10+ GB** | RTX 3090/4090 ou usar `--scale=0.5` |

### Otimização TensorRT para máxima performance

**VapourSynth com TensorRT:**
```python
from vsrife import rife
import vapoursynth as vs

core = vs.core
clip = core.bs.VideoSource(source="input.mp4")
clip = core.resize.Bicubic(clip, format=vs.RGBH, matrix_in_s="709")

clip = rife(
    clip,
    model="4.26",
    sc=False,                    # Scene detection off
    trt=True,                    # TensorRT
    trt_static_shape=True,       # Shapes estáticas
    trt_optimization_level=5,    # Otimização máxima
    trt_cache_dir="/workspace/tensorrt"
)

clip = core.resize.Bicubic(clip, format=vs.YUV420P8, matrix_s="709")
clip.set_output()
```

**Conversão ONNX para TensorRT engine:**
```bash
trtexec --bf16 --fp16 \
  --onnx=model.onnx \
  --minShapes=input:1x3x8x8 \
  --optShapes=input:1x3x720x1280 \
  --maxShapes=input:1x3x1080x1920 \
  --saveEngine=model.engine \
  --builderOptimizationLevel=5 \
  --useCudaGraph
```

---

## RIFE 4.22.lite: otimizado para vídeos de difusão

A variante **lite** utiliza framework de treinamento similar ao modelo completo, porém com **custo computacional reduzido**. O RIFE 4.22.lite é especificamente otimizado para pós-processamento de vídeos gerados por modelos de difusão (AnimateDiff, Stable Video Diffusion, etc.).

| Característica | Lite | Standard | Heavy |
|----------------|------|----------|-------|
| Custo computacional | Baixo | Moderado | Alto |
| Tamanho do modelo | ~8 MB | ~12 MB | ~15 MB |
| VRAM (1080p) | 1.8GB | 2.3GB | 3.5GB |
| Caso de uso | Difusão, mobile | Geral | Qualidade máxima |

**Quando usar cada versão:**
- **4.22.lite**: Vídeos AI-generated, recursos limitados
- **v4.25**: Recomendação oficial para maioria das cenas
- **v4.26.heavy**: Qualidade máxima sem restrição de tempo

---

## Licença MIT: uso comercial permitido

```
MIT License - Copyright (c) 2021 hzwer

Permissões:
✅ Uso comercial sem royalties
✅ Modificação e criação de derivados
✅ Distribuição e sublicenciamento
✅ Manter modificações proprietárias

Obrigações:
⚠️ Incluir copyright e licença em todas as cópias

Exemplo de atribuição para projetos comerciais:
"This software includes RIFE (Real-Time Intermediate Flow Estimation)
Copyright (c) 2021 hzwer - Licensed under MIT License
https://github.com/hzwer/Practical-RIFE"
```

**Importante**: Embora o código seja MIT, os datasets de treinamento podem ter licenças não-comerciais. Consulte os repositórios oficiais para detalhes completos.

---

## Integração com FlowFrames, SVFI e VapourSynth

### FlowFrames (Windows GUI)
```
Configurações recomendadas:
- AI Model: RIFE 4.x
- UHD Mode: Ativar para 4K+
- CUDA Fast Mode: FP16 para velocidade
- GPU IDs: 0,1,2,3 para multi-GPU
```

### SVFI - Linha de comando
```bash
cd "C:\Program Files (x86)\Steam\steamapps\common\SVFI"

# Batch processing
for %i in ("D:\videos\*.mp4") do (
  one_line_shot_args.exe --input "%i" --task-id "%~ni" --config "Configs\SVFI_Config.ini"
)
```

### VapourSynth-RIFE-ncnn-Vulkan
```python
import vapoursynth as vs
core = vs.core

clip = core.lsmas.LWLibavSource("input.mp4")
rgb_clip = core.resize.Bicubic(clip, format=vs.RGBS, matrix_in_s="709")

# Scene change detection
yuv_clip = core.misc.SCDetect(clip, threshold=0.1)
rgb_clip = core.std.CopyFrameProps(rgb_clip, yuv_clip)

# RIFE interpolation
result = core.rife.RIFE(rgb_clip, model=72, sc=True, uhd=True)  # model=72 = v4.26

result = core.resize.Bicubic(result, format=vs.YUV420P10, matrix_s="709")
result.set_output()
```

### rife-ncnn-vulkan CLI (cross-platform)
```bash
# Diretório para diretório
./rife-ncnn-vulkan -i input_frames/ -o output_frames/ -m rife-v4.6

# Pipeline completo com FFmpeg
mkdir input_frames output_frames
ffmpeg -i input.mp4 input_frames/frame_%08d.png
./rife-ncnn-vulkan -i input_frames -o output_frames -u  # -u = UHD mode
ffmpeg -framerate 48 -i output_frames/%08d.png -c:v libx264 -crf 20 output.mp4
```

---

## Comparação definitiva: RIFE vs FILM vs VFIMamba vs DAIN

### Benchmarks de qualidade (PSNR)

| Dataset | RIFE v4.26 | FILM | VFIMamba | DAIN |
|---------|------------|------|----------|------|
| **Vimeo90K** | 35.615 dB | ~35.5 dB | **36.64 dB** | ~35.0 dB |
| **UCF101** | 35.28 dB | Competitivo | Competitivo | - |
| **X-TEST 4K** | Baseline | Bom | **+0.80 dB** | - |

### Velocidade relativa (1080p, 2x, RTX 4090)

| Método | FPS | Relativo ao RIFE |
|--------|-----|------------------|
| **RIFE v4.26** | ~410 | Baseline |
| VFIMamba | Eficiente | ~70-80% |
| FILM | ~12 | **30x mais lento** |
| DAIN | ~3-5 | **80-100x mais lento** |

### Recomendação por cenário

| Cenário | Melhor opção | Alternativa |
|---------|--------------|-------------|
| **Vídeo AI-generated** | RIFE v4.22.lite | VFIMamba |
| **Produção profissional** | FILM | VFIMamba |
| **Playback real-time (SVP)** | RIFE v4.15-lite | - |
| **Conteúdo 4K** | VFIMamba | FILM |
| **Movimento extremo (>50px)** | FILM | VFIMamba |
| **Processamento em lote** | RIFE | - |
| **Anime/2D** | RIFE-anime / GMFSS | VFIMamba |
| **GPUs AMD** | RIFE-NCNN | DAIN-NCNN |

---

## Conclusão

O **RIFE v4.26** permanece a escolha ideal para interpolação de frames quando velocidade é prioritária, oferecendo performance até **27x superior ao DAIN** com qualidade competitiva. Para cenários onde qualidade absoluta supera velocidade, **VFIMamba** (NeurIPS 2024) estabelece novo estado da arte com **PSNR 36.64 dB** no Vimeo90K e escala linear para resoluções altas. O **FILM** excele em movimentos grandes (>50 pixels) e produção profissional, enquanto o **DAIN** é largamente superado pelas alternativas modernas.

A arquitetura IFNet com privileged distillation e refinamento coarse-to-fine permite ao RIFE balancear qualidade e eficiência de forma única. A licença MIT permissiva, ampla integração com ferramentas (ComfyUI, FlowFrames, SVFI, VapourSynth), e suporte a hardware diverso (NVIDIA via CUDA, AMD/Intel via Vulkan) consolidam o RIFE como a solução mais versátil para interpolação de vídeo em 2025.