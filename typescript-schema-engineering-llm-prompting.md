# A revolução dos prompts para código TypeScript: aumentando a precisão das LLMs

A engenharia de prompts para código TypeScript evoluiu significativamente, transformando simples instruções textuais em sistemas sofisticados que potencializam drasticamente a precisão das LLMs. Esta pesquisa compila as técnicas mais eficazes, oferecendo métodos concretos para melhorar suas interações com modelos de linguagem em projetos de código novos e existentes.

## Schema Engineering: a evolução do prompt engineering para TypeScript

O **Schema Engineering** está substituindo a engenharia de prompts tradicional ao usar definições de tipos TypeScript para controlar e restringir as respostas das LLMs. Esta abordagem, exemplificada pelo projeto Microsoft TypeChat, **elimina a necessidade de prompts complexos** e fornece **validação automática** das respostas.

```typescript
// Em vez de longos prompts textuais, defina tipos:
interface PedidoCafe {
  tipo: "latte" | "espresso" | "cappuccino";
  tamanho: "pequeno" | "médio" | "grande";
  temperatura?: "gelado" | "quente" | "extra quente";
  extras?: string[];
}
```

Esta estrutura tipada guia a LLM a fornecer respostas válidas e bem formadas, reduzindo drasticamente as alucinações. Quando a resposta falha na validação, o sistema envia diagnósticos de volta para o modelo para autocorreção.

Outras técnicas TypeScript que melhoram significativamente a compreensão de código incluem:

1. **Definição explícita de interfaces nos prompts** - incluir definições completas de tipos aumenta a capacidade do modelo de gerar código estruturado corretamente
2. **Bibliotecas de validação** como Zod e ts-prompt para criação de prompts tipados
3. **"Saídas de emergência"** em esquemas de tipo para reduzir alucinações:

```typescript
type Acao = 
  | { tipo: "pedido"; produto: string; quantidade: number }
  | { tipo: "pesquisa"; termo: string }
  | { tipo: "desconhecido"; entrada: string }; // Reduz alucinações
```

## Decomposição eficiente de tarefas complexas

A decomposição de tarefas complexas em subtarefas menores aumenta a precisão das LLMs em **25-40%** para problemas complexos. Três abordagens se destacam:

### Decomposed Prompting (DecomP)
Divide tarefas complexas em subtarefas modulares, cada uma delegada a manipuladores específicos:

```typescript
// Exemplo conceitual de DecomP
const decomposerPrompt = "QC: Concatenar a primeira letra de cada palavra em 'Projeto TypeScript'";
const subtarefas = [
  "Q1: [split] Quais são as palavras em 'Projeto TypeScript'?",
  "Q2: (foreach) [str_pos] Qual é a primeira letra de cada palavra?",
  "Q3: [merge] Concatenar as letras com espaços"
];
```

### Chain-of-Thought e suas variantes
A técnica "Let's think step-by-step" melhora significativamente o desempenho em tarefas de raciocínio multi-etapas:

```
Para implementar um sistema de cache TypeScript:
1. Primeiro, vamos definir a interface Cache com métodos get, set e delete
2. Em seguida, implementaremos uma classe que usa Map para armazenamento
3. Depois, adicionaremos tratamento para tempos de expiração
4. Por fim, implementaremos métodos auxiliares para estatísticas de uso
```

### Frameworks de Decomposição
O LangChain Expression Language (LCEL) facilita a composição de cadeias de componentes para processar tarefas modularmente:

```typescript
import { RunnableSequence, RunnableParallel } from "@langchain/core/runnables";

// Decompor a tarefa em componentes paralelos
const jokeChain = ChatPromptTemplate.fromTemplate("Crie uma piada sobre {topic}") 
  .pipe(model)
  .pipe(new StringOutputParser());

const analysisChain = ChatPromptTemplate.fromTemplate("Analise o código {code}") 
  .pipe(model)
  .pipe(new StringOutputParser());

// Execução paralela de subtarefas
const parallelChain = RunnableParallel({
  joke: jokeChain,
  analysis: analysisChain
});
```

## Paralelização com múltiplas LLMs sem conflitos

A paralelização pode **reduzir o tempo de processamento em até 70%** para fluxos decomponíveis. Três estratégias se destacam:

### Fan-out/Fan-in com LangGraph
Este padrão permite distribuir trabalho para múltiplos nós e depois convergir os resultados:

```typescript
// Fan-out: distribuir de Node A para Node B e Node C
graph.addEdge("nodeA", ["nodeB", "nodeC"]);

// Fan-in: convergir de Node B e Node C para Node D
graph.addEdge(["nodeB", "nodeC"], "nodeD");
```

### Compartilhamento de Estado Controlado
Uso de objetos de estado compartilhado com mecanismos específicos para combinar resultados:

```typescript
// Estado com redutor para lidar com atualizações paralelas
class Estado {
  // Quando múltiplos nós atualizarem lista simultaneamente, append em vez de substituir
  lista: Annotated<string[], operator.add>;
  
  // Para contadores, somar os valores em vez de substituir
  contador: Annotated<number, operator.add>;
}
```

### Equipes de Agentes Especializados
Frameworks como CrewAI permitem criar equipes de agentes com papéis específicos:

```typescript
const researcherAgent = new Agent({
  role: "Pesquisador TypeScript",
  goal: "Analisar padrões de código TypeScript",
  tools: [searchTool, analysisTool]
});

const developerAgent = new Agent({
  role: "Desenvolvedor TypeScript",
  goal: "Implementar soluções otimizadas",
  tools: [codeTool, testTool]
});

const crew = new Crew({
  agents: [researcherAgent, developerAgent],
  tasks: [analyzeTask, implementTask]
});
```

## Templates de prompts que transformam a comunicação

Os templates mais eficazes compartilham uma estrutura fundamental que inclui:

1. **Contexto e propósito** - explicação clara do problema
2. **Requisitos funcionais** - descrição precisa do que o código deve fazer
3. **Restrições e especificações técnicas** - limitações e requisitos não-funcionais
4. **Exemplos relacionados** - códigos semelhantes como referência
5. **Formato de saída esperado** - estrutura da resposta desejada

### Template para geração de função TypeScript

```markdown
### Function Generation Template:

**Propósito da Função**: [Descrição detalhada do que a função deve fazer]

**Nome da Função**: [Nome seguindo convenções apropriadas]

**Parâmetros de Entrada**:
- [nome]: [tipo] - [descrição/propósito]
- [nome]: [tipo] - [descrição/propósito]

**Tipo de Retorno**: [Tipo de dados TypeScript que a função deve retornar]

**Comportamento Esperado**:
- [Descrição passo a passo do comportamento esperado]
- [Casos de borda que devem ser tratados]

**Contexto Adicional**: [Informações relevantes sobre o ambiente, bibliotecas, etc.]
```

### Exemplo concreto com API externa

```markdown
**Propósito da Função**: Buscar o clima atual para uma cidade usando a API WeatherStack.

**Nome da Função**: getCurrentWeather

**Parâmetros de Entrada**:
- city: string - O nome da cidade para obter informações de clima
- apiKey: string - A chave de API para autenticação com a WeatherStack

**Tipo de Retorno**: Promise<WeatherData> - Um objeto com informações de clima

**Comportamento Esperado**:
- Validar os parâmetros de entrada
- Construir a URL da API com os parâmetros
- Fazer uma requisição HTTP para a API
- Processar a resposta e transformar em um formato utilizável
- Lidar com erros de rede e da API
- Retornar os dados de clima formatados

**Contexto Adicional**:
- A função deve ser assíncrona e usar Fetch API ou Axios
- Deve incluir tratamento adequado de erros
- WeatherData é um tipo que já existe na aplicação
```

## Estruturação para Claude Code e agentes personalizados

### Técnicas específicas para Claude Code

Claude Code atinge **maior eficácia** quando os prompts seguem estas práticas:

1. **Arquivos CLAUDE.md** - armazenamento de comandos frequentes e preferências
2. **Comandos personalizados** - templates em arquivos Markdown na pasta `.claude/commands`
3. **Marcadores XML** - uso de tags como `<instructions>`, `<example>`, `<context>`
4. **Contextualização do projeto** - estrutura de diretórios, dependências e arquivos relevantes

### Criação de agentes IA personalizados

Para criar agentes de IA personalizados eficazes:

```markdown
Você é um especialista em engenharia de código TypeScript com foco em [domínio específico]. 
Seu objetivo é [propósito principal].

Siga estas diretrizes ao gerar código:
- Adote o estilo [descrever convenções de codificação]
- Utilize apenas bibliotecas presentes no package.json
- Priorize [performance/legibilidade/manutenibilidade]
- Documente seguindo o padrão [descrever padrão]

Seu fluxo de trabalho deve ser:
1. Analise o contexto do código atual e entenda sua função
2. Identifique áreas para melhoria ou implementação
3. Explique sua abordagem antes de implementar
4. Implemente a solução
5. Valide a solução contra os requisitos
```

## Exemplos práticos: bases existentes vs. novos projetos

A abordagem difere significativamente entre bases de código existentes e novos projetos:

### Para bases de código existentes
Exige análise do código atual, adaptação a padrões existentes e foco na integração:

```markdown
Analise esta base de código TypeScript e sugira como implementar [nova funcionalidade].

<estrutura_diretórios>
[Estrutura de pastas relevantes]
</estrutura_diretórios>

<código_relevante>
// Trecho de código existente relacionado
</código_relevante>

A nova funcionalidade deve:
1. Seguir o mesmo padrão arquitetural
2. Utilizar as mesmas bibliotecas quando possível
3. Manter consistência com convenções de nomenclatura
4. Ser testável usando o framework de teste atual
```

### Para novos projetos
Permite maior liberdade criativa e foco na estruturação inicial:

```markdown
Crie a estrutura inicial para um novo projeto TypeScript com as seguintes características:

<requisitos>
- Frontend em React com Next.js
- Estado gerenciado com Redux
- Autenticação de usuários
- Comunicação com API REST
</requisitos>

<preferências>
- Uso de TypeScript estrito
- Testes com Jest
- Estilização com Tailwind CSS
</preferências>

Por favor, forneça:
1. Estrutura de diretórios recomendada
2. Configuração de TypeScript (tsconfig.json)
3. Dependências necessárias (package.json)
4. Arquivos iniciais principais
```

## Direcionamentos práticos para maximizar resultados

Para maximizar a precisão das LLMs com código TypeScript:

1. **Adote Schema Engineering** sobre prompts textuais tradicionais, utilizando bibliotecas como TypeChat
2. **Defina saídas de emergência** em seus esquemas de tipos para reduzir alucinações
3. **Decomponha problemas complexos** usando técnicas como DecomP ou Chain-of-Thought
4. **Paralelize com controle** usando mecanismos como RunnableParallel e padrões fan-out/fan-in
5. **Utilize templates estruturados** que incluam propósito, parâmetros, tipos e comportamento esperado
6. **Adapte a abordagem** com base no contexto - integração em código existente vs. criação de novos projetos
7. **Aproveite ferramentas especializadas** como LangChain, LangGraph, CrewAI e bibliotecas de validação como Zod

A combinação destas técnicas pode transformar significativamente suas interações com LLMs, elevando a precisão e reduzindo o tempo de desenvolvimento tanto para projetos existentes quanto para novas implementações em TypeScript.