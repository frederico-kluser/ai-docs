# Documentação Técnica Definitiva do TensorFlow.js
<!-- Arquivo renomeado para: documentacao-tensorflowjs-completa.md -->

Machine learning no navegador e Node.js atinge maturidade com **TensorFlow.js 4.x**, oferecendo aceleração GPU via WebGL/WebGPU e compatibilidade com modelos Python. Esta documentação técnica em português brasileiro serve como referência completa para desenvolvedores que buscam implementar soluções de ML em produção, desde operações matemáticas básicas até treinamento e inferência de modelos complexos.

---

## 1. Instalação rápida e detecção automática GPU/CPU

O TensorFlow.js **4.22.0** (versão estável atual) oferece múltiplas opções de instalação adaptadas ao ambiente de execução. Para aplicações browser, a biblioteca detecta automaticamente o melhor backend disponível, priorizando **WebGPU** > **WebGL** > **WASM** > **CPU**.

### Instalação via npm/yarn

```bash
# Browser - pacote principal com WebGL
npm install @tensorflow/tfjs

# Node.js com bindings nativos (recomendado para servidor)
npm install @tensorflow/tfjs-node

# Node.js com GPU CUDA (Linux apenas)
npm install @tensorflow/tfjs-node-gpu

# Backends opcionais para browser
npm install @tensorflow/tfjs-backend-wasm
npm install @tensorflow/tfjs-backend-webgpu
```

### Instalação via CDN

```html
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js"></script>
```

### Padrão de fallback GPU/CPU para produção

Este snippet detecta e inicializa o melhor backend disponível com fallback automático:

```typescript
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgpu';
import '@tensorflow/tfjs-backend-wasm';
import { setWasmPaths } from '@tensorflow/tfjs-backend-wasm';

interface BackendConfig {
  name: string;
  check: () => Promise<boolean>;
}

async function initializeBestBackend(): Promise<string> {
  setWasmPaths('/wasm/');
  
  const backends: BackendConfig[] = [
    {
      name: 'webgpu',
      check: async () => typeof navigator !== 'undefined' && 'gpu' in navigator
    },
    {
      name: 'webgl',
      check: async () => {
        if (typeof document === 'undefined') return false;
        const canvas = document.createElement('canvas');
        return !!(canvas.getContext('webgl2') || canvas.getContext('webgl'));
      }
    },
    {
      name: 'wasm',
      check: async () => typeof WebAssembly !== 'undefined'
    },
    {
      name: 'cpu',
      check: async () => true
    }
  ];

  for (const backend of backends) {
    try {
      if (await backend.check() && await tf.setBackend(backend.name)) {
        await tf.ready();
        console.log(`Backend inicializado: ${backend.name}`);
        return backend.name;
      }
    } catch (e) {
      console.warn(`Backend ${backend.name} falhou:`, e);
    }
  }
  throw new Error('Nenhum backend disponível');
}

// Uso em produção
async function main() {
  const backend = await initializeBestBackend();
  tf.enableProdMode(); // Desabilita validações para performance
  // Código ML aqui
}
```

### Comparativo de performance dos backends

| Backend | Velocidade | Melhor Uso |
|---------|-----------|------------|
| **WebGPU** | Mais rápido (browser) | Modelos grandes, Chrome 113+ |
| **WebGL** | Rápido | Uso geral em browsers |
| **WASM** | Moderado | Modelos pequenos (<3MB), dispositivos móveis |
| **tfjs-node** | Muito rápido | Servidor, treinamento |
| **CPU** | Lento | Fallback, testes |

---

## 2. Operações matemáticas e tensores

Tensores são a estrutura de dados fundamental do TensorFlow.js, representando arrays multidimensionais com **dtype** fixo. Todas as operações são imutáveis — cada operação cria um novo tensor.

### Criação de tensores

```typescript
// Assinaturas principais
tf.tensor(values: TypedArray | Array, shape?: number[], dtype?: DataType): tf.Tensor
tf.scalar(value: number | boolean, dtype?: DataType): tf.Scalar
tf.zeros(shape: number[], dtype?: DataType): tf.Tensor
tf.ones(shape: number[], dtype?: DataType): tf.Tensor
tf.fill(shape: number[], value: number): tf.Tensor
tf.linspace(start: number, stop: number, num: number): tf.Tensor1D
tf.range(start: number, stop: number, step?: number): tf.Tensor1D

// Exemplos práticos
const tensor = tf.tensor([[1, 2], [3, 4]]);           // Shape inferido [2, 2]
const explicito = tf.tensor([1, 2, 3, 4], [2, 2]);   // Shape explícito
const zeros = tf.zeros([3, 3]);                       // Matriz 3x3 de zeros
const sequencia = tf.linspace(0, 1, 5);               // [0, 0.25, 0.5, 0.75, 1]

// Tensores aleatórios
tf.randomNormal([2, 2], 0, 1);       // Distribuição normal μ=0, σ=1
tf.randomUniform([2, 2], 0, 1);      // Uniforme [0, 1)
tf.truncatedNormal([2, 2]);          // Normal truncada (valores > 2σ rejeitados)

// Variáveis mutáveis (para treinamento)
const v = tf.variable(tf.tensor([1, 2, 3]));
v.assign(tf.tensor([4, 5, 6]));      // Única forma de alterar valor
```

### Manipulação de tensores

```typescript
// Reshape - total de elementos deve coincidir
const a = tf.tensor1d([1, 2, 3, 4, 5, 6]);
a.reshape([2, 3]).print();            // [[1,2,3], [4,5,6]]

// Slice - extração de subconjunto
const x = tf.tensor2d([[1, 2, 3], [4, 5, 6]]);
x.slice([0, 1], [2, 2]).print();      // [[2,3], [5,6]] - início [0,1], tamanho [2,2]

// Concat - concatenação ao longo de eixo
const b = tf.tensor2d([[7, 8, 9]]);
tf.concat([x, b], 0).print();         // Concatena verticalmente

// Stack/Unstack - adiciona/remove dimensão
const v1 = tf.tensor1d([1, 2]);
const v2 = tf.tensor1d([3, 4]);
tf.stack([v1, v2]).print();           // [[1,2], [3,4]] - nova dimensão axis=0

// Transpose
x.transpose().print();                 // Transposta da matriz

// ExpandDims/Squeeze
const vec = tf.tensor1d([1, 2, 3]);
vec.expandDims(0).print();            // Shape: [1, 3] - adiciona batch dimension
```

### Operações matemáticas element-wise

```typescript
// Aritmética básica
const a = tf.tensor([1, 2, 3, 4]);
const b = tf.tensor([10, 20, 30, 40]);

a.add(b).print();     // [11, 22, 33, 44]
a.sub(b).print();     // [-9, -18, -27, -36]
a.mul(b).print();     // [10, 40, 90, 160]
a.div(b).print();     // [0.1, 0.1, 0.1, 0.1]
a.pow(tf.scalar(2)).print();  // [1, 4, 9, 16]

// Funções unárias
a.sqrt().print();     // [1, 1.41, 1.73, 2]
a.square().print();   // [1, 4, 9, 16]
a.exp().print();      // [e¹, e², e³, e⁴]
a.log().print();      // [0, 0.69, 1.1, 1.39]
a.abs().print();      // Valor absoluto

// Trigonometria
tf.sin(a).print();
tf.cos(a).print();

// Ativações como operações
tf.sigmoid(a).print();   // 1/(1+e^(-x))
tf.relu(a).print();      // max(0, x)
tf.softmax(a).print();   // Normalização probabilística
```

### Álgebra linear

```typescript
// Multiplicação de matrizes
const m1 = tf.tensor2d([[1, 2], [3, 4]]);
const m2 = tf.tensor2d([[5, 6], [7, 8]]);
m1.matMul(m2).print();    // [[19, 22], [43, 50]]

// Produto escalar
const v1 = tf.tensor1d([1, 2, 3]);
const v2 = tf.tensor1d([4, 5, 6]);
v1.dot(v2).print();       // 32 (1*4 + 2*5 + 3*6)

// Norma
v1.euclideanNorm().print();  // √(1+4+9) = 3.74

// Einsum - notação Einstein para operações tensoriais
const x = tf.tensor2d([[1, 2], [3, 4]]);
tf.einsum('ij->ji', x).print();        // Transposta
tf.einsum('ij,jk->ik', m1, m2).print(); // matMul

// Decomposição QR
const [q, r] = tf.linalg.qr(m1);
q.print(); r.print();
```

### Operações estatísticas e de redução

```typescript
const x = tf.tensor2d([[1, 2, 3], [4, 5, 6]]);

// Reduções globais
x.sum().print();          // 21
x.mean().print();         // 3.5
x.min().print();          // 1
x.max().print();          // 6

// Reduções ao longo de eixo
x.sum(0).print();         // [5, 7, 9] - soma colunas
x.sum(1).print();         // [6, 15] - soma linhas
x.mean(1, true).print();  // [[2], [5]] - keepDims=true mantém dimensão

// Índices de min/max
x.argMax(1).print();      // [2, 2] - índice do máximo em cada linha

// Momentos estatísticos
const {mean, variance} = tf.moments(x);
mean.print();
variance.print();

// Top-K
const {values, indices} = tf.topk(tf.tensor1d([3, 1, 4, 1, 5]), 3);
values.print();   // [5, 4, 3]
indices.print();  // [4, 2, 0]
```

### Comparação e operações lógicas

```typescript
const a = tf.tensor1d([1, 2, 3, 4]);
const b = tf.tensor1d([2, 2, 2, 2]);

// Comparações retornam tensores booleanos
a.greater(b).print();      // [false, false, true, true]
a.equal(b).print();        // [false, true, false, false]
a.lessEqual(b).print();    // [true, true, false, false]

// Operações lógicas
const cond = tf.tensor1d([true, false, true], 'bool');
tf.logicalNot(cond).print();  // [false, true, false]

// where - seleção condicional
tf.where(
  tf.tensor1d([true, false, true], 'bool'),
  tf.tensor1d([1, 2, 3]),
  tf.tensor1d([4, 5, 6])
).print();  // [1, 5, 3]
```

### Broadcasting - regras de propagação de dimensões

O broadcasting alinha dimensões da **direita para esquerda**, expandindo automaticamente dimensões de tamanho 1:

```typescript
// Matriz [2,3] + Vetor [3] = Matriz [2,3]
const matrix = tf.tensor2d([[1, 2, 3], [4, 5, 6]]);
const vector = tf.tensor1d([10, 20, 30]);
matrix.add(vector).print();  // [[11,22,33], [14,25,36]]

// Coluna [3,1] + Linha [1,4] = Matriz [3,4]
const col = tf.tensor2d([[1], [2], [3]]);
const row = tf.tensor2d([[1, 2, 3, 4]]);
col.add(row).print();  // Broadcast para [3,4]

// ERRO: shapes incompatíveis [3] e [4] - não pode fazer broadcast
// tf.add(tf.tensor1d([1,2,3]), tf.tensor1d([1,2,3,4])); // Erro!
```

### Quando usar TensorFlow.js vs JavaScript nativo para matemática

| Cenário | Recomendação |
|---------|-------------|
| Arrays pequenos (<100 elementos) | JavaScript nativo (menor overhead) |
| Operações matriciais grandes | TensorFlow.js (aceleração GPU) |
| Loops sobre elementos individuais | JavaScript nativo |
| Operações batch/vetorizadas | TensorFlow.js |
| Precisão crítica (financeiro) | JavaScript nativo (controle total) |
| Pipeline de ML | TensorFlow.js (integração) |

---

## 3. Pipeline de dados e pré-processamento

A API `tf.data` oferece um pipeline declarativo para processamento de dados com transformações encadeadas, otimizado para treinamento de modelos.

### tf.data.Dataset - criação de datasets

```typescript
// A partir de arrays
const dataset = tf.data.array([1, 2, 3, 4, 5]);

// A partir de generator (para dados sob demanda)
function* dataGenerator() {
  for (let i = 0; i < 100; i++) {
    yield { x: i, y: i * 2 };
  }
}
const genDataset = tf.data.generator(dataGenerator);

// CSV remoto
const csvDataset = tf.data.csv('https://example.com/data.csv', {
  columnConfigs: {
    label: { isLabel: true }
  }
});

// Webcam (browser)
const webcam = await tf.data.webcam(videoElement, {
  resizeWidth: 224,
  resizeHeight: 224,
  centerCrop: true
});
const frame = await webcam.capture();

// Microfone (browser)
const mic = await tf.data.microphone({
  fftSize: 1024,
  numFramesPerSpectrogram: 10
});
```

### Transformações de dataset

```typescript
const dataset = tf.data.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

// Shuffle - embaralha com buffer
const shuffled = dataset.shuffle(5, 'seed123');

// Map - transforma cada elemento
const doubled = dataset.map(x => x * 2);

// Filter - filtra elementos
const evens = dataset.filter(x => x % 2 === 0);

// Batch - agrupa em lotes
const batched = dataset.batch(3);  // [[1,2,3], [4,5,6], [7,8,9], [10]]

// Repeat - repete dataset
const repeated = dataset.repeat(3);  // Repete 3 vezes

// Take/Skip - limita/pula elementos
const first5 = dataset.take(5);
const after3 = dataset.skip(3);

// Prefetch - otimização de I/O
const optimized = dataset.prefetch(2);

// Pipeline completo de treinamento (ordem recomendada)
const trainingPipeline = tf.data.array(dados)
  .shuffle(1000)      // 1. Shuffle primeiro
  .map(normalize)     // 2. Transformações
  .batch(32)          // 3. Batch
  .prefetch(1);       // 4. Prefetch no final
```

### Pré-processamento de imagens

```typescript
// Carregar imagem como tensor
const imgTensor = tf.browser.fromPixels(imageElement, 3);  // 3 canais RGB

// Resize
const resized = tf.image.resizeBilinear(imgTensor, [224, 224]);
const nearestNeighbor = tf.image.resizeNearestNeighbor(imgTensor, [224, 224]);

// Crop and Resize
const boxes = tf.tensor2d([[0, 0, 1, 1]]);  // [y1, x1, y2, x2] normalizados
const boxInd = tf.tensor1d([0], 'int32');
const cropped = tf.image.cropAndResize(
  imgTensor.expandDims(0) as tf.Tensor4D,
  boxes,
  boxInd,
  [224, 224]
);

// Flip horizontal
const flipped = tf.image.flipLeftRight(imgTensor.expandDims(0) as tf.Tensor4D);

// Conversão de cores
const grayscale = tf.image.rgbToGrayscale(imgTensor);
const rgb = tf.image.grayscaleToRGB(grayscale);

// Pipeline completo de pré-processamento
function preprocessImage(img: HTMLImageElement): tf.Tensor4D {
  return tf.tidy(() => {
    let tensor = tf.browser.fromPixels(img);
    tensor = tf.image.resizeBilinear(tensor, [224, 224]);
    tensor = tensor.toFloat().div(255);  // Normaliza para [0, 1]
    return tensor.expandDims(0) as tf.Tensor4D;  // Adiciona batch dimension
  });
}
```

### Normalização

```typescript
// Min-Max para [0, 1]
function minMaxNormalize(tensor: tf.Tensor): tf.Tensor {
  return tf.tidy(() => {
    const min = tensor.min();
    const max = tensor.max();
    return tensor.sub(min).div(max.sub(min));
  });
}

// Z-score (média 0, variância 1)
function zScoreNormalize(tensor: tf.Tensor): tf.Tensor {
  return tf.tidy(() => {
    const mean = tensor.mean();
    const std = tensor.sub(mean).square().mean().sqrt();
    return tensor.sub(mean).div(std);
  });
}

// ImageNet normalization (para modelos pré-treinados)
function imagenetNormalize(tensor: tf.Tensor): tf.Tensor {
  const mean = tf.tensor([0.485, 0.456, 0.406]);
  const std = tf.tensor([0.229, 0.224, 0.225]);
  return tensor.sub(mean).div(std);
}
```

### One-hot encoding

```typescript
// Assinatura
tf.oneHot(indices: tf.Tensor | number[], depth: number): tf.Tensor

// Exemplo
const labels = tf.tensor1d([0, 1, 2, 3], 'int32');
const oneHot = tf.oneHot(labels, 4);
oneHot.print();
// [[1, 0, 0, 0],
//  [0, 1, 0, 0],
//  [0, 0, 1, 0],
//  [0, 0, 0, 1]]

// Label encoder customizado
function createLabelEncoder(labels: string[]) {
  const unique = [...new Set(labels)].sort();
  const toIndex = new Map(unique.map((l, i) => [l, i]));
  return {
    encode: (label: string) => toIndex.get(label)!,
    decode: (idx: number) => unique[idx],
    numClasses: unique.length
  };
}
```

---

## 4. Construção de modelos: Sequential vs Functional

O TensorFlow.js oferece duas APIs para construção de modelos: **Sequential** para redes lineares simples e **Functional** para arquiteturas complexas.

### Sequential API

```typescript
// Método 1: Constructor com array
const model = tf.sequential({
  layers: [
    tf.layers.dense({inputShape: [784], units: 128, activation: 'relu'}),
    tf.layers.dropout({rate: 0.2}),
    tf.layers.dense({units: 64, activation: 'relu'}),
    tf.layers.dense({units: 10, activation: 'softmax'})
  ]
});

// Método 2: add() incremental
const model = tf.sequential();
model.add(tf.layers.dense({inputShape: [784], units: 128, activation: 'relu'}));
model.add(tf.layers.dense({units: 10, activation: 'softmax'}));

// Visualizar arquitetura
model.summary();
```

### Functional API

```typescript
// Entrada explícita
const input = tf.input({shape: [784]});

// Camadas aplicadas via .apply()
const x = tf.layers.dense({units: 128, activation: 'relu'}).apply(input);
const x2 = tf.layers.dropout({rate: 0.2}).apply(x);
const output = tf.layers.dense({units: 10, activation: 'softmax'}).apply(x2);

// Criar modelo
const model = tf.model({inputs: input, outputs: output});

// Múltiplas entradas
const input1 = tf.input({shape: [32], name: 'numeric'});
const input2 = tf.input({shape: [100], name: 'text'});
const branch1 = tf.layers.dense({units: 16}).apply(input1);
const branch2 = tf.layers.dense({units: 32}).apply(input2);
const merged = tf.layers.concatenate().apply([branch1, branch2]);
const out = tf.layers.dense({units: 1, activation: 'sigmoid'}).apply(merged);
const multiInputModel = tf.model({inputs: [input1, input2], outputs: out});

// Múltiplas saídas
const shared = tf.layers.dense({units: 64}).apply(input);
const classOutput = tf.layers.dense({units: 10, activation: 'softmax', name: 'class'}).apply(shared);
const regOutput = tf.layers.dense({units: 1, name: 'regression'}).apply(shared);
const multiOutputModel = tf.model({inputs: input, outputs: [classOutput, regOutput]});
```

### Matriz de decisão: quando usar cada API

| Característica | Sequential | Functional |
|----------------|-----------|------------|
| Topologia linear | ✅ | ✅ |
| Múltiplas entradas | ❌ | ✅ |
| Múltiplas saídas | ❌ | ✅ |
| Skip connections (ResNet) | ❌ | ✅ |
| Camadas compartilhadas | ❌ | ✅ |
| Complexidade de código | ⭐ | ⭐⭐ |
| Depuração | Mais fácil | Mais controle |

**Regra prática**: Use Sequential para redes feedforward simples. Use Functional para qualquer arquitetura com ramificações ou conexões residuais.

---

## 5. Camadas disponíveis - referência exaustiva

### Camadas Core

```typescript
// Dense - totalmente conectada
tf.layers.dense({
  units: number,                              // Obrigatório
  inputShape?: number[],                      // Obrigatório na primeira camada
  activation?: 'relu' | 'sigmoid' | 'softmax' | 'tanh' | 'linear' | ...,
  useBias?: boolean,                          // Default: true
  kernelInitializer?: string,                 // Default: 'glorotUniform'
  biasInitializer?: string,                   // Default: 'zeros'
  kernelRegularizer?: tf.regularizers.l1({l1: 0.01}) | tf.regularizers.l2({l2: 0.01}),
  biasRegularizer?: Regularizer,
  activityRegularizer?: Regularizer
})

// Dropout - regularização
tf.layers.dropout({rate: 0.5})

// Flatten - achata para 1D
tf.layers.flatten()

// Reshape
tf.layers.reshape({targetShape: [7, 7, 256]})

// Permute - reordena eixos
tf.layers.permute({dims: [2, 1]})
```

### Camadas convolucionais

```typescript
// Conv2D
tf.layers.conv2d({
  filters: 32,                               // Número de filtros
  kernelSize: 3,                             // Ou [3, 3]
  strides: [1, 1],                           // Default: [1, 1]
  padding: 'same' | 'valid',                 // Default: 'valid'
  activation: 'relu',
  dataFormat: 'channelsLast',                // Default
  dilationRate: [1, 1],
  kernelInitializer: 'glorotUniform',
  kernelRegularizer: tf.regularizers.l2({l2: 0.0001})
})

// Conv1D - para sequências
tf.layers.conv1d({filters: 64, kernelSize: 3, activation: 'relu'})

// Conv2DTranspose - deconvolução
tf.layers.conv2dTranspose({filters: 32, kernelSize: 3, strides: 2})

// SeparableConv2D - eficiente em memória
tf.layers.separableConv2d({filters: 64, kernelSize: 3})

// DepthwiseConv2D
tf.layers.depthwiseConv2d({kernelSize: 3, depthMultiplier: 1})

// UpSampling2D
tf.layers.upSampling2d({size: [2, 2], interpolation: 'nearest'})
```

### Camadas de pooling

```typescript
// MaxPooling
tf.layers.maxPooling2d({poolSize: [2, 2], strides: [2, 2], padding: 'valid'})
tf.layers.maxPooling1d({poolSize: 2})

// AveragePooling
tf.layers.averagePooling2d({poolSize: [2, 2]})
tf.layers.averagePooling1d({poolSize: 2})

// GlobalPooling - reduz espacialmente para 1 valor por filtro
tf.layers.globalMaxPooling2d()
tf.layers.globalAveragePooling2d()  // Comum antes de Dense final em CNNs
```

### Camadas recorrentes

```typescript
// LSTM
tf.layers.lstm({
  units: 128,                                // Dimensionalidade do output
  activation: 'tanh',                        // Default
  recurrentActivation: 'sigmoid',            // Default: 'hardSigmoid'
  returnSequences: false,                    // True para empilhar LSTMs
  returnState: false,                        // Retorna estado final
  dropout: 0.1,                              // Dropout nas entradas
  recurrentDropout: 0.1,                     // Dropout nas conexões recorrentes
  unroll: false,                             // Desrola para performance (mais memória)
  stateful: false                            // Mantém estado entre batches
})

// GRU - mais leve que LSTM
tf.layers.gru({
  units: 64,
  returnSequences: true,
  dropout: 0.2
})

// SimpleRNN - básica
tf.layers.simpleRNN({units: 32})

// Bidirectional - processa em ambas direções
tf.layers.bidirectional({
  layer: tf.layers.lstm({units: 64}),
  mergeMode: 'concat'  // 'sum' | 'mul' | 'ave' | 'concat'
})

// TimeDistributed - aplica camada a cada timestep
tf.layers.timeDistributed({
  layer: tf.layers.dense({units: 32})
})

// ConvLSTM2D - para vídeo
tf.layers.convLstm2d({
  filters: 32,
  kernelSize: 3,
  returnSequences: true
})
```

### Camadas de normalização

```typescript
// BatchNormalization - normaliza por batch
tf.layers.batchNormalization({
  axis: -1,                                  // Eixo do canal
  momentum: 0.99,                            // Momentum para média móvel
  epsilon: 0.001,                            // Previne divisão por zero
  center: true,                              // Adiciona offset beta
  scale: true                                // Multiplica por gamma
})

// LayerNormalization - normaliza por amostra (bom para RNNs/Transformers)
tf.layers.layerNormalization({
  axis: -1,
  epsilon: 0.001
})
```

### Embedding

```typescript
tf.layers.embedding({
  inputDim: 10000,                           // Tamanho do vocabulário
  outputDim: 128,                            // Dimensão do embedding
  inputLength: 100,                          // Comprimento da sequência
  embeddingsInitializer: 'uniform',
  maskZero: false                            // True se 0 é padding
})
```

### Camadas de merge

```typescript
// Todas aceitam array de tensores
tf.layers.add()                              // Soma element-wise
tf.layers.multiply()                         // Produto element-wise
tf.layers.average()                          // Média element-wise
tf.layers.maximum()                          // Máximo element-wise
tf.layers.minimum()                          // Mínimo element-wise
tf.layers.concatenate({axis: -1})            // Concatenação

// Uso no Functional API
const merged = tf.layers.concatenate().apply([branch1, branch2]);
```

### Camadas de ativação avançadas

```typescript
tf.layers.activation({activation: 'relu'})   // Standalone
tf.layers.leakyReLU({alpha: 0.3})            // max(alpha*x, x)
tf.layers.elu({alpha: 1.0})                  // x if x>0, alpha*(exp(x)-1) if x<0
tf.layers.prelu()                            // alpha aprendido por canal
tf.layers.softmax({axis: -1})
tf.layers.thresholdedReLU({theta: 1.0})
```

### Funções de ativação disponíveis (strings)

| Ativação | Fórmula | Uso Típico |
|----------|---------|-----------|
| `'relu'` | max(0, x) | Hidden layers padrão |
| `'sigmoid'` | 1/(1+e^-x) | Classificação binária (output) |
| `'softmax'` | e^xi / Σe^xj | Classificação multi-classe (output) |
| `'tanh'` | (e^x - e^-x)/(e^x + e^-x) | RNNs, valores [-1, 1] |
| `'linear'` | x | Regressão (output) |
| `'elu'` | x if x>0, α(e^x-1) if x<0 | Alternativa a ReLU |
| `'selu'` | λ * elu(x, α) | Self-normalizing networks |
| `'swish'` | x * sigmoid(x) | Arquiteturas modernas |
| `'softplus'` | log(1 + e^x) | Suave aproximação de ReLU |

---

## 6. Treinamento e otimização

### Compilação do modelo

```typescript
model.compile({
  optimizer: 'adam',                         // String ou instância
  loss: 'categoricalCrossentropy',           // Função de perda
  metrics: ['accuracy']                      // Métricas de avaliação
});
```

### Funções de perda disponíveis

| Loss | Uso | String |
|------|-----|--------|
| Categorical Crossentropy | Multi-classe (one-hot labels) | `'categoricalCrossentropy'` |
| Sparse Categorical Crossentropy | Multi-classe (integer labels) | `'sparseCategoricalCrossentropy'` |
| Binary Crossentropy | Binária | `'binaryCrossentropy'` |
| Mean Squared Error | Regressão | `'meanSquaredError'` |
| Mean Absolute Error | Regressão robusta | `'meanAbsoluteError'` |
| Huber Loss | Regressão (outliers) | `tf.losses.huberLoss` |

```typescript
// Loss customizado
const customLoss = (yTrue: tf.Tensor, yPred: tf.Tensor) => {
  return tf.losses.softmaxCrossEntropy(yTrue, yPred).mean();
};

model.compile({optimizer: 'adam', loss: customLoss});
```

### Otimizadores

```typescript
// SGD com momentum
tf.train.sgd(learningRate: number)
tf.train.momentum(learningRate: number, momentum: number)

// Adaptativos
tf.train.adam(learningRate?: number, beta1?: number, beta2?: number, epsilon?: number)
// Defaults: lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-7

tf.train.adamax(learningRate?: number)
tf.train.rmsprop(learningRate: number, decay?: number, momentum?: number)
tf.train.adagrad(learningRate: number)
tf.train.adadelta(learningRate?: number, rho?: number)
```

| Otimizador | Quando Usar | Learning Rate Típica |
|------------|-------------|---------------------|
| **Adam** | Default para maioria dos casos | 0.001 |
| **SGD + Momentum** | Fine-tuning, convergência mais estável | 0.01 |
| **RMSprop** | RNNs, objetivos não-estacionários | 0.001 |
| **Adagrad** | Features esparsas (NLP) | 0.01 |
| **Adamax** | Grandes vocabulários | 0.002 |

### Métodos de treinamento

```typescript
// model.fit() - principal
const history = await model.fit(xTrain, yTrain, {
  epochs: 100,
  batchSize: 32,
  validationSplit: 0.2,                      // 20% para validação
  validationData: [xVal, yVal],              // Ou dados explícitos
  shuffle: true,                             // Embaralha a cada época
  callbacks: {
    onEpochEnd: async (epoch, logs) => {
      console.log(`Época ${epoch}: loss=${logs?.loss?.toFixed(4)}`);
      await tf.nextFrame();                  // Permite atualização da UI
    }
  }
});

// model.fitDataset() - para tf.data.Dataset
await model.fitDataset(dataset, {
  epochs: 50,
  validationData: valDataset
});

// model.trainOnBatch() - treinamento batch a batch
const metrics = await model.trainOnBatch(xBatch, yBatch);
```

### Callbacks

```typescript
// Early Stopping built-in
const earlyStopping = tf.callbacks.earlyStopping({
  monitor: 'val_loss',
  patience: 10,                              // Épocas sem melhora
  minDelta: 0.001,                           // Melhora mínima
  mode: 'min',                               // 'min' | 'max' | 'auto'
  restoreBestWeights: true
});

// Callback customizado
class LRScheduler extends tf.Callback {
  async onEpochEnd(epoch: number, logs?: tf.Logs) {
    if (epoch > 0 && epoch % 10 === 0) {
      const currentLR = (this.model.optimizer as any).learningRate;
      this.model.optimizer.setLearningRate(currentLR * 0.9);
    }
  }
}

await model.fit(x, y, {
  epochs: 100,
  callbacks: [earlyStopping, new LRScheduler()]
});
```

### Computação de gradientes

```typescript
// tf.grad() - gradiente de função escalar
const f = (x: tf.Tensor) => x.square().mean();
const gradF = tf.grad(f);
gradF(tf.tensor([1, 2, 3])).print();  // Derivada

// tf.variableGrads() - gradientes para variáveis
const w = tf.variable(tf.randomNormal([2, 2]));
const {value, grads} = tf.variableGrads(() => {
  return tf.sum(w.square());
});
console.log('Gradiente:', grads);

// Loop de treinamento customizado
const optimizer = tf.train.adam(0.001);

function trainStep(x: tf.Tensor, y: tf.Tensor): tf.Scalar {
  return tf.tidy(() => {
    const loss = optimizer.minimize(() => {
      const pred = model.predict(x) as tf.Tensor;
      return tf.losses.softmaxCrossEntropy(y, pred).mean();
    }, true) as tf.Scalar;
    return loss;
  });
}
```

---

## 7. Inferência e deploy

### Predição

```typescript
// model.predict() - inferência padrão
const predictions = model.predict(inputTensor, {
  batchSize: 32,
  verbose: false
}) as tf.Tensor;

// model.predictOnBatch() - sem overhead de batching
const batchPredictions = model.predictOnBatch(batchTensor) as tf.Tensor;

// Pós-processamento típico
const probabilities = await predictions.data();
const classIndex = predictions.argMax(-1).dataSync()[0];
```

### Salvamento de modelos

```typescript
// Browser - IndexedDB (recomendado)
await model.save('indexeddb://meu-modelo');

// Browser - LocalStorage (modelos pequenos)
await model.save('localstorage://meu-modelo');

// Browser - Download como arquivos
await model.save('downloads://meu-modelo');  // Gera model.json + weights.bin

// Node.js - Sistema de arquivos
await model.save('file://./modelo');

// HTTP - Upload para servidor
await model.save('http://servidor.com/upload');

// Com headers customizados
await model.save(tf.io.browserHTTPRequest(
  'http://api.exemplo.com/models',
  {method: 'PUT', headers: {'Authorization': 'Bearer token'}}
));
```

### Carregamento de modelos

```typescript
// tf.loadLayersModel() - modelos Keras/Layers (treináveis)
const model = await tf.loadLayersModel('indexeddb://meu-modelo');
const model = await tf.loadLayersModel('https://cdn.exemplo.com/model.json');

// tf.loadGraphModel() - modelos convertidos (inferência apenas, mais rápidos)
const graphModel = await tf.loadGraphModel('https://cdn.exemplo.com/model.json');
const graphModel = await tf.loadGraphModel(
  'https://tfhub.dev/google/model/1',
  {fromTFHub: true}
);

// Carregar de arquivos locais (browser)
const model = await tf.loadLayersModel(
  tf.io.browserFiles([jsonFile, weightsFile])
);

// Gerenciamento de modelos salvos
const models = await tf.io.listModels();   // Lista todos
await tf.io.removeModel('indexeddb://antigo');
await tf.io.copyModel('indexeddb://a', 'localstorage://b');
```

### Quantização e otimização

A quantização reduz o tamanho do modelo convertendo pesos de float32 para formatos menores:

```bash
# Converter modelo Python com quantização
tensorflowjs_converter \
  --input_format=tf_saved_model \
  --output_format=tfjs_graph_model \
  --quantize_float16 \
  ./saved_model \
  ./web_model

# Opções de quantização
# --quantize_float16  → ~50% menor, mínima perda de precisão
# --quantize_uint16   → ~50% menor
# --quantize_uint8    → ~75% menor, pode afetar precisão
```

| Quantização | Redução | Impacto na Precisão | Uso |
|-------------|---------|---------------------|-----|
| Nenhuma (float32) | 0% | Nenhum | Desenvolvimento |
| float16 | ~50% | Mínimo | Produção com GPU |
| uint8 | ~75% | Moderado | Mobile, edge |

---

## 8. Modelos pré-treinados e transfer learning

### Modelos oficiais disponíveis

**Classificação de Imagens**
```typescript
import * as mobilenet from '@tensorflow-models/mobilenet';
const model = await mobilenet.load();
const predictions = await model.classify(imageElement);
// [{className: 'tabby cat', probability: 0.98}, ...]
```

**Detecção de Objetos**
```typescript
import * as cocoSsd from '@tensorflow-models/coco-ssd';
const model = await cocoSsd.load({base: 'mobilenet_v2'});
const predictions = await model.detect(image);
// [{bbox: [x, y, w, h], class: 'person', score: 0.95}, ...]
```

**Pose Estimation**
```typescript
import * as poseDetection from '@tensorflow-models/pose-detection';
const detector = await poseDetection.createDetector(
  poseDetection.SupportedModels.MoveNet,
  {modelType: poseDetection.movenet.modelType.SINGLEPOSE_LIGHTNING}
);
const poses = await detector.estimatePoses(video);
// 17 keypoints: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles
```

**Detecção Facial**
```typescript
import * as faceLandmarksDetection from '@tensorflow-models/face-landmarks-detection';
const detector = await faceLandmarksDetection.createDetector(
  faceLandmarksDetection.SupportedModels.MediaPipeFaceMesh,
  {runtime: 'tfjs', maxFaces: 1}
);
const faces = await detector.estimateFaces(image);
// 478 landmarks 3D por face
```

**Hand Tracking**
```typescript
import * as handPoseDetection from '@tensorflow-models/hand-pose-detection';
const detector = await handPoseDetection.createDetector(
  handPoseDetection.SupportedModels.MediaPipeHands,
  {runtime: 'tfjs', maxHands: 2}
);
const hands = await detector.estimateHands(image);
// 21 keypoints por mão
```

**NLP**
```typescript
// Universal Sentence Encoder - embeddings semânticos
import * as use from '@tensorflow-models/universal-sentence-encoder';
const model = await use.load();
const embeddings = await model.embed(['Hello world', 'Hi there']);
// Shape: [2, 512]

// Toxicity Classifier
import * as toxicity from '@tensorflow-models/toxicity';
const model = await toxicity.load(0.9);
const predictions = await model.classify(['texto a verificar']);
```

### Transfer learning workflow

```typescript
// 1. Carregar modelo base
const baseModel = await tf.loadLayersModel('mobilenet_url');

// 2. Obter camada de features (remover classificador)
const featureLayer = baseModel.getLayer('conv_pw_13_relu');
const featureExtractor = tf.model({
  inputs: baseModel.inputs,
  outputs: featureLayer.output
});

// 3. Congelar camadas base
featureExtractor.layers.forEach(layer => layer.trainable = false);

// 4. Adicionar classificador customizado
const input = tf.input({shape: featureExtractor.outputs[0].shape.slice(1)});
let x = tf.layers.flatten().apply(input);
x = tf.layers.dense({units: 128, activation: 'relu'}).apply(x);
x = tf.layers.dropout({rate: 0.5}).apply(x);
const output = tf.layers.dense({units: NUM_CLASSES, activation: 'softmax'}).apply(x);
const classifier = tf.model({inputs: input, outputs: output});

// 5. Pipeline de inferência
async function classify(image: HTMLImageElement) {
  const features = featureExtractor.predict(preprocessImage(image));
  return classifier.predict(features);
}

// 6. Fine-tuning (descongelar últimas camadas)
for (let i = baseModel.layers.length - 5; i < baseModel.layers.length; i++) {
  baseModel.layers[i].trainable = true;
}

// 7. Treinar com learning rate baixa
classifier.compile({
  optimizer: tf.train.adam(0.0001),  // LR baixa para fine-tuning
  loss: 'categoricalCrossentropy'
});
```

### KNN Classifier (sem treinamento)

```typescript
import * as knnClassifier from '@tensorflow-models/knn-classifier';
import * as mobilenet from '@tensorflow-models/mobilenet';

const classifier = knnClassifier.create();
const net = await mobilenet.load();

// Adicionar exemplos
function addExample(image: HTMLImageElement, classId: number) {
  const embedding = net.infer(image, true);  // Extrai features
  classifier.addExample(embedding, classId);
}

// Classificar
async function predict(image: HTMLImageElement) {
  const embedding = net.infer(image, true);
  return await classifier.predictClass(embedding);
  // {label: '0', confidences: {0: 0.9, 1: 0.1}, classIndex: 0}
}
```

---

## 9. Gerenciamento de memória e performance

### Descarte de tensores

```typescript
// Manual - dispose()
const tensor = tf.tensor([1, 2, 3]);
// ... uso
tensor.dispose();

// Automático - tf.tidy() (RECOMENDADO)
const result = tf.tidy(() => {
  const a = tf.tensor([1, 2, 3]);
  const b = tf.tensor([4, 5, 6]);
  const sum = a.add(b);
  return sum.square();  // Apenas este tensor é mantido
});
// a, b, sum são automaticamente descartados

// Para operações assíncronas
async function predict(input: tf.Tensor): Promise<Float32Array> {
  const output = model.predict(input) as tf.Tensor;
  const data = await output.data();  // Copia para CPU
  output.dispose();  // Descarta tensor GPU
  return data as Float32Array;
}
```

### Monitoramento de memória

```typescript
// Verificar uso atual
console.log(tf.memory());
// {numTensors: 42, numDataBuffers: 42, numBytes: 168000, unreliable: false}

// Profile de operações
const profile = await tf.profile(() => {
  return model.predict(input);
});
console.log(`Peak bytes: ${profile.peakBytes}`);
profile.kernels.forEach(k => {
  console.log(`${k.name}: ${k.kernelTimeMs}ms`);
});

// Debug mode (loga todas operações)
tf.enableDebugMode();
```

### Padrões para evitar memory leaks

```typescript
// ✅ Loop de inferência correto
async function runInferenceLoop(video: HTMLVideoElement) {
  while (running) {
    const prediction = tf.tidy(() => {
      const frame = tf.browser.fromPixels(video);
      const processed = preprocess(frame);
      return model.predict(processed);
    });
    
    const data = await prediction.data();
    prediction.dispose();
    
    renderResults(data);
    await tf.nextFrame();  // Yield para browser
  }
}

// ✅ Warmup antes de produção
async function warmupModel(model: tf.LayersModel, inputShape: number[]) {
  const dummy = tf.zeros([1, ...inputShape]);
  const warmup = model.predict(dummy) as tf.Tensor;
  await warmup.data();  // Força compilação
  warmup.dispose();
  dummy.dispose();
}

// ✅ Descarte de modelo
model.dispose();
```

### Otimização de performance

```typescript
// 1. Modo produção
tf.enableProdMode();  // Remove validações

// 2. Batch predictions
const batched = tf.stack([img1, img2, img3]);
const predictions = model.predict(batched);  // Uma chamada para 3 imagens

// 3. Evitar sync desnecessário
// ❌ Lento - força sync
const data = tensor.dataSync();

// ✅ Rápido - assíncrono
const data = await tensor.data();

// 4. Manter operações no GPU
// ❌ CPU-GPU roundtrip
const result1 = model1.predict(input);
const arr = result1.dataSync();  // Para CPU
const result2 = model2.predict(tf.tensor(arr));  // De volta para GPU

// ✅ Mantém no GPU
const result1 = model1.predict(input);
const result2 = model2.predict(result1);
```

---

## 10. Padrões avançados e casos de uso reais

### Web Workers para inferência não-bloqueante

**worker.js**
```javascript
importScripts('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs');

let model;

self.onmessage = async (e) => {
  if (e.data.type === 'load') {
    model = await tf.loadLayersModel(e.data.modelUrl);
    self.postMessage({type: 'ready'});
  }
  
  if (e.data.type === 'predict') {
    const input = tf.tensor(e.data.input);
    const prediction = model.predict(input);
    const result = await prediction.data();
    input.dispose();
    prediction.dispose();
    self.postMessage({type: 'result', data: Array.from(result)});
  }
};
```

**main.js**
```javascript
const worker = new Worker('worker.js');

worker.postMessage({type: 'load', modelUrl: '/model/model.json'});

worker.onmessage = (e) => {
  if (e.data.type === 'ready') {
    console.log('Modelo carregado no worker');
  }
  if (e.data.type === 'result') {
    renderPrediction(e.data.data);
  }
};

// Enviar predição
worker.postMessage({type: 'predict', input: inputArray});
```

### Streaming de webcam com pose detection

```typescript
async function setupPoseDetection() {
  const video = document.getElementById('video') as HTMLVideoElement;
  const canvas = document.getElementById('canvas') as HTMLCanvasElement;
  const ctx = canvas.getContext('2d')!;
  
  // Setup webcam
  const stream = await navigator.mediaDevices.getUserMedia({
    video: {width: 640, height: 480}
  });
  video.srcObject = stream;
  await video.play();
  
  // Setup detector
  const detector = await poseDetection.createDetector(
    poseDetection.SupportedModels.MoveNet,
    {modelType: poseDetection.movenet.modelType.SINGLEPOSE_THUNDER}
  );
  
  // Loop de detecção
  async function detect() {
    const poses = await detector.estimatePoses(video);
    
    // Desenhar frame
    ctx.drawImage(video, 0, 0);
    
    // Desenhar keypoints
    for (const pose of poses) {
      for (const keypoint of pose.keypoints) {
        if (keypoint.score && keypoint.score > 0.5) {
          ctx.beginPath();
          ctx.arc(keypoint.x, keypoint.y, 5, 0, 2 * Math.PI);
          ctx.fillStyle = 'red';
          ctx.fill();
        }
      }
    }
    
    requestAnimationFrame(detect);
  }
  
  detect();
}
```

### Classificador de áudio em tempo real

```typescript
async function setupAudioClassifier() {
  const recognizer = await speechCommands.create('BROWSER_FFT');
  await recognizer.ensureModelLoaded();
  
  const labels = recognizer.wordLabels();
  console.log('Classes:', labels);
  
  recognizer.listen(
    result => {
      const scores = result.scores as Float32Array;
      const maxIndex = scores.indexOf(Math.max(...scores));
      const confidence = scores[maxIndex];
      
      if (confidence > 0.9) {
        console.log(`Detectado: ${labels[maxIndex]} (${(confidence * 100).toFixed(1)}%)`);
      }
    },
    {
      probabilityThreshold: 0.75,
      includeSpectrogram: false,
      overlapFactor: 0.5
    }
  );
  
  // Para parar
  // recognizer.stopListening();
}
```

### Browser vs Node.js

| Aspecto | Browser | Node.js |
|---------|---------|---------|
| Backend padrão | WebGL | TensorFlow C++ |
| GPU | WebGL/WebGPU | CUDA (tfjs-node-gpu) |
| Performance | ~100x CPU (WebGL) | Nativo TensorFlow |
| Operações | Assíncronas | Síncronas |
| Canvas | Nativo | Requer pacote `canvas` |
| Uso | Aplicações web | Servidor, batch processing |

```typescript
// Node.js - carregar imagem
const tf = require('@tensorflow/tfjs-node');
const fs = require('fs');

const imageBuffer = fs.readFileSync('imagem.jpg');
const tensor = tf.node.decodeImage(imageBuffer, 3);

// Node.js com TensorBoard
await model.fit(x, y, {
  callbacks: tf.node.tensorBoard('./logs')
});
// Visualizar: tensorboard --logdir=./logs
```

---

## 11. Guia de decisão: quando usar o quê

### Árvore de decisão para seleção de backend

```
Precisa de ML no browser?
├── Sim
│   ├── Modelo grande (>50MB) ou operações intensivas?
│   │   ├── Sim → WebGPU (se Chrome 113+) ou WebGL
│   │   └── Não → WASM (melhor para modelos pequenos)
│   └── Dispositivo móvel/low-end?
│       └── WASM com SIMD
└── Não (servidor)
    ├── GPU disponível (CUDA)?
    │   ├── Sim → @tensorflow/tfjs-node-gpu
    │   └── Não → @tensorflow/tfjs-node (CPU nativo)
    └── Portabilidade máxima?
        └── @tensorflow/tfjs (JS puro)
```

### Decisão de arquitetura de modelo

```
Tipo de dado?
├── Imagens
│   ├── Classificação → MobileNet + Dense (transfer learning)
│   ├── Detecção de objetos → COCO-SSD
│   ├── Segmentação → BodyPix / DeepLab
│   └── Custom → Conv2D + BatchNorm + MaxPool + Dense
├── Sequências (texto/áudio)
│   ├── Curtas (<100 tokens) → Conv1D + GlobalMaxPool
│   ├── Longas → LSTM/GRU bidirecionais
│   └── Embeddings semânticos → Universal Sentence Encoder
├── Tabulares
│   └── Dense layers com BatchNorm e Dropout
└── Séries temporais
    ├── Univariadas → LSTM/GRU
    └── Multivariadas → Conv1D + LSTM
```

### Decisão de API (Sequential vs Functional)

```
Modelo tem...
├── Topologia linear simples? → Sequential
├── Múltiplas entradas? → Functional
├── Múltiplas saídas? → Functional
├── Skip connections (ResNet)? → Functional
├── Camadas compartilhadas? → Functional
└── Dúvida? → Functional (mais flexível)
```

### Decisão de otimizador

```
Tipo de problema?
├── Geral / Primeiro teste → Adam (lr=0.001)
├── Fine-tuning → SGD + Momentum (lr=0.0001)
├── RNNs / Sequências → RMSprop (lr=0.001)
├── Dados esparsos (NLP) → Adagrad (lr=0.01)
└── Convergência instável → Reduzir learning rate em 10x
```

### Limitações conhecidas vs Python TensorFlow

| Funcionalidade | TensorFlow.js | Python TensorFlow |
|----------------|---------------|-------------------|
| Treinamento distribuído | ❌ | ✅ |
| TPUs | ❌ | ✅ |
| Ops customizados | Limitado | ✅ Completo |
| Performance de treinamento | 10-15x mais lento | Referência |
| Model zoo | ~20 modelos | 1000+ |
| RaggedTensors | Limitado | ✅ |

**Conclusão**: TensorFlow.js é ideal para **inferência no browser**, **prototipagem rápida**, e **aplicações edge**. Para treinamento de modelos grandes e pesquisa, Python TensorFlow permanece a escolha principal. A estratégia recomendada é **treinar em Python** e **fazer deploy via TensorFlow.js** após conversão.