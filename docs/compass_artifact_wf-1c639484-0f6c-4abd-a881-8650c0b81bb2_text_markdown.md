# Tutorial Completo: GPT-5.1-Codex-Max com LangChain.js e Zod
<!-- Arquivo renomeado para: tutorial-gpt5-codex-langchain-zod.md -->

O **GPT-5.1-Codex-Max** é o modelo de codificação agêntica de fronteira da OpenAI, lançado em 18 de novembro de 2025. Este tutorial demonstra como integrá-lo com LangChain.js usando Node.js 24+ com suporte nativo a TypeScript e schemas Zod para saídas estruturadas.

## Verificação do modelo e arquitetura

O GPT-5.1-Codex-Max é um modelo real da OpenAI, confirmado pela documentação oficial e pelo System Card publicado em novembro de 2025. Ele foi projetado especificamente para tarefas de codificação de longa duração, podendo operar de forma coerente por **milhões de tokens** através de uma técnica chamada "compaction". O modelo está disponível exclusivamente através da **Responses API** — não funciona com a Chat Completions API tradicional.

As principais características incluem suporte a quatro níveis de esforço de raciocínio (`none`, `medium`, `high`, `xhigh`), consumo de **30% menos tokens de pensamento** que o GPT-5.1-Codex em esforço médio, e capacidade de executar sessões de até 24 horas. O modelo suporta function calling, structured outputs, compaction e a ferramenta web_search nativamente.

## Configuração do ambiente Node.js 24+

O Node.js 24, lançado em 6 de maio de 2025 com codinome "Krypton", traz suporte nativo a TypeScript através de "type stripping" — uma técnica que substitui anotações de tipo por espaços em branco, preservando números de linha para debugging sem necessidade de source maps.

### Instalação e verificação

```bash
# Verificar versão do Node.js (deve ser 24.x ou superior)
node --version

# Criar diretório do projeto
mkdir gpt5-langchain-tutorial && cd gpt5-langchain-tutorial

# Inicializar projeto
npm init -y
```

### Configuração do package.json

```json
{
  "name": "gpt5-langchain-tutorial",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node src/index.ts",
    "typecheck": "tsc --noEmit",
    "dev": "node --watch src/index.ts"
  },
  "dependencies": {
    "@langchain/core": "^0.3.40",
    "@langchain/openai": "^1.2.0",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.8.0"
  }
}
```

**Importante:** A versão do Zod deve ser **3.x** — o Zod v4 ainda não é compatível com LangChain.js devido a problemas conhecidos na conversão para JSON Schema (issues #8357 e #8413 no GitHub).

### Configuração do tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": true,
    "rewriteRelativeImportExtensions": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
```

A opção **`erasableSyntaxOnly`** (TypeScript 5.8+) é crucial — ela gera erros de compilação para sintaxes TypeScript que não podem ser simplesmente "apagadas", como `enum`, `namespace` com código runtime e parameter properties. Isso garante compatibilidade com o type stripping do Node.js.

### Variáveis de ambiente (.env.example)

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
LANGSMITH_API_KEY=ls__xxxxxxxxxxxxx
LANGSMITH_TRACING=true
LANGCHAIN_PROJECT=gpt5-codex-tutorial
```

## Schemas Zod para saídas estruturadas

O Zod é a biblioteca padrão para definição de schemas em LangChain.js. O método `.describe()` adiciona metadados que são convertidos para JSON Schema e fornecem contexto para o LLM gerar respostas no formato correto.

### Padrões fundamentais de schema

```typescript
// src/schemas/code-review.ts
import { z } from "zod";

export const CodeIssueSchema = z.object({
  line: z.number().describe("Número da linha onde o problema foi encontrado"),
  severity: z.enum(["critical", "warning", "info"])
    .describe("Severidade: critical para bugs, warning para melhorias, info para sugestões"),
  category: z.enum(["security", "performance", "maintainability", "bug"])
    .describe("Categoria do problema identificado"),
  description: z.string().describe("Descrição clara do problema"),
  suggestion: z.string().describe("Sugestão de correção com código quando aplicável")
});

export const CodeReviewSchema = z.object({
  summary: z.string().describe("Resumo executivo da revisão em 2-3 frases"),
  overallScore: z.number().min(0).max(10)
    .describe("Nota geral do código de 0 a 10"),
  issues: z.array(CodeIssueSchema)
    .describe("Lista de problemas encontrados ordenados por severidade"),
  positiveAspects: z.array(z.string())
    .describe("Aspectos positivos do código que devem ser mantidos"),
  refactoringPriority: z.nullable(z.string())
    .describe("Prioridade de refatoração, null se não necessário")
});

// Inferência de tipos TypeScript a partir do schema
export type CodeReview = z.infer<typeof CodeReviewSchema>;
export type CodeIssue = z.infer<typeof CodeIssueSchema>;
```

Use **`z.nullable()`** em vez de `z.optional()` para campos opcionais quando trabalhar com modelos de raciocínio — esta é uma limitação conhecida da integração.

## Configuração do LangChain.js com Responses API

O ChatOpenAI do LangChain.js suporta a Responses API através da opção `useResponsesApi`. Esta configuração é **obrigatória** para o GPT-5.1-Codex-Max.

### Configuração básica do modelo

```typescript
// src/lib/model.ts
import { ChatOpenAI } from "@langchain/openai";

export function createCodexModel(reasoningEffort: "none" | "medium" | "high" | "xhigh" = "medium") {
  return new ChatOpenAI({
    model: "gpt-5.1-codex-max",
    temperature: 0,
    maxRetries: 3,
    timeout: 120000, // 2 minutos - modelos de raciocínio podem demorar
    
    // Ativa a Responses API (obrigatório para GPT-5.1-Codex-Max)
    useResponsesApi: true,
    
    // Configuração customizada para headers ou base URL
    configuration: {
      defaultHeaders: {
        "X-Request-Source": "langchain-tutorial"
      }
    }
  });
}

// Para tarefas mais simples, use modelos mais rápidos
export function createFastModel() {
  return new ChatOpenAI({
    model: "gpt-4o-mini",
    temperature: 0,
    maxRetries: 6
  });
}
```

### Modelo com saída estruturada

```typescript
// src/lib/structured-model.ts
import { ChatOpenAI } from "@langchain/openai";
import { CodeReviewSchema } from "../schemas/code-review.ts";

export function createCodeReviewModel() {
  const baseModel = new ChatOpenAI({
    model: "gpt-5.1-codex-max",
    temperature: 0,
    useResponsesApi: true
  });

  // withStructuredOutput configura o modelo para retornar JSON validado
  return baseModel.withStructuredOutput(CodeReviewSchema, {
    name: "code_review",
    strict: true, // Ativa strict mode da OpenAI para conformidade de schema
    method: "jsonSchema" // Padrão para modelos de raciocínio
  });
}
```

## Exemplos práticos completos

### Exemplo básico: Extração de entidades

```typescript
// src/examples/basic-extraction.ts
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const PersonSchema = z.object({
  name: z.string().describe("Nome completo da pessoa"),
  role: z.string().describe("Cargo ou função profissional"),
  company: z.nullable(z.string()).describe("Empresa onde trabalha, null se não mencionado"),
  skills: z.array(z.string()).describe("Lista de habilidades técnicas mencionadas")
});

async function extractPerson(text: string) {
  const model = new ChatOpenAI({
    model: "gpt-4o-mini", // Modelo rápido para extração simples
    temperature: 0
  }).withStructuredOutput(PersonSchema, { strict: true });

  const result = await model.invoke([
    {
      role: "system",
      content: "Extraia informações da pessoa mencionada no texto."
    },
    {
      role: "user",
      content: text
    }
  ]);

  return result;
}

// Uso
const pessoa = await extractPerson(
  "João Silva é desenvolvedor sênior na TechCorp, especializado em TypeScript, Node.js e arquitetura de microsserviços."
);

console.log(pessoa);
// { name: "João Silva", role: "desenvolvedor sênior", company: "TechCorp", skills: ["TypeScript", "Node.js", "arquitetura de microsserviços"] }
```

### Exemplo intermediário: Revisão de código com GPT-5.1-Codex-Max

```typescript
// src/examples/code-review.ts
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { CodeReviewSchema, type CodeReview } from "../schemas/code-review.ts";

const SYSTEM_PROMPT = `Você é um revisor de código sênior especializado em TypeScript e Node.js.
Analise o código fornecido com foco em:
- Vulnerabilidades de segurança
- Problemas de performance
- Manutenibilidade e legibilidade
- Bugs potenciais

Seja específico nas sugestões, incluindo código quando apropriado.`;

async function reviewCode(code: string): Promise<CodeReview> {
  const model = new ChatOpenAI({
    model: "gpt-5.1-codex-max",
    temperature: 0,
    useResponsesApi: true,
    maxRetries: 3
  }).withStructuredOutput(CodeReviewSchema, {
    name: "code_review",
    strict: true
  });

  const result = await model.invoke([
    new SystemMessage(SYSTEM_PROMPT),
    new HumanMessage(`Analise este código:\n\n\`\`\`typescript\n${code}\n\`\`\``)
  ]);

  return result;
}

// Exemplo de uso
const codeToReview = `
async function getUser(id: any) {
  const query = "SELECT * FROM users WHERE id = " + id;
  const result = await db.query(query);
  return result[0];
}
`;

const review = await reviewCode(codeToReview);
console.log("Score:", review.overallScore);
console.log("Issues:", review.issues.length);
review.issues.forEach(issue => {
  console.log(`[${issue.severity}] Linha ${issue.line}: ${issue.description}`);
});
```

### Exemplo avançado: Agente de refatoração com ferramentas

```typescript
// src/examples/refactoring-agent.ts
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { HumanMessage } from "@langchain/core/messages";

// Definição de ferramentas que o modelo pode usar
const analyzeComplexityTool = tool(
  async ({ code }) => {
    // Simulação de análise de complexidade
    const lines = code.split("\n").length;
    const functions = (code.match(/function|=>/g) || []).length;
    return JSON.stringify({
      lines,
      functions,
      complexity: lines > 50 ? "high" : lines > 20 ? "medium" : "low"
    });
  },
  {
    name: "analyze_complexity",
    description: "Analisa a complexidade ciclomática e métricas do código",
    schema: z.object({
      code: z.string().describe("Código fonte para análise")
    })
  }
);

const suggestPatternTool = tool(
  async ({ pattern, context }) => {
    const patterns: Record<string, string> = {
      "factory": "Use Factory Pattern para desacoplar a criação de objetos",
      "strategy": "Use Strategy Pattern para algoritmos intercambiáveis",
      "observer": "Use Observer Pattern para notificações reativas"
    };
    return patterns[pattern] || `Padrão ${pattern} sugerido para: ${context}`;
  },
  {
    name: "suggest_pattern",
    description: "Sugere um design pattern apropriado para o contexto",
    schema: z.object({
      pattern: z.string().describe("Nome do design pattern"),
      context: z.string().describe("Contexto onde aplicar o pattern")
    })
  }
);

// Schema para a resposta final
const RefactoringPlanSchema = z.object({
  originalComplexity: z.string().describe("Avaliação da complexidade original"),
  proposedChanges: z.array(z.object({
    description: z.string(),
    priority: z.enum(["high", "medium", "low"]),
    estimatedEffort: z.string()
  })).describe("Lista de mudanças propostas"),
  refactoredCode: z.string().describe("Código refatorado completo"),
  improvementMetrics: z.object({
    readabilityGain: z.number().min(0).max(100),
    maintainabilityGain: z.number().min(0).max(100),
    testabilityGain: z.number().min(0).max(100)
  }).describe("Métricas de melhoria estimadas em porcentagem")
});

async function createRefactoringPlan(code: string) {
  // Primeiro, usa o modelo com ferramentas para análise
  const analysisModel = new ChatOpenAI({
    model: "gpt-5.1-codex-max",
    temperature: 0,
    useResponsesApi: true
  }).bindTools([analyzeComplexityTool, suggestPatternTool]);

  // Executa análise inicial
  const analysisResult = await analysisModel.invoke([
    new HumanMessage(`Analise este código e sugira melhorias:\n\n${code}`)
  ]);

  // Depois, gera plano estruturado
  const planModel = new ChatOpenAI({
    model: "gpt-5.1-codex-max",
    temperature: 0,
    useResponsesApi: true
  }).withStructuredOutput(RefactoringPlanSchema, { strict: true });

  const plan = await planModel.invoke([
    new HumanMessage(`
      Baseado na análise anterior, crie um plano de refatoração completo.
      
      Código original:
      ${code}
      
      Análise:
      ${JSON.stringify(analysisResult.tool_calls, null, 2)}
    `)
  ]);

  return plan;
}

// Uso
const legacyCode = `
function processData(data) {
  let result = [];
  for (let i = 0; i < data.length; i++) {
    if (data[i].type === 'A') {
      result.push({ ...data[i], processed: true, value: data[i].value * 2 });
    } else if (data[i].type === 'B') {
      result.push({ ...data[i], processed: true, value: data[i].value + 10 });
    } else if (data[i].type === 'C') {
      result.push({ ...data[i], processed: true, value: data[i].value / 2 });
    }
  }
  return result;
}
`;

const plan = await createRefactoringPlan(legacyCode);
console.log("Plano de Refatoração:", JSON.stringify(plan, null, 2));
```

## Tratamento de erros robusto

Os modelos de raciocínio podem recusar requisições por motivos de segurança ou falhar por limites de tokens. Um tratamento adequado é essencial para produção.

```typescript
// src/lib/error-handling.ts
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

class StructuredOutputError extends Error {
  constructor(
    message: string,
    public readonly cause?: unknown,
    public readonly refusal?: string
  ) {
    super(message);
    this.name = "StructuredOutputError";
  }
}

interface InvokeOptions<T> {
  model: ReturnType<ChatOpenAI["withStructuredOutput"]>;
  messages: Parameters<ChatOpenAI["invoke"]>[0];
  maxRetries?: number;
  onRetry?: (attempt: number, error: Error) => void;
}

async function invokeWithRetry<T>({
  model,
  messages,
  maxRetries = 3,
  onRetry
}: InvokeOptions<T>): Promise<T> {
  let lastError: Error | undefined;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await model.invoke(messages);
      
      // Verifica se houve recusa do modelo
      if (result && typeof result === "object" && "refusal" in result) {
        throw new StructuredOutputError(
          "Modelo recusou a requisição",
          undefined,
          result.refusal as string
        );
      }
      
      return result as T;
      
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      
      // Erros que não devem ser retentados
      if (error instanceof StructuredOutputError && error.refusal) {
        throw error;
      }
      
      // Rate limit ou erro temporário
      const isRetryable = 
        lastError.message.includes("429") ||
        lastError.message.includes("timeout") ||
        lastError.message.includes("ECONNRESET");
      
      if (!isRetryable || attempt === maxRetries) {
        throw new StructuredOutputError(
          `Falha após ${attempt} tentativas: ${lastError.message}`,
          lastError
        );
      }
      
      // Backoff exponencial com jitter
      const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 1000, 30000);
      onRetry?.(attempt, lastError);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}

// Uso
const ResponseSchema = z.object({
  answer: z.string(),
  confidence: z.number()
});

async function safeInvoke(question: string) {
  const model = new ChatOpenAI({
    model: "gpt-4o-mini",
    temperature: 0
  }).withStructuredOutput(ResponseSchema, { strict: true });

  try {
    const result = await invokeWithRetry({
      model,
      messages: [{ role: "user", content: question }],
      maxRetries: 3,
      onRetry: (attempt, error) => {
        console.warn(`Tentativa ${attempt} falhou: ${error.message}. Retentando...`);
      }
    });
    
    return { success: true, data: result };
    
  } catch (error) {
    if (error instanceof StructuredOutputError) {
      console.error("Erro estruturado:", error.message);
      if (error.refusal) {
        console.error("Motivo da recusa:", error.refusal);
      }
    }
    return { success: false, error: error instanceof Error ? error.message : "Erro desconhecido" };
  }
}
```

## Otimização e melhores práticas

### Controle de esforço de raciocínio

O parâmetro `reasoning.effort` controla quantos tokens de "pensamento" o modelo usa. Para a Responses API com LangChain.js, configure através de opções do modelo.

```typescript
// Diferentes níveis para diferentes tarefas
const quickModel = new ChatOpenAI({
  model: "gpt-5.1-codex-max",
  useResponsesApi: true,
  // Para tarefas simples, use esforço mínimo
  modelKwargs: {
    reasoning: { effort: "none" }
  }
});

const deepModel = new ChatOpenAI({
  model: "gpt-5.1-codex-max", 
  useResponsesApi: true,
  // Para tarefas complexas, máximo raciocínio
  modelKwargs: {
    reasoning: { effort: "xhigh" }
  }
});
```

### Roteamento inteligente de modelos

```typescript
// src/lib/model-router.ts
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

type TaskComplexity = "simple" | "moderate" | "complex" | "expert";

const modelConfig: Record<TaskComplexity, { model: string; reasoning?: string }> = {
  simple: { model: "gpt-4o-mini" },
  moderate: { model: "gpt-4o" },
  complex: { model: "gpt-5.1-codex-max", reasoning: "medium" },
  expert: { model: "gpt-5.1-codex-max", reasoning: "xhigh" }
};

function selectModel(complexity: TaskComplexity) {
  const config = modelConfig[complexity];
  
  return new ChatOpenAI({
    model: config.model,
    temperature: 0,
    useResponsesApi: config.model.includes("5.1"),
    ...(config.reasoning && {
      modelKwargs: { reasoning: { effort: config.reasoning } }
    })
  });
}

// Classificador de complexidade
const ComplexitySchema = z.object({
  complexity: z.enum(["simple", "moderate", "complex", "expert"]),
  reasoning: z.string()
});

async function routeTask(task: string) {
  const classifier = new ChatOpenAI({ model: "gpt-4o-mini", temperature: 0 })
    .withStructuredOutput(ComplexitySchema);
  
  const { complexity } = await classifier.invoke([
    {
      role: "system",
      content: `Classifique a complexidade da tarefa:
        - simple: perguntas diretas, formatação básica
        - moderate: análise simples, transformações de dados
        - complex: debugging, otimização, arquitetura
        - expert: refatoração completa, sistemas distribuídos, segurança`
    },
    { role: "user", content: task }
  ]);
  
  return selectModel(complexity);
}
```

### Cache com Redis

```typescript
// src/lib/cache.ts
import { ChatOpenAI } from "@langchain/openai";
import { createHash } from "node:crypto";

// Cache simples em memória (para produção, use Redis)
const cache = new Map<string, { result: unknown; timestamp: number }>();
const TTL = 3600000; // 1 hora

function getCacheKey(model: string, messages: unknown[]): string {
  const content = JSON.stringify({ model, messages });
  return createHash("sha256").update(content).digest("hex");
}

async function cachedInvoke<T>(
  model: ChatOpenAI,
  messages: Parameters<ChatOpenAI["invoke"]>[0]
): Promise<T> {
  const key = getCacheKey(model.model, messages as unknown[]);
  const cached = cache.get(key);
  
  if (cached && Date.now() - cached.timestamp < TTL) {
    console.log("Cache hit!");
    return cached.result as T;
  }
  
  const result = await model.invoke(messages);
  cache.set(key, { result, timestamp: Date.now() });
  
  return result as T;
}
```

## Estratégias de teste

```typescript
// src/tests/schema-validation.test.ts
import { describe, it, expect } from "node:test";
import { z } from "zod";
import { CodeReviewSchema } from "../schemas/code-review.ts";

describe("CodeReviewSchema", () => {
  it("deve aceitar dados válidos", () => {
    const validData = {
      summary: "Código bem estruturado",
      overallScore: 8,
      issues: [
        {
          line: 10,
          severity: "warning",
          category: "performance",
          description: "Loop pode ser otimizado",
          suggestion: "Use map() em vez de for"
        }
      ],
      positiveAspects: ["Boa nomenclatura", "Código modular"],
      refactoringPriority: null
    };
    
    const result = CodeReviewSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });
  
  it("deve rejeitar score fora do intervalo", () => {
    const invalidData = {
      summary: "Test",
      overallScore: 15, // Inválido: máximo é 10
      issues: [],
      positiveAspects: [],
      refactoringPriority: null
    };
    
    const result = CodeReviewSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
  });
});

// Teste de integração com mock
describe("Code Review Integration", () => {
  it("deve retornar estrutura correta do modelo", async () => {
    // Em testes, use modelo mais barato ou mock
    const { reviewCode } = await import("../examples/code-review.ts");
    
    const result = await reviewCode("const x = 1;");
    
    // Valida estrutura do retorno
    expect(result).toHaveProperty("summary");
    expect(result).toHaveProperty("overallScore");
    expect(typeof result.overallScore).toBe("number");
    expect(Array.isArray(result.issues)).toBe(true);
  });
});
```

Execute os testes com Node.js nativo:

```bash
node --test src/tests/*.test.ts
```

## Guia de troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| `Error: 400 Invalid schema` | Zod v4 incompatível | Instale `zod@^3.22.4` |
| `z.optional() ignorado` | Modelos de raciocínio não suportam | Use `z.nullable()` |
| `Enum not supported` | TypeScript type stripping | Use `--experimental-transform-types` ou unions |
| `withStructuredOutput retorna Record<string, any>` | Bug com Zod v4 | Downgrade para Zod v3 |
| Timeout em requisições | Modelos de raciocínio demoram mais | Aumente `timeout` para 120000+ |
| Rate limit 429 | Muitas requisições | Implemente backoff exponencial |
| Streaming não funciona | `stream()` não suporta structured output | Use `streamEvents()` ao invés |

### Verificação de compatibilidade do schema

```typescript
import { zodToJsonSchema } from "zod-to-json-schema";

function validateSchemaCompatibility(schema: z.ZodTypeAny): void {
  try {
    const jsonSchema = zodToJsonSchema(schema);
    console.log("Schema válido para OpenAI:");
    console.log(JSON.stringify(jsonSchema, null, 2));
    
    // Verifica tamanho (OpenAI tem limite de ~64KB)
    const size = JSON.stringify(jsonSchema).length;
    if (size > 60000) {
      console.warn(`⚠️ Schema muito grande: ${size} bytes`);
    }
  } catch (error) {
    console.error("Schema incompatível:", error);
  }
}
```

## Resumo de versões testadas

| Pacote | Versão | Observações |
|--------|--------|-------------|
| Node.js | 24.x+ | Type stripping habilitado por padrão |
| TypeScript | 5.8+ | Necessário para `erasableSyntaxOnly` |
| @langchain/openai | 1.2.0 | Suporte a Responses API |
| @langchain/core | 0.3.40 | Core do LangChain.js |
| zod | 3.22.4 | ⚠️ Não use v4 com LangChain.js |
| zod-to-json-schema | 3.x | Usado internamente pelo LangChain |

O GPT-5.1-Codex-Max representa o estado da arte em modelos de codificação agêntica, oferecendo capacidades sem precedentes para tarefas de programação de longa duração. Combinado com a elegância do TypeScript nativo no Node.js 24 e a robustez dos schemas Zod, esta stack fornece uma base sólida para construir aplicações de IA de nível profissional.