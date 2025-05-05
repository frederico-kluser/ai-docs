# Guia de desenvolvimento de sistema de edição de código TypeScript com LLM e ts-morph

Este guia detalha a construção de um sistema em que modelos de linguagem (LLMs) criem e editem aplicações TypeScript por meio de uma *representação interna* baseada em ts-morph, em vez de operar sobre os arquivos de código diretamente. Será abordado o porquê técnico de usar ts-morph, como estruturar essa representação do projeto (arquivos, classes, funções, tipos etc.), métodos de navegação semântica por objetivos, e mecanismos de edição seguras (edições locais, commit/rollback, revisão assistida). Também discutiremos como sincronizar as mudanças internas com o código real, como essa abordagem reduz alucinações do LLM e melhora o controle de contexto, além de considerações de arquitetura (frontend, backend LLM, persistência) e exemplos de fluxo (ex.: “Adicionar endpoint REST de atualização de usuário”).

## 1. Justificativa técnica: por que ts-morph?

- *Interface de alto nível: ts-morph fornece uma API de alto nível para navegar e manipular AST de TypeScript, encapsulando a complexidade da *Compiler API do TypeScript ([ts-morph - Documentation](https://ts-morph.com/#:~:text=Purpose)) ([Getting Started With Handling TypeScript ASTs](https://www.jameslmilner.com/posts/ts-ast-and-ts-morph-intro/#:~:text=Some%20might%20argue%20that%20the,deal%20with%20the%20TypeScript%20code)). Em vez de usar diretamente métodos brutos (ts.forEachChild, ts.isXyz(node), etc.), o ts-morph cria objetos ricos com métodos convenientes (ex.: .getClasses(), .setType(), .rename(), etc.) ([Getting Started With Handling TypeScript ASTs](https://www.jameslmilner.com/posts/ts-ast-and-ts-morph-intro/#:~:text=Some%20might%20argue%20that%20the,deal%20with%20the%20TypeScript%20code)). Isso torna a codificação da lógica de edição muito mais simples e expressiva.

- *Preservação de formatação e integridade: Ao contrário da edição por manipulação de strings, que é frágil e facilmente quebra a sintaxe ou formatação do código, o ts-morph trabalha sobre a AST real do projeto. Assim, ele mantém o código consistente (incluindo comentários, identação, estilo) e evita quebras acidentais. Além disso, o ts-morph **acompanha as mudanças* na árvore sintática internamente, atualizando nós já navegados após cada alteração ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=This%20library%20makes%20manipulations%20easy,syntax%20tree%20changes%20between%20manipulations)) ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=%2F%2F%20sourcefile%20contains%3A%20interface%20Person,name%3A%20number)). Por exemplo, após nameProperty.setType("number"), o getText() reflete “name: number;” corretamente ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=%2F%2F%20sourcefile%20contains%3A%20interface%20Person,name%3A%20number)). Isso evita que o LLM precise re-navegar do início a cada modificação.

- *Comparação de abordagens*: Uma visão comparativa ilustra as vantagens:

  | Abordagem           | Vantagens                                   | Desvantagens                              |
  |---------------------|---------------------------------------------|-------------------------------------------|
  | *Strings* (manipulação bruta)     | Simples inicialmente                          | Muito suscetível a erros sintáticos; não conhece estrutura do código (arriscado quebrar código) |
  | *AST puro (Compiler API)* | Total controle; mantém semântica do código  | API verosa e de baixo nível; requer muito código para tarefas comuns; difícil de navegar manualmente ([Getting Started With Handling TypeScript ASTs](https://www.jameslmilner.com/posts/ts-ast-and-ts-morph-intro/#:~:text=Some%20might%20argue%20that%20the,deal%20with%20the%20TypeScript%20code)) |
  | *ts-morph* (wrapper)      | API expressiva e de alto nível; rastreia mudanças; preserva estilo ([ts-morph - Documentation](https://ts-morph.com/#:~:text=Purpose)) ([Getting Started With Handling TypeScript ASTs](https://www.jameslmilner.com/posts/ts-ast-and-ts-morph-intro/#:~:text=Some%20might%20argue%20that%20the,deal%20with%20the%20TypeScript%20code)) ([Generating 17,000 lines of working test code in less than an hour | early Blog](https://www.startearly.ai/post/openai-startearlyai-unit-tests-benchmark-generating-1000-unit-tests-under-an-hour#:~:text=ts,and%20analyze%20TypeScript%20code%20programmatically)) | Curva de aprendizado inicial; overhead de performance para muitos arquivos |

  Como observam as documentações, ts-morph “wraps the TypeScript compiler API so it’s simple” ([ts-morph - Documentation](https://ts-morph.com/#:~:text=Purpose)) e tem “API poderosa e amigável” que simplifica manipulação de código TypeScript ([Generating 17,000 lines of working test code in less than an hour | early Blog](https://www.startearly.ai/post/openai-startearlyai-unit-tests-benchmark-generating-1000-unit-tests-under-an-hour#:~:text=ts,and%20analyze%20TypeScript%20code%20programmatically)). Ou seja, oferece o melhor do AST (segurança semântica) com facilidade de uso.

- *Exemplos de uso: Bibliotecas como Codemod e sistemas de refatoração usam ts-morph (ou ferramentas similares) para automação de código. Por exemplo, o [ts-morph](https://codemod.com/blog/ts-morph-support) é usado em engines de *codemod para migrações de código TypeScript, mostrando-se “poderoso para mudanças de código programáticas” ([Codemod AI Now Supports ts-morph](https://codemod.com/blog/ts-morph-support#:~:text=previous%20blog%20post%20%2C%20where,morph%20alongside)). E codemods facilitam tarefas como renomear funções, migrar APIs, reorganizar estrutura etc. como ilustrado por Cole Turner: AST permite “mudar quase tudo – por exemplo: renomear funções/variáveis, atualizar apps/libraries, refatorar grandes quantidades de código de forma determinística, impor boas práticas” ([Refactor your code or code your refactor? | by Cole Turner | Medium](https://medium.com/@colecodes/refactor-your-code-or-code-your-refactor-4765fd2456ee#:~:text=Under%20the%20hood%20the%20abstract,about%20anything%20%E2%80%94%20for%20example)).

Em resumo, usar ts-morph ao invés de editar texto diretamente garante manipulações semanticamente corretas e de fácil codificação, enquanto edições puras por string são arriscadas e a API bruta do TypeScript é verbosa. A camada de abstração do ts-morph reduz a chance de erros sintáticos e facilita grandes transformações automatizadas.

## 2. Abstração da aplicação com ts-morph

Para que o LLM atue sobre o código, construímos uma representação interna do projeto TypeScript usando ts-morph. Isso envolve modelar o projeto e suas dependências, e indexar entidades como arquivos, classes, funções e tipos.

- *Projeto ts-morph*: Criamos um objeto Project carregando o tsconfig.json ou adicionando todos os arquivos .ts do repositório. Esse projeto é a raíz de nosso modelo: ele contém a AST de cada arquivo fonte e configurações de compilador. Exemplo:
  ts
  const project = new Project({ tsConfigFilePath: "tsconfig.json" });
  const sourceFiles = project.getSourceFiles(); // carrega todos os .ts do projeto
  
  Dessa forma, temos acesso a cada arquivo como SourceFile no ts-morph.

- *Grafo de arquivos (dependências)*: Cada arquivo pode importar e exportar módulos. Usamos métodos como sourceFile.getImportDeclarations() para obter todas as importações de um arquivo ([ts-morph - Imports](https://ts-morph.com/details/imports#:~:text=Imports%20of%20a%20source%20file,can%20be%20retrieved%20by%20calling)). Para cada ImportDeclaration, podemos descobrir qual arquivo é referenciado (p.ex. via getModuleSpecifierSourceFile()) ([ts-morph - Imports](https://ts-morph.com/details/imports#:~:text=Get%20the%20referenced%20source%20file%3A)), montando assim um grafo de dependência entre arquivos/arquivos. Isso permite, por exemplo, identificar qual componente ou rota pertence a cada módulo.

- *Elementos de código (classes, funções, tipos, etc.)*: Com ts-morph, navegamos facilmente a AST:
  - Obter todas as classes: const classes = sourceFile.getClasses();
  - Funções top-level: sourceFile.getFunctions()
  - Interfaces: sourceFile.getInterfaces()
  - Exportações de variáveis ou enums: sourceFile.getExportedDeclarations()
  - Além disso, podemos filtrar por nome: .getClass("Nome"), .getFunction("nome") ([ts-morph - Navigating the AST](https://ts-morph.com/navigation/#:~:text=In%20general%2C%20you%20can%20easily,get%20all%20the%20child%20nodes)). Cada elemento retornado (por exemplo, um ClassDeclaration) dá acesso a seu corpo, métodos, atributos e tipos associados.
  - Podemos extrair metadados: nomes, assinaturas (parameters, retorno), tipos de propriedades, comentários JSDoc etc.

- *Mapa semântico*: Para facilitar buscas orientadas a objetivo, podemos construir índices de entidades-chave. Por exemplo, criar dicionários em memória que mapeiem nomes de funções (ou parte deles) a seus nós AST. Poderíamos indexar termos por significado (por exemplo, em português “CPF”) associando-os ao código relevante (uma função validaCPF). Isso pode ser feito por simples filtros nos nós existentes: 
  ts
  const funcCPF = project.getFunctions().find(f => /cpf/i.test(f.getName()));
  
  Ou usando comentários/documentação: verificar JSDoc/@description em getJsDocs(). Assim, o LLM pode instruir “editar função que valida CPF” e o sistema traduz para sourceFile.getFunction("validaCPF") ou busca por trecho de código que menciona “CPF”.

- *Modelo de dados*: Internamente, podemos manter objetos representando o modelo do projeto (um repositório de nós AST) e até gerar estruturas (structures) JSON via node.getStructure() que permitem recriar partes do código ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=const%20project%20%3D%20new%20Project%28,const%20classesFileStructure%20%3D%20classesFile.getStructure)). Essas estruturas podem servir para persistência ou comparação. 

Resumindo, usamos o ts-morph para criar um *grafo de objetos* representando a aplicação: projetos contêm arquivos; arquivos contêm classes, funções e tipos; e cada nó AST sabe de seus vizinhos (pai/filhos, referências). Isso permite navegação e modificação programática muito mais rica que texto simples.

## 3. Navegação semântica orientada a objetivos

Para que o LLM atenda comandos de alto nível (ex: “Editar função que valida CPF” ou “Adicionar endpoint REST de atualização de usuário”), o sistema precisa mapear linguagem natural a trechos específicos do código. Algumas estratégias:

- *Busca por nome/símbolo*: O sistema pode extrair palavras-chave da instrução. Exemplo: “função que valida CPF” sugere procurar em todas as funções por variantes de “cpf” ou “valida”. Usamos ts-morph para iterar funções e usar regex:
  ts
  const target = project.getFunctions().find(f => /validar?CPF/i.test(f.getName()));
  
  Similarmente, para “endpoint REST”, podemos buscar controllers (por convenção de nome ou anotação). 

- *Filtragem por contexto*: Além do nome, podemos verificar parâmetros e tipos. Se soubermos que “CPF” é um tipo especial (ex.: string específica), podemos filtrar funções com parâmetros/tipos relativos. Ou usar comentários: se a função possui um JSDoc explicando “Valida se o CPF…” em .getJsDocs(), o LLM pode indicar editar essa função.

- *Indexação semântica (avançada): Para projetos maiores, podemos usar técnicas de *semantic code search. Uma abordagem é criar embeddings de trechos de código (via modelo de linguagem) para consulta semântica. Por exemplo, usar um modelo de embedding para cada função+comentário e indexar num vetor DB (tipo Qdrant ([Semantic Code Search. There’s been a lot of buzz lately about… | by Xiaojing | Medium](https://medium.com/@wangxj03/semantic-code-search-010c22e7d267#:~:text=Creating%20Embeddings))). Assim, o comando em NL é convertido em embedding e recupera funções semanticamente relacionadas. Ferramentas modernas de semantic code search seguem essa ideia ([Search Through Your Codebase - Qdrant](https://qdrant.tech/documentation/advanced-tutorials/code-search/#:~:text=code%20based%20on%20similar%20logic,these%20tasks%20with%20embeddings)). O LLM pode sugerir a consulta, mas a correspondência real é feita por similaridade de texto/código. 

- *Contexto de código no prompt*: Alternativamente, incluímos trechos relevantes no prompt do LLM. Exemplo: extraímos e injetamos no contexto da conversa as assinaturas das funções encontradas e pedimos ao LLM para confirmar se é a desejada. Isso mantém o LLM focado no escopo certo, evitando buscas excessivamente amplas.

- *Navegação dirigida*: Uma vez identificado o nó-alvo pelo comando (por estratégia acima), podemos ir até ele usando as APIs do ts-morph (ex.: sourceFile.getClassOrThrow("X"), getFunction("Y")). Isso permite que as instruções do LLM sejam específicas (“edite o método validarCPF”), eliminando ambiguidades de linha de código.

Essa etapa de mapear intenção para local de código pode ser auxiliada tanto por inteligência (análise de código) quanto por interação usuário-assistente (o LLM pode pedir confirmação sobre qual função, exibindo contexto).

## 4. Edições seguras da representação (LLM + ts-morph)

Uma vez selecionado o local certo na AST, permitimos que o LLM modifique usando métodos do ts-morph. Para manter segurança e controle:

- *Edições atômicas/localizadas*: Em vez de reescrever todo o código, executamos alterações pontuais na AST. Por exemplo:
  ts
  const nameProp = personInterface.getPropertyOrThrow("name");
  nameProp.setType("number");
  
  Isso altera somente o tipo daquela propriedade, mantendo todo o resto intacto ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=%2F%2F%20sourcefile%20contains%3A%20interface%20Person,name%3A%20number)). Em geral, usamos APIs de inserção (ex.: addMethod, insertStatement), remoção (node.remove()), ou alteração (rename, setType, etc.) para mudanças específicas. Isso minimiza o risco de efeitos colaterais não previstos.

- *Modificações propostas pelo LLM: Em um possível fluxo, o LLM pode responder com comandos ou snippets de API do ts-morph. Podemos adotar um formato restrito (p. ex., JSON com ação+alvo) para forçar saídas estruturadas. Cada sugestão é aplicada no projeto em memória, **sem* ainda salvar no disco. 

- *Validação e revisão*: Antes de confirmar a alteração:
  1. *Compilação e testes*: Rodamos o compilador TypeScript (ou project.emit()) e testes automatizados para detectar erros introduzidos.
  2. *Geração de diffs*: Comparamos o estado antes e depois (p. ex. sourceFile.getText() de cada arquivo) para montar diffs. Podemos apresentar isso ao desenvolvedor ou a outro agente (talvez outro LLM) para revisão.
  3. *Revisão assistida: Opcionalmente, o próprio LLM pode revisar suas mudanças (com outro prompt), explicando o que fez ou procurando problemas. A equipe humana pode aprovar antes do *commit.

- *Rollback/Transação*: Se a alteração falhar nas validações, descartamos as mudanças no objeto Project. Como ts-morph mantém tudo em memória até save(), basta não chamar save() em caso de erro. Se necessário, reabastecemos o estado inicial (fazendo novo load do código fonte original).

- *Iterações sucessivas: Experimentos de *codemod AI mostram que refinamentos iterativos melhoram a acurácia ([Codemod AI Now Supports ts-morph](https://codemod.com/blog/ts-morph-support#:~:text=Our%20experiments%2C%20using%20our%20publicly,4o%20in%20our%20experiments)). Portanto, podemos permitir múltiplas rodadas LLM-&gt;edição-&gt;validação, ajustando o prompt a cada passo. Assim como feito pela Codemod AI (que levou precisão de 26% para 54% em exemplos de antes/depois usando 4 iterações) ([Codemod AI Now Supports ts-morph](https://codemod.com/blog/ts-morph-support#:~:text=Our%20experiments%2C%20using%20our%20publicly,4o%20in%20our%20experiments)), nosso sistema pode incluir uma espécie de “pipeline de refinamento” de mudanças do código.

- *Controle de acesso*: O sistema pode restringir o que o LLM pode alterar. Por exemplo, permitir apenas certos arquivos/símbolos, ou só inserir comandos de API (evitar eval). Essa contenção reduz chance de alterações indesejadas.

Em resumo, as edições do LLM atuam sobre o AST de forma segura: mudam apenas o necessário, testam antes de persistir, e podem ser revertidas se algo der errado. A codificação estruturada via ts-morph evita as “interminglings” caóticas que ocorrem com edições literais de código (“// existing code here”), conforme observado por desenvolvedores de LLMs ([Prompting LLMs to Modify Existing Code using ASTs](https://codeplusequalsai.com/static/blog/prompting_llms_to_modify_existing_code_using_asts.html?p#:~:text=But%20could%20LLMs%20modify%20Abstract,Syntax%20Trees)).

## 5. Sincronização com o código real

Depois que as alterações forem validadas, sincronizamos a representação interna com os arquivos reais:

- *Salvar alterações*: Ts-morph permite escrever as mudanças de volta ao sistema de arquivos. Por exemplo, basta chamar await project.save() (ou saveSync()) para que cada SourceFile alterado seja gravado em disco ([ts-morph - Emitting](https://ts-morph.com/emitting#:~:text=%2F%2F%20save%20the%20new%20files,save)). Internamente, isso reescreve o arquivo TypeScript com o conteúdo atualizado da AST.

- *Controle de versão*: Idealmente, integramos com um repositório Git. Cada alteração aprovada pode corresponder a um commit. Isso mantém o histórico e facilita rollback. É possível ainda abrir um pull request automaticamente com as mudanças para revisão humana.

- *Persistência da representação*: Embora possamos reconstituir o Project apenas recarregando os arquivos .ts, às vezes é útil armazenar metadados extra. Por exemplo, podemos salvar um snapshot do AST (via .getStructure()) ou de índices (nome→nó) num banco de dados. Isso acelera operações subsequentes e mantém estado entre reinicializações do serviço. De qualquer forma, a fonte da verdade continua sendo o código no disco; o ts-morph age como uma camada de trabalho que pode ser restaurada a partir dos arquivos fonte quando o sistema reinicia.

- *Consistência e concorrência*: Se vários agentes (LLMs ou usuários) estiverem editando simultaneamente, precisamos de sincronização. Uma abordagem é bloquear o projeto durante alterações críticas ou aplicar mudanças sequencialmente. Alternativamente, cada sessão pode atuar em uma cópia isolada e depois mesclar (merge) as mudanças no repositório principal, resolvendo conflitos.

Com esses mecanismos, garantimos que toda mudança feita na árvore sintática seja refletida no código real, com segurança e rastreabilidade.

## 6. Menor alucinação e melhor controle de contexto

Ao usar ts-morph e um modelo interno estruturado, reduzimos as alucinações típicas dos LLMs e aumentamos o controle sobre o contexto:

- *Contexto preciso*: Em vez de fornecer ao LLM uma grande quantidade de código texto para entender, podemos dar só os trechos relevantes (por exemplo, a função alvo em AST ou sua assinatura). O LLM então gera comandos de manipulação, não código irrestrito. Isso reduz a tentação do modelo de “inventar” código fora do escopo. Conforme observado, instruir o LLM a gerar mudanças sobre AST leva a melhores resultados do que pedir para reescrever livremente o código existente ([Prompting LLMs to Modify Existing Code using ASTs](https://codeplusequalsai.com/static/blog/prompting_llms_to_modify_existing_code_using_asts.html?p#:~:text=Programming%20languages%20are%20for%20humans,at%20least%20in%20simple%20cases)).

- *Semântica real*: Usando a AST, obrigamos o LLM a trabalhar com a estrutura real do programa, o que limita seu campo de jogo. Ele vê os nomes e tipos corretos de variáveis, métodos etc., e produz comandos coerentes com essa estrutura. Isso atua como “grounding” (ancoragem) do modelo no código real, mitigando saídas fantasiosas. (Por exemplo, não é permitido o LLM criar uma variável inexistente sem antes declará-la na AST.)

- *Retroalimentação de validação*: Testes automáticos e verificações de TypeScript (diferente de texto puro) capturam erros gerados pelo LLM. Quando a alteração falha, ela é rejeitada, forçando revisão. Isso reduz o risco de “hallucination” virar bug no código. Em outras palavras, só aceitamos mudanças que compilem e passem nos testes, alinhando o LLM à realidade do projeto.

- *Iterações*: O próprio processo iterativo (refinar até “convergir” no resultado correto) inibe conclusões precipitadas do LLM. Modelos podem ter alucinações, mas sessões de ajuste fazem com que a solução seja coesa com exemplos reais de código base, como mostrado pela Codemod AI ([Codemod AI Now Supports ts-morph](https://codemod.com/blog/ts-morph-support#:~:text=Our%20experiments%2C%20using%20our%20publicly,4o%20in%20our%20experiments)).

Portanto, este fluxo estruturado (AST + validações + revisão) garante que o LLM fique “nos trilhos” do código existente. Em vez de lhe dar carte blanche para escrever código arbitrário, limitamos sua atuação a um conjunto conhecido de operações sobre a AST, o que naturalmente contém a alucinação e oferece controle total do contexto.

## 7. Arquitetura do sistema

Uma arquitetura típica para esse sistema inclui:

- *Frontend / Interface*: Pode ser uma aplicação web ou plugin (VSCode, por exemplo) onde o usuário faz solicitações (textuais ou via UI) – ex: “Adicionar endpoint de usuário”. O frontend exibe mensagens do LLM, diffs de código, logs de validação e permite revisões manuais. Também exibe o diagrama do projeto ou lista de arquivos, conforme necessário.

- *Servidor de LLM (backend)*: Serviço que conversa com o modelo de linguagem (GPT-4o, etc.), recebendo instruções do usuário e estados de código. Esse módulo é responsável por:
  - Montar prompts: por exemplo, incluir assinatura de função ou contexto de código.
  - Interpretar respostas do LLM (pode vir em formato JSON de comandos ts-morph ou texto instruções).
  - Pode usar técnica de RAG (Recuperação de Informação): buscar trechos do projeto ou da documentação relevante para incluir no prompt, enriquecendo o contexto.

- *Módulo ts-morph (editor de código)*: Um serviço (por exemplo, em Node.js) que mantém o Project. Ele recebe comandos de edição (via JSON ou outra API) e executa as operações na árvore sintática, conforme detalhado na seção anterior. Também roda compilador/testes e gera diffs.

- *Armazenamento / persistência*: Aqui ficam os arquivos fonte (repositório Git) e, opcionalmente, bases auxiliares (índices de símbolos, banco de dados de sessões, logs). A persistência permite reconstruir o estado (recarregar Project) após reinicialização ou em múltiplas instâncias.

- *Orquestração e segurança*: Um componente coordenador que controla o fluxo completo, lidar com travamentos (locks), sessões de usuário e autenticação, se necessário. Também faz escalonamento de tarefas (ex.: deixar rodar testes em background) e tratamento de exceções (rollback em caso de erro).

- *Fluxo de dados*: Em um pedido típico, o usuário envia a instrução, o frontend encaminha ao LLM backend; o backend consulta (se precisar) o módulo ts-morph para contexto; formulado o prompt, o LLM responde instruções de modificação; o backend traduz essas instruções e manda para o módulo ts-morph aplicar no Project; então validamos/testamos, e retornamos ao usuário os resultados (diff ou erro). Em caso de sucesso, chamamos project.save() ([ts-morph - Emitting](https://ts-morph.com/emitting#:~:text=%2F%2F%20save%20the%20new%20files,save)) e talvez fazemos commit.

- *Exemplo de componentes*:

  | Componente       | Função                                                               |
  |------------------|----------------------------------------------------------------------|
  | *Frontend UI*  | Captura solicitações do usuário (em NL ou menu gráfico) e mostra resultados (código, diffs, logs).  |
  | *LLM Service*  | Gera prompts/respostas. Pode incluir múltiplos modelos (por ex. GPT-4o para escrever código, GPT-4 para revisão). |
  | *AST Editor*   | Instância do ts-morph que carrega o projeto. Exponibiliza API para navegação/edição.          |
  | *Validação*    | Runner de compilação e testes (CI). Garante que AST compilado está correto antes de salvar.     |
  | *Repositório Git* | Armazena o código-fonte real. Usado como armazenamento definitivo e para versionamento.        |

Essa arquitetura clara permite que cada parte foque em sua especialidade (interface com usuário, inteligência, manipulação de código, persistência) e possibilita escalabilidade e manutenção do sistema.

## 8. Exemplo prático: adicionar um endpoint REST

*Caso de uso*: “Adicionar endpoint REST que atualiza dados do usuário”. Fluxo sugerido:

1. *Análise preliminar*: O sistema reconhece “endpoint REST”, “atualizar usuário”. Possivelmente busca um arquivo de rotas (ex.: userRouter.ts) ou controller (UserController) que lide com usuários. Suponha que exista userController.ts com endpoints GET/POST, mas não PUT.

2. *Preparação para edição*: O LLM gera, a partir desse objetivo, os comandos ts-morph necessários. Por exemplo:
   - Criar método updateUser na classe controller: classDec.addMethod({ name: "updateUser", parameters: [...], returnType: "User", statements: [...] });
   - Adicionar decorator/rota: se usar framework (ex.: @Put("/:id") acima do método).
   - Importar ou usar repositório de usuários: inserir import { userService } from "../services/UserService"; se necessário.
   - Atualizar arquivo de rotas: router.put("/user/:id", userController.updateUser.bind(userController)); via addStatements na fonte das rotas.

3. *Aplicar mudanças localmente*: O ts-morph executa esses comandos, alterando apenas os locais certos. Por exemplo:
   ts
   const controller = project.getClassOrThrow("UserController");
   controller.addMethod({
     name: "updateUser",
     parameters: [{ name: "id", type: "string" }, { name: "data", type: "Partial<User>" }],
     returnType: "Promise<User>",
     statements: [
       "return userService.updateUser(id, data);"
     ]
   });
   
   Isso insere um novo método no AST de UserController.

4. *Validação*: Rodar project.emit()/tsc e testes unitários. Suponha que haja um teste para PUT /user/:id; ele falha porque criamos a função sem implementação ou rota. Nesse caso, o LLM revisa (outro prompt) para adicionar resposta HTTP adequada ou ajustar rota. Após correção, tudo compila e passa no teste.

5. *Sincronização*: Ao final, project.save() grava os arquivos modificados (UserController.ts, possivelmente userRoutes.ts). O sistema faz commit no Git (mensagem: “feat: endpoint PUT /user/:id para atualização de usuário”).

6. *Feedback ao usuário*: O frontend mostra o diff gerado e pede confirmação final. Após OK, a mudança é aplicada oficialmente no repositório.

Esse é apenas um exemplo; muitos outros fluxos (adição de classe, refatoração de função, correção de bug) seguem etapas similares. O importante é que o LLM *não edita texto livre*; ele instrui operações concretas na AST, tornando o processo previsível e rastreável.

## 9. Conclusão

Construir um sistema onde LLMs editam aplicações TypeScript via ts-morph envolve criar uma abstração estruturada do código e um fluxo controlado de edição. O uso de ts-morph (em vez de textos planos) assegura modificações sintaticamente válidas e preserva o estilo do código ([ts-morph - Documentation](https://ts-morph.com/#:~:text=Purpose)) ([Getting Started With Handling TypeScript ASTs](https://www.jameslmilner.com/posts/ts-ast-and-ts-morph-intro/#:~:text=Some%20might%20argue%20that%20the,deal%20with%20the%20TypeScript%20code)). Essa abordagem tira proveito das capacidades das ASTs para refatoração e geração de código ([Refactor your code or code your refactor? | by Cole Turner | Medium](https://medium.com/@colecodes/refactor-your-code-or-code-your-refactor-4765fd2456ee#:~:text=Under%20the%20hood%20the%20abstract,about%20anything%20%E2%80%94%20for%20example)), ao mesmo tempo que contém o LLM a comandos claros, minimizando alucinações ([Prompting LLMs to Modify Existing Code using ASTs](https://codeplusequalsai.com/static/blog/prompting_llms_to_modify_existing_code_using_asts.html?p#:~:text=Programming%20languages%20are%20for%20humans,at%20least%20in%20simple%20cases)). Ao sincronizar cada mudança ao código real apenas após validação e revisão, garantimos confiabilidade. 

Em um sistema bem arquitetado — com frontend de controle, backend LLM e módulo ts-morph dedicados —, comandos de alto nível (como “editar validação de CPF” ou “adicionar endpoint REST”) são traduzidos em operações de AST precisas. Essa pipeline promove automação inteligente sem perder o controle humano/automatizado das alterações, resultando em desenvolvimento de software mais ágil e seguro.

*Fontes:* A documentação e exemplos do ts-morph ([ts-morph - Documentation](https://ts-morph.com/#:~:text=Purpose)) ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=This%20library%20makes%20manipulations%20easy,syntax%20tree%20changes%20between%20manipulations)) ([ts-morph - Performance](https://ts-morph.com/manipulation/performance#:~:text=%2F%2F%20sourcefile%20contains%3A%20interface%20Person,name%3A%20number)) ([ts-morph - Imports](https://ts-morph.com/details/imports#:~:text=Imports%20of%20a%20source%20file,can%20be%20retrieved%20by%20calling)), blogs e estudos sobre AST e codemods ([Codemod AI Now Supports ts-morph](https://codemod.com/blog/ts-morph-support#:~:text=previous%20blog%20post%20%2C%20where,morph%20alongside)) ([Prompting LLMs to Modify Existing Code using ASTs](https://codeplusequalsai.com/static/blog/prompting_llms_to_modify_existing_code_using_asts.html?p#:~:text=Programming%20languages%20are%20for%20humans,at%20least%20in%20simple%20cases)) ([Refactor your code or code your refactor? | by Cole Turner | Medium](https://medium.com/@colecodes/refactor-your-code-or-code-your-refactor-4765fd2456ee#:~:text=Under%20the%20hood%20the%20abstract,about%20anything%20%E2%80%94%20for%20example)) foram referenciados para embasar este guia.