# 🚀 Guia Completo para ZeroGPU no Hugging Face Spaces

## 1. 📖 O que é ZeroGPU e Por que é Diferente?

O **ZeroGPU** é uma infraestrutura de GPU compartilhada do Hugging Face que gerencia dinamicamente recursos de GPU para
aplicações de Machine Learning. A principal inovação está em sua abordagem **"serverless"** ou sob demanda.

### 🔄 Arquitetura Tradicional vs. ZeroGPU

| Característica       | GPU Tradicional (T4, A10G, etc.)                              | ZeroGPU (H200 slice)                                                                              |
| :------------------- | :------------------------------------------------------------ | :------------------------------------------------------------------------------------------------ |
| **Alocação**         | GPU dedicada e reservada 24/7 enquanto o Space estiver ativo. | GPU alocada apenas quando uma função decorada é executada e liberada após.                        |
| **Custo**            | Cobrança por minuto de _runtime_, independente de uso.        | Acesso gratuito para uso, com cotas diárias de minutos. Hosting requer assinatura PRO/Enterprise. |
| **Modelo Econômico** | Pay-as-you-go (pode ficar caro).                              | Custo fixo para criadores (via assinatura), extremamente custo-efetivo para modelos grandes.      |
| **Hardware**         | Variado (T4, L4, A100, etc.).                                 | Fatia (_slice_) de uma NVIDIA **H200** com **70GB de VRAM** por workload.                         |
| **Multi-GPU**        | Configuração estática e fixa (ex: 4x L4).                     | Suporte a múltiplas GPUs concorrentes para uma única aplicação.                                   |

**O Princípio Fundamental**: No ZeroGPU, a GPU **não está disponível** quando seu aplicativo inicia. O processo
principal roda em CPU. Apenas quando uma função específica (decorada com `@spaces.GPU`) é chamada, o sistema cria um
processo "fork", aloca uma GPU para ele, executa a função e finaliza o fork. Por isso, qualquer tentativa de acessar a
GPU (como `model.to('cuda')`) **fora** de uma função decorada causará falha.

## 2. ⚙️ Como Implementar Corretamente

### 📦 Pré-requisitos e Configuração

1.  **Hardware do Space**: No menu de configurações (_Settings_) do seu Space, o hardware deve ser **"ZeroGPU"**.
2.  **SDK Suportado**: Apenas **Gradio** (versão 4+).
3.  **Versões Compatíveis**:
    - **Python**: 3.10.13.
    - **PyTorch**: Versões da 2.1.0 até a mais recente são suportadas. Consulte a
      [documentação oficial](https://huggingface.co/docs/hub/en/spaces-zerogpu) para a lista completa.
4.  **Requirements.txt**: Para garantir uma instalação compatível com CUDA, use:
    ```txt
    --extra-index-url https://download.pytorch.org/whl/cu121
    torch>=2.1.0
    transformers
    gradio>=4.0.0
    ```
    A flag `--extra-index-url` é crucial para obter os binários corretos do PyTorch.

### 🧠 Padrão de Código Essencial

A regra de ouro: **NUNCA carregue o modelo ou chame qualquer operação CUDA no escopo global do `app.py`**.

```python
# CORRETO ✅
import gradio as gr
import spaces
import torch

# 1. Importe a biblioteca spaces
import spaces

# 2. NÃO carregue o modelo aqui. Defina variáveis vazias ou estado.
model = None
tokenizer = None

@spaces.GPU
def load_model_once():
    """Função para carregar o modelo dentro do contexto GPU."""
    global model, tokenizer
    if model is None:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("seu-modelo")
        model = AutoModelForCausalLM.from_pretrained("seu-modelo")
        model.to('cuda')  # SEGURO: dentro da função decorada
    return model, tokenizer

@spaces.GPU
def generate(prompt):
    """Função principal de inferência."""
    # Carrega o modelo na primeira chamada
    local_model, local_tokenizer = load_model_once()
    # Realiza a inferência
    inputs = local_tokenizer(prompt, return_tensors="pt").to('cuda')
    with torch.no_grad():
        outputs = local_model.generate(**inputs)
    return local_tokenizer.decode(outputs[0])

# Interface Gradio
iface = gr.Interface(fn=generate, inputs="text", outputs="text")
iface.launch()
```

**Erro Comum (que vivenciamos)** ❌:

```python
# ERRADO ❌ - Causa "No @spaces.GPU function detected"
import spaces
from transformers import pipeline

# O pipeline tenta ir para 'cuda' no escopo global, antes de qualquer @spaces.GPU
pipe = pipeline("text-to-speech", "suno/bark", device="cuda")

@spaces.GPU
def generate(text):
    return pipe(text)  # Tarde demais! A GPU já falhou ao inicializar.
```

### ⏱ Gerenciamento de Duração e Filas

Funções decoradas com `@spaces.GPU` têm um limite padrão de **60 segundos**. Para tarefas mais longas, defina uma
duração máxima:

```python
@spaces.GPU(duration=120)  # Máximo de 120 segundos
def generate_long(prompt, steps=50):
    # ... geração lenta ...
    return result
```

**Importante**: Especificar uma duração **menor e mais realista** para suas funções dá **maior prioridade na fila** de
espera do ZeroGPU para os visitantes do seu Space. O uso é regido por cotas diárias:

| Tipo de Conta   | Cota Diária de GPU | Prioridade na Fila |
| :-------------- | :----------------- | :----------------- |
| Não autenticado | 2 minutos          | Baixa              |
| Conta Gratuita  | 3.5 minutos        | Média              |
| **PRO / Team**  | **25 minutos**     | **Mais Alta**      |
| Enterprise      | 45 minutos         | Mais Alta          |

## 3. 🚀 Otimização de Performance

### 🛠 Compilação "Ahead-of-Time" (AoT)

Como o ZeroGPU cria um novo processo para cada tarefa, a compilação JIT padrão (`torch.compile`) não é eficiente, pois
precisaria recompilar a cada vez. A solução é a **compilação antecipada**:

```python
import spaces
import torch

@spaces.GPU(duration=300)  # Compilação pode ser demorada
def compile_model():
    # 1. Capturar entradas de exemplo
    with spaces.aoti_capture(model) as call:
        dummy_output = model(dummy_input)
    # 2. Exportar o modelo
    exported = torch.export.export(model, args=call.args)
    # 3. Compilar
    compiled_model = spaces.aoti_compile(exported)
    return compiled_model

# Compila uma vez e usa muitas vezes
compiled = compile_model()
spaces.aoti_apply(compiled, model)  # Substitui o 'forward' do modelo
```

Essa técnica pode acelerar a inferência em **1.3x a 1.8x**.

### 💾 Gerenciamento de Estado com Cache

Para evitar recarregar o modelo em toda chamada (dentro do mesmo processo), use cache:

```python
from functools import lru_cache

@spaces.GPU
@lru_cache(maxsize=1)  # Cache dentro do processo
def get_model():
    model = AutoModel.from_pretrained("meu-modelo").to('cuda')
    return model

@spaces.GPU
def predict(prompt):
    model = get_model()  # Carrega apenas na primeira chamada do processo
    return model.generate(prompt)
```

## 4. 🐛 Solução de Problemas Comuns

| Problema                                 | Causa Provável                                                                         | Solução                                                                                                           |
| :--------------------------------------- | :------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **`"No @spaces.GPU function detected"`** | O código tentou acessar `'cuda'` antes da primeira função decorada ser chamada.        | Garanta que **todo** acesso a CUDA (`.to('cuda')`, `torch.cuda.*`) esteja **dentro** de uma função `@spaces.GPU`. |
| **`"Can't initialize NVML"`**            | O PyTorch tentou inicializar a GPU no processo principal (CPU).                        | É um **sintoma** do problema acima, não a causa raiz. Corrija o acesso prematuro à GPU.                           |
| **Modelo não carrega / OOM**             | O processo fork tem 70GB, mas o modelo pode ser grande.                                | Use quantização (`.to(torch.float16)`), carregue com `device_map="auto"` ou otimize com AoT.                      |
| **Latência alta na primeira chamada**    | Carregamento do modelo do disco.                                                       | Use o padrão de cache mostrado acima. A compilação AoT também ajuda.                                              |
| **Erro de Timeout ( >60s )**             | A função excedeu o limite padrão.                                                      | Use o parâmetro `@spaces.GPU(duration=...)` para aumentar o limite.                                               |
| **Space trava ao usar Client API**       | Requisições programáticas não passam o token de usuário, esgotando a cota rapidamente. | Extraia e passe o header `X-IP-Token` da request do usuário final para o Client Gradio.                           |

## 5. ✅ Checklist para Implantação

Antes de publicar seu Space ZeroGPU, confirme:

1.  [ ] **Hardware** está configurado como "ZeroGPU" nas Settings.
2.  [ ] **Nenhuma operação CUDA** (`to('cuda')`, `torch.cuda.*`) no escopo global.
3.  [ ] **Todas as funções** que usam GPU estão decoradas com `@spaces.GPU`.
4.  [ ] **Duração** (`duration=`) definida para funções que levam mais de ~50s.
5.  [ ] **`requirements.txt`** especifica uma versão compatível do PyTorch com `--extra-index-url`.
6.  [ ] **Logs de Build** foram verificados para confirmar `torch.cuda.is_available()` é `True` durante a execução da
        função decorada.

A principal mentalidade para dominar o ZeroGPU é internalizar seu **modelo de execução sob demanda**. Uma vez que você
estrutura seu código para carregar modelos e executar computações pesadas **exclusivamente** dentro das funções
decoradas `@spaces.GPU`, pode aproveitar uma GPU poderosa (H200) de forma gratuita e eficiente para seus demos.

Para se aprofundar, consulte a [documentação oficial do ZeroGPU](https://huggingface.co/docs/hub/en/spaces-zerogpu) e o
[blog sobre compilação AoT](https://huggingface.co/blog/zerogpu-aoti).
