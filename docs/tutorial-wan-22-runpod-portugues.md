# 🎬 TUTORIAL DEFINITIVO: Wan 2.2 Remix no Runpod com ComfyUI
## Guia Passo-a-Passo para Maximizar Produção em 1 Hora

**Objetivo**: Configurar do zero e gerar o máximo de vídeos possível em 1 hora de uso.

**Custo estimado total**: $0.50 a $1.50 (dependendo da GPU escolhida)

---

# ETAPA 1: CRIAR CONTA E ADICIONAR CRÉDITOS (5 minutos)

## Passo 1.1: Acesse runpod.io e crie sua conta

1. Vá para **https://runpod.io**
2. Clique em **Sign Up** (canto superior direito)
3. Use Google, GitHub ou email para criar conta

## Passo 1.2: Adicione créditos

1. Após login, clique em **Billing** no menu lateral esquerdo
2. Clique em **Add Credits**
3. **Recomendação**: Adicione **$10** para começar

> 💡 **Por que $10?** Com RTX 4090 ($0.39/hora) você terá ~25 horas de uso. Suficiente para aprender e gerar dezenas de vídeos.

---

# ETAPA 2: ENTENDER OS TIPOS DE CLOUD E ARMAZENAMENTO

## ⚠️ INFORMAÇÃO CRÍTICA: Community Cloud vs Secure Cloud

O Runpod tem **DOIS tipos de Cloud** com diferenças importantes:

| Característica | Community Cloud | Secure Cloud |
|----------------|-----------------|--------------|
| **Preço GPU** | 💰 20-30% mais barato | 💸 Mais caro |
| **Network Volume** | ❌ **NÃO DISPONÍVEL** | ✅ Disponível |
| **Infraestrutura** | Hosts terceirizados | Data centers T3/T4 |
| **SLA de uptime** | Nenhum | 99.99% garantido |
| **Melhor para** | Experimentos, hobby | Produção, uso intensivo |

> ⚠️ **IMPORTANTE**: Network Volumes **SÓ funcionam no Secure Cloud**! Esta é uma limitação arquitetural permanente, não um bug.

---

## ESCOLHA SUA OPÇÃO:

### 🅰️ OPÇÃO A: Secure Cloud + Network Volume (RECOMENDADO para uso frequente)

**Vantagens**:
- Dados persistem mesmo ao TERMINAR o pod
- Não precisa re-baixar modelos nunca
- Mais confiável e estável

**Desvantagens**:
- GPU ~20-30% mais cara
- Network Volume custa $0.07/GB/mês extra

**Custo exemplo**: RTX 4090 ~$0.44-0.55/hr + Network Volume 100GB = $7/mês

### 🅱️ OPÇÃO B: Community Cloud + Volume Disk (Mais barato, requer cuidado)

**Vantagens**:
- GPU 20-30% mais barata
- Dados em `/workspace` persistem ao dar **STOP** no pod

**Desvantagens**:
- ❌ Dados são **PERDIDOS** ao dar **TERMINATE** no pod
- Precisa fazer backup manual antes de terminar
- Volume Disk parado cobra $0.20/GB/mês (mais caro que Network Volume!)

**Custo exemplo**: RTX 4090 ~$0.34-0.39/hr (sem custo extra de volume)

---

## 📊 Entendendo o Armazenamento no Runpod

| Tipo de Storage | O que é | Persiste ao STOP? | Persiste ao TERMINATE? | Custo |
|-----------------|---------|-------------------|------------------------|-------|
| **Container Disk** | Sistema operacional, apps | ❌ NÃO | ❌ NÃO | $0.10/GB/mês |
| **Volume Disk** | `/workspace` | ✅ SIM | ❌ NÃO | $0.10/GB rodando, $0.20/GB parado |
| **Network Volume** | Storage independente | ✅ SIM | ✅ SIM | $0.07/GB/mês |

### O que significa STOP vs TERMINATE?

| Ação | O que acontece | Quando usar |
|------|----------------|-------------|
| **STOP** | Pod desliga, Volume Disk preservado, continua cobrando storage | Pausas curtas (horas/dias) |
| **TERMINATE** | Pod deletado, **TUDO perdido** (exceto Network Volume) | Não vai usar mais / quer economizar |

---

## Se escolher OPÇÃO A (Secure Cloud + Network Volume):

### Passo 2.1: Criar o Network Volume

1. No menu lateral, clique em **Storage**
2. Clique em **+ New Network Volume**
3. Configure assim:

| Campo | Valor RECOMENDADO | Por quê |
|-------|-------------------|---------|
| **Name** | `comfyui-wan22` | Para identificar facilmente |
| **Datacenter Region** | **EU-RO-1** ou **EUR-IS-1** | Boa disponibilidade + drivers atualizados |
| **Size** | **100 GB** | Suficiente para Wan 2.2 + espaço extra |

4. Clique em **Create**

> ⚠️ **CRÍTICO**: A região do Network Volume é PERMANENTE. Você SÓ poderá usar pods **Secure Cloud** na mesma região!

**Custo do Network Volume**: $0.07/GB/mês = **$7/mês para 100GB**

### 💰 BÔNUS: Savings Plan (Economize 15-20% no Secure Cloud)

No Secure Cloud, você verá um botão **"Create Savings Plan"**. Este é um recurso exclusivo que pode reduzir significativamente seus custos se você planeja usar bastante.

#### O que é Savings Plan?

É um **compromisso de uso** onde você paga adiantado por um período e recebe desconto nas taxas horárias:

| Período | Desconto | Exemplo RTX 4090 |
|---------|----------|------------------|
| **1 mês** | ~15% off | De $0.55/hr → ~$0.47/hr |
| **3 meses** | ~20% off | De $0.55/hr → ~$0.44/hr |

#### Como funciona:

1. Você paga adiantado pelo período escolhido
2. A GPU fica **reservada** para você (garantida!)
3. Mesmo se você der STOP, o plano continua válido para o próximo pod com a mesma GPU
4. O plano tem data de expiração fixa - parar o pod **NÃO estende** o prazo

#### ⚠️ Regras importantes:

- ❌ **NÃO pode ser cancelado** após a compra
- ❌ **NÃO pode ser pausado** ou reembolsado
- ❌ **NÃO se transfere** para outro tipo de GPU
- ✅ Se você parar o pod, o desconto aplica ao próximo pod **do mesmo tipo de GPU**

#### Quando vale a pena?

| Situação | Savings Plan? |
|----------|---------------|
| Uso ocasional (1-2x por semana) | ❌ NÃO vale |
| Uso frequente (quase todo dia) | ✅ VALE |
| Projeto de longa duração | ✅ VALE |
| Só testando/aprendendo | ❌ NÃO vale |

> 💡 **Dica**: Se você vai usar a GPU por mais de **40% do tempo** durante o período, o Savings Plan compensa. Para uso ocasional de Wan 2.2, **NÃO recomendamos** - use On-Demand normal.

---

## Se escolher OPÇÃO B (Community Cloud sem Network Volume):

### Passo 2.1: Entender o Volume Disk

No Community Cloud, seus dados ficam no **Volume Disk** (montado em `/workspace`).

**Regras importantes**:
1. ✅ Ao dar **STOP**: dados em `/workspace` são preservados
2. ❌ Ao dar **TERMINATE**: **TUDO é perdido para sempre**
3. ⚠️ Pod parado cobra $0.20/GB/mês pelo Volume Disk

### Passo 2.2: Configurar backup (ESSENCIAL para Community Cloud)

Antes de dar TERMINATE em qualquer pod, você **DEVE** fazer backup! Veja a **ETAPA 9** no final deste tutorial para instruções detalhadas de backup.

**Opções de backup**:
- **Cloud Sync** (integrado no Runpod) → Backblaze B2, Amazon S3, Google Cloud
- **rclone** → Google Drive, Dropbox, OneDrive
- **runpodctl** → Transferência direta para seu PC

---

# ETAPA 3: CRIAR O POD (5-10 minutos)

Esta é a etapa mais importante. Esta seção está dividida em **DUAS PARTES**:

| Parte | O que fazer | Quando |
|-------|-------------|--------|
| **PARTE A** | 📖 LER e ENTENDER todas as configurações | **PRIMEIRO** - Leia TUDO antes de mexer no site |
| **PARTE B** | ▶️ EXECUTAR os passos no Runpod | **DEPOIS** - Só depois de entender tudo |

> ⚠️ **IMPORTANTE**: Leia a PARTE A inteira antes de começar a PARTE B! Assim você não vai errar nada.

---

# ═══════════════════════════════════════════════════════════════
# PARTE A: ENTENDER AS CONFIGURAÇÕES (Leia primeiro!)
# ═══════════════════════════════════════════════════════════════

Nesta parte você vai **APRENDER** o que cada configuração significa. **NÃO FAÇA NADA NO SITE AINDA!** Apenas leia e entenda.

---

## A.1: ENTENDER A TELA DE SELEÇÃO DE GPU

Quando você clicar em "+ Deploy", verá uma lista de GPUs disponíveis. Cada linha mostra:
- **Nome da GPU** (ex: RTX 5090, RTX 4090, L40S, A100)
- **VRAM** (memória da GPU - quanto mais, melhor)
- **Preço/hora** (varia por região e tipo de cloud)
- **Disponibilidade** (ícone verde = disponível)

### 🎯 QUAL GPU ESCOLHER PARA WAN 2.2?

| Objetivo | GPU | VRAM | Preço/Hora | Vídeos/Hora* | Recomendação |
|----------|-----|------|-----------|--------------|--------------|
| **💰 ECONÔMICO** | RTX 4090 | 24GB | $0.34-0.44 | 10-15 | Bom custo-benefício |
| **⭐ RECOMENDADO** | **RTX 5090** | **32GB** | **$0.69-0.89** | **18-25** | **MELHOR PARA WAN 2.2** |
| **🚀 MAIS VRAM** | L40S | 48GB | $0.89-0.99 | 15-20 | Para 720p ou vídeos longos |
| **💎 PROFISSIONAL** | A100 80GB | 80GB | $1.89-2.09 | 20-25 | Overkill para iniciantes |

*Vídeos de 5 segundos em 480p com Lightning LoRA

### ⭐ Por que RTX 5090 é a MELHOR escolha para Wan 2.2?

| Vantagem | Explicação |
|----------|------------|
| **32GB VRAM** | 8GB a mais que RTX 4090 - permite vídeos maiores e 720p |
| **27-35% mais rápida** | Arquitetura Blackwell é significativamente mais rápida |
| **CUDA 12.8** | Última versão, otimizada para novos modelos |
| **Preço justo** | $0.69/hr é excelente pelo desempenho entregue |
| **Melhor para I2V** | Benchmarks mostram ganhos enormes em image-to-video |

> 💡 **Nota sobre disponibilidade**: A RTX 5090 é mais nova e pode ter menos disponibilidade em algumas regiões. Regiões recomendadas: **EUR-IS-1**, **EU-RO-1**, **US-CA-2**

> ⚠️ **IMPORTANTE SOBRE DRIVERS**: Algumas regiões têm drivers mais antigos (570.x) que podem causar problemas. A região **US-CA-2** geralmente tem drivers atualizados (575+). Se tiver problemas, tente mudar de região.

---

## A.2: ENTENDER O POD TEMPLATE (CRÍTICO PARA RTX 5090!)

### O que é um Template?

O **Pod Template** define **TUDO** que vem pré-instalado no seu pod:
- Sistema operacional base (Ubuntu)
- Versão do CUDA (CRÍTICO para RTX 5090!)
- Versão do PyTorch
- Programas instalados (ComfyUI, Python, etc.)
- Configurações de portas
- Variáveis de ambiente

### ⚠️ CRÍTICO PARA RTX 5090

A RTX 5090 usa arquitetura **Blackwell** e requer **CUDA 12.8** ou superior. Templates antigos com CUDA < 12.8 **NÃO FUNCIONAM** com RTX 5090!

### 🎯 TEMPLATE RECOMENDADO:

| Template | Imagem Docker | CUDA | Compatibilidade |
|----------|---------------|------|-----------------|
| **Better ComfyUI Slim (5090)** | `madiator2011/better-comfyui:slim-5090` | **12.8** | ✅ **RTX 5090** |

### Por que usar `madiator2011/better-comfyui:slim-5090`?

| Vantagem | Explicação |
|----------|------------|
| **CUDA 12.8** | Versão correta para arquitetura Blackwell (RTX 5090) |
| **PyTorch Nightly 2.7+** | Compilado para CUDA 12.8 |
| **ComfyUI + Manager** | Já vem instalado e funcionando |
| **Zasper** | Terminal/IDE leve (substitui JupyterLab) - 4x mais eficiente! |
| **FileBrowser** | Gerenciador visual de arquivos pelo navegador |
| **Network Volume** | Projetado para usar com storage persistente |
| **Ultra-leve (~650MB)** | Imagem compacta, deploy rápido (~2-3 min) |
| **Python 3.12** | Versão moderna do Python |

### 🔧 Ferramentas incluídas no template:

| Ferramenta | Porta | O que faz |
|------------|-------|-----------|
| **ComfyUI** | 8188 | Interface principal para gerar vídeos |
| **FileBrowser** | 8080 | Upload/download de arquivos pelo navegador |
| **Zasper** | 8048 | Terminal e IDE (substitui Jupyter) |
| **SSH** | 22 | Acesso via linha de comando |

> 💡 **IMPORTANTE**: Este template **NÃO tem JupyterLab**! Use **Zasper** (porta 8048) para acessar o terminal, ou **FileBrowser** (porta 8080) para gerenciar arquivos visualmente.

### 📁 Estrutura de pastas do template:

```
/workspace/madapps/ComfyUI/      ← Instalação do ComfyUI
├── models/
│   ├── checkpoints/            ← Modelos principais
│   ├── loras/                  ← LoRAs
│   ├── vae/                    ← VAE
│   ├── text_encoders/          ← Encoders de texto
│   └── diffusion_models/       ← Modelos de difusão (Wan 2.2)
├── custom_nodes/               ← Custom nodes instalados
├── input/                      ← Imagens de entrada
└── output/                     ← Vídeos gerados
```

> ⚠️ **ATENÇÃO**: O caminho é `/workspace/madapps/ComfyUI/` (NÃO `/workspace/ComfyUI/`!)

### O que acontece se usar template ERRADO?

Se você usar um template antigo (CUDA < 12.8) com RTX 5090:

```
❌ ERRO: CUDA driver version is insufficient for CUDA runtime version
❌ ERRO: no kernel image is available for execution on the device
❌ ERRO: RuntimeError: CUDA error: no kernel image is available
```

---

## A.3: ENTENDER OS CAMPOS DA CONFIGURAÇÃO

Quando você selecionar uma GPU, abrirá a tela de configuração com vários campos. Aqui está o que cada um significa:

### 📛 **Pod Name** (Nome do Pod)
- **O que é**: Nome para identificar seu pod
- **Valor recomendado**: `wan22-5090` (ou qualquer nome descritivo)
- **Dica**: Use nomes que ajudem a identificar o propósito

### 🔢 **GPU Count** (Quantidade de GPUs)
- **O que é**: Quantas GPUs você quer
- **Valor recomendado**: **1** (uma é suficiente para Wan 2.2)
- **Aviso**: Mais GPUs = preço multiplicado!

### ☁️ **Cloud Type** (Tipo de Nuvem) - ⚠️ LEIA COM ATENÇÃO!

| Tipo | Network Volume? | Preço GPU | Melhor para |
|------|-----------------|-----------|-------------|
| **Community Cloud** | ❌ NÃO DISPONÍVEL | ~20-30% mais barato | Usuários que fazem backup manual |
| **Secure Cloud** | ✅ Disponível | Mais caro | Usuários que querem dados persistentes |

> ⚠️ **CRÍTICO**: Se você criou um Network Volume na Etapa 2 e quer usá-lo, você **DEVE** selecionar **Secure Cloud**! No Community Cloud, a opção de Network Volume não aparece.

**Escolha baseada na sua decisão na Etapa 2**:
- Se escolheu **OPÇÃO A** (Secure Cloud + Network Volume): Selecione **Secure Cloud**
- Se escolheu **OPÇÃO B** (Community Cloud): Selecione **Community Cloud**

### 💵 **Instance Pricing** (Modelo de Preço)
- **On-Demand**: Preço cheio (~$0.69-0.89/hr para RTX 5090), GPU garantida
- **Spot**: ~50% mais barato, MAS pode ser cancelado a qualquer momento!
- **Savings Plan** (só Secure Cloud): Paga adiantado por 1-3 meses, recebe 15-20% desconto
- **Valor recomendado**: **On-Demand** ✅ (para uso ocasional/aprendizado)

> 💡 **Sobre Savings Plan**: Só aparece no Secure Cloud! Se você vai usar muito (quase todo dia por semanas), pode valer a pena. Para uso ocasional de Wan 2.2, fique com On-Demand.

### 💰 **Create Savings Plan** (Botão - só Secure Cloud)
- **O que é**: Opção para pagar adiantado e receber desconto
- **Quando usar**: Projetos longos com uso intensivo (>40% do tempo)
- **Quando NÃO usar**: Aprendizado, testes, uso ocasional
- **Veja detalhes**: Explicado na ETAPA 2, seção Savings Plan

### 💾 **Container Disk** (Disco do Container)
- **O que é**: Espaço temporário para sistema e cache
- **Valor recomendado**: **20 GB**
- **AVISO**: Este espaço é **APAGADO** quando você dá STOP no pod!

### 💾 **Volume Disk** (Disco de Volume) - Aparece no Community Cloud
- **O que é**: Armazenamento em `/workspace`
- **Persiste ao STOP**: ✅ Sim
- **Persiste ao TERMINATE**: ❌ **NÃO - dados perdidos para sempre!**
- **Valor recomendado**: **100 GB** (para modelos Wan 2.2)

### 💾 **Network Volume** (Volume de Rede) - SÓ aparece no Secure Cloud
- **O que é**: Seu armazenamento PERMANENTE (criado na Etapa 2)
- **Persiste ao STOP**: ✅ Sim
- **Persiste ao TERMINATE**: ✅ Sim
- **Valor recomendado**: Selecione o volume que você criou

### 📁 **Volume Mount Path** (Caminho de Montagem)
- **O que é**: Onde o storage aparece dentro do pod
- **Valor recomendado**: `/workspace` (padrão)

### 🌐 **Expose HTTP Ports** (Portas HTTP)
- **O que é**: Portas para acessar serviços pela internet
- **Valor recomendado**: `8188, 8080, 8048` (o template já configura automaticamente)
  - **8188** = ComfyUI (interface principal)
  - **8080** = FileBrowser (gerenciador de arquivos web)
  - **8048** = Zasper (terminal e IDE - substituto do Jupyter)

> 💡 **IMPORTANTE**: Este template NÃO usa JupyterLab! Ele usa **Zasper** (mais leve e eficiente) e **FileBrowser** para gerenciar arquivos.

### ✅ **SSH Terminal Access** (Checkbox)
- **O que é**: Habilita acesso SSH ao pod
- **Valor recomendado**: **Marcado** ✅ (geralmente já vem marcado)

---

## A.4: RESUMO DAS CONFIGURAÇÕES RECOMENDADAS

### 🅰️ Se você escolheu SECURE CLOUD (com Network Volume):

| Campo | Valor Recomendado |
|-------|-------------------|
| **GPU** | RTX 5090 |
| **Pod Name** | `wan22-5090` |
| **GPU Count** | 1 |
| **Cloud Type** | **Secure Cloud** ← Para usar Network Volume |
| **Instance Pricing** | On-Demand |
| **Template** | `madiator2011/better-comfyui:slim-5090` |
| **Container Disk** | 20 GB |
| **Network Volume** | (o que você criou na Etapa 2) |
| **Volume Mount Path** | `/workspace` |
| **SSH Terminal Access** | ✅ Marcado |

### 🅱️ Se você escolheu COMMUNITY CLOUD (sem Network Volume):

| Campo | Valor Recomendado |
|-------|-------------------|
| **GPU** | RTX 5090 |
| **Pod Name** | `wan22-5090` |
| **GPU Count** | 1 |
| **Cloud Type** | **Community Cloud** ← Mais barato |
| **Instance Pricing** | On-Demand |
| **Template** | `madiator2011/better-comfyui:slim-5090` |
| **Container Disk** | 20 GB |
| **Volume Disk** | **100 GB** ← Para os modelos |
| **Volume Mount Path** | `/workspace` |
| **SSH Terminal Access** | ✅ Marcado |

### 🔧 O que vem pré-instalado no template:

| Ferramenta | Porta | Para que serve |
|------------|-------|----------------|
| **ComfyUI** | 8188 | Interface principal para gerar vídeos |
| **FileBrowser** | 8080 | Gerenciador de arquivos (upload/download) |
| **Zasper** | 8048 | Terminal e IDE (substituto do Jupyter) |
| **SSH** | 22 | Acesso via linha de comando |

### 📋 Checklist Visual - SECURE CLOUD:

```
CONFIGURAÇÃO SECURE CLOUD + NETWORK VOLUME
==========================================
[ ] GPU: RTX 5090 (32GB VRAM)
[ ] Pod Name: wan22-5090
[ ] GPU Count: 1
[ ] Cloud: Secure Cloud ← OBRIGATÓRIO para Network Volume!
[ ] Pricing: On-Demand (~$0.69-0.89/hr)
[ ] Template: madiator2011/better-comfyui:slim-5090 ← CRÍTICO!
[ ] Container Disk: 20 GB
[ ] Network Volume: SEU_VOLUME_AQUI ← CRÍTICO!
[ ] Mount Path: /workspace
[ ] SSH Terminal Access: ☑ (marcado)
```

### 📋 Checklist Visual - COMMUNITY CLOUD:

```
CONFIGURAÇÃO COMMUNITY CLOUD + VOLUME DISK
==========================================
[ ] GPU: RTX 5090 (32GB VRAM)
[ ] Pod Name: wan22-5090
[ ] GPU Count: 1
[ ] Cloud: Community Cloud ← Mais barato!
[ ] Pricing: On-Demand (~$0.69-0.89/hr)
[ ] Template: madiator2011/better-comfyui:slim-5090 ← CRÍTICO!
[ ] Container Disk: 20 GB
[ ] Volume Disk: 100 GB ← Para os modelos!
[ ] Mount Path: /workspace
[ ] SSH Terminal Access: ☑ (marcado)
```

> ⚠️ **PONTOS CRÍTICOS**:
> 1. **Template DEVE ser `madiator2011/better-comfyui:slim-5090`** (CUDA 12.8)
> 2. **Secure Cloud**: Network Volume DEVE ser selecionado
> 3. **Community Cloud**: Volume Disk de 100GB para os modelos + **fazer backup antes de TERMINATE!**

---

# ═══════════════════════════════════════════════════════════════
# PARTE B: EXECUTAR OS PASSOS (Faça depois de ler a Parte A!)
# ═══════════════════════════════════════════════════════════════

Agora que você **ENTENDEU** tudo, vamos **EXECUTAR** os passos no Runpod.

---

## B.1: Acessar a Tela de Deploy

1. No menu lateral esquerdo, clique em **Pods**
2. Clique no botão **+ Deploy** (canto superior direito)

---

## B.2: Filtrar e Selecionar a GPU

1. **ANTES de selecionar a GPU**, clique em **Additional Filters** no topo
2. Em **CUDA Version**, selecione **12.8** (importante para RTX 5090!)
3. **Selecione o tipo de Cloud baseado na sua escolha na Etapa 2**:
   - **Secure Cloud**: Se você criou Network Volume e quer usá-lo
   - **Community Cloud**: Se você quer economizar e vai fazer backup manual
4. Localize a **RTX 5090** na lista
5. Verifique se tem ícone verde ✅ (disponível)
6. Clique em **Deploy** na linha da RTX 5090

> 💡 **Isso NÃO cria o pod ainda!** Apenas abre a tela de configuração.

---

## B.3: Selecionar o Template (CRÍTICO!)

1. Na tela de configuração, localize **"Template"** ou **"Pod Template"**
2. Clique em **"Change Template"**
3. Na barra de busca, digite: `better comfyui slim 5090`
4. Selecione: **"Better ComfyUI Slim (5090 supported)"** do Madiator2011
   - Ou busque por: `madiator2011/better-comfyui:slim-5090`
5. Clique para selecionar o template

> ⚠️ **NÃO USE** templates sem "5090" no nome - eles não funcionam com RTX 5090!

---

## B.4: Configurar os Outros Campos

Preencha os campos conforme sua escolha de Cloud:

### Se escolheu SECURE CLOUD:

1. **Pod Name**: Digite `wan22-5090` (ou outro nome)
2. **GPU Count**: Mantenha **1**
3. **Cloud Type**: Já deve estar em **Secure Cloud**
4. **Instance Pricing**: Selecione **On-Demand**
5. **Container Disk**: Digite **20** GB
6. **Network Volume**: 
   - Clique no dropdown
   - **SELECIONE O VOLUME QUE VOCÊ CRIOU NA ETAPA 2**
   - ⚠️ Este é o passo mais crítico! Sem isso você perde tudo!
7. **Volume Mount Path**: Mantenha `/workspace`
8. **SSH Terminal Access**: Verifique se está **✅ marcado**

> 💡 **Sobre o botão "Create Savings Plan"**: Você verá este botão no Secure Cloud. Ele permite pagar adiantado por 1-3 meses e receber 15-20% de desconto. **Para iniciantes e uso ocasional, IGNORE este botão** - use On-Demand normal. Veja detalhes na ETAPA 2.

### Se escolheu COMMUNITY CLOUD:

1. **Pod Name**: Digite `wan22-5090` (ou outro nome)
2. **GPU Count**: Mantenha **1**
3. **Cloud Type**: Já deve estar em **Community Cloud**
4. **Instance Pricing**: Selecione **On-Demand**
5. **Container Disk**: Digite **20** GB
6. **Volume Disk**: Digite **100** GB (para armazenar os modelos)
7. **Volume Mount Path**: Mantenha `/workspace`
8. **SSH Terminal Access**: Verifique se está **✅ marcado**

> ⚠️ **LEMBRETE COMMUNITY CLOUD**: Seus dados em `/workspace` sobrevivem ao **STOP**, mas são **PERDIDOS** ao **TERMINATE**! Veja a ETAPA 9 sobre como fazer backup.

> 💡 **Nota**: Este template NÃO tem checkbox "Start Jupyter Notebook" porque usa **Zasper** em vez de Jupyter.

---

## B.5: REVISAR E FAZER O DEPLOY

1. **REVISE** todas as configurações mais uma vez:
   - [ ] Template é `slim-5090`?
   - [ ] (Secure Cloud) Network Volume está selecionado?
   - [ ] (Community Cloud) Volume Disk tem 100GB?

2. **Clique no botão de Deploy**:
   - **Secure Cloud**: Clique em **Deploy On-Demand** (botão azul)
   - **Community Cloud**: Clique em **Deploy On-Demand**
   
   > ⚠️ **NÃO clique em "Create Savings Plan"** a menos que você tenha lido a seção sobre isso na ETAPA 2 e tenha certeza que quer se comprometer!

3. Aguarde ~2-5 minutos para inicializar

### O que acontece durante o deploy:

| Status | Significado |
|--------|-------------|
| **Creating** | Runpod está alocando a GPU para você |
| **Starting** | O container está sendo baixado e iniciado |
| **Running** | ✅ Pronto para usar! |

> ⏱️ **Tempo típico**: 2-5 minutos no primeiro deploy (precisa baixar o template). Depois é mais rápido (~1-2 min).

---

## B.6: VERIFICAR SE ESTÁ FUNCIONANDO

Quando o status for **"Running"**:

1. Clique no botão **Connect** (ou clique no pod)
2. Você verá **três serviços HTTP** disponíveis:

| Serviço | Porta | O que é | Para que usar |
|---------|-------|---------|---------------|
| **ComfyUI** | 8188 | Interface de geração | ⭐ Principal - gerar vídeos |
| **FileBrowser** | 8080 | Gerenciador de arquivos | Upload/download de arquivos |
| **Zasper** | 8048 | Terminal e IDE | Rodar comandos, baixar modelos |

3. **Para testar**, clique em **"ComfyUI"** (porta 8188)
4. Se abrir a interface do ComfyUI com nodes, está funcionando! ✅

### 🔧 Para que serve cada ferramenta:

**ComfyUI (8188)** - Interface principal onde você vai:
- Carregar workflows
- Configurar parâmetros dos vídeos
- Gerar e visualizar resultados

**FileBrowser (8080)** - Gerenciador visual para:
- Fazer upload de imagens do seu computador
- Baixar vídeos gerados
- Navegar nas pastas de modelos
- Login padrão: `admin` / `admin`

**Zasper (8048)** - Terminal e IDE para:
- Rodar comandos `wget` para baixar modelos
- Editar arquivos de configuração
- Instalar pacotes Python

> ⚠️ **Se der erro 502 ou 503**: Aguarde mais 1-2 minutos. Os serviços ainda estão iniciando.

> ⚠️ **Se der erro de CUDA**: Você provavelmente usou o template errado. Termine o pod e crie um novo com o template `slim-5090`.

---

## 📊 COMPARATIVO DE CUSTOS (Para 1 hora de uso)

| Configuração | GPU | Cloud | Pricing | Custo/Hora |
|--------------|-----|-------|---------|------------|
| **💰 Econômico** | RTX 4090 | Community | Spot | ~$0.22* |
| **⭐ Bom custo-benefício** | RTX 4090 | Community | On-Demand | ~$0.34-0.44 |
| **🚀 RECOMENDADO** | **RTX 5090** | **Community** | **On-Demand** | **~$0.69-0.89** |
| **💎 Mais VRAM** | L40S | Community | On-Demand | ~$0.89-0.99 |
| **🏢 Enterprise** | A100 80GB | Secure | On-Demand | ~$1.89-2.09 |

*Spot pode ser interrompido a qualquer momento!

> 💡 **Por que RTX 5090 é o melhor custo-benefício para Wan 2.2?**
> - 32GB VRAM permite vídeos maiores e 720p
> - 27-35% mais rápida que RTX 4090
> - Custo por vídeo é menor devido à velocidade

---

# ETAPA 4: ACESSAR O POD E BAIXAR MODELOS (20-30 minutos)

## Passo 4.1: Acessar o Zasper (Terminal)

O template **Better ComfyUI Slim** usa **Zasper** em vez de JupyterLab. Zasper é um substituto mais leve e eficiente (usa 4x menos memória).

1. Quando o pod estiver "Running", clique em **Connect**
2. Clique em **"Zasper"** (porta 8048)
3. Uma nova aba abrirá com a interface do Zasper

> 💡 **Alternativa**: Você também pode usar o **FileBrowser** (porta 8080) para fazer upload/download de arquivos visualmente, ou **SSH** para acesso via linha de comando.

## Passo 4.2: Abrir o Terminal no Zasper

1. No Zasper, clique em **"Terminal"** no menu ou na tela inicial
2. Uma aba de terminal será aberta
3. Você verá um prompt de comando

> 📝 **Dica**: Se preferir usar SSH em vez do Zasper, vá em **Connect** → **SSH** e copie o comando de conexão.

## Passo 4.3: Baixar os Modelos do Wan 2.2 Remix

Cole estes comandos um por um no terminal:

> ⚠️ **CAMINHO CORRETO PARA ESTE TEMPLATE**: 
> O ComfyUI fica em `/workspace/madapps/ComfyUI/` (NÃO em `/workspace/ComfyUI/`!)

### Primeiro, navegue até a pasta de modelos:
```bash
cd /workspace/madapps/ComfyUI/models
```

### Baixar o modelo HIGH NOISE (expert de alto ruído):
```bash
cd diffusion_models
wget -c https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors
```

> ⏱️ **Tempo estimado**: 5-8 minutos (~14GB)

### Baixar o modelo LOW NOISE (expert de baixo ruído):
```bash
wget -c https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors
```

> ⏱️ **Tempo estimado**: 5-8 minutos (~14GB)

### Baixar o Text Encoder (codificador de texto):
```bash
cd ../text_encoders
wget -c https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
```

> ⏱️ **Tempo estimado**: 2-3 minutos (~5GB)

### Baixar o VAE:
```bash
cd ../vae
wget -c https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors
```

> ⏱️ **Tempo estimado**: 30 segundos (~500MB)

### (OPCIONAL) Baixar Lightning LoRA para gerar 5x mais rápido:
```bash
cd ../loras
mkdir -p wan_lightning
cd wan_lightning
wget -c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors"
wget -c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors"
```

> 💡 **O que é Lightning LoRA?** 
> É um "acelerador" que reduz os passos de geração de 25 para apenas 4, tornando cada vídeo ~5x mais rápido. A qualidade é levemente inferior, mas permite gerar MUITO mais vídeos por hora.

> ⚠️ **Nota**: Os links foram atualizados em Dez/2024. Os arquivos foram movidos pelo autor para uma nova pasta.

## Passo 4.4: Verificar se tudo foi baixado

```bash
# Para template slim-5090:
cd /workspace/madapps/ComfyUI/models
find . -name "*.safetensors" -type f

# Ou se estiver usando outro caminho:
# cd /workspace/ComfyUI/models
# find . -name "*.safetensors" -type f
```

Você deve ver:
```
./diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors
./diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors
./text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
./vae/wan_2.1_vae.safetensors
./loras/wan_lightning/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors
./loras/wan_lightning/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors
```

---

# ETAPA 5: ACESSAR O COMFYUI (2 minutos)

## Passo 5.1: Abrir o ComfyUI

1. Volte para a página do Runpod (aba do pod)
2. Clique em **Connect**
3. Clique em **"ComfyUI"** (porta 8188)
4. O ComfyUI abrirá em uma nova aba

> 🎉 Se você ver uma interface com nodes (caixas conectadas), parabéns! O ComfyUI está funcionando.

## Passo 5.2: Custom Nodes Pré-Instalados

O template **Better ComfyUI Slim** já vem com alguns custom nodes essenciais:

| Node | Para que serve |
|------|----------------|
| **ComfyUI-Manager** | Instalar/gerenciar outros nodes |
| **ComfyUI-Crystools** | Monitor de recursos (CPU, GPU, VRAM) |
| **ComfyUI-KJNodes** | Utilitários diversos |

## Passo 5.3: Instalar Nodes Adicionais (se necessário)

1. No ComfyUI, clique em **Manager** (botão no topo)
2. Clique em **Install Custom Nodes**
3. Pesquise e instale:
   - **ComfyUI-VideoHelperSuite** (para exportar MP4)
   - Outros nodes que o workflow pedir
4. Após instalar, clique em **Restart** para reiniciar o ComfyUI

---

# ETAPA 6: CARREGAR O WORKFLOW E GERAR VÍDEOS (5 minutos)

## Passo 6.1: Carregar o Workflow Oficial

1. No ComfyUI, clique em **Workflow** (menu superior)
2. Clique em **Browse Templates**
3. Vá até a aba **Video**
4. Encontre **"Wan2.2 14B I2V"** e clique para carregar

Se aparecer **"Missing Nodes"** (nodes faltando):
1. Clique em **Manager** → **Install Missing Custom Nodes**
2. Instale tudo que aparecer
3. Reinicie o ComfyUI

## Passo 6.2: Configurar os Modelos

No workflow carregado, verifique cada node:

| Node | Selecione |
|------|-----------|
| **Load Diffusion Model** (1º) | `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` |
| **Load Diffusion Model** (2º) | `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` |
| **Load CLIP** | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` |
| **Load VAE** | `wan_2.1_vae.safetensors` |

## Passo 6.3: Carregar sua Imagem

1. Encontre o node **Load Image**
2. Clique em **choose file to upload**
3. Selecione uma imagem do seu computador

> 💡 **Dicas para imagem**:
> - Use imagens claras e bem iluminadas
> - Resolução ideal: 720×480 ou 480×720
> - Evite imagens muito complexas para o primeiro teste

## Passo 6.4: Escrever o Prompt

Encontre o node **CLIP Text Encode** (Positive) e escreva seu prompt.

### Fórmula para prompts eficazes:
```
[Ação do sujeito] + [Movimento de câmera] + [Atmosfera/Iluminação] + [Estilo]
```

### Exemplos de prompts que funcionam bem:

**Para uma pessoa:**
```
The woman slowly turns her head toward the camera with a gentle smile. Her hair moves softly in the breeze. Soft golden hour lighting, cinematic, shallow depth of field.
```

**Para uma paisagem:**
```
Gentle waves crash on the shore as clouds drift slowly across the sky. The camera remains static. Peaceful atmosphere, natural lighting, 4K quality.
```

**Para um animal:**
```
The cat stretches lazily and yawns, then looks directly at the camera. Indoor lighting, cozy atmosphere, high detail.
```

### Prompt Negativo (no node CLIP Text Encode - Negative):
```
blurry, low quality, watermark, text, static, frozen, glitch, artifacts
```

## Passo 6.5: Configurar Parâmetros para Máxima Produção

### Para MÁXIMA VELOCIDADE (mais vídeos/hora):

| Parâmetro | Valor | Onde encontrar |
|-----------|-------|----------------|
| **Width** | 640 | Node EmptyLatentVideo |
| **Height** | 480 | Node EmptyLatentVideo |
| **Frames** | 49 | Node EmptyLatentVideo (≈3 segundos) |
| **Steps** | 20 | Node KSampler |
| **CFG** | 6 | Node KSampler |

**Tempo por vídeo**: ~3-4 minutos
**Vídeos por hora**: ~15-20

### Para QUALIDADE EQUILIBRADA:

| Parâmetro | Valor | Onde encontrar |
|-----------|-------|----------------|
| **Width** | 720 | Node EmptyLatentVideo |
| **Height** | 480 | Node EmptyLatentVideo |
| **Frames** | 65 | Node EmptyLatentVideo (≈4 segundos) |
| **Steps** | 25 | Node KSampler |
| **CFG** | 6 | Node KSampler |

**Tempo por vídeo**: ~5-7 minutos
**Vídeos por hora**: ~8-12

## Passo 6.6: GERAR!

1. Pressione **Ctrl+Enter** ou clique em **Queue Prompt**
2. Observe a barra de progresso
3. O vídeo aparecerá no node **Video Combine** quando terminar
4. Arquivos são salvos em `/workspace/ComfyUI/output/`

---

# ETAPA 7: EXPORTAR E BAIXAR VÍDEOS

## Passo 7.1: Localizar os Vídeos

Os vídeos são salvos automaticamente em:
```
/workspace/madapps/ComfyUI/output/
```

## Passo 7.2: Baixar para seu Computador

### Método 1: Via FileBrowser (Mais fácil) ⭐
1. Acesse o **FileBrowser** (porta 8080)
2. Login: `admin` / `admin` (padrão)
3. Navegue até `workspace/madapps/ComfyUI/output/`
4. Clique no arquivo de vídeo → **Download**

### Método 2: Via Interface do ComfyUI
1. No node **Video Combine**, clique no vídeo gerado
2. Use "Save As" no menu de contexto

### Método 3: Via Zasper
1. Acesse o **Zasper** (porta 8048)
2. Use o navegador de arquivos lateral para encontrar o vídeo
3. Clique com botão direito → **Download**

---

# ETAPA 8: PARAR O POD (MUITO IMPORTANTE!)

## ⚠️ NUNCA ESQUEÇA DE PARAR O POD!

Um pod rodando cobra continuamente, mesmo sem uso.

### Como parar:
1. Vá para **Pods** no menu lateral do Runpod
2. Encontre seu pod
3. Clique no botão **Stop** (ícone de pause) ou **Terminate** (ícone de lixeira)

### ⚠️ Diferença CRÍTICA entre Stop e Terminate:

#### Se você usa SECURE CLOUD + Network Volume:

| Ação | Container Disk | Network Volume | Custo enquanto parado |
|------|----------------|----------------|----------------------|
| **Stop** | ❌ Apagado | ✅ Preservado | Network Volume ($0.07/GB/mês) |
| **Terminate** | ❌ Apagado | ✅ Preservado | Network Volume ($0.07/GB/mês) |

> ✅ No Secure Cloud com Network Volume, você pode dar **TERMINATE** sem medo! Os modelos continuam salvos.

#### Se você usa COMMUNITY CLOUD (sem Network Volume):

| Ação | Container Disk | Volume Disk (/workspace) | Custo enquanto parado |
|------|----------------|--------------------------|----------------------|
| **Stop** | ❌ Apagado | ✅ Preservado | Volume Disk ($0.20/GB/mês) |
| **Terminate** | ❌ Apagado | ❌ **PERDIDO PARA SEMPRE** | $0 |

> ⚠️ **CUIDADO COMMUNITY CLOUD**: Se você der **TERMINATE**, perde todos os modelos! Faça backup antes (veja ETAPA 9).

### 💡 Quando usar STOP vs TERMINATE:

| Situação | Secure Cloud | Community Cloud |
|----------|--------------|-----------------|
| Pausa curta (horas) | STOP | STOP |
| Pausa longa (dias) | TERMINATE | STOP (caro!) ou BACKUP + TERMINATE |
| Não vai usar mais | TERMINATE | BACKUP + TERMINATE |

---

# 📊 RESUMO DE CUSTOS

## Cenário: 1 hora de uso intensivo

| Item | Custo |
|------|-------|
| RTX 4090 × 1 hora | $0.39-0.44 |
| Network Volume 100GB × 1 mês | $7.00 (rateado: ~$0.23/dia) |
| **TOTAL 1 HORA** | **~$0.50-0.70** |

## O que você consegue em 1 hora:

| Configuração | Vídeos/Hora | Custo/Vídeo |
|--------------|-------------|-------------|
| 480p, 49 frames, 20 steps | ~15-20 | ~$0.03 |
| 480p, 65 frames, 25 steps | ~8-12 | ~$0.05 |
| 720p, 81 frames, 25 steps | ~4-6 | ~$0.10 |

---

# 🛠️ SOLUÇÃO DE PROBLEMAS

## "CUDA out of memory" / Erro de memória

**Causa**: Resolução ou frames muito altos para a GPU.

**Solução**:
1. Reduza Width/Height para 480×640
2. Reduza Frames para 49
3. Se persistir, use modelo GGUF (menor)

## Nodes vermelhos / "Missing nodes"

**Causa**: Custom nodes não instalados.

**Solução**:
1. Manager → Install Missing Custom Nodes
2. Reinicie o ComfyUI

## Vídeo sai preto/corrompido

**Causa**: VAE incorreto ou erro de modelo.

**Solução**:
1. Verifique se está usando `wan_2.1_vae.safetensors`
2. Verifique se AMBOS os modelos (high e low noise) estão carregados
3. Reduza resolução para teste

## Download lento dos modelos

**Causa**: Conexão ou servidor do HuggingFace.

**Solução**:
1. Use o parâmetro `-c` no wget (continua download interrompido)
2. Tente em horário diferente
3. Use `aria2c` para downloads paralelos

---

# ETAPA 9: BACKUP DOS MODELOS (ESSENCIAL PARA COMMUNITY CLOUD!)

> ⚠️ **ESTA ETAPA É OBRIGATÓRIA SE VOCÊ USA COMMUNITY CLOUD!** Se você usa Secure Cloud com Network Volume, pode pular esta etapa.

## Por que fazer backup?

No Community Cloud, ao dar **TERMINATE** no pod, **TODOS os seus dados são perdidos para sempre**, incluindo:
- Modelos baixados (~35GB)
- Custom nodes instalados
- Vídeos gerados
- Configurações

## Quando fazer backup?

- **SEMPRE** antes de dar TERMINATE
- Periodicamente, se você tem trabalhos importantes
- Depois de baixar novos modelos ou configurar algo novo

## Opções de Backup:

### OPÇÃO 1: Cloud Sync (Integrado no Runpod) ⭐ RECOMENDADO

O Runpod tem integração nativa com serviços de cloud storage:

1. No painel do Runpod, vá para **Pods**
2. Clique no seu pod
3. Clique em **Cloud Sync**
4. Configure sua conta de storage:

| Serviço | Custo | Facilidade |
|---------|-------|------------|
| **Backblaze B2** | ~$0.005/GB/mês | ⭐⭐⭐⭐⭐ Mais barato |
| Amazon S3 | ~$0.023/GB/mês | ⭐⭐⭐⭐ |
| Google Cloud | ~$0.020/GB/mês | ⭐⭐⭐⭐ |
| Dropbox | Grátis até 2GB | ⭐⭐⭐ |

5. Selecione as pastas para sincronizar:
   - `/workspace/madapps/ComfyUI/models/` (mais importante!)
   - `/workspace/madapps/ComfyUI/custom_nodes/`
   - `/workspace/madapps/ComfyUI/output/`

### OPÇÃO 2: rclone para Google Drive

O Cloud Sync **NÃO suporta** Google Drive diretamente. Use rclone:

```bash
# Instalar rclone
curl https://rclone.org/install.sh | sudo bash

# Configurar Google Drive
rclone config
# Siga as instruções para adicionar "gdrive"

# Fazer backup dos modelos
rclone sync -P /workspace/madapps/ComfyUI/models gdrive:runpod-backup/models

# Para restaurar depois:
rclone sync -P gdrive:runpod-backup/models /workspace/madapps/ComfyUI/models
```

### OPÇÃO 3: runpodctl (Transferência direta para seu PC)

O `runpodctl` já vem instalado em todos os pods:

```bash
# No pod - criar código de transferência
runpodctl send /workspace/madapps/ComfyUI/models
# Output: Code is: 8338-galileo-collect-fidel

# No seu computador - receber os arquivos
# Primeiro instale: https://github.com/runpod/runpodctl
runpodctl receive 8338-galileo-collect-fidel
```

> ⚠️ **Nota**: runpodctl é melhor para arquivos menores. Para ~35GB de modelos, use Cloud Sync ou rclone.

### OPÇÃO 4: Não fazer backup (re-baixar modelos)

Se você tem boa conexão de internet e não quer se preocupar com backup:

1. Salve este tutorial (tem todos os comandos de download)
2. Quando criar novo pod, execute os comandos da ETAPA 4 novamente
3. Tempo: ~20-30 minutos para re-baixar tudo

**Custo-benefício**: Se você usa pouco (1-2x/mês), pode ser mais barato re-baixar do que pagar storage.

## 📊 Comparativo de Custos de Storage

| Opção | Custo Mensal (100GB) | Prós | Contras |
|-------|---------------------|------|---------|
| Volume Disk parado | **$20/mês** | Simples | Muito caro! |
| Network Volume (Secure) | **$7/mês** | Automático | Requer Secure Cloud |
| Backblaze B2 | **$0.50/mês** | Muito barato | Precisa configurar |
| Google Drive (grátis) | **$0** | Grátis | Limite 15GB |
| Re-baixar | **$0** | Zero custo | Perde 30min toda vez |

> 💡 **Recomendação**: Para uso frequente, Backblaze B2 + Cloud Sync é a melhor opção!

---

# ✅ CHECKLIST RÁPIDO

## Primeira vez - SECURE CLOUD (setup ~40 min):
- [ ] Criar conta no Runpod
- [ ] Adicionar $10 de créditos
- [ ] Criar Network Volume (100GB, região EU-RO-1 ou EUR-IS-1)
- [ ] Criar Pod em **Secure Cloud** com RTX 5090 + template `slim-5090`
- [ ] Conectar o Network Volume ao pod
- [ ] Acessar **Zasper** (porta 8048) e baixar modelos
- [ ] Instalar custom nodes necessários

## Primeira vez - COMMUNITY CLOUD (setup ~40 min):
- [ ] Criar conta no Runpod
- [ ] Adicionar $10 de créditos
- [ ] Criar Pod em **Community Cloud** com RTX 5090 + template `slim-5090`
- [ ] Configurar Volume Disk com 100GB
- [ ] Acessar **Zasper** (porta 8048) e baixar modelos
- [ ] Instalar custom nodes necessários
- [ ] ⚠️ Configurar backup (Cloud Sync ou rclone) - ESSENCIAL!

## Sessões seguintes (início ~2 min):
- [ ] Ligar o Pod (Start)
- [ ] Aguardar ~1-2 minutos
- [ ] Abrir **ComfyUI** (porta 8188)
- [ ] Carregar workflow
- [ ] Gerar vídeos!
- [ ] **PARAR O POD ao terminar** ⚠️
- [ ] ⚠️ (Community Cloud) Fazer backup antes de TERMINATE!

## Portas do template Better ComfyUI Slim:
| Porta | Serviço |
|-------|---------|
| **8188** | ComfyUI (interface principal) |
| **8080** | FileBrowser (gerenciador de arquivos) |
| **8048** | Zasper (terminal/IDE) |
| **22** | SSH |

---

# 🔗 LINKS ÚTEIS

| Recurso | Link |
|---------|------|
| Modelos Oficiais Wan 2.2 | huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged |
| Wan 2.2 Remix (NSFW) | huggingface.co/FX-FeiHou/wan2.2-Remix |
| Lightning LoRA | huggingface.co/Kijai/WanVideo_comfy |
| Documentação ComfyUI | docs.comfy.org/tutorials/video/wan/wan2_2 |
| Workflows Prontos | comfyanonymous.github.io/ComfyUI_examples/wan22/ |

---

**🎬 Pronto! Agora você sabe configurar e usar o Wan 2.2 no Runpod do zero ao vídeo final!**

**Lembre-se:**
- ✅ **Secure Cloud**: Dados persistem no Network Volume, pode dar TERMINATE sem medo
- ⚠️ **Community Cloud**: Faça backup antes de TERMINATE ou perde tudo!
- 💰 A chave para economia é **sempre parar o pod quando terminar**

Com boas práticas, você pode gerar dezenas de vídeos por menos de $1!
