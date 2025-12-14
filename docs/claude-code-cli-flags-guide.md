# Guia Completo das Flags do Claude Code

Documentação técnica detalhada sobre todas as flags disponíveis no Claude Code CLI, com foco em exemplos práticos, casos de uso reais e cenários de aplicação.

## Lista completa de flags por categoria

### Flags de Segurança e Permissões

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--dangerously-skip-permissions` | Ignora todas as verificações de permissão | `claude --dangerously-skip-permissions "corrigir erros no código"` |
| `--allowedTools` | Especifica ferramentas que Claude pode usar sem pedir permissão | `claude --allowedTools "Edit" "Read" "Bash(npm test:*)" "prompt"` |
| `--permission-prompt-tool` | Define ferramenta MCP para lidar com solicitações de permissão | `claude -p --permission-prompt-tool mcp_auth_tool "criar arquivo"` |

### Flags de Formato de Saída

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `-p`, `--print` | Modo não interativo (headless) | `claude -p "explique esta função"` |
| `--output-format` | Define formato de saída (text, json, stream-json) | `claude -p --output-format json "prompt"` |
| `--json` | Atalho para `--output-format json` | `claude -p --json "prompt"` |

### Flags de Debugging e Logging

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--verbose` | Mostra saída detalhada (requer formato json) | `claude -p --verbose --output-format json "prompt"` |
| `--mcp-debug` | Ajuda a identificar problemas com servidores MCP | `claude --mcp-debug "prompt"` |

### Flags de Sessão

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--continue` | Continua automaticamente a conversa mais recente | `claude --continue` |
| `--resume` | Permite selecionar uma conversa para retomar | `claude --resume` |
| `--max-agent-turns` | Limita número de turnos no modo não interativo | `claude -p --max-agent-turns 5 "prompt"` |

### Flags de Ambiente e Configuração

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `-e`, `--env` | Define variáveis de ambiente | `claude -e KEY=value "prompt"` |

## Flags de Segurança e Permissões

### `--dangerously-skip-permissions`

**Descrição**: Ignora todas as verificações de permissão, permitindo que o Claude execute operações sem pedir aprovação.

**Sintaxe**:
```bash
claude --dangerously-skip-permissions "seu prompt aqui"
```

**Cenários de uso**:
- Automação de correção de erros de linting
- Geração de código boilerplate sem interrupções
- Refatoração automatizada de código

**Exemplos práticos**:

```bash
# Corrigir erros de linting
claude --dangerously-skip-permissions "execute o linter e corrija todos os erros encontrados"

# Gerar código boilerplate
claude --dangerously-skip-permissions "crie um novo componente React para formulário de login"

# Refatorar código automaticamente
claude --dangerously-skip-permissions "refatore o módulo de autenticação usando padrões modernos"
```

**Riscos de segurança**:
- Execução de comandos arbitrários sem confirmação
- Possível perda ou corrupção de dados
- Vulnerabilidade a ataques de injeção de prompt

**Recomendação**: Use apenas em ambientes controlados, preferencialmente em contêineres sem acesso à internet.

### `--allowedTools`

**Descrição**: Especifica quais ferramentas o Claude pode usar sem solicitar permissão.

**Sintaxe**:
```bash
claude --allowedTools "Ferramenta1" "Ferramenta2(subcomando:parâmetro)" "prompt"
```

**Ferramentas comuns**:
- `Edit` - permite edição de arquivos
- `Create` - permite criação de arquivos
- `Read` - permite leitura de arquivos
- `Write` - permite escrita em arquivos
- `Bash` - permite execução de comandos bash (pode ser limitada a comandos específicos)

**Exemplos práticos**:

```bash
# Permitir apenas leitura de arquivos
claude --allowedTools "Read" "analise o código no arquivo main.js"

# Permitir leitura e edição de arquivos
claude --allowedTools "Read" "Edit" "refatore o código em src/"

# Permitir comandos git específicos e edição
claude --allowedTools "Bash(git diff:*)" "Bash(git commit:*)" "Edit" "faça commit das mudanças"
```

**Exemplos com curingas**:
```bash
# Permitir qualquer comando npm test
claude --allowedTools "Bash(npm test:*)" "execute todos os testes"

# Permitir comandos git
claude --allowedTools "Bash(git:*)" "crie um branch e faça um commit"
```

## Flags de Formato de Saída

### `--output-format`

**Descrição**: Define o formato da saída quando o Claude Code é executado em modo não interativo.

**Sintaxe**:
```bash
claude -p --output-format <FORMATO> "prompt"
```

**Formatos disponíveis**:
- `text` (padrão) - Retorna apenas o texto da resposta
- `json` - Resposta encapsulada em objeto JSON com metadados
- `stream-json` - Série de objetos JSON enviados à medida que são gerados

**Exemplos práticos**:

```bash
# Formato texto (padrão)
claude -p "explique como funciona a flag print"

# Formato JSON
claude -p --output-format json "analise este código" > resultado.json

# Stream JSON para processamento em tempo real
claude -p --output-format stream-json "crie um script Python" | python processador.py
```

**Estrutura da saída JSON**:
```json
{
  "cost_usd": 0.003,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "result": "Texto da resposta aqui...",
  "session_id": "abc123"
}
```

**Modo verbose com JSON**:
```bash
claude -p --verbose --output-format json "depure este código"
```

**Saída verbose (mais detalhada)**:
```json
[
  {
    "role": "user",
    "content": "Depure este código"
  },
  {
    "role": "assistant",
    "content": "Vou ajudar a depurar esse código..."
  },
  {
    "role": "system",
    "cost_usd": 0.003,
    "duration_ms": 1234,
    "duration_api_ms": 800,
    "result": "Texto da resposta...",
    "session_id": "abc123"
  }
]
```

### `-p` / `--print`

**Descrição**: Habilita o modo não interativo (headless) no Claude Code.

**Sintaxe**:
```bash
claude -p "prompt"
# ou
claude --print "prompt"
```

**Cenários de uso**:
- Automação em scripts
- Integração com pipelines CI/CD
- Uso em hooks de git

**Exemplos práticos**:

```bash
# Uso básico
claude -p "explique esta função JavaScript"

# Com entrada via stdin
cat arquivo.js | claude -p "explique este código"

# Para scripts de automação
echo "O que é 2+2?" | claude -p
```

## Flags de Debugging e Logging

### `--verbose`

**Descrição**: Fornece informações detalhadas durante a execução do Claude Code.

**Sintaxe**:
```bash
claude -p --verbose --output-format json "prompt"
```

**Observação**: Sempre deve ser usado com `--output-format json` ou `--output-format stream-json`.

**Cenários de uso**:
- Depuração de problemas com Claude Code
- Análise de custos e desempenho
- Diagnóstico de erros em scripts automatizados

**Exemplos práticos**:

```bash
# Depurar um problema de código com saída detalhada
claude -p --verbose --output-format json "depure este erro de TypeScript"

# Analisar logs com informações completas
cat logs.txt | claude -p --verbose --output-format json "analise estes erros"

# Resolver problemas de integração com APIs
claude -p --verbose --output-format json "gere exemplo de chamada OAuth2"
```

### `--mcp-debug`

**Descrição**: Ajuda a identificar problemas de configuração ao trabalhar com servidores MCP (Model Context Protocol).

**Sintaxe**:
```bash
claude --mcp-debug "prompt"
```

**Cenários de uso**:
- Diagnóstico de problemas com servidores MCP
- Configuração de ferramentas personalizadas
- Depuração de comunicação entre Claude e ferramentas externas

**Exemplos práticos**:

```bash
# Diagnosticar problema com servidor MCP personalizado
claude --mcp-debug "use a ferramenta para analisar este arquivo"

# Depurar configuração de MCP em projeto compartilhado
cd meu-projeto && claude --mcp-debug "execute os testes unitários"

# Identificar problemas com ferramentas externas
claude --mcp-debug "execute a consulta SQL no banco de dados"
```

## Cenários práticos de uso

### 1. Automação em CI/CD

Integrar o Claude Code em pipelines de CI/CD para analisar código e gerar documentação:

```bash
# Analisar código modificado em PR
FILES=$(git diff --name-only main...HEAD)
echo $FILES | claude -p --output-format json "analise estes arquivos e identifique problemas de segurança" > analise_seguranca.json

# Gerar documentação atualizada
claude -p --allowedTools "Read" "Create" "gere documentação para as APIs modificadas" > docs/api_reference.md

# Hook de pre-commit para revisão de código
cat $(git diff --cached --name-only) | claude -p --output-format json "revise este código e liste problemas" > review.json
```

### 2. Debugging e Correção de Bugs

Usar o Claude Code para identificar e corrigir bugs:

```bash
# Análise detalhada de um erro
cat logs.txt | claude -p "analise este trace de erro e explique a causa raiz"

# Debugging com visualização completa do processo
claude -p --verbose --output-format json "encontre o bug neste código TypeScript" < buggy_code.ts

# Correção automática de erros conhecidos
claude --dangerously-skip-permissions "encontre e corrija todos os problemas de escopo de variáveis no módulo auth"
```

### 3. Gerenciamento de Sessões

Continuar trabalho em sessões anteriores:

```bash
# Continuar última sessão automaticamente
claude --continue

# Selecionar uma sessão específica para continuar
claude --resume

# Continuar sessão em modo não interativo
claude --continue --print "continue refatorando o código"
```

### 4. Integração com Scripts

Usar o Claude Code em scripts para automação:

```bash
#!/bin/bash
# Exemplo de script usando Claude Code

# Extrair todos os TODOs do código
TODOS=$(find . -name "*.js" -o -name "*.ts" | xargs cat | grep -i "TODO")

# Enviar para o Claude Code analisar
echo "$TODOS" | claude -p --output-format json "organize estes TODOs por prioridade" > todos_priorizados.json

# Processar resultado com jq
cat todos_priorizados.json | jq -r '.result' > todo_report.md
```

## Combinações comuns de flags

### Para Automação e Scripts

```bash
# Saída JSON para processamento programático
claude -p --output-format json "prompt"

# Opção mais curta para saída JSON
claude -p --json "prompt"

# JSON com streaming para respostas longas
claude -p --output-format stream-json "prompt"

# Modo headless com permissões pré-aprovadas
claude -p --allowedTools "Read" "Edit" "prompt"
```

### Para Debugging

```bash
# Saída verbose em formato JSON
claude -p --verbose --output-format json "prompt"

# Debugging de servidores MCP
claude --mcp-debug "prompt"

# Debugging com limite de turnos
claude -p --verbose --output-format json --max-agent-turns 5 "prompt"
```

### Para Operações sem supervisão

```bash
# Pular todas as permissões (em ambiente seguro)
claude --dangerously-skip-permissions "prompt"

# Definir ferramentas específicas permitidas
claude --allowedTools "Bash(npm test:*)" "Edit" "prompt"

# Combinar com formato de saída estruturado
claude --dangerously-skip-permissions -p --output-format json "prompt"
```

### Para Continuação de Sessões

```bash
# Continuar última sessão com novo prompt
claude --continue "continue com este novo prompt"

# Continuar em modo não interativo
claude --continue --print "continue e resuma o progresso"

# Retomar sessão específica
claude --resume abc123 "continue a partir daqui"
```

## Foco especial em flags específicas

### `--dangerously-skip-permissions`

Esta flag permite que o Claude Code opere sem solicitar permissões, o que é útil para automação, mas deve ser usado com extrema cautela.

**Casos de uso ideais:**
- Ambientes isolados como contêineres Docker
- Tarefas repetitivas bem definidas (correções de linting, geração de boilerplate)
- Pipelines de CI/CD em ambientes controlados

**Práticas recomendadas de segurança:**
- Use apenas em ambientes isolados sem acesso à internet
- Limite o escopo das operações
- Mantenha backups ou use controle de versão
- Revise todas as alterações antes de usar em produção

**Exemplo em contêiner de desenvolvimento:**
```bash
# Usando no contêiner de dev da Anthropic 
docker run --rm -v $(pwd):/code anthropic/claude-code-devcontainer \
  claude --dangerously-skip-permissions "atualizar dependências e corrigir problemas de tipo"
```

### `--allowedTools`

Especifica quais ferramentas o Claude pode usar sem pedir permissão, oferecendo controle granular.

**Exemplos detalhados:**

```bash
# Permitir apenas leitura de arquivos
claude --allowedTools "Read" "analise o código"

# Permitir leitura e edição de arquivos específicos
claude --allowedTools "Read" "Edit" "melhore o código de auth.js"

# Permitir comandos npm test
claude --allowedTools "Bash(npm test:*)" "execute e corrija os testes"

# Permitir comandos git específicos
claude --allowedTools "Bash(git status:*)" "Bash(git diff:*)" "analise as mudanças pendentes"

# Permitir acesso a ferramentas MCP
claude --allowedTools "mcp__puppeteer__puppeteer_navigate" "teste esta página web"
```

**Regras de permissão avançadas:**

- **Comandos exatos:** `Bash(npm run build)`
- **Prefixos com curinga:** `Bash(npm run test:*)`
- **Domínios específicos:** `WebFetchTool(domain:example.com)`
- **Ferramentas MCP:** `mcp__server_name__tool_name`

**Considerações de segurança:**
- Seja específico nas permissões - evite padrões muito amplos
- Considere separadores de comando (como `&&`) ao definir curingas
- Teste as permissões em ambiente seguro

### `--output-format`

Define o formato da saída para facilitar a automação e integração com outras ferramentas.

**Opções detalhadas:**

1. **text** (padrão):
   ```bash
   claude -p "explique esta função"
   # Saída: Texto simples da resposta
   ```

2. **json**:
   ```bash
   claude -p --output-format json "explique esta função"
   # Saída: {"cost_usd": 0.003, "duration_ms": 1234, "result": "...", "session_id": "abc123"}
   ```

3. **stream-json**:
   ```bash
   claude -p --output-format stream-json "crie um script Python"
   # Saída: Série de objetos JSON enviados incrementalmente
   ```

**Scripts de processamento:**

```python
# Exemplo de script para processar saída stream-json
import json
import sys

for line in sys.stdin:
    try:
        chunk = json.loads(line)
        print(f"Processando chunk: {len(chunk.get('result', ''))}")
        # Processar cada fragmento aqui
    except json.JSONDecodeError:
        pass
```

**Casos de uso:**
- Pipelines de CI/CD
- Scripts de automação
- Análise de dados em tempo real
- Integração com outras ferramentas

### Flags de debugging e logging

Ferramentas essenciais para resolver problemas e entender o comportamento do Claude Code.

**`--verbose`:**
- Mostra conversa completa e metadados
- Requer `--output-format json` ou `--output-format stream-json`
- Fornece informações de custo, duração e ID de sessão
- Útil para diagnóstico de problemas e análise de desempenho

```bash
claude -p --verbose --output-format json "depure este código" > debug_log.json
```

**`--mcp-debug`:**
- Mostra detalhes sobre a comunicação com servidores MCP
- Ajuda a identificar problemas de configuração
- Exibe mensagens de erro detalhadas
- Fundamental para depurar integrações com ferramentas externas

```bash
claude --mcp-debug "use a ferramenta customizada para analisar este arquivo"
```

**Exemplo de diagnóstico de problema:**
```bash
# Identificar por que uma ferramenta MCP específica está falhando
claude --mcp-debug "use a ferramenta XYZ para processar este arquivo" 2> mcp_debug.log

# Analisar o log
cat mcp_debug.log | grep ERROR
```

## Tipos de Arquivo

O Claude Code não possui flags específicas para diferentes tipos de arquivo. Em vez disso, ele detecta e processa diferentes tipos de arquivo automaticamente com base no conteúdo e na extensão. Ele suporta:

- Linguagens de programação: JavaScript, Python, Java, C/C++, Go, Rust, PHP, Ruby, etc.
- Arquivos de marcação: HTML, XML, Markdown, etc.
- Arquivos de estilo: CSS, SCSS, LESS, etc.
- Arquivos de configuração: JSON, YAML, TOML, etc.
- Arquivos de documentação: Markdown, reStructuredText, etc.

**Como trabalhar com diferentes tipos de arquivo:**

```bash
# Analisar arquivo JavaScript
claude "explique o que o arquivo app.js faz"

# Documentar arquivo Python
claude "adicione docstrings ao arquivo utils.py"

# Refatorar arquivo CSS
claude "refatore o arquivo styles.css para melhorar a legibilidade"
```

**Limitações:**
- Arquivos binários e formatos proprietários podem não ser totalmente compreendidos
- Arquivos muito grandes podem exceder o limite de contexto
- Formatos muito específicos podem ter suporte limitado

## Variáveis de Ambiente e Configuração

O Claude Code suporta várias variáveis de ambiente para controlar seu comportamento:

| Variável | Propósito |
|----------|-----------|
| `DISABLE_AUTOUPDATER` | Desativa atualizador automático (valor: 1) |
| `DISABLE_BUG_COMMAND` | Desativa comando /bug (valor: 1) |
| `DISABLE_COST_WARNINGS` | Desativa avisos de custo (valor: 1) |
| `HTTP_PROXY`, `HTTPS_PROXY` | Especifica servidores proxy |
| `MCP_TIMEOUT` | Timeout em ms para inicialização do servidor MCP |
| `MCP_TOOL_TIMEOUT` | Timeout em ms para execução de ferramentas MCP |

**Configuração de projeto vs. global:**

```bash
# Configuração global
claude config set -g <chave> <valor>

# Configuração de projeto
claude config set <chave> <valor>

# Adicionar a listas (como allowedTools)
claude config add <chave> <valor>

# Remover de listas
claude config remove <chave> <valor>
```

**Exemplos:**

```bash
# Desativar atualizador automático
claude config set -g autoUpdaterStatus disabled

# Definir tema escuro
claude config set -g theme dark

# Adicionar ferramenta permitida
claude config add allowedTools "Bash(npm test:*)"
```

## Exemplos Concretos para Cenários Comuns

### 1. Revisão de Código Automatizada

```bash
#!/bin/bash
# Cria revisão de código automatizada para um PR

# Obter arquivos modificados
FILES=$(git diff --name-only origin/main...HEAD)

# Enviar para Claude para revisão
echo $FILES | claude -p --output-format json "revise estes arquivos e encontre problemas de segurança, desempenho e manutenção. Formate a saída como uma lista em Markdown com seções por categoria de problema." > code_review.json

# Extrair resultado e criar comentário no PR
cat code_review.json | jq -r '.result' > review.md
gh pr comment --body-file review.md
```

### 2. Debugging de Produção

```bash
#!/bin/bash
# Script para analisar logs de erro de produção

# Extrair últimos 100 logs de erro
LOGS=$(tail -n 100 /var/log/app/errors.log)

# Analisar com Claude Code
echo "$LOGS" | claude -p --verbose --output-format json "analise estes logs de erro, identifique padrões, sugira possíveis causas raiz e recomende próximos passos para investigação. Formate como um relatório de incidente." > analise_erro.json

# Salvar resultado e metadados separadamente
cat analise_erro.json | jq -r '.[2].result' > relatorio_erro.md
cat analise_erro.json | jq '.[2].cost_usd' > custo.txt
```

### 3. Integração em Scripts de Build

```bash
#!/bin/bash
# Gerar documentação atualizada como parte do build

# Gerar arquivos de documentação
claude -p --allowedTools "Read" "Create" "Write" --output-format json "gere documentação atualizada para todas as APIs neste projeto. Crie um arquivo README.md principal e arquivos separados para cada módulo principal. Use formato Markdown." > doc_generation.json

# Verificar sucesso
if grep -q "Documentação gerada com sucesso" doc_generation.json; then
  echo "Documentação atualizada com sucesso"
else
  echo "Falha ao gerar documentação"
  exit 1
fi
```

### 4. Processamento de Dados com Stream JSON

```bash
#!/bin/bash
# Processar dados grandes em tempo real

# Streaming para processamento incremental
cat large_dataset.csv | claude -p --output-format stream-json "analise este dataset CSV e identifique anomalias. Para cada linha, verifique se os valores estão dentro dos limites esperados e destaque as exceções." | python process_stream.py

# Onde process_stream.py seria:
import json
import sys

anomalies = []
for line in sys.stdin:
    try:
        chunk = json.loads(line)
        if 'anomalia' in chunk.get('result', '').lower():
            anomalies.append(chunk.get('result', ''))
            print(f"Anomalia detectada: {chunk.get('result', '')}")
    except json.JSONDecodeError:
        pass

print(f"Total de anomalias encontradas: {len(anomalies)}")
```

## Considerações Finais

O Claude Code oferece uma variedade de flags que permitem personalizar seu comportamento para diferentes cenários. Para um uso eficiente:

1. **Segurança em primeiro lugar**: Use `--dangerously-skip-permissions` apenas em ambientes controlados.

2. **Automação eficiente**: Combine `-p` com `--output-format json` para scripts e integração com pipelines.

3. **Debugging aprimorado**: Use `--verbose` e `--mcp-debug` para resolver problemas complexos.

4. **Permissões granulares**: Defina permissões específicas com `--allowedTools` em vez de ignorar todas as verificações.

5. **Monitoramento de custos**: Use `/cost` interativamente ou analise os metadados em saídas JSON para rastrear custos.

Para obter ajuda sobre qualquer flag, execute:
```bash
claude -h
```

Esta documentação fornece um ponto de partida para o uso eficaz das flags do Claude Code. Experimente diferentes combinações conforme necessário para seus casos de uso específicos.