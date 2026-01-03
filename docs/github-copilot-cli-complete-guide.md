# Microsoft Copilot CLI: Guia Técnico Completo e Definitivo

O GitHub Copilot CLI representa a evolução definitiva da assistência por IA no terminal, substituindo a extensão legada `gh copilot` por uma ferramenta agêntica totalmente autônoma. Esta versão transforma fundamentalmente o fluxo de trabalho no terminal: em vez de apenas sugerir comandos, o novo CLI pode executar operações complexas, criar pull requests, modificar arquivos e integrar-se diretamente com o ecossistema GitHub — tudo através de linguagem natural. Com suporte aos modelos **Claude Sonnet 4.5** (padrão) e **GPT-5**, oferece capacidades de raciocínio avançadas que transcendem simples autocompletar. A ferramenta está disponível para assinantes Pro ($10/mês), Pro+ ($39/mês), Business e Enterprise, consumindo requisições premium do seu plano mensal.

---

## Sumário Executivo

O GitHub Copilot CLI emergiu como a principal ferramenta de IA para desenvolvedores no terminal em 2025. Três pontos críticos definem seu estado atual:

1. **Transição arquitetural**: A extensão legada `gh copilot` foi **descontinuada em outubro de 2025**, substituída pelo novo comando `copilot` standalone
2. **Modelo agêntico**: O novo CLI opera como um agente autônomo capaz de executar tarefas completas, não apenas sugerir comandos
3. **Consumo de requisições premium**: Cada interação consome requisições do limite mensal — **300** no plano Pro, **1.500** no Pro+

Para desenvolvedores que migram da versão legada, a mudança principal é passar de `gh copilot suggest/explain` para simplesmente `copilot` seguido de linguagem natural.

---

## 1. Introdução e Visão Geral

### 1.1 O que é o Copilot CLI

O GitHub Copilot CLI é um **assistente de IA nativo para terminal** que permite interagir com seu ambiente de desenvolvimento através de linguagem natural. Diferente de ferramentas tradicionais que apenas sugerem comandos, o Copilot CLI:

- **Executa operações diretamente** após aprovação do usuário
- **Modifica arquivos** de código e configuração
- **Interage com GitHub** (issues, PRs, repositórios) nativamente
- **Raciocina sobre contexto** do projeto atual
- **Delega tarefas** para o Copilot coding agent na nuvem

**Nomenclatura oficial atualizada:**

| Versão | Comando | Status | Período |
|--------|---------|--------|---------|
| GitHub Copilot in the CLI | `gh copilot` | **DESCONTINUADO** | 2023-2025 |
| GitHub Copilot CLI | `copilot` | **ATIVO** | 2025+ |

### 1.2 Arquitetura e tecnologia

A arquitetura do Copilot CLI baseia-se em três pilares:

**Harness agêntico compartilhado**: O CLI utiliza o mesmo framework do Copilot coding agent do GitHub.com, permitindo raciocínio multi-step e execução autônoma de tarefas complexas.

**Model Context Protocol (MCP)**: Protocolo extensível que permite integrar servidores personalizados. O CLI vem pré-configurado com o **GitHub MCP Server**, habilitando acesso nativo a repositórios, issues e pull requests.

**Modelos de IA disponíveis:**

| Modelo | Multiplicador | Uso Recomendado |
|--------|--------------|-----------------|
| Claude Sonnet 4.5 | 1x (padrão) | Tarefas gerais de desenvolvimento |
| Claude Sonnet 4 | 1x | Alternativa equilibrada |
| Claude Opus 4 | 10x | Raciocínio complexo |
| GPT-5 | 1x | Alternativa OpenAI |
| GPT-5 mini | 1x | Tarefas simples |
| Gemini 2.5 Pro | 1x | Integração Google |

### 1.3 Comparação com alternativas

O mercado de CLIs assistidos por IA expandiu significativamente. Análise comparativa:

| Aspecto | GitHub Copilot CLI | Amazon Q CLI | Warp AI Terminal |
|---------|-------------------|--------------|------------------|
| **Foco** | Desenvolvimento geral + GitHub | Ecossistema AWS | Terminal completo |
| **Modelo padrão** | Claude Sonnet 4.5 | Bedrock (dinâmico) | Proprietário |
| **Preço** | $10-39/mês individual | $3-19/usuário/mês | Freemium |
| **Integração Git** | Nativa (GitHub) | Manual | Integrada |
| **MCP Support** | Sim | Não | Sim |
| **Tipo** | CLI standalone | CLI standalone | Terminal substituto |

**Dados de mercado** (estudo Faros AI): Copilot apresenta taxa de adoção **2x maior**, taxa de aceitação de sugestões **2x melhor**, e economia de **10h/semana** versus 7h/semana do Amazon Q.

### 1.4 Requisitos de sistema

**Requisitos mínimos:**

| Componente | Requisito |
|------------|-----------|
| Node.js | v22 ou superior |
| npm | v10 ou superior |
| PowerShell (Windows) | v6 ou superior |
| Assinatura | Pro, Pro+, Business ou Enterprise |

**Plataformas suportadas:**

| Sistema | Suporte | Observações |
|---------|---------|-------------|
| Linux (64-bit) | ✅ Completo | Todas as distribuições principais |
| macOS | ✅ Completo | Intel e Apple Silicon |
| Windows (WSL) | ✅ Completo | Recomendado para Windows |
| Windows (PowerShell) | ⚠️ Experimental | Funcionalidades limitadas |
| Android 32-bit | ❌ Não suportado | Use ARM64 |

---

## 2. Instalação Completa

### 2.1 Windows (múltiplos métodos)

**Método 1: WinGet (recomendado para Windows nativo)**
```powershell
winget install GitHub.Copilot
```

**Método 2: npm (universal)**
```powershell
# Verificar versão do Node.js (requer v22+)
node --version

# Instalar globalmente
npm install -g @github/copilot
```

**Método 3: WSL (recomendado para funcionalidades completas)**
```bash
# No terminal WSL (Ubuntu/Debian)
curl -fsSL https://gh.io/copilot-install | bash
```

**Pós-instalação no Windows:**
```powershell
# Verificar instalação
copilot --version

# Iniciar e autenticar
copilot
# Siga o comando /login quando solicitado
```

### 2.2 macOS (múltiplos métodos)

**Método 1: Homebrew (recomendado)**
```bash
brew install github-copilot
```

**Método 2: Script de instalação**
```bash
curl -fsSL https://gh.io/copilot-install | bash
```

**Método 3: npm**
```bash
# Verificar Node.js
node --version  # Deve ser v22+

# Instalar
npm install -g @github/copilot
```

**Instalação em diretório customizado:**
```bash
curl -fsSL https://gh.io/copilot-install | PREFIX="$HOME/.local" bash
```

### 2.3 Linux (todas as distribuições principais)

**Ubuntu/Debian:**
```bash
# Opção 1: Script oficial
curl -fsSL https://gh.io/copilot-install | bash

# Opção 2: npm (após instalar Node.js 22)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install -g @github/copilot
```

**Fedora/RHEL/CentOS:**
```bash
# Instalar Node.js 22
sudo dnf module install nodejs:22

# Instalar Copilot CLI
npm install -g @github/copilot
```

**Arch Linux:**
```bash
# Via AUR ou npm após instalar nodejs
sudo pacman -S nodejs npm
npm install -g @github/copilot
```

**openSUSE:**
```bash
sudo zypper install nodejs22
npm install -g @github/copilot
```

**Instalação como root (para /usr/local/bin):**
```bash
curl -fsSL https://gh.io/copilot-install | sudo bash
```

**Instalação de versão específica:**
```bash
curl -fsSL https://gh.io/copilot-install | VERSION="v0.0.369" bash
```

### 2.4 Verificação da instalação

```bash
# Verificar versão instalada
copilot --version

# Exibir ajuda completa
copilot --help

# Verificar configuração de ajuda
copilot help config

# Testar conectividade (iniciar sessão interativa)
copilot
```

**Saída esperada:**
```
GitHub Copilot CLI v0.0.367
Usage: copilot [options]
```

### 2.5 Resolução de problemas de instalação

**Erro: "Node.js version too old"**
```bash
# Atualizar via nvm
nvm install 22
nvm use 22

# Ou via Homebrew (macOS)
brew upgrade node
```

**Erro: "EACCES permission denied"**
```bash
# Corrigir permissões npm
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Reinstalar
npm install -g @github/copilot
```

**Erro: "ETIMEDOUT" ou "ECONNRESET"**
```bash
# Verificar conectividade
curl -v https://registry.npmjs.org

# Configurar proxy se necessário
npm config set proxy http://proxy.empresa.com:8080
npm config set https-proxy http://proxy.empresa.com:8080
```

**Erro de SSL/certificado:**
```bash
# Definir certificados corporativos
export NODE_EXTRA_CA_CERTS="/caminho/para/certificado-corporativo.crt"
```

---

## 3. Configuração e Autenticação

### 3.1 Autenticação inicial

**Método 1: OAuth via navegador (recomendado)**
```bash
# Iniciar Copilot CLI
copilot

# Na sessão interativa, usar comando de login
/login
```

O navegador abrirá automaticamente para autenticação OAuth com sua conta GitHub.

**Método 2: Personal Access Token (PAT)**
```bash
# Criar PAT em: https://github.com/settings/personal-access-tokens/new
# Habilitar permissão: "Copilot Requests"

# Configurar variável de ambiente
export GH_TOKEN="ghp_seu_token_aqui"

# Alternativa
export GITHUB_TOKEN="ghp_seu_token_aqui"
```

**Verificar status de autenticação:**
```bash
# Na sessão interativa
/usage
```

### 3.2 Variáveis de ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `GH_TOKEN` | Token de autenticação (prioridade) | `ghp_xxx` |
| `GITHUB_TOKEN` | Token alternativo | `ghp_xxx` |
| `XDG_CONFIG_HOME` | Diretório de configuração | `~/.config` |
| `COPILOT_MODEL` | Modelo de IA padrão | `gpt-5` |
| `HTTPS_PROXY` | Proxy HTTPS | `http://proxy:8080` |
| `HTTP_PROXY` | Proxy HTTP | `http://proxy:8080` |
| `NO_PROXY` | Exceções de proxy | `localhost,127.0.0.1` |
| `NODE_EXTRA_CA_CERTS` | Certificados CA customizados | `/path/to/ca.crt` |

**Configuração persistente (Bash/Zsh):**
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export COPILOT_MODEL="claude-sonnet-4.5"
export GH_TOKEN="seu_token"
```

### 3.3 Arquivos de configuração

**Localização dos arquivos:**

| Plataforma | Diretório |
|------------|-----------|
| Linux/macOS | `~/.copilot/` |
| Windows | `%USERPROFILE%\.copilot\` |

**Arquivos principais:**

```
~/.copilot/
├── config.json          # Configurações gerais
├── mcp-config.json      # Servidores MCP
└── copilot-instructions.md  # Instruções personalizadas
```

**Exemplo de config.json:**
```json
{
  "trusted_folders": [
    "/home/usuario/projetos",
    "/home/usuario/workspace"
  ],
  "analytics_opt_in": false,
  "confirm_command_execution": true
}
```

**Exemplo de mcp-config.json:**
```json
{
  "mcpServers": {
    "github": {
      "type": "builtin",
      "enabled": true
    },
    "microsoft-learn": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@anthropic/microsoft-learn-mcp-server"]
    }
  }
}
```

### 3.4 Integração com shells

**Bash:**
```bash
# Adicionar ao ~/.bashrc
alias cop='copilot'
alias copp='copilot -p'

# Função para execução rápida
copilot_exec() {
    copilot -p "$*" --allow-all-tools
}
alias cex='copilot_exec'
```

**Zsh:**
```zsh
# Adicionar ao ~/.zshrc
alias cop='copilot'
alias copp='copilot -p'

# Autocompletar (se disponível)
# compdef _copilot copilot
```

**Fish:**
```fish
# Adicionar ao ~/.config/fish/config.fish
alias cop='copilot'
alias copp='copilot -p'
```

**PowerShell:**
```powershell
# Adicionar ao $PROFILE
Set-Alias -Name cop -Value copilot
function copp { copilot -p $args }
```

**Aliases para versão legada (se ainda em uso):**
```bash
# Bash/Zsh - versão gh copilot
echo 'eval "$(gh copilot alias -- bash)"' >> ~/.bashrc
source ~/.bashrc

# Cria aliases: ghcs (suggest) e ghce (explain)
```

### 3.5 Configuração para ambientes corporativos

**Proxy com autenticação:**
```bash
export HTTPS_PROXY="http://usuario:senha@proxy.empresa.com:8080"
export HTTP_PROXY="http://usuario:senha@proxy.empresa.com:8080"
export NO_PROXY="localhost,127.0.0.1,.empresa.com"
```

**URLs para allowlist de firewall:**
```
github.com
api.github.com
*.github.com
copilot-proxy.githubusercontent.com
api.githubcopilot.com
*.githubcopilot.com
default.exp-tas.com
```

**Certificados SSL corporativos:**
```bash
# Exportar certificado da CA corporativa
export NODE_EXTRA_CA_CERTS="/etc/ssl/certs/empresa-ca-bundle.crt"

# Para VS Code (se aplicável)
# settings.json
{
  "http.proxy": "http://proxy.empresa.com:8080",
  "http.proxyStrictSSL": true
}
```

**Configuração para GitHub Enterprise Server:**
```bash
# Definir hostname customizado
export GH_HOST="github.empresa.com"
```

---

## 4. Comandos e Funcionalidades Core

### 4.1 Referência completa de comandos

**Sintaxe principal:**
```bash
copilot [opções]
```

**Opções de linha de comando:**

| Opção | Forma Curta | Descrição |
|-------|-------------|-----------|
| `--prompt` | `-p` | Executar prompt único (modo programático) |
| `--allow-all-tools` | | Permitir todas as ferramentas sem aprovação |
| `--allow-tool` | | Permitir ferramenta específica |
| `--deny-tool` | | Bloquear ferramenta específica |
| `--agent` | | Especificar agente customizado |
| `--banner` | | Exibir banner animado |
| `--resume` | | Retomar sessão anterior |
| `--continue` | | Continuar sessão mais recente |
| `--version` | `-v` | Exibir versão |
| `--help` | `-h` | Exibir ajuda |

**Comandos slash (modo interativo):**

| Comando | Função |
|---------|--------|
| `/login` | Autenticar com GitHub |
| `/model` | Trocar modelo de IA |
| `/agent` | Selecionar agente customizado |
| `/mcp` | Gerenciar servidores MCP |
| `/mcp add` | Adicionar servidor MCP |
| `/mcp show` | Exibir servidores configurados |
| `/add-dir` | Adicionar diretório confiável |
| `/cwd` | Mudar diretório de trabalho |
| `/delegate` | Delegar tarefa para coding agent |
| `/feedback` | Enviar feedback |
| `/usage` | Ver estatísticas de uso |
| `?` | Exibir ajuda |

**Execução direta de shell:**
```bash
# Prefixar com ! executa comando diretamente
!git status
!ls -la
!npm install
```

### 4.2 Consultas em linguagem natural

O Copilot CLI aceita prompts em linguagem natural diretamente:

**Modo interativo:**
```bash
copilot
# Digite diretamente:
> Encontre todos os arquivos JavaScript maiores que 1MB
> Mostre os commits da última semana e faça um resumo
> Crie uma função Python que valide CPF
```

**Modo programático:**
```bash
copilot -p "Liste todos os processos usando mais de 100MB de memória"
copilot -p "Converta todos os arquivos PNG para JPG nesta pasta" --allow-tool 'shell(convert)'
```

**Padrões eficazes de prompt:**

| Padrão | Exemplo |
|--------|---------|
| Específico | "Encontre arquivos .log maiores que 500MB modificados nos últimos 7 dias" |
| Com contexto | "Neste projeto React, crie um componente de formulário de login" |
| Com formato | "Gere um script bash com comentários explicando cada etapa" |
| Com referência | "Corrija o bug em @src/utils/validator.js" |

### 4.3 Explicação de comandos

Para entender comandos complexos, use linguagem natural:

**Exemplos:**
```bash
# Modo interativo
> Explique este comando: find . -name "*.log" -mtime +30 -delete

# Modo programático
copilot -p "Explique: git rebase --interactive HEAD~5"

# Com contexto
copilot -p "O que faz: awk '{sum+=$1} END {print sum}' arquivo.txt"
```

**Saída típica:**
```
Este comando faz o seguinte:
• find . - busca a partir do diretório atual
• -name "*.log" - arquivos com extensão .log
• -mtime +30 - modificados há mais de 30 dias
• -delete - remove os arquivos encontrados

⚠️ Cuidado: Este comando deleta arquivos permanentemente!
```

**Versão legada (se ainda em uso):**
```bash
gh copilot explain 'du -sh * | sort -h'
gh copilot explain 'git log --oneline --graph --decorate --all'
```

### 4.4 Sugestão de comandos

**Consultas diretas:**
```bash
# Modo interativo
copilot
> Como faço para encontrar arquivos duplicados nesta pasta?
> Qual comando mostra uso de disco por diretório?
> Como mato processos com arquivos deletados abertos?

# Modo programático
copilot -p "Comando para monitorar uso de CPU em tempo real"
```

**Exemplos práticos por categoria:**

**Sistema:**
```bash
> Encontrar os 10 maiores arquivos no sistema
> Listar portas TCP em uso
> Verificar espaço em disco de todos os volumes
> Monitorar processos ordenados por memória
```

**Rede:**
```bash
> Verificar se a porta 8080 está acessível em servidor.com
> Listar todas as conexões de rede estabelecidas
> Fazer download de arquivo mostrando progresso
> Verificar DNS de um domínio
```

**Texto e arquivos:**
```bash
> Encontrar todos os arquivos contendo "TODO" recursivamente
> Substituir "antigo" por "novo" em todos os arquivos .txt
> Contar linhas de código em arquivos Python
> Extrair emails de um arquivo de log
```

**Versão legada:**
```bash
gh copilot suggest "instalar docker" -t shell
gh copilot suggest "desfazer último commit" -t git
gh copilot suggest "listar pull requests abertos" -t gh
```

### 4.5 Geração de scripts

O Copilot CLI gera scripts completos com documentação:

**Exemplos:**
```bash
# Script de backup
copilot -p "Crie um script bash que faça backup incremental de /home para /backup com compressão"

# Script de deploy
copilot -p "Gere um script de deploy que: 1) faça pull do git, 2) instale dependências npm, 3) rode testes, 4) reinicie PM2"

# Automação
copilot -p "Script Python que monitora pasta e converte novos vídeos MP4 para WebM"
```

**Workflow interativo para scripts:**
```bash
copilot
> Preciso de um script que:
> - Monitore uma pasta para novos arquivos CSV
> - Processe cada arquivo convertendo datas para formato ISO
> - Mova arquivos processados para pasta "concluidos"
> - Envie notificação por email em caso de erro
```

O Copilot gerará o script completo, explicará cada seção e perguntará se deseja criar o arquivo.

---

## 5. Funcionalidades Avançadas

### 5.1 Integração com Git

O Copilot CLI oferece integração nativa profunda com Git:

**Operações de commit:**
```bash
> Stage as mudanças, escreva um commit referenciando #1234, e abra um PR draft
> Commit com mensagem seguindo Conventional Commits
> Amend o último commit mudando apenas a mensagem
```

**Operações de branch:**
```bash
> Criar branch feature/auth-improvements e mudar para ela
> Deletar branches locais já mergeadas
> Sincronizar branch atual com main resolvendo conflitos
```

**Histórico e análise:**
```bash
> Mostrar commits do usuário 'joao' no último mês com mensagem contendo 'fix'
> Listar arquivos modificados entre duas tags
> Encontrar commit que introduziu bug no arquivo utils.py
```

**Operações de merge e rebase:**
```bash
> Fazer rebase interativo dos últimos 5 commits
> Fazer squash dos commits de feature para um único
> Cherry-pick commits específicos para branch atual
```

**Modo programático para automação:**
```bash
copilot -p "Reverter o último commit mantendo mudanças unstaged" --allow-tool 'shell(git)'
copilot -p "Mostrar diff entre HEAD e HEAD~3" --allow-tool 'shell(git)'
```

### 5.2 Assistência para cloud CLIs

**Azure CLI:**
```bash
> Criar resource group 'meu-rg' na região brazilsouth
> Listar todas as VMs no subscription atual
> Criar Azure Function com runtime Node.js 20
> Configurar Application Insights para minha aplicação
```

**AWS CLI:**
```bash
> Listar todos os buckets S3 com tamanho total
> Criar instância EC2 t3.micro com Amazon Linux 2
> Configurar CloudWatch alarm para CPU > 80%
> Descrever todas as funções Lambda na região
```

**GCP gcloud:**
```bash
> Listar projetos GCP disponíveis
> Criar cluster GKE com 3 nodes
> Deploy de Cloud Function a partir do código local
```

**Integração via MCP (Model Context Protocol):**

```json
// ~/.copilot/mcp-config.json
{
  "mcpServers": {
    "azure": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@azure/mcp-server"]
    },
    "microsoft-learn": {
      "type": "local", 
      "command": "npx",
      "args": ["-y", "@anthropic/microsoft-learn-mcp-server"]
    }
  }
}
```

### 5.3 Docker e containers

**Operações básicas:**
```bash
> Rodar container nginx mapeando porta 8080 para 80 com volume da pasta atual
> Listar containers rodando com uso de recursos
> Parar e remover todos os containers parados
> Fazer pull da imagem mais recente do postgres
```

**Dockerfile generation:**
```bash
> Criar Dockerfile multi-stage para aplicação Node.js
> Criar Dockerfile otimizado para Python com poetry
> Gerar docker-compose.yml para stack LAMP
```

**Exemplos de comandos gerados:**
```bash
# Container nginx com volume
docker run -d --name my-nginx \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:latest

# Limpeza de recursos
docker system prune -af --volumes
```

**Debugging de containers:**
```bash
> Mostrar logs dos últimos 100 registros do container api
> Executar shell bash dentro do container web
> Inspecionar variáveis de ambiente do container
> Verificar health check status de todos containers
```

### 5.4 Pipelines e automação

**GitHub Actions:**
```bash
> Criar workflow que roda testes em PRs e deploy automático em push para main
> Gerar Action que faz lint do código Python com flake8 e mypy
> Workflow para build e push de imagem Docker para GHCR
```

**Exemplo de workflow gerado:**
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh
```

**CI/CD queries:**
```bash
> Listar workflows com falha na última semana
> Mostrar jobs mais lentos do workflow de CI
> Reexecutar job falhado do último workflow
```

**Modo programático para pipelines:**
```bash
# Em script de CI
copilot -p "Analisar código em busca de vulnerabilidades de segurança" \
  --allow-tool 'shell(npm audit)' \
  --deny-tool 'shell(rm)'
```

### 5.5 Sistema de aprovação de ferramentas

O Copilot CLI implementa um modelo de segurança baseado em aprovação:

**Permitir todas as ferramentas:**
```bash
copilot --allow-all-tools
```

**Permitir ferramentas específicas:**
```bash
# Permitir qualquer comando shell
copilot --allow-tool 'shell'

# Permitir comando específico
copilot --allow-tool 'shell(git)'
copilot --allow-tool 'shell(npm)'
copilot --allow-tool 'shell(docker)'

# Permitir escrita de arquivos
copilot --allow-tool 'write'

# Permitir servidor MCP específico
copilot --allow-tool 'My-MCP-Server'
copilot --allow-tool 'My-MCP-Server(tool_name)'
```

**Bloquear ferramentas:**
```bash
# Prevenir comandos perigosos
copilot --allow-all-tools --deny-tool 'shell(rm)'
copilot --allow-all-tools --deny-tool 'shell(rm -rf)'
copilot --deny-tool 'shell(git push --force)'
```

**Combinação de permissões:**
```bash
# Permitir tudo exceto rm e push forçado
copilot --allow-all-tools \
  --deny-tool 'shell(rm)' \
  --deny-tool 'shell(git push --force)' \
  --deny-tool 'shell(sudo)'
```

### 5.6 Servidores MCP e extensibilidade

**Adicionar servidor MCP:**
```bash
# Modo interativo
/mcp add

# Visualizar servidores configurados
/mcp show
```

**Configuração manual (~/.copilot/mcp-config.json):**
```json
{
  "mcpServers": {
    "github": {
      "type": "builtin",
      "enabled": true
    },
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/usuario"]
    },
    "postgres": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

**Servidores MCP populares:**

| Servidor | Função |
|----------|--------|
| `github` | Acesso a repos, issues, PRs (built-in) |
| `filesystem` | Operações de arquivo expandidas |
| `postgres` | Queries e gerenciamento de DB |
| `sqlite` | Database SQLite local |
| `brave-search` | Busca na web |
| `microsoft-learn` | Documentação Microsoft |

### 5.7 Delegação para Coding Agent

O comando `/delegate` envia tarefas para o Copilot coding agent na nuvem:

```bash
# Modo interativo
/delegate implementar testes de integração para o módulo de autenticação
/delegate refatorar o AuthService para usar injeção de dependência
/delegate criar documentação API usando OpenAPI 3.0
```

**Quando usar delegação:**
- Tarefas que requerem múltiplas modificações de arquivo
- Refatorações complexas em todo o projeto
- Criação de PRs completos com commits
- Tarefas que se beneficiam de execução em ambiente isolado

---

## 6. Dicas da Comunidade e Melhores Práticas

### 6.1 Features mais elogiadas

A comunidade de desenvolvedores destacou consistentemente estas funcionalidades:

**Geração de comandos complexos** é o recurso mais valorizado. Desenvolvedores relatam economia de **10+ horas semanais** em tarefas como manipulação de arquivos, operações git e configuração de ambientes.

**Explicação de comandos legados** recebeu elogios especiais para onboarding em projetos existentes. Um desenvolvedor comentou: *"Finalmente entendi aquele script bash de 200 linhas que ninguém documenta"*.

**Transparência no consumo** também foi destacada: *"A ferramenta mostra claramente quantas requisições premium você usou. Sem limites opacos ou cálculos confusos de tokens"*.

**Integração nativa com GitHub** diferencia o Copilot CLI de alternativas: criar PRs, consultar issues e gerenciar repositórios diretamente do terminal.

### 6.2 Truques e atalhos

**Referência de arquivos com @:**
```bash
> Explique @config/webpack.config.js
> Corrija o bug em @src/components/UserForm.tsx
> Otimize @utils/database.py para performance
```

**Resumo de sessão:**
```bash
# No final de uma sessão produtiva
> Resuma o que fizemos nesta sessão em formato de changelog
```

**Checkpoint automático:**
O Copilot CLI faz commit automático de mudanças não staged antes de operações destrutivas. Você pode reverter facilmente se algo der errado.

**Atalhos de teclado no modo interativo:**
- `Ctrl+C`: Cancelar operação atual
- `Ctrl+D`: Sair da sessão
- `↑/↓`: Navegar histórico de prompts
- `!comando`: Executar comando shell diretamente

**Instruções customizadas por projeto:**
```markdown
<!-- .github/copilot-instructions.md -->
# Instruções do Copilot

## Estilo de código
- Use TypeScript strict mode
- Prefira funções arrow para componentes React
- Siga Conventional Commits para mensagens

## Contexto do projeto
- Este é um e-commerce usando Next.js 14
- Backend em Node.js com Prisma ORM
- Deploy via Vercel
```

### 6.3 Casos de uso reais

**Caso 1: Migração de banco de dados**
```bash
> Analisar schema atual do PostgreSQL e gerar migrations para adicionar soft delete em todas as tabelas
```

**Caso 2: Debugging de produção**
```bash
> Analisar logs do container api-prod dos últimos 30 minutos e identificar padrões de erro
> Criar query para encontrar requisições com latência > 2s no último dia
```

**Caso 3: Automação de infraestrutura**
```bash
> Criar Terraform para provisionar VPC AWS com 3 subnets públicas e 3 privadas
> Gerar Ansible playbook para configurar nginx como reverse proxy
```

**Caso 4: Code review automatizado**
```bash
copilot -p "Revisar @src/auth/login.ts para vulnerabilidades de segurança" \
  --allow-tool 'shell(npm audit)'
```

**Caso 5: Documentação**
```bash
> Gerar README.md completo para este projeto baseado na estrutura de arquivos
> Criar documentação de API a partir dos arquivos de rota
```

### 6.4 Otimização de produtividade

**Dica 1: Sessões focadas**
Inicie novas conversas ao mudar de tópico. Conversas longas consomem mais tokens e podem atingir limites.

**Dica 2: Prompts específicos**
```bash
# ❌ Vago
> Arruma o código

# ✅ Específico
> Refatorar função validateUser em @src/auth.ts para usar early return e reduzir aninhamento
```

**Dica 3: Modo programático para scripts**
```bash
# Em scripts de automação
copilot -p "$TASK_DESCRIPTION" --allow-tool 'shell(git)' --allow-tool 'write'
```

**Dica 4: Monitorar uso**
```bash
# Verificar consumo regularmente
/usage
```

**Dica 5: Combinar com ferramentas existentes**
```bash
# Pipar saída para copilot
cat error.log | copilot -p "Analisar estes erros e sugerir correções"

# Usar em conjunto com outras CLIs
gh pr list --json number,title | copilot -p "Resuma estes PRs"
```

---

## 7. Troubleshooting Completo

### 7.1 Erros comuns e soluções

**Erro: "Unknown command 'copilot'"**
```bash
# Verificar se está instalado
which copilot
npm list -g @github/copilot

# Reinstalar
npm install -g @github/copilot
```

**Erro: "You do not have access to GitHub Copilot CLI"**
```bash
# Soluções:
# 1. Verificar assinatura em github.com/settings/copilot
# 2. Para contas de organização: pedir admin para habilitar CLI
# 3. Verificar se plano inclui CLI (Free não inclui)
```

**Erro: "spawn gh ENOENT"**
```bash
# O novo Copilot CLI requer gh CLI mesmo com GH_TOKEN
# Instalar GitHub CLI
brew install gh  # macOS
winget install GitHub.cli  # Windows
```

**Erro: "Rate limit exceeded"**
```bash
# Verificar uso
/usage

# Soluções:
# 1. Aguardar reset do limite
# 2. Usar modelo com menor multiplicador
# 3. Considerar upgrade para Pro+ (1500 requisições)
```

**Erro: "ECONNREFUSED" ou timeout**
```bash
# Testar conectividade
curl -v https://api.githubcopilot.com/_ping
curl -v https://copilot-proxy.githubusercontent.com/_ping

# Verificar proxy
echo $HTTPS_PROXY
echo $HTTP_PROXY
```

### 7.2 Problemas de autenticação

**Problema: Token OAuth inválido**
```bash
# Limpar e reautenticar
unset GH_TOKEN
unset GITHUB_TOKEN

# Nova autenticação
copilot
/login
```

**Problema: Loop de autenticação**
```bash
# Limpar credenciais
gh auth logout
git credential reject << EOF
protocol=https
host=github.com
EOF

# Reautenticar
gh auth login --web -h github.com
```

**Problema: Acesso de organização negado**
1. Verificar se admin habilitou "Copilot in the CLI" nas políticas
2. Verificar se sua conta está incluída na política de Copilot
3. Contatar administrador da organização

**Problema: PAT não funciona**
```bash
# PATs tradicionais não são totalmente suportados
# Usar fine-grained PAT com permissão "Copilot Requests"
# Criar em: github.com/settings/personal-access-tokens/new
```

### 7.3 Problemas de rede

**Configuração de proxy completa:**
```bash
# ~/.bashrc ou ~/.zshrc
export HTTP_PROXY="http://proxy.empresa.com:8080"
export HTTPS_PROXY="http://proxy.empresa.com:8080"
export NO_PROXY="localhost,127.0.0.1,.empresa.local"

# Com autenticação
export HTTPS_PROXY="http://usuario:senha@proxy.empresa.com:8080"
```

**URLs para allowlist corporativa:**
```
github.com
api.github.com
*.github.com
copilot-proxy.githubusercontent.com
api.githubcopilot.com
*.githubcopilot.com
default.exp-tas.com
objects.githubusercontent.com
```

**Certificados SSL corporativos:**
```bash
# Definir bundle de CA
export NODE_EXTRA_CA_CERTS="/etc/ssl/certs/empresa-ca-bundle.crt"

# Verificar certificado
openssl s_client -connect api.githubcopilot.com:443 -CAfile /etc/ssl/certs/empresa-ca-bundle.crt
```

**Debug de conectividade:**
```bash
# Teste básico
curl -v https://api.githubcopilot.com/_ping

# Com proxy
curl -v --proxy http://proxy:8080 https://api.githubcopilot.com/_ping

# Verificar DNS
nslookup api.githubcopilot.com
dig api.githubcopilot.com
```

### 7.4 Compatibilidade de shell

**Matriz de compatibilidade:**

| Shell | Status | Observações |
|-------|--------|-------------|
| Bash | ✅ | Totalmente suportado |
| Zsh | ✅ | Atualizar powerlevel10k se houver problemas |
| Fish | ⚠️ | Aliases requerem config manual |
| PowerShell Core (pwsh) | ✅ | Recomendado para Windows |
| PowerShell 5.1 | ⚠️ | Funcionalidade limitada |
| Command Prompt | ❌ | Não recomendado |
| Git Bash | ❌ | Limitações com execução |

**Problema: Zsh com powerlevel10k desatualizado**
```bash
cd ~/.oh-my-zsh/custom/themes/powerlevel10k
git pull
source ~/.zshrc
```

**Problema: PowerShell PSReadLine**
```powershell
# Se usando screen reader
Import-Module PSReadLine
```

**Problema: Aliases não funcionam**
```bash
# Bash - verificar se está carregando
cat ~/.bashrc | grep copilot

# Recarregar
source ~/.bashrc

# Criar manualmente se necessário
alias cop='copilot'
```

### 7.5 Gestão de versões e atualizações

**Verificar versão atual:**
```bash
copilot --version
```

**Atualizar via npm:**
```bash
npm update -g @github/copilot
```

**Atualizar via Homebrew:**
```bash
brew upgrade github-copilot
```

**Instalar versão específica:**
```bash
npm install -g @github/copilot@0.0.367

# Via script
curl -fsSL https://gh.io/copilot-install | VERSION="v0.0.365" bash
```

**Desinstalar:**
```bash
# npm
npm uninstall -g @github/copilot

# Homebrew
brew uninstall github-copilot

# Limpar configurações (opcional)
rm -rf ~/.copilot
```

**Migrar de gh-copilot para novo CLI:**
```bash
# 1. Desinstalar extensão legada
gh extension remove gh-copilot

# 2. Instalar novo CLI
npm install -g @github/copilot

# 3. Reautenticar
copilot
/login

# 4. Atualizar aliases
# Trocar 'gh copilot' por 'copilot' nos scripts
```

---

## 8. Recursos Adicionais e Referências

### 8.1 Preços e limites

**Planos individuais:**

| Plano | Preço | Requisições Premium/Mês | Copilot CLI |
|-------|-------|------------------------|-------------|
| Free | $0 | 50 | ❌ Não incluído |
| Pro | $10/mês ou $100/ano | 300 | ✅ Incluído |
| Pro+ | $39/mês ou $390/ano | 1.500 | ✅ Incluído |

**Planos organizacionais:**

| Plano | Preço | Requisições Premium | Copilot CLI |
|-------|-------|---------------------|-------------|
| Business | $19/usuário/mês | 300/seat | ✅ Controlado por política |
| Enterprise | $39/usuário/mês | 1.000/seat | ✅ Controlado por política |

**Multiplicadores de modelo:**

| Modelo | Multiplicador | Custo por Interação |
|--------|--------------|---------------------|
| GPT-5 mini, GPT-4.1 | 1x (incluído) | 0 requisições premium |
| Claude Sonnet 4.5 | 1x | 1 requisição premium |
| Claude Opus 4 | 10x | 10 requisições premium |
| GPT-4.5 | 50x | 50 requisições premium |

**Requisições premium adicionais:** $0.04 USD por requisição

### 8.2 Políticas de dados

| Aspecto | Retenção |
|---------|----------|
| Prompts e sugestões | 28 dias |
| Dados de engajamento | 2 anos |
| Treinamento com dados Business/Enterprise | ❌ Não ocorre |

### 8.3 Fluxo de confiança de diretórios

No primeiro acesso a um diretório, o Copilot CLI solicita confirmação:

```
Durante esta sessão do GitHub Copilot CLI, o Copilot pode tentar ler,
modificar e executar arquivos nesta pasta e subpastas.

[1] Sim, prosseguir (apenas esta sessão)
[2] Sim, e lembrar (confiar permanentemente)
[3] Não, sair
```

**Gerenciar diretórios confiáveis:**
```bash
# Adicionar via comando
/add-dir /caminho/para/projeto

# Ou editar config.json
# ~/.copilot/config.json
{
  "trusted_folders": [
    "/home/usuario/projetos",
    "/home/usuario/workspace"
  ]
}
```

### 8.4 Instruções customizadas

**Nível de repositório:**
```markdown
<!-- .github/copilot-instructions.md -->
# Instruções para Copilot

## Tecnologias do projeto
- Framework: Next.js 14 com App Router
- Estilização: Tailwind CSS
- Banco de dados: PostgreSQL com Prisma
- Testes: Jest + Testing Library

## Convenções
- Commits seguem Conventional Commits
- Componentes em PascalCase
- Funções utilitárias em camelCase
- Variáveis de ambiente prefixadas com NEXT_PUBLIC_ para cliente
```

**Nível de usuário:**
```markdown
<!-- ~/.copilot/copilot-instructions.md -->
# Minhas preferências

- Preferir TypeScript sobre JavaScript
- Usar async/await em vez de .then()
- Comentários em português brasileiro
- Seguir princípios SOLID
```

### 8.5 Recursos oficiais

| Recurso | URL |
|---------|-----|
| Documentação oficial | docs.github.com/en/copilot |
| Repositório CLI | github.com/github/copilot-cli |
| Status de serviço | githubstatus.com |
| Gerenciar assinatura | github.com/settings/copilot |
| Criar PAT | github.com/settings/personal-access-tokens |
| Políticas de organização | github.com/organizations/[org]/settings/copilot |

### 8.6 Glossário técnico

| Termo | Definição |
|-------|-----------|
| **Premium Request** | Interação que consome do limite mensal |
| **MCP** | Model Context Protocol - protocolo de extensibilidade |
| **Coding Agent** | Agente na nuvem para tarefas autônomas |
| **Harness Agêntico** | Framework de execução multi-step |
| **Trusted Folder** | Diretório com permissão de modificação |
| **Slash Command** | Comando iniciado com / no modo interativo |

---

## Conclusão

O GitHub Copilot CLI representa uma mudança paradigmática na interação com terminais. A transição de simples sugestor de comandos para **agente autônomo completo** abre possibilidades antes impensáveis: criar PRs, refatorar código, gerenciar infraestrutura e automatizar workflows complexos — tudo através de linguagem natural.

**Três insights-chave para maximizar o valor:**

1. **Dominar o sistema de permissões** (`--allow-tool`, `--deny-tool`) permite automação segura em scripts de CI/CD sem comprometer a segurança
2. **Extensibilidade via MCP** transforma o Copilot CLI em hub central conectando databases, APIs e ferramentas customizadas
3. **Instruções customizadas** por projeto garantem respostas contextualizadas e aderentes aos padrões da equipe

Para desenvolvedores já imersos no ecossistema GitHub, o Copilot CLI elimina fricção significativa. Para organizações, o modelo de governança via políticas permite adoção controlada. O consumo de **requisições premium** exige monitoramento, mas o `/usage` command e a transparência do sistema facilitam o planejamento.

A descontinuação do `gh copilot` em favor do novo CLI agêntico indica direção clara: GitHub aposta em assistentes cada vez mais autônomos e capazes. Desenvolvedores que dominarem esta ferramenta agora estarão preparados para a próxima geração de desenvolvimento assistido por IA.