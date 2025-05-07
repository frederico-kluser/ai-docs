# Comparativo de APIs LLM: Limites de uso e preços em 2025

O panorama das APIs de grandes modelos de linguagem evoluiu significativamente até o início de 2025, com provedores competindo tanto em preços quanto em acessibilidade. Esta comparação examina as atuais restrições de uso e estruturas de preços entre os principais provedores de APIs LLM, destacando diferenças-chave que impactam as escolhas dos desenvolvedores para implantações em produção.

## Ofertas de nível gratuito: De generosas a inexistentes

Cada provedor adota uma abordagem dramaticamente diferente para uso gratuito, com alguns oferecendo tokens gratuitos substanciais enquanto outros não fornecem nenhum nível gratuito:

| Provedor | Tokens Mensais Gratuitos | Limites de Taxa (Nível Gratuito) | Modelos Disponíveis | Notas Adicionais |
|----------|---------------------|-------------------------|------------------|-----------------|
| Anthropic | Uso máximo de $10 | 5 RPM, 20K ITPM, 8K OTPM | Claude 3.5 Sonnet | Limite diário de 300K tokens |
| DeepSeek | Sem nível gratuito oficial | N/A | N/A | Disponível na prévia do Azure a $0 |
| Google Gemini | Ilimitado para modelos gratuitos | Gemini 2.5 Flash: 10 RPM, 250K TPM, 500 RPD | Todos os modelos com limites | Modelos Pro: 2 RPM, 32K TPM, 50 RPD |
| OpenAI | Crédito inicial de $5 + Tokens Diários Gratuitos (1-10M) | Severamente restrito | Acesso limitado | Tokens gratuitos requerem compartilhamento de dados |
| Azure OpenAI | Crédito de $200 (30 dias) | 1K TPM para todos os modelos | Modelos limitados | Usuários de teste gratuito têm cota zero para modelos avançados |
| Ollama | Ilimitado (código aberto) | Dependente do hardware | Todos os modelos disponíveis | Apenas implantação local |

## Limites de nível pago: Equilibrando throughput e custo

Existem variações significativas na forma como os provedores estruturam seus níveis pagos e o throughput máximo permitido:

| Provedor | Estrutura de Níveis | RPM do Nível Padrão | TPM do Nível Padrão | Máximo do Nível Empresarial |
|----------|----------------|-------------------|-------------------|--------------------------|
| Anthropic | Baseado em uso ($5-$400) | 50 RPM | Varia por modelo | Personalizado via vendas |
| DeepSeek | Sem níveis explícitos | "Sem restrições" | Ilimitado (alegado) | Arranjos personalizados disponíveis |
| Google Gemini | 3 níveis baseados em uso | Gemini 2.5 Flash: 1K RPM | 1M TPM | Nível 3: 5K+ RPM, 10M+ TPM |
| OpenAI | 5 níveis baseados em gastos | Nível 1: Varia por modelo | Varia por modelo | Nível 5: ~10K RPM, 30M TPM |
| Azure OpenAI | Padrão e Empresarial | GPT-4o: 2,7K RPM | 450K TPM | GPT-4o: 180K RPM, 30M TPM |
| Ollama | N/A (auto-hospedado) | Configurável (padrão: 4) | Dependente do hardware | Dependente do hardware |

## Requisições simultâneas: O desafio da concorrência

Limites de taxa impactam significativamente a arquitetura da aplicação, com amplas variações no processamento concorrente permitido:

| Provedor | Limite de Requisições Concorrentes | Método de Limitação de Taxa | Capacidade de Pico | Sistema de Fila |
|----------|--------------------------|----------------------|------------------|--------------|
| Anthropic | Nível gratuito: 1, Pago: Baseado em RPM | Algoritmo de token bucket | Sim | API de Lotes de Mensagens: fila máx. 100K |
| DeepSeek | Nenhum limite específico mencionado | Sem limites de taxa explícitos | N/A | Conexões permanecem abertas durante tráfego alto |
| Google Gemini | Gratuito: 3 sessões concorrentes | Limites por projeto | Limitado | Limites TPM e RPM aplicados |
| OpenAI | Baseado em nível e modelo | Três níveis (RPM, RPD, TPM) | Limitado | GPT-4o Nível 5: limite de fila em lote de 5B |
| Azure OpenAI | Baseado na proporção RPM/TPM | Varia por família de modelo | Limitado | API em Lote tem limites de fila separados |
| Ollama | Padrão: 4 por modelo | Contador simples | Não | Fila máxima: 512 requisições |

## Preços: A economia de tokens

**Os preços dos modelos variam dramaticamente entre provedores, com diferenças de até 30x para capacidades comparáveis:**

| Provedor | Preço de Token de Entrada (por milhão) | Preço de Token de Saída (por milhão) | Tamanho da Janela de Contexto | Características Especiais de Preço |
|----------|--------------------------------|----------------------------------|---------------------|-------------------------|
| Anthropic | Claude 3 Opus: $15<br>Claude 3 Sonnet: $3<br>Claude 3 Haiku: $0,25 | Claude 3 Opus: $75<br>Claude 3 Sonnet: $15<br>Claude 3 Haiku: $1,25 | 200K tokens todos os modelos | Cache de prompt disponível |
| DeepSeek | DeepSeek-V3: $0,27<br>DeepSeek-R1: $0,55 | DeepSeek-V3: $1,10<br>DeepSeek-R1: $2,19 | 64K tokens | Descontos fora de pico<br>Desconto de cache hit: 74-75% |
| Google Gemini | Gemini 2.5 Pro: $1,25-$2,50<br>Gemini 2.5 Flash: $0,15<br>Gemini 1.5 Flash-8B: $0,0375 | Gemini 2.5 Pro: $10-$15<br>Gemini 2.5 Flash: $0,60<br>Gemini 1.5 Flash-8B: $0,15-$0,30 | Gemini 2.5 Pro: 1M tokens<br>Gemini 2.0 Flash: 1M tokens | Preços em níveis para contextos grandes<br>Taxas de armazenamento de contexto |
| OpenAI | GPT-4.1: $2<br>GPT-4o: $3<br>GPT-4o mini: $0,15 | GPT-4.1: $8<br>GPT-4o: $10<br>GPT-4o mini: $0,60 | GPT-4.1: 1M tokens<br>GPT-4o: 128K tokens | 75% de desconto para prompts em cache<br>50% de desconto em lote |
| Azure OpenAI | Similar à OpenAI com variações por tipo de implantação | Similar à OpenAI com variações por tipo de implantação | Varia por modelo | Implantações Globais/Zona de Dados/Regionais<br>Unidades de Throughput Provisionadas |
| Ollama | $0 (apenas custos de computação local) | $0 (apenas custos de computação local) | Padrão: 4K (configurável) | Apenas custos de hardware |

## Outras restrições de uso: As letras miúdas

Além dos limites principais e preços, os provedores implementam restrições adicionais que impactam significativamente o design da aplicação:

| Provedor | Limitações Especiais | Mudanças Recentes | Vantagens Principais |
|----------|---------------------|----------------|----------------|
| Anthropic | Contagem de tokens varia para prompts em cache | Novo Plano Max com limites de taxa mais altos<br>Claude 3.7 Sonnet com pensamento estendido | 128K tokens de saída no modo de pensamento estendido<br>Limites de gasto personalizados por workspace |
| DeepSeek | Tamanho mínimo de cache: 64 tokens<br>Timeout de conexão de 30 minutos | Atualizado para DeepSeek-V3<br>Lançado sob Licença MIT | Sem limites de taxa explícitos<br>Descontos significativos de cache |
| Google Gemini | Grounding com Pesquisa: 500 gratuitos/dia depois $35 por 1K<br>Geração de imagem: $0,03/imagem | Gemini 2.5 Pro introduzido em maio de 2025<br>Preços em níveis para contextos maiores | Capacidades multimodais incluídas<br>Nível gratuito generoso |
| OpenAI | Desempenho degrada com >10 requisições concorrentes<br>Processamento de áudio tem preços separados | Novos modelos GPT-4.1 (abril de 2025)<br>Queda de preço de 83-90% em 16 meses | API em Lote com 50% de desconto<br>75% de desconto em prompt em cache |
| Azure OpenAI | Máximo de 30 instâncias de recurso por região<br>Níveis de desempenho baseados em uso mensal | Novas opções de implantação (Global/Zona de Dados)<br>Remoção de restrições de implantação de modelo | Três tipos de implantação para necessidades de conformidade<br>Recurso de spillover para gerenciamento de tráfego |
| Ollama | Limitações dependentes de hardware<br>Licenças específicas do modelo podem ser aplicáveis | Nova configuração de tamanho de contexto<br>Suporte a chamada de função melhorado | Completamente configurável<br>Sem custos baseados em uso |

## Conclusão

A seleção de provedor permanece altamente dependente de casos de uso específicos. Google Gemini oferece o nível gratuito mais generoso para desenvolvedores, enquanto DeepSeek afirma throughput ilimitado para aplicações de alto volume. Anthropic proporciona equilíbrio com preços moderados e limites de taxa claros, enquanto OpenAI continua com reduções agressivas de preço. Azure adiciona opções de conformidade através de tipos de implantação regionais, e Ollama fornece uma opção de custo-benefício para aqueles dispostos a gerenciar sua própria infraestrutura. Considere seus requisitos específicos de throughput, orçamento e recursos ao fazer sua seleção.