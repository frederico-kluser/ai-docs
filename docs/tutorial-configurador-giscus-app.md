---
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

... (continua)