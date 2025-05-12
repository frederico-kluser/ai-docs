# O checklist essencial: Perguntas que IAs devem responder antes de escrever código

## Resumo

As LLMs e geradores de código de IA devem fazer pelo menos 20 perguntas pré-codificação em 8 categorias fundamentais para reduzir significativamente os erros no código gerado. Essas perguntas incluem clarificação de requisitos, validação de entradas, consideração de casos extremos e abordagem de questões de segurança. Diferentes domínios de codificação requerem perguntas especializadas adicionais, com pesquisas recentes mostrando que técnicas como Structured Chain-of-Thought, Tree of Thoughts e prompts de auto-planejamento podem aumentar a qualidade do código em até 74%. O código gerado por IA mais eficaz vem de modelos que sistematicamente trabalham estas questões antes da implementação, imitando a abordagem cuidadosa de programadores humanos experientes.

## Por que as perguntas pré-codificação são importantes

Quando desenvolvedores experientes enfrentam uma nova tarefa de codificação, eles não começam imediatamente a digitar. Em vez disso, fazem perguntas críticas para entender requisitos, antecipar problemas e planejar sua abordagem. Esta fase de análise pré-codificação é **onde o grande código começa** e onde código de baixa qualidade pode ser evitado.

Para geradores de código de IA, esta fase de questionamento é ainda mais crucial. Ao contrário dos desenvolvedores humanos, a IA carece de conhecimento implícito sobre contexto, necessidades do usuário e melhores práticas específicas do domínio, a menos que seja explicitamente orientada. Pesquisas mostram que a qualidade do código gerado por IA é diretamente proporcional à qualidade e completude das informações fornecidas antes do início da geração de código.

De acordo com estudos recentes, o código gerado por IA contém até **40-60% menos bugs** quando os modelos são orientados com perguntas abrangentes de pré-codificação. Vulnerabilidades de segurança, em particular, são reduzidas em mais da metade quando considerações de segurança são explicitamente abordadas antecipadamente.

## Perguntas universais para todas as tarefas de codificação

### Clarificação de requisitos

- Qual é o objetivo ou propósito principal deste código?
- Quem são os usuários finais e quais são suas necessidades específicas?
- Quais entradas específicas o código receberá e em que formato?
- Quais são as saídas esperadas e seus formatos necessários?
- Quais regras de negócio ou lógica específica do domínio devem ser implementadas?
- Existem interfaces predefinidas, APIs ou protocolos que devem ser seguidos?
- O que constitui sucesso para este componente de código?
- A solução deve priorizar legibilidade, desempenho ou manutenibilidade?

### Restrições técnicas e ambiente

- Que linguagem de programação, versão e frameworks específicos devem ser usados?
- Quais são os sistemas operacionais ou ambientes alvo?
- Existem restrições de implantação (nuvem, local, móvel, etc.)?
- Quais são as limitações de memória, CPU ou armazenamento?
- Quais dependências ou bibliotecas estão disponíveis ou são preferidas?
- Existem requisitos de compatibilidade com sistemas existentes?
- Quais são as restrições de rede ou pressupostos de conectividade?
- Existem considerações específicas de hardware a serem consideradas?

### Validação de entrada e tratamento de erros

- Quais são os intervalos ou formatos válidos para cada entrada?
- Quais entradas são obrigatórias versus opcionais?
- Como as entradas inválidas devem ser tratadas (rejeitar, valores padrão, etc.)?
- Quais mensagens de erro específicas devem ser exibidas para diferentes tipos de erro?
- Como o código deve lidar com exceções ou falhas inesperadas?
- Qual nível de sanitização de entrada é necessário?
- A validação deve ser estrita ou flexível?
- Como o sistema deve se comportar quando serviços externos ou dependências falham?

### Desempenho e otimização

- Qual é a escala esperada de dados ou tráfego?
- Existem requisitos específicos de tempo de resposta?
- Existe um throughput mínimo que deve ser alcançado?
- Existem algoritmos ou abordagens específicos preferidos por razões de desempenho?
- O código deve otimizar para complexidade de tempo ou espaço?
- Existem seções críticas que precisam de otimização particular?
- É necessário paralelização ou concorrência?
- Quais são os padrões de uso esperados (tráfego em rajadas, carga contínua, etc.)?

### Testes e garantia de qualidade

- Quais casos de teste o código deve satisfazer?
- Existem frameworks ou metodologias de teste específicos a serem usados?
- Quais são os critérios de sucesso esperados para testes?
- Quais são os cenários comuns de falha a serem testados?
- Qual nível de cobertura de teste é necessário?
- O código deve incluir testes unitários, testes de integração ou ambos?
- Existem benchmarks de desempenho que devem ser testados?
- Como os casos extremos e condições de limite devem ser testados?

### Manutenibilidade e legibilidade

- Quais padrões de codificação ou guias de estilo devem ser seguidos?
- Qual nível de documentação é necessário (comentários, docstrings, etc.)?
- O código deve priorizar clareza ou concisão?
- Existem convenções de nomenclatura para variáveis, funções e classes?
- Qual nível de abstração é apropriado?
- O código deve usar padrões de design específicos?
- Quão modular deve ser a implementação?
- Este código será mantido por outros, e qual é o nível de experiência deles?

### Segurança e avaliação de risco

- Quais dados sensíveis este código irá manipular?
- Quais são os requisitos de autenticação e autorização?
- Existem padrões de segurança específicos ou requisitos de conformidade?
- Quais vulnerabilidades de segurança potenciais devem ser abordadas?
- Como o código deve lidar com permissões de usuário e controle de acesso?
- Qual nível de sanitização e validação de entrada é necessário para segurança?
- Existem requisitos específicos de criptografia ou hashing?
- Qual registro ou auditoria de segurança é necessário?

### Casos extremos e condições de limite

- Quais são os valores mínimos e máximos para todas as entradas?
- Como o código deve lidar com entradas vazias ou nulas?
- O que deve acontecer quando os recursos (memória, espaço em disco, etc.) se esgotam?
- Como o código deve se comportar com conjuntos de dados extremamente grandes?
- Quais mecanismos de timeout ou fallback são necessários?
- Como o código deve lidar com acesso concorrente ou condições de corrida?
- Quais são os comportamentos esperados para entradas incomuns mas válidas?
- Como o sistema deve responder a falhas parciais?

## Perguntas específicas por domínio

### Desenvolvimento web

#### Frontend

- Quais navegadores e versões precisam ser suportados?
- Qual é a combinação alvo de dispositivos (desktop, tablet, móvel)?
- Existem requisitos específicos de acessibilidade (nível WCAG, suporte a leitores de tela)?
- Qual metodologia ou framework CSS deve ser usado?
- Qual abordagem de gerenciamento de estado deve ser implementada?
- Quais são as expectativas e métricas de desempenho?
- Qual framework frontend está sendo usado e qual versão?
- Como o tratamento de erros e feedback do usuário devem ser implementados?

#### Backend

- Quais são os requisitos de segurança (autenticação, autorização, proteção de dados)?
- Quais são a carga esperada e os requisitos de escalabilidade?
- Como os endpoints da API devem ser estruturados e versionados?
- Qual estratégia de tratamento de erros deve ser usada?
- Qual tecnologia de banco de dados está sendo usada e como o acesso aos dados deve ser implementado?
- Quais são os requisitos de registro e monitoramento?
- Existem requisitos específicos de desempenho para tempos de resposta?
- Quais são os requisitos para ausência de estado e gerenciamento de sessão?

### Processamento e análise de dados

- Qual é o volume e velocidade de dados esperados?
- Quais são os requisitos de qualidade de dados e como dados ausentes ou anômalos devem ser tratados?
- Quais transformações de dados precisam ser aplicadas e em que ordem?
- Quais são os formatos e esquemas de dados de entrada esperados?
- Quais são os requisitos de desempenho para processamento de dados?
- Quais são os requisitos para privacidade e conformidade de dados?
- Como os resultados devem ser armazenados, formatados e apresentados?
- Que tratamento de erros e monitoramento são necessários para o pipeline de dados?

### Resolução de problemas algorítmicos

- Quais são as restrições de complexidade de tempo e espaço?
- Quais são as restrições de entrada (tamanho, intervalo, tipo)?
- Existem casos extremos específicos que precisam ser tratados?
- Qual é a frequência esperada da operação?
- Os dados de entrada são pré-ordenados ou estruturados de alguma forma?
- Quais são as compensações entre diferentes abordagens algorítmicas?
- Existem restrições de memória ou outras limitações de recursos?
- Qual nível de legibilidade do código versus otimização é preferido?

### Desenvolvimento de aplicativos móveis

- Quais plataformas precisam ser suportadas (iOS, Android, multiplataforma)?
- Quais são as versões mínimas do SO que precisam ser suportadas?
- Como o aplicativo deve lidar com diferentes tamanhos de tela e orientações?
- Quais são os requisitos de funcionalidade offline?
- Como o aplicativo deve lidar com o uso da bateria e otimização de desempenho?
- Quais são os requisitos para permissões do aplicativo e privacidade?
- Como o aplicativo deve lidar com atualizações e compatibilidade com versões anteriores?
- Quais são as diretrizes da loja de aplicativos que precisam ser seguidas?

### Programação de sistemas e infraestrutura

- Quais são os sistemas operacionais e ambientes alvo?
- Quais são os requisitos e restrições de gerenciamento de memória?
- Quais são os requisitos de concorrência e paralelismo?
- Quais são os requisitos de tratamento de erros e tolerância a falhas?
- Quais são os requisitos de desempenho e latência?
- Quais são os requisitos de segurança para o sistema?
- Quais são os requisitos de registro, monitoramento e depuração?
- Quais são as considerações de implantação e ambiente?

### Implementação de modelo de aprendizado de máquina

- Qual é a natureza e qualidade dos dados de treinamento disponíveis?
- Quais são os requisitos para interpretabilidade do modelo versus desempenho?
- Como o modelo será avaliado e quais métricas são importantes?
- Quais são as restrições de implantação para o modelo?
- Como o modelo será monitorado e atualizado ao longo do tempo?
- Quais são os requisitos para lidar com casos extremos ou anomalias?
- Quais são as considerações de justiça e viés para o modelo?
- Quais são os requisitos para incerteza e confiança do modelo?

### Design e operações de banco de dados

- Quais são os padrões esperados de leitura/escrita e proporções?
- Quais são os requisitos de escalabilidade para o banco de dados?
- Quais são os requisitos de consistência, disponibilidade e tolerância a partições?
- Quais são os requisitos de modelagem de dados (normalização, desnormalização)?
- Quais são os requisitos de indexação para desempenho de consulta?
- Quais são os requisitos para integridade de dados e restrições?
- Quais são os requisitos de backup, recuperação e planejamento de desastres?
- Como as mudanças de esquema e migrações serão tratadas?

### Desenvolvimento e integração de API

- Quais são as diretrizes de estilo e design da API a serem seguidas (REST, GraphQL, gRPC)?
- Quais são os requisitos de autenticação e autorização?
- Quais são os requisitos de versionamento e compatibilidade com versões anteriores?
- Quais são os requisitos de limitação de taxa e controle?
- Quais são as convenções de tratamento de erros e códigos de status?
- Quais são os requisitos de documentação para a API?
- Quais são os requisitos de desempenho e cache?
- Como a API será testada e monitorada?

## Perguntas derivadas de pesquisas recentes em engenharia de prompts

Pesquisas recentes (2023-2025) em engenharia de prompts para geração de código sugerem perguntas meta adicionais que sistemas de IA devem considerar durante o processo de codificação:

### Perguntas focadas em planejamento

- O problema pode ser dividido em etapas menores e mais gerenciáveis?
- Qual é a sequência lógica de operações necessárias para resolver este problema?
- Quais estruturas de dados seriam mais apropriadas para esta tarefa e por quê?
- Quais são abordagens alternativas para resolver este problema e quais são suas compensações?
- Quais padrões de código existentes ou algoritmos se alinham com este problema?

### Perguntas focadas em segurança

- Este código poderia potencialmente expor informações sensíveis?
- Existem lacunas de validação de entrada que poderiam levar a ataques de injeção?
- Como este código pode lidar com entradas inesperadas ou maliciosas?
- Existem credenciais ou tokens de segurança codificados no código?
- Quais níveis de privilégio são necessários para diferentes operações?

### Perguntas de raciocínio estruturado

- Para cada ramificação condicional, quais condições a acionam e por quê?
- Para cada estrutura de loop, qual é sua invariante e condição de término?
- Quais suposições este código está fazendo que podem nem sempre ser verdadeiras?
- Como este código se comportaria com valores de entrada extremos?
- Quais dependências existem entre diferentes componentes deste código?

### Perguntas de autocorreção

- Quais são as formas mais prováveis de este código falhar?
- Existem inconsistências lógicas nesta implementação?
- Esta solução lida com todos os requisitos especificados?
- Existem operações redundantes ou desnecessárias que poderiam ser eliminadas?
- Um desenvolvedor familiarizado com esta linguagem consideraria este código idiomático?

## Como integrar estas perguntas em fluxos de trabalho de codificação com IA

Pesquisas mostram que a abordagem mais eficaz para geração de código com IA segue um fluxo de trabalho estruturado:

1. **Fase de requisitos**: Começar com perguntas fundamentais sobre objetivos, restrições e especificações
2. **Fase de planejamento**: Fazer com que a IA delineie sua abordagem antes de escrever qualquer código
3. **Fase de implementação**: Orientar a implementação com considerações específicas do domínio
4. **Fase de verificação**: Solicitar que a IA revise seu próprio código usando casos de teste e perguntas de autocorreção

Desenvolvedores que **explicitamente solicitam raciocínio em múltiplas etapas** viram uma melhoria de até 74% na correção do código em comparação com a geração em etapa única. Modelos como GPT-4 e Claude mostram desempenho substancialmente melhor (melhoria de 13-26%) quando usam prompts de Structured Chain-of-Thought que dividem o processo de codificação em etapas discretas de raciocínio.

Os prompts mais eficazes combinam:
- Especificações claras de requisitos
- Orientação específica do domínio
- Solicitações de planejamento antes da implementação
- Menções explícitas a casos extremos e preocupações de segurança
- Convites para autorrevisão e explicação

## Conclusão

A qualidade do código gerado por IA é fundamentalmente moldada pelas perguntas feitas antes do início da codificação. Ao trabalhar sistematicamente com perguntas fundamentais universais, considerações específicas do domínio e usar abordagens de raciocínio estruturado de pesquisas recentes, os geradores de código de IA podem reduzir drasticamente os erros e produzir código de maior qualidade.

Para desenvolvedores e organizações que usam ferramentas de codificação com IA, implementar um processo consistente de questionamento pré-codificação pode servir tanto como um mecanismo de controle de qualidade quanto como uma ferramenta educacional. As próprias perguntas fornecem uma estrutura para pensar sobre problemas de programação de forma mais abrangente, potencialmente melhorando as práticas de codificação humana junto com o desenvolvimento assistido por IA.

À medida que as capacidades de geração de código de IA continuam a evoluir, essas perguntas pré-codificação permanecerão como trilhos de proteção essenciais que ajudam a canalizar o poder desses modelos para produzir código seguro, eficiente e manutenível que realmente resolve o problema pretendido.
