# Requisitos de Inferência Local do Qwen3 4B para Dispositivos Móveis

O Qwen3 4B pode ser executado em smartphones modernos com **8GB de RAM** ou mais, usando quantização de 4 bits (Q4_K_M). iPhones a partir do modelo 15 Pro e dispositivos Android com Snapdragon 8 Gen 2 ou superior conseguem atingir velocidades utilizáveis de **10-22 tokens por segundo**. A quantização Q4_K_M, que ocupa apenas **2,5GB**, oferece o melhor equilíbrio entre qualidade e desempenho para uso móvel, permitindo contextos de até 4K tokens sem problemas de memória.

## Especificações oficiais do modelo Qwen3 4B

O Qwen3 4B possui **4 bilhões de parâmetros** (3,6B excluindo embeddings), utilizando arquitetura Transformer densa com 36 camadas e atenção de consulta agrupada (GQA) com 32 cabeças de atenção e 8 cabeças KV. A Alibaba/Qwen disponibiliza oficialmente versões quantizadas em formato GGUF, desde Q4_K_M (2,5GB) até Q8_0 (4,28GB), com contexto nativo de **32.768 tokens** extensível até 131K com YaRN.

Para implantação móvel, a documentação oficial recomenda três frameworks principais: **ExecuTorch** (iOS e Android), **MNN** (framework próprio da Alibaba otimizado para Qwen) e **llama.cpp** (versão b5401 ou superior). A equipe Qwen não publica requisitos mínimos de hardware explícitos, deixando essas especificações para serem derivadas dos tamanhos dos modelos quantizados.

## Requisitos completos para iPhone

A tabela abaixo resume as especificações necessárias para executar o Qwen3 4B em dispositivos iOS:

| Especificação | Mínimo | Recomendado |
|--------------|--------|-------------|
| Modelo iPhone | iPhone 14 Pro | iPhone 15 Pro ou superior |
| Chip A-series | A16 Bionic | A17 Pro ou A18 Pro |
| RAM | 6GB | 8GB |
| Versão iOS | iOS 15 | iOS 17+ (iOS 18 para Core ML otimizado) |
| Quantização | Q4_K_M obrigatório | Q4_K_M ou Q5_K_M |

Os modelos confirmados como funcionais incluem: **iPhone 14 Pro/Pro Max** (6GB RAM, A16 Bionic) com desempenho marginal usando apenas Q4_K_M; **iPhone 15 Pro/Pro Max** (8GB RAM, A17 Pro) como opção recomendada com ~18-22 tokens/segundo; **iPhone 16/16 Pro** (8GB RAM, A18/A18 Pro) com excelente desempenho de ~20-25 tokens/segundo; e **iPhone 17 Pro/Air** (8-12GB RAM, A19) como opção ideal com ~25-30 tokens/segundo.

O framework **llama.cpp com GGUF** representa a escolha mais madura para iOS, oferecendo aceleração Metal GPU nativa e ampla compatibilidade. Aplicativos como Private LLM, LLMFarm e Enclave AI utilizam este backend. O Core ML com modelos stateful no iOS 18+ pode oferecer até **13x mais velocidade** no cache KV, mas requer conversão de modelo mais complexa.

## Requisitos completos para Android

A tabela abaixo apresenta as especificações para dispositivos Android:

| Especificação | Mínimo | Recomendado |
|--------------|--------|-------------|
| RAM | 8GB | 12GB |
| Processador | Snapdragon 8 Gen 1 | Snapdragon 8 Gen 3 ou Dimensity 9300 |
| GPU | Adreno 730 | Adreno 750 |
| Quantização | Q4_K_M | Q4_K_M ou Q5_K_M |

### Compatibilidade detalhada por processador

**Qualcomm Snapdragon:**
- **8 Elite e 8 Gen 3**: Totalmente recomendados, ~20 tokens/segundo, melhor suporte NPU
- **8 Gen 2**: Muito bom, ~12-15 tokens/segundo estimados
- **8 Gen 1 e 8+ Gen 1**: Suportados, mas com problemas de throttling térmico
- **870 e inferiores**: Marginais, apenas ~4-5 tokens/segundo

**MediaTek Dimensity:**
- **9300**: Melhor desempenho geral, design all-big-core, **3x mais rápido** que SD870
- **9200 e 8300**: Suportados com bom desempenho
- **9000**: Marginal, design mais antigo

**Google Tensor:**
- **G4 e G3** (Pixel 9/8): Suportados mas moderados, GPU Mali menos otimizada
- **G2**: Marginal, restrições térmicas significativas

**Samsung Exynos:**
- **2400**: Provavelmente funcional, dados limitados
- **2200 e anteriores**: Não recomendados, desempenho inferior

Uma descoberta crítica dos testes comunitários: GPUs **Adreno superam Mali em 1,6-5x** nas tarefas de LLM devido à melhor otimização dos kernels OpenCL. Dispositivos com Mali-G720 atingem apenas **3-5% de utilização ALU** durante o prefill, resultando em desempenho drasticamente inferior.

## Impacto da quantização no desempenho móvel

| Quantização | RAM Necessária | Impacto na Velocidade | Impacto na Qualidade |
|-------------|----------------|----------------------|---------------------|
| Q4_K_M | ~2,8GB (com 4K ctx) | 100% (baseline) | +1% perplexidade |
| Q5_K_M | ~3,2GB (com 4K ctx) | ~95% | +0,6% perplexidade |
| Q8_0 | ~4,6GB (com 4K ctx) | ~85-90% | +0,2% perplexidade |

O **Q4_K_M é a escolha ideal para dispositivos móveis**, oferecendo degradação de qualidade mínima (~1% de aumento na perplexidade) com o menor consumo de memória. A diferença prática entre Q4_K_M e Q8_0 é imperceptível para a maioria das tarefas conversacionais, mas Q8_0 pode beneficiar tarefas de raciocínio complexo ou programação.

### Overhead de memória por tamanho de contexto

O cache KV adiciona memória significativa conforme o contexto aumenta:

| Contexto | Cache KV | Q4_K_M Total | Q8_0 Total |
|----------|----------|--------------|------------|
| 2K tokens | ~0,15GB | ~2,65GB | ~4,45GB |
| 4K tokens | ~0,30GB | ~2,80GB | ~4,60GB |
| 8K tokens | ~0,60GB | ~3,10GB | ~4,90GB |
| 16K tokens | ~1,20GB | ~3,70GB | ~5,50GB |

Para dispositivos com 8GB de RAM, recomenda-se limitar o contexto a **4K-8K tokens** com Q4_K_M para operação estável.

## Benchmarks de velocidade por categoria de dispositivo

### iPhone (llama.cpp, Q4_K_M)
| Dispositivo | Tokens/segundo estimados |
|------------|-------------------------|
| iPhone 15 Pro (A17 Pro) | **18-22 t/s** |
| iPhone 16 Pro (A18 Pro) | **20-25 t/s** |
| iPhone Air (A19) | **25-30 t/s** |
| iPhone 14 Pro (A16) | ~15-18 t/s |

### Android (llama.cpp CPU, 4-bit)
| Processador | Prefill (t/s) | Decodificação (t/s) |
|------------|---------------|---------------------|
| Dimensity 9300 | 45-56 | **8-12** |
| Snapdragon 8 Gen 3 | 35-45 | **7-10** |
| Snapdragon 8+ Gen 1 | 20-28 | 5-7 |
| Kirin 9000E | 15-20 | 4-5 |

A velocidade mínima considerada utilizável é de **3 tokens/segundo** (baseado em pesquisas de UX que indicam 400ms por token como limite). Velocidades acima de **10 t/s** proporcionam experiência confortável.

## Problemas comuns e soluções

### Erros de memória insuficiente (OOM)

Uma limitação crítica descoberta nos testes: dispositivos Pixel (5-8 Pro) possuem um **limite de 4,35GB para memória GPU** em cargas de trabalho LLM, independentemente da RAM total do dispositivo. Isso significa que modelos Q8_0 do Qwen3 4B (~4,6GB com contexto) podem falhar mesmo em dispositivos com 12GB de RAM.

**Soluções:**
- Usar quantização Q4_K_M obrigatoriamente em dispositivos com 6-8GB
- Limitar contexto a 2K-4K tokens em dispositivos com restrições de memória
- Fechar aplicativos em segundo plano antes de executar o modelo

### Throttling térmico

Testes acadêmicos revelaram que dispositivos **Snapdragon 8 Gen 3 podem ter frequência reduzida pela metade** após aproximadamente 9 rodadas de inferência contínua, resultando em degradação de **30% no desempenho**. Processadores Dimensity e Kirin demonstraram comportamento mais estável (~10% de degradação).

**Mitigações:**
- Remover capas do dispositivo durante uso prolongado
- Evitar carregar o dispositivo durante inferência
- Permitir intervalos entre consultas longas

### Problemas específicos por framework

No **MLC-LLM**, usar layout de peso `_0` ao invés de `_1` em GPUs Adreno resolve travamentos de UI de 20-50 segundos durante o prefill. Para dispositivos Samsung, preferir `q4f16_0` em vez de `q4f16_1` para evitar desligamentos do dispositivo.

No **llama.cpp**, configurar o número de threads igual ao número de núcleos grandes (big cores) apenas, não incluindo núcleos de eficiência, que frequentemente degradam o desempenho.

## Seleção de framework para inferência

| Framework | Pontos Fortes | Melhor Uso |
|-----------|--------------|------------|
| **llama.cpp** | Mais maduro, ampla compatibilidade GGUF, Metal no iOS, OpenCL no Android | Inferência CPU, máxima compatibilidade |
| **MLC-LLM** | Aceleração GPU nativa, app Android disponível | Dispositivos com Adreno GPU |
| **MNN** | Framework oficial Alibaba, otimizado para Qwen | Melhor integração com Qwen3 |
| **ExecuTorch** | Suporte oficial Qwen3, multiplataforma | Desenvolvimento profissional |
| **Core ML** | Melhor uso do Neural Engine, iOS 18+ stateful | Performance máxima em iPhone |

Para **implantação rápida**, llama.cpp via aplicativos como Private LLM (iOS) ou MLC Chat (Android) oferece a menor barreira de entrada. Para **desenvolvimento personalizado**, ExecuTorch ou MNN são recomendados pela equipe Qwen.

## Recomendações finais por caso de uso

**Assistente de chat básico (8GB RAM):**
- Quantização: Q4_K_M (2,5GB)
- Contexto: 2K-4K tokens
- Velocidade esperada: 10-15 t/s em flagships

**Programação e raciocínio (12GB+ RAM):**
- Quantização: Q5_K_M ou Q8_0
- Contexto: 4K-8K tokens
- Velocidade esperada: 8-12 t/s

**Análise de documentos longos (12GB+ RAM):**
- Quantização: Q4_K_M (para maximizar contexto disponível)
- Contexto: 8K-16K tokens
- Velocidade esperada: 5-10 t/s

## Conclusão

O Qwen3 4B representa uma opção viável para inferência local em smartphones modernos, com a ressalva de que **hardware de 2024 ou mais recente** é praticamente obrigatório para experiência satisfatória. A combinação de iPhone 15 Pro ou superior, ou Android com Snapdragon 8 Gen 2+ e 8GB de RAM, usando quantização Q4_K_M via llama.cpp, proporciona velocidades de **15-25 tokens/segundo** — suficiente para uso conversacional interativo.

A principal limitação identificada é o **limite de memória GPU em dispositivos Android**, que restringe modelos maiores independentemente da RAM total. Para maximizar compatibilidade, Q4_K_M com contexto de 4K tokens deve ser a configuração padrão, ajustando apenas em dispositivos com 12GB+ de RAM confirmados como funcionais.