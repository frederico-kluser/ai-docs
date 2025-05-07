# Agentes de IA em terminal com poderes web: Opções gratuitas com BYOK

Agentes de IA baseados em terminal emergiram como poderosas ferramentas de produtividade para desenvolvedores e usuários avançados que preferem interfaces de linha de comando. As ferramentas mais capazes combinam assistência de IA com capacidades de navegação web, permitindo aos usuários fornecerem suas próprias chaves de API. Após extensa pesquisa, apenas duas ferramentas satisfazem completamente todos os critérios: Browser-use CLI e AutoGen MultimodalWebSurfer. Claude Code oferece excelentes capacidades web, mas requer assinatura, enquanto outras ferramentas têm capacidades de navegação web limitadas ou inexistentes.

## Comparação de agentes de IA baseados em terminal

| Ferramenta | Uso Gratuito | Chave API Própria | Navegação Web | Instalação | Modelos Suportados | Desenvolvimento Ativo |
|------|-------------|-------------|--------------|--------------|------------------|-------------------|
| Browser-use CLI | ✓ | ✓ | **Excelente** | Moderada | Múltiplos | Alto |
| AutoGen MultimodalWebSurfer | ✓ | ✓ | **Excelente** | Complexa | Múltiplos | Alto |
| Claude Code | ✗ | ✗ | Muito Bom | Simples | Apenas Claude | Alto |
| AI-Shell | ✓ | ✓ | Limitado | Simples | OpenAI | Moderado |
| ShellGPT | ✓ | ✓ | Limitado | Simples | Múltiplos | Alto |
| Shell-AI | ✓ | ✓ | Nenhum | Simples | Múltiplos | Moderado |
| Shell Sage | ✓ | ✓ | Nenhum | Moderada | Múltiplos | Baixo |

## Melhores agentes de IA em terminal com navegação web

### Browser-use CLI

**Descrição**: Browser-use é uma ferramenta de terminal de código aberto que permite a modelos de IA controlar e interagir com navegadores web. Ela conecta LLMs e automação de navegador, permitindo instruções em linguagem natural para realizar tarefas web complexas.

**Instalação**:
```bash
pip install browser-use
# Com funcionalidade de memória
pip install "browser-use[memory]"
# Dependências do navegador
patchright install chromium --with-deps --no-shell
```

**Capacidades web**: 
- Automação completa de navegador com entendimento visual e HTML
- Suporte a múltiplas abas
- Rastreamento de ações via XPaths
- Suporte a perfil de navegador personalizado
- Gravação de tela em HD
- **Desempenho de navegação web**: 89% de precisão no WebVoyager Dataset com GPT-4o

**Compatibilidade de API**:
- OpenAI (GPT-4o recomendado)
- Modelos Claude da Anthropic
- Modelos Gemini do Google
- Azure OpenAI
- DeepSeek, Ollama, Grok, Novita

**Limitações da versão gratuita**: Sem limitações funcionais, mas requer auto-hospedagem e gerenciamento do próprio ambiente. A versão em nuvem ($30/mês) oferece infraestrutura pré-configurada, mas com as mesmas funcionalidades.

**Feedback da comunidade**: Usuários elogiam sua flexibilidade na escolha do modelo, mas observam que o processo de configuração pode ser tecnicamente exigente. Tem desempenho melhor que o Operator da OpenAI em benchmarks.

**Versus Claude Code**: Mais flexível na escolha do modelo e personalização, permite usar perfis de navegador existentes, mas requer configuração mais complexa que o Claude Code.

### AutoGen MultimodalWebSurfer

**Descrição**: Parte do framework AutoGen da Microsoft, o MultimodalWebSurfer é um agente baseado em terminal que controla um navegador web através do Playwright, permitindo que sistemas de IA naveguem e interajam com conteúdo web.

**Instalação**:
```bash
pip install -U "autogen-agentchat" "autogen-ext[openai,web-surfer]"
playwright install --with-deps chromium
```

**Capacidades web**: 
- Navegação web automatizada através do Chromium
- Manipulação de elementos web interativos
- Captura e análise de screenshots
- Gerenciamento de estado de sessão
- Processamento de conteúdo visual
- Integração com outros agentes AutoGen

**Compatibilidade de API**:
- OpenAI GPT-4o (modelo principal recomendado)
- Outros modelos OpenAI com visão e chamada de função
- Suporte limitado para Claude da Anthropic e modelos locais

**Limitações da versão gratuita**: Gratuito para uso, mas requer suas próprias chaves de API. Configuração técnica pode ser desafiadora.

**Feedback da comunidade**: Usuários apreciam a integração com o framework AutoGen mais amplo, mas relatam problemas com navegação de botão voltar e gerenciamento de abas.

**Versus Claude Code**: Mais personalizável, mas requer configuração técnica. Parte de um framework de agente maior que permite sistemas multi-agentes complexos. Gratuito, mas com custos de API versus o modelo de assinatura do Claude Code.

## Ferramentas com capacidades limitadas de navegação web

### AI-Shell

AI-Shell converte linguagem natural para comandos de shell, mas **não possui navegação web integrada**. Pode gerar comandos que usam ferramentas como `curl` para requisições web básicas, mas não navega em sites ou mantém sessões de navegação.

**Instalação**: `npm install -g @builder.io/ai-shell`

**Compatibilidade de API**: Modelos OpenAI (padrão: gpt-4o-mini)

**Limitações**: Sem navegação web real, apenas ajuda a gerar comandos para interações web

### ShellGPT (sgpt)

ShellGPT tem **interação web limitada** através de chamadas de função. Pode abrir URLs no navegador do sistema, mas não consegue recuperar ou processar conteúdo web diretamente.

**Instalação**: `pip install shell-gpt`

**Compatibilidade de API**: Modelos OpenAI, modelos locais via Ollama/LiteLLM

**Capacidades web**: Limitadas a abrir URLs via função `open_url_in_browser`

## Ferramentas sem capacidades de navegação web

### Shell-AI

Um assistente de IA de terminal mínimo focado na geração de comandos de shell e snippets de código. **Sem capacidades de navegação web**.

### Shell Sage

Um companheiro de terminal de código aberto com suporte a modelo local. **Sem funcionalidade de navegação web**, mas suporta múltiplos provedores de IA.

## Claude Code (referência)

Claude Code é a ferramenta de codificação baseada em terminal da Anthropic usando Claude 3.7 Sonnet. **Tem capacidades de navegação web** através de servidores MCP, mas não atende a todos os critérios por não ser gratuito (requer assinatura Claude Max ou preços de API).

**Custo**: $100/mês com Claude Max ou aproximadamente $6-12/dia usando preços de API do Anthropic Console

**Capacidades web**: Pode pesquisar na web por informações relacionadas a tarefas de codificação, documentação de referência e mais

## Fazendo a escolha certa para suas necessidades

**Para máximo poder de navegação web**: Browser-use CLI oferece a automação web mais abrangente, especialmente para fluxos de trabalho complexos que requerem interação com navegador. Destaca-se por sua personalização e execução paralela de tarefas.

**Para integração de framework**: AutoGen MultimodalWebSurfer se destaca quando você precisa de navegação web como parte de um sistema multi-agente, particularmente se você já está usando ou planeja usar o framework AutoGen.

**Para comandos de shell simples com necessidades web mínimas**: AI-Shell ou ShellGPT são suficientes se suas interações web são limitadas a gerar comandos curl/wget ou abrir URLs.

**Para usuários preocupados com custos**: Todas as ferramentas requerem chaves de API, mas usar modelos locais com Shell Sage ou ShellGPT via Ollama pode minimizar custos enquanto sacrifica capacidades de navegação web.

**Para codificação com pesquisa web**: Se o orçamento permitir, Claude Code proporciona excelente integração de assistência de codificação e navegação web em um pacote polido.

O ecossistema de IA baseado em terminal continua a evoluir rapidamente, com Browser-use CLI atualmente oferecendo o melhor equilíbrio de capacidades web, personalização e acesso gratuito (com sua própria chave de API) para usuários que precisam de navegação web poderosa em seu agente de IA de terminal.