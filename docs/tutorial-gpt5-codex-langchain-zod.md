---
# Tutorial Completo: GPT-5.1-Codex-Max com LangChain.js e Zod

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
```
... (continua)