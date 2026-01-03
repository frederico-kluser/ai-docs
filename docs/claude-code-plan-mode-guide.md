# Claude Code CLI Plan Mode: Documentação Técnica Completa

O **Plan Mode** é um recurso fundamental do Claude Code que separa análise e planejamento da execução de código, oferecendo um ambiente read-only seguro para explorar codebases, planejar mudanças complexas e revisar código antes de qualquer modificação. Esta funcionalidade transforma o fluxo de trabalho de desenvolvimento, garantindo que desenvolvedores mantenham controle total sobre as alterações propostas pela IA antes de sua implementação.

O recurso foi introduzido silenciosamente por volta da versão **v1.0.16-v1.0.18** (aproximadamente junho de 2025) e desde então recebeu múltiplas atualizações, incluindo a introdução de subagentes dedicados ao planejamento e melhorias significativas na experiência do usuário. A filosofia por trás do Plan Mode reflete o compromisso da Anthropic com **desenvolvimento assistido por IA seguro e controlado** — permitindo que Claude analise profundamente um codebase sem o risco de modificações acidentais.

## O que é o Plan Mode e como ele difere do modo padrão

O Plan Mode é um dos **quatro modos de permissão** disponíveis no Claude Code, cada um com níveis distintos de autonomia para a IA. No modo `default` (padrão), Claude solicita permissão no primeiro uso de cada ferramenta. O modo `acceptEdits` aceita automaticamente permissões de edição de arquivos durante a sessão. Já o modo `bypassPermissions` ignora todas as verificações de permissão, exigindo um ambiente seguro e isolado.

O Plan Mode (`plan`) se diferencia fundamentalmente ao **restringir Claude exclusivamente a operações de leitura**. Neste modo, Claude pode analisar arquivos, pesquisar no codebase, buscar informações na web e criar planos detalhados, mas está **completamente bloqueado de fazer qualquer modificação** — seja editar arquivos, executar comandos ou alterar configurações. Esta separação entre análise e execução representa a essência do design philosophy do Plan Mode.

A documentação oficial da Anthropic define: *"Plan Mode instrui Claude a criar um plano analisando o codebase com operações read-only, perfeito para explorar codebases, planejar mudanças complexas ou revisar código com segurança."*

### Ferramentas disponíveis versus bloqueadas

No Plan Mode, Claude tem acesso a um conjunto específico de ferramentas read-only:

- **Read**: Visualização de arquivos e conteúdo
- **LS**: Listagem de diretórios
- **Glob**: Buscas por padrões de arquivo
- **Grep**: Pesquisas em conteúdo
- **Task**: Subagentes de pesquisa
- **WebFetch/WebSearch**: Análise e busca na web
- **NotebookRead**: Leitura de notebooks Jupyter

Ferramentas de modificação permanecem bloqueadas: **Edit/MultiEdit** (edições de arquivo), **Write** (criação de arquivos), **Bash** (execução de comandos não-readonly), **NotebookEdit** e qualquer ferramenta MCP que modifique estado do sistema.

## Métodos de ativação e configuração

### Atalho de teclado Shift+Tab

O método mais comum para ativar o Plan Mode é através do atalho **Shift+Tab**, que cicla entre os modos de permissão. A sequência funciona assim:

1. **Normal Mode** → Pressione **Shift+Tab** → **Auto-Accept Mode** (indicador: `⏵⏵ accept edits on`)
2. **Auto-Accept Mode** → Pressione **Shift+Tab** → **Plan Mode** (indicador: `⏸ plan mode on`)
3. **Plan Mode** → Pressione **Shift+Tab** → Retorna ao Normal Mode

O indicador visual `⏸ plan mode on` aparece no canto inferior esquerdo do terminal quando o modo está ativo. Importante notar que existem **problemas conhecidos no Windows** onde Shift+Tab pode não funcionar corretamente — um workaround usando Alt+M foi documentado nas issues do GitHub (#3390, #5885).

### Flag CLI --permission-mode plan

Para iniciar uma nova sessão diretamente no Plan Mode:

```bash
claude --permission-mode plan
```

Para executar queries no modo headless (não-interativo) com Plan Mode:

```bash
claude --permission-mode plan -p "Analise o sistema de autenticação e sugira melhorias"
```

### Configuração como padrão no arquivo settings

É possível definir o Plan Mode como modo padrão através do arquivo de configuração `.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

A hierarquia de configurações segue esta precedência (da maior para menor): políticas gerenciadas enterprise (`managed-settings.json`), argumentos de linha de comando, configurações locais do projeto (`.claude/settings.local.json`), configurações compartilhadas do projeto (`.claude/settings.json`), e finalmente configurações do usuário (`~/.claude/settings.json`).

### Seleção de modelo com Opus 4.5 Plan Mode

Uma funcionalidade avançada permite usar **Opus 4.5 para planejamento** e **Sonnet 4.5 para execução**. Através do comando `/model`, selecione a opção 4: "Use Opus 4.5 in plan mode, Sonnet 4.5 otherwise". Esta combinação aproveita a capacidade analítica superior do Opus para criar planos mais detalhados enquanto utiliza o Sonnet para implementação eficiente.

## Funcionamento interno e fluxo de trabalho

### As quatro fases do planejamento

O sistema de prompts interno guia Claude através de quatro fases distintas quando em Plan Mode:

**Fase 1 - Compreensão Inicial**: O objetivo é desenvolver uma compreensão abrangente da solicitação do usuário. Claude lê código relevante, faz perguntas de esclarecimento e usa paralelismo para tarefas de exploração.

**Fase 2 - Design**: Claude projeta uma abordagem de implementação, fornecendo contexto de background abrangente, descrevendo requisitos e constraints, e solicitando um plano de implementação detalhado.

**Fase 3 - Revisão**: Os planos são revisados para garantir alinhamento com as expectativas. Claude lê arquivos críticos para aprofundar o entendimento e esclarece questões restantes com o usuário.

**Fase 4 - Plano Final**: O plano é escrito em um arquivo markdown interno, incluindo apenas a abordagem recomendada (não todas as alternativas), mantendo concisão mas detalhamento suficiente para execução, e listando caminhos de arquivos críticos a serem modificados.

### Armazenamento e transição de planos

Os planos são armazenados como **arquivos markdown na pasta interna de planos** do Claude. Quando Claude está pronto para implementar após apresentar o plano, ele utiliza a ferramenta **ExitPlanMode** que lê o arquivo do plano, apresenta um **diálogo de confirmação yes/no** ao usuário e transita para o modo de execução se aprovado.

A documentação técnica especifica que esta ferramenta deve ser usada apenas quando a tarefa requer planejar etapas de implementação de código — para tarefas de pesquisa onde o objetivo é apenas entender o codebase, o ExitPlanMode não deve ser invocado.

## Guia prático de uso com exemplos

### Padrão Plan → Code → Debug → Commit

Este é o fluxo de trabalho favorito da comunidade:

```
1. Shift+Tab duas vezes (entra no Plan Mode)
2. Brainstorm com Claude usando @ references para contexto
3. Itere até estar satisfeito com a solução
4. Shift+Tab duas vezes (muda para Auto-Edit Mode)
5. Deixe Claude implementar com intervenção mínima
6. Commit das mudanças
```

### Exemplo de refatoração complexa

```bash
# Inicie em Plan Mode
claude --permission-mode plan

> Preciso refatorar nosso sistema de autenticação para usar OAuth2. 
> Crie um plano detalhado de migração.

# Refinamentos iterativos:
> E quanto à compatibilidade retroativa?
> Como devemos lidar com a migração do banco de dados?
```

### Padrão Document & Clear para tarefas extensas

Para sessões mais longas onde o contexto pode se tornar extenso:

1. Use Plan Mode para desenvolver a estratégia
2. Peça para Claude salvar o plano em um arquivo `.md` (ex: `docs/PLAN.md`)
3. Execute `/clear` para limpar o estado da conversa
4. Inicie nova sessão apontando para o documento do plano
5. Execute a implementação

### Integração com pipelines

```bash
# Pipe de entrada para Claude em plan mode
bun lint | claude --permission-mode plan "Vamos planejar como corrigir estes warnings de linting"
git diff --staged | claude --permission-mode plan "Revise este diff e planeje melhorias"
```

## Configuração avançada e parâmetros

### Parâmetro plan_mode_required para subagentes

Para configurações de equipe que exigem aprovação de plano antes de implementação, o parâmetro `plan_mode_required` pode ser utilizado no spawn de subagentes:

```json
{
  "plan_mode_required": true
}
```

### Integração com hooks

O sistema de hooks reconhece o Plan Mode. O campo `permission_mode` no input do hook conterá um dos valores: `"default"`, `"plan"`, `"acceptEdits"` ou `"bypassPermissions"`. Exemplo de estrutura de input de hook:

```json
{
  "session_id": "abc123",
  "permission_mode": "plan",
  "hook_event_name": "PreToolUse",
  "tool_name": "Read",
  "tool_input": {...}
}
```

### Integração com SDK

Para o Claude Agent SDK, modos de permissão incluindo `plan` podem ser configurados programaticamente:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const result = await query({
  prompt: "Analise este codebase",
  options: {
    permissionMode: 'plan'
  }
});
```

## Casos de uso ideais e quando evitar

### Quando usar Plan Mode

O Plan Mode é especialmente valioso em cenários específicos. Para **implementações multi-etapa** onde a feature requer edições em múltiplos arquivos, o planejamento prévio previne inconsistências e erros de integração. Na **exploração de código**, quando você quer pesquisar o codebase extensivamente antes de qualquer mudança, o modo read-only elimina o risco de alterações acidentais.

Para **desenvolvimento interativo**, quando você quer iterar na direção do projeto com Claude antes de comprometer recursos, o Plan Mode oferece o ambiente ideal para discussão técnica. Em **refatorações complexas** como migrações de arquitetura ou mudanças de paradigma (ex: migrar para OAuth2), o planejamento detalhado é essencial para sucesso.

O modo também é excelente para **onboarding em novos codebases** e **revisões de segurança**, onde análise sem risco de modificação é crítica.

### Quando evitar Plan Mode

O Plan Mode pode ser desnecessário para edições simples em arquivo único, correções rápidas de typos, tarefas que exigem baixa latência, ou quando você confia em Claude e deseja mudanças imediatas. Nestes casos, o overhead do ciclo plan-approve-execute pode reduzir produtividade sem benefício proporcional.

## Limitações conhecidas e troubleshooting

### Problemas comuns e soluções

| Problema | Solução |
|----------|---------|
| Plano muito verboso | Peça a Claude para focar em aspectos específicos |
| Claude ignora plan mode | Verifique se o indicador `⏸ plan mode on` aparece no terminal |
| Conflitos com YOLO mode | Em versões antigas havia conflito com `--dangerously-skip-permissions` — agora resolvido |
| Uso excessivo de contexto | Para sessões longas, salve o plano em arquivo externo, use `/clear`, retome com referência ao plano |
| Shift+Tab não funciona (Windows) | Use workaround Alt+M conforme issues #3390 e #5885 |

### Limitações técnicas

O código fonte do Claude Code não é publicamente disponível (o pacote NPM é compilado), portanto detalhes de implementação interna vêm de análise reversa e estudo de prompts. O caminho exato para a pasta interna de planos não é documentado em fontes oficiais. Não foram encontradas variáveis de ambiente específicas para configuração do Plan Mode — apenas configurações gerais como `MAX_THINKING_TOKENS`.

## Histórico de versões e atualizações recentes

| Versão | Data Aproximada | Mudanças |
|--------|-----------------|----------|
| v1.0.16-v1.0.18 | ~12 Jun 2025 | Plan Mode introduzido silenciosamente |
| v1.0.45 | Jul 2025 | Corrigido bug onde plano rejeitado de sub-task era descartado |
| v2.0.x | Dez 2025 | UX de saída melhorada: diálogo yes/no simplificado |
| v2.0.x | Dez 2025 | Novo Plan subagent introduzido |
| v2.0.x | Dez 2025 | Parâmetro `plan_mode_required` para teammates |
| v2.0.x | Dez 2025 | Planos mais precisos e execução mais completa |
| v2.0.x | Dez 2025 | Input de feedback ao rejeitar planos |

Atualizações recentes também incluem a **Interactive Question Tool** (para Opus 4.5 Plan Mode) que permite a Claude fazer perguntas detalhadas de esclarecimento durante o planejamento, capacidade de **resumo de subagentes** existentes, e **seleção dinâmica de modelo** onde Claude escolhe inteligentemente o melhor modelo para cada tarefa de subagente.

## Perspectivas de diferentes usuários

### Para novos usuários

Comece usando Plan Mode para qualquer tarefa que envolva mais de um arquivo. O padrão mais simples é: **Shift+Tab duas vezes** para entrar, descreva o que você quer fazer, revise o plano, **Shift+Tab duas vezes** para sair e executar. Não aceite o primeiro plano — faça perguntas, peça refinamentos, verifique edge cases.

### Para power users

Explore a combinação Opus 4.5 + Sonnet 4.5 via `/model`. Configure `defaultMode: "plan"` em projetos críticos. Use hooks para integrar Plan Mode em workflows de CI/CD. Salve planos em arquivos `.md` e use `/clear` + referência ao plano para sessões longas sem perda de contexto.

### Para foco em segurança e controle

Plan Mode é uma **camada de defesa** essencial contra modificações não intencionais. O diálogo de confirmação ao sair adiciona uma verificação explícita. Para ambientes enterprise, combine com `managed-settings.json` para enforçar Plan Mode como padrão organizacional.

## Conclusão

O Plan Mode representa uma evolução significativa na filosofia de ferramentas de coding assistido por IA, priorizando **controle humano explícito** sobre autonomia irrestrita da IA. A separação clara entre análise e execução não apenas aumenta segurança, mas frequentemente resulta em código de maior qualidade — o tempo investido no planejamento se traduz em implementações mais coerentes e menos retrabalho.

Para maximizar os benefícios, desenvolvedores devem tratar o Plan Mode não como uma etapa burocrática, mas como uma **oportunidade de colaboração técnica** com Claude. Use frases como "Me corrija se eu estiver errado..." para reduzir viés da IA, combine com extended thinking (`ultrathink`) para decisões arquiteturais complexas, e mantenha o escopo de cada sessão de planejamento focado no que será implementado nos próximos 30 minutos.

A funcionalidade continua evoluindo rapidamente — as atualizações da v2.0.x demonstram o compromisso da Anthropic em refinar tanto a experiência do usuário quanto a qualidade dos planos gerados. Desenvolvedores devem monitorar o CHANGELOG oficial para novas capabilities à medida que o Claude Code amadurece.