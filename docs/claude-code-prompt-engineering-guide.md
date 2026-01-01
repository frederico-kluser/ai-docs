# Guia Definitivo de Prompt Engineering para Claude Code com Claude Opus 4.5

**Claude Code redefine o desenvolvimento ágil**: esta ferramenta de linha de comando da Anthropic transforma como desenvolvedores interagem com IA para codificação. Com acesso completo ao sistema de arquivos, execução de comandos bash e capacidade de operar autonomamente por sessões de 30+ minutos, Claude Code oferece uma experiência fundamentalmente diferente das interfaces de chat tradicionais. Este guia consolidado apresenta técnicas oficiais e descobertas da comunidade para extrair o máximo potencial do Opus 4.5.

O diferencial crítico está na arquitetura agêntica: enquanto Claude.ai processa interações isoladas, Claude Code opera como um **REPL autônomo** capaz de explorar codebases, executar testes, criar commits e até abrir pull requests—tudo em uma única sessão contínua. Dominar os padrões de prompting específicos para este ambiente multiplica drasticamente sua produtividade.

---

## Arquitetura e funcionamento do Claude Code

Claude Code opera como um loop REPL (Read-Eval-Print Loop) agêntico que executa diretamente no terminal. Diferente das interfaces web, possui **acesso total ao sistema de arquivos**, capacidade de executar comandos shell e integração nativa com git. A arquitetura inclui um sistema de ferramentas built-in (Read, Write, Edit, Bash, Glob, Grep) e suporte a MCP (Model Context Protocol) para conexão com serviços externos.

O modelo Opus 4.5, lançado em novembro de 2025, representa o ápice da engenharia de software assistida por IA da Anthropic. Com **80.9% no SWE-bench Verified** (versus 77.2% do Sonnet), o modelo demonstra superioridade em debugging multi-sistema, refatorações em larga escala e tarefas de longa duração. Notavelmente, utiliza até **65% menos tokens** que predecessores para resultados equivalentes ou superiores.

### Diferenças fundamentais entre CLI e interface web

| Característica | Claude Code (CLI) | Claude.ai (Web) |
|----------------|-------------------|-----------------|
| Acesso a arquivos | Sistema completo local | Upload individual |
| Execução de comandos | Bash/shell direto | Nenhum |
| Capacidade agêntica | Tarefas multi-passo autônomas | Interações single-turn |
| Fonte de contexto | Estrutura completa do projeto + MCP | Documentos uploaded |
| Integração Git | Operações nativas, criação de PRs | Nenhuma |

O sistema de ferramentas do Claude Code inclui: **Read** (leitura de arquivos), **Write** (criação de arquivos), **Edit** (modificação), **Bash** (execução de comandos), **Glob** (busca por padrão), **Grep** (busca em conteúdo), **WebSearch** e **WebFetch** para acesso à web, e **Task** para criação de sub-agentes especializados.

---

## Princípios fundamentais de prompting

A especificidade é o fator mais determinante para resultados de qualidade no Claude Code. O modelo consegue inferir intenções, mas não lê mentes—quanto mais contexto concreto você fornecer, melhores serão os outputs.

### Padrões de instrução explícita

```
❌ Ruim: "adicione testes para foo.py"
✅ Bom: "escreva um novo caso de teste para foo.py, cobrindo o edge case 
       onde o usuário está deslogado. evite mocks"

❌ Ruim: "por que ExecutionFactory tem uma API tão estranha?"
✅ Bom: "analise o histórico git de ExecutionFactory e resuma como sua 
       API evoluiu ao longo do tempo"

❌ Ruim: "adicione um widget de calendário"
✅ Bom: "examine como widgets existentes são implementados na home page 
       para entender os padrões. HotDogWidget.php é um bom exemplo. 
       Siga o padrão para implementar um widget de calendário que 
       permita usuários selecionar um mês e paginar para frente/trás."
```

### Os quatro modos de prompting

A comunidade identificou quatro modos distintos que otimizam diferentes tipos de tarefas:

**Modo Build**: Instruções curtas, concretas, sem meta-instruções. Use para implementação direta.
```
> Crie um endpoint REST em /api/users que retorne JSON paginado
```

**Modo Debug**: Compartilhe contexto primeiro (logs, erros, ambiente) antes de pedir diagnóstico.
```
> Estou vendo este erro após as mudanças de auth: [cole o erro]. 
> Aqui está o log relevante: [cole logs]. 
> Diagnostique antes de sugerir correções.
```

**Modo Refine**: Peça crítica OU reescrita, nunca ambos simultaneamente.
```
> Revise esta função para problemas de performance primeiro, 
> depois sugira melhorias
```

**Modo Learn**: Solicite explicações e ensino conceitual.
```
> Explique como o rebalancing do Kafka funciona no contexto 
> do nosso setup de consumers
```

### Fornecimento de contexto eficiente

O Claude Code oferece múltiplas formas de injetar contexto:

- **Referência direta**: `@src/utils/helpers.js` (com tab-completion)
- **Drag and drop**: Arraste imagens diretamente no prompt
- **Paste de screenshots**: Cmd+Ctrl+Shift+4 no macOS
- **Piping**: `cat logs.txt | claude -p "explique"`
- **URLs**: Cole URLs para fetch automático
- **Arquivos CLAUDE.md**: Carregamento automático de contexto persistente
- **MCP servers**: Fontes de dados externas via Model Context Protocol

---

## Estratégias de decomposição de tarefas

### O workflow Explore → Plan → Code → Commit

Este é o padrão recomendado oficialmente pela Anthropic para maximizar qualidade e controle:

```bash
# Fase 1: Exploração (somente leitura)
> Leia os arquivos de autenticação em src/auth/. 
> Não escreva código ainda.
> Quais padrões esses arquivos usam para tratamento de erros?

# Fase 2: Planejamento
> Crie um plano para adicionar suporte OAuth2. 
> Think hard sobre edge cases.
> [Revise o plano, forneça feedback]

# Fase 3: Implementação
> Implemente a fase 1 do seu plano (configuração do cliente OAuth).

# Fase 4: Commit
> Faça commit dessas mudanças com mensagem descritiva e crie um PR.
```

A separação explícita entre fases previne que o Claude "pule" direto para implementação antes de entender completamente o problema.

### Test-Driven Development com Claude

O padrão TDD funciona excepcionalmente bem com Claude Code:

```bash
# Passo 1: Escreva testes
> Escreva testes para UserNotificationService baseado nesses pares 
> input/output:
> - Usuário com preferência email → envia email
> - Usuário opted out → sem notificação
> Estamos fazendo TDD, então NÃO crie implementações mock.

# Passo 2: Verifique que falham
> Execute os testes e confirme que falham. 
> NÃO escreva código de implementação ainda.

# Passo 3: Commit dos testes
> Commit os testes com mensagem "Add notification service tests"

# Passo 4: Implemente
> Escreva código que passe os testes. Não modifique os testes. 
> Continue até todos passarem.

# Passo 5: Verifique com subagent
> Use um subagent para verificar se a implementação não está 
> overfitting aos testes.
```

### Decomposição por complexidade

Para tarefas grandes, use esta estratégia de fragmentação:

- **Tarefas enormes** (15-25 subtarefas): Aplicações completas, rewrites maiores
- **Tarefas grandes** (8-15 subtarefas): Módulos de feature, refatorações significativas
- **Tarefas médias** (3-8 subtarefas): Novos componentes, endpoints de API
- **Tarefas pequenas**: Implementação direta

```bash
# Em vez de: "refatore toda essa codebase"
# Faça assim:
> Auditoria de segurança para módulos de autenticação (src/auth/) apenas
> Refatore camada de queries do banco com novos padrões (src/db/)
> Gere suítes de teste para endpoints da API (src/api/)
> Modernize componentes legacy para TypeScript (src/legacy/)
```

---

## Referência completa de comandos

### Comandos de instalação

```bash
# MacOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew (MacOS)
brew install --cask claude-code

# Windows
irm https://claude.ai/install.ps1 | iex

# NPM (requer Node.js 18+)
npm install -g @anthropic-ai/claude-code
```

### Comandos CLI principais

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `claude` | Inicia REPL interativo | `claude` |
| `claude "query"` | Inicia com prompt inicial | `claude "explique este projeto"` |
| `claude -p "query"` | Modo print (SDK), executa e sai | `claude -p "explique esta função"` |
| `cat file \| claude -p` | Processa conteúdo via pipe | `cat logs.txt \| claude -p "explique"` |
| `claude -c` | Continua conversa mais recente | `claude -c` |
| `claude --resume` | Seleção interativa de sessão | `claude --resume` |
| `claude update` | Atualiza para versão mais recente | `claude update` |

### Flags CLI essenciais

| Flag | Descrição |
|------|-----------|
| `--model <alias>` | Especifica modelo (opus, sonnet, haiku, opusplan) |
| `--add-dir <path>` | Adiciona diretórios de trabalho |
| `--allowedTools` | Pré-autoriza ferramentas específicas |
| `--disallowedTools` | Bloqueia ferramentas específicas |
| `--append-system-prompt` | Adiciona ao system prompt padrão |
| `--system-prompt` | Substitui system prompt inteiro |
| `--max-turns <n>` | Limita turnos agênticos |
| `--permission-mode plan` | Modo somente leitura |
| `--dangerously-skip-permissions` | Pula todos os prompts de permissão |
| `--output-format json` | Formato de saída (text, json, stream-json) |

### Slash commands internos

**Gerenciamento de sessão:**
- `/help` - Exibe todos os comandos disponíveis
- `/clear` - Reseta histórico de conversa
- `/exit` - Sai da sessão REPL
- `/resume` - Resume sessões nomeadas
- `/rename` - Nomeia sessão atual

**Gerenciamento de contexto:**
- `/compact [instruções]` - Comprime conversa com foco opcional
- `/context` - Visualiza uso de contexto como grade colorida
- `/cost` - Exibe estatísticas de uso de tokens

**Projeto e memória:**
- `/init` - Gera guia CLAUDE.md do projeto
- `/memory` - Edita arquivos CLAUDE.md
- `/add-dir` - Adiciona diretórios de trabalho

**Configuração:**
- `/config` - Abre interface de configurações
- `/permissions` - Gerencia ferramentas permitidas/negadas
- `/model` - Troca modelo Claude
- `/theme` - Muda tema da UI

**Desenvolvimento:**
- `/review` - Solicita code review
- `/todos` - Lista TODOs rastreados
- `/agents` - Gerencia subagentes customizados
- `/rewind` - Volta ao checkpoint

### Atalhos de teclado

| Atalho | Ação |
|--------|------|
| **Ctrl+O** | Toggle modo verbose (mostra thinking) |
| **Tab** | Toggle extended thinking on/off |
| **Shift+Tab** | Cicla modos de permissão |
| **Ctrl+B** | Move tarefa para background |
| **Ctrl+R** | Busca reversa no histórico |
| **Ctrl+L** | Limpa tela, preserva conversa |
| **Ctrl+G** | Edita prompt em editor externo (v2.0.10+) |
| **Escape** | Para/interrompe Claude |
| **Escape x2** | Volta no histórico para editar prompt anterior |
| **#** | Adiciona ao CLAUDE.md (memória) |
| **!comando** | Executa bash diretamente (bypass Claude) |

---

## Capacidades avançadas e comandos ocultos

### Extended thinking: a hierarquia de gatilhos

Claude Code possui uma **camada de pré-processamento** que detecta palavras-chave específicas e aloca budgets de thinking automaticamente:

| Nível | Palavras-chave | Budget de Tokens | Custo Estimado |
|-------|----------------|------------------|----------------|
| **Básico** | "think" | ~4.000 tokens | ~$0.06/tarefa |
| **Intermediário** | "think hard", "think more", "think deeply" | ~10.000 tokens | ~$0.15/tarefa |
| **Máximo** | "**ultrathink**", "think harder", "think really hard" | ~32.000 tokens | ~$0.48/tarefa |

**Exemplos de sintaxe exata:**
```bash
> Analise esta codebase e recomende oportunidades de otimização ultrathink

> Precisamos migrar de REST para GraphQL. Think harder sobre a 
> estratégia de migração.

> Design uma arquitetura de e-commerce escalável. 
> Por favor ultrathink este desafio.

> think hard sobre potenciais vulnerabilidades de segurança nesta abordagem
```

**Nota crítica**: O gatilho ultrathink **só funciona quando MAX_THINKING_TOKENS não está definido**. Quando configurado, essa variável de ambiente tem prioridade e controla o budget de thinking para TODAS as requisições.

### Controles de budget de thinking

**Variáveis de ambiente:**
```bash
# Define budget customizado de tokens de thinking (mínimo 1.024)
export MAX_THINKING_TOKENS=32000

# Controla máximo de tokens de output
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=8192
```

**Configuração em settings.json (não documentada oficialmente):**
```json
{
  "alwaysThinkingEnabled": true
}
```

Adicione a `~/.claude/settings.json` para forçar thinking mode habilitado por padrão.

**Visualização do processo de thinking:**
- **Ctrl+O**: Toggle modo verbose para ver reasoning interno em texto itálico cinza
- **Tab**: Toggle thinking mode on/off durante sessão

### Comandos e ferramentas internas

**Bypass de shell com prefixo `!`:**
```bash
!git status
!npm test
!ls -la
```
Executa comandos diretamente, bypassing o modo conversacional.

**Ferramentas internas parcialmente documentadas:**
- `Read` - Leitura de arquivos
- `Write` - Escrita de arquivos
- `Edit` - Edição de arquivos
- `Bash` - Execução de comandos shell
- `ExitPlanMode` - Ferramenta não documentada que troca modos de permissão
- `Task` - Spawn de sub-agentes
- `Explore` - Exploração read-only da codebase

### Variáveis de ambiente completas

```bash
# Core
ANTHROPIC_API_KEY=<key>
ANTHROPIC_MODEL=<model-name>

# Thinking/Tokens
MAX_THINKING_TOKENS=<number>
CLAUDE_CODE_MAX_OUTPUT_TOKENS=<number>

# Controles de modelo
ANTHROPIC_DEFAULT_OPUS_MODEL=<model>
ANTHROPIC_DEFAULT_SONNET_MODEL=<model>
ANTHROPIC_DEFAULT_HAIKU_MODEL=<model>
CLAUDE_CODE_SUBAGENT_MODEL=<model>

# Controles de comportamento
DISABLE_AUTOUPDATER=1
DISABLE_TELEMETRY=1
DISABLE_PROMPT_CACHING=1
DISABLE_COST_WARNINGS=1
BASH_MAX_TIMEOUT_MS=<ms>
MCP_TOOL_TIMEOUT=<ms>

# Debugging
DEBUG_CLAUDE_CODE=1
```

### O modo opusplan: híbrido inteligente

O modelo alias `opusplan` oferece o melhor dos dois mundos:
- **Plan Mode**: Usa Opus 4.5 para reasoning complexo e decisões de arquitetura
- **Execution Mode**: Troca automaticamente para Sonnet 4.5 para geração de código

```bash
claude --model opusplan
```

Isto dá o reasoning superior do Opus para planejamento e a eficiência do Sonnet para implementação.

---

## Templates de prompts e padrões prontos

### Estrutura recomendada para CLAUDE.md

```markdown
# Nome do Projeto

## Comandos
- `npm run build`: Build do projeto
- `npm run test`: Executa testes
- `npm run lint`: Executa linter

## Estilo de Código
- Use ES modules (import/export), não CommonJS
- Prefira TypeScript strict mode
- Componentes devem ser funcionais com hooks

## Arquitetura
- `src/api/`: Endpoints REST
- `src/services/`: Lógica de negócio
- `src/models/`: Modelos do banco

## Anti-padrões a Evitar
- Nunca coloque lógica de negócio em controllers
- Não use any-typing em TypeScript
- Evite queries N+1 no banco

## Requisitos de Teste
- Todo código novo requer testes unitários
- Testes de integração para endpoints da API
- Execute testes antes de commit
```

### Comando customizado para fix de issues

Crie `.claude/commands/fix-issue.md`:

```markdown
Por favor analise e corrija a issue do GitHub: $ARGUMENTS.

Siga estes passos:
1. Use `gh issue view` para obter detalhes da issue
2. Entenda o problema descrito na issue
3. Busque na codebase por arquivos relevantes
4. Implemente as mudanças necessárias para corrigir
5. Escreva e execute testes para verificar o fix
6. Garanta que código passa linting e type checking
7. Crie mensagem de commit descritiva
8. Push e crie um PR

Use o GitHub CLI (`gh`) para todas as tarefas relacionadas ao GitHub.
```

### Template de debugging

```
Estou encontrando este erro: [cole mensagem de erro exata]

Contexto:
- Isso começou a acontecer após: [mudanças recentes]
- Passos de reprodução: [como triggerar]
- Ambiente: [versão Node, OS, etc.]

Por favor:
1. Primeiro diagnostique a causa raiz - não sugira fixes imediatamente
2. Trace o caminho de execução que leva a este erro
3. Identifique quais edge cases poderiam causar isso
4. Então sugira um fix que endereça a causa raiz
5. Recomende validação para prevenir este tipo de bug no futuro
```

### Checklist de deployment para produção

```
Estou prestes a deployar esta mudança para produção. 
Faça de advogado do diabo:
- Quais edge cases eu perdi?
- O que poderia quebrar sob alta carga?
- Existem implicações de segurança?
- Que monitoramento devo adicionar?
- Qual é meu plano de rollback?
```

### Template de code review

```markdown
Realize um code review compreensivo das mudanças recentes:
1. Verifique se código segue nossas convenções TypeScript e React
2. Verifique tratamento de erros e estados de loading apropriados
3. Garanta padrões de acessibilidade
4. Revise cobertura de testes para nova funcionalidade
5. Verifique vulnerabilidades de segurança
6. Valide implicações de performance
7. Confirme que documentação está atualizada

Use nosso checklist de qualidade estabelecido e atualize CLAUDE.md 
com novos padrões descobertos.
```

---

## Anti-padrões e erros comuns

### Anti-padrões em CLAUDE.md

**❌ Não faça @-mention de arquivos de documentação inteiros:**
```markdown
# Ruim - infla a context window
@docs/full-api-reference.md
```
```markdown
# Bom - referência com contexto
Para uso complexo da API ou FooBarError, veja docs/api-reference.md 
para troubleshooting.
```

**❌ Não use apenas constraints negativas:**
```markdown
# Ruim - Claude fica travado
Nunca use a flag --force.
```
```markdown
# Bom - fornece alternativas
Evite --force flag; use --force-with-lease para force pushes mais seguros.
```

**❌ Não escreva documentação verbosa:**
```markdown
# Ruim - tratando CLAUDE.md como onboarding de dev júnior
O diretório components contém todos os componentes React. 
Componentes são organizados por feature...
```
```markdown
# Bom - conciso, acionável
- Componentes em src/components/ usam padrões funcionais com hooks
- Prefira composição sobre herança
```

### Anti-padrões de workflow

**❌ Deixar Claude pular direto para código:**
```bash
# Ruim
> Adicione suporte OAuth

# Bom
> Analise nosso sistema de auth atual e crie um plano para suporte OAuth. 
> Não escreva código até eu aprovar.
```

**❌ Misturar modos de prompting:**
```bash
# Ruim - muitas instruções, cria confusão
> Corrija o bug de login, adicione testes, deixe rápido, evite ser 
> verboso, e também melhore performance
```

**❌ Confiar em auto-compaction:**
> "Evito /compact o máximo possível. A compactação automática é opaca, propensa a erros e não bem otimizada."

**Melhor: Workflow Document & Clear:**
1. Peça para Claude salvar plano/progresso em arquivo .md
2. `/clear` o estado
3. Inicie nova sessão, diga ao Claude para ler o .md e continuar

### Anti-padrões de subagents

**❌ Subagents customizados que isolam contexto:**
> Criar um subagent `PythonTests` esconde todo contexto de testes do agente principal—ele não consegue mais raciocinar holisticamente sobre mudanças.

**❌ Ativação inconsistente:**
> Claude frequentemente ignora subagents apropriados a menos que você os nomeie explicitamente.

**Melhor abordagem**: Use `Task()` para arquitetura Master-Clone, deixando o agente principal decidir quando e como delegar trabalho.

### Anti-padrões de geração de código

**❌ Over-engineering (tendência do Opus 4.5):**
```markdown
# Adicione ao CLAUDE.md para prevenir
Evite over-engineering. Apenas faça mudanças diretamente solicitadas 
ou claramente necessárias. Uma feature simples não precisa de 
configurabilidade extra.
```

**❌ Criar arquivos temporários desnecessários:**
```markdown
# Adicione ao CLAUDE.md
Se você criar quaisquer arquivos temporários, scripts ou helpers 
para iteração, limpe esses arquivos removendo-os ao final da tarefa.
```

---

## Workflows práticos de ponta a ponta

### Workflow de desenvolvimento paralelo multi-agente

**Usando git worktrees para sessões Claude paralelas:**
```bash
# Crie worktrees separadas para features diferentes
git worktree add ../project-auth -b feature/auth
git worktree add ../project-ui -b feature/ui-refresh

# Execute Claude em cada (terminais separados)
cd ../project-auth && claude
cd ../project-ui && claude
```

### Workflow para codebase grande (400K+ linhas)

**Desenvolvimento paralelo baseado em sprints:**
```bash
# Fase 1: Planejamento com Claude
> Quebre esta feature em tarefas adequadas para desenvolvimento paralelo
> Identifique dependências e conflitos potenciais
> Agrupe tarefas em sprints baseado no que é seguro executar simultaneamente
> Crie cards de tarefa claros para cada "agente"

# Fase 2: Prompt de verificação
> Você revisou esses documentos de sprint contra a codebase?
> Esses requisitos fazem sentido baseado em @path-to-feature-docs/?
> Alguma mudança necessária para garantir que agentes completem 
> essas tarefas como engenheiros staff com 15+ anos de experiência?

# Fase 3: Lance 4 terminais paralelos
# Terminal 1-4: Cada um recebe seu card de sprint
> Você é agente 1, engenheiro staff com mais de 15 anos de experiência.
> Por favor revise completamente @sprint1/
> Comece sua tarefa, garantindo:
> - Usar nosso handler de erro customizado
> - Escrever testes para funcionalidade, não implementação
> - Executar linter, build e testes antes de declarar conclusão
```

### Workflow visual com screenshots

```bash
# Dê ao Claude habilidade de ver
# (Instale Puppeteer MCP server ou iOS Simulator MCP)

> Aqui está o mockup do design [paste/drag imagem]
> Implemente este design em React
> Tire um screenshot do resultado
> Compare com o mock e itere até corresponder

# Geralmente 2-3 iterações produz bons resultados
```

### Workflow de capability máxima

```bash
# Inicie Claude em plan mode
claude --permission-mode plan

# Dentro da sessão:
> Leia o módulo de autenticação e ultrathink sobre vulnerabilidades 
> de segurança
> [Revise output de thinking com Ctrl+O]
> think harder sobre a estratégia de migração considerando 
> backward compatibility
> [Shift+Tab para trocar para auto-accept mode para implementação]
> Implemente as correções passo a passo
```

---

## Quick reference cheatsheet

### Instalação rápida
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Comandos mais usados
| Comando | Ação |
|---------|------|
| `claude` | Inicia sessão interativa |
| `claude -c` | Continua última conversa |
| `claude --model opus` | Usa Opus 4.5 |
| `claude --model opusplan` | Híbrido Opus+Sonnet |
| `/clear` | Limpa contexto |
| `/context` | Visualiza uso de tokens |
| `/cost` | Mostra custos da sessão |
| `/model sonnet` | Troca para Sonnet |
| `/init` | Gera CLAUDE.md |
| `/compact` | Comprime conversa |

### Gatilhos de thinking
| Gatilho | Budget |
|---------|--------|
| "think" | ~4K tokens |
| "think hard" | ~10K tokens |
| "**ultrathink**" | ~32K tokens |

### Atalhos essenciais
| Tecla | Ação |
|-------|------|
| `Ctrl+O` | Ver thinking |
| `Tab` | Toggle thinking |
| `Shift+Tab` | Ciclar modos permissão |
| `Escape` | Parar execução |
| `#` | Adicionar à memória |
| `!cmd` | Bash direto |

### Variáveis de ambiente críticas
```bash
MAX_THINKING_TOKENS=32000    # Budget de thinking
ANTHROPIC_MODEL=opus         # Modelo padrão
DISABLE_PROMPT_CACHING=1     # Desabilita cache
```

### Modelo por caso de uso
| Caso | Modelo |
|------|--------|
| Arquitetura complexa | `opus` |
| Desenvolvimento diário | `sonnet` |
| Planejamento + execução | `opusplan` |
| Tarefas rápidas/subagents | `haiku` |

### Workflow padrão
1. `/init` → gerar CLAUDE.md
2. "Explore..." → entender código
3. "Plan..." com `think hard` → estratégia
4. "Implement..." → executar
5. "Commit..." → finalizar

### Níveis de confiança das features
| Feature | Status |
|---------|--------|
| think/think hard/ultrathink | ✅ Oficial |
| MAX_THINKING_TOKENS | ✅ Oficial |
| alwaysThinkingEnabled | ⚠️ Comunidade (funciona) |
| Ctrl+O verbose | ✅ Oficial |
| opusplan | ✅ Oficial |
| Comandos !hidden | ❌ Especulativo |

---

## Considerações finais e gaps identificados

Este guia consolida tanto documentação oficial da Anthropic quanto descobertas da comunidade de desenvolvedores. Algumas áreas apresentam **incertezas**:

**Features confirmadas e estáveis**: Os gatilhos de thinking (think, think hard, ultrathink), controles via MAX_THINKING_TOKENS, modo opusplan, todos os slash commands documentados e a arquitetura de CLAUDE.md são oficialmente suportados.

**Features da comunidade com alta confiança**: A configuração `alwaysThinkingEnabled` em settings.json foi verificada funcionando por múltiplas fontes independentes, embora não apareça na documentação oficial.

**Features especulativas**: Alguns comandos ocultos relatados em fontes únicas (como !memory, !tokens, !daemon) não puderam ser verificados independentemente e devem ser tratados com ceticismo.

A evolução rápida do Claude Code significa que features podem mudar entre versões. Sempre verifique `/status` para confirmar sua versão e consulte a documentação oficial em `code.claude.com/docs` para atualizações mais recentes.

O domínio do Claude Code com Opus 4.5 representa uma mudança de paradigma no desenvolvimento de software—transformando o modelo de "assistente que responde perguntas" para "engenheiro autônomo que executa projetos". Os desenvolvedores que dominarem estes padrões de prompting ganharão uma vantagem competitiva significativa na era do desenvolvimento assistido por IA.