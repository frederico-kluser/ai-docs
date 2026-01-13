# Tutorial completo do configurador Giscus.app

O Giscus é um sistema de comentários gratuito e open-source alimentado pelo GitHub Discussions que permite adicionar uma seção de comentários a qualquer website. A configuração através do site giscus.app é feita via um **configurador interativo** que valida automaticamente seu repositório e gera o script de incorporação. Este guia documenta cada seção da interface, mensagens de validação e erros comuns.

---

## Interface completa do configurador em ordem de aparição

O configurador do giscus.app apresenta **7 seções principais** que aparecem sequencialmente na página. Cada seção deve ser preenchida na ordem correta, pois algumas dependem de validações anteriores.

### Seção 1: Language (Idioma)

A primeira seção permite selecionar o idioma da interface do widget Giscus. Aparece como um **dropdown** no topo da área de configuração. Suporta mais de **30 idiomas** incluindo Português, Inglês, Espanhol, Japonês, Chinês, entre outros. O idioma selecionado define o valor `data-lang` no script final.

### Seção 2: Repository (Repositório)

Esta é a seção mais crítica do configurador. Contém:

- **Campo de texto** com label "repository:" 
- **Texto auxiliar**: "A **public** GitHub repository. This repo is where the discussions will be linked to."
- **Lista de requisitos** exibida abaixo do campo:
  1. "The repository is **public**, otherwise visitors will not be able to view the discussion."
  2. "The **giscus** app is **installed**, otherwise visitors will not be able to comment and react."  
  3. "The **Discussions** feature is **turned on** by enabling it for your repository."

O formato correto para entrada é `username/repository-name` (exemplo: `pthurmond/patrickthurmond-comments`). **Não usar** URL completa como `https://github.com/username/repo`.

### Seção 3: Page ↔️ Discussions Mapping (Mapeamento)

Define como o Giscus encontra a Discussion correspondente a cada página. Apresenta **6 opções de radio buttons**:

| Opção | Descrição |
|-------|-----------|
| **pathname** | Título da Discussion contém o `pathname` da página (ex: `/blog/post-1`). **Recomendado** por ser portável e funcionar em localhost |
| **URL** | Título contém a URL completa da página |
| **title** | Título contém o conteúdo da tag `<title>` HTML |
| **og:title** | Título contém o valor da meta tag `og:title` |
| **specific** | Termo específico definido pelo usuário (revela campo de texto adicional) |
| **number** | Número específico de Discussion (revela campo numérico; não suporta criação automática) |

**Checkbox adicional**: "Use strict title matching" — quando marcado, usa hash SHA-1 para matching exato, evitando confusões com títulos similares. O valor `data-strict` será `"1"`.

### Seção 4: Discussion Category (Categoria de Discussion)

Esta seção **só aparece após validação bem-sucedida** do repositório na Seção 2.

**Localização visual**: Imediatamente abaixo da seção de Mapping.

**Elementos da interface**:
- **Label**: "Discussion Category"  
- **Dropdown/Select**: Lista todas as categorias de Discussions do repositório
- **Texto de recomendação**: "It is recommended to use a category with the **Announcements** type so that new discussions can only be created by maintainers and giscus."
- **Checkbox abaixo**: "Only search for discussions in this category"

**Categorias padrão do GitHub Discussions** (aparecem no dropdown):
- **Announcements** — Apenas mantenedores podem criar (recomendada)
- **General** — Discussão aberta
- **Ideas** — Compartilhar ideias
- **Q&A** — Formato pergunta e resposta
- **Show and tell** — Mostrar projetos

**Comportamento do dropdown**:
1. Se repositório inválido: dropdown desabilitado ou mostra "No categories found"
2. Se repositório válido: popula automaticamente com categorias disponíveis
3. Seleção define `data-category` e `data-category-id` no script

### Seção 5: Features (Funcionalidades)

Grupo de **4 checkboxes** para configurar comportamento do widget:

| Checkbox | Atributo | Descrição |
|----------|----------|-----------|
| "Enable reactions for the main post" | `data-reactions-enabled="1"` | Exibe reações antes dos comentários |
| "Emit discussion metadata" | `data-emit-metadata="1"` | Envia metadados para a janela pai via postMessage |
| "Place the comment box above the comments" | `data-input-position="top"` | Move caixa de input para cima |
| "Load the comments lazily" | `data-loading="lazy"` | Carrega apenas quando usuário rolar até o widget |

### Seção 6: Theme (Tema)

**Dropdown** com mais de **20 opções de tema**:

**Temas principais**:
- `light` / `dark` — Temas GitHub padrão
- `light_high_contrast` / `dark_high_contrast` — Alto contraste
- `dark_dimmed` — GitHub Dark Dimmed
- `preferred_color_scheme` — **Recomendado** (respeita preferência do usuário)
- `transparent_dark` — Fundo transparente escuro
- `noborder_light` / `noborder_dark` / `noborder_gray` — Sem bordas
- `cobalt` — RStudio Cobalt
- `purple_dark` — Roxo escuro
- `gruvbox` / `gruvbox_dark` / `gruvbox_light` — Família Gruvbox
- `catppuccin_latte` / `catppuccin_frappe` / `catppuccin_macchiato` / `catppuccin_mocha` — Família Catppuccin
- **Custom** — URL para CSS personalizado

### Seção 7: Enable giscus (Habilitar giscus)

A seção final contém o **código do script gerado** em um bloco de código copiável.

**Estados da seção**:
- **Incompleto**: Exibe mensagem "You have not configured your repository and/or category. The values for those fields will not show up until you fill them out."
- **Completo**: Exibe script completo com todos os valores preenchidos

---

## Mensagens de validação e indicadores visuais

### Validação bem-sucedida do repositório

Quando o repositório atende todos os critérios:
- **Indicador visual**: ✅ **Checkmark verde** aparece após o campo de texto do repositório
- **Comportamento**: O dropdown de Discussion Category torna-se ativo e populado
- **Script**: Seção "Enable giscus" mostra valores reais de `data-repo-id` e `data-category-id`

### Validação falha do repositório

Quando algum critério não é atendido:
- **Mensagem de erro**: **"Cannot use giscus on this repository. Make sure all of the above criteria has been met."**
- **Dropdown de categoria**: Mostra **"No categories found"**
- **Script**: Mantém placeholders `[ENTER REPO HERE]`, `[ENTER REPO ID HERE]`, etc.

### Erros de runtime (widget incorporado)

Quando o Giscus está no site mas encontra problemas:

| Erro | Mensagem | Causa |
|------|----------|-------|
| App não instalado | `"giscus is not installed on this repository"` (HTTP 403) | GitHub App não foi instalado no repositório |
| Discussion não encontrada | `"Discussion not found"` (HTTP 404) | Repositório privado, discussion deletada, ou mapping incorreto |
| Falha ao criar discussion | `"Unable to create discussion with request body"` | Categoria especificada não existe |
| Erro de CSP | `"giscus.app refused to connect"` | Content Security Policy bloqueia iframe |

---

## Processo completo de configuração passo a passo

### Fase 1: Preparação do repositório

**Passo 1** — Criar ou selecionar repositório público no GitHub. Recomendação: criar repositório dedicado com nome descritivo como `meusite-comments`.

**Passo 2** — Habilitar GitHub Discussions:
1. Acessar repositório → **Settings** (aba superior direita)
2. Rolar até seção **Features**
3. Marcar checkbox **"Discussions"**
4. Opcionalmente clicar "Set up discussions"

**Passo 3** — Instalar o Giscus GitHub App:
1. Acessar **https://github.com/apps/giscus**
2. Clicar botão **"Install"** ou **"Configure"**
3. Selecionar conta/organização
4. Escolher **"Only select repositories"** (recomendado) e selecionar o repositório específico
5. Clicar **"Save"** ou **"Install"**

**Passo 4** — Criar categoria personalizada (opcional mas recomendado):
1. Acessar repositório → aba **Discussions**
2. Na sidebar esquerda, clicar ícone de **lápis** ao lado de "Categories"
3. Criar nova categoria (ex: "Blog Comments") com formato **Announcements**
4. Salvar categoria

### Fase 2: Configuração no giscus.app

**Passo 5** — Acessar **https://giscus.app/** e rolar até "Configuration"

**Passo 6** — Preencher campo Repository com formato `username/repo`:
- Aguardar checkmark verde ✅ de validação
- Se erro aparecer, verificar: repositório público? Discussions habilitadas? App instalado?

**Passo 7** — Selecionar Page ↔️ Discussions Mapping:
- Recomendação: **pathname** para portabilidade
- Marcar **"Use strict title matching"** para evitar conflitos

**Passo 8** — Selecionar Discussion Category no dropdown:
- Escolher categoria criada ou "Announcements"
- Marcar **"Only search for discussions in this category"**

**Passo 9** — Configurar Features:
- Marcar opções desejadas (lazy loading recomendado para performance)

**Passo 10** — Selecionar Theme:
- Recomendação: `preferred_color_scheme`

### Fase 3: Implementação

**Passo 11** — Copiar script da seção "Enable giscus":

```html
<script src="https://giscus.app/client.js"
        data-repo="username/repository"
        data-repo-id="R_kgDOK3lJcQ"
        data-category="Announcements"
        data-category-id="DIC_kwDOK3lJcc4Cbm3J"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="pt"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```

**Passo 12** — Adicionar ao template/HTML do site onde comentários devem aparecer:
- Opcionalmente adicionar container: `<section class="giscus"></section>`

---

## Formato dos IDs gerados

Os IDs são identificadores GraphQL do GitHub codificados em Base64:

- **data-repo-id**: Formato `R_kgDO...` (ex: `"R_kgDOK3lJcQ"`) ou formato legacy `"MDEwOlJlcG9zaXRvcnkzNTE5NTgwNTM="`
- **data-category-id**: Formato `DIC_kwDO...` (ex: `"DIC_kwDOK3lJcc4Cbm3J"`) ou formato legacy `"MDE4OkRpc2N1c3Npb25DYXRlZ29yeTMyNzk2NTc1"`

**Obtenção manual via GitHub GraphQL API** (alternativa ao giscus.app):
```graphql
query {
  repository(owner: "username", name: "repo") {
    id
    discussionCategories(first: 10) {
      edges { node { id name } }
    }
  }
}
```

---

## Erros comuns e soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Checkmark não aparece | Formato incorreto do repositório | Usar `username/repo`, não URL completa |
| "No categories found" | Discussions não habilitadas | Habilitar em Settings → Features |
| Widget não carrega | IDs faltando ou incorretos | Usar script completo do giscus.app |
| Erro 403 no widget | App não instalado | Instalar em github.com/apps/giscus |
| Comentários não aparecem | Repositório privado | Mudar para público |
| Discussion errada vinculada | Mapping ambíguo | Habilitar "strict title matching" |
| CSP blocking | Headers de segurança | Adicionar giscus.app às políticas frame-src, script-src |

---

## Conclusão

O configurador giscus.app oferece uma interface intuitiva que **valida automaticamente** os requisitos e **gera o script completo** com todos os IDs necessários. Os pontos críticos são: garantir repositório público, instalar o GitHub App, habilitar Discussions, e usar categoria **Announcements** para evitar spam. O dropdown de Discussion Category só aparece após validação bem-sucedida do repositório, servindo como indicador de que a configuração está correta. Para sites com dark mode, `preferred_color_scheme` adapta automaticamente, e `lazy loading` melhora significativamente a performance inicial da página.# Tutorial completo do configurador Giscus.app
<!-- Arquivo renomeado para: tutorial-configurador-giscus-app.md -->

O Giscus é um sistema de comentários gratuito e open-source alimentado pelo GitHub Discussions que permite adicionar uma seção de comentários a qualquer website. A configuração através do site giscus.app é feita via um **configurador interativo** que valida automaticamente seu repositório e gera o script de incorporação. Este guia documenta cada seção da interface, mensagens de validação e erros comuns.

---

## Interface completa do configurador em ordem de aparição

O configurador do giscus.app apresenta **7 seções principais** que aparecem sequencialmente na página. Cada seção deve ser preenchida na ordem correta, pois algumas dependem de validações anteriores.

### Seção 1: Language (Idioma)

A primeira seção permite selecionar o idioma da interface do widget Giscus. Aparece como um **dropdown** no topo da área de configuração. Suporta mais de **30 idiomas** incluindo Português, Inglês, Espanhol, Japonês, Chinês, entre outros. O idioma selecionado define o valor `data-lang` no script final.

### Seção 2: Repository (Repositório)

Esta é a seção mais crítica do configurador. Contém:

- **Campo de texto** com label "repository:" 
- **Texto auxiliar**: "A **public** GitHub repository. This repo is where the discussions will be linked to."
- **Lista de requisitos** exibida abaixo do campo:
  1. "The repository is **public**, otherwise visitors will not be able to view the discussion."
  2. "The **giscus** app is **installed**, otherwise visitors will not be able to comment and react."  
  3. "The **Discussions** feature is **turned on** by enabling it for your repository."

O formato correto para entrada é `username/repository-name` (exemplo: `pthurmond/patrickthurmond-comments`). **Não usar** URL completa como `https://github.com/username/repo`.

### Seção 3: Page ↔️ Discussions Mapping (Mapeamento)

Define como o Giscus encontra a Discussion correspondente a cada página. Apresenta **6 opções de radio buttons**:

| Opção | Descrição |
|-------|-----------|
| **pathname** | Título da Discussion contém o `pathname` da página (ex: `/blog/post-1`). **Recomendado** por ser portável e funcionar em localhost |
| **URL** | Título contém a URL completa da página |
| **title** | Título contém o conteúdo da tag `<title>` HTML |
| **og:title** | Título contém o valor da meta tag `og:title` |
| **specific** | Termo específico definido pelo usuário (revela campo de texto adicional) |
| **number** | Número específico de Discussion (revela campo numérico; não suporta criação automática) |

**Checkbox adicional**: "Use strict title matching" — quando marcado, usa hash SHA-1 para matching exato, evitando confusões com títulos similares. O valor `data-strict` será `"1"`.

### Seção 4: Discussion Category (Categoria de Discussion)

Esta seção **só aparece após validação bem-sucedida** do repositório na Seção 2.

**Localização visual**: Imediatamente abaixo da seção de Mapping.

**Elementos da interface**:
- **Label**: "Discussion Category"  
- **Dropdown/Select**: Lista todas as categorias de Discussions do repositório
- **Texto de recomendação**: "It is recommended to use a category with the **Announcements** type so that new discussions can only be created by maintainers and giscus."
- **Checkbox abaixo**: "Only search for discussions in this category"

**Categorias padrão do GitHub Discussions** (aparecem no dropdown):
- **Announcements** — Apenas mantenedores podem criar (recomendada)
- **General** — Discussão aberta
- **Ideas** — Compartilhar ideias
- **Q&A** — Formato pergunta e resposta
- **Show and tell** — Mostrar projetos

**Comportamento do dropdown**:
1. Se repositório inválido: dropdown desabilitado ou mostra "No categories found"
2. Se repositório válido: popula automaticamente com categorias disponíveis
3. Seleção define `data-category` e `data-category-id` no script

### Seção 5: Features (Funcionalidades)

Grupo de **4 checkboxes** para configurar comportamento do widget:

| Checkbox | Atributo | Descrição |
|----------|----------|-----------|
| "Enable reactions for the main post" | `data-reactions-enabled="1"` | Exibe reações antes dos comentários |
| "Emit discussion metadata" | `data-emit-metadata="1"` | Envia metadados para a janela pai via postMessage |
| "Place the comment box above the comments" | `data-input-position="top"` | Move caixa de input para cima |
| "Load the comments lazily" | `data-loading="lazy"` | Carrega apenas quando usuário rolar até o widget |

### Seção 6: Theme (Tema)

**Dropdown** com mais de **20 opções de tema**:

**Temas principais**:
- `light` / `dark` — Temas GitHub padrão
- `light_high_contrast` / `dark_high_contrast` — Alto contraste
- `dark_dimmed` — GitHub Dark Dimmed
- `preferred_color_scheme` — **Recomendado** (respeita preferência do usuário)
- `transparent_dark` — Fundo transparente escuro
- `noborder_light` / `noborder_dark` / `noborder_gray` — Sem bordas
- `cobalt` — RStudio Cobalt
- `purple_dark` — Roxo escuro
- `gruvbox` / `gruvbox_dark` / `gruvbox_light` — Família Gruvbox
- `catppuccin_latte` / `catppuccin_frappe` / `catppuccin_macchiato` / `catppuccin_mocha` — Família Catppuccin
- **Custom** — URL para CSS personalizado

### Seção 7: Enable giscus (Habilitar giscus)

A seção final contém o **código do script gerado** em um bloco de código copiável.

**Estados da seção**:
- **Incompleto**: Exibe mensagem "You have not configured your repository and/or category. The values for those fields will not show up until you fill them out."
- **Completo**: Exibe script completo com todos os valores preenchidos

---

## Mensagens de validação e indicadores visuais

### Validação bem-sucedida do repositório

Quando o repositório atende todos os critérios:
- **Indicador visual**: ✅ **Checkmark verde** aparece após o campo de texto do repositório
- **Comportamento**: O dropdown de Discussion Category torna-se ativo e populado
- **Script**: Seção "Enable giscus" mostra valores reais de `data-repo-id` e `data-category-id`

### Validação falha do repositório

Quando algum critério não é atendido:
- **Mensagem de erro**: **"Cannot use giscus on this repository. Make sure all of the above criteria has been met."**
- **Dropdown de categoria**: Mostra **"No categories found"**
- **Script**: Mantém placeholders `[ENTER REPO HERE]`, `[ENTER REPO ID HERE]`, etc.

### Erros de runtime (widget incorporado)

Quando o Giscus está no site mas encontra problemas:

| Erro | Mensagem | Causa |
|------|----------|-------|
| App não instalado | `"giscus is not installed on this repository"` (HTTP 403) | GitHub App não foi instalado no repositório |
| Discussion não encontrada | `"Discussion not found"` (HTTP 404) | Repositório privado, discussion deletada, ou mapping incorreto |
| Falha ao criar discussion | `"Unable to create discussion with request body"` | Categoria especificada não existe |
| Erro de CSP | `"giscus.app refused to connect"` | Content Security Policy bloqueia iframe |

---

## Processo completo de configuração passo a passo

### Fase 1: Preparação do repositório

**Passo 1** — Criar ou selecionar repositório público no GitHub. Recomendação: criar repositório dedicado com nome descritivo como `meusite-comments`.

**Passo 2** — Habilitar GitHub Discussions:
1. Acessar repositório → **Settings** (aba superior direita)
2. Rolar até seção **Features**
3. Marcar checkbox **"Discussions"**
4. Opcionalmente clicar "Set up discussions"

**Passo 3** — Instalar o Giscus GitHub App:
1. Acessar **https://github.com/apps/giscus**
2. Clicar botão **"Install"** ou **"Configure"**
3. Selecionar conta/organização
4. Escolher **"Only select repositories"** (recomendado) e selecionar o repositório específico
5. Clicar **"Save"** ou **"Install"**

**Passo 4** — Criar categoria personalizada (opcional mas recomendado):
1. Acessar repositório → aba **Discussions**
2. Na sidebar esquerda, clicar ícone de **lápis** ao lado de "Categories"
3. Criar nova categoria (ex: "Blog Comments") com formato **Announcements**
4. Salvar categoria

### Fase 2: Configuração no giscus.app

**Passo 5** — Acessar **https://giscus.app/** e rolar até "Configuration"

**Passo 6** — Preencher campo Repository com formato `username/repo`:
- Aguardar checkmark verde ✅ de validação
- Se erro aparecer, verificar: repositório público? Discussions habilitadas? App instalado?

**Passo 7** — Selecionar Page ↔️ Discussions Mapping:
- Recomendação: **pathname** para portabilidade
- Marcar **"Use strict title matching"** para evitar conflitos

**Passo 8** — Selecionar Discussion Category no dropdown:
- Escolher categoria criada ou "Announcements"
- Marcar **"Only search for discussions in this category"**

**Passo 9** — Configurar Features:
- Marcar opções desejadas (lazy loading recomendado para performance)

**Passo 10** — Selecionar Theme:
- Recomendação: `preferred_color_scheme`

### Fase 3: Implementação

**Passo 11** — Copiar script da seção "Enable giscus":

```html
<script src="https://giscus.app/client.js"
        data-repo="username/repository"
        data-repo-id="R_kgDOK3lJcQ"
        data-category="Announcements"
        data-category-id="DIC_kwDOK3lJcc4Cbm3J"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="pt"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```

**Passo 12** — Adicionar ao template/HTML do site onde comentários devem aparecer:
- Opcionalmente adicionar container: `<section class="giscus"></section>`

---

## Formato dos IDs gerados

Os IDs são identificadores GraphQL do GitHub codificados em Base64:

- **data-repo-id**: Formato `R_kgDO...` (ex: `"R_kgDOK3lJcQ"`) ou formato legacy `"MDEwOlJlcG9zaXRvcnkzNTE5NTgwNTM="`
- **data-category-id**: Formato `DIC_kwDO...` (ex: `"DIC_kwDOK3lJcc4Cbm3J"`) ou formato legacy `"MDE4OkRpc2N1c3Npb25DYXRlZ29yeTMyNzk2NTc1"`

**Obtenção manual via GitHub GraphQL API** (alternativa ao giscus.app):
```graphql
query {
  repository(owner: "username", name: "repo") {
    id
    discussionCategories(first: 10) {
      edges { node { id name } }
    }
  }
}
```

---

## Erros comuns e soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Checkmark não aparece | Formato incorreto do repositório | Usar `username/repo`, não URL completa |
| "No categories found" | Discussions não habilitadas | Habilitar em Settings → Features |
| Widget não carrega | IDs faltando ou incorretos | Usar script completo do giscus.app |
| Erro 403 no widget | App não instalado | Instalar em github.com/apps/giscus |
| Comentários não aparecem | Repositório privado | Mudar para público |
| Discussion errada vinculada | Mapping ambíguo | Habilitar "strict title matching" |
| CSP blocking | Headers de segurança | Adicionar giscus.app às políticas frame-src, script-src |

---

## Conclusão

O configurador giscus.app oferece uma interface intuitiva que **valida automaticamente** os requisitos e **gera o script completo** com todos os IDs necessários. Os pontos críticos são: garantir repositório público, instalar o GitHub App, habilitar Discussions, e usar categoria **Announcements** para evitar spam. O dropdown de Discussion Category só aparece após validação bem-sucedida do repositório, servindo como indicador de que a configuração está correta. Para sites com dark mode, `preferred_color_scheme` adapta automaticamente, e `lazy loading` melhora significativamente a performance inicial da página.