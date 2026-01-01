# Guia Definitivo Motion+ - Documentação Completa em Português Brasileiro

O Motion+ (anteriormente Framer Motion) é o framework de animação mais poderoso para React, oferecendo **animações declarativas**, gestos avançados, animações de layout e componentes premium exclusivos. Este guia abrangente cobre **todas as APIs, hooks, componentes e padrões** necessários para dominar animações web profissionais, desde instalação básica até técnicas avançadas de otimização de performance.

---

## Parte 1: Primeiros passos

### Instalação e configuração inicial

O Motion pode ser instalado via qualquer gerenciador de pacotes JavaScript. A biblioteca requer **React 18.2 ou superior**.

```bash
# npm
npm install motion

# Yarn
yarn add motion

# pnpm
pnpm add motion
```

**Para Vue.js:**
```bash
npm install motion-v
```

**Via CDN (jsDelivr):**
```html
<script type="module">
  import motion from "https://cdn.jsdelivr.net/npm/motion@latest/react/+esm"
</script>
```

### Importação correta para cada ambiente

A importação varia conforme seu ambiente de desenvolvimento. Para **React padrão**, use a importação direta:

```typescript
import { motion } from "motion/react"
```

Para **Next.js App Router com Server Components**, existem duas abordagens. A primeira adiciona a diretiva `"use client"` no topo do arquivo. A segunda, mais otimizada para bundle size, utiliza a importação específica para client:

```typescript
// Opção 1: Diretiva use client
"use client"
import { motion } from "motion/react"

// Opção 2: Bundle menor, sem diretiva necessária
import * as motion from "motion/react-client"
```

**Para Vue:**
```typescript
import { motion } from "motion-v"
```

**Para JavaScript Vanilla:**
```typescript
import { animate } from "motion"
```

### Motion gratuito vs Motion+ Premium

O Motion oferece uma versão gratuita robusta e uma versão premium com pagamento único de **$299**. A diferença fundamental está nos componentes exclusivos e recursos avançados.

| Recurso | Motion Gratuito | Motion+ Premium |
|---------|-----------------|-----------------|
| Componentes de animação core | ✅ | ✅ |
| Exemplos disponíveis | 80+ | 330+ |
| Tutoriais | 20+ | 40+ |
| APIs Premium (Carousel, Ticker) | ❌ | ✅ |
| Comunidade Discord privada | ❌ | ✅ |
| Acesso ao repositório GitHub privado | ❌ | ✅ |
| VS Code Bezier Editor | ❌ | ✅ |
| Early access a novos recursos | ❌ | ✅ |

**Componentes exclusivos Motion+:**
- **Carousel** - Carrossel infinito performático (+5.5kb)
- **Ticker** - Marquee infinito animado (+2.1kb)
- **AnimateNumber** - Animação de números/contadores (+2.5kb)
- **splitText** - Divisão de texto em caracteres/palavras (+0.7kb)
- **Typewriter** - Efeito de digitação natural
- **Cursor** - Cursores customizados animados

### Configuração TypeScript

O Motion possui tipagem TypeScript nativa. Para componentes motion customizados, utilize `HTMLMotionProps`:

```typescript
import { motion, HTMLMotionProps } from "motion/react"

type MotionDivProps = HTMLMotionProps<"div">

const AnimatedCard: React.FC<MotionDivProps> = (props) => {
  return <motion.div {...props} />
}
```

### Otimização de bundle com LazyMotion

Para aplicações onde bundle size é crítico, utilize `LazyMotion` com componentes `m` em vez de `motion`:

```typescript
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

function App({ children }) {
  return (
    <LazyMotion features={domAnimation}>
      <m.div animate={{ opacity: 1 }} />
    </LazyMotion>
  )
}
```

**Pacotes de features disponíveis:**
- `domAnimation`: Animações básicas, variants, exit, gestos (~16kb)
- `domMax`: Feature set completo incluindo layout animations (~27kb)

---

## Parte 2: Fundamentos

### Componentes Motion e elementos HTML/SVG

O Motion fornece um componente animável para **cada elemento HTML e SVG**. Estes componentes aceitam todas as props nativas do elemento mais props de animação especiais.

```typescript
// Elementos HTML
<motion.div />
<motion.span />
<motion.button />
<motion.input />
<motion.nav />
<motion.ul />
<motion.li />
<motion.section />
<motion.article />

// Elementos SVG
<motion.svg />
<motion.path />
<motion.circle />
<motion.rect />
<motion.line />
<motion.g />
```

**Criando componentes motion customizados:**

```typescript
import { motion } from "motion/react"
import { forwardRef } from "react"

// Componente deve usar forwardRef
const MyButton = forwardRef((props, ref) => (
  <button ref={ref} {...props} />
))

const MotionButton = motion.create(MyButton)

// Uso
<MotionButton whileHover={{ scale: 1.1 }} />
```

### A prop `animate` - API completa

A prop `animate` define o estado alvo da animação. O Motion automaticamente anima entre valores quando eles mudam.

```typescript
// Objeto de valores
<motion.div animate={{ x: 100, opacity: 1 }} />

// Array de keyframes
<motion.div animate={{ x: [0, 100, 50, 100] }} />

// Label de variant
<motion.div animate="visible" variants={variants} />

// Múltiplos variants
<motion.div animate={["visible", "highlighted"]} />
```

### Props de animação fundamentais

| Prop | Tipo | Descrição |
|------|------|-----------|
| `initial` | `boolean \| Target \| VariantLabels` | Estado inicial antes da animação |
| `animate` | `Target \| VariantLabels` | Estado alvo da animação |
| `exit` | `Target \| VariantLabels` | Animação ao remover do DOM |
| `transition` | `Transition` | Configuração da transição |
| `variants` | `Variants` | Objeto de estados nomeados |

**Exemplos práticos:**

```typescript
// Animação de entrada
<motion.div
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
/>

// Desabilitar animação inicial
<motion.div initial={false} animate={{ x: 100 }} />

// Com variantes
const cardVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1 }
}

<motion.div
  variants={cardVariants}
  initial="hidden"
  animate="visible"
/>
```

### Propriedades CSS animáveis

O Motion pode animar praticamente qualquer propriedade CSS, mas oferece **propriedades de transform independentes** para melhor controle:

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `x`, `y`, `z` | `number \| string` | Translação |
| `scale`, `scaleX`, `scaleY` | `number` | Escala |
| `rotate`, `rotateX`, `rotateY`, `rotateZ` | `number \| string` | Rotação |
| `skew`, `skewX`, `skewY` | `number \| string` | Inclinação |
| `originX`, `originY` | `number (0-1)` | Origem do transform |

**Propriedades SVG especiais:**
- `pathLength`: 0-1, quanto do path é desenhado
- `pathSpacing`: Espaçamento de dash
- `pathOffset`: Offset do início do dash

**Tipos de valores suportados:**
- Números: `100`, `1.5`, `0`
- Strings com unidades: `"50%"`, `"100vh"`, `"calc(100vw - 50px)"`
- Cores: Hex, RGB, RGBA, HSL, HSLA
- `"auto"` para height/width

### Sistema de Variants - Orquestração pai-filho

Variants são objetos que definem estados de animação nomeados. Eles **propagam automaticamente** para componentes motion filhos.

```typescript
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

function List({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

**Propriedades de orquestração:**

| Propriedade | Tipo | Padrão | Descrição |
|-------------|------|--------|-----------|
| `when` | `"beforeChildren" \| "afterChildren" \| false` | `false` | Ordem relativa aos filhos |
| `delayChildren` | `number` | `0` | Delay antes dos filhos |
| `staggerChildren` | `number` | `0` | Intervalo entre cada filho |
| `staggerDirection` | `1 \| -1` | `1` | Direção do stagger |

**Variants dinâmicos com funções:**

```typescript
const itemVariants = {
  hidden: { opacity: 0 },
  visible: (custom: number) => ({
    opacity: 1,
    transition: { delay: custom * 0.1 }
  })
}

// Uso com prop custom
{items.map((item, i) => (
  <motion.div
    key={item.id}
    custom={i}
    variants={itemVariants}
  />
))}
```

### Transições - Spring, Tween e Inertia

O Motion oferece três tipos de transição: **spring** (física de mola), **tween** (baseada em duração) e **inertia** (desaceleração).

#### Transições Spring (Padrão)

Springs são o tipo padrão para a maioria das animações, proporcionando movimento natural.

**Springs baseadas em duração:**

```typescript
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: "spring",
    duration: 0.8,
    bounce: 0.4  // 0-1, quantidade de bounce
  }}
/>
```

**Springs baseadas em física:**

```typescript
<motion.div
  animate={{ scale: 1.2 }}
  transition={{
    type: "spring",
    stiffness: 400,  // Rigidez da mola (padrão: 100)
    damping: 25,     // Resistência (padrão: 10)
    mass: 1,         // Massa do objeto (padrão: 1)
    velocity: 0      // Velocidade inicial
  }}
/>
```

#### Transições Tween

Animações baseadas em duração e curvas de easing.

```typescript
<motion.div
  animate={{ opacity: 1 }}
  transition={{
    type: "tween",
    duration: 0.5,
    ease: "easeInOut"
  }}
/>
```

**Funções de easing disponíveis:**
- `"linear"`
- `"easeIn"`, `"easeOut"`, `"easeInOut"`
- `"circIn"`, `"circOut"`, `"circInOut"`
- `"backIn"`, `"backOut"`, `"backInOut"`
- `"anticipate"`
- Cubic bezier: `[0.17, 0.67, 0.83, 0.67]`
- Função customizada: `(t) => t * t`

#### Transições Inertia

Usadas principalmente para drag, simulam desaceleração natural.

```typescript
<motion.div
  drag
  dragTransition={{
    power: 0.3,
    timeConstant: 200,
    modifyTarget: target => Math.round(target / 50) * 50,
    min: 0,
    max: 500
  }}
/>
```

#### Configurações por propriedade

```typescript
<motion.div
  animate={{ x: 100, opacity: 1 }}
  transition={{
    default: { type: "spring" },
    opacity: { duration: 0.3, ease: "linear" }
  }}
/>
```

### Keyframes

Keyframes permitem animações multi-step:

```typescript
// Keyframes simples
<motion.div animate={{ x: [0, 100, 50, 100] }} />

// Keyframe wildcard (usa valor atual)
<motion.div animate={{ x: [null, 100, 0] }} />

// Com controle de timing
<motion.div
  animate={{
    x: [0, 100, 200],
    transition: {
      duration: 3,
      times: [0, 0.2, 1],  // Posições 0%, 20%, 100%
      ease: ["easeIn", "easeOut"]
    }
  }}
/>
```

### Repetição de animações

```typescript
<motion.div
  animate={{ rotate: 360 }}
  transition={{
    duration: 2,
    repeat: Infinity,        // ou número específico
    repeatType: "reverse",   // "loop" | "reverse" | "mirror"
    repeatDelay: 0.5
  }}
/>
```

---

## Parte 3: Sistema de Gestos

### Gestos de drag

O sistema de drag do Motion é completo e altamente configurável.

```typescript
// Drag em ambas direções
<motion.div drag />

// Drag apenas horizontal ou vertical
<motion.div drag="x" />
<motion.div drag="y" />

// Com animação durante drag
<motion.div
  drag
  whileDrag={{ scale: 1.1, boxShadow: "0px 10px 20px rgba(0,0,0,0.2)" }}
/>
```

**Props de drag completas:**

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `drag` | `boolean \| "x" \| "y"` | `false` | Habilita drag |
| `dragConstraints` | `object \| RefObject` | - | Limites do drag |
| `dragElastic` | `number \| object \| false` | `0.5` | Elasticidade fora dos limites |
| `dragMomentum` | `boolean` | `true` | Aplica inércia ao soltar |
| `dragSnapToOrigin` | `boolean` | `false` | Retorna à origem ao soltar |
| `dragDirectionLock` | `boolean` | `false` | Trava no primeiro eixo detectado |
| `dragPropagation` | `boolean` | `false` | Propaga para filhos |
| `dragControls` | `DragControls` | - | Controle programático |
| `dragListener` | `boolean` | `true` | Responde a eventos de pointer |

**Constraints por referência:**

```typescript
function DragContainer() {
  const constraintsRef = useRef(null)

  return (
    <motion.div ref={constraintsRef} style={{ width: 300, height: 200 }}>
      <motion.div
        drag
        dragConstraints={constraintsRef}
        dragElastic={0.1}
      />
    </motion.div>
  )
}
```

**Controle programático com useDragControls:**

```typescript
import { motion, useDragControls } from "motion/react"

function Scrubber() {
  const dragControls = useDragControls()

  return (
    <>
      <div
        onPointerDown={(e) => dragControls.start(e, { snapToCursor: true })}
        style={{ touchAction: "none" }}
      >
        Arraste aqui
      </div>
      <motion.div
        drag="x"
        dragControls={dragControls}
        dragListener={false}
      />
    </>
  )
}
```

**Callbacks de drag:**

```typescript
<motion.div
  drag
  onDragStart={(event, info) => console.log(info.point)}
  onDrag={(event, info) => console.log(info.velocity)}
  onDragEnd={(event, info) => console.log(info.offset)}
  onDirectionLock={(axis) => console.log(`Travado em ${axis}`)}
/>

// Estrutura do objeto info:
// { point: { x, y }, delta: { x, y }, offset: { x, y }, velocity: { x, y } }
```

### Gestos de hover e tap

```typescript
// Hover
<motion.button
  whileHover={{ scale: 1.1, backgroundColor: "#f00" }}
  onHoverStart={(event) => console.log("Hover iniciou")}
  onHoverEnd={(event) => console.log("Hover terminou")}
/>

// Tap/Press
<motion.button
  whileTap={{ scale: 0.95 }}
  onTapStart={(event) => console.log("Tap iniciou")}
  onTap={(event) => console.log("Tap completado")}
  onTapCancel={(event) => console.log("Tap cancelado")}
/>

// Focus (segue regras do :focus-visible)
<motion.input
  whileFocus={{ borderColor: "#00f", scale: 1.02 }}
/>
```

**Nota de acessibilidade:** Elementos com props de tap são automaticamente acessíveis por teclado. `Enter` dispara `onTapStart` e `whileTap`.

### Gestos de pan

Pan detecta movimento do pointer após pressionar (>3 pixels).

```typescript
<motion.div
  onPan={(event, info) => console.log(info.point)}
  onPanStart={(event, info) => console.log("Pan iniciou")}
  onPanEnd={(event, info) => console.log(info.velocity)}
  style={{ touchAction: "none" }}  // Necessário para touch
/>
```

### Detecção de viewport com whileInView

```typescript
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{
    once: true,           // Anima apenas uma vez
    root: scrollRef,      // Elemento scrollável ancestral
    margin: "0px -20px",  // Margem do viewport
    amount: 0.5           // "some" | "all" | 0-1
  }}
  onViewportEnter={(entry) => console.log("Entrou no viewport")}
  onViewportLeave={(entry) => console.log("Saiu do viewport")}
/>
```

---

## Parte 4: Animações de Layout

### A prop `layout` - mágica do Motion

A prop `layout` anima automaticamente mudanças de layout usando transforms CSS de alta performance.

```typescript
// Boolean - anima posição E tamanho
<motion.div layout />

// "position" - apenas posição
<motion.img layout="position" />

// "size" - apenas tamanho
<motion.div layout="size" />
```

**Casos de uso poderosos:**

```typescript
// Animar propriedades "inanimáveis"
<motion.div
  layout
  style={{ justifyContent: isExpanded ? "flex-start" : "center" }}
/>

// Toggle de estado
function Expandable() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <motion.div
      layout
      style={{
        width: isOpen ? 300 : 100,
        height: isOpen ? 200 : 50
      }}
      onClick={() => setIsOpen(!isOpen)}
    />
  )
}
```

### Shared layout animations com layoutId

O `layoutId` conecta elementos diferentes para transições suaves entre eles.

```typescript
function TabBar({ tabs, activeTab }) {
  return (
    <ul>
      {tabs.map(tab => (
        <li key={tab.id}>
          {tab.label}
          {activeTab === tab.id && (
            <motion.div
              layoutId="underline"
              className="underline"
            />
          )}
        </li>
      ))}
    </ul>
  )
}
```

**Transição hero entre páginas:**

```typescript
// Lista de cards
function CardList() {
  return (
    <ul>
      {items.map(item => (
        <motion.li layoutId={`card-${item.id}`} key={item.id}>
          <Link to={`/item/${item.id}`}>{item.title}</Link>
        </motion.li>
      ))}
    </ul>
  )
}

// Página de detalhe
function CardDetail({ item }) {
  return (
    <motion.div layoutId={`card-${item.id}`}>
      <h1>{item.title}</h1>
      <p>{item.description}</p>
    </motion.div>
  )
}
```

### LayoutGroup - sincronização de componentes

`LayoutGroup` agrupa componentes que afetam o layout uns dos outros mas não re-renderizam juntos.

```typescript
import { LayoutGroup } from "motion/react"

function Accordion() {
  return (
    <LayoutGroup>
      <AccordionItem />
      <AccordionItem />
      <AccordionItem />
    </LayoutGroup>
  )
}
```

**Namespace para layoutId:**

```typescript
// Evita conflitos entre instâncias
function TabRow({ id, items }) {
  return (
    <LayoutGroup id={id}>
      {items.map(item => <Tab key={item.id} {...item} />)}
    </LayoutGroup>
  )
}

// IDs não conflitam
<TabRow id="header" items={headerItems} />
<TabRow id="footer" items={footerItems} />
```

### Props auxiliares de layout

| Prop | Tipo | Descrição |
|------|------|-----------|
| `layoutDependency` | `any` | Força recálculo apenas quando valor muda |
| `layoutScroll` | `boolean` | Necessário dentro de containers scrolláveis |
| `layoutRoot` | `boolean` | Necessário dentro de `position: fixed` |

```typescript
// Otimização de performance
<motion.nav layout layoutDependency={isOpen} />

// Dentro de scroll container
<motion.div layoutScroll style={{ overflow: "scroll" }}>
  <motion.div layout />
</motion.div>

// Dentro de fixed element
<motion.div layoutRoot style={{ position: "fixed" }}>
  <motion.div layout />
</motion.div>
```

### Customizando transições de layout

```typescript
// Transição específica para layout
<motion.div
  layout
  animate={{ opacity: 0.5 }}
  transition={{
    opacity: { ease: "linear" },
    layout: { type: "spring", stiffness: 300, damping: 30 }
  }}
/>
```

---

## Parte 5: Referência de Hooks

### useAnimate - Controle imperativo de animações

O hook mais poderoso do Motion para animações programáticas, sequências e timelines.

```typescript
import { useAnimate } from "motion/react"

function Component() {
  const [scope, animate] = useAnimate()

  const handleClick = async () => {
    // Anima elemento específico
    await animate(scope.current, { x: 100 })
    
    // Anima por seletor (escopado)
    await animate("li", { opacity: 1 })
    
    // Sequência de animações
    await animate([
      [scope.current, { x: "100%" }],
      ["li", { opacity: 1 }],
      [".box", { scale: 1.2 }, { at: "<" }],  // Junto com anterior
      [".text", { y: 0 }, { at: "+0.5" }]     // 0.5s após anterior
    ])
  }

  return (
    <ul ref={scope}>
      <li>Item 1</li>
      <li>Item 2</li>
    </ul>
  )
}
```

**Controles de playback:**

```typescript
const controls = animate(element, { x: 100 })

controls.play()
controls.pause()
controls.stop()
controls.complete()

controls.time = 0.5   // Pula para tempo específico
controls.speed = 2    // Dobra velocidade
```

### useMotionValue - Valores reativos

Motion values são atualizados **fora do ciclo de render do React** para máxima performance.

```typescript
import { motion, useMotionValue } from "motion/react"

function Component() {
  const x = useMotionValue(0)

  return (
    <>
      <motion.div drag="x" style={{ x }} />
      <motion.div style={{ x }} />  {/* Segue o primeiro */}
    </>
  )
}
```

**Métodos disponíveis:**

| Método | Descrição |
|--------|-----------|
| `get()` | Retorna valor atual |
| `set(value)` | Atualiza valor (batched) |
| `jump(value)` | Atualiza imediatamente, reseta velocity |
| `getVelocity()` | Retorna velocidade por segundo |
| `isAnimating()` | Retorna se está animando |
| `stop()` | Para animação ativa |
| `on(event, callback)` | Inscreve em eventos |

**Eventos:**
- `"change"` - Valor mudou
- `"animationStart"` - Animação iniciou
- `"animationComplete"` - Animação completou
- `"animationCancel"` - Animação cancelada

### useTransform - Transformação de valores

Cria motion values derivados de outros motion values.

```typescript
import { useMotionValue, useTransform } from "motion/react"

function Component() {
  const x = useMotionValue(0)
  
  // Mapeamento de ranges
  const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])
  const backgroundColor = useTransform(
    x,
    [-200, 0, 200],
    ["#ff0000", "#ffffff", "#0000ff"]
  )

  return (
    <motion.div drag="x" style={{ x, opacity, backgroundColor }} />
  )
}
```

**Com função transform:**

```typescript
const x = useMotionValue(0)
const y = useMotionValue(0)
const rotate = useTransform(() => x.get() + y.get())
```

**Opções:**

```typescript
useTransform(
  value,
  inputRange,
  outputRange,
  {
    clamp: false,  // Continua além do range (padrão: true)
    ease: "easeInOut",
    mixer: customMixerFunction
  }
)
```

### useSpring - Motion values com física de mola

```typescript
import { useSpring, useMotionValue } from "motion/react"

// Spring direto
const x = useSpring(0)
x.set(100)  // Anima com spring

// Spring seguindo outro motion value
const rawX = useMotionValue(0)
const smoothX = useSpring(rawX, {
  stiffness: 300,
  damping: 30,
  restDelta: 0.001
})

<motion.div drag="x" style={{ x: smoothX }} />
```

### useScroll - Animações vinculadas ao scroll

```typescript
import { useScroll, useTransform } from "motion/react"

function ProgressBar() {
  const { scrollYProgress } = useScroll()
  
  return <motion.div style={{ scaleX: scrollYProgress }} />
}
```

**Valores retornados:**
- `scrollX`, `scrollY` - Posição absoluta (pixels)
- `scrollXProgress`, `scrollYProgress` - Progresso 0-1

**Tracking de elemento específico:**

```typescript
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end end"]  // [início, fim]
})

return <div ref={ref}>...</div>
```

**Sintaxe de offset:**
- Nomes: `"start"`, `"center"`, `"end"`
- Números: `0`, `0.5`, `1`
- Pixels: `"100px"`, `"-50px"`
- Porcentagem: `"50%"`
- Viewport: `"50vh"`, `"100vw"`

### useVelocity - Rastreamento de velocidade

```typescript
import { useMotionValue, useVelocity, useTransform } from "motion/react"

const x = useMotionValue(0)
const xVelocity = useVelocity(x)
const scale = useTransform(
  xVelocity,
  [-3000, 0, 3000],
  [2, 1, 2]
)

// Encadeamento para aceleração
const xAcceleration = useVelocity(xVelocity)
```

### useMotionTemplate - Interpolação de strings

```typescript
import { useMotionValue, useMotionTemplate } from "motion/react"

const blur = useMotionValue(10)
const saturate = useMotionValue(50)
const filter = useMotionTemplate`blur(${blur}px) saturate(${saturate}%)`

<motion.div style={{ filter }} />
```

### useReducedMotion - Acessibilidade

Detecta preferência do usuário por movimento reduzido.

```typescript
import { useReducedMotion } from "motion/react"

function Sidebar({ isOpen }) {
  const shouldReduceMotion = useReducedMotion()
  const closedX = shouldReduceMotion ? 0 : "-100%"

  return (
    <motion.div
      animate={{
        opacity: isOpen ? 1 : 0,
        x: isOpen ? 0 : closedX
      }}
    />
  )
}
```

**Retorna:**
- `true` - Usuário prefere movimento reduzido
- `false` - Movimento normal
- `null` - Preferência desconhecida (SSR)

### useInView - Intersection Observer

```typescript
import { useInView } from "motion/react"

function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref, {
    once: true,
    margin: "0px 100px -50px 0px",
    amount: 0.5  // "some" | "all" | 0-1
  })

  return (
    <div ref={ref}>
      {isInView ? "Visível!" : "Escondido"}
    </div>
  )
}
```

### useAnimationControls - Orquestração

```typescript
import { motion, useAnimationControls } from "motion/react"

function Component() {
  const controls = useAnimationControls()

  const sequence = async () => {
    await controls.start({ x: 100 })
    await controls.start({ y: 100 })
    controls.set({ rotate: 0 })  // Sem animação
  }

  return <motion.div animate={controls} onClick={sequence} />
}
```

### useMotionValueEvent - Inscrição em eventos

```typescript
import { useMotionValue, useMotionValueEvent } from "motion/react"

function Component() {
  const x = useMotionValue(0)

  useMotionValueEvent(x, "change", (latest) => {
    console.log("x mudou para", latest)
  })

  useMotionValueEvent(x, "animationStart", () => {
    console.log("Animação iniciou")
  })

  return <motion.div style={{ x }} />
}
```

---

## Parte 6: AnimatePresence

### Animando mount/unmount de componentes

`AnimatePresence` mantém elementos no DOM enquanto executam suas animações de saída.

```typescript
import { AnimatePresence, motion } from "motion/react"

function Modal({ isOpen }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          key="modal"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
        />
      )}
    </AnimatePresence>
  )
}
```

### Props do AnimatePresence

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `mode` | `"sync" \| "wait" \| "popLayout"` | `"sync"` | Sequenciamento de enter/exit |
| `initial` | `boolean` | `true` | Desabilita animação inicial dos filhos |
| `custom` | `any` | - | Dados para variants dinâmicos |
| `onExitComplete` | `() => void` | - | Callback após todos saírem |
| `propagate` | `boolean` | `false` | Propaga para AnimatePresence aninhados |

### Modos de operação

**`mode="sync"` (Padrão):**
Elementos entram e saem simultaneamente.

```typescript
<AnimatePresence mode="sync">
  {items.map(item => (
    <motion.div key={item.id} exit={{ opacity: 0 }} />
  ))}
</AnimatePresence>
```

**`mode="wait"`:**
Novo elemento aguarda o anterior sair completamente. Ideal para transições de página.

```typescript
<AnimatePresence mode="wait">
  <motion.div
    key={currentPage}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0, transition: { ease: "easeIn" } }}
    transition={{ ease: "easeOut" }}
  />
</AnimatePresence>
```

**`mode="popLayout"`:**
Elementos saindo são removidos do fluxo do layout imediatamente. Combina bem com `layout` prop.

```typescript
<motion.ul layout style={{ position: "relative" }}>
  <AnimatePresence mode="popLayout">
    {todos.map(todo => (
      <motion.li
        key={todo.id}
        layout
        exit={{ opacity: 0, x: 50 }}
      />
    ))}
  </AnimatePresence>
</motion.ul>
```

### Exit dinâmico com custom

```typescript
const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 300 : -300,
    opacity: 0
  }),
  center: { x: 0, opacity: 1 },
  exit: (direction: number) => ({
    x: direction < 0 ? 300 : -300,
    opacity: 0
  })
}

function Slideshow({ direction, image }) {
  return (
    <AnimatePresence custom={direction} mode="wait">
      <motion.img
        key={image.src}
        custom={direction}
        variants={variants}
        initial="enter"
        animate="center"
        exit="exit"
      />
    </AnimatePresence>
  )
}
```

### Hooks de presença

```typescript
import { useIsPresent, usePresence } from "motion/react"

// Apenas verificar estado
function Component() {
  const isPresent = useIsPresent()
  return <div>{isPresent ? "Presente" : "Saindo..."}</div>
}

// Controle manual de remoção
function ManualExit() {
  const [isPresent, safeToRemove] = usePresence()

  useEffect(() => {
    if (!isPresent) {
      // Fazer cleanup, então chamar safeToRemove
      const timer = setTimeout(safeToRemove, 1000)
      return () => clearTimeout(timer)
    }
  }, [isPresent, safeToRemove])

  return <div>...</div>
}
```

---

## Parte 7: Animações de Scroll

### Barra de progresso de scroll

```typescript
import { motion, useScroll, useSpring } from "motion/react"

function ProgressBar() {
  const { scrollYProgress } = useScroll()
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  })

  return (
    <motion.div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        height: 4,
        background: "#0066ff",
        scaleX,
        transformOrigin: "0%"
      }}
    />
  )
}
```

### Parallax effects

```typescript
import { useRef } from "react"
import { motion, useScroll, useTransform } from "motion/react"

function useParallax(value: MotionValue<number>, distance: number) {
  return useTransform(value, [0, 1], [-distance, distance])
}

function ParallaxSection({ id }) {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  })
  const y = useParallax(scrollYProgress, 300)

  return (
    <section>
      <div ref={ref}>
        <motion.h2 style={{ y }}>Seção {id}</motion.h2>
      </div>
    </section>
  )
}
```

### Detecção de direção do scroll

```typescript
import { useScroll, useMotionValueEvent } from "motion/react"
import { useState } from "react"

function Header() {
  const { scrollY } = useScroll()
  const [hidden, setHidden] = useState(false)

  useMotionValueEvent(scrollY, "change", (latest) => {
    const previous = scrollY.getPrevious() ?? 0
    setHidden(latest > previous && latest > 150)
  })

  return (
    <motion.header
      animate={{ y: hidden ? -100 : 0 }}
      transition={{ duration: 0.35 }}
    />
  )
}
```

### Scroll horizontal

```typescript
const containerRef = useRef(null)
const { scrollXProgress } = useScroll({
  container: containerRef,
  axis: "x"
})

<div ref={containerRef} style={{ overflowX: "scroll" }}>
  {items}
</div>
```

### Scroll-triggered reveals com whileInView

```typescript
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.5 }}
  transition={{ duration: 0.5 }}
>
  Conteúdo revelado no scroll
</motion.div>
```

---

## Parte 8: Motion+ Premium

### Componente Carousel

O Carousel do Motion+ é altamente performático, acessível e leve (+5.5kb).

**Instalação:**
```bash
npm install "https://api.motion.dev/registry.tgz?package=motion-plus&version=2.0.2&token=SEU_TOKEN"
```

```typescript
import { Carousel, useCarousel } from "motion-plus/react"

const items = [
  <img src="/img1.jpg" alt="Imagem 1" />,
  <img src="/img2.jpg" alt="Imagem 2" />,
  <img src="/img3.jpg" alt="Imagem 3" />
]

function ImageCarousel() {
  return (
    <Carousel
      items={items}
      loop={true}
      snap={true}
      gap={20}
      fade={true}
    >
      <Navigation />
      <Pagination />
    </Carousel>
  )
}
```

**Props do Carousel:**

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `items` | `ReactNode[]` | Obrigatório | Array de itens |
| `axis` | `"x" \| "y"` | `"x"` | Direção do scroll |
| `gap` | `number` | - | Espaçamento entre itens |
| `loop` | `boolean` | `true` | Scroll infinito |
| `snap` | `boolean` | `true` | Snap scroll |
| `fade` | `boolean` | - | Fade nas bordas |
| `itemSize` | `"fill"` | - | Itens preenchem container |

**Hook useCarousel:**

```typescript
function Navigation() {
  const { 
    nextPage, 
    prevPage, 
    gotoPage,
    currentPage, 
    totalPages,
    isNextActive,
    isPrevActive 
  } = useCarousel()

  return (
    <div>
      <button onClick={prevPage} disabled={!isPrevActive}>
        Anterior
      </button>
      <span>{currentPage + 1} / {totalPages}</span>
      <button onClick={nextPage} disabled={!isNextActive}>
        Próximo
      </button>
    </div>
  )
}
```

**Pagination dots:**

```typescript
function Pagination() {
  const { currentPage, totalPages, gotoPage } = useCarousel()

  return (
    <ul className="dots">
      {Array.from({ length: totalPages }, (_, i) => (
        <li key={i}>
          <motion.button
            animate={{ opacity: currentPage === i ? 1 : 0.5 }}
            onClick={() => gotoPage(i)}
          />
        </li>
      ))}
    </ul>
  )
}
```

### Ticker Component

Marquee infinito com suporte a drag e scroll.

```typescript
import { Ticker } from "motion-plus/react"

const items = [
  <span>NOTÍCIA 1</span>,
  <span>NOTÍCIA 2</span>,
  <span>NOTÍCIA 3</span>
]

<Ticker items={items} velocity={100} />
```

### AnimateNumber

Animação de transição numérica com suporte a locale.

```typescript
import { AnimateNumber } from "motion-plus/react"

<AnimateNumber
  locales="pt-BR"
  format={{ style: "currency", currency: "BRL" }}
>
  {1234.56}
</AnimateNumber>
```

### splitText

Divide texto para animações por caractere, palavra ou linha.

```typescript
import { splitText } from "motion-plus"
import { animate, stagger } from "motion"

const element = document.querySelector("h1")
const { chars, words, lines } = splitText(element)

animate(chars, { y: [-20, 0], opacity: [0, 1] }, {
  delay: stagger(0.03)
})
```

---

## Parte 9: Padrões Avançados

### Transições de página com Next.js App Router

```typescript
// app/template.tsx
"use client"
import { motion } from "motion/react"

const variants = {
  hidden: { opacity: 0, x: -100 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 100 }
}

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.main
      variants={variants}
      initial="hidden"
      animate="enter"
      transition={{ type: "spring", stiffness: 100 }}
    >
      {children}
    </motion.main>
  )
}
```

### Transições de página com React Router

```typescript
import { AnimatePresence, motion } from "motion/react"
import { useLocation, useOutlet } from "react-router-dom"

const pageVariants = {
  initial: { opacity: 0, x: -100 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 100 }
}

function AnimatedOutlet() {
  const location = useLocation()
  const element = useOutlet()

  return (
    <AnimatePresence mode="wait">
      {element && (
        <motion.div
          key={location.pathname}
          variants={pageVariants}
          initial="initial"
          animate="animate"
          exit="exit"
        >
          {element}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

### Stagger patterns complexos

```typescript
import { stagger } from "motion/react"

const gridVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      delayChildren: stagger(0.05, {
        from: "center",  // Efeito ripple do centro
        ease: "easeOut"
      })
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, scale: 0 },
  visible: { opacity: 1, scale: 1 }
}

function Grid() {
  return (
    <motion.div
      className="grid"
      variants={gridVariants}
      initial="hidden"
      animate="visible"
    >
      {cells.map(cell => (
        <motion.div key={cell.id} variants={itemVariants} />
      ))}
    </motion.div>
  )
}
```

### Animações SVG path drawing

```typescript
const pathVariants = {
  hidden: { pathLength: 0, opacity: 0 },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: { duration: 2, ease: "easeInOut" },
      opacity: { duration: 0.01 }
    }
  }
}

function DrawingIcon() {
  return (
    <motion.svg initial="hidden" animate="visible" viewBox="0 0 100 100">
      <motion.path
        d="M10 10 L90 90"
        variants={pathVariants}
        stroke="#000"
        strokeWidth="2"
        fill="none"
      />
    </motion.svg>
  )
}
```

### Modal com backdrop animado

```typescript
function AnimatedModal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            key="backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black"
            onClick={onClose}
          />
          <motion.div
            key="modal"
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="modal-content"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Lista reordenável animada

```typescript
import { Reorder } from "motion/react"

function TodoList() {
  const [items, setItems] = useState(initialItems)

  return (
    <Reorder.Group
      axis="y"
      values={items}
      onReorder={setItems}
      as="ul"
    >
      {items.map(item => (
        <Reorder.Item
          key={item.id}
          value={item}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          whileDrag={{ scale: 1.05, boxShadow: "0 5px 15px rgba(0,0,0,0.2)" }}
        >
          {item.text}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

---

## Parte 10: Guia de Performance

### Propriedades performáticas vs custosas

**Use preferencialmente (aceleradas por GPU):**
- `transform` (x, y, scale, rotate)
- `opacity`
- `filter`
- `clipPath`

**Evite animar diretamente:**
- `width`, `height`, `padding`, `margin`
- `top`, `left`, `right`, `bottom`
- `border`, `borderRadius` (use `clipPath` como alternativa)

```typescript
// ✅ Performático
<motion.div animate={{ x: 100, opacity: 0.5 }} />

// ❌ Custoso - causa layout thrashing
<motion.div animate={{ width: 200, marginLeft: 50 }} />

// ✅ Alternativa para borderRadius
<motion.div animate={{ clipPath: "inset(0 round 50px)" }} />
```

### Otimizações com motion values

```typescript
// ✅ Motion values atualizam fora do React
const x = useMotionValue(0)
const opacity = useTransform(x, [-100, 0, 100], [0, 1, 0])

return <motion.div style={{ x, opacity }} />

// ❌ Evite - causa re-renders
const [x, setX] = useState(0)
<motion.div animate={{ x }} />
```

### LazyMotion para bundle menor

```typescript
// features.ts
export { domAnimation as default } from "motion/react"

// App.tsx
import { LazyMotion } from "motion/react"
import * as m from "motion/react-m"

const loadFeatures = () => import("./features").then(res => res.default)

function App() {
  return (
    <LazyMotion features={loadFeatures}>
      <m.div animate={{ opacity: 1 }} />
    </LazyMotion>
  )
}
```

### Cleanup adequado de animações

```typescript
useEffect(() => {
  const controls = animate(element, { x: 100 })
  
  return () => {
    controls.stop()  // Sempre limpar!
  }
}, [])
```

### Problemas comuns de performance

| Problema | Solução |
|----------|---------|
| Layout animations lentas | Use `layoutDependency` para limitar recálculos |
| Muitos motion values | Compartilhe entre componentes quando possível |
| Memory leaks | Sempre chame `stop()` em useEffect cleanup |
| Re-renders excessivos | Use `React.memo` e `useMemo` para variants |
| Layout thrashing | Anime transforms em vez de propriedades de layout |

---

## Parte 11: Receitas de Integração

### Com Radix UI

```typescript
import * as Dialog from "@radix-ui/react-dialog"
import { AnimatePresence, motion } from "motion/react"

function Modal({ open, onOpenChange, children }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Trigger>Abrir</Dialog.Trigger>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.5 }}
                exit={{ opacity: 0 }}
                className="overlay"
              />
            </Dialog.Overlay>
            <Dialog.Content asChild>
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                {children}
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  )
}
```

### Com shadcn/ui

```typescript
// Opção 1: Wrap em motion.div
<motion.div animate={{ scale: 1.1 }}>
  <Button>Clique</Button>
</motion.div>

// Opção 2: motion.create (verificar compatibilidade)
import { Button } from "@/components/ui/button"
const MotionButton = motion.create(Button)

<MotionButton whileHover={{ scale: 1.05 }}>
  Clique
</MotionButton>
```

### Com Zustand

```typescript
import { create } from "zustand"
import { AnimatePresence, motion } from "motion/react"

const useToastStore = create((set, get) => ({
  toasts: [],
  addToast: (toast) => set({ toasts: [...get().toasts, toast] }),
  removeToast: (id) => set({ 
    toasts: get().toasts.filter(t => t.id !== id) 
  })
}))

function ToastContainer() {
  const toasts = useToastStore(state => state.toasts)

  return (
    <AnimatePresence>
      {toasts.map(toast => (
        <motion.div
          key={toast.id}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, x: 100 }}
        >
          {toast.message}
        </motion.div>
      ))}
    </AnimatePresence>
  )
}
```

### Server Components no Next.js

```typescript
// components/motion-wrappers.tsx
"use client"
import { motion, HTMLMotionProps } from "motion/react"
import { forwardRef } from "react"

export const MotionDiv = forwardRef<HTMLDivElement, HTMLMotionProps<"div">>(
  (props, ref) => <motion.div ref={ref} {...props} />
)

// Uso em Server Component
import { MotionDiv } from "@/components/motion-wrappers"

export default function Page() {
  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      Conteúdo
    </MotionDiv>
  )
}
```

---

## Parte 12: Referência Rápida

### Cheat sheet de props

```typescript
// Animação básica
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.3, type: "spring" }}
/>

// Gestos
<motion.div
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  whileFocus={{ borderColor: "blue" }}
  whileDrag={{ boxShadow: "0 10px 20px rgba(0,0,0,0.2)" }}
  whileInView={{ opacity: 1 }}
/>

// Drag
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  dragElastic={0.2}
  dragMomentum={true}
/>

// Layout
<motion.div
  layout
  layoutId="shared-element"
/>

// Variants
<motion.div
  variants={variants}
  initial="hidden"
  animate="visible"
  exit="exit"
/>
```

### Padrões copy-paste

**Fade in on mount:**
```typescript
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
/>
```

**Slide up on scroll:**
```typescript
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
/>
```

**Button press effect:**
```typescript
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
/>
```

**Staggered list:**
```typescript
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => <motion.li key={i} variants={item} />)}
</motion.ul>
```

### FAQ e Troubleshooting

**Exit animation não funciona:**
- Verifique se o elemento é filho direto de `AnimatePresence`
- Certifique-se de que há uma `key` única
- Use `mode="wait"` se precisar sequenciar

**Layout animation não anima:**
- Elementos `display: inline` não suportam transforms
- SVGs não suportam layout animations
- Verifique se o elemento pai tem `position: relative`

**AnimatePresence com múltiplos filhos:**
- Use `mode="popLayout"` para listas
- Cada filho precisa de `key` única e estável
- Não use índice de array como key

**Hydration mismatch no SSR:**
- Use `initial={false}` com cuidado
- Considere `useReducedMotion` para valores iniciais
- Evite valores aleatórios em `initial`

**Performance ruim:**
- Anime apenas transforms e opacity
- Use `LazyMotion` para bundle menor
- Implemente `layoutDependency` para layout animations
- Sempre faça cleanup em useEffect

---

## Conclusão

Este guia cobre a **totalidade da API do Motion+**, desde conceitos fundamentais até técnicas avançadas de otimização. As principais lições para dominar o framework são:

1. **Prefira transforms e opacity** para animações performáticas
2. **Use variants** para orquestração pai-filho elegante
3. **Implemente `layoutId`** para transições hero impressionantes
4. **Combine hooks** como `useScroll` + `useTransform` + `useSpring` para efeitos de scroll suaves
5. **Sempre limpe animações** em useEffect para evitar memory leaks
6. **Respeite acessibilidade** com `useReducedMotion`

O Motion+ continua evoluindo com novos recursos sendo adicionados regularmente. Para atualizações, consulte sempre a documentação oficial em **motion.dev/docs**.