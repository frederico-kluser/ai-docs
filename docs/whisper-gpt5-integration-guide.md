# Tutorial: Integrando Whisper e GPT-5 (modo XHIGH)

Este guia resume a mesma configuração usada no projeto *video-generator* para adicionar captura de áudio com Whisper e geração de conteúdo com GPT-5 (endpoint `/v1/responses`) em qualquer aplicação JavaScript/TypeScript moderna.

## 1. Pré-requisitos

- Node.js 18+ e npm ou yarn atualizados.
- Conta na OpenAI com acesso ao modelo `gpt-5.1-codex-max` e ao `gpt-4o-mini-transcribe`.
- Chave API (`OPENAI_API_KEY`) com permissão para os dois modelos.
- Navegador com suporte ao `MediaRecorder` para capturar áudio (Chrome/Edge/Brave 114+).

## 2. Dependências essenciais

```bash
npm install openai@^6.15.0
```

A versão 6.15.0 já inclui o endpoint `/v1/responses` e suporte ao parâmetro `reasoning` exigido para o modo XHIGH.

## 3. Gerenciando a chave OpenAI

```ts
// lib/openaiKey.ts
export const OPENAI_KEY_STORAGE_KEY = 'devfolio:openai-api-key';

export function getStoredOpenAIKey() {
  return localStorage.getItem(OPENAI_KEY_STORAGE_KEY) ?? '';
}

export function setStoredOpenAIKey(value: string) {
  localStorage.setItem(OPENAI_KEY_STORAGE_KEY, value.trim());
}
```

Em aplicações desktop/server, prefira variáveis de ambiente (`process.env.OPENAI_API_KEY`).

## 4. Cliente OpenAI compartilhado

```ts
// lib/openaiClient.ts
import OpenAI from 'openai';
import { getStoredOpenAIKey } from './openaiKey';

export function requireOpenAIClient() {
  const apiKey = getStoredOpenAIKey();
  if (!apiKey) throw new Error('Configure sua chave OpenAI antes de usar o microfone.');

  return new OpenAI({
    apiKey,
    timeout: 60_000,
    maxRetries: 3,
    dangerouslyAllowBrowser: true,
  });
}
```

> **Dica:** `dangerouslyAllowBrowser` só deve ser usado em ambientes controlados; em produção crie um backend-proxy.

## 5. Capturando e normalizando áudio

```ts
const MIME_EXTENSION_MAP: Record<string, string> = {
  'audio/webm': 'webm',
  'audio/webm;codecs=opus': 'webm',
  'audio/ogg': 'ogg',
  'audio/ogg;codecs=opus': 'ogg',
  'audio/mp4': 'm4a',
  'audio/mpeg': 'mp3',
  'audio/wav': 'wav',
};

function resolveExtensionFromMime(mime?: string) {
  if (!mime) return 'webm';
  const entry = Object.entries(MIME_EXTENSION_MAP).find(([key]) =>
    mime.toLowerCase().startsWith(key),
  );
  return entry?.[1] ?? 'webm';
}
```

Use `MediaRecorder` para gerar um `Blob` e converta para `File` com a extensão correta antes de enviar ao Whisper.

## 6. Transcrição com Whisper (`gpt-4o-mini-transcribe`)

```ts
import { requireOpenAIClient } from './openaiClient';

export async function transcribeAudioBlob(blob: Blob, language = 'pt') {
  const extension = resolveExtensionFromMime(blob.type);
  const file = blob instanceof File
    ? blob
    : new File([blob], `voice-input.${extension}`, { type: blob.type || 'audio/webm' });

  const client = requireOpenAIClient();
  const transcription = await client.audio.transcriptions.create({
    file,
    model: 'gpt-4o-mini-transcribe',
    response_format: 'text',
    temperature: 0,
    language,
  });

  return typeof transcription === 'string'
    ? transcription.trim()
    : transcription.text?.trim() ?? '';
}
```

## 7. Modelo e schemas para GPT-5

```ts
const BLOG_MODEL = 'gpt-5.1-codex-max';
const blogSchema = { /* JSON Schema usado para o post em PT-BR */ } as const;
const translationSchema = { /* Schema para traduções EN/ES */ } as const;
```

Estruture prompts de sistema e usuário de acordo com o conteúdo esperado, mantendo as instruções editoriais em blocos com listas claras.

## 8. Requisição ao endpoint `/v1/responses`

O ponto crítico é usar o recurso `client.responses.create` **sem** `temperature`/`top_p`, que são incompatíveis com `gpt-5.1-codex-max`. Em vez disso, configure o modo XHIGH via `reasoning.effort`.

```ts
import { requireOpenAIClient } from './openaiClient';

export async function generatePortugueseBlogDraft(transcript: string, context: BlogGenerationContext) {
  if (!transcript.trim()) throw new Error('Nada foi capturado pelo microfone.');

  const systemPrompt = 'Você é o ChatGPT 5 operando no modo XHIGH...';
  const userPrompt = `Briefing transcrito:\n"""${transcript}"""...`;

  const client = requireOpenAIClient();
  const response = await client.responses.create({
    model: BLOG_MODEL,
    reasoning: { effort: 'xhigh' },
    instructions: systemPrompt,
    input: [{ role: 'user', content: userPrompt }],
    text: {
      format: {
        type: 'json_schema',
        name: 'blog_post_pt',
        strict: true,
        schema: blogSchema,
      },
    },
  });

  const outputText = response.output_text?.trim();
  if (!outputText) throw new Error('A resposta da IA veio vazia.');
  return JSON.parse(outputText);
}
```

Para traduções ou outras tarefas, reutilize o mesmo padrão alterando apenas o prompt e o schema.

## 9. Boas práticas e dicas

- **Valide o JSON** retornado com helpers (`parseJSON`) e sanitize campos (categorias, tags, autor padrão, datas ISO).
- **Retries inteligentes:** o SDK já aplica `maxRetries`, mas trate mensagens claras ao usuário em caso de falhas.
- **Latência:** grab a UI progress indicator tanto para upload de áudio quanto para geração do post.
- **Segurança:** nunca exponha chaves permanentes em builds públicos; use storage seguro ou um backend simples para proxyar requisições.
- **Datas e contexto:** injete `todayISO` e listas de categorias/tags diretamente no prompt para manter consistência editorial.

## 10. Checklist final

1. ✅ Dependências instaladas (`openai@6.15.0`).
2. ✅ `OPENAI_API_KEY` configurada/localStorage salvo.
3. ✅ Captura de áudio convertida em `File` com MIME correto.
4. ✅ Transcrição rodando em `gpt-4o-mini-transcribe`.
5. ✅ Geração de conteúdo via `/v1/responses` com `reasoning: { effort: 'xhigh' }`.
6. ✅ Saída validada contra JSON Schema antes de persistir ou exibir.

Com esses passos, qualquer projeto pode replicar a mesma experiência do *video-generator*, combinando captura de briefing por voz e criação de posts ricos usando Whisper + GPT-5 XHIGH.
