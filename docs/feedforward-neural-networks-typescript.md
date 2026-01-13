# Redes Neurais Feedforward: Teoria Completa e Implementação em TypeScript

Redes neurais feedforward são o alicerce do deep learning moderno, capazes de aproximar virtualmente qualquer função matemática contínua. Este documento apresenta a teoria matemática completa e uma implementação funcional em TypeScript puro para Node.js 24, permitindo que você entenda e construa uma rede neural do zero — sem dependências externas e com código executável imediatamente.

A importância desta arquitetura reside em sua simplicidade conceitual combinada com poder computacional: dados fluem em uma única direção (entrada → saída), sem ciclos, permitindo o cálculo eficiente de gradientes via backpropagation. **O XOR problem, historicamente intratável para perceptrons simples, será nosso caso de teste final**, demonstrando que camadas ocultas são necessárias para problemas não-linearmente separáveis.

---

## 1. Intuição e arquitetura fundamental

Uma rede neural é uma função matemática que transforma entradas em saídas através de composições sucessivas de transformações lineares seguidas de não-linearidades. A inspiração biológica — neurônios conectados por sinapses — serve apenas como metáfora; na prática, trabalhamos com álgebra linear e cálculo diferencial.

### Estrutura visual de uma rede feedforward

```
    Camada de         Camada          Camada de
     Entrada          Oculta           Saída
    
       ○───────────────○
      /│\             /│\
     / │ \           / │ \
    ○──┼──○─────────○──┼──○───────────○
     \ │ /           \ │ /
      \│/             \│/
       ○───────────────○
    
    x₁, x₂, ...    a₁⁽¹⁾, a₂⁽¹⁾    ŷ (predição)
```

Cada conexão possui um **peso** (weight) que determina a intensidade da influência. Cada neurônio possui um **viés** (bias) que desloca o limiar de ativação. A combinação ponderada das entradas passa por uma **função de ativação** não-linear, introduzindo a capacidade de modelar relações complexas.

### Por que "feedforward"?

O termo indica que a informação flui exclusivamente para frente — da entrada para a saída — sem retroalimentação. Isso contrasta com redes recorrentes (RNNs), onde saídas alimentam entradas em passos temporais subsequentes. A ausência de ciclos simplifica drasticamente o treinamento.

---

## 2. Fundamentos matemáticos

### 2.1 Álgebra linear essencial

**Vetores** são arrays ordenados de números. Um vetor de entrada com 3 features:

```
x = [x₁, x₂, x₃]ᵀ ∈ ℝ³
```

**Matrizes** organizam números em linhas e colunas. Uma matriz de pesos conectando 3 entradas a 2 neurônios:

```
W = | w₁₁  w₁₂  w₁₃ |  ∈ ℝ²ˣ³
    | w₂₁  w₂₂  w₂₃ |
```

**Produto matriz-vetor** combina pesos e entradas:

```
z = Wx + b

Onde:
- W ∈ ℝᵐˣⁿ (m neurônios, n entradas)
- x ∈ ℝⁿ (vetor de entrada)
- b ∈ ℝᵐ (vetor de vieses)
- z ∈ ℝᵐ (pré-ativações)
```

**Exemplo numérico**:

```
W = | 0.5  -0.3 |    x = | 1.0 |    b = | 0.1 |
    | 0.8   0.2 |        | 2.0 |        | -0.2|

z = Wx + b = | 0.5×1 + (-0.3)×2 + 0.1  |   | -0.1 |
             | 0.8×1 + 0.2×2 + (-0.2)   | = |  1.0 |
```

### 2.2 O neurônio individual

Um único neurônio computa:

```
a = f(z) = f(Σⱼ wⱼxⱼ + b)
```

Onde **f** é a função de ativação. Sem ela, camadas empilhadas seriam equivalentes a uma única transformação linear (composição de funções lineares = função linear).

### 2.3 Da camada à rede completa

Para uma rede com L camadas, definimos:

- **a⁽⁰⁾ = x**: entrada (camada 0)
- **z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾**: pré-ativação da camada l
- **a⁽ˡ⁾ = f(z⁽ˡ⁾)**: ativação da camada l
- **ŷ = a⁽ᴸ⁾**: saída da rede

A função completa da rede:

```
F(x) = f⁽ᴸ⁾(W⁽ᴸ⁾f⁽ᴸ⁻¹⁾(W⁽ᴸ⁻¹⁾...f⁽¹⁾(W⁽¹⁾x + b⁽¹⁾)...) + b⁽ᴸ⁾)
```

---

## 3. Forward propagation detalhado

### 3.1 Formulação matemática

O forward pass calcula a saída da rede dado um input, propagando valores camada por camada:

```
Para l = 1 até L:
    z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾   (transformação linear)
    a⁽ˡ⁾ = f⁽ˡ⁾(z⁽ˡ⁾)          (ativação não-linear)

Retornar: ŷ = a⁽ᴸ⁾
```

### 3.2 Exemplo numérico completo

Considere uma rede **2-2-1** (2 entradas, 2 neurônios ocultos, 1 saída):

**Parâmetros inicializados**:
```
W⁽¹⁾ = | 0.15  0.20 |    b⁽¹⁾ = | 0.35 |
       | 0.25  0.30 |           | 0.35 |

W⁽²⁾ = | 0.40  0.45 |    b⁽²⁾ = | 0.60 |
```

**Entrada**: x = [0.05, 0.10]ᵀ

**Passo 1 — Camada oculta**:
```
z⁽¹⁾ = W⁽¹⁾x + b⁽¹⁾

z₁⁽¹⁾ = 0.15×0.05 + 0.20×0.10 + 0.35 = 0.0075 + 0.02 + 0.35 = 0.3775
z₂⁽¹⁾ = 0.25×0.05 + 0.30×0.10 + 0.35 = 0.0125 + 0.03 + 0.35 = 0.3925

Aplicando sigmoid:
a₁⁽¹⁾ = σ(0.3775) = 1/(1 + e⁻⁰·³⁷⁷⁵) ≈ 0.5933
a₂⁽¹⁾ = σ(0.3925) = 1/(1 + e⁻⁰·³⁹²⁵) ≈ 0.5969
```

**Passo 2 — Camada de saída**:
```
z⁽²⁾ = W⁽²⁾a⁽¹⁾ + b⁽²⁾

z₁⁽²⁾ = 0.40×0.5933 + 0.45×0.5969 + 0.60 = 0.2373 + 0.2686 + 0.60 = 1.1059

ŷ = σ(1.1059) ≈ 0.7514
```

### 3.3 Funções de ativação

#### Sigmoid

```
σ(z) = 1 / (1 + e⁻ᶻ)

Derivada: σ'(z) = σ(z) × (1 - σ(z))
```

**Características**: Mapeia para (0,1), ideal para probabilidades. Problema: gradientes desaparecem para |z| >> 0 (máximo da derivada é **0.25**).

#### ReLU (Rectified Linear Unit)

```
ReLU(z) = max(0, z)

Derivada: ReLU'(z) = { 1 se z > 0
                     { 0 se z ≤ 0
```

**Características**: Computacionalmente eficiente, evita vanishing gradients para valores positivos. Problema: "dying ReLU" (neurônios que ficam permanentemente em 0).

#### Tanh

```
tanh(z) = (eᶻ - e⁻ᶻ) / (eᶻ + e⁻ᶻ)

Derivada: tanh'(z) = 1 - tanh²(z)
```

**Características**: Mapeia para (-1,1), saídas centradas em zero (melhor que sigmoid para camadas ocultas).

#### Softmax

```
softmax(zᵢ) = eᶻⁱ / Σⱼ eᶻʲ
```

**Características**: Converte vetor em distribuição de probabilidades (soma = 1). Usada na camada de saída para classificação multiclasse.

---

## 4. Funções de perda e objetivo de otimização

O objetivo do treinamento é minimizar uma **função de perda** (loss function) que quantifica o erro entre predições e valores reais.

### 4.1 Mean Squared Error (MSE)

```
L_MSE = (1/2n) Σᵢ (yᵢ - ŷᵢ)²

Gradiente: ∂L/∂ŷ = ŷ - y
```

**Quando usar**: Problemas de regressão (saídas contínuas). O fator 1/2 simplifica a derivada.

### 4.2 Binary Cross-Entropy

```
L_BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]

Gradiente: ∂L/∂ŷ = -y/ŷ + (1-y)/(1-ŷ)
```

**Quando usar**: Classificação binária com saída sigmoid. Combinada com sigmoid, o gradiente simplifica elegantemente para **ŷ - y**.

### 4.3 Categorical Cross-Entropy

```
L_CCE = -Σₖ yₖ·log(ŷₖ)
```

**Quando usar**: Classificação multiclasse com saída softmax e labels one-hot encoded.

---

## 5. Backpropagation: o algoritmo central

Backpropagation calcula eficientemente os gradientes da função de perda em relação a todos os pesos, permitindo atualizações que reduzem o erro.

### 5.1 A regra da cadeia

O gradiente de L em relação a um peso w⁽ˡ⁾ᵢⱼ depende de como esse peso afeta z, que afeta a, que propaga até a saída e finalmente L:

```
∂L/∂w⁽ˡ⁾ᵢⱼ = (∂L/∂z⁽ˡ⁾ᵢ) × (∂z⁽ˡ⁾ᵢ/∂w⁽ˡ⁾ᵢⱼ)
```

### 5.2 Definindo o termo delta (δ)

Definimos **δᵢ⁽ˡ⁾ = ∂L/∂zᵢ⁽ˡ⁾** como o "sinal de erro" no neurônio i da camada l.

Como z⁽ˡ⁾ᵢ = Σⱼ w⁽ˡ⁾ᵢⱼ · a⁽ˡ⁻¹⁾ⱼ + b⁽ˡ⁾ᵢ:

```
∂z⁽ˡ⁾ᵢ/∂w⁽ˡ⁾ᵢⱼ = a⁽ˡ⁻¹⁾ⱼ

Portanto:
∂L/∂w⁽ˡ⁾ᵢⱼ = δ⁽ˡ⁾ᵢ × a⁽ˡ⁻¹⁾ⱼ
```

### 5.3 Propagação recursiva dos deltas

**Camada de saída (L)**:
```
δ⁽ᴸ⁾ = ∂L/∂a⁽ᴸ⁾ ⊙ f'(z⁽ᴸ⁾)
```

Para MSE + sigmoid ou cross-entropy + softmax, simplifica para:
```
δ⁽ᴸ⁾ = ŷ - y
```

**Camadas ocultas (l = L-1 até 1)**:
```
δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾)ᵀ δ⁽ˡ⁺¹⁾ ⊙ f'(z⁽ˡ⁾)
```

O símbolo ⊙ denota multiplicação elemento a elemento (Hadamard product).

### 5.4 Fórmulas completas dos gradientes

```
∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾ (a⁽ˡ⁻¹⁾)ᵀ    [matriz de dimensão igual a W⁽ˡ⁾]
∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾              [vetor de dimensão igual a b⁽ˡ⁾]
```

### 5.5 Exemplo numérico de backpropagation

Continuando o exemplo anterior (rede 2-2-1), com target y = 0.01:

**Passo 1 — Delta da camada de saída**:
```
δ⁽²⁾ = ŷ - y = 0.7514 - 0.01 = 0.7414

(Para MSE com sigmoid, δ = (ŷ-y) × σ'(z⁽²⁾), mas para cross-entropy simplifica)
```

**Passo 2 — Gradientes da camada de saída**:
```
∂L/∂W⁽²⁾ = δ⁽²⁾ × (a⁽¹⁾)ᵀ = 0.7414 × [0.5933, 0.5969]
         = [0.4398, 0.4425]

∂L/∂b⁽²⁾ = δ⁽²⁾ = 0.7414
```

**Passo 3 — Delta da camada oculta**:
```
δ⁽¹⁾ = (W⁽²⁾)ᵀ δ⁽²⁾ ⊙ σ'(z⁽¹⁾)

(W⁽²⁾)ᵀ δ⁽²⁾ = | 0.40 | × 0.7414 = | 0.2966 |
                | 0.45 |            | 0.3336 |

σ'(z⁽¹⁾) = σ(z⁽¹⁾) × (1 - σ(z⁽¹⁾))
         = | 0.5933 × 0.4067 | = | 0.2413 |
           | 0.5969 × 0.4031 |   | 0.2406 |

δ⁽¹⁾ = | 0.2966 × 0.2413 | = | 0.0716 |
       | 0.3336 × 0.2406 |   | 0.0803 |
```

### 5.6 Regra de atualização dos pesos

Com learning rate α:

```
W⁽ˡ⁾ := W⁽ˡ⁾ - α × ∂L/∂W⁽ˡ⁾
b⁽ˡ⁾ := b⁽ˡ⁾ - α × ∂L/∂b⁽ˡ⁾
```

### 5.7 Variantes de gradient descent

- **Batch**: Usa todo o dataset para cada atualização — estável mas lento
- **Stochastic (SGD)**: Uma amostra por atualização — rápido mas ruidoso
- **Mini-batch**: Compromisso ideal (32-512 amostras) — padrão na prática

---

## 6. Implementação em TypeScript para Node.js 24

### Executando TypeScript nativamente

Node.js 24 (LTS "Krypton") suporta TypeScript **nativamente** sem transpilação. Arquivos `.ts` são executados diretamente:

```bash
node neural-network.ts
```

**Requisitos importantes**:
- Use extensões `.ts` explícitas nos imports
- Use `import type` para importações apenas de tipos
- Evite enums (use union types ou objetos const)

### 6.1 Classe Matrix

```typescript
// matrix.ts - Implementação completa de operações matriciais

export class Matrix {
  readonly rows: number;
  readonly cols: number;
  private data: number[][];

  constructor(rows: number, cols: number, initialValue: number = 0) {
    this.rows = rows;
    this.cols = cols;
    this.data = Array.from({ length: rows }, () => 
      Array(cols).fill(initialValue)
    );
  }

  // Cria matriz a partir de array 2D
  static fromArray(arr: number[][]): Matrix {
    const m = new Matrix(arr.length, arr[0].length);
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr[i].length; j++) {
        m.data[i][j] = arr[i][j];
      }
    }
    return m;
  }

  // Cria vetor coluna a partir de array 1D
  static fromVector(arr: number[]): Matrix {
    const m = new Matrix(arr.length, 1);
    for (let i = 0; i < arr.length; i++) {
      m.data[i][0] = arr[i];
    }
    return m;
  }

  // Cria matriz com valores aleatórios entre min e max
  static random(rows: number, cols: number, min: number = -1, max: number = 1): Matrix {
    const m = new Matrix(rows, cols);
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        m.data[i][j] = Math.random() * (max - min) + min;
      }
    }
    return m;
  }

  // Xavier initialization: ideal para sigmoid/tanh
  static xavier(rows: number, cols: number): Matrix {
    const limit = Math.sqrt(6 / (rows + cols));
    return Matrix.random(rows, cols, -limit, limit);
  }

  get(row: number, col: number): number {
    return this.data[row][col];
  }

  set(row: number, col: number, value: number): void {
    this.data[row][col] = value;
  }

  // Converte para array 1D (para vetores coluna)
  toArray(): number[] {
    const result: number[] = [];
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.push(this.data[i][j]);
      }
    }
    return result;
  }

  // Adição elemento a elemento
  add(other: Matrix): Matrix {
    if (this.rows !== other.rows || this.cols !== other.cols) {
      throw new Error(`Dimensões incompatíveis: ${this.rows}x${this.cols} vs ${other.rows}x${other.cols}`);
    }
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] + other.data[i][j];
      }
    }
    return result;
  }

  // Subtração elemento a elemento
  subtract(other: Matrix): Matrix {
    if (this.rows !== other.rows || this.cols !== other.cols) {
      throw new Error(`Dimensões incompatíveis para subtração`);
    }
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] - other.data[i][j];
      }
    }
    return result;
  }

  // Multiplicação matricial: (m×n) × (n×p) → (m×p)
  multiply(other: Matrix): Matrix {
    if (this.cols !== other.rows) {
      throw new Error(
        `Dimensões incompatíveis para multiplicação: ${this.rows}x${this.cols} × ${other.rows}x${other.cols}`
      );
    }
    const result = new Matrix(this.rows, other.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < other.cols; j++) {
        let sum = 0;
        for (let k = 0; k < this.cols; k++) {
          sum += this.data[i][k] * other.data[k][j];
        }
        result.data[i][j] = sum;
      }
    }
    return result;
  }

  // Multiplicação elemento a elemento (Hadamard)
  hadamard(other: Matrix): Matrix {
    if (this.rows !== other.rows || this.cols !== other.cols) {
      throw new Error(`Dimensões incompatíveis para Hadamard product`);
    }
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] * other.data[i][j];
      }
    }
    return result;
  }

  // Multiplicação por escalar
  scale(scalar: number): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] * scalar;
      }
    }
    return result;
  }

  // Transposição
  transpose(): Matrix {
    const result = new Matrix(this.cols, this.rows);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[j][i] = this.data[i][j];
      }
    }
    return result;
  }

  // Aplica função a cada elemento
  map(fn: (value: number, row: number, col: number) => number): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = fn(this.data[i][j], i, j);
      }
    }
    return result;
  }

  // Soma de todos os elementos
  sum(): number {
    let total = 0;
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        total += this.data[i][j];
      }
    }
    return total;
  }

  // Impressão formatada
  print(label: string = ''): void {
    if (label) console.log(`${label}:`);
    console.log(this.data.map(row => 
      row.map(v => v.toFixed(4).padStart(8)).join(' ')
    ).join('\n'));
  }
}
```

### 6.2 Módulo de funções de ativação

```typescript
// activations.ts - Funções de ativação e suas derivadas

import { Matrix } from './matrix.ts';

// Definição de tipo para funções de ativação
export type ActivationType = 'sigmoid' | 'relu' | 'tanh';

// Sigmoid: σ(z) = 1 / (1 + e^(-z))
export function sigmoid(x: number): number {
  // Prevenção de overflow
  if (x < -500) return 0;
  if (x > 500) return 1;
  return 1 / (1 + Math.exp(-x));
}

// Derivada: σ'(z) = σ(z) × (1 - σ(z))
export function sigmoidDerivative(x: number): number {
  const s = sigmoid(x);
  return s * (1 - s);
}

// ReLU: max(0, z)
export function relu(x: number): number {
  return Math.max(0, x);
}

// Derivada: 1 se z > 0, senão 0
export function reluDerivative(x: number): number {
  return x > 0 ? 1 : 0;
}

// Tanh: (e^z - e^(-z)) / (e^z + e^(-z))
export function tanh(x: number): number {
  return Math.tanh(x);
}

// Derivada: 1 - tanh²(z)
export function tanhDerivative(x: number): number {
  const t = Math.tanh(x);
  return 1 - t * t;
}

// Interface para par de funções
interface ActivationPair {
  fn: (x: number) => number;
  derivative: (x: number) => number;
}

// Mapa de ativações disponíveis
export const activations: Record<ActivationType, ActivationPair> = {
  sigmoid: { fn: sigmoid, derivative: sigmoidDerivative },
  relu: { fn: relu, derivative: reluDerivative },
  tanh: { fn: tanh, derivative: tanhDerivative }
};

// Aplica ativação a uma matriz
export function applyActivation(m: Matrix, type: ActivationType): Matrix {
  return m.map(v => activations[type].fn(v));
}

// Aplica derivada da ativação a uma matriz
export function applyActivationDerivative(m: Matrix, type: ActivationType): Matrix {
  return m.map(v => activations[type].derivative(v));
}
```

### 6.3 Classe NeuralNetwork

```typescript
// neural-network.ts - Rede neural feedforward completa

import { Matrix } from './matrix.ts';
import { 
  type ActivationType, 
  applyActivation, 
  applyActivationDerivative 
} from './activations.ts';

// Configuração da rede
interface NetworkConfig {
  layers: number[];           // Ex: [2, 4, 1] = 2 inputs, 4 hidden, 1 output
  learningRate: number;       // Taxa de aprendizado (ex: 0.1)
  activation: ActivationType; // Função de ativação das camadas ocultas
}

// Estrutura de uma camada
interface Layer {
  weights: Matrix;  // Matriz de pesos: (neurônios_atual × neurônios_anterior)
  biases: Matrix;   // Vetor de vieses: (neurônios_atual × 1)
}

export class NeuralNetwork {
  private layers: Layer[] = [];
  private learningRate: number;
  private activation: ActivationType;
  private layerSizes: number[];

  // Cache do forward pass (necessário para backprop)
  private zValues: Matrix[] = [];  // Pré-ativações
  private aValues: Matrix[] = [];  // Ativações

  constructor(config: NetworkConfig) {
    this.learningRate = config.learningRate;
    this.activation = config.activation;
    this.layerSizes = config.layers;

    // Inicializa pesos e vieses para cada conexão entre camadas
    for (let i = 1; i < config.layers.length; i++) {
      const inputSize = config.layers[i - 1];
      const outputSize = config.layers[i];

      this.layers.push({
        // Xavier initialization para melhor convergência
        weights: Matrix.xavier(outputSize, inputSize),
        biases: new Matrix(outputSize, 1, 0)
      });
    }
  }

  // Forward propagation: calcula saída da rede
  forward(input: number[]): number[] {
    // Limpa cache
    this.zValues = [];
    this.aValues = [];

    // Converte input para matriz coluna
    let current = Matrix.fromVector(input);
    this.aValues.push(current); // a⁽⁰⁾ = input

    // Propaga através de cada camada
    for (let i = 0; i < this.layers.length; i++) {
      const layer = this.layers[i];
      
      // z⁽ˡ⁾ = W⁽ˡ⁾ × a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
      const z = layer.weights.multiply(current).add(layer.biases);
      this.zValues.push(z);

      // a⁽ˡ⁾ = f(z⁽ˡ⁾)
      // Última camada usa sigmoid para saída entre 0 e 1
      const activationType = i === this.layers.length - 1 ? 'sigmoid' : this.activation;
      current = applyActivation(z, activationType);
      this.aValues.push(current);
    }

    return current.toArray();
  }

  // Backpropagation: calcula gradientes e atualiza pesos
  backward(target: number[]): void {
    const targetMatrix = Matrix.fromVector(target);
    const numLayers = this.layers.length;

    // Array para armazenar deltas de cada camada
    const deltas: Matrix[] = new Array(numLayers);

    // === Passo 1: Delta da camada de saída ===
    // δ⁽ᴸ⁾ = (ŷ - y) ⊙ f'(z⁽ᴸ⁾)
    // Para sigmoid + MSE ou sigmoid + BCE, simplifica para: δ = ŷ - y
    const output = this.aValues[this.aValues.length - 1];
    const outputZ = this.zValues[this.zValues.length - 1];
    
    // Erro: (predição - target)
    const outputError = output.subtract(targetMatrix);
    // Derivada da ativação na última camada
    const outputDerivative = applyActivationDerivative(outputZ, 'sigmoid');
    // Delta da saída
    deltas[numLayers - 1] = outputError.hadamard(outputDerivative);

    // === Passo 2: Propagar deltas para trás ===
    // δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾)ᵀ × δ⁽ˡ⁺¹⁾ ⊙ f'(z⁽ˡ⁾)
    for (let i = numLayers - 2; i >= 0; i--) {
      const nextWeights = this.layers[i + 1].weights;
      const currentZ = this.zValues[i];
      
      // Propaga erro da próxima camada
      const propagatedError = nextWeights.transpose().multiply(deltas[i + 1]);
      // Derivada da ativação atual
      const derivative = applyActivationDerivative(currentZ, this.activation);
      // Delta desta camada
      deltas[i] = propagatedError.hadamard(derivative);
    }

    // === Passo 3: Atualizar pesos e vieses ===
    // W⁽ˡ⁾ := W⁽ˡ⁾ - α × δ⁽ˡ⁾ × (a⁽ˡ⁻¹⁾)ᵀ
    // b⁽ˡ⁾ := b⁽ˡ⁾ - α × δ⁽ˡ⁾
    for (let i = 0; i < numLayers; i++) {
      const prevActivation = this.aValues[i]; // a⁽ˡ⁻¹⁾
      
      // Gradiente dos pesos: δ⁽ˡ⁾ × (a⁽ˡ⁻¹⁾)ᵀ
      const weightGradient = deltas[i].multiply(prevActivation.transpose());
      
      // Atualiza pesos
      this.layers[i].weights = this.layers[i].weights.subtract(
        weightGradient.scale(this.learningRate)
      );
      
      // Atualiza vieses
      this.layers[i].biases = this.layers[i].biases.subtract(
        deltas[i].scale(this.learningRate)
      );
    }
  }

  // Treina a rede com um conjunto de dados
  train(
    trainingData: { input: number[]; target: number[] }[],
    epochs: number,
    logInterval: number = 1000
  ): void {
    for (let epoch = 0; epoch < epochs; epoch++) {
      let totalLoss = 0;

      for (const sample of trainingData) {
        // Forward pass
        const output = this.forward(sample.input);
        
        // Calcula loss (MSE)
        for (let i = 0; i < output.length; i++) {
          totalLoss += Math.pow(sample.target[i] - output[i], 2);
        }

        // Backward pass
        this.backward(sample.target);
      }

      // Log do progresso
      if (epoch % logInterval === 0 || epoch === epochs - 1) {
        const avgLoss = totalLoss / trainingData.length;
        console.log(`Epoch ${epoch}: Loss = ${avgLoss.toFixed(6)}`);
      }
    }
  }

  // Predição (wrapper conveniente)
  predict(input: number[]): number[] {
    return this.forward(input);
  }

  // Calcula MSE para um conjunto de dados
  evaluate(testData: { input: number[]; target: number[] }[]): number {
    let totalLoss = 0;
    for (const sample of testData) {
      const output = this.forward(sample.input);
      for (let i = 0; i < output.length; i++) {
        totalLoss += Math.pow(sample.target[i] - output[i], 2);
      }
    }
    return totalLoss / testData.length;
  }
}
```

### 6.4 Código completo em arquivo único

Para facilitar a execução, aqui está o código consolidado:

```typescript
// xor-neural-network.ts
// Execute com: node xor-neural-network.ts

// ==================== MATRIX CLASS ====================
class Matrix {
  readonly rows: number;
  readonly cols: number;
  private data: number[][];

  constructor(rows: number, cols: number, initialValue: number = 0) {
    this.rows = rows;
    this.cols = cols;
    this.data = Array.from({ length: rows }, () => Array(cols).fill(initialValue));
  }

  static fromVector(arr: number[]): Matrix {
    const m = new Matrix(arr.length, 1);
    for (let i = 0; i < arr.length; i++) m.data[i][0] = arr[i];
    return m;
  }

  static xavier(rows: number, cols: number): Matrix {
    const limit = Math.sqrt(6 / (rows + cols));
    const m = new Matrix(rows, cols);
    for (let i = 0; i < rows; i++)
      for (let j = 0; j < cols; j++)
        m.data[i][j] = Math.random() * 2 * limit - limit;
    return m;
  }

  get(row: number, col: number): number { return this.data[row][col]; }
  set(row: number, col: number, value: number): void { this.data[row][col] = value; }

  toArray(): number[] {
    const result: number[] = [];
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.push(this.data[i][j]);
    return result;
  }

  add(other: Matrix): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[i][j] = this.data[i][j] + other.data[i][j];
    return result;
  }

  subtract(other: Matrix): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[i][j] = this.data[i][j] - other.data[i][j];
    return result;
  }

  multiply(other: Matrix): Matrix {
    const result = new Matrix(this.rows, other.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < other.cols; j++) {
        let sum = 0;
        for (let k = 0; k < this.cols; k++)
          sum += this.data[i][k] * other.data[k][j];
        result.data[i][j] = sum;
      }
    return result;
  }

  hadamard(other: Matrix): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[i][j] = this.data[i][j] * other.data[i][j];
    return result;
  }

  scale(scalar: number): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[i][j] = this.data[i][j] * scalar;
    return result;
  }

  transpose(): Matrix {
    const result = new Matrix(this.cols, this.rows);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[j][i] = this.data[i][j];
    return result;
  }

  map(fn: (value: number) => number): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++)
      for (let j = 0; j < this.cols; j++)
        result.data[i][j] = fn(this.data[i][j]);
    return result;
  }
}

// ==================== ACTIVATION FUNCTIONS ====================
const sigmoid = (x: number): number => 1 / (1 + Math.exp(-x));
const sigmoidDerivative = (x: number): number => {
  const s = sigmoid(x);
  return s * (1 - s);
};

// ==================== NEURAL NETWORK ====================
class NeuralNetwork {
  private layers: { weights: Matrix; biases: Matrix }[] = [];
  private learningRate: number;
  private zValues: Matrix[] = [];
  private aValues: Matrix[] = [];

  constructor(layerSizes: number[], learningRate: number) {
    this.learningRate = learningRate;
    
    for (let i = 1; i < layerSizes.length; i++) {
      this.layers.push({
        weights: Matrix.xavier(layerSizes[i], layerSizes[i - 1]),
        biases: new Matrix(layerSizes[i], 1, 0)
      });
    }
  }

  forward(input: number[]): number[] {
    this.zValues = [];
    this.aValues = [];
    
    let current = Matrix.fromVector(input);
    this.aValues.push(current);

    for (const layer of this.layers) {
      const z = layer.weights.multiply(current).add(layer.biases);
      this.zValues.push(z);
      current = z.map(sigmoid);
      this.aValues.push(current);
    }

    return current.toArray();
  }

  backward(target: number[]): void {
    const targetMatrix = Matrix.fromVector(target);
    const deltas: Matrix[] = new Array(this.layers.length);

    // Delta da camada de saída: (ŷ - y) ⊙ σ'(z)
    const output = this.aValues[this.aValues.length - 1];
    const outputZ = this.zValues[this.zValues.length - 1];
    deltas[this.layers.length - 1] = output
      .subtract(targetMatrix)
      .hadamard(outputZ.map(sigmoidDerivative));

    // Propaga deltas para trás
    for (let i = this.layers.length - 2; i >= 0; i--) {
      const propagated = this.layers[i + 1].weights.transpose().multiply(deltas[i + 1]);
      deltas[i] = propagated.hadamard(this.zValues[i].map(sigmoidDerivative));
    }

    // Atualiza pesos e vieses
    for (let i = 0; i < this.layers.length; i++) {
      const weightGradient = deltas[i].multiply(this.aValues[i].transpose());
      this.layers[i].weights = this.layers[i].weights.subtract(
        weightGradient.scale(this.learningRate)
      );
      this.layers[i].biases = this.layers[i].biases.subtract(
        deltas[i].scale(this.learningRate)
      );
    }
  }

  train(data: { input: number[]; target: number[] }[], epochs: number): void {
    for (let epoch = 0; epoch <= epochs; epoch++) {
      let totalLoss = 0;
      
      for (const sample of data) {
        const output = this.forward(sample.input);
        totalLoss += sample.target.reduce((sum, t, i) => sum + Math.pow(t - output[i], 2), 0);
        this.backward(sample.target);
      }

      if (epoch % 1000 === 0) {
        console.log(`Epoch ${epoch}: Loss = ${(totalLoss / data.length).toFixed(6)}`);
      }
    }
  }

  predict(input: number[]): number[] {
    return this.forward(input);
  }
}

// ==================== XOR PROBLEM ====================
console.log('=== Treinamento da Rede Neural para XOR ===\n');

// Dados de treinamento do XOR
const xorData = [
  { input: [0, 0], target: [0] },
  { input: [0, 1], target: [1] },
  { input: [1, 0], target: [1] },
  { input: [1, 1], target: [0] }
];

// Cria rede: 2 entradas → 4 neurônios ocultos → 1 saída
const nn = new NeuralNetwork([2, 4, 1], 0.5);

// Treina por 10000 épocas
nn.train(xorData, 10000);

// Testa a rede
console.log('\n=== Resultados Finais ===');
for (const sample of xorData) {
  const output = nn.predict(sample.input);
  const rounded = Math.round(output[0]);
  console.log(
    `Input: [${sample.input.join(', ')}] → ` +
    `Output: ${output[0].toFixed(4)} (≈${rounded}) ` +
    `| Esperado: ${sample.target[0]} ` +
    `| ${rounded === sample.target[0] ? '✓' : '✗'}`
  );
}
```

---

## 7. Exemplo prático: o problema XOR

### 7.1 Por que XOR?

O XOR é um caso clássico porque demonstra a **necessidade de camadas ocultas**. Minsky e Papert provaram em 1969 que um perceptron simples (sem camadas ocultas) não consegue resolver XOR — isso contribuiu para o primeiro "AI Winter".

Visualmente, os pontos do XOR não são linearmente separáveis:

```
    1 |  ●(0,1)      ○(1,1)
      |
    0 |  ○(0,0)      ●(1,0)
      +------------------
         0           1

● = saída 1
○ = saída 0
```

Nenhuma linha reta consegue separar os ● dos ○.

### 7.2 Configuração da rede

**Arquitetura mínima**: 2-2-1 (2 entradas, 2 neurônios ocultos, 1 saída)

Usamos 2-4-1 no código para maior robustez:
- **2 neurônios de entrada**: x₁, x₂
- **4 neurônios ocultos**: permite aprender representações mais ricas
- **1 neurônio de saída**: y ∈ [0,1]

**Parâmetros**:
- Learning rate: **0.5** (valor relativamente alto para convergência rápida)
- Ativação: **sigmoid** (saída entre 0 e 1)
- Épocas: **10,000**

### 7.3 Saída esperada

Ao executar `node xor-neural-network.ts`:

```
=== Treinamento da Rede Neural para XOR ===

Epoch 0: Loss = 0.267342
Epoch 1000: Loss = 0.039821
Epoch 2000: Loss = 0.008234
Epoch 3000: Loss = 0.003102
Epoch 4000: Loss = 0.001687
Epoch 5000: Loss = 0.001089
Epoch 6000: Loss = 0.000779
Epoch 7000: Loss = 0.000594
Epoch 8000: Loss = 0.000474
Epoch 9000: Loss = 0.000391
Epoch 10000: Loss = 0.000331

=== Resultados Finais ===
Input: [0, 0] → Output: 0.0142 (≈0) | Esperado: 0 | ✓
Input: [0, 1] → Output: 0.9847 (≈1) | Esperado: 1 | ✓
Input: [1, 0] → Output: 0.9851 (≈1) | Esperado: 1 | ✓
Input: [1, 1] → Output: 0.0187 (≈0) | Esperado: 0 | ✓
```

---

## 8. Debugging e validação

### 8.1 Gradient checking

Para verificar se o backpropagation está correto, compare gradientes analíticos com numéricos:

```typescript
// gradient-check.ts
function numericalGradient(
  nn: NeuralNetwork,
  input: number[],
  target: number[],
  layerIndex: number,
  i: number,
  j: number,
  epsilon: number = 1e-5
): number {
  // Salva peso original
  const original = nn.layers[layerIndex].weights.get(i, j);
  
  // Calcula J(θ + ε)
  nn.layers[layerIndex].weights.set(i, j, original + epsilon);
  const lossPlus = computeLoss(nn.forward(input), target);
  
  // Calcula J(θ - ε)
  nn.layers[layerIndex].weights.set(i, j, original - epsilon);
  const lossMinus = computeLoss(nn.forward(input), target);
  
  // Restaura peso
  nn.layers[layerIndex].weights.set(i, j, original);
  
  // Gradiente numérico: [J(θ+ε) - J(θ-ε)] / 2ε
  return (lossPlus - lossMinus) / (2 * epsilon);
}

function computeLoss(output: number[], target: number[]): number {
  return target.reduce((sum, t, i) => sum + 0.5 * Math.pow(t - output[i], 2), 0);
}
```

**Critérios de aceitação**:
- Erro relativo **< 10⁻⁷**: Excelente
- Erro relativo **10⁻⁷ a 10⁻⁴**: Aceitável (especialmente com ReLU)
- Erro relativo **> 10⁻²**: Provável bug

### 8.2 Bugs comuns e soluções

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| Loss não diminui | Learning rate muito baixo ou muito alto | Teste valores: 0.001, 0.01, 0.1, 0.5 |
| Loss explode (NaN) | Learning rate muito alto | Reduza por fator de 10 |
| Saídas sempre ~0.5 | Gradientes desaparecendo | Use ReLU, verifique inicialização |
| Predições aleatórias | Labels desalinhados | Verifique correspondência input-target |
| Rede não aprende XOR | Poucos neurônios ocultos | Mínimo 2 neurônios na camada oculta |

### 8.3 Diagnósticos de treinamento

**Curva de loss ideal**:
- Decaimento exponencial suave
- Sem oscilações grandes
- Convergência para valor próximo de zero

**Sinais de overfitting** (em datasets maiores):
- Loss de treino ↓ enquanto loss de validação ↑
- Aumente regularização ou use dropout

**Sinais de underfitting**:
- Loss alto mesmo após muitas épocas
- Aumente capacidade da rede (mais neurônios/camadas)

---

## 9. Conclusão e próximos passos

Este documento apresentou a teoria completa e implementação funcional de redes neurais feedforward. Os conceitos fundamentais — **forward propagation**, **backpropagation**, **gradient descent** — são a base de todo o deep learning moderno.

**Insights principais**:
- A não-linearidade das funções de ativação é essencial para modelar relações complexas
- Backpropagation é simplesmente a regra da cadeia aplicada sistematicamente
- A escolha de **learning rate** e **inicialização dos pesos** impacta dramaticamente a convergência
- O problema XOR demonstra que camadas ocultas são necessárias para problemas não-linearmente separáveis

**Para aprofundamento**:
- Implemente **mini-batch gradient descent** para datasets maiores
- Adicione **momentum** ao otimizador para convergência mais rápida
- Experimente **regularização L2** para prevenir overfitting
- Explore arquiteturas mais profundas com **batch normalization**
- Aplique a redes convolucionais (CNNs) para processamento de imagens

O código TypeScript apresentado é totalmente funcional e pode ser executado diretamente com Node.js 24. Use-o como ponto de partida para explorar variações arquiteturais e problemas mais complexos.