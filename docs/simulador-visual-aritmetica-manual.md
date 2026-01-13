---
# Simulador visual de aritmética manual: soluções e implementação

**Não existe uma biblioteca JavaScript pronta** que visualize operações aritméticas passo a passo como humanos fazem no papel, incluindo carry e borrow animados. Esta lacuna representa uma oportunidade para criar algo valioso. A melhor abordagem é construir uma solução customizada usando **SVG + Rough.js + GSAP**, combinando aparência de papel com animações sequenciais controladas por um motor de cálculo separado.

---

## O cenário atual de soluções existentes

Após pesquisa exaustiva em GitHub, NPM, CodePen e plataformas educacionais, **nenhuma biblioteca JavaScript oferece visualização completa de aritmética manual**. Os projetos encontrados cobrem aspectos parciais:

| Projeto | Operações | Carry/Borrow | Animação | Tecnologia |
|---------|-----------|--------------|----------|------------|
| NTProductions/simple-long-division | Divisão apenas | ❌ | ❌ | JS puro |
| pkra/mathjax-extension-longdiv | Divisão (estático) | ❌ | ❌ | MathJax |
| Khan/perseus | Framework de exercícios | ❌ | ❌ | React |
| Mathigon libraries | Parser de expressões | ❌ | ✅ | TypeScript |
| PhET SceneryStack | Framework de simulações | ❌ | ✅ | TypeScript |

O **Graspable Math** (integrado ao GeoGebra) é a referência mais próxima do conceito, oferecendo manipulação dinâmica de notação algébrica com gestos. No entanto, é focado em álgebra, não aritmética básica, e não é open source.

---

## Bibliotecas recomendadas para construção customizada

### Aparência de papel: Rough.js é essencial

**Rough.js** (roughjs.com) cria gráficos com aparência desenhada à mão em **menos de 9KB**. Funciona com Canvas e SVG, perfeito para simular escrita no papel.

```javascript
import rough from 'roughjs';
const rc = rough.svg(svgElement);
// Linha horizontal separadora da operação
rc.line(10, 100, 200, 100, { strokeWidth: 2, roughness: 0.8 });
// Retângulo destacando o carry
rc.rectangle(50, 10, 20, 20, { fill: 'yellow', fillStyle: 'hachure' });
```

O algoritmo interno randomiza endpoints e adiciona curvatura sutil, criando traços orgânicos. Configurações de `roughness` entre **0.5-1.5** produzem efeito natural sem exagero.

### Animação sequencial: GSAP ou Anime.js

**GSAP** (gsap.com) oferece o melhor controle de timeline para sequenciar passos aritméticos:

```javascript
gsap.timeline()
  .to('.digit-6', { opacity: 1, duration: 0.3 })
  .to('.digit-7', { opacity: 1, duration: 0.3 }, "+=0.2")
  .to('.carry-indicator', { scale: 1.2, color: 'red', duration: 0.5 })
  .to('.result-digit', { y: 0, opacity: 1, duration: 0.4 });
```

**Anime.js** é alternativa mais leve (~6KB) com sintaxe similar. Ambos integram bem com React via refs.

### Framework educacional completo: p5.js + p5.teach.js

Para quem prefere uma abordagem mais estruturada, **p5.teach.js** foi criado especificamente para animações matemáticas educacionais:

- Suporte nativo a TeX/KaTeX para notação matemática
- Inspirado no Manim (3Blue1Brown)
- Desenvolvido no Google Summer of Code 2021
- URL: https://two-ticks.github.io/p5.teach.js/

---

## A escolha técnica: por que SVG supera Canvas aqui

Para visualização de aritmética com **menos de 100 elementos** (dígitos, linhas, símbolos), **SVG é a escolha superior**:

| Fator | SVG ✅ | Canvas |
|-------|--------|--------|
| Acessibilidade | Nativa (DOM-based) | Requer ARIA manual |
| Qualidade de texto | Sempre nítido | Pode ficar fuzzy |
| Eventos de interação | Built-in por elemento | Cálculo manual de hit-testing |
| Integração React | Elementos como JSX | Requer refs e useEffect |
| Debug | Inspecionável no DevTools | Opaco |
| Animação | CSS transitions funcionam | requestAnimationFrame obrigatório |

Canvas seria preferível apenas para **milhares de partículas** ou efeitos de desenho em tempo real. Rough.js suporta ambos, então a migração é trivial se necessário.

---# Simulador visual de aritmética manual: soluções e implementação
<!-- Arquivo renomeado para: simulador-visual-aritmetica-manual.md -->

**Não existe uma biblioteca JavaScript pronta** que visualize operações aritméticas passo a passo como humanos fazem no papel, incluindo carry e borrow animados. Esta lacuna representa uma oportunidade para criar algo valioso. A melhor abordagem é construir uma solução customizada usando **SVG + Rough.js + GSAP**, combinando aparência de papel com animações sequenciais controladas por um motor de cálculo separado.

---

## O cenário atual de soluções existentes

Após pesquisa exaustiva em GitHub, NPM, CodePen e plataformas educacionais, **nenhuma biblioteca JavaScript oferece visualização completa de aritmética manual**. Os projetos encontrados cobrem aspectos parciais:

| Projeto | Operações | Carry/Borrow | Animação | Tecnologia |
|---------|-----------|--------------|----------|------------|
| NTProductions/simple-long-division | Divisão apenas | ❌ | ❌ | JS puro |
| pkra/mathjax-extension-longdiv | Divisão (estático) | ❌ | ❌ | MathJax |
| Khan/perseus | Framework de exercícios | ❌ | ❌ | React |
| Mathigon libraries | Parser de expressões | ❌ | ✅ | TypeScript |
| PhET SceneryStack | Framework de simulações | ❌ | ✅ | TypeScript |

O **Graspable Math** (integrado ao GeoGebra) é a referência mais próxima do conceito, oferecendo manipulação dinâmica de notação algébrica com gestos. No entanto, é focado em álgebra, não aritmética básica, e não é open source.

---

## Bibliotecas recomendadas para construção customizada

### Aparência de papel: Rough.js é essencial

**Rough.js** (roughjs.com) cria gráficos com aparência desenhada à mão em **menos de 9KB**. Funciona com Canvas e SVG, perfeito para simular escrita no papel.

```javascript
import rough from 'roughjs';
const rc = rough.svg(svgElement);
// Linha horizontal separadora da operação
rc.line(10, 100, 200, 100, { strokeWidth: 2, roughness: 0.8 });
// Retângulo destacando o carry
rc.rectangle(50, 10, 20, 20, { fill: 'yellow', fillStyle: 'hachure' });
```

O algoritmo interno randomiza endpoints e adiciona curvatura sutil, criando traços orgânicos. Configurações de `roughness` entre **0.5-1.5** produzem efeito natural sem exagero.

### Animação sequencial: GSAP ou Anime.js

**GSAP** (gsap.com) oferece o melhor controle de timeline para sequenciar passos aritméticos:

```javascript
gsap.timeline()
  .to('.digit-6', { opacity: 1, duration: 0.3 })
  .to('.digit-7', { opacity: 1, duration: 0.3 }, "+=0.2")
  .to('.carry-indicator', { scale: 1.2, color: 'red', duration: 0.5 })
  .to('.result-digit', { y: 0, opacity: 1, duration: 0.4 });
```

**Anime.js** é alternativa mais leve (~6KB) com sintaxe similar. Ambos integram bem com React via refs.

### Framework educacional completo: p5.js + p5.teach.js

Para quem prefere uma abordagem mais estruturada, **p5.teach.js** foi criado especificamente para animações matemáticas educacionais:

- Suporte nativo a TeX/KaTeX para notação matemática
- Inspirado no Manim (3Blue1Brown)
- Desenvolvido no Google Summer of Code 2021
- URL: https://two-ticks.github.io/p5.teach.js/

---

## A escolha técnica: por que SVG supera Canvas aqui

Para visualização de aritmética com **menos de 100 elementos** (dígitos, linhas, símbolos), **SVG é a escolha superior**:

| Fator | SVG ✅ | Canvas |
|-------|--------|--------|
| Acessibilidade | Nativa (DOM-based) | Requer ARIA manual |
| Qualidade de texto | Sempre nítido | Pode ficar fuzzy |
| Eventos de interação | Built-in por elemento | Cálculo manual de hit-testing |
| Integração React | Elementos como JSX | Requer refs e useEffect |
| Debug | Inspecionável no DevTools | Opaco |
| Animação | CSS transitions funcionam | requestAnimationFrame obrigatório |

Canvas seria preferível apenas para **milhares de partículas** ou efeitos de desenho em tempo real. Rough.js suporta ambos, então a migração é trivial se necessário.

---

## Arquitetura recomendada para o projeto

A separação entre **motor de cálculo** e **renderização** é fundamental para manutenibilidade e testabilidade:

```
ArithmeticVisualizer/
├── engine/
│   ├── types.ts           // Interfaces de Step e Operation
│   ├── addition.ts        // Gera steps de adição com carry
│   ├── subtraction.ts     // Gera steps de subtração com borrow
│   ├── multiplication.ts  // Gera steps de multiplicação longa
│   └── division.ts        // Gera steps de divisão longa
├── visualization/
│   ├── RoughSVGRenderer.tsx   // Integração Rough.js + SVG
│   ├── DigitRenderer.tsx      // Renderiza dígitos individuais
│   ├── CarryIndicator.tsx     // Visualiza "vai um"
│   └── OperationLine.tsx      // Linhas separadoras
├── state/
│   ├── useCalculation.ts      // Hook que gera steps
│   └── useStepAnimation.ts    // Controle play/pause/next
└── components/
    ├── Visualizer.tsx         // Componente principal
    └── Controls.tsx           // Botões de controle
```

### Interface de Step para o motor de cálculo

```typescript
interface CalculationStep {
  type: 'highlight' | 'add_digits' | 'write_carry' | 'write_result' | 'borrow';
  column: number;
  row?: number;
  values: {
    operandA?: number;
    operandB?: number;
    carry?: number;
    result?: number;
  };
  explanation: string; // "6 + 7 = 13, escreve 3, vai 1"
}

// Exemplo de geração para 357 + 286
function generateAdditionSteps(a: number, b: number): CalculationStep[] {
  const steps: CalculationStep[] = [];
  let carry = 0;
  const digitsA = String(a).split('').reverse().map(Number);
  const digitsB = String(b).split('').reverse().map(Number);
  
  for (let col = 0; col < Math.max(digitsA.length, digitsB.length); col++) {
    const dA = digitsA[col] ?? 0;
    const dB = digitsB[col] ?? 0;
    const sum = dA + dB + carry;
    
    steps.push({
      type: 'highlight',
      column: col,
      values: { operandA: dA, operandB: dB },
      explanation: `Coluna ${col}: destacando ${dA} e ${dB}`
    });
    
    steps.push({
      type: 'add_digits',
      column: col,
      values: { operandA: dA, operandB: dB, carry, result: sum },
      explanation: carry > 0 
        ? `${dA} + ${dB} + ${carry} (vai um) = ${sum}`
        : `${dA} + ${dB} = ${sum}`
    });
    
    if (sum >= 10) {
      steps.push({
        type: 'write_carry',
        column: col + 1,
        values: { carry: Math.floor(sum / 10) },
        explanation: `Escreve ${sum % 10}, vai ${Math.floor(sum / 10)}`
      });
    }
    
    steps.push({
      type: 'write_result',
      column: col,
      values: { result: sum % 10 },
      explanation: `Resultado na coluna: ${sum % 10}`
    });
    
    carry = Math.floor(sum / 10);
  }
  return steps;
}
```

### Hook de animação por steps

```typescript
function useStepAnimation<T>(steps: T[], intervalMs = 800) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!isPlaying || currentStep >= steps.length - 1) return;
    const timer = setTimeout(() => setCurrentStep(s => s + 1), intervalMs);
    return () => clearTimeout(timer);
  }, [isPlaying, currentStep, steps.length, intervalMs]);

  return {
    step: steps[currentStep],
    stepIndex: currentStep,
    total: steps.length,
    isPlaying,
    isComplete: currentStep >= steps.length - 1,
    play: () => setIsPlaying(true),
    pause: () => setIsPlaying(false),
    next: () => setCurrentStep(s => Math.min(s + 1, steps.length - 1)),
    prev: () => setCurrentStep(s => Math.max(s - 1, 0)),
    reset: () => { setCurrentStep(0); setIsPlaying(false); },
    goTo: (idx: number) => setCurrentStep(Math.max(0, Math.min(idx, steps.length - 1)))
  };
}
```

---

## Algoritmos das quatro operações

### Adição com carry (vai um)
Processar da direita para esquerda. Se soma ≥ 10, escrever unidade e carregar dezena para próxima coluna.

### Subtração com borrow (empresta um)
Se dígito superior < inferior, "emprestar" 10 da coluna à esquerda, reduzindo-a em 1. Visualizar o risco sobre o número emprestado.

### Multiplicação longa
Multiplicar cada dígito do multiplicador por todos os dígitos do multiplicando, gerando **linhas parciais** deslocadas. Somar linhas parciais no final.

```
    23958233 × 5830
    ────────────────
    00000000       ← × 0
   71874699        ← × 30
  191665864        ← × 800
 119791165         ← × 5000
────────────────────
 139676498390
```

### Divisão longa
Processo iterativo: dividir, multiplicar, subtrair, baixar próximo dígito. Cada iteração produz um dígito do quociente.

---

## Edge cases a tratar na implementação

- **Dígitos desiguais**: Alinhar pela direita, tratar posições ausentes como 0
- **Zeros à esquerda**: Não exibir no resultado final (357 vs 0357)
- **Operações com zero**: 0 + n = n, 0 × n = 0, n ÷ 0 = erro
- **Números negativos**: Converter para subtração ou marcar sinal separadamente
- **Decimais**: Alinhar pela vírgula, não pela direita; adicionar zeros para igualar casas

---

## Recursos open source adaptáveis

### Mathigon (MIT License)
Ecossistema TypeScript completo para educação matemática:
- **hilbert.js**: Parser de expressões e CAS básico
- **fermat.js**: Operações aritméticas e estatísticas
- **boost.js**: Animações e manipulação DOM
- URL: https://github.com/mathigon

### PhET SceneryStack (GPL-3.0)
Framework maduro para simulações educacionais da Universidade do Colorado:
- Acessibilidade first-class (screen readers, navegação por teclado)
- Biblioteca Dot para matemática
- Biblioteca Scenery para renderização
- URL: https://github.com/phetsims

### Motion Canvas (MIT)
Alternativa TypeScript ao Manim para web:
- Generator functions para animações passo a passo
- Preview em tempo real com Vite
- URL: https://motioncanvas.io/

---

## Estilização de aparência de papel

```css
.paper-background {
  background-color: #fffef0;
  background-image: 
    linear-gradient(#e8e8e8 1px, transparent 1px);
  background-size: 100% 24px;
  font-family: 'Patrick Hand', 'Caveat', cursive;
}

.digit {
  font-size: 28px;
  transition: all 0.3s ease;
}

.digit--highlighted {
  color: #2563eb;
  transform: scale(1.1);
}

.carry-indicator {
  font-size: 14px;
  color: #dc2626;
  position: absolute;
  top: -12px;
}
```

Fontes recomendadas do Google Fonts: **Patrick Hand**, **Caveat**, **Indie Flower** para aparência manuscrita.

---

## Integração com React/TypeScript/Vite

Para o projeto DevFolio mencionado, a estrutura sugerida integra naturalmente:

```tsx
// components/ArithmeticVisualizer.tsx
import { useState } from 'react';
import { useStepAnimation } from '../state/useStepAnimation';
import { generateAdditionSteps } from '../engine/addition';
import { RoughSVGRenderer } from '../visualization/RoughSVGRenderer';

export function ArithmeticVisualizer() {
  const [operandA, setOperandA] = useState(357);
  const [operandB, setOperandB] = useState(286);
  const steps = generateAdditionSteps(operandA, operandB);
  const animation = useStepAnimation(steps, 1000);

  return (
    <div className="paper-background p-8 rounded-lg shadow-lg">
      <RoughSVGRenderer 
        operandA={operandA} 
        operandB={operandB}
        currentStep={animation.step}
        stepIndex={animation.stepIndex}
      />
      <div className="flex gap-4 mt-4 justify-center">
        <button onClick={animation.prev}>← Anterior</button>
        <button onClick={animation.isPlaying ? animation.pause : animation.play}>
          {animation.isPlaying ? '⏸ Pausar' : '▶ Play'}
        </button>
        <button onClick={animation.next}>Próximo →</button>
        <button onClick={animation.reset}>↺ Reiniciar</button>
      </div>
      <p className="text-center mt-2 text-gray-600">
        {animation.step?.explanation}
      </p>
    </div>
  );
}
```

A combinação de **SVG + Rough.js + GSAP + React hooks** cria uma solução elegante, acessível e com a aparência autêntica de matemática feita no papel. O projeto seria pioneiro no ecossistema JavaScript, preenchendo uma lacuna significativa em ferramentas educacionais de matemática.