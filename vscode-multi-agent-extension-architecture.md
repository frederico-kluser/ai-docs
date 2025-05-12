# Refatoração do Kilo Code para Multi-Agentes

## Visão Geral

O Kilocode atual é uma extensão de VS Code que executa um agente conversacional único, usando LangChain e APIs como OpenAI para gerar código e responder perguntas. Para suportar **múltiplas instâncias de agentes** simultaneamente (cada uma com seu próprio contexto e histórico), é necessário refatorar vários módulos-chave e introduzir um componente de orquestração em Node.js. Cada agente rodará isoladamente, mas poderá comunicar-se com os outros via um **orquestrador central**. O sistema deve permitir controle em tempo real via terminal (por exemplo, comandos de roteamento ou injeção de mensagens) e ampliar a UI do Kilocode para exibir múltiplas colunas de chat (uma coluna por agente ativo). Além disso, manteremos LangChain e OpenAI como provedores LLM e adicionaremos suporte ao modelo DeepSeek (um LLM avançado de \~600B parâmetros) como opção de fornecedor adicional.

## Módulos a Modificar

A refatoração envolve os seguintes subsistemas do Kilocode:

* **Gerenciamento de Sessões/Agentes:** Criação de uma nova camada que mantém múltiplas instâncias de agentes. Cada instância deve ter seu próprio objeto de **ChatSession** ou similar (incluindo histórico, modo de operação e recursos do LangChain). Atualmente, o Kilocode provavelmente instancia um único agente por workspace; precisaremos alterar a lógica para poder criar e rastrear *N* agentes em paralelo. Isso envolve modificar o código que inicializa o LangChain e a chain de ferramentas (RefactorChain) para aceitar um identificador de instância (por exemplo, `agentId`) e manter estados separados. Cada instância deve carregar seu próprio **Memory/Buffer** independente (por exemplo, usando [`BufferMemory` do LangChain](https://python.langchain.com/docs/modules/memory) ou similar), isolando conversas.

* **Interface de Chat (Webview):** O front-end do Kilocode, implementado em webview, precisa suportar múltiplas conversas lado a lado. Cada instância de agente corresponderá a um painel webview distinto aberto numa coluna do editor. Usamos `vscode.window.createWebviewPanel` especificando `ViewColumn.One`, `Two`, etc. para posicionar cada chat em colunas separadas. Por exemplo, com `panel = vscode.window.createWebviewPanel(id, title, vscode.ViewColumn.One, options)`, podemos abrir um chat na coluna 1, depois outro na coluna 2, etc. O VSCode permite **apenas uma coluna por painel**; para exibir N agentes, criamos N painéis distintos. Usamos `panel.reveal(...)` ou arraste do usuário para mover painéis entre colunas. Portanto, o módulo responsável pela criação do webview deve ser ajustado para gerenciar um mapa de `agentId -> WebviewPanel`. Cada painel enviará/receberá mensagens de seu respectivo agente via mensagem postMessage no webview.

* **Provider de Modelos (LLM):** Atualmente, Kilocode usa LangChain com OpenAI e possivelmente outros LLM (Gemini, Claude). Precisamos **incluir DeepSeek** como opção de modelo. Isso implica alterar o módulo de configuração de provedores de API, adicionando credenciais ou endpoint do DeepSeek. Pode-se implementar um novo “provider” no LangChain (ex.: uma classe `DeepSeekProvider` ou um adaptador similar ao `OpenAIChat`), ou usar chamadas REST/SDK do DeepSeek-V3. Citando fontes, o DeepSeek-V3 é um modelo de IA com \~600B parâmetros competitivo internacionalmente, justificando sua integração. No código, adaptaríamos o módulo de seleção de modelo (provavelmente onde se escolhe entre GPT-4, Claude, etc.) para aceitar “DeepSeek” e configurar chave/endereço da API. Além disso, verificar compatibilidade de formatos (por exemplo, DeepSeek pode usar JSON semelhante ao OpenAI, facilitando a integração via LangChain).

* **Comunicação e Orquestração:** Precisamos adicionar um **serviço externo em Node.js** que atue como orquestrador. Esse serviço cria e gerencia as instâncias de agentes (talvez executando subprocessos Node ou processos isolados de LangChain), e roda uma interface CLI para enviar comandos e mensagens a cada agente. Módulos afetados: código existente de execução de comandos (que executa no terminal) deve agora encaminhar solicitações para o orquestrador. O orquestrador também roteará mensagens entre agentes, conforme necessário. O protocolo de comunicação entre orquestrador e agentes pode ser via **WebSockets** ou **RPC**. Em Node.js, podemos usar `child_process.fork()` ou o módulo `cluster` para executar cada agente em processo separado, garantindo que cada agente tenha espaço de memória isolado. O Node também permite comunicação IPC nativa (usando `process.send()` em processos forked). Como alternativa, podemos usar WebSockets (ex.: biblioteca `ws` ou Socket.IO) para estabelecer canais bidirecionais entre orquestrador e cada agente, suportando mensagens em tempo real. Vale notar que “WebSocket é um transporte baseado em mensagens, enquanto RPC é um padrão de comunicação”; podemos escolher WebSockets para fluxo livre de mensagens e empurrar atualizações em tempo real ao CLI e UI. Se desejado, frameworks RPC (JSON-RPC ou gRPC) poderiam ser implementados sobre WebSocket/HTTP para chamadas estruturadas. Por exemplo, com **RPC sobre WebSocket** (como WAMP) podemos fazer chamadas de função remotas (ex.: `agent.sendCommand()`, `agent.getStatus()`) sem abrir portas extras no firewall.

## Isolamento de Estado por Instância

Para evitar interferência entre conversas paralelas, cada agente precisa de **estado isolado** (memória de chat, variáveis, contexto). Conforme prática recomendada, deve-se usar *instâncias distintas de agentes/langchain* por conversa. Por exemplo, ao iniciar uma nova instância `agentX`, criar um novo objeto LangChain chain com seu próprio Memory Chain (como `BufferMemory` ou `ConversationBufferWindowMemory`), evitando reutilizar objetos globais. No Node.js, podemos usar `AsyncLocalStorage` para manter contexto assíncrono separado por requisição, ou armazenar cada sessão em um banco de dados (Redis, Mongo) indexado por `agentId`. Em escala maior, Redis pode servir como **armazenamento de sessão externa**: cada agente armazena seu histórico e estado em chaves separadas, permitindo persistência e compartilhamento controlado. A sugestão da documentação do LangChain é criar “para cada pedido uma instância separada do agente” para evitar conflitos. Portanto, garantimos que, mesmo com N agentes ativos, cada um opera em seu próprio contexto de memória, atualizando e acessando apenas seus dados.

## Comunicação Entre Instâncias

Os agentes poderão cooperar ou trocar informações por meio do orquestrador. Estruturas possíveis incluem:

* **WebSocket (ou Socket.IO):** ideal para comunicação *tempo-real*, bidirecional. O orquestrador abre um servidor WebSocket; cada instância de agente (processo ou módulo Node) conecta-se como cliente. Mensagens (JSON) são enviadas via socket para outros agentes ou para o CLI. WebSocket provê canal de baixo atraso para notificações instantâneas de eventos (por exemplo, um agente terminar uma subtarefa).

* **RPC (JSON-RPC/gRPC):** define chamadas de procedimento remoto. Poderíamos implementar RPC simples sobre HTTP ou WebSocket. JSON-RPC permitiria ao orquestrador invocar funções em agentes (ex.: `agentX.runTask(params)`) retornando resultados. Para Node.js, há bibliotecas JSON-RPC leves. gRPC seria mais complexo (requer Protobufs), mas oferece forte tipagem e streaming. A diferença fundamental é que “WebSocket é um transporte baseado em mensagens, enquanto RPC é um padrão de comunicação”. Se optarmos por RPC, podemos ainda usar WebSocket como transporte (ex.: protocolo WAMP menciona RPC sobre WebSocket). Em todo caso, é importante padronizar o canal: WebSocket puro é suficiente, já que podemos definir formatos de mensagem próprios no JSON.

* **Filas e Pub/Sub (Opcional):** alternativas incluem usar Redis Pub/Sub ou um broker (RabbitMQ/Kafka) para envio de mensagens entre orquestrador e agentes. Isso desacopla componentes, mas adiciona latência e complexidade. Para cenários em tempo real e controle via terminal, WebSocket/RPC são mais diretos.

Tabela resumo de comunicação:

| Método de Comunicação        | Características                                | Vantagens                                                         | Desafios                                                     |
| ---------------------------- | ---------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------ |
| **WebSocket (bidirecional)** | Canal contínuo TCP/WebSocket.                  | Baixa latência; mensagens em push; compatível com Node.js.        | Requer manter conexão ativa; escalabilidade (N conexões).    |
| **RPC (JSON-RPC/gRPC)**      | Chamadas de procedimento remoto com estrutura. | API estruturada; fácil de depurar; pode usar HTTP ou WebSocket.   | Overhead de formatação; complexidade de sincronização.       |
| **Pub/Sub (Redis/Kafka)**    | Agentes assinam tópicos e publicam mensagens.  | Desacoplamento; persistência opcional; escalável horizontalmente. | Potencial atraso; infra adicional; nem sempre “instantâneo”. |

## Orquestrador Node.js e Controle via Terminal

O orquestrador será uma aplicação Node.js executada em CLI. Ele deve:

* **Criar e encerrar instâncias de agentes:** por comandos (ex.: `node orchestrator.js start agent1`). Isso pode usar `child_process.fork()` para rodar cada agente em processo isolado. Cada processo carrega a stack do agente (LangChain, LLM). O cluster do Node.js também usa `fork()` para criar workers IPC, sugerindo essa abordagem.

* **Roteamento de Mensagens:** lê comandos do usuário (pode usar o módulo `readline` do Node ou um CLI framework) e envia instruções via canal escolhido. Exemplo: digitar “agent1: run task X” no terminal faz o orquestrador emitir uma mensagem JSON via WebSocket/RPC a `agent1`. O terminal pode exibir saída de cada agente (por multiplexação) ou logs consolidado. Poderíamos prefixar cada linha de log com o ID do agente.

* **Comunicação Tempo-Real:** utilizando WebSocket, podemos ouvir eventos de cada agente (respostas, erros, solicitações de outro agente) e reagir imediatamente, imprimindo no terminal ou redistribuindo. O Node.js, com seu modelo de *event loop* não bloqueante, gerencia muitas conexões/conversas concorrentemente. Ou seja, mesmo em um único thread, ele lida bem com E/S de rede assíncrona, permitindo vários agentes ativos sem travar o CLI.

* **Estrutura de Comandos:** definir um protocolo simples. Por exemplo, `agentId.command` para chamar funções (run, stop, send message); `broadcast.message` para todos; `list` para listar agentes ativos; etc. O orquestrador parseia comandos, converte em JSON-RPC ou mensagens definidas e envia pelo WebSocket/RPC. Recebe resultados e exibe no console do usuário.

* **Persistência (Opcional):** pode manter estado de quais agentes estão ativos (num arquivo ou memória). Se o orchestrador reiniciar, talvez recarregue agentes pendentes. Mas é secundário.

Como Node.js lida com múltiplas conexões em paralelo graças ao seu *non-blocking I/O*, ele é adequado para este orquestrador onde cada agente é uma fonte/consumidor de mensagens independente. A comunicação IPC (entre processos Node) ou via sockets permite troca eficiente de dados sem travamentos na aplicação principal.

## Interface de Usuário com Múltiplas Colunas

Para representar cada agente separadamente, modificamos a UI baseada em editor do Kilocode: ao invés de um único painel de chat, permitimos **múltiplas colunas de chat simultâneas**. O VSCode suporta painéis webview distintos em colunas One, Two, Three etc. Conforme a documentação, “um painel webview só pode aparecer em uma coluna de editor por vez. Chamar `reveal()` ou arrastar o painel move-o para outra coluna”. Dessa forma, podemos criar uma nova instância de webview para cada agente: p.e., após `createWebviewPanel` inicial nas colunas 1, 2, 3, cada agente terá sua própria coluna. O código da extensão deve gerenciar esses painéis, mapeando cada agente ao respectivo painel. No frontend (HTML/JS dos webviews), exibimos um título ou identificador do agente (ex.: “Agente A”) e usamos cores ou ícones distintos para diferenciar conversas. A troca de mensagens entre frontend e backend da extensão via `webview.postMessage` permanece, mas agora inclui o `agentId` para rotear corretamente. Em resumo, a UI gerencia um *workspace de chats paralelos*, facilitando ao usuário acompanhar várias conversas de agentes simultâneos.

## Integração do Modelo DeepSeek

Para adicionar o DeepSeek, alteramos o módulo de provedores de LLM. No Kilocode, isso significa atualizar a configuração de *Provider Profiles* e possivelmente a própria cadeia de chamadas da API do modelo. Usaremos o DeepSeek-V3 (consulte a descrição de modelo com 600B parâmetros) configurando o endpoint apropriado. Por exemplo, se DeepSeek oferece uma API REST, criaríamos um handler semelhante ao `OpenAIAPI` em LangChain. Isso mantém o uso de LangChain (apenas adicionamos um case “deepseek” no switch de provedores). Em modo local, o usuário pode inserir chave/API ou usar a integração oficial caso exista. Na interface de configuração do Kilocode (settings), disponibilizamos “DeepSeek” como opção de modelo, similar ao GPT-4 ou Gemini. Assim, cada instância de agente pode usar DeepSeek como modelo subjacente (mantendo também OpenAI via `gpt-3.5-turbo`, etc., conforme preferência). Nenhuma mudança estrutural grande é necessária no fluxo da extensão – apenas na camada de abstração de modelo, para que as chamadas ao LLM suportem DeepSeek.

## Resumo

A refatoração proposta transforma o Kilocode num sistema multi-agente coordenado:

* **Novos módulos/ajustes:** Criar um **AgenteManager** para instanciar múltiplos agentes, estender o front-end webview para várias colunas e adaptar o sistema de provedores para incluir DeepSeek.
* **Comunicação:** Utilizar **WebSockets** ou RPC para mensagens em tempo real entre agentes e orquestrador. Por exemplo, um *canal WS bidirecional* permite enviar comandos instantâneos aos agentes, e esses agentes publicam eventos de volta.
* **Isolamento de estado:** Cada agente tem seu próprio espaço de memória (chain) e configurações LangChain, conforme recomendações de isolamento. Isso previne contaminação de dados entre conversas simultâneas.
* **Orquestrador Node.js:** Um servidor Node gerencia processos de agentes (via `child_process.fork()`), lida com CLI e rotea mensagens. Node.js é apropriado para isso pois seu *event loop* não bloqueante lida bem com múltiplas conexões assíncronas.
* **UI com colunas múltiplas:** Criar múltiplos painéis de chat (uma por agente) usando `createWebviewPanel` em colunas diferentes. Cada painel se conecta a um `agentId` específico para comunicação.

Abaixo, tabela esquemática dos componentes:

| Componente           | Função                                          | Alterações Principais                                                                                  |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Agente (instância)   | Gera respostas, executa cadeias de LangChain    | Adicionar identificador; memória isolada; DeepSeek como opção de LLM.                                  |
| UI (Webview)         | Mostra chat do agente                           | Suportar múltiplos webviews (colunas One, Two, Three); roteamento de mensagens via `postMessage`.      |
| Orquestrador Node.js | Coordena agentes, recebe comandos do terminal   | Implementar CLI com `readline`; spawn de processos de agentes; canal WebSocket/RPC para comunicação.   |
| Comunicação (WS/RPC) | Canal entre orquestrador, agentes e CLI         | Estabelecer servidor WS no orquestrador; definir protocolos de mensagens JSON para comandos e eventos. |
| Model Provider       | Fornece acesso aos LLM (OpenAI, DeepSeek, etc.) | Incluir DeepSeek no configurador de modelos; adaptar adaptadores de API.                               |

Em suma, a proposta envolve isolar logicamente cada agente, oferecer um canal de comunicação central e expandir a interface para visualizar múltiplas conversas. As citações técnicas reforçam essas escolhas: Node.js permite concorrência eficiente pelo seu modelo *non-blocking*, o uso de `fork()` isola processos, isolar instâncias evita conflitos de estado, e WebSockets são adequados para comunicação em tempo real. Esta arquitetura modular atende às exigências de controle interativo e escalabilidade de vários agentes conversacionais em paralelo, mantendo as bases de LangChain e suportando o novo modelo DeepSeek.

**Fontes:** Documentação do LangChain sobre multi-agentes, especificação do VSCode Webview, discussão sobre Node.js *event loop* e Child Processes, e informações oficiais do modelo DeepSeek.
