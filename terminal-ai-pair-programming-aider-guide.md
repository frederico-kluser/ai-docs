# Aider: O seu assistente de programação com IA direto no terminal

Aider é uma poderosa ferramenta de pair programming com IA que funciona no terminal, permitindo aos desenvolvedores editar código em seus repositórios Git locais através de interações em linguagem natural com modelos de linguagem avançados (LLMs). Com o Aider, você pode construir novos projetos ou trabalhar em bases de código existentes, aproveitando ao máximo o potencial da IA para aumentar sua produtividade de desenvolvimento.

## A revolução do pair programming com IA

O Aider conecta-se a diversos provedores de LLM e atua como uma interface entre esses modelos de IA e seus arquivos de código local, permitindo que a IA faça alterações diretas em sua base de código enquanto mantém um controle de versão adequado. Seu diferencial é a capacidade de entender o contexto do seu código, trabalhar com múltiplos arquivos e se integrar perfeitamente ao seu fluxo de trabalho de desenvolvimento.

**12% mais produtivo** é o que os usuários frequentemente relatam ao incorporar o Aider em seus fluxos de trabalho de desenvolvimento, com alguns afirmando até **quadruplicação de produtividade** em certas tarefas.

O Aider foi projetado para funcionar com a maioria das linguagens de programação populares e se integra perfeitamente ao Git, permitindo um controle detalhado sobre as alterações realizadas pela IA.

## Principais recursos

### Mapeamento inteligente de repositórios

O Aider cria um mapa conciso de todo o seu repositório Git que inclui as classes e funções mais importantes, junto com seus tipos e assinaturas de chamada. Isso ajuda o LLM a entender o código que está editando e como ele se relaciona com outras partes da base de código.

- Utiliza algoritmos de classificação de grafos para otimizar o mapa
- Ajusta dinamicamente o tamanho do mapa do repositório com base no estado do chat
- Fornece contexto abrangente sem enviar todos os arquivos ao LLM
- Foca nos elementos de código mais relevantes para a conversa atual

### Integração profunda com Git

- Cria commits automáticos com mensagens descritivas para alterações feitas pela IA
- Preserva alterações do usuário com commits separados
- Permite desfazer facilmente as alterações feitas pela IA com o comando `/undo`
- Suporta visualização de diffs e execução de comandos git diretamente do chat

### Modos de chat especializados

Aider fornece quatro modos distintos de chat para diferentes necessidades:

1. **Modo code** - Faz alterações diretas no seu código com base em suas solicitações
2. **Modo ask** - Discute seu código e responde perguntas sem fazer alterações
3. **Modo architect** - Usa dois modelos: um para propor mudanças e outro para implementá-las
4. **Modo help** - Responde perguntas sobre como usar o próprio Aider

### Comandos integrados no chat

- Conjunto extenso de comandos com barra (/) para controlar o Aider (ex.: `/add`, `/drop`, `/commit`, `/model`)
- Suporte para mensagens de múltiplas linhas e vários métodos de entrada
- Comandos para gerenciar histórico de chat, executar comandos shell e muito mais

### Suporte a múltiplas linguagens

- Funciona com a maioria das linguagens de programação populares
- Suporte específico de linting para muitas linguagens (detecta e corrige erros de sintaxe automaticamente)
- Suporte de mapeamento de repositório para uma ampla gama de linguagens (mais de 150 linguagens e formatos de arquivo)

### Integração com LLMs

- Funciona melhor com Claude 3.5 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o
- Pode se conectar a quase qualquer LLM, incluindo modelos locais
- Permite alternar entre modelos durante uma sessão de chat

### Recursos adicionais

- **Voice-to-code** - Fale instruções para o Aider sem precisar digitar
- **Integração de imagens e páginas web** - Adicione contexto visual ao seu chat de programação
- **Linting e testes automatizados** - Corrija erros automaticamente
- **Integração com IDE** - Use comentários com IA no seu editor para acionar o Aider
- **Interface baseada em navegador** - Use o Aider em um navegador em vez do terminal
- **Suporte a convenções de codificação** - Diga ao Aider para seguir o estilo do seu projeto

## Instalação

O Aider oferece vários métodos de instalação:

### Instalação rápida (com Python 3.8-3.13 existente)
```
python -m pip install aider-install
aider-install
```

### Instalação em uma linha (Windows)
```
powershell -ExecutionPolicy ByPass -c "irm https://aider.chat/install.ps1 | iex"
```

### Instalação em uma linha (Mac & Linux)
```
curl -LsSf https://aider.chat/install.sh | sh
```

### Instalação com uv
```
python -m pip install uv  # Se necessário
uv tool install --force --python python3.12 aider-chat@latest
```

### Instalação com pipx
```
python -m pip install pipx  # Se necessário
pipx install aider-chat
```

### Instalação com pip
```
python -m pip install -U --upgrade-strategy only-if-needed aider-chat
```

## Como usar o Aider

### Iniciando o Aider

Execute o Aider com os arquivos de código-fonte que você deseja editar:

```
aider <arquivo1> <arquivo2> ...
```

Isso adiciona os arquivos à sessão de chat para que o Aider possa ver e editar seu conteúdo.

### Usando com LLMs

Especifique qual modelo usar:

```
# o3-mini
aider --model o3-mini --api-key openai=<chave>

# Claude 3.7 Sonnet
aider --model sonnet --api-key anthropic=<chave>
```

### Fazendo alterações no código

No prompt `aider >`, peça alterações no código e o Aider editará os arquivos para realizar sua solicitação. Ele mostrará as diferenças das alterações que está fazendo e automaticamente fará commit delas no git.

### Interação no chat

- Use `/help <pergunta>` para pedir ajuda sobre como usar o Aider
- Use comandos com barra como `/add`, `/drop`, `/model` para controlar o Aider
- Alterne entre modos de chat com `/chat-mode <modo>` ou use `/code`, `/ask`, `/architect`, `/help`
- Use `/undo` para reverter alterações que você não gostou

### Editando arquivos

- Adicione apenas os arquivos que precisam ser editados para sua tarefa
- O Aider pode tentar descobrir quais arquivos editar com base em suas solicitações
- O Aider automaticamente incluirá contexto de arquivos relacionados

## Modos de chat

O Aider oferece diferentes modos de chat para diferentes necessidades:

### Modo code
Este é o modo padrão, onde o Aider faz alterações diretas no seu código com base em suas solicitações.

```
aider> Adicione validação de entrada para a função calculate_factorial
```

### Modo ask
Neste modo, o Aider apenas responde perguntas sobre seu código sem fazer alterações.

```
aider> /ask Como funciona a função de autenticação neste código?
```

### Modo architect
Um fluxo de trabalho em duas etapas onde um modelo propõe uma solução e outro a implementa:

```
aider> /architect Implemente um sistema de cache para melhorar o desempenho das consultas ao banco de dados
```

### Modo help
Obtenha ajuda sobre como usar o próprio Aider:

```
aider> /help Como posso adicionar múltiplos arquivos ao chat?
```

## Comandos de chat avançados

O Aider oferece uma rica coleção de comandos internos:

| Comando | Descrição |
|---------|-----------|
| `/add <arquivo>` | Adiciona arquivos à sessão de chat |
| `/drop <arquivo>` | Remove arquivos da sessão de chat |
| `/ls` | Lista arquivos na sessão de chat |
| `/diff` | Mostra alterações desde sua última mensagem |
| `/commit [mensagem]` | Faz commit de todas as alterações |
| `/undo` | Desfaz e descarta a última alteração |
| `/run <comando>` | Executa um comando e compartilha resultados |
| `/clear` | Limpa o histórico de chat atual |
| `/tokens` | Mostra uso de tokens para o chat atual |
| `/git <comando>` | Executa comandos git brutos |
| `/model <modelo>` | Alterna para um modelo LLM diferente |
| `/voice` | Inicia a gravação de voz (comandos por voz) |
| `/multiline-mode` | Alterna para o modo de entrada multilinha |
| `/help [tópico]` | Obtém ajuda sobre o Aider |

## Integração com IDE

### Modo Watch Files

Aider pode monitorar seus arquivos em busca de comentários especiais com IA que acionam alterações no código:

1. Execute o Aider com a flag `--watch-files` para monitorar seu repositório
2. Adicione comentários que começam ou terminam com `AI`, `AI!` ou `AI?`
3. O Aider detectará esses comentários e realizará as ações apropriadas

### Sintaxe de comentários com IA

- **AI!**: Aciona o Aider para fazer alterações no seu código
- **AI?**: Aciona o Aider para responder à sua pergunta
- Comentários regulares com **AI**: Acumulam como instruções até que um `AI!` seja adicionado

Estilos de comentários suportados:
```
# Estilo Python e bash
// Estilo Javascript
-- Estilo SQL
```

### Exemplo de uso

```python
def factorial(n):
    # AI! Implemente essa função para calcular o fatorial de n
    pass
```

O Aider detectará o comentário e implementará a função factorial.

## Recursos avançados

### Voice-to-code

O Aider permite usar comandos de voz para editar seu código:

1. Inicie a gravação de voz com o comando `/voice` no chat
2. Fale suas instruções de codificação claramente
3. Pressione ENTER quando terminar de falar
4. O Aider transcreve sua fala e executa os comandos

### Linting e testes automáticos

- **Linting integrado**: Inclui linters para a maioria das linguagens de programação populares
- **Linters personalizados**: Especifique seu linter preferido com `--lint-cmd <cmd>`
- **Execução automática**: Por padrão, faz lint dos arquivos após cada edição
- **Configuração por linguagem**: Use `--lint "language: cmd"` para especificar diferentes linters para diferentes linguagens

### Testes integrados

- **Testes manuais**: Use `/test <comando-de-teste>` para executar testes e compartilhar resultados
- **Testes automáticos**: Configure com `--test-cmd <comando-de-teste>` e `--auto-test`
- **Tratamento de erros**: O Aider tenta corrigir erros se o comando retornar um código de saída diferente de zero

## Configuração

### Arquivo de configuração YAML

A maioria das opções do Aider pode ser definida em um arquivo `.aider.conf.yml`. O Aider procurará este arquivo nos seguintes locais:

1. Diretório atual
2. Raiz do repositório Git
3. Diretório home do usuário

Exemplo de configuração:

```yaml
# Modelo principal
model: sonnet

# Configurações gerais
map-tokens: 1024
auto-commits: true
input-history-file: .aider.input.history
chat-history-file: .aider.chat.history.md

# Configurações de linting
lint-cmd: "flake8"
auto-lint: true
```

### Variáveis de ambiente

As chaves de API e outras configurações sensíveis podem ser armazenadas em um arquivo `.env`:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
DEEPSEEK_API_KEY=...
```

O Aider procurará um arquivo `.env` na raiz do repositório Git.

### Opções de linha de comando

O Aider suporta uma ampla gama de opções de linha de comando:

```
aider --model sonnet --api-key anthropic=<chave> --no-auto-commits --map-tokens 2048
```

## Conexão com LLMs

O Aider pode se conectar a uma variedade de LLMs:

### OpenAI
```
aider --model o3-mini --api-key openai=<chave>
aider --model gpt-4o --api-key openai=<chave>
```

### Anthropic
```
aider --model claude-3-5-sonnet-20240620 --api-key anthropic=<chave>
aider --model sonnet --api-key anthropic=<chave>
```

### DeepSeek
```
aider --model deepseek-chat --api-key deepseek=<chave>
aider --model deepseek --api-key deepseek=<chave>
```

### Modelos locais
```
# Usando Ollama
aider --model ollama/<modelo-ollama>

# Usando LM Studio
export LM_STUDIO_API_KEY=dummy-api-key
export LM_STUDIO_API_BASE=http://localhost:1234/v1
aider --model <modelo-local>
```

## Linguagens suportadas

O Aider trabalha com uma ampla gama de linguagens de programação:

- Python
- JavaScript/TypeScript
- HTML/CSS
- Java
- Go
- Ruby
- Rust
- C/C++
- PHP
- E muitas outras (mais de 150 linguagens e formatos de arquivo)

O suporte para linting e mapeamento de repositório pode variar entre linguagens.

## Integração com Git

O Aider é profundamente integrado com o Git para fornecer controle de versão e rastreamento fácil de alterações de código geradas por IA:

### Workflow de Git

1. O Aider cria um repositório Git se for iniciado em um diretório sem um
2. Após fazer alterações nos arquivos, o Aider automaticamente faz commits dessas alterações com mensagens descritivas
3. Antes de editar arquivos com alterações não commitadas, o Aider primeiro faz commit dessas alterações

### Opções de configuração Git

- `--no-auto-commits`: Desativa commits automáticos do git
- `--no-dirty-commits`: Impede o commit de arquivos modificados antes de aplicar edições
- `--no-git`: Desativa completamente a integração com git
- `--git-commit-verify`: Habilita hooks de pré-commit (desativados por padrão)

## Exemplos de uso

### Criando um novo arquivo

```
aider> Crie um script Python que calcule números primos até um limite fornecido pelo usuário
```

### Modificando código existente

```
aider factorial.py
aider> Adicione manipulação de erros para entradas negativas na função factorial
```

### Uso com modo architect

```
aider app.py
aider> /architect Implemente um sistema de login com autenticação básica nesta aplicação Flask
```

### Uso com comentários de IA em IDE

```python
# app.py
def calculate_area(width, height):
    return width * height

# AI! Adicione uma função para calcular o volume de um objeto 3D
```

## Boas práticas

1. **Adicione apenas os arquivos necessários**: Adicione apenas os arquivos que precisarão ser editados
2. **Use modos de chat apropriados**: Use o modo ask para perguntas e o modo code para alterações
3. **Limpe o contexto regularmente**: Use `/drop` para remover arquivos que não são mais necessários
4. **Verifique as alterações**: Revise os diffs antes de continuar com mais alterações
5. **Use `/undo` quando necessário**: Se as alterações não estiverem corretas, use `/undo` e tente novamente
6. **Aproveite a integração com Git**: O Aider cuida do controle de versão para você
7. **Experimente diferentes modelos**: Use `/model` para alternar entre modelos para diferentes tarefas

## Limitações

1. **Desempenho do modelo**: A qualidade das alterações de código depende do LLM utilizado
2. **Contexto limitado**: Mesmo com mapeamento de repositório, há limites para o quanto do código o LLM pode "ver"
3. **Linguagens menos comuns**: O suporte para linguagens menos populares pode ser mais limitado
4. **Projetos muito grandes**: Bases de código extremamente grandes podem ser desafiadoras
5. **Necessidade de revisão**: Sempre revise as alterações sugeridas pela IA antes de integrá-las em produção

## Conclusão

O Aider é uma ferramenta revolucionária que traz o poder dos LLMs diretamente para o seu fluxo de trabalho de desenvolvimento. Ao integrar-se perfeitamente com o Git e fornecer uma interface natural de chat para edição de código, o Aider permite que desenvolvedores aumentem significativamente sua produtividade sem sacrificar o controle sobre suas bases de código.