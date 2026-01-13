# Tutorial Completo: Geração de Imagens com gpt-image-1.5 e Node.js

O modelo **gpt-image-1.5** representa a mais avançada tecnologia de geração de imagens da OpenAI, lançado em **16 de dezembro de 2025**. Este guia oferece instruções completas para desenvolvedores que desejam integrar capacidades de geração de imagens em aplicações Node.js, cobrindo desde a configuração inicial até padrões de produção em escala.

O gpt-image-1.5 é **4x mais rápido** que seu antecessor, oferece melhor seguimento de instruções, suporta prompts de até **32.000 caracteres**, permite fundos transparentes e múltiplas imagens por requisição — capacidades inexistentes nos modelos DALL-E anteriores. Com a descontinuação do DALL-E 2 e DALL-E 3 programada para maio de 2026, a migração para os modelos GPT Image é essencial.

---

## Quick Start em 15 linhas de código

Este exemplo mínimo demonstra a geração de uma imagem funcional com tratamento de erros:

```javascript
import OpenAI from "openai";
import fs from "fs";

const openai = new OpenAI();

try {
  const result = await openai.images.generate({
    model: "gpt-image-1.5",
    prompt: "Um gato laranja usando óculos de sol em uma praia tropical",
    size: "1024x1024",
    quality: "high"
  });
  
  const imageBuffer = Buffer.from(result.data[0].b64_json, "base64");
  fs.writeFileSync("imagem_gerada.png", imageBuffer);
  console.log("Imagem salva com sucesso!");
} catch (error) {
  console.error(`Erro: ${error.message}`);
}
```

A API key deve estar configurada na variável de ambiente `OPENAI_API_KEY`. O modelo retorna imagens em formato **base64** por padrão, diferente dos modelos DALL-E que retornavam URLs temporárias.

---

## Configuração completa do ambiente de desenvolvimento

### Requisitos do sistema e instalação do SDK

O SDK oficial da OpenAI para Node.js versão **6.9.0** requer Node.js **20 LTS ou superior**. Execute a instalação via npm:

```bash
npm install openai
```

O SDK também suporta Deno (v1.28+), Bun (1.0+), Cloudflare Workers e Vercel Edge Runtime. Para TypeScript, a versão mínima requerida é **4.9**.

### Configuração de autenticação

A abordagem recomendada utiliza variáveis de ambiente, permitindo que o SDK carregue automaticamente as credenciais:

```bash
export OPENAI_API_KEY="sk-sua-chave-aqui"
```

Para cenários que exigem configuração explícita ou múltiplas organizações:

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  timeout: 120000,  // 2 minutos para geração de imagens
  maxRetries: 3     // Retentativas automáticas para erros 429/5xx
});
```

A verificação de organização pode ser necessária antes de utilizar os modelos GPT Image. Acesse o [console de desenvolvedor](https://platform.openai.com/organization/settings) para completar essa verificação.

### Estrutura de projeto recomendada

```
project/
├── src/
│   ├── services/
│   │   └── imageService.js      # Serviço principal de geração
│   ├── utils/
│   │   ├── fileHandler.js       # Manipulação de arquivos
│   │   └── s3Uploader.js        # Upload para cloud storage
│   ├── routes/
│   │   └── imageRoutes.js       # Endpoints da API
│   └── middleware/
│       └── validation.js        # Validação de requisições
├── .env                         # Variáveis de ambiente (não commitar)
└── package.json
```

---

## Referência completa da API

### Modelos disponíveis e suas características

| Modelo | Nome na API | Características | Status |
|--------|-------------|-----------------|--------|
| **GPT Image 1.5** | `gpt-image-1.5` | Estado da arte, 4x mais rápido, melhor seguimento de instruções | Recomendado |
| **GPT Image 1** | `gpt-image-1` | Alta qualidade profissional | Disponível |
| **GPT Image 1 Mini** | `gpt-image-1-mini` | Custo-eficiente para alto volume | Disponível |
| **DALL-E 3** | `dall-e-3` | Legado, prompt máximo de 4.000 caracteres | Descontinuado maio/2026 |
| **DALL-E 2** | `dall-e-2` | Legado, suporta variações | Descontinuado maio/2026 |

### Método images.generate() — Parâmetros completos

```typescript
const response = await openai.images.generate({
  // OBRIGATÓRIO
  prompt: string,              // Descrição da imagem (até 32.000 caracteres)
  
  // MODELO
  model: "gpt-image-1.5",      // Opções: gpt-image-1.5, gpt-image-1, gpt-image-1-mini
  
  // DIMENSÕES
  size: "1024x1024",           // Opções: 1024x1024, 1536x1024 (paisagem), 
                               //         1024x1536 (retrato), auto
  
  // QUALIDADE
  quality: "high",             // Opções: auto, high, medium, low
  
  // FORMATO DE SAÍDA
  output_format: "png",        // Opções: png, jpeg, webp
  output_compression: 100,     // 0-100% (apenas jpeg/webp)
  background: "transparent",   // Opções: transparent, opaque, auto
  
  // QUANTIDADE
  n: 1,                        // 1-10 imagens por requisição
  
  // STREAMING (opcional)
  stream: false,               // Habilita modo streaming
  partial_images: 2,           // 0-3 imagens parciais durante geração
  
  // MODERAÇÃO
  moderation: "auto",          // Opções: auto, low
  
  // IDENTIFICAÇÃO
  user: "user_123"             // ID do usuário final para monitoramento
});
```

### Método images.edit() — Edição de imagens existentes

O modelo GPT Image suporta edição com até **16 imagens de entrada** (máximo 50MB cada):

```typescript
import OpenAI, { toFile } from "openai";
import fs from "fs";

const client = new OpenAI();

async function editarImagem() {
  try {
    const response = await client.images.edit({
      model: "gpt-image-1",
      image: fs.createReadStream("original.png"),
      mask: fs.createReadStream("mascara.png"),  // Áreas transparentes = regiões a editar
      prompt: "Adicionar um chapéu vermelho na pessoa",
      size: "1024x1024",
      quality: "high",
      input_fidelity: "high"  // Controla fidelidade às características da imagem original
    });

    const imageBuffer = Buffer.from(response.data[0].b64_json, "base64");
    fs.writeFileSync("editada.png", imageBuffer);
    console.log("Edição concluída!");
  } catch (error) {
    if (error instanceof OpenAI.APIError) {
      console.error(`Erro ${error.status}: ${error.message}`);
    }
  }
}
```

### Tipos TypeScript completos

```typescript
import OpenAI from "openai";

// Tipos de parâmetros de requisição
type ImageGenerateParams = OpenAI.Images.ImageGenerateParams;
type ImageEditParams = OpenAI.Images.ImageEditParams;

// Estrutura da resposta
interface ImagesResponse {
  created: number;           // Unix timestamp
  data: Array<{
    b64_json?: string;       // Dados base64 da imagem
    url?: string;            // URL (apenas DALL-E, válida por 60 min)
    revised_prompt?: string; // Prompt revisado (DALL-E 3)
  }>;
}

// Tipos de erro
type APIError = OpenAI.APIError;
type RateLimitError = OpenAI.RateLimitError;
type BadRequestError = OpenAI.BadRequestError;
type AuthenticationError = OpenAI.AuthenticationError;
```

---

## Masterclass em engenharia de prompts

### Princípios fundamentais para prompts eficazes

A qualidade da imagem gerada depende diretamente da especificidade do prompt. Prompts vagos produzem resultados genéricos, enquanto prompts detalhados garantem controle preciso sobre o resultado final. Os princípios essenciais incluem:

**Especificidade de elementos**: Em vez de "um cachorro", descreva "um golden retriever adulto com pelo dourado brilhante, sentado em um gramado verde". Inclua cenário, objetos, cores, humor e elementos específicos que deseja ver na imagem.

**Atmosfera e iluminação**: Palavras como "sereno", "dramático", "místico" ou "futurista" direcionam o mood. Especifique condições de luz: "luz dourada do pôr do sol", "iluminação neon cyberpunk", "luz suave de estúdio com softbox".

**Perspectiva e composição**: Defina ângulos como "vista aérea", "close-up macro", "plano médio cinematográfico", ou "perspectiva isométrica para diagrama técnico".

### Exemplos práticos por categoria de uso

**Fotografia de produto profissional:**
```javascript
const promptProduto = `Fotografia profissional de produto: tênis esportivo vermelho 
e branco, fundo branco seamless, iluminação de estúdio com softbox lateral, 
reflexo sutil no chão, qualidade comercial de catálogo, resolução 8K, 
foco nítido nos detalhes de textura do material`;
```

**Ilustração para interface de usuário:**
```javascript
const promptUI = `Design de ícone minimalista para aplicativo de finanças,
estilo flat design com cores gradiente de azul para roxo, linhas limpas,
formas geométricas simples, fundo transparente, vetorial, escalável`;
```

**Arte conceitual para jogos:**
```javascript
const promptConceito = `Arte conceitual de personagem: guerreira élfica com armadura 
de cristal azul luminescente, cabelos brancos longos esvoaçantes, segurando 
arco mágico com runas brilhantes, floresta mística ao fundo com névoa,
iluminação volumétrica, estilo digital painting, paleta de cores frias`;
```

**Diagrama técnico:**
```javascript
const promptTecnico = `Ilustração técnica mostrando arquitetura de microserviços,
vista isométrica, linhas limpas estilo blueprint, componentes rotulados,
setas indicando fluxo de dados, fundo branco, cores corporativas azul e cinza`;
```

### Modificadores de estilo mais eficazes

Os modificadores de estilo transformam drasticamente o resultado. Adicione estes termos ao final do prompt conforme necessário:

- **Fotorrealismo**: "shot on Canon EOS R5, 85mm lens f/1.4, shallow depth of field"
- **Ilustração digital**: "digital art, vibrant colors, sharp lines, ArtStation trending"
- **Aquarela**: "watercolor painting, soft flowing colors, paper texture visible"
- **Cinematográfico**: "cinematic lighting, anamorphic lens, film grain, movie still"
- **Minimalista**: "minimalist design, simple shapes, limited color palette, negative space"

---

## Análise de custos e estratégias de otimização

### Tabela de preços atual (Janeiro 2026)

| Modelo | Qualidade | 1024×1024 | Tamanhos maiores |
|--------|-----------|-----------|------------------|
| **gpt-image-1.5** | Low | $0.011 | $0.016 |
| **gpt-image-1.5** | Medium | $0.042 | $0.063 |
| **gpt-image-1.5** | High | $0.167 | $0.250 |
| **gpt-image-1-mini** | Low | $0.005 | $0.006 |
| **gpt-image-1-mini** | Medium | $0.011 | $0.015 |
| **gpt-image-1-mini** | High | $0.036 | $0.052 |
| **dall-e-3** | Standard | $0.040 | $0.080 |
| **dall-e-3** | HD | $0.080 | $0.120 |

### Estratégias de otimização de custos

O custo pode ser reduzido significativamente com escolhas estratégicas de modelo e qualidade. Para **prototipagem e testes**, utilize `gpt-image-1-mini` com qualidade `low` — o custo de apenas **$0.005 por imagem** permite iteração extensiva de prompts sem impacto no orçamento.

Para **produção em escala** (redes sociais, blogs, conteúdo diário), `gpt-image-1-mini` com qualidade `medium` oferece o melhor custo-benefício a **$0.011 por imagem** — equivalente a 100 imagens por dólar.

Reserve `gpt-image-1.5` com qualidade `high` apenas para **materiais premium**: campanhas publicitárias, assets de alta visibilidade ou trabalhos para clientes exigentes.

```javascript
// Função para selecionar modelo baseado no caso de uso
function selecionarModelo(casoDeUso) {
  const configuracoes = {
    teste:      { model: "gpt-image-1-mini", quality: "low" },
    producao:   { model: "gpt-image-1-mini", quality: "medium" },
    premium:    { model: "gpt-image-1.5", quality: "high" },
    balanceado: { model: "gpt-image-1", quality: "medium" }
  };
  return configuracoes[casoDeUso] || configuracoes.producao;
}
```

---

## Padrões de integração para produção

### API REST completa com Express.js

```javascript
import express from "express";
import OpenAI from "openai";
import { body, validationResult } from "express-validator";
import rateLimit from "express-rate-limit";
import helmet from "helmet";

const app = express();
const openai = new OpenAI();

// Middleware de segurança
app.use(helmet());
app.use(express.json({ limit: "10kb" }));

// Rate limiting: 10 requisições por minuto por IP
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: { error: "Muitas requisições. Tente novamente em 1 minuto." }
});

// Validação de requisição
const validarRequisicao = [
  body("prompt")
    .trim()
    .notEmpty().withMessage("Prompt é obrigatório")
    .isLength({ max: 32000 }).withMessage("Prompt excede limite de 32.000 caracteres"),
  body("size")
    .optional()
    .isIn(["1024x1024", "1536x1024", "1024x1536", "auto"])
    .withMessage("Tamanho inválido"),
  body("quality")
    .optional()
    .isIn(["auto", "high", "medium", "low"])
    .withMessage("Qualidade inválida")
];

// Sanitização de prompt
function sanitizarPrompt(prompt) {
  if (typeof prompt !== "string") return null;
  return prompt
    .slice(0, 32000)
    .replace(/[\x00-\x1F\x7F]/g, "")  // Remove caracteres de controle
    .trim();
}

// Endpoint principal de geração
app.post("/api/v1/gerar-imagem", limiter, validarRequisicao, async (req, res) => {
  // Validar erros
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const promptLimpo = sanitizarPrompt(req.body.prompt);
  if (!promptLimpo) {
    return res.status(400).json({ error: "Prompt inválido" });
  }

  const { 
    size = "1024x1024", 
    quality = "medium",
    model = "gpt-image-1.5",
    background = "auto"
  } = req.body;

  try {
    const response = await openai.images.generate({
      model,
      prompt: promptLimpo,
      size,
      quality,
      background,
      n: 1
    });

    // Retornar apenas dados necessários
    res.status(200).json({
      imagem: response.data[0].b64_json,
      modelo: model,
      tamanho: size,
      qualidade: quality
    });

  } catch (error) {
    console.error("Erro na geração:", {
      status: error.status,
      code: error.code,
      requestId: error.request_id
    });

    if (error.code === "content_policy_violation") {
      return res.status(400).json({ 
        error: "Prompt rejeitado pela política de conteúdo. Modifique e tente novamente."
      });
    }
    
    if (error.status === 429) {
      return res.status(429).json({ 
        error: "Limite de requisições excedido. Aguarde e tente novamente.",
        retryAfter: 60
      });
    }

    res.status(500).json({ error: "Falha na geração de imagem" });
  }
});

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));
```

### Utilitário completo para manipulação de arquivos

```javascript
import fs from "fs";
import fsp from "fs/promises";
import path from "path";
import https from "https";
import crypto from "crypto";

class GerenciadorImagens {
  constructor(opcoes = {}) {
    this.diretorioSaida = opcoes.diretorioSaida || "./imagens-geradas";
  }

  // Salvar imagem base64 em arquivo
  async salvarBase64(base64Data, nomeArquivo = null) {
    try {
      const base64Limpo = base64Data.replace(/^data:image\/\w+;base64,/, "");
      const buffer = Buffer.from(base64Limpo, "base64");
      
      const nomeArquivoFinal = nomeArquivo || this.gerarNomeArquivo("png");
      const caminhoArquivo = path.join(this.diretorioSaida, nomeArquivoFinal);
      
      await fsp.mkdir(this.diretorioSaida, { recursive: true });
      await fsp.writeFile(caminhoArquivo, buffer);
      
      return { 
        caminho: caminhoArquivo, 
        nomeArquivo: nomeArquivoFinal,
        tamanhoBytes: buffer.length 
      };
    } catch (error) {
      throw new Error(`Falha ao salvar imagem: ${error.message}`);
    }
  }

  // Gerar nome de arquivo único
  gerarNomeArquivo(extensao = "png") {
    const timestamp = Date.now();
    const aleatorio = crypto.randomBytes(4).toString("hex");
    return `imagem_${timestamp}_${aleatorio}.${extensao}`;
  }

  // Converter base64 para buffer
  base64ParaBuffer(base64Data) {
    const base64Limpo = base64Data.replace(/^data:image\/\w+;base64,/, "");
    return Buffer.from(base64Limpo, "base64");
  }
}

export default GerenciadorImagens;
```

### Integração com AWS S3

```javascript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import crypto from "crypto";

class UploaderS3 {
  constructor(config = {}) {
    this.cliente = new S3Client({
      region: config.region || process.env.AWS_REGION,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
      }
    });
    this.bucket = config.bucket || process.env.S3_BUCKET;
  }

  async uploadBase64(base64Data, opcoes = {}) {
    try {
      const base64Limpo = base64Data.replace(/^data:image\/\w+;base64,/, "");
      const buffer = Buffer.from(base64Limpo, "base64");
      
      const key = opcoes.key || this.gerarKey(opcoes.prefixo);
      
      const comando = new PutObjectCommand({
        Bucket: this.bucket,
        Key: key,
        Body: buffer,
        ContentType: opcoes.contentType || "image/png",
        Metadata: opcoes.metadata || {}
      });

      await this.cliente.send(comando);

      return {
        key,
        url: `https://${this.bucket}.s3.amazonaws.com/${key}`,
        tamanhoBytes: buffer.length
      };
    } catch (error) {
      throw new Error(`Falha no upload S3: ${error.message}`);
    }
  }

  gerarKey(prefixo = "imagens-geradas") {
    const timestamp = Date.now();
    const aleatorio = crypto.randomBytes(8).toString("hex");
    return `${prefixo}/${timestamp}-${aleatorio}.png`;
  }
}

// Uso integrado com OpenAI
async function gerarEUploadS3(prompt, openai, uploaderS3) {
  const response = await openai.images.generate({
    model: "gpt-image-1.5",
    prompt,
    quality: "high"
  });

  const resultado = await uploaderS3.uploadBase64(
    response.data[0].b64_json,
    { 
      prefixo: "imagens-ia",
      metadata: { 
        prompt: prompt.substring(0, 256),  // Truncar para metadados
        geradoEm: new Date().toISOString() 
      }
    }
  );

  return resultado;
}

export { UploaderS3, gerarEUploadS3 };
```

### Componente React para frontend

```jsx
import React, { useState, useCallback } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:3000";

export default function GeradorImagens() {
  const [prompt, setPrompt] = useState("");
  const [imagemGerada, setImagemGerada] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);

  const gerarImagem = useCallback(async () => {
    if (!prompt.trim()) {
      setErro("Digite uma descrição para a imagem");
      return;
    }

    setCarregando(true);
    setErro(null);
    setImagemGerada(null);

    try {
      const response = await fetch(`${API_URL}/api/v1/gerar-imagem`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          prompt: prompt.trim(),
          size: "1024x1024",
          quality: "medium"
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Falha na geração");
      }

      const data = await response.json();
      setImagemGerada({
        src: `data:image/png;base64,${data.imagem}`,
        timestamp: new Date().toISOString()
      });
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }, [prompt]);

  const baixarImagem = useCallback(() => {
    if (!imagemGerada) return;
    
    const link = document.createElement("a");
    link.href = imagemGerada.src;
    link.download = `imagem-gerada-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, [imagemGerada]);

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <h1>Gerador de Imagens com IA</h1>
      
      <div style={{ marginBottom: "20px" }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Descreva a imagem que deseja gerar..."
          rows={4}
          disabled={carregando}
          maxLength={32000}
          style={{ width: "100%", padding: "12px", borderRadius: "8px" }}
        />
        <small>{prompt.length}/32.000 caracteres</small>
        
        <button 
          onClick={gerarImagem} 
          disabled={carregando || !prompt.trim()}
          style={{ 
            marginTop: "10px", 
            padding: "12px 24px", 
            backgroundColor: carregando ? "#ccc" : "#10a37f",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: carregando ? "not-allowed" : "pointer"
          }}
        >
          {carregando ? "Gerando..." : "Gerar Imagem"}
        </button>
      </div>

      {carregando && (
        <div style={{ textAlign: "center", padding: "40px" }}>
          <p>Gerando imagem, aguarde...</p>
        </div>
      )}

      {erro && (
        <div style={{ 
          backgroundColor: "#fee", 
          color: "#c00", 
          padding: "12px", 
          borderRadius: "8px" 
        }}>
          <strong>Erro:</strong> {erro}
        </div>
      )}

      {imagemGerada && (
        <div>
          <img 
            src={imagemGerada.src} 
            alt="Imagem gerada" 
            style={{ maxWidth: "100%", borderRadius: "8px", marginTop: "20px" }}
          />
          <button onClick={baixarImagem} style={{ marginTop: "10px" }}>
            Baixar Imagem
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## Playbook de tratamento de erros

### Tabela de referência de erros completa

| Código HTTP | Tipo de Erro | Descrição | Deve Retentar? |
|-------------|--------------|-----------|----------------|
| 400 | `BadRequestError` | Requisição malformada ou parâmetros inválidos | Não |
| 400 | `content_policy_violation` | Prompt viola políticas de segurança | Não (modificar prompt) |
| 401 | `AuthenticationError` | API key inválida, revogada ou ausente | Não |
| 403 | `PermissionDeniedError` | API key sem permissão para o endpoint | Não |
| 429 | `RateLimitError` | Limite de requisições excedido | Sim (com backoff) |
| 429 | `insufficient_quota` | Cota de cobrança excedida | Não (verificar faturamento) |
| ≥500 | `InternalServerError` | Problemas no servidor OpenAI | Sim |
| N/A | `APIConnectionError` | Problemas de rede, proxy ou SSL | Sim |
| N/A | `APIConnectionTimeoutError` | Timeout da requisição | Sim |

### Implementação de retry com exponential backoff

```javascript
import OpenAI from "openai";

class ServicoImagensComRetry {
  constructor(opcoes = {}) {
    this.cliente = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      maxRetries: 0,  // Desabilitar retries built-in para controle customizado
      timeout: opcoes.timeout || 120000
    });
    
    this.maxTentativas = opcoes.maxTentativas || 5;
    this.delayInicial = opcoes.delayInicial || 1000;
    this.delayMaximo = opcoes.delayMaximo || 60000;
  }

  async dormir(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  calcularDelay(tentativa) {
    // Exponential backoff: 1s, 2s, 4s, 8s, 16s...
    let delay = this.delayInicial * Math.pow(2, tentativa);
    
    // Adicionar jitter (0-100% do delay) para evitar thundering herd
    delay = delay * (0.5 + Math.random());
    
    return Math.min(delay, this.delayMaximo);
  }

  ehErroRetentavel(error) {
    if (error instanceof OpenAI.APIError) {
      if (error.status === 429 && error.code !== "insufficient_quota") return true;
      if (error.status >= 500) return true;
    }
    if (error.code === "ECONNRESET" || error.code === "ETIMEDOUT") return true;
    return false;
  }

  naoDeveRetentar(error) {
    if (error instanceof OpenAI.APIError) {
      if (error.code === "content_policy_violation") return true;
      if (error.code === "insufficient_quota") return true;
      if (error.status === 400 || error.status === 401 || error.status === 403) return true;
    }
    return false;
  }

  async gerarComRetry(prompt, opcoes = {}) {
    let ultimoErro;
    
    for (let tentativa = 0; tentativa <= this.maxTentativas; tentativa++) {
      try {
        const response = await this.cliente.images.generate({
          model: opcoes.model || "gpt-image-1.5",
          prompt,
          n: opcoes.n || 1,
          size: opcoes.size || "1024x1024",
          quality: opcoes.quality || "medium"
        });
        
        return {
          sucesso: true,
          dados: response.data,
          tentativas: tentativa + 1
        };
        
      } catch (error) {
        ultimoErro = error;
        
        console.error(`Tentativa ${tentativa + 1} falhou:`, {
          nome: error.name,
          status: error.status,
          codigo: error.code,
          requestId: error.request_id
        });
        
        // Não retentar certos erros
        if (this.naoDeveRetentar(error)) break;
        
        // Verificar se é retentável e há tentativas restantes
        if (this.ehErroRetentavel(error) && tentativa < this.maxTentativas) {
          const delay = this.calcularDelay(tentativa);
          console.log(`Retentando em ${Math.round(delay)}ms (tentativa ${tentativa + 2}/${this.maxTentativas + 1})`);
          await this.dormir(delay);
          continue;
        }
        
        break;
      }
    }
    
    return {
      sucesso: false,
      erro: this.formatarErro(ultimoErro),
      tentativas: this.maxTentativas + 1
    };
  }

  formatarErro(error) {
    if (error instanceof OpenAI.APIError) {
      return {
        tipo: error.name,
        status: error.status,
        codigo: error.code,
        mensagem: error.message,
        requestId: error.request_id,
        retentavel: this.ehErroRetentavel(error)
      };
    }
    return {
      tipo: "ErroDesconhecido",
      mensagem: error.message,
      retentavel: false
    };
  }
}

// Uso
const servico = new ServicoImagensComRetry({
  maxTentativas: 5,
  delayInicial: 1000,
  timeout: 120000
});

const resultado = await servico.gerarComRetry(
  "Uma paisagem de montanhas ao pôr do sol",
  { quality: "high" }
);

if (resultado.sucesso) {
  console.log("Imagem gerada após", resultado.tentativas, "tentativa(s)");
} else {
  console.error("Falha após", resultado.tentativas, "tentativas:", resultado.erro);
}
```

---

## Checklist de produção

### Segurança

- [ ] API keys armazenadas em secrets manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] API keys **nunca** expostas no código client-side
- [ ] Rate limiting implementado no backend
- [ ] Validação e sanitização de todos os inputs
- [ ] Logs configurados sem expor secrets ou dados sensíveis
- [ ] Limites de gastos configurados no dashboard OpenAI
- [ ] Headers de segurança configurados (helmet.js)

### Resiliência

- [ ] Retry com exponential backoff implementado
- [ ] Timeout apropriado configurado (120s para imagens)
- [ ] Circuit breaker para falhas consecutivas
- [ ] Tratamento específico para content policy violations
- [ ] Fallback para modelo alternativo quando necessário
- [ ] Health checks configurados

### Monitoramento

- [ ] Logging estruturado de requisições (sem prompts sensíveis)
- [ ] Métricas de latência (p50, p95, p99)
- [ ] Taxa de erros monitorada
- [ ] Alertas para erros 429 frequentes
- [ ] Tracking de custos por usuário/projeto
- [ ] Request ID logado para debugging

### Performance

- [ ] Cache de imagens por hash do prompt implementado
- [ ] Processamento baseado em filas para alto volume
- [ ] Compressão de imagens quando apropriado
- [ ] CDN configurado para servir imagens
- [ ] Concurrent request limiting implementado

---

## Guia de troubleshooting

### Erro 429: "Too Many Requests"

**Causas possíveis**: Limite de RPM/IPM excedido, burst rate limiting, ou cota de faturamento esgotada.

**Solução**: Implementar espaçamento entre requisições e verificar headers de rate limit:

```javascript
const response = await cliente.images.generate({...}).withResponse();
console.log("Requisições restantes:", response.headers.get("x-ratelimit-remaining-requests"));
```

### Erro: content_policy_violation

**Solução**: Modificar o prompt para evitar conteúdo proibido. Este erro **não deve ser retentado** — o prompt precisa ser alterado. Evite: personagens com copyright, figuras públicas reais, violência explícita, conteúdo adulto.

### Timeout após 60 segundos

**Causa**: O modelo gpt-image-1.5 pode levar até 30-60 segundos para gerar imagens de alta qualidade.

**Solução**: Configure timeout adequado:

```javascript
const cliente = new OpenAI({
  timeout: 120 * 1000  // 2 minutos
});
```

### Erro 401: "Invalid API Key"

**Checklist de verificação**:
1. Verificar se a key não foi revogada no dashboard
2. Confirmar ausência de espaços em branco na variável de ambiente
3. Verificar permissões da key para geração de imagens
4. Confirmar associação correta de organização/projeto

---

## Calculadora de custos

### Fórmula para estimativa mensal

```javascript
function calcularCustoMensal(imagensPorDia, modelo, qualidade, tamanho) {
  const precos = {
    "gpt-image-1.5": {
      low:    { "1024x1024": 0.011, maior: 0.016 },
      medium: { "1024x1024": 0.042, maior: 0.063 },
      high:   { "1024x1024": 0.167, maior: 0.250 }
    },
    "gpt-image-1-mini": {
      low:    { "1024x1024": 0.005, maior: 0.006 },
      medium: { "1024x1024": 0.011, maior: 0.015 },
      high:   { "1024x1024": 0.036, maior: 0.052 }
    }
  };

  const ehTamanhoMaior = tamanho !== "1024x1024";
  const precoPorImagem = precos[modelo][qualidade][ehTamanhoMaior ? "maior" : "1024x1024"];
  const imagensMes = imagensPorDia * 30;
  
  return {
    precoPorImagem,
    imagensMes,
    custoMensal: (imagensMes * precoPorImagem).toFixed(2),
    custoAnual: (imagensMes * 12 * precoPorImagem).toFixed(2)
  };
}

// Exemplo: 100 imagens/dia com gpt-image-1-mini medium
const estimativa = calcularCustoMensal(100, "gpt-image-1-mini", "medium", "1024x1024");
console.log(`Custo mensal estimado: $${estimativa.custoMensal}`);
// Output: Custo mensal estimado: $33.00
```

### Comparativo de cenários de uso

| Cenário | Modelo | Qualidade | Imagens/mês | Custo mensal |
|---------|--------|-----------|-------------|--------------|
| Startup MVP | gpt-image-1-mini | low | 500 | $2.50 |
| Blog com IA | gpt-image-1-mini | medium | 1.000 | $11.00 |
| E-commerce | gpt-image-1.5 | medium | 3.000 | $126.00 |
| Agência criativa | gpt-image-1.5 | high | 1.000 | $167.00 |
| Enterprise | gpt-image-1.5 | high | 10.000 | $1,670.00 |

---

## Templates de código prontos para uso

### Template 1: Serviço completo de geração

```javascript
// services/ImageGenerationService.js
import OpenAI from "openai";
import fs from "fs/promises";
import path from "path";
import crypto from "crypto";

export class ImageGenerationService {
  constructor(config = {}) {
    this.client = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      timeout: config.timeout || 120000,
      maxRetries: config.maxRetries || 3
    });
    
    this.defaultModel = config.defaultModel || "gpt-image-1.5";
    this.defaultQuality = config.defaultQuality || "medium";
    this.outputDir = config.outputDir || "./output";
  }

  async generate(prompt, options = {}) {
    const {
      model = this.defaultModel,
      quality = this.defaultQuality,
      size = "1024x1024",
      background = "auto",
      outputFormat = "png",
      saveToFile = false,
      filename = null
    } = options;

    try {
      const response = await this.client.images.generate({
        model,
        prompt,
        quality,
        size,
        background,
        output_format: outputFormat,
        n: 1
      });

      const base64Data = response.data[0].b64_json;
      const buffer = Buffer.from(base64Data, "base64");

      let filePath = null;
      if (saveToFile) {
        await fs.mkdir(this.outputDir, { recursive: true });
        const finalFilename = filename || `img_${Date.now()}_${crypto.randomBytes(4).toString("hex")}.${outputFormat}`;
        filePath = path.join(this.outputDir, finalFilename);
        await fs.writeFile(filePath, buffer);
      }

      return {
        success: true,
        base64: base64Data,
        buffer,
        filePath,
        metadata: {
          model,
          quality,
          size,
          promptLength: prompt.length,
          generatedAt: new Date().toISOString()
        }
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: error.name || "UnknownError",
          message: error.message,
          status: error.status,
          code: error.code,
          requestId: error.request_id
        }
      };
    }
  }

  async edit(imagePath, prompt, options = {}) {
    const {
      model = "gpt-image-1",
      maskPath = null,
      quality = "medium",
      size = "1024x1024"
    } = options;

    try {
      const imageStream = await fs.readFile(imagePath);
      const editParams = {
        model,
        image: imageStream,
        prompt,
        quality,
        size
      };

      if (maskPath) {
        editParams.mask = await fs.readFile(maskPath);
      }

      const response = await this.client.images.edit(editParams);
      
      return {
        success: true,
        base64: response.data[0].b64_json,
        buffer: Buffer.from(response.data[0].b64_json, "base64")
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: error.name,
          message: error.message,
          status: error.status
        }
      };
    }
  }
}

export default ImageGenerationService;
```

### Template 2: Express.js API completa

```javascript
// app.js - API completa com todas as funcionalidades
import express from "express";
import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import { ImageGenerationService } from "./services/ImageGenerationService.js";

const app = express();
const imageService = new ImageGenerationService();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: "50mb" }));

// Rate limiting
app.use("/api", rateLimit({
  windowMs: 60000,
  max: 20,
  message: { error: "Rate limit exceeded" }
}));

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

// Geração de imagem
app.post("/api/generate", async (req, res) => {
  const { prompt, model, quality, size, background } = req.body;

  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Prompt is required" });
  }

  const result = await imageService.generate(prompt, {
    model,
    quality,
    size,
    background
  });

  if (result.success) {
    res.json({
      image: result.base64,
      metadata: result.metadata
    });
  } else {
    const statusCode = result.error.status || 500;
    res.status(statusCode).json({ error: result.error });
  }
});

// Edição de imagem
app.post("/api/edit", async (req, res) => {
  const { imageBase64, prompt, maskBase64, quality } = req.body;

  if (!imageBase64 || !prompt) {
    return res.status(400).json({ error: "Image and prompt are required" });
  }

  // Salvar temporariamente para processamento
  const tempDir = "./temp";
  const fs = await import("fs/promises");
  await fs.mkdir(tempDir, { recursive: true });

  const imagePath = `${tempDir}/input_${Date.now()}.png`;
  await fs.writeFile(imagePath, Buffer.from(imageBase64, "base64"));

  let maskPath = null;
  if (maskBase64) {
    maskPath = `${tempDir}/mask_${Date.now()}.png`;
    await fs.writeFile(maskPath, Buffer.from(maskBase64, "base64"));
  }

  const result = await imageService.edit(imagePath, prompt, {
    maskPath,
    quality
  });

  // Limpar arquivos temporários
  await fs.unlink(imagePath).catch(() => {});
  if (maskPath) await fs.unlink(maskPath).catch(() => {});

  if (result.success) {
    res.json({ image: result.base64 });
  } else {
    res.status(500).json({ error: result.error });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

---

## Conclusão

O modelo **gpt-image-1.5** representa um salto significativo na qualidade e velocidade de geração de imagens via API. Com suporte a prompts de 32.000 caracteres, fundos transparentes, múltiplas imagens por requisição e velocidade 4x superior ao antecessor, ele se posiciona como a escolha definitiva para aplicações de produção.

A migração dos modelos DALL-E para os modelos GPT Image é urgente, dado o prazo de descontinuação em maio de 2026. O modelo **gpt-image-1-mini** oferece uma opção extraordinariamente econômica para casos de alto volume, custando apenas **$0.005 por imagem** na qualidade low — viabilizando projetos que antes seriam financeiramente inviáveis.

Para produção robusta, a combinação de retry com exponential backoff, validação rigorosa de inputs, rate limiting no backend e monitoramento adequado de custos garante uma implementação resiliente e escalável. O SDK oficial da OpenAI para Node.js v6.9.0 oferece excelente suporte TypeScript e tratamento de erros granular, facilitando a construção de aplicações profissionais.