# nve: Execute comandos em qualquer versão do Node.js

O **nve** é uma ferramenta CLI de código aberto que permite executar qualquer comando ou arquivo usando versões específicas do Node.js, sem alterar a configuração global do sistema. Diferente de gerenciadores de versão como nvm ou fnm, o nve é projetado para **execuções pontuais** — ideal para testes de compatibilidade, benchmarking e CI/CD. Com **708 estrelas no GitHub**, downloads semanais de aproximadamente **5.000-6.600 no npm**, e **74 releases** ao longo de 6 anos, o projeto é mantido ativamente por ehmicky, ex-líder técnico do Netlify Build.

## O que o nve faz e como funciona internamente

O nve resolve um problema específico: executar comandos com diferentes versões do Node.js de forma rápida e sem configuração permanente. Quando você executa `nve 12 npm test`, a ferramenta automaticamente baixa o binário do Node.js 12 (se ainda não estiver em cache), armazena-o localmente, e executa o comando `npm test` usando essa versão específica — tudo em uma única chamada.

O diferencial mais poderoso é a capacidade de rodar **múltiplas versões simultaneamente**: `nve 20,18,16 npm test` executa os testes nas três versões sequencialmente, enquanto `nve --parallel 20,18,16 npm test` roda todas em paralelo. Internamente, o nve utiliza uma arquitetura modular construída sobre o **nvexeca** (API programática), que por sua vez depende do **get-node** para download de binários, **node-version-alias** para resolver aliases como `latest` e `lts`, e **preferred-node-version** para detectar a versão do projeto a partir de arquivos como `.nvmrc` ou `package.json`.

Os benchmarks oficiais demonstram vantagem significativa: **nve executa em 295ms**, contra **741ms do nvm exec** e **1058ms do npx node** — aproximadamente 2.5x mais rápido que o nvm.

## Sintaxe completa e opções disponíveis

A sintaxe básica segue o padrão `nve [OPÇÕES] VERSÃO [COMANDO] [ARGUMENTOS]`. O nve aceita especificadores de versão flexíveis: números exatos (`12.22.1`), major versions (`12`), ranges semver (`<18`, `>=16`), e aliases especiais (`latest`, `lts`, `global`, `local`). O alias `local` é particularmente útil pois lê automaticamente a versão do `.nvmrc`, `.node-version`, ou do campo `engines.node` no `package.json`.

As opções de linha de comando incluem:

- `--parallel` / `-p`: Executa todas as versões simultaneamente
- `--continue` / `-c`: Continua executando outras versões mesmo se uma falhar
- `--mirror` / `-m`: Especifica mirror alternativo (ex: `https://npmmirror.com/mirrors/node`)
- `--fetch` / `-f`: Força atualização da lista de versões (bypass do cache de 1 hora)
- `--arch` / `-a`: Define arquitetura CPU (x32, x64, arm, arm64, s390x, ppc64)
- `--progress`: Mostra barra de progresso durante download (habilitado por padrão)

## Exemplos práticos de uso

```bash
# Executar testes em versão específica
nve 18 npm test

# Testar compatibilidade em múltiplas versões
nve 20,18,16 npm test

# Execução paralela para maior velocidade
nve --parallel 20,18,16 npm test

# Usar versão do projeto (.nvmrc ou package.json)
nve local npm run build

# Versão LTS mais recente
nve lts node --version

# Range de versões (Node menor que 18)
nve "<18" npm test

# Pre-cache de binários (baixa sem executar comando)
nve 20,18,16 node --version

# Mirror alternativo para regiões com acesso lento
nve --mirror=https://npmmirror.com/mirrors/node 16 npm test

# Descobrir versão mais recente de uma major
nve 18    # Output: 18.19.0 (sem comando, apenas imprime)
```

## Limitações e cenários onde não usar

O nve foi projetado com escopo deliberadamente limitado. **Não substitui gerenciadores de versão** como nvm, fnm ou volta — ele complementa essas ferramentas. Para sessões de desenvolvimento prolongadas ou projetos inteiros, use um gerenciador que configure a versão para todo o shell.

Restrições técnicas importantes:

- Requer **Node.js ≥18.18.0** instalado globalmente (a versão executada pode ser qualquer uma)
- Módulos nativos funcionam apenas com **N-API** e Node ≥8.12.0
- A opção `--parallel` não funciona com comandos interativos ou que não suportam concorrência
- Aliases personalizados do nvm não são reconhecidos — apenas `latest`, `lts`, `global`, `local`
- npm requer Node ≥6 para funcionar corretamente

## Instalação e configuração

A instalação é simples via qualquer gerenciador de pacotes Node:

```bash
# npm (recomendado para instalação global)
npm install -g nve

# yarn
yarn global add nve

# pnpm
pnpm add -g nve

# npx (uso sem instalação permanente)
npx nve 18 npm test
```

O nve armazena binários baixados em um diretório de cache global (`~/.cache/nve/` no Linux, localização apropriada em cada OS). Não há configuração adicional necessária — o cache é gerenciado automaticamente.

## Percepção da comunidade e casos reais

A discussão pública sobre o nve é **limitada mas consistentemente positiva**. Não há reviews negativos significativos encontrados no Reddit, Stack Overflow ou Hacker News. A ferramenta é mencionada em guias comparativos de gerenciadores Node, incluindo artigos no Honeybadger Blog e no repositório `node-version-usage`.

Os pontos mais elogiados pela comunidade são a **velocidade** (benchmark documentado de 2.5x mais rápido que nvm exec), o **suporte multiplataforma** sem necessidade de Bash ou privilégios de administrador no Windows, e a capacidade única de **execução multi-versão**.

A credibilidade do autor fortalece a confiança no projeto: ehmicky foi **líder técnico do Netlify Build** por 2.5 anos e é mantenedor do **execa** (7.300 estrelas), uma das bibliotecas mais usadas para execução de processos em Node.js.

## Comparação com alternativas

| Ferramenta | Tipo | Velocidade | Windows | Multi-versão | Melhor uso |
|------------|------|------------|---------|--------------|------------|
| **nve** | Executor one-off | 295ms | ✅ Sem admin | ✅ Sim | Testes, CI/CD, benchmarks |
| **nvm** | Gerenciador | 741ms | ❌ | ❌ | Desenvolvimento Unix |
| **fnm** | Gerenciador | Muito rápido | ✅ | ❌ | Desenvolvimento geral |
| **volta** | Gerenciador | Muito rápido | ✅ | ❌ | Projetos em equipe |
| **n** | Gerenciador | Moderado | ❌ | ❌ | Instalações simples |
| **asdf** | Multi-runtime | Moderado | ❌ | ❌ | Projetos multi-linguagem |

O nve se diferencia por **não competir** com gerenciadores de versão. Enquanto nvm/fnm/volta gerenciam qual versão está ativa no shell ou projeto, o nve permite execuções isoladas sem mudar nada permanentemente. A **recomendação é usar ambos**: um gerenciador (fnm ou volta são os mais modernos) para o dia-a-dia, e nve para testes de compatibilidade.

## Ecossistema de projetos relacionados do ehmicky

O nve é a peça central de um ecossistema modular de 9+ pacotes interconectados:

- **nvexeca**: API programática do nve para uso em scripts Node.js
- **get-node**: Download e cache de binários Node.js com verificação de checksum
- **preferred-node-version**: Detecta versão preferida de `.nvmrc`, `.node-version`, `package.json`
- **node-version-alias**: Resolve aliases (`latest`, `lts`, `erbium`) para versões específicas
- **normalize-node-version**: Valida e normaliza ranges de versão (**66.000 downloads/semana**)
- **all-node-versions**: Lista todas as versões disponíveis no nodejs.org
- **fetch-node-website**: Cliente HTTP para a API do nodejs.org/dist

Esta arquitetura em camadas permite que desenvolvedores usem exatamente o nível de abstração necessário — desde o CLI completo até componentes individuais para integração em outras ferramentas.

## Estatísticas e atividade do projeto

| Métrica | Valor |
|---------|-------|
| Estrelas GitHub | 708 |
| Forks | 13 |
| Downloads npm/semana | 5.000-6.600 |
| Versão atual | 18.0.3 (junho 2025) |
| Total de releases | 74 |
| Commits | 1.560+ |
| Issues abertas | 0 |
| Cobertura de testes | 100% |
| Licença | Apache-2.0 |

O projeto demonstra **manutenção ativa e madura**: todas as issues estão resolvidas, releases regulares acontecem, e dependências são atualizadas consistentemente. A ausência de issues abertas e o alto número de releases indicam um projeto estável em produção.

## Dicas avançadas e melhores práticas

**Pre-caching para CI/CD**: Execute `nve 20,18,16 node --version` no início do pipeline para baixar binários antes dos testes, garantindo execuções subsequentes instantâneas.

**Modo offline**: Use `--no-fetch` para trabalhar com lista de versões em cache quando sem conexão — útil para ambientes isolados.

**Integração com gerenciadores**: Configure seu `.nvmrc` ou `package.json` normalmente e use `nve local npm test` para testar com a versão do projeto sem precisar trocar versões no shell.

**Debugging de compatibilidade**: Execute `nve 8 --print 'JSON.stringify(process.versions)'` para inspecionar detalhes de runtime de versões específicas.

**Scripts de release**: Combine nve com nvexeca para automatizar testes de compatibilidade em scripts Node.js antes de publicar pacotes npm.

## Conclusão

O nve preenche uma lacuna específica no ecossistema Node.js: **execução rápida e não-intrusiva de comandos em versões específicas**. Sua velocidade superior, suporte nativo a Windows, e capacidade de multi-versão fazem dele a escolha ideal para testes de compatibilidade, pipelines CI/CD, e benchmarking. Para desenvolvedores que já usam nvm, fnm ou volta, o nve não substitui — ele **complementa**, oferecendo uma ferramenta especializada para quando você precisa testar rapidamente em outra versão sem mudar seu ambiente de desenvolvimento.