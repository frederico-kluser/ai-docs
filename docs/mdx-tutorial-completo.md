# Tutorial Completo de MDX: Markdown com Superpoderes de JSX

**MDX é uma tecnologia revolucionária que une a simplicidade do Markdown com o poder dos componentes React**, permitindo criar conteúdo interativo e dinâmico para documentação, blogs e sites. Criado por John Otander em 2017 e mantido pelo ecossistema unified, o MDX evoluiu através de três versões principais, culminando na **v3 (outubro 2023)** que oferece suporte a ES2024, sintaxe `await` e melhor integração com bundlers modernos. Este tutorial abrange desde fundamentos até casos avançados, fornecendo exemplos práticos para implementação imediata.

---

## Fundamentos: entendendo o que é MDX e sua arquitetura

MDX permite escrever JSX diretamente em documentos Markdown, possibilitando importar componentes como gráficos interativos, alertas e widgets, incorporando-os naturalmente ao conteúdo. A motivação original era resolver limitações do Markdown tradicional: **ausência de componentes reutilizáveis**, impossibilidade de incluir elementos interativos, e dificuldade em criar documentação "viva" com exemplos executáveis.

### Evolução das versões v1, v2 e v3

| Característica | v1 (Abril 2019) | v2 (Fevereiro 2022) | v3 (Outubro 2023) |
|----------------|-----------------|---------------------|-------------------|
| **Módulos** | CommonJS | ESM exclusivo | ESM (Node 16+) |
| **JSX Runtime** | Apenas React | Qualquer runtime | Automático (clássico depreciado) |
| **GFM** | Integrado | Plugin necessário | Plugin necessário |
| **Expressões JS** | Limitadas | Suporte completo | ES2024, suporte a `await` |
| **Performance** | Base | 25% mais rápido, bundles 250% menores | Código gerado mais limpo |
| **TypeScript** | Não | JSDoc types | Types completos |

A **v2 foi uma reescrita quase completa**, introduzindo suporte a qualquer runtime JSX (React, Preact, Vue), eliminando a necessidade de linhas em branco entre JSX e Markdown, e migrando completamente para ES Modules. A **v3 é um "major pequeno"** focado em refinamentos: suporte a `await`, adjacência de expressões JSX, e depreciação do runtime clássico.

### Como funciona o compilador MDX

O MDX utiliza um **pipeline unified** que transforma o código fonte através de múltiplas representações AST:

```
MDX Source → Parse (micromark) → mdast → remark plugins → 
           → hast (via remark-rehype) → rehype plugins → 
           → esast (via rehype-recma) → JavaScript
```

O processo começa com **micromark** parseando a sintaxe MDX em mdast (Markdown Abstract Syntax Tree). Plugins remark transformam a estrutura Markdown. O **remark-rehype** converte para hast (HTML AST), onde plugins rehype atuam. Finalmente, **rehype-recma** gera esast (ECMAScript AST), produzindo JavaScript executável.

**Exemplo de compilação:**

```mdx
import {Chart} from './chart.js'
export const year = 2024

# Dados de {year}
<Chart year={year} color="#fcb32c" />
```

Compila para:

```javascript
import {jsx as _jsx, jsxs as _jsxs} from 'react/jsx-runtime'
import {Chart} from './chart.js'

export const year = 2024

function _createMdxContent(props) {
  const _components = {h1: 'h1', ...props.components}
  return _jsxs(_Fragment, {
    children: [
      _jsx(_components.h1, {children: ["Dados de ", year]}),
      _jsx(Chart, {year: year, color: "#fcb32c"})
    ]
  })
}

export default function MDXContent(props = {}) {
  return _createMdxContent(props)
}
```

### Ecossistema unified, remark e rehype

O **unified** é a interface central para processamento de conteúdo com syntax trees. O **remark** processa Markdown (mdast), enquanto **rehype** processa HTML (hast). Pacotes-chave do MDX incluem:

- **@mdx-js/mdx**: Compilador core (`compile`, `evaluate`, `createProcessor`)
- **@mdx-js/loader**: Integração webpack
- **@mdx-js/rollup**: Plugin Rollup/Vite
- **@mdx-js/esbuild**: Plugin esbuild
- **@mdx-js/react**: Context provider React (opcional)
- **remark-mdx**: Adiciona sintaxe MDX ao remark

---

## Configuração e setup com diferentes ambientes

### Instalação de pacotes essenciais

```bash
# Core MDX
npm install @mdx-js/mdx

# React runtime (opcional, para MDXProvider)
npm install @mdx-js/react

# TypeScript types
npm install @types/mdx

# Plugins comuns
npm install remark-gfm remark-frontmatter rehype-slug rehype-highlight
```

### Configuração por bundler

**Vite** (usando @mdx-js/rollup):

```javascript
// vite.config.js
import mdx from '@mdx-js/rollup'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    // IMPORTANTE: enforce 'pre' com @vitejs/plugin-react
    { enforce: 'pre', ...mdx({ /* options */ }) },
    react({ include: /\.(jsx|js|mdx|md|tsx|ts)$/ })
  ]
})
```

**Webpack** (usando @mdx-js/loader):

```javascript
// webpack.config.js
export default {
  module: {
    rules: [{
      test: /\.mdx?$/,
      use: [
        { loader: 'babel-loader', options: {} },
        {
          loader: '@mdx-js/loader',
          options: {
            jsxImportSource: 'react',
            remarkPlugins: [],
            rehypePlugins: []
          }
        }
      ]
    }]
  }
}
```

**esbuild**:

```javascript
import mdx from '@mdx-js/esbuild'
import esbuild from 'esbuild'

await esbuild.build({
  entryPoints: ['index.mdx'],
  format: 'esm',
  outfile: 'output.js',
  plugins: [mdx({ jsxImportSource: 'react' })]
})
```

### Integração com frameworks populares

**Next.js** (App Router):

```javascript
// next.config.mjs
import createMDX from '@next/mdx'
import remarkGfm from 'remark-gfm'

const nextConfig = {
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
}

const withMDX = createMDX({
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [],
  }
})

export default withMDX(nextConfig)
```

Arquivo obrigatório `mdx-components.tsx` na raiz:

```typescript
import type { MDXComponents } from 'mdx/types'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => <h1 className="text-4xl font-bold">{children}</h1>,
    ...components,
  }
}
```

**Astro**:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import remarkGfm from 'remark-gfm'

export default defineConfig({
  integrations: [
    mdx({
      remarkPlugins: [remarkGfm],
      extendMarkdownConfig: true,
    })
  ],
})
```

**Gatsby**:

```javascript
// gatsby-config.mjs
import remarkGfm from "remark-gfm"
import rehypeSlug from "rehype-slug"

const config = {
  plugins: [{
    resolve: `gatsby-plugin-mdx`,
    options: {
      mdxOptions: {
        remarkPlugins: [remarkGfm],
        rehypePlugins: [rehypeSlug],
      },
    },
  }],
}

export default config
```

### Configuração TypeScript

Crie o arquivo de declaração `mdx.d.ts`:

```typescript
// src/types/mdx.d.ts
declare module '*.mdx' {
  let MDXComponent: (props: any) => JSX.Element;
  export default MDXComponent;
}
```

Atualize `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["react", "react-dom", "mdx"],
    "jsx": "react-jsx"
  },
  "include": ["src", "src/types"]
}
```

Para IDE, instale a extensão **mdx-js/mdx-analyzer** no VS Code.

---

## Sintaxe e features: dominando a escrita MDX

### Markdown padrão e diferenças importantes

MDX suporta CommonMark com algumas **diferenças críticas**:

| Feature | Markdown Padrão | MDX |
|---------|-----------------|-----|
| Blocos de código indentados | ✅ Funciona | ❌ Não suportado |
| Autolinks `<http://...>` | ✅ Funciona | ❌ Conflita com JSX |
| Comentários HTML | `<!-- -->` | `{/* comentário */}` |
| Caracteres `<` e `{` | Livres | Devem ser escapados: `\<` ou `\{` |

Para habilitar **GitHub Flavored Markdown** (tabelas, strikethrough, task lists), instale `remark-gfm`:

```javascript
remarkPlugins: [remarkGfm]
```

### Importação e uso de componentes React

```mdx
import { Alert } from './Alert'
import Chart from './Chart'

# Meu Artigo

Conteúdo regular em Markdown aqui.

<Alert type="warning">
  Isso é um alerta personalizado!
</Alert>

<Chart 
  data={[1, 2, 3, 4]} 
  color="blue" 
  showLegend={true}
/>
```

**Para Markdown funcionar dentro de JSX**, o conteúdo precisa estar em linhas separadas com linhas em branco:

```mdx
{/* ✅ Correto - Markdown É parseado */}
<div>

Este é um `parágrafo` com **formatação**.

</div>

{/* ❌ Incorreto - Markdown NÃO é parseado */}
<div>Este é um `parágrafo` literal.</div>
```

### Exportação de dados e metadados

```mdx
export const metadata = {
  title: 'Meu Post',
  date: '2024-06-01',
  tags: ['react', 'mdx']
}

export const formatDate = (d) => new Date(d).toLocaleDateString('pt-BR')

# {metadata.title}

Publicado em {formatDate(metadata.date)}
```

Acesso em outros arquivos:

```jsx
import Post, { metadata } from './post.mdx'

function BlogPage() {
  return (
    <article>
      <h1>{metadata.title}</h1>
      <Post />
    </article>
  )
}
```

### Expressões JavaScript inline

```mdx
export const items = ['Maçã', 'Banana', 'Cereja']
export const count = 5

{/* Cálculos */}
Dois mais dois é {2 + 2}.

{/* Métodos */}
Pi é aproximadamente {Math.PI.toFixed(4)}.

{/* Condicionais */}
{count > 0 && <p>Você tem {count} itens</p>}

{/* Mapeamento */}
<ul>
  {items.map((item, i) => <li key={i}>{item}</li>)}
</ul>
```

**Limitação importante**: Apenas **expressões** são permitidas, não statements:

```mdx
{/* ❌ ERRADO - statements */}
{if (x) { return <p>Oi</p> }}

{/* ✅ CORRETO - expressões */}
{x && <p>Oi</p>}
{x ? <ComponenteA /> : <ComponenteB />}
```

### MDXProvider e mapeamento de componentes

O **MDXProvider** permite sobrescrever elementos HTML globalmente:

```jsx
import { MDXProvider } from '@mdx-js/react'

const components = {
  h1: props => <h1 className="text-4xl font-bold" {...props} />,
  h2: props => <h2 className="text-2xl" {...props} />,
  a: props => <a className="text-blue-500 hover:underline" {...props} />,
  pre: props => <pre className="bg-gray-900 p-4 rounded" {...props} />,
  code: props => <code className="bg-gray-100 px-1 rounded" {...props} />,
  
  // Componentes customizados (shortcodes)
  Alert: AlertComponent,
  YouTube: YouTubeEmbed,
}

function App({ children }) {
  return (
    <MDXProvider components={components}>
      {children}
    </MDXProvider>
  )
}
```

**Shortcodes** ficam disponíveis globalmente sem imports:

```mdx
# Meu Post

<Alert type="info">
  Nenhum import necessário!
</Alert>

<YouTube id="dQw4w9WgXcQ" />
```

---

## Casos de uso avançados: recursos profissionais

### Syntax highlighting com Shiki (abordagem moderna)

Shiki usa o mesmo motor TextMate do VS Code, oferecendo highlighting preciso em tempo de compilação:

```bash
npm install rehype-pretty-code shiki
```

```javascript
import rehypePrettyCode from 'rehype-pretty-code'

const mdxOptions = {
  rehypePlugins: [[rehypePrettyCode, {
    theme: 'github-dark',
    // Ou temas duais para light/dark mode:
    // theme: { dark: 'github-dark', light: 'github-light' }
  }]],
}
```

**Recursos avançados** (sintaxe meta):

````markdown
```js {1,4-5} title="exemplo.js"
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)  // Esta linha destacada
  return <button>{count}</button>        // Esta também
}
```
````

### Renderização matemática com KaTeX

```bash
npm install remark-math rehype-katex katex
```

```javascript
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'

const mdxOptions = {
  remarkPlugins: [remarkMath],
  rehypePlugins: [rehypeKatex], // ANTES de syntax highlighters
}
```

Adicione o CSS no layout:

```javascript
import 'katex/dist/katex.min.css'
```

Uso no MDX:

```mdx
Inline: $E = mc^2$

Bloco:
$$
L = \frac{1}{2} \rho v^2 S C_L
$$
```

**KaTeX vs MathJax**: KaTeX é **10x mais rápido** e produz bundles menores. Prefira KaTeX a menos que precise de recursos LaTeX avançados.

### Diagramas com Mermaid

**Opção A - Server-side** (rehype-mermaid, requer Playwright):

```bash
npm install rehype-mermaid playwright
npx playwright install --with-deps chromium
```

```javascript
import rehypeMermaid from 'rehype-mermaid'

const mdxOptions = {
  rehypePlugins: [[rehypeMermaid, { strategy: 'inline-svg' }]],
}
```

**Opção B - Client-side** (componente customizado):

```jsx
// components/Mermaid.tsx
import mermaid from 'mermaid'
import { useEffect, useRef } from 'react'

export function Mermaid({ chart }) {
  const ref = useRef(null)
  
  useEffect(() => {
    mermaid.initialize({ startOnLoad: true, theme: 'default' })
    mermaid.contentLoaded()
  }, [])
  
  return <pre className="mermaid" ref={ref}>{chart}</pre>
}
```

### Frontmatter YAML

```bash
npm install remark-frontmatter remark-mdx-frontmatter
```

```javascript
import remarkFrontmatter from 'remark-frontmatter'
import remarkMdxFrontmatter from 'remark-mdx-frontmatter'

const mdxOptions = {
  remarkPlugins: [
    remarkFrontmatter,
    [remarkMdxFrontmatter, { name: 'frontmatter' }]
  ],
}
```

O frontmatter YAML é convertido em export:

```mdx
---
title: Meu Post
date: 2024-06-01
tags: ["react", "mdx"]
---

# {frontmatter.title}
```

### MDX Remoto (next-mdx-remote)

Para conteúdo de CMS ou banco de dados:

```bash
npm install next-mdx-remote
```

**App Router (RSC)**:

```typescript
import { MDXRemote } from 'next-mdx-remote/rsc'
import remarkGfm from 'remark-gfm'

export default async function Page() {
  const markdown = await fetch('https://cms.example.com/post').then(r => r.text())
  
  return (
    <MDXRemote
      source={markdown}
      options={{
        parseFrontmatter: true,
        mdxOptions: {
          remarkPlugins: [remarkGfm],
        },
      }}
      components={components}
    />
  )
}
```

**⚠️ AVISO DE SEGURANÇA CRÍTICO**: MDX compila para JavaScript e executa no servidor. **NUNCA compile MDX de fontes não confiáveis**. Isso equivale a executar `eval()` em input do usuário, permitindo **Remote Code Execution (RCE)**.

---

## Boas práticas: organização, performance e segurança

### Estrutura de arquivos recomendada

```
project/
├── content/           # Arquivos MDX
│   ├── docs/         
│   │   ├── getting-started.mdx
│   │   └── api-reference.mdx
│   └── blog/
│       └── meu-post.mdx
├── components/        
│   ├── mdx/          # Componentes específicos para MDX
│   │   ├── CodeBlock.tsx
│   │   ├── Callout.tsx
│   │   └── index.ts  # Barrel export
│   └── ui/           # Componentes UI gerais
├── lib/              # Utilitários MDX
└── layouts/          # Layouts para páginas MDX
```

Use **kebab-case** para arquivos MDX (`getting-started.mdx`) e **PascalCase** para componentes (`CodeBlock.tsx`).

### Otimização de performance

Prefira **compilação em build-time** ao invés de runtime - não há impacto de performance no cliente. Use code splitting para componentes pesados:

```jsx
import { lazy, Suspense } from 'react'

const HeavyChart = lazy(() => import('./HeavyChart'))

// No MDXProvider
const components = {
  Chart: (props) => (
    <Suspense fallback={<div>Carregando...</div>}>
      <HeavyChart {...props} />
    </Suspense>
  )
}
```

### Segurança com conteúdo de usuários

Para conteúdo de usuários, **use Markdown comum** ao invés de MDX:

```jsx
import ReactMarkdown from 'react-markdown'

// Seguro para conteúdo de usuários
<ReactMarkdown>{userContent}</ReactMarkdown>
```

Se MDX for necessário, use **safe-mdx** que não executa JavaScript:

```jsx
import { SafeMdxRenderer } from 'safe-mdx'

<SafeMdxRenderer 
  markdown={code} 
  components={allowedComponents} 
/>
```

### Testing de conteúdo MDX

Configure Jest para transformar MDX:

```javascript
// jest.config.js
module.exports = {
  transform: {
    '^.+\\.mdx?$': '@storybook/addon-docs/jest-transform-mdx'
  }
}
```

Snapshot testing:

```jsx
import renderer from 'react-test-renderer'
import MyContent from './content.mdx'

test('MDX renderiza corretamente', () => {
  const tree = renderer.create(<MyContent />).toJSON()
  expect(tree).toMatchSnapshot()
})
```

### Acessibilidade

Mantenha **hierarquia de headings correta** (não pule níveis), use **alt text descritivo** em imagens, e evite links genéricos como "clique aqui":

```mdx
{/* ✅ Correto */}
Leia o [guia completo de migração](/docs/migration) para detalhes.

{/* ❌ Evitar */}
Para mais informações, [clique aqui](/docs/migration).
```

---

## Exemplos práticos: implementações completas

### Blog técnico com Next.js

```typescript
// app/blog/[slug]/page.tsx
import { MDXRemote } from 'next-mdx-remote/rsc'
import { readFile } from 'fs/promises'
import path from 'path'
import remarkGfm from 'remark-gfm'
import rehypePrettyCode from 'rehype-pretty-code'

export default async function BlogPost({ params }) {
  const filePath = path.join(process.cwd(), 'content/blog', `${params.slug}.mdx`)
  const source = await readFile(filePath, 'utf-8')
  
  return (
    <article className="prose prose-lg mx-auto">
      <MDXRemote
        source={source}
        options={{
          parseFrontmatter: true,
          mdxOptions: {
            remarkPlugins: [remarkGfm],
            rehypePlugins: [[rehypePrettyCode, { theme: 'github-dark' }]],
          },
        }}
        components={components}
      />
    </article>
  )
}
```

### Documentação com Docusaurus

```mdx
---
title: Getting Started
sidebar_position: 1
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Getting Started

<Tabs>
  <TabItem value="npm" label="npm">
    ```bash
    npm install meu-pacote
    ```
  </TabItem>
  <TabItem value="yarn" label="Yarn">
    ```bash
    yarn add meu-pacote
    ```
  </TabItem>
</Tabs>
```

### Apresentações com MDX Deck

```bash
npm install mdx-deck
```

```mdx
// slides.mdx
import { yellow } from '@mdx-deck/themes'
export const theme = yellow

# Minha Apresentação

---

## Slide 2

- Ponto importante
- Outro ponto

<Notes>
Notas do apresentador - visíveis apenas no modo apresentador
</Notes>

---

<Steps>
  <Step>Primeiro ponto aparece</Step>
  <Step>Depois este</Step>
  <Step>Por fim este</Step>
</Steps>
```

Execute com `npx mdx-deck slides.mdx`.

---

## Troubleshooting: erros comuns e soluções

### Erro "require() of ES Module not supported"

**Causa**: Mistura de ESM e CommonJS.

**Soluções**:
1. Adicione `"type": "module"` ao `package.json`
2. Use extensão `.mjs` para arquivos de configuração
3. Use imports dinâmicos: `const mdx = await import('@mdx-js/mdx')`

### Erro "Cannot use import statement"

**Causa**: Projeto não está configurado para ESM.

**Solução**: Configure o projeto consistentemente como ESM ou CommonJS. Para Next.js/Vite, use `.mjs` para configs.

### Erro "Could not parse import/exports with acorn"

**Causa**: JavaScript inválido após palavras-chave `import` ou `export`.

**Solução**: Verifique se statements import/export são JavaScript válido. Não inicie parágrafos com as palavras "import" ou "export".

### Erro "Unexpected character, expected expression"

**Causa**: Caracteres `<` ou `{` não escapados.

**Solução**:
```mdx
{/* Escape caracteres especiais */}
A sintaxe é \{expressão\} ou \<Componente\>

{/* Ou use expressões */}
A sintaxe é {'{'} expressão {'}'} ou {'<'} Componente {'>'}
```

### Checklist de migração v2 para v3

- [ ] Atualize Node.js para 16+
- [ ] Passe opção `baseUrl` ao usar `evaluate`, `run`, ou `outputFormat: 'function-body'`
- [ ] Remova opção `useDynamicImport` (agora comportamento padrão)
- [ ] Migre do runtime JSX clássico para automático
- [ ] Atualize plugins remark/rehype para versões mais recentes
- [ ] Substitua `MDXContext` e `withMDXComponents` depreciados por `useMDXComponents`

---

## Conclusão: MDX como ferramenta de produtividade

MDX representa uma evolução significativa na criação de conteúdo, unindo a **simplicidade do Markdown** com a **flexibilidade de componentes React**. Com a v3 estável e um ecossistema robusto de plugins, é possível criar desde blogs simples até sistemas de documentação interativa complexos.

As **melhores práticas essenciais** incluem: preferir compilação em build-time para performance máxima, nunca compilar MDX não confiável por questões de segurança, manter separação clara entre conteúdo e lógica, e usar o MDXProvider para componentes globais. Para projetos novos, considere frameworks como **Nextra** (Next.js), **Docusaurus** (documentação), ou **Astro** (sites estáticos) que oferecem integração MDX pronta para uso.

O **playground oficial** em mdxjs.com/playground é recurso essencial para debugging e experimentação. A documentação oficial permanece a fonte mais confiável e atualizada para referência de APIs e guias de migração entre versões.