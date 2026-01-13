# Guia completo de estruturas narrativas para games

A escolha da estrutura narrativa define fundamentalmente como jogadores experienciam uma história interativa. Este guia examina **cinco estruturas clássicas** (três atos, Pirâmide de Freytag, Jornada do Herói, Save the Cat e Kishotenketsu), **cinco estruturas alternativas** (circular, in medias res, fragmentada, paralela e episódica), e suas adaptações específicas para o meio interativo. A tensão central do design narrativo em games reside no equilíbrio entre agência do jogador e visão autoral—um problema que cada estrutura resolve de maneira distinta. Compreender essas ferramentas permite designers escolherem conscientemente como guiar jogadores através de experiências emocionais, respeitando tanto a história quanto a interatividade.

---

## Estruturas clássicas formam a fundação de toda narrativa

### A estrutura de três atos permanece universal

Originada nas observações de Aristóteles em *Poética* (335 a.C.) sobre tragédia requerer "começo, meio e fim", a estrutura de três atos foi formalizada modernamente por Syd Field em *Screenplay* (1979). A divisão segue proporções aproximadas de **25% / 50% / 25%**:

**Ato I (Setup)** estabelece personagens, mundo e conflito. O *inciting incident* perturba o status quo, e o *Plot Point 1* (aproximadamente 25%) força o protagonista a se comprometer com a jornada. Em games, este ato frequentemente integra-se ao tutorial—Spider-Man sendo picado pela aranha serve simultaneamente como incidente incitante e justificativa narrativa para o jogador aprender mecânicas.

**Ato II (Confrontation)** ocupa metade da história com obstáculos crescentes. O *midpoint* (50%) marca uma revelação ou reversão que transforma o protagonista de reativo para proativo. O *Plot Point 2* (75%) representa o momento mais baixo antes da resolução.

**Ato III (Resolution)** traz o clímax e a nova estabilidade. Games podem estender ou comprimir este ato dependendo se desejam reflexão pós-climax ou impacto imediato.

### Pirâmide de Freytag privilegia simetria dramática

Gustav Freytag analisou tragédias shakespearianas e gregas em *Die Technik des Dramas* (1863), propondo cinco partes simétricas: **exposição → ação ascendente → clímax → ação descendente → desfecho**. A diferença crucial da estrutura de três atos está na posição do clímax—Freytag o coloca no centro, criando simetria entre ascensão e queda.

```
                     CLÍMAX
                       /\
                      /  \
                     /    \
          Ação      /      \    Ação
        Ascendente /        \ Descendente
                  /          \
    Exposição___/            \___Desfecho
```

Esta estrutura funciona melhor para **tragédias** onde a queda após o clímax é tão importante quanto a ascensão. Em games, Dark Souls utiliza implicitamente esta estrutura—o midgame frequentemente apresenta o maior desafio (Ornstein e Smough em Dark Souls 1), com áreas posteriores explorando consequências e resolução.

### Jornada do Herói oferece transformação arquetípica

Joseph Campbell identificou em *O Herói de Mil Faces* (1949) um padrão universal: "Um herói se aventura do mundo comum para uma região de maravilhas sobrenaturais; forças fabulosas são encontradas e uma vitória decisiva é obtida; o herói retorna com o poder de conceder bênçãos a seus semelhantes."

Os **17 estágios originais** de Campbell foram condensados por Christopher Vogler em 12 para aplicação em Hollywood:

| Ato | Estágio | Função Narrativa |
|-----|---------|------------------|
| I | 1. Mundo Comum | Vida normal antes da aventura |
| | 2. Chamado à Aventura | Problema/desafio apresentado |
| | 3. Recusa do Chamado | Hesitação inicial |
| | 4. Encontro com o Mentor | Guia fornece sabedoria/ferramentas |
| | 5. Travessia do Primeiro Limiar | Compromisso com a jornada |
| II | 6. Testes, Aliados, Inimigos | Desafios e formação de alianças |
| | 7. Aproximação da Caverna Oculta | Preparação para o desafio central |
| | 8. Provação | Maior desafio; morte/renascimento simbólico |
| | 9. Recompensa | Herói obtém tesouro/conhecimento |
| III | 10. Caminho de Volta | Retorno com stakes renovados |
| | 11. Ressurreição | Teste final; transformação completa |
| | 12. Retorno com o Elixir | Herói volta transformado |

Mass Effect segue esta estrutura meticulosamente: Shepard começa em missão rotineira (Mundo Comum), descobre a ameaça Reaper (Chamado), recebe status de Spectre do Conselho (Mentor), e atravessa uma jornada de três jogos que culmina em sacrifício transformador.

### Save the Cat prescreve beats comerciais precisos

Blake Snyder especificou em *Save the Cat!* (2005) **15 beats com posições percentuais exatas**, tornando-se o framework mais prescritivo:

| Beat | Posição | Descrição |
|------|---------|-----------|
| Opening Image | 0-1% | Snapshot visual do mundo do protagonista |
| Theme Stated | ~5% | Tema central articulado |
| Set-Up | 1-10% | Estabelecer mundo comum |
| Catalyst | ~10% | Incidente incitante |
| Debate | 10-20% | Hesitação do herói |
| Break Into Two | ~22% | Compromisso com novo mundo |
| B Story | ~27% | Subplot (frequentemente romance) |
| Fun and Games | 27-50% | "Promessa da premissa"—cenas do trailer |
| Midpoint | 50% | Falsa vitória ou falsa derrota |
| Bad Guys Close In | 50-68% | Pressões externas/internas aumentam |
| All Is Lost | ~75% | Rock bottom; "cheiro de morte" |
| Dark Night of the Soul | 75-77% | Herói processa perda |
| Break Into Three | ~77% | Síntese—herói descobre solução |
| Finale | 77-99% | Confrontação e resolução |
| Final Image | 99-100% | Espelho transformado da Opening Image |

O conceito "Save the Cat" refere-se a fazer o protagonista realizar algo simpático cedo—como Aladdin dando pão roubado a crianças famintas—para conquistar investimento emocional do público.

### Kishotenketsu cria narrativa sem conflito central

Esta estrutura sino-japonesa de quatro atos (**Ki-Shō-Ten-Ketsu**) representa uma alternativa fundamental ao modelo ocidental baseado em conflito:

| Ato | Kanji | Função |
|-----|-------|--------|
| Ki (起) | Introdução | Estabelecer personagens e situação |
| Shō (承) | Desenvolvimento | Aprofundar compreensão |
| Ten (転) | Reviravolta | Elemento inesperado; mudança de perspectiva |
| Ketsu (結) | Conclusão | Reconciliar primeiros atos com a reviravolta |

A tensão narrativa emerge do **contraste** entre a base (Ki + Shō) e a reviravolta (Ten), não de conflito protagonista-antagonista. *Your Name* (2016) exemplifica: Taki e Mitsuha estabelecem conexão através de troca de corpos (Ki-Shō), a revelação de que Mitsuha morreu três anos antes transforma completamente o contexto (Ten), e a reconciliação temporal salva a cidade (Ketsu).

Shigeru Miyamoto aplica Kishotenketsu ao **level design** de Mario: introduzir mecânica com segurança (Ki), desenvolver habilidade do jogador (Shō), introduzir complicação à mecânica (Ten), jogador domina forma evoluída (Ketsu). Cada fase de Mario segue este padrão em miniatura.

---

## Estruturas alternativas expandem possibilidades expressivas

### Estrutura circular enfatiza transformação através de espelhamento

Narrativas circulares começam e terminam no mesmo ponto—físico, temático ou emocional—criando contraste que evidencia transformação. O espelhamento pode ser visual (mesma composição de cena), temporal (retorno ao mesmo momento), ou temático (mesmas questões respondidas diferentemente).

*The Lion King* abre e fecha com apresentação de herdeiro ao reino, mas a segunda apresentação carrega todo o peso da jornada de Simba. Em games, **roguelikes narrativos** como Hades utilizam estrutura circular: cada run retorna a Zagreus emergindo do rio Styx, mas relacionamentos e conhecimento acumulam-se através das repetições, transformando o significado de cada ciclo.

### In medias res e anacronia manipulam temporalidade

Começar *in medias res* ("no meio das coisas") joga o público direto na ação, revelando contexto gradualmente através de flashbacks (analepse) ou flashforwards (prolepse). Horace cunhou o termo em *Ars Poetica* (13 a.C.), e a *Odisseia* permanece exemplo fundacional—Odisseu já está cativo na ilha de Calipso quando a narrativa começa.

Games utilizam esta técnica de formas únicas. *God of War* (2018) abre com Kratos já estabelecido na Escandinávia, revelando seu passado grego gradualmente. A técnica funciona especialmente bem quando o **tutorial emerge do contexto narrativo**—o jogador aprende mecânicas enquanto o protagonista demonstra habilidades já desenvolvidas.

Flashforwards criam tensão através de inevitabilidade percebida. *Breaking Bad* frequentemente abre temporadas com flashforwards mostrando consequências devastadoras, fazendo o público questionar "como chegamos aqui?" durante toda a temporada.

### Narrativas fragmentadas exigem montagem ativa do público

Estruturas modulares quebram a narrativa em segmentos discretos apresentados fora de ordem cronológica. O público deve ativamente montar significado a partir dos fragmentos—processo que gera engajamento cognitivo profundo mas arrisca confusão se mal executado.

*Her Story* revolucionou esta abordagem em games: jogadores acessam banco de dados de clipes de entrevista policial através de buscas por palavras-chave, reconstruindo gradualmente uma narrativa de mistério. O jogo não tem "ordem correta"—cada jogador experiencia fragmentos em sequência única, mas todos convergem para compreensão similar.

O **estilo Rashomon** (do filme de Kurosawa, 1950) apresenta o mesmo evento de múltiplas perspectivas contraditórias, questionando a possibilidade de verdade objetiva. *The Usual Suspects* exemplifica narrativamente; em games, *Octopath Traveler* permite experienciar eventos de diferentes ângulos através de seus oito protagonistas.

### Estruturas paralelas tecem múltiplos protagonistas

Narrativas com múltiplos protagonistas podem ser convergentes (caminhos separados que colidem no clímax) ou divergentes (início comum que se fragmenta). O "cinema de hiperlink" (termo de Roger Ebert) conecta múltiplas histórias aparentemente não-relacionadas através de coincidência, tema ou interseção eventual—*Babel*, *Magnolia* e *Crash* exemplificam.

Em games, *GTA V* alterna entre três protagonistas jogáveis com arcos independentes que convergem em missões de heist. *Nier: Automata* usa perspectivas paralelas de forma mais radical—jogar como 2B, depois como 9S revelando informações ocultas da primeira playthrough, e finalmente como A2 para a conclusão completa.

O desafio de estruturas paralelas está no **balanceamento de investimento**: cada linha narrativa compete por atenção do jogador, e linhas mais fracas drenam engajamento das mais fortes.

### Estrutura episódica equilibra satisfação imediata com arco longo

O formato episódico oferece histórias completas em cada unidade enquanto contribui para narrativa maior. A distinção **serializado vs. procedural** é crucial:

- **Procedural**: Cada episódio resolve completamente (Law & Order, casos de Monster Hunter)
- **Serializado**: Arco contínuo através de episódios (Breaking Bad, maior parte dos RPGs modernos)
- **Híbrido**: "Monstro da semana" com mitologia contínua (Buffy, X-Files, série Persona)

Telltale Games popularizou narrativa episódica em games—*The Walking Dead* lançou em cinco episódios, permitindo que reações da comunidade influenciassem desenvolvimento de episódios posteriores. O formato cria antecipação entre episódios mas arrisca perder jogadores que abandonam durante hiatos.

---

## Adaptações para interatividade transformam estruturas clássicas

### Narrativas ramificadas criam ilusão de agência ilimitada

Branching narrative permite que escolhas do jogador determinem quais cenas são apresentadas. A abordagem mais comum não é árvore pura (que cria complexidade exponencial—3 escolhas por ponto × 3 pontos = 27 finais) mas **estrutura de funil**: caminhos divergem temporariamente mas reconvergem em pontos de ancoragem narrativos.

*Detroit: Become Human* representa o extremo do investimento em branching, com centenas de resultados possíveis e custos de produção correspondentemente massivos. A maioria dos jogos opta por abordagem de *Until Dawn*: personagens podem morrer em vários pontos (criando variação dramática) mas a estrutura geral permanece consistente.

Pesquisa acadêmica revelou dado surpreendente: jogadores frequentemente **não conseguem distinguir entre agência real e ilusória**. Estudo de Fendt et al. (2012) mostrou "nenhuma diferença significativa nos sentimentos reportados de agência" entre narrativas genuinamente ramificadas e narrativas lineares com feedback simulado de escolha. Telltale Games recebeu crítica por esta "ilusão de escolha"—marketing prometendo impacto de decisões que a estrutura não sustentava.

### Design hub-and-spoke oferece liberdade direcionada

A estrutura hub-and-spoke apresenta localização central (hub) de onde irradiam missões em ordem escolhida pelo jogador. Mass Effect estabeleceu o modelo com a Normandy: entre missões, jogadores exploram a nave, conversam com companheiros, desenvolvem relacionamentos. A ordem de missões afeta como informações são reveladas e relacionamentos progridem.

O desafio central é **manter coerência quando o autor não controla sequência**. Informações críticas devem estar acessíveis independentemente de caminho; dificuldade deve escalar apropriadamente para encontro em qualquer ordem; desenvolvimento de personagens deve progredir naturalmente independentemente de quando conteúdo é acessado.

*Dragon Age: The Veilguard* adotou hub-and-spoke explicitamente após críticas a *Inquisition* por "mundo aberto vazio". O hub "The Lighthouse" oferece quarters de companheiros que upgrades visualmente conforme relacionamentos desenvolvem—fornecendo feedback tangível de progressão narrativa.

### Critical path com conteúdo opcional cria profundidade em camadas

O modelo "string of pearls" (cunhado por Jesse Schell) representa **99% dos games já criados**: narrativa principal como pérolas em cordão com pequenas ramificações entre elas. Jogadores sempre retornam ao cordão principal, mas conteúdo opcional enriquece a experiência.

*The Witcher 3* elevou este modelo ao fazer side quests rivalizar ou superar a qualidade da quest principal. O Barão Sangrento—tecnicamente side quest—contém narrativa mais memorável que muitas storylines principais de outros jogos. O segredo está em **introduzir conteúdo secundário através de encontros na história principal**, não como ícones arbitrários em mapa.

**Environmental storytelling** escala particularmente bem: custos de produção menores que branching de diálogo mas recompensa jogadores dedicados. Dark Souls domina esta técnica—posicionamento de itens, arquitetura, descrições de equipamentos contam história de civilizações caídas sem exposição explícita. YouTubers como VaatiVidya construíram carreiras sintetizando lore fragmentado, e esta discussão comunitária tornou-se parte da experiência designed.

### Narrativa emergente acontece na interseção de sistemas

Henry Jenkins definiu narrativa emergente como histórias "não pré-estruturadas ou pré-programadas, tomando forma através do gameplay, porém não tão desestruturadas, caóticas e frustrantes quanto a vida real." Histórias emergem da interação jogador-sistema, não de conteúdo autoral.

*Dwarf Fortress* pioneirou sistemas de caracterização para narrativa emergente. Anões têm personalidades detalhadas derivadas de pesquisa psicológica, sistemas de memória (lembram trauma, celebram vitórias, guardam rancores), e relacionamentos que evoluem organicamente. A comunidade produz contos ilustrados de sessões de gameplay—histórias que nenhum autor escreveu mas que possuem arcos dramáticos emergentes.

*Crusader Kings 3* funciona como "máquina de Game of Thrones": intriga política, casamentos, assassinatos e guerras emergem de regras sistêmicas sem narrativa orquestrada. Jogadores descrevem experiências como "receber nova temporada de Game of Thrones a cada playthrough."

*RimWorld* explicita-se como "gerador de histórias" com "AI Storytellers"—diferentes personalidades controlando frequência e severidade de eventos. "Cassandra Classic" escalada desafios progressivamente; "Randy Random" introduz caos imprevisível. Cada configuração gera tipos diferentes de narrativa emergente.

### A tensão agência-autoria define o meio

James Newman observou: "Videogames não apresentam cenários infinitamente variáveis... Não importa quão criativa, exploratória ou desviante seja a performance do jogador, ela é limitada por regras."

Esta tensão fundamental entre promessa de interatividade e necessidade de conteúdo autoral define design narrativo em games. Soluções incluem:

**Focar na jornada, não no destino**: Mass Effect entrega os mesmos beats narrativos, mas jogadores esculpem personalidade e relacionamentos de Shepard ao longo do caminho.

**Escolhas locais significativas**: Em vez de mudar o plot inteiro, escolhas afetam personagens individuais, locais ou dinâmicas de relacionamento.

**Reconhecer restrições como tema**: BioShock transformou crítica à falta de agência em revelação narrativa—"Would you kindly?" recontextualiza todas as ações anteriores do jogador como manipuladas.

**Disco Elysium**: Falha como conteúdo interessante. Skill checks falhos fornecem momentos narrativos únicos, removendo medo de escolhas "erradas" e transformando toda interação em oportunidade de descoberta.

---

## Componentes estruturais funcionam diferentemente em contexto interativo

### Inciting incident pode ser gatilhado pelo jogador

O incidente incitante perturba o status quo do protagonista e inicia a jornada. Frameworks tradicionais posicionam-no aproximadamente **10-12%** do início, mas games introduzem variação crucial: o jogador pode ser agente ativo do incidente, não observador passivo.

Quando o jogador dispara o incidente (aceitar missão, abrir porta proibida, atacar primeiro inimigo), investimento aumenta—*sua* ação iniciou tudo. Games também podem usar **in medias res** para pular tutorial e dropar jogadores direto na ação, revelando contexto posteriormente.

A integração tutorial-incidente é técnica comum: em *Spider-Man: Miles Morales*, Miles sendo picado pela aranha é simultaneamente incidente incitante e justificativa para aprender poderes. O tutorial torna-se narrativamente orgânico—protagonista literalmente aprende novas habilidades.

### Midpoint shift pode ser mecanicamente reforçado

O midpoint marca mudança de paradigma no centro da história—nova informação significativa, stakes irrevogavelmente elevados, ponto sem retorno. Em games, esta transformação pode ser **incorporada em mecânicas**:

*Spec Ops: The Line*: O ataque com fósforo branco no midpoint parece vitória do jogador até revelar-se massacre de civis. Esta "falsa vitória" que se revela horror moral define o restante da experiência.

*BioShock*: A revelação "Would you kindly?" aproximadamente no midpoint recontextualiza completamente a agência percebida do jogador através do jogo inteiro.

*The Last of Us*: A seção de Pittsburgh marca shift de Joel protegendo Ellie como "carga" para investimento emocional genuíno—mudança motivacional reforçada por mecânicas de cooperação.

Games podem marcar midpoints através de:
- Mudanças permanentes de gameplay (novas mecânicas, habilidades perdidas)
- Transformação ambiental (mundo muda de estado)
- Shifts de relacionamento com NPCs
- Ajustes de curva de dificuldade

### All Is Lost pode ser experienciado mecanicamente

O momento "All Is Lost" (~75%) representa rock bottom—"esmagado, sem esperança, derrotado." Em mídia passiva, audiência observa; em games, jogadores podem **experienciar mecanicamente** a perda:

**Stripping mecânico**: Jogos literalmente removem recursos—armas, habilidades, aliados, safe rooms. Metroid frequentemente tira power-ups de Samus em momentos cruciais.

**Isolamento narrativo**: Personagens que acompanharam o jogador são mortos, capturados ou separados. A missão suicida de Mass Effect 2 coloca aliados em risco genuíno.

**Opressão ambiental**: Level design reforça desesperança—espaços claustrofóbicos, escuridão, ambientes hostis sem respiro.

**Remoção de agência**: Alguns jogos restringem temporariamente controle do jogador através de sequências de captura, estados de ferimento ou cutscenes narrativas.

O desafio é balancear dificuldade genuína (suportando o sentimento "all is lost") contra frustração que causa jogadores a abandonar. A emoção deve vir de contexto narrativo, não de punição mecânica arbitrária.

### Múltiplos finais aproveitam capacidade única do meio

Games oferecem estruturas de final impossíveis em mídia linear:

**Finais alternados**: Conclusões drasticamente diferentes baseadas em escolhas cumulativas. *428: Shibuya Scramble* tem 85+ finais; *The Witcher 3* tem estados de mundo divergentes.

**Finais modulares/segmentados**: Coleção de segmentos de epílogo independentes mostrando consequências de escolhas específicas. Fallout apresenta 100+ permutações de final através de slides mostrando destino de cada facção e local afetado por decisões do jogador.

**Golden endings**: Melhor resultado possível requerendo condições específicas ou porcentagem de completude. JRPGs frequentemente bloqueiam "true ending" atrás de side quests completas.

**Finais de alinhamento moral**: Caminhos bom/neutro/mau levando a conclusões diferentes (inFamous, BioShock).

Cada final deve sentir-se merecido baseado em ações do jogador. O design deve evitar fazer um final obviamente "correto"—cada rota precisa de validade narrativa própria. Considerar replayability: finais são suficientemente diferentes para justificar replay?

---

## Pacing interativo opera sob regras distintas

### Tensão e alívio seguem padrões de gameplay loop

Alternância entre tensão e alívio mantém engajamento—"repetição iguala tédio." Em games, esta alternância deve harmonizar com gameplay loops:

**Pacing ambiental**: Safe rooms (Resident Evil), áreas de hub, e zonas de exploração fornecem alívio natural.

**Pacing mecânico**: Sequências de upgrade, gerenciamento de inventário, e árvores de diálogo deslocam foco de ação para reflexão.

**Controle procedural**: Sistemas de AI Director (Left 4 Dead, Alien: Isolation) ajustam dinamicamente intensidade baseado em performance do jogador—saúde baixa reduz spawns; longos períodos sem encontro triggeram eventos.

**Pacing de horror**: Horror games tipicamente usam proporção aproximada de **3:1 tensão-para-alívio** para manter pavor sem exaurir jogadores.

A diferença fundamental de mídia linear: **jogadores parcialmente controlam pacing** através de escolhas de exploração, configurações de dificuldade, e estilo de jogo. O designer pode influenciar mas não ditar completamente.

### Subplots funcionam como side quests com qualidade variável

Side quests podem melhorar ou danificar pacing:

**Efeitos positivos**: Pausas da intensidade da quest principal; pacing controlado pelo jogador; profundidade de mundo; desenvolvimento de personagens secundários; variedade mecânica.

**Efeitos negativos**: Quebram urgência narrativa ("o mundo está acabando mas vou coletar ervas"); desconexão de temas principais danifica coerência; quantidade sobre qualidade cria fadiga.

CD Projekt Red estabeleceu best practices: introduzir side content através de encontros na história principal (o Barão Sangrento emerge de busca por Ciri, não de ícone de mapa); garantir que side quests toquem em temas do plot principal, mesmo tangencialmente; escalar disponibilidade de conteúdo secundário com urgência narrativa (menos distrações próximo ao clímax).

### Ludonarrative consonance/dissonance afeta coerência emocional

**Dissonância ludonarrativa** (termo de Clint Hocking, 2007) ocorre quando gameplay e narrativa contam histórias conflitantes:

- Nathan Drake de Uncharted: Herói charmoso em cutscenes, assassino de massa em gameplay
- Niko Bellic de GTA IV: Assombrado por violência passada em cutscenes, comete violência constante em gameplay
- Lara Croft de Tomb Raider 2013: Traumatizada pela primeira morte em cutscene, mata centenas em gameplay

**Consonância ludonarrativa** cria experiência coesa:
- Dead Space: Background de engenheiro de Isaac justifica armas improvisadas
- Journey: Cooperação multiplayer reforça temas de conexão
- Papers, Please: Gameplay burocrático cria cumplicidade moral na narrativa

**Dissonância intencional** pode ser ferramenta expressiva:
- Spec Ops: The Line torna jogadores cúmplices de atrocidades, depois os confronta
- A dissonância torna-se comentário temático sobre violência em games

---

## Framework analítico para escolha de estrutura

### Escolha de estrutura base depende de tipo de história

| Tipo de História | Estrutura Recomendada | Justificativa |
|------------------|----------------------|---------------|
| Jornada de transformação pessoal | Jornada do Herói | Padrão arquetípico de crescimento |
| Thriller/ação comercial | Save the Cat | Beats precisos maximizam engajamento |
| Tragédia com consequências | Pirâmide de Freytag | Ênfase em queda pós-clímax |
| Horror/twist | Kishotenketsu | Tensão de contraste, não conflito |
| Ensemble/coral | Estrutura Paralela | Múltiplas perspectivas enriquecem tema |
| Mistério/investigação | In Medias Res + Fragmentada | Reconstituição ativa engaja |
| Narrativa longa (RPG 40+ horas) | Hub-and-Spoke | Jogador controla pacing |
| Roguelike | Circular + Emergente | Repetição com transformação |
| Visual Novel | Branching pesado | Escolhas são o gameplay |

### Beats obrigatórios variam por estrutura mas compartilham função

Toda estrutura funcional requer:
1. **Estabelecimento** de mundo/personagem antes de disrupção
2. **Incidente incitante** que força engajamento
3. **Escalation progressiva** de stakes
4. **Ponto de virada** que transforma protagonista
5. **Climax** que testa transformação
6. **Resolução** que demonstra novo estado

A posição e ênfase destes beats varia: Hero's Journey expande a jornada; Save the Cat especifica posições percentuais; Kishotenketsu substitui "climax de conflito" por "twist de perspectiva."

### Interatividade fragmenta estruturas de formas previsíveis

Jogadores quebram estruturas autorais através de:
- **Exploração não-sequencial**: Acessando conteúdo em ordem não-pretendida
- **Variação de pacing**: Gastando 2 horas ou 20 em cada área
- **Falha e repetição**: Experienciando mesmo conteúdo múltiplas vezes
- **Abandono**: Nunca experienciando conteúdo posterior

Designers compensam através de:
- **Pontos de convergência forçados**: Momentos que todos jogadores experienciam
- **Escalation de dificuldade não-linear**: Permitindo encontro em qualquer ordem
- **Narrativa ambiental**: Não dependendo de sequência para funcionar
- **Beats redundantes**: Informações críticas reforçadas em múltiplos locais

### Planejamento de revelações requer tracking de estado

Em games, autor não controla quando jogador recebe informação. Sistemas de planejamento incluem:

**Variáveis de estado**: Baldur's Gate 3 rastreia tipo de personagem, ações, desenvolvimentos para informar branching.

**Storylets**: Pequenas peças atômicas de história taggeadas com qualidades, surfadas por sistema baseado em estado do jogador (abordagem Fallen London/Disco Elysium).

**Gating por progressão**: Conteúdo narrativo bloqueado até condições mecânicas cumpridas.

**Fallback dialogue**: NPCs têm linhas genéricas para quando jogador encontra-os fora de sequência esperada.

---

## Conclusão: estrutura serve experiência, não o contrário

A escolha de estrutura narrativa em games não é decisão acadêmica mas ferramenta prática que molda experiência emocional do jogador. **Três atos** e **Save the Cat** oferecem frameworks comercialmente testados quando o objetivo é acessibilidade e engajamento amplo. **Jornada do Herói** funciona para narrativas de transformação pessoal—especialmente RPGs onde o jogador investe dezenas de horas em desenvolvimento de personagem. **Kishotenketsu** abre possibilidades para histórias sem antagonistas claros, particularmente efetivo em horror e slice-of-life.

Para interatividade, **hub-and-spoke** equilibra liberdade de jogador com coerência narrativa; **branching** cria ownership pessoal mas multiplica custos exponencialmente; **narrativa emergente** oferece replayability infinita ao custo de controle autoral. A tensão entre agência e autoria não tem solução—apenas trade-offs conscientes.

O insight mais útil da pesquisa: **jogadores frequentemente não distinguem agência real de ilusória**. Design narrativo efetivo não requer branching infinito—requer que cada momento *sinta-se* significativo. Disco Elysium prova que skill checks falhos podem ser tão interessantes quanto sucessos; Hades demonstra que morte pode avançar narrativa; Dark Souls mostra que silêncio autoral convida colaboração comunitária.

Estruturas são ferramentas, não prisões. Os melhores jogos narrativos—The Last of Us, Red Dead Redemption 2, Disco Elysium—adaptam frameworks clássicos ao meio interativo enquanto respeitam o que torna games únicos: a capacidade de fazer jogadores *viverem* a história, não apenas observá-la.