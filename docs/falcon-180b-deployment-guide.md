# Como rodar o gigante Falcon 180B: guia completo para soluções offline e na nuvem

O Falcon 180B (uncensored) é um dos LLMs mais potentes disponíveis como open-source, com 180 bilhões de parâmetros. Este relatório apresenta as melhores alternativas para rodá-lo dentro do seu orçamento de R$40.000, tanto em hardware NVIDIA recém-anunciado quanto no Google Cloud.

## Requisitos básicos do modelo Falcon 180B

O Falcon 180B exige recursos substanciais devido ao seu tamanho massivo:

- **Memória em precisão completa (BF16)**: Aproximadamente 640GB de VRAM (~8x GPUs A100 de 80GB)
- **Armazenamento para pesos do modelo**: ~360GB em formato BF16 completo
- **RAM do sistema**: Varia conforme o nível de quantização, de 76GB (2-bit) até 193GB (8-bit)

Com **técnicas de quantização**, os requisitos podem ser significativamente reduzidos:
- Quantização 8-bit reduz para ~320GB VRAM (~50% do original)
- Quantização 4-bit reduz para ~160GB VRAM (~25% do original)
- Quantização 2-bit reduz para ~76GB RAM

A execução do modelo sem otimização é praticamente inviável em qualquer configuração portátil ou de custo acessível, tornando as técnicas de otimização essenciais para nosso cenário.

## Solução offline: mini máquinas NVIDIA recém-anunciadas

A NVIDIA lançou recentemente dois sistemas compactos relevantes para nossa análise:

### 1. NVIDIA DGX Spark (anteriormente Project DIGITS)

**Especificações principais:**
- Processador: NVIDIA GB10 Grace Blackwell Superchip
- GPU: Arquitetura Blackwell com 5ª geração de Tensor Cores
- Memória: 128GB de memória unificada LPDDR5X
- Desempenho AI: Até 1.000 TOPS (FP4)
- Armazenamento: Opções de 1TB ou 4TB SSD NVMe
- Form factor: Extremamente compacto (15cm x 15cm x 5.05cm), 1,2kg
- Preço: $3.999 (modelo 4TB) ≈ **R$22.391**

**Capacidade para Falcon 180B:**
- Sozinho: Pode executar modelos de até 200B parâmetros, mas exige quantização agressiva
- Dois DGX Spark conectados: Podem lidar com modelos de até 405B parâmetros
- **Viabilidade**: Poderia executar o Falcon 180B com quantização de 3-4 bits, especialmente com dois dispositivos conectados (ainda dentro do orçamento de R$40.000)

### 2. NVIDIA DGX Station

**Especificações principais:**
- Processador: NVIDIA GB300 Grace Blackwell Ultra
- Memória: 784GB de memória coerente (288GB GPU HBM3e + 496GB CPU LPDDR5X)
- Desempenho AI: Até 20 petaFLOPS
- Preço estimado: $100.000+ ≈ **R$560.000+**

**Capacidade para Falcon 180B:**
- Executaria o Falcon 180B sem comprometimentos, mas **excede significativamente o orçamento**

### 3. NVIDIA Jetson Orin Nano Super

Com apenas 8GB de memória por R$1.395, este dispositivo é **inadequado** para executar o Falcon 180B em qualquer configuração.

## Solução online: Google Compute Engine

O principal desafio para configurações brasileiras é a **ausência de GPUs A100/H100 na região southamerica-east1 (São Paulo)**. As melhores opções são:

### 1. Configuração A2 baseada nos EUA (desempenho completo)

- **Tipo de máquina**: a2-ultragpu-8g (8× A100 80GB)
- **Região**: us-central1 (Iowa) - mais próxima do Brasil com disponibilidade de A100
- **Preço sob demanda**: ~$40,55/hora (~R$227/hora ou ~R$163.440/mês)
- **Com desconto de 3 anos**: ~$13.320/mês (~R$74.592/mês)
- **Prós**: Desempenho completo do Falcon 180B sem sacrifícios de quantização
- **Contras**: Maior latência, custo elevado (acima do orçamento mensal)

### 2. Configuração A2 com modelo quantizado (recomendada)

- **Tipo de máquina**: a2-ultragpu-4g (4× A100 80GB) 
- **Região**: us-central1
- **Modelo**: Falcon 180B quantizado (GPTQ ou QLoRA)
- **Preço sob demanda**: ~$20,28/hora (~R$113/hora ou ~R$81.720/mês)
- **Com desconto de 1 ano**: ~R$51.483/mês
- **Com desconto de 3 anos**: ~R$36.774/mês
- **Prós**: Menor custo, ainda com bom desempenho usando modelo quantizado
- **Contras**: Alguma degradação na qualidade do modelo, latência do Brasil

### Estratégias de otimização de custos

1. **Instâncias Spot**:
   - 60-91% de desconto (reduz a opção 2 para ~R$7.354-R$32.688/mês)
   - Risco de preempção (interrupção)
   - Ideal para cargas não críticas ou testes

2. **Uso com demanda**:
   - Pagar apenas pelas horas utilizadas
   - Para uso esporádico: 10 horas/semana = ~R$4.520/mês

## Técnicas de otimização para execução eficiente

### 1. Quantização (essencial para ambas as soluções)

```python
# Exemplo de quantização 4-bit com bitsandbytes
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-180B",
    torch_dtype=torch.bfloat16,
    load_in_4bit=True,
    device_map="auto",
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
    )
)
```

**Modelos pré-quantizados recomendados**:
- TheBloke/Falcon-180B-GPTQ (várias versões de 2 a 8 bits)
- TheBloke/Falcon-180B-Chat-GPTQ (versão para chat)

### 2. Sharding entre múltiplas GPUs

```python
# Mapeamento automático entre dispositivos
model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-180B",
    torch_dtype=torch.bfloat16,
    device_map="auto",  # Distribui automaticamente entre GPUs
)
```

Para o DGX Spark, conectar dois dispositivos via NVIDIA ConnectX permite dividir o modelo entre eles.

### 3. CPU offloading para grandes modelos

```python
from accelerate import init_empty_weights, infer_auto_device_map

# Mapa de dispositivos com offloading para CPU
device_map = infer_auto_device_map(
    model,
    max_memory={0: "40GiB", 1: "40GiB", "cpu": "200GiB"},
    no_split_module_classes=["RWAttention", "TransformerEncoderLayer"]
)
```

### 4. Inferência com memória eficiente (Flash Attention e Paged Attention)

Estas otimizações são implementadas automaticamente pelo Text Generation Inference (TGI), que é altamente recomendado para execução eficiente.

## Guia de implementação passo a passo

### Solução offline (DGX Spark)

1. **Requisitos de software**:
   - PyTorch 2.0+
   - Transformers 4.33+
   - CUDA 12.2+
   - Bibliotecas adicionais: bitsandbytes, accelerate, safetensors

2. **Configuração inicial**:
   ```bash
   # Instalar dependências
   pip install torch --extra-index-url https://download.pytorch.org/whl/cu122
   pip install "transformers>=4.33.0" "accelerate>=0.22.0" "bitsandbytes>=0.39.0"
   pip install safetensors
   
   # Login no Hugging Face (necessário para aceitar licença do modelo)
   huggingface-cli login
   ```

3. **Download de modelo quantizado**:
   ```bash
   # Recomendado: versão GPTQ 4-bit
   git lfs install
   git clone https://huggingface.co/TheBloke/Falcon-180B-GPTQ
   ```

4. **Execução do modelo**:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM
   
   # Carregar modelo quantizado
   model_id = "TheBloke/Falcon-180B-GPTQ"
   tokenizer = AutoTokenizer.from_pretrained(model_id)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       device_map="auto",
       revision="gptq-4bit--1g-actorder_True"
   )
   
   # Função para gerar texto
   def generate_response(message):
       inputs = tokenizer(message, return_tensors="pt").to("cuda")
       output = model.generate(
           input_ids=inputs["input_ids"],
           attention_mask=inputs["attention_mask"],
           max_new_tokens=512,
           temperature=0.7,
           top_p=0.9,
           repetition_penalty=1.1
       )
       response = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
       return response
   ```

5. **Integração com LangChain**:
   ```python
   from langchain import HuggingFacePipeline, PromptTemplate, LLMChain
   from transformers import pipeline
   
   # Criar pipeline de geração de texto
   text_generation_pipeline = pipeline(
       "text-generation",
       model=model,
       tokenizer=tokenizer,
       max_new_tokens=512,
       temperature=0.7,
       top_p=0.9
   )
   
   # Criar LangChain HuggingFacePipeline
   llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
   
   # Definir template de prompt
   template = """
   Instrução: {query}
   Resposta:
   """
   prompt = PromptTemplate(template=template, input_variables=["query"])
   
   # Criar LLMChain
   chain = LLMChain(llm=llm, prompt=prompt)
   
   # Gerar resposta
   response = chain.run("Explique o que é computação quântica em termos simples")
   print(response)
   ```

### Solução online (Google Cloud)

1. **Criar instância GCE**:
   - Escolher a2-ultragpu-4g (4× A100 80GB)
   - Selecionar região us-central1
   - Configurar disco de boot com pelo menos 200GB

2. **Instalar dependências**:
   ```bash
   # Atualizar e instalar driver NVIDIA
   sudo apt-get update
   sudo apt-get install -y nvidia-driver-535
   
   # Instalar Docker
   sudo apt-get install -y docker.io
   
   # Configurar NVIDIA Container Toolkit
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

3. **Executar utilizando Text Generation Inference (recomendado)**:
   ```bash
   export MODEL=TheBloke/Falcon-180B-Chat-GPTQ
   export REVISION=gptq-4bit--1g-actorder_True
   
   # Executar container TGI
   docker run --gpus all --shm-size 1g -p 8080:80 \
       ghcr.io/huggingface/text-generation-inference:latest \
       --model-id $MODEL \
       --revision $REVISION \
       --max-total-tokens 4096 \
       --max-input-length 3584 \
       --max-batch-prefill-tokens 4096
   ```

4. **Integração com LangChain**:
   ```python
   from langchain.llms import HuggingFaceTextGenInference
   from langchain import PromptTemplate, LLMChain
   
   # Conectar ao servidor TGI
   llm = HuggingFaceTextGenInference(
       inference_server_url="http://localhost:8080/",
       max_new_tokens=512,
       top_k=10,
       top_p=0.95,
       temperature=0.7,
       repetition_penalty=1.1,
   )
   
   # Criar template e chain
   template = """Instrução: {query}
   Resposta:"""
   prompt = PromptTemplate(template=template, input_variables=["query"])
   chain = LLMChain(llm=llm, prompt=prompt)
   
   # Gerar resposta
   response = chain.run("Como implementar um chatbot usando LangChain?")
   print(response)
   ```

## Comparação de custo-benefício e recomendações finais

### Comparação de custos

| Solução | Custo inicial | Custos mensais | Vantagens | Desvantagens |
|---------|---------------|----------------|-----------|--------------|
| **DGX Spark (1 unidade)** | R$22.391 | Apenas eletricidade | Sem custos recorrentes, portabilidade, privacidade | Performance limitada, quantização agressiva necessária |
| **DGX Spark (2 unidades)** | R$44.782 | Apenas eletricidade | Melhor desempenho, sem custos recorrentes | Acima do orçamento inicial, setup mais complexo |
| **GCE sob demanda** | R$0 | ~R$113/hora | Pague apenas pelo uso, sem investimento inicial | Custos elevados para uso contínuo, latência do Brasil |
| **GCE com spot instances** | R$0 | ~R$10-45/hora | Mais econômico, sem investimento inicial | Preempções ocasionais, latência do Brasil |

### Recomendações finais

1. **Para uso frequente mas não contínuo**: NVIDIA DGX Spark (R$22.391)
   - Quantizar o Falcon 180B para 4-bit (Q4_K_M)
   - Configuração ideal para desenvolvimento e pesquisa
   - Sem custos recorrentes após aquisição
   - Opção de adicionar segunda unidade posteriormente para melhor desempenho

2. **Para uso ocasional**: Google Cloud com instâncias spot
   - Ideal para experimentos periódicos ou projetos com prazo determinado
   - Configurar a2-ultragpu-4g com Falcon 180B quantizado
   - Custo estimado: R$10-45/hora (depende da demanda)
   - Implementar checkpointing para evitar perda de trabalho durante preempções

3. **Solução híbrida recomendada**:
   - Adquirir um DGX Spark para desenvolvimento local e testes
   - Utilizar Google Cloud para cargas de trabalho mais intensivas ou temporárias
   - Esta combinação mantém o custo total dentro do orçamento de R$40.000
   - Permite flexibilidade entre uso local e na nuvem

A escolha ideal dependerá do seu padrão específico de uso. Para desenvolvimento e experimentação constante, a solução offline com DGX Spark oferece o melhor valor a longo prazo. Para uso esporádico mas intensivo, a solução na nuvem com instâncias spot proporciona a melhor relação custo-benefício.

Em ambos os casos, as técnicas de otimização descritas são essenciais para viabilizar a execução deste modelo massivo dentro das restrições orçamentárias especificadas.