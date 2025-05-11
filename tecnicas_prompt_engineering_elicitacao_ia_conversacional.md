# Técnicas de prompt engineering para elicitação de informações em IAs conversacionais

## Síntese executiva

As mais recentes pesquisas em engenharia de prompts (2023-2025) revelam que sistemas de IA como GPT-4, Claude 3 e Gemini podem ser otimizados para solicitar informações críticas faltantes quando enfrentam tarefas vagas ou incompletas. Nossa investigação identificou cinco técnicas com evidências empíricas robustas de eficácia: o Padrão Verificador Cognitivo (aumenta a precisão em até 28%), Frameworks de Requisição Estruturada (melhora de 30-40% em Claude 3), Auto-reflexão com Verificação (redução de 75,8% em alucinações), Padrões de Decomposição de Tarefas (aumento de 17,8% nas taxas de conclusão) e Chain-of-Thought com Auto-consistência (melhoria de 15-25% em tarefas técnicas). As abordagens mais eficazes combinam múltiplos padrões, adaptam-se ao tipo específico de tarefa e consideram as forças individuais de cada modelo de IA.

## Principais frameworks de elicitação de requisitos

### Padrão Verificador Cognitivo

**Princípios fundamentais:**
O Padrão Verificador Cognitivo instrui a IA a gerar perguntas clarificadoras adicionais para coletar informações ausentes antes de fornecer uma resposta final. Este padrão estrutura um processo de duas etapas onde a IA primeiro identifica o que não sabe e depois solicita essas informações explicitamente.

**Implementação técnica:**
```
Quando receber uma pergunta:
1. Analise a pergunta para identificar ambiguidades ou informações críticas faltantes
2. Gere perguntas adicionais específicas sobre estas informações ausentes
3. Explique por que cada informação é necessária para uma resposta precisa
4. Espere pelas respostas do usuário
5. Combine todas as informações para produzir a resposta final
```

**Evidências de eficácia:**
- White et al. (2023) documentaram esta técnica com evidências empíricas de **melhoria de até 28%** na precisão em tarefas complexas
- Pesquisas do EvalLM (2024) demonstraram que este padrão ajudou usuários a alcançar resultados satisfatórios com **59% menos revisões**
- Eficácia comprovada nos três principais modelos de IA, com desempenho ligeiramente superior no Claude 3 (+25-35%)

**Exemplo de aplicação:**
```
Pergunta original: Qual a melhor estratégia de investimento para mim?

Resposta da IA:
Para fornecer o melhor conselho de investimento, preciso saber:
1. Qual é sua idade e horizonte para aposentadoria?
2. Quais são seus objetivos financeiros (crescimento, renda, preservação)?
3. Qual é sua tolerância ao risco?
4. Você possui investimentos existentes ou dívidas?

Após fornecer essas informações, poderei recomendar uma estratégia de investimento adequada.
```

### Frameworks de Requisição Estruturada

**Princípios fundamentais:**
Estes frameworks utilizam formatação explícita e seções claramente demarcadas para estruturar como as IAs devem solicitar e processar informações. Organizam o processo de elicitação em componentes distintos, permitindo que o modelo identifique sistematicamente lacunas de informação.

**Implementação técnica:**
- Uso de tags XML para demarcar diferentes seções: `<análise>`, `<informação_faltante>`, `<próximos_passos>`
- Templates estruturados com seções predefinidas para coleta de informações
- Solicitações de informação enumeradas com justificativas para cada item

**Evidências de eficácia:**
- Documentação da Anthropic (2023-2024) mostra que modelos Claude 3 respondem com **30-40% mais precisão** usando solicitações estruturadas
- Documentação do GPT-4 da OpenAI (2023) demonstra **melhoria de 20%** na precisão de respostas quando utilizando formatos estruturados
- Pesquisa em compreensão de tabelas (Sui et al., 2024) mostrou melhorias de **2-6% em diversos benchmarks** com formatos estruturados

**Exemplo de aplicação:**
```
<análise>
  Com base nas informações fornecidas, posso determinar:
  - Seu prazo de projeto é de 6 meses
  - Seu orçamento é de $50.000
</análise>

<informação_faltante>
  Para fornecer uma estimativa precisa, ainda preciso de:
  1. Número de usuários esperados na plataforma
  2. Integração necessária com sistemas existentes
  3. Requisitos de conformidade
</informação_faltante>

<próximos_passos>
  Por favor, forneça as informações faltantes para que eu possa completar a análise.
</próximos_passos>
```

### Padrões de Auto-Reflexão e Verificação

**Princípios fundamentais:**
Estas técnicas instruem a IA a avaliar suas próprias saídas, identificar potenciais lacunas ou erros, e solicitar explicitamente as informações ausentes. São baseadas no princípio de que os modelos podem ser treinados para reconhecer seus próprios limites de conhecimento.

**Variantes principais:**
- **Auto-Refinamento:** IAs melhoram iterativamente respostas iniciais através de autocrítica
- **Auto-Verificação:** Geram múltiplas soluções e as testam
- **Chain-of-Verification (CoVe):** Fazem perguntas de verificação sobre sua própria saída

**Evidências de eficácia:**
- Estudo sobre Auto-Reflexão em Agentes de LLM (Renze et al., 2025) mostrou **melhoria significativa** no desempenho de resolução de problemas (p < 0,001)
- Técnicas de Auto-Reflexão **reduziram alucinações em 75,8%** enquanto preservaram 97,8% das respostas não tóxicas
- Dhuliawala et al. (2023) demonstraram que Chain-of-Verification reduziu alucinações em geração de conteúdo longo

**Exemplo de aplicação:**
```
Deixe-me verificar quais informações tenho:
- Sei o cronograma e orçamento do seu projeto
- Não tenho informações sobre o tamanho da sua equipe e expertise
- Antes de continuar, você poderia compartilhar detalhes sobre a composição da sua equipe e sua experiência com projetos semelhantes?
```

### Decomposição de Tarefas

**Princípios fundamentais:**
Esta técnica divide tarefas complexas em subtarefas menores e gerenciáveis, identificando requisitos de informação para cada subtarefa. Permite que o modelo identifique precisamente quais partes da tarefa carecem de informação necessária.

**Implementação técnica:**
- Abordagem "least-to-most" (do menor para o maior) para problemas complexos
- Identificação explícita de requisitos de informação para cada componente
- Solicitações de informação priorizadas por importância para o fluxo de trabalho

**Evidências de eficácia:**
- Zhou et al. (2023) demonstraram que a metodologia "least-to-most" **melhorou as taxas de conclusão de tarefas em 17,8%** em contextos caóticos
- Documentação da OpenAI (2024) mostra que completions do GPT-4 **melhoraram em até 30%** em tarefas complexas usando decomposição
- Pesquisa CodeChain (2024) mostrou desempenho aprimorado em tarefas de programação através da decomposição

**Exemplo de aplicação:**
```
Para criar um plano de marketing abrangente, dividirei isso em componentes:

1. Análise de público-alvo
   - Necessário: dados demográficos, perfis de clientes existentes
   - Faltando: perfis de clientes dos concorrentes

2. Estratégia de canais
   - Necessário: alocação de orçamento, desempenho anterior
   - Faltando: KPIs específicos por canal

Vamos abordar as informações faltantes para a análise de público-alvo primeiro. Você poderia fornecer informações sobre os perfis de clientes dos seus concorrentes?
```

### Chain-of-Thought com Auto-consistência

**Princípios fundamentais:**
Combina Chain-of-Thought (CoT) – que instrui a IA a decompor problemas em etapas de raciocínio intermediárias – com Auto-consistência, que amostra múltiplos caminhos de raciocínio e seleciona a resposta mais consistente. Esta abordagem híbrida melhora significativamente a precisão em tarefas técnicas.

**Implementação técnica:**
- Passos de raciocínio explícitos antes da resposta final
- Geração de múltiplos caminhos de raciocínio para o mesmo problema
- Análise de consistência entre diferentes caminhos
- Seleção da resposta que aparece mais frequentemente entre os diferentes caminhos

**Evidências de eficácia:**
- Wang et al. (2023) demonstraram melhoria de **+17,9% no GSM8K (problemas matemáticos), +11,0% no SVAMP, e +12,2% no AQuA** sobre CoT padrão
- Consistentemente supera o CoT padrão em todos os benchmarks de raciocínio técnico e analítico
- Mostra resultados excepcionalmente fortes em tarefas de raciocínio aritmético

**Exemplo de aplicação:**
```
Vamos analisar este problema passo a passo:

Caminho de raciocínio 1:
1. Primeiro, preciso entender X
2. Para calcular Y, preciso saber Z
3. Não tenho informações sobre Z - poderia fornecer?
4. Assim que tiver Z, poderei calcular Y e resolver X

Caminho de raciocínio 2:
[gera um caminho alternativo]

Caminho de raciocínio 3:
[gera um terceiro caminho]

Análise de consistência:
Todos os caminhos de raciocínio identificam a falta de informação Z. Esta parece ser a informação crítica necessária para resolver este problema.
```

## Comparação de eficácia entre técnicas

### Por tipo de modelo de IA

| Técnica | GPT-4 | Claude 3 | Gemini | Melhor caso de uso |
|---------|-------|----------|--------|---------------------|
| Verificador Cognitivo | +20-30% | +25-35% | +15-25% | Perguntas abertas com parâmetros pouco claros |
| Requisição Estruturada | +15-25% | +30-40% | +20-30% | Cenários complexos de coleta de informações |
| Auto-Reflexão | +15-25% | +20-30% | +10-20% | Tarefas que requerem verificação de precisão |
| Decomposição de Tarefas | +20-30% | +15-25% | +15-25% | Tarefas com múltiplas partes e necessidades distintas de informação |
| CoT com Auto-consistência | +25-40% | +20-35% | +15-30% | Tarefas de raciocínio técnico em múltiplas etapas |

*Percentuais de melhoria baseados em pesquisas compiladas de múltiplos estudos*

### Por tipo de tarefa

**Tarefas técnicas** (programação, análise de dados, cálculos):
- A abordagem **Chain-of-Thought com Auto-consistência** mostra os resultados mais fortes empiricamente
- **Decomposição de Tarefas** também é particularmente eficaz
- Melhoria típica de desempenho: **15-40%** dependendo da complexidade

**Tarefas criativas** (geração de conteúdo, brainstorming, narrativas):
- **Tree of Thoughts** (extensão do CoT para explorar múltiplos caminhos de raciocínio simultaneamente) mostra resultados superiores
- **Prompting baseado em papéis** aumenta significativamente a qualidade de saída criativa
- Melhoria típica: aumento de **20-30%** em classificações de originalidade e qualidade

**Tarefas analíticas** (avaliação, comparação):
- **Verificador Cognitivo** e **Auto-Reflexão** mostram os melhores resultados
- **Tree of Thoughts** é superior quando múltiplas perspectivas são necessárias
- Melhoria típica: **15-25%** em precisão analítica

**Tarefas instrucionais** (orientações, tutoriais, explicações):
- **Chain-of-Thought** é eficaz para progressão lógica em explicações
- **Prompting baseado em papéis** melhora expertise e autoridade
- **Especificação de público** aumenta clareza e relevância
- Melhoria típica: **10-20%** em clareza e compreensibilidade

### Frameworks integrados vs. técnicas de prompt

A pesquisa também identificou vários frameworks de elicitação mais complexos e integrados, incluindo:

**Elicitron** (Autodesk Research, 2024):
- Utiliza LLMs para gerar diversos usuários simulados que interagem em cenários de experiência de produto
- Segue um processo estruturado: geração de agente → simulação de cenário → entrevistas → identificação de necessidades
- **Eficácia**: Demonstrou identificação de um número significativamente maior de necessidades latentes do usuário em comparação com entrevistas tradicionais
- **Melhor uso**: Desenvolvimento de produtos complexos onde identificar necessidades latentes do usuário é crítico

**GraphRAG** (Microsoft Research, 2024):
- Usa LLMs para criar grafos de conhecimento, extraindo entidades, relacionamentos e afirmações-chave
- Organiza informações em clusters hierárquicos para capturar diferentes níveis de abstração
- **Eficácia**: Consistentemente superou o RAG básico, com taxa de vitória de 70-80% em métricas de abrangência e diversidade
- **Melhor uso**: Situações envolvendo grandes corpora de informação complexa onde relacionamentos entre conceitos são importantes

**ELICIT** (ICLR, 2025):
- Cria uma "biblioteca de capacidades" de vetores de tarefa que codificam diferentes capacidades aprendidas em contexto
- Usa um módulo de recuperação para selecionar dinamicamente capacidades relevantes para consultas arbitrárias
- **Eficácia**: Mostrou melhoria significativa em desempenho matemático (por exemplo, de 21,3% para Mistral)
- **Melhor uso**: Aprimorar capacidades específicas (como raciocínio matemático) enquanto mantém desempenho geral

## Técnicas de refinamento iterativo de tarefas

As técnicas mais eficazes para refinamento iterativo de tarefas incluem:

### Self-Refine

**Princípios fundamentais:**
Abordagem para melhorar saídas iniciais de LLMs através de um processo iterativo de três etapas:
1. A IA gera uma saída inicial com base em um prompt
2. A mesma IA fornece feedback multi-aspecto sobre sua própria saída
3. A IA então refina sua saída com base neste feedback
4. As etapas 2-3 se repetem até que se atinja qualidade suficiente

**Evidências de eficácia:**
- Avaliada em 7 tarefas diversas (otimização de código, raciocínio matemático, geração de diálogo, etc.)
- Alcançou **melhoria absoluta de ~20%** no desempenho de tarefas em comparação com geração em etapa única
- Demonstrou melhorar saídas mesmo de modelos state-of-the-art como GPT-4
- Avaliadores humanos consistentemente preferiram saídas Self-Refine sobre geração direta

### Ferramenta "Think" da Anthropic

**Princípios fundamentais:**
Cria um espaço dedicado para pensamento estruturado durante tarefas complexas nos modelos Claude:
1. A IA processa a solicitação inicial
2. Em pontos críticos de decisão, pode invocar a ferramenta "think"
3. Usando este espaço dedicado, a IA raciocina através de problemas complexos passo a passo
4. O raciocínio é registrado mas não mostrado ao usuário a menos que solicitado

**Evidências de eficácia:**
- No benchmark de domínio aéreo da Anthropic, o uso da ferramenta "think" com um prompt otimizado alcançou **melhoria relativa de 54%** sobre a linha de base (0,570 vs. 0,370)
- No domínio de varejo, a ferramenta "think" sozinha alcançou 0,812, comparado a 0,783 para a linha de base
- Contribuiu para a pontuação state-of-the-art do Claude 3.7 Sonnet de 0,623 no SWE-Bench

### Pesquisa Profunda (Deep Research)

**Princípios fundamentais:**
Sistema projetado para pesquisa autônoma multi-etapa em tópicos complexos:
1. Decompõe questões complexas em sub-questões menores e gerenciáveis
2. Busca e analisa autonomamente informações de diversas fontes online
3. Sintetiza descobertas em um relatório abrangente e bem citado
4. Fornece citações claras vinculadas diretamente aos materiais originais

**Evidências de eficácia:**
- No GAIA (benchmark de Agente de IA Geral), estabeleceu um novo recorde state-of-the-art
- Particularmente forte em tarefas de Nível 3 que requerem pesquisa complexa em múltiplas etapas
- Alta pontuação pass@1 mostrando precisão mesmo na primeira tentativa de responder perguntas
- Superou modelos anteriores no benchmark "Humanity's Last Exam", pontuando **26,6% de precisão** (mais que o dobro dos modelos anteriores da OpenAI)

## Recomendações baseadas no contexto de uso

### Por tipo de modelo

**Para GPT-4/GPT-4o:**
- Beneficia-se mais de estrutura explícita em tarefas técnicas
- Responde bem à liberdade criativa em tarefas generativas
- Desempenha melhor com 2-3 exemplos em cenários few-shot
- **Melhor técnica**: Chain-of-Thought com Auto-consistência para tarefas técnicas; Verificador Cognitivo para tarefas analíticas

**Para modelos Claude 3:**
- Excelente com prompts estruturados com tags XML
- Beneficia-se de instruções explícitas de "pensamento" para raciocínio complexo
- Mostra desempenho mais forte com janelas de contexto mais longas
- **Melhor técnica**: Requisição Estruturada para tarefas complexas; ferramenta "Think" para raciocínio multi-etapa

**Para modelos Gemini:**
- Melhor desempenho com integração de contexto multimodal
- Beneficia-se de orientação explícita de raciocínio
- Mostra desempenho mais forte com integração de pesquisa web para tarefas factuais
- **Melhor técnica**: Decomposição de Tarefas para problemas complexos; Tree of Thoughts para exploração criativa

### Por cenário de aplicação

**Para assistentes virtuais corporativos:**
- Priorize **Requisição Estruturada** para capturar todas as informações necessárias
- Implemente **Auto-Reflexão** para reduzir alucinações em contextos corporativos sensíveis
- Combine com **Decomposição de Tarefas** para solicitações complexas de múltiplas partes

**Para suporte técnico e solução de problemas:**
- Utilize **Chain-of-Thought com Auto-consistência** para problemas técnicos
- Implemente **Verificador Cognitivo** para determinar informações necessárias sobre o problema
- Combine com técnicas de **Auto-Reflexão** para verificação de precisão

**Para assistentes de pesquisa e educação:**
- Priorize **Pesquisa Profunda** para consultas de pesquisa abrangentes
- Utilize **Decomposição de Tarefas** para tópicos educacionais complexos
- Implemente **GraphRAG** para sintetizar informações através de múltiplas fontes

**Para assistentes de fluxo de trabalho criativo:**
- Utilize **Tree of Thoughts** para ideação e exploração criativa
- Implemente **Prompting baseado em papéis** para controle de estilo e tom
- Combine com técnicas de **Auto-Refinamento** para melhoria iterativa

## Considerações práticas para implementação

1. **Otimização específica para modelo:** Diferentes modelos respondem melhor a diferentes padrões - Claude 3 mostra melhorias mais fortes com formatos estruturados, enquanto GPT-4 se destaca com padrões focados em raciocínio.

2. **Combinando padrões:** Pesquisas mostram que combinar padrões complementares (por exemplo, Chain-of-Thought com Verificador Cognitivo) pode produzir benefícios multiplicativos, melhorando a precisão de resposta em até 45-50% em cenários complexos.

3. **Eficiência de tokens:** Considere a sobrecarga de tokens de diferentes padrões, especialmente para sistemas em produção. Técnicas como CoT podem aumentar significativamente o uso de tokens.

4. **Adaptação de domínio:** Padrões devem ser adaptados a requisitos de conhecimento específicos do domínio - domínios médicos, jurídicos e técnicos se beneficiam de formulação de contexto especializada.

5. **Experiência do usuário:** Equilibre a abrangência da elicitação de informações com a experiência do usuário - muitas perguntas podem levar ao abandono do usuário. Em interfaces conversacionais, considere limitar solicitações iniciais a 3-4 itens críticos.

## Conclusão

Nossa investigação identifica várias técnicas de engenharia de prompts com evidências empíricas sólidas para melhorar a capacidade dos sistemas de IA conversacional de solicitar informações críticas faltantes. As abordagens mais eficazes combinam múltiplos padrões complementares, adaptam-se ao tipo específico de tarefa, e consideram as forças individuais de cada modelo de IA.

Para implementação prática, recomendamos começar com o Padrão Verificador Cognitivo como base, integrar elementos de Requisição Estruturada para clareza, e adicionar Auto-Reflexão para verificação de precisão. Para tarefas técnicas complexas, incorporar Chain-of-Thought com Auto-consistência, enquanto para tarefas criativas ou exploratórias, considerar abordagens Tree of Thoughts.

A pesquisa mostra claramente que não existe uma abordagem única ideal para todos os cenários, mas sim que a eficácia da elicitação de informações depende criticamente da correspondência entre a técnica de prompting, o tipo de tarefa, o modelo específico de IA, e as necessidades do caso de uso.