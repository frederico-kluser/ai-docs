# npkill: o guia definitivo para limpar node_modules

O **npkill** é uma ferramenta CLI interativa que permite localizar e excluir pastas `node_modules` em todo o sistema, liberando espaço em disco de forma rápida e segura. Com mais de **9.000 estrelas no GitHub**, **~7.672 downloads semanais no npm** e suporte ativo de desenvolvimento (última versão v0.12.2 em junho de 2025), tornou-se o padrão da comunidade JavaScript para gerenciamento de espaço em disco. A ferramenta se destaca por sua interface visual interativa, avisos de segurança para pacotes críticos do sistema e execução sem instalação via `npx npkill`. Desenvolvedores relatam economia de **50GB a 200GB+** de espaço após uma única execução.

---

## O que é e como funciona tecnicamente

O npkill foi criado pela equipe voidcosmos (Juan Torres e Nya García) como solução para um problema universal dos desenvolvedores JavaScript: o acúmulo de pastas node_modules em projetos antigos ou abandonados. Cada projeto Node.js pode ter centenas de megabytes em dependências, e ao longo do tempo, esses "buracos negros" de armazenamento podem consumir dezenas de gigabytes.

A arquitetura técnica utiliza **TypeScript** com operações de disco de baixo nível e **Worker Threads** para buscas paralelas, resultando em performance **70% mais rápida** após a atualização v0.11.1. O pacote é minimalista com apenas **3 dependências de produção**: `ansi-escapes` (códigos ANSI do terminal), `picocolors` (cores) e `open-file-explorer` (abertura de diretórios). A interface TUI (Terminal User Interface) permite navegação visual pelos resultados, mostrando tamanho de cada pasta e data de última modificação.

### Requisitos e instalação

| Requisito | Especificação |
|-----------|---------------|
| **Node.js** | v14 ou superior (use `npkill@0.8.3` para Node < 14) |
| **Sistemas** | Windows, macOS, Linux |
| **Terminal** | Requer suporte TTY (Git Bash no Windows não funciona) |
| **Licença** | MIT |

```bash
# Execução rápida (recomendado - sem instalação)
npx npkill

# Instalação global
npm i -g npkill

# Com yarn
yarn global add npkill

# Com pnpm
pnpx npkill
```

---

## Funcionalidades principais e comandos disponíveis

A interface interativa do npkill oferece navegação intuitiva com teclas de seta ou estilo vim (j/k). O sistema de **avisos visuais** (⚠️) alerta quando uma pasta node_modules pertence a aplicações do sistema como Spotify, Discord ou VSCode, evitando exclusões acidentais que quebrariam esses programas.

### Controles de navegação

| Tecla | Ação |
|-------|------|
| ↑ / k | Mover para cima |
| ↓ / j | Mover para baixo |
| PgUp / Ctrl+u | Página anterior |
| PgDown / Ctrl+d | Próxima página |
| Space / Del | Excluir pasta selecionada |
| **T** | Alternar modo multi-seleção |
| **V** | Seleção por intervalo |
| **o** | Abrir no explorador de arquivos |
| e | Exibir popup de erros |
| Q / Ctrl+c | Sair |

### Opções de linha de comando

O npkill oferece personalização completa através de flags CLI. A opção `--dry-run` permite simular exclusões sem efetivamente remover arquivos, ideal para verificar o que seria afetado. O suporte a **saída JSON** (`--json` e `--json-stream`) possibilita integração com scripts e automações.

```bash
# Iniciar em diretório específico
npkill -d ~/projetos

# Buscar a partir do diretório home
npkill --full

# Ordenar por tamanho (maior primeiro)
npkill --sort size

# Mostrar tamanhos em GB
npkill --gb

# Excluir diretórios específicos da busca
npkill --exclude "backups, ignorar-isso"

# Alvo customizado (não apenas node_modules)
npkill --target vendor,.cache,dist

# Modo simulação (não exclui nada)
npkill --dry-run

# Saída JSON para automação
npkill --json > resultados.json
npkill --json-stream | jq '.result.path'

# Auto-excluir TODOS (use com cuidado!)
npkill --delete-all -x
```

### Recursos avançados (v0.12+)

O **modo multi-seleção** (ativado com `T`) permite selecionar múltiplas pastas para exclusão em lote. A **seleção por intervalo** (tecla `V`) facilita marcar grupos de pastas consecutivas. A barra de progresso mostra o status da busca em tempo real, e o sistema de logs salva informações na pasta temporária do sistema ao sair.

---

## Limitações conhecidas e o que a ferramenta NÃO faz

O npkill é projetado especificamente para **localização e exclusão** de pastas inteiras, não para otimização interna de node_modules. As principais limitações documentadas incluem:

O **CLI pode travar durante exclusões** de pastas muito grandes ou com muitos arquivos. **Terminais sem suporte TTY** (como Git Bash no Windows) não funcionam corretamente. A **ordenação por caminho** pode tornar o terminal lento quando há muitos resultados. **Cálculos de tamanho** ocasionalmente mostram valores maiores que o real.

Funcionalidades **não suportadas**:
- Não reduz tamanho de node_modules individual (use node-prune para isso)
- Não move para lixeira - exclusão é permanente (issue #60 aberta desde 2019)
- Não compacta/arquiva antes de excluir (issue #46 solicitada)
- Não detecta alguns node_modules em rotas muito aninhadas (issue #199)
- Compatibilidade limitada com **pnpm** no Windows devido a symlinks

---

## O que a comunidade diz: opiniões e avaliações

O sentimento da comunidade é **extremamente positivo (~95% favorável)** em todas as plataformas analisadas. O npkill recebeu endossos de desenvolvedores influentes como **Addy Osmani** (líder de engenharia do Chrome no Google), que comentou: *"npkill é ótimo para listar grandes diretórios node_modules e remover os antigos que você não precisa. Libere alguns gigas!"*

No **Twitter/X**, posts sobre a ferramenta alcançaram mais de **148.000 visualizações**, com 2.100+ curtidas em demonstrações virais. Usuários relatam economia de espaço impressionante: **@stoitec** liberou 200GB+, **@MrAhmadAwais** relatou 50GB+, e **@_jessicasachs** recuperou mais de 100GB.

No **Dev.to**, artigos sobre npkill recebem alta interação. Comentários típicos incluem: *"Isso é realmente incrível, ainda lembro quando eu deletava cada pasta node_modules manualmente uma por uma"* e *"FERRAMENTA INCRÍVEL!! Não sabia que tinha desperdiçado mais de 10GB de espaço em node_modules!"*

Artigos no **Medium** descrevem a ferramenta como *"Marie Kondo para projetos JavaScript"* e *"um salva-vidas para desenvolvedores com HDs menores"*. A facilidade de uso com `npx npkill` (sem instalação) é consistentemente elogiada.

### Críticas construtivas da comunidade

As principais reclamações se concentram em casos específicos: incompatibilidade com Git Bash no Windows, problemas ocasionais com pnpm e symlinks, e o desejo de mover arquivos para lixeira ao invés de exclusão permanente. A velocidade de exclusão também foi mencionada como área para melhoria (issue #172).

---

## Dicas de uso e melhores práticas

**Para iniciantes**: Sempre execute primeiro com `--dry-run` para visualizar o que seria excluído. Use `npkill -d ~/projetos` para focar apenas em diretórios de desenvolvimento, evitando varrer o sistema inteiro. Preste atenção aos avisos ⚠️ que indicam node_modules de aplicações do sistema.

**Para usuários avançados**: Combine `--sort size` com `--gb` para identificar rapidamente os maiores consumidores de espaço. Use o modo multi-seleção (`T`) para limpezas em lote eficientes. Aproveite a saída JSON para criar scripts automatizados: `npkill --json | jq '.results[] | select(.size > 104857600)'` filtra apenas pastas maiores que 100MB.

**Integração com workflows**: Execute npkill periodicamente (mensalmente) como parte da manutenção do ambiente de desenvolvimento. Para backups automatizados, `npkill -d ~/backups --delete-all -x` pode limpar node_modules de projetos arquivados. Lembre-se que após excluir, você precisará executar `npm install` para restaurar dependências quando voltar a trabalhar no projeto.

**Alvos alternativos**: A flag `-t` permite buscar outras pastas além de node_modules. Desenvolvedores PHP podem usar `npkill -t vendor`, e para limpar caches de build: `npkill -t dist,.cache,build`.

---

## Estatísticas de popularidade e manutenção

| Métrica | Valor |
|---------|-------|
| **Estrelas GitHub** | ~9.000 |
| **Forks** | 225 |
| **Downloads semanais (npm)** | ~7.672 |
| **Commits** | 861+ |
| **Releases** | 32 |
| **Contribuidores** | 28 |
| **Issues abertas** | 12 |
| **Última versão** | v0.12.2 (junho 2025) |

O projeto demonstra **desenvolvimento ativo e consistente**. A versão 0.11.1 ("The Performance Update") trouxe melhorias significativas de 70% na velocidade de busca e 90% na otimização da UI. O time core responde a issues e aceita contribuições regularmente. Patrocinadores incluem **Salesforce** e **Thinkmill** via OpenCollective.

---

## Alternativas e comparações detalhadas

### node-prune (4.400+ estrelas)
Ferramenta em **Go** por TJ Holowaychuk que remove arquivos desnecessários **de dentro** de node_modules (markdown, testes, TypeScript fonte). Não busca pastas pelo sistema - otimiza um único projeto para deploy. Extremamente rápida (~200ms), ideal para **serverless/Lambda**. Porém, não é mais mantida ativamente (último release em 2017).

### rimraf (22.000+ dependentes)
Implementação cross-platform de `rm -rf`, essencial para **Windows** onde limites de caminho causam problemas. Não tem busca/descoberta - você precisa saber o caminho exato. Ideal para **scripts CI/CD** e automação: `rimraf node_modules && npm ci`.

### pnpm (33.200+ estrelas)
Gerenciador de pacotes alternativo que **previne o problema** usando armazenamento content-addressable com symlinks. Cada versão de pacote existe uma única vez no disco, independente de quantos projetos a usam. Para projetos novos ou migração, é a solução mais eficiente a longo prazo.

### depcheck
Analisa dependências para encontrar pacotes **não utilizados** em package.json. Complementar ao npkill - primeiro use depcheck para remover dependências desnecessárias, depois npkill para limpar pastas antigas. Os mantenedores recomendam migrar para **Knip** como alternativa mais moderna.

### Quando usar cada ferramenta

Para **limpeza interativa geral**, npkill é a melhor escolha pela segurança e visualização. Para **otimização de deploy**, combine node-prune + clean-modules. Para **scripts automatizados**, use rimraf. Para **prevenção de bloat em novos projetos**, adote pnpm como gerenciador de pacotes.

---

## Conclusão

O npkill consolidou-se como ferramenta indispensável no arsenal de desenvolvedores JavaScript. Sua combinação de **interface intuitiva**, **avisos de segurança**, **performance otimizada** e **execução sem instalação** (`npx npkill`) resolve elegantemente o problema crônico de acúmulo de node_modules. Com desenvolvimento ativo, comunidade engajada e melhorias contínuas de performance, representa a solução mais completa para recuperação de espaço em disco.

A recomendação é incorporar npkill à rotina mensal de manutenção, usar `--dry-run` para verificações seguras, e considerar pnpm para novos projetos como estratégia preventiva. Para desenvolvedores que trabalham com múltiplos projetos, a economia de **dezenas a centenas de gigabytes** justifica amplamente os poucos segundos necessários para executar a ferramenta.