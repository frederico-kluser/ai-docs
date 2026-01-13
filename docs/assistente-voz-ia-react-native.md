# Assistente de Voz IA com React Native: Viabilidade e Arquitetura

**React Native não pode criar apps nativos para Apple Watch**, mas uma arquitetura híbrida combina o melhor dos dois mundos. O app do iPhone pode ser 100% React Native, enquanto o Watch requer Swift/SwiftUI com comunicação via `react-native-watch-connectivity`. Esta abordagem é usada por apps em produção como BlueWallet e Jitsi Meet. A integração com Siri via App Intents também necessita de código nativo, mas funcionalidades básicas de Siri Shortcuts funcionam bem com bibliotecas existentes.

A boa notícia é que as bibliotecas de áudio e integração OpenAI estão maduras e bem mantidas. O `expo-audio` (SDK 52+) ou `react-native-nitro-sound` oferecem gravação de alta qualidade compatível com Whisper API, streaming SSE para respostas GPT funciona nativamente, e até transcrição on-device é possível com `whisper.rn`. O maior trade-off é aceitar ~50-100ms de latência adicional comparado ao desenvolvimento nativo puro.

---

## Opções para desenvolvimento Apple Watch

### React Native não suporta interface watchOS

A documentação oficial do `react-native-watch-connectivity` é explícita: "This library does NOT allow you to create a Watch App in React Native but rather facilitates communication with a Watch App written in Swift/Objective-C." O watchOS não suporta os engines JavaScript (JavaScriptCore ou V8) que React Native requer, e componentes WKInterface não são renderizáveis via React Native.

A única solução viável é a **arquitetura híbrida**: app watchOS nativo em Swift/SwiftUI que se comunica com o app React Native do iPhone via WatchConnectivity framework. O pacote `react-native-watch-connectivity` (v1.1.0, ~2.940 downloads semanais, 763 stars no GitHub) fornece esta ponte com suporte a:

- **Mensagens interativas** via `sendMessage()` quando o Watch está acessível
- **Sincronização de contexto** via `updateApplicationContext()` para dados em background  
- **Transferência de arquivos** via `transferFile()` para enviar dados maiores
- **Monitoramento de estado** via `getWatchReachability()` e `getIsPaired()`

```javascript
import { sendMessage, watchEvents, updateApplicationContext } from 'react-native-watch-connectivity';

// Enviar mensagem para o Watch
const sendToWatch = (data) => {
  sendMessage(
    { action: 'transcription', payload: data },
    (reply) => console.log('Watch respondeu:', reply),
    (error) => console.error('Erro:', error)
  );
};

// Escutar mensagens do Watch
useEffect(() => {
  const unsubscribe = watchEvents.on('message', (message) => {
    if (message.action === 'startRecording') {
      // Iniciar gravação no iPhone
    }
  });
  return () => unsubscribe();
}, []);
```

### Estratégia recomendada para o projeto

O fluxo proposto (Watch grava → Whisper transcreve → GPT processa → resposta de volta) funcionaria assim:

1. **Watch** (Swift/SwiftUI): Interface de gravação, exibe transcrição, botão de confirmação
2. **iPhone** (React Native): Recebe áudio via WatchConnectivity, processa com APIs OpenAI
3. **Comunicação**: Mensagens bidirecionais via `react-native-watch-connectivity`

Para Expo, funciona apenas com **Bare Workflow** usando EAS Build. Há issues conhecidos (#795, #2578 no expo/eas-cli) com provisioning profiles para targets Watch.

---

## Gravação de áudio e configuração

### Bibliotecas atualizadas para 2025

**IMPORTANTE:** O pacote `react-native-audio-recorder-player` foi **descontinuado** e renasceu como `react-native-nitro-sound` (v0.2.10, novembro 2025). Para projetos Expo, o `expo-av` está deprecado no SDK 52+ — use `expo-audio` com a nova API baseada em hooks.

```typescript
// expo-audio (SDK 52+)
import { useAudioRecorder, AudioModule, RecordingPresets, setAudioModeAsync } from 'expo-audio';

export default function VoiceRecorder() {
  const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  
  useEffect(() => {
    (async () => {
      await AudioModule.requestRecordingPermissionsAsync();
      await setAudioModeAsync({ playsInSilentMode: true, allowsRecording: true });
    })();
  }, []);

  const record = async () => {
    await audioRecorder.prepareToRecordAsync();
    audioRecorder.record();
  };

  const stop = async () => {
    await audioRecorder.stop();
    // audioRecorder.uri contém o arquivo gravado
  };
}
```

Os formatos suportados são **totalmente compatíveis** com Whisper API: `.m4a` (AAC) é o padrão no iOS, e MP3, WAV, WEBM também funcionam. Configure qualidade otimizada para voz:

```typescript
const audioSettings = {
  AVSampleRateKeyIOS: 44100,
  AVFormatIDKeyIOS: AVEncodingOption.aac,
  AVEncoderAudioQualityKeyIOS: AVEncoderAudioQualityIOSType.high,
  AudioChannels: 1,  // Mono é suficiente para voz
};
```

Para **streaming em tempo real** (transcrição live), use `react-native-live-audio-stream` que emite chunks base64 conforme grava — ideal para integração futura com Whisper streaming.

---

## Integração completa com OpenAI

### Enviando áudio para Whisper API

A integração usa FormData padrão com `fetch`. **Não defina Content-Type manualmente** — deixe o fetch configurar o boundary automaticamente:

```typescript
const transcribeAudio = async (audioUri: string, apiKey: string) => {
  const formData = new FormData();
  const filename = audioUri.split('/').pop() || 'recording.m4a';
  
  formData.append('file', {
    uri: Platform.OS === 'android' ? audioUri : audioUri.replace('file://', ''),
    type: 'audio/m4a',
    name: filename
  } as any);
  formData.append('model', 'whisper-1');
  formData.append('language', 'pt');  // Português

  const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}` },
    body: formData
  });

  return (await response.json()).text;
};
```

### Streaming de respostas GPT

O pacote `react-native-sse` é a solução mais madura para Server-Sent Events em React Native:

```typescript
import EventSource from 'react-native-sse';

const streamGPTResponse = async (userMessage: string, onChunk: (text: string) => void) => {
  const es = new EventSource('https://api.openai.com/v1/chat/completions', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`,
    },
    method: 'POST',
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{ role: 'user', content: userMessage }],
      stream: true,
    }),
  });

  let fullResponse = '';
  
  es.addEventListener('message', (event) => {
    if (event.data === '[DONE]') { es.close(); return; }
    const content = JSON.parse(event.data).choices?.[0]?.delta?.content;
    if (content) { fullResponse += content; onChunk(fullResponse); }
  });
};
```

### TTS e reprodução de áudio

```typescript
import * as FileSystem from 'expo-file-system';
import { Audio } from 'expo-av';

const playTTSResponse = async (text: string) => {
  const response = await fetch('https://api.openai.com/v1/audio/speech', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model: 'tts-1', voice: 'nova', input: text }),
  });

  const arrayBuffer = await response.arrayBuffer();
  const base64 = Buffer.from(arrayBuffer).toString('base64');
  const fileUri = FileSystem.cacheDirectory + 'tts_output.mp3';
  await FileSystem.writeAsStringAsync(fileUri, base64, { encoding: 'base64' });
  
  const { sound } = await Audio.Sound.createAsync({ uri: fileUri });
  await sound.playAsync();
};
```

### Segurança crítica para produção

**⚠️ NUNCA exponha API keys no código cliente.** A documentação oficial de segurança React Native alerta: "Anything included in your code could be accessed in plain text by anyone inspecting the app bundle."

A arquitetura recomendada usa um **backend proxy**:

```
React Native App → Seu Backend (Node/Python) → OpenAI API
                        ↑
                   API Key armazenada
                   apenas no servidor
```

Para variáveis de ambiente em desenvolvimento, use `react-native-config` (bare RN) ou prefixo `EXPO_PUBLIC_` (Expo).

---

## Siri, App Intents e ativação por voz

### Capacidades atuais do react-native-siri-shortcut

O pacote `react-native-siri-shortcut` (v3.2.4, ~4k downloads semanais) permite doar shortcuts para Siri Suggestions e apresentar o botão "Adicionar à Siri". **Status de manutenção:** inativo desde dezembro 2023, mas funcional.

```javascript
import { donateShortcut, presentShortcut } from 'react-native-siri-shortcut';

const shortcutOptions = {
  activityType: "com.myapp.askassistant",
  title: "Perguntar ao Assistente",
  suggestedInvocationPhrase: "Chamar assistente",
  isEligibleForPrediction: true
};

donateShortcut(shortcutOptions);  // Aparece nas Sugestões Siri
presentShortcut(shortcutOptions); // Mostra UI "Adicionar à Siri"
```

Para Expo, adicione o config plugin: `@config-plugins/react-native-siri-shortcut`. **Não funciona no Expo Go** — requer development build.

### App Intents requer código nativo

A API App Intents (iOS 16+), essencial para integração moderna com Siri, **não possui bridge React Native**. Implementar requer:

1. **Código Swift** definindo o AppIntent
2. **Bridging header** para interop Swift/Objective-C
3. **Deep links** para comunicar com a camada React Native
4. Potencial **patch no RCTLinkingManager** para capturar links em cold-launch

```swift
// BookAppointmentIntent.swift (código nativo necessário)
import AppIntents

@available(iOS 16, *)
struct AskAssistantIntent: AppIntent {
    static let title: LocalizedStringResource = "Perguntar ao Assistente"
    static var openAppWhenRun: Bool = true
    
    func perform() -> some IntentResult {
        UIApplication.shared.open(URL(string: "myapp://assistant?trigger=siri")!)
        return .result()
    }
}
```

### Alternativas para ativação por voz sem Siri

| Solução | Pacote | Uso |
|---------|--------|-----|
| **Wake Word** | `@picovoice/porcupine-react-native` | "Hey Assistant" personalizado |
| **Reconhecimento de fala** | `@react-native-voice/voice` | Transcrição contínua |
| **Detecção de atividade** | `react-native-vad` | Detecta quando usuário fala |

O Porcupine oferece keywords built-in (Alexa, Computer, Jarvis) e suporta palavras customizadas (requer console Picovoice). Funciona offline com **97%+ precisão**.

---

## Módulos nativos e bridging

### TurboModules é o novo padrão

React Native 0.76+ tornou TurboModules o **padrão**, eliminando overhead do bridge antigo. Benefícios para apps de áudio:

- **Até 99% de redução** no overhead de chamadas nativas
- **Comunicação síncrona** possível (antes sempre async)
- **Zero-copy memory access** via JSI — crítico para buffers de áudio
- **Lazy loading** de módulos melhora startup

### Expo Modules API para bridges customizados

Se precisar bridgear frameworks iOS não disponíveis, o **Expo Modules API** é recomendado sobre TurboModules puros:

```swift
// modules/natural-language/ios/NaturalLanguageModule.swift
import ExpoModulesCore
import NaturalLanguage

public class NaturalLanguageModule: Module {
  public func definition() -> ModuleDefinition {
    Name("NaturalLanguage")
    
    Function("analyzeSentiment") { (text: String) -> Double in
      let tagger = NLTagger(tagSchemes: [.sentimentScore])
      tagger.string = text
      let (tag, _) = tagger.tag(at: text.startIndex, unit: .paragraph, scheme: .sentimentScore)
      return Double(tag?.rawValue ?? "0") ?? 0
    }
  }
}
```

Vantagens: Swift como linguagem principal (não Obj-C), menos boilerplate, compatibilidade automática com arquiteturas old/new.

### Pacotes existentes para necessidades do projeto

| Necessidade | Pacote | Maturidade |
|-------------|--------|------------|
| Watch Communication | `react-native-watch-connectivity` | ★★★★☆ |
| Speech Recognition | `expo-speech-recognition` | ★★★★★ |
| On-device Whisper | `whisper.rn` | ★★★★☆ |
| Core ML | `react-native-coreml` | ★★★☆☆ |
| TensorFlow Lite | `react-native-fast-tflite` | ★★★★★ |
| Apple Intelligence | `@react-native-ai/apple` | ★★★☆☆ (Preview) |

O **`whisper.rn`** permite transcrição totalmente offline usando whisper.cpp com aceleração Core ML no iOS — elimina dependência de API para transcrição.

### Apple Intelligence e Foundation Models

O pacote `@react-native-ai/apple` (por Callstack) já oferece acesso ao modelo de ~3B parâmetros on-device:

```typescript
import { apple } from '@react-native-ai/apple';
import { generateText, streamText } from 'ai';

const response = await generateText({
  model: apple(),
  prompt: 'Resuma meu dia em uma frase',
});
```

**Requisitos:** iOS 26+, dispositivo com Apple Intelligence (iPhone 15 Pro+, iPhone 16), React Native 0.80+, New Architecture. O iPhone 16e provavelmente suportará, dependendo da linha do produto.

---

## Arquitetura e gerenciamento de estado

### Estrutura de projeto recomendada

```
src/
├── features/
│   ├── voice/
│   │   ├── hooks/useVoiceRecording.ts
│   │   ├── services/openaiService.ts
│   │   └── store/voiceStore.ts
│   ├── presets/
│   └── settings/
├── native/                 # Bridges customizados
│   └── watch/
├── services/
│   ├── api/client.ts
│   └── storage/mmkvStorage.ts
└── shared/

ios/
├── VoiceAssistant/         # App principal
└── WatchExtension/         # App Watch (Swift/SwiftUI)
```

### MMKV para persistência de alta performance

**Evite AsyncStorage** para este projeto. O `react-native-mmkv` é **20-30x mais rápido** e suporta App Groups para compartilhar dados com a extensão Watch:

```typescript
import { createMMKV } from 'react-native-mmkv';

export const storage = createMMKV({
  id: 'voice-assistant',
  encryptionKey: 'your-secret-key',
  mode: 'multi-process'  // Necessário para App Groups
});

// Operações síncronas (sem async/await)
storage.set('presets', JSON.stringify(presets));
const presets = JSON.parse(storage.getString('presets') || '[]');
```

### Zustand para estado global

Zustand é a escolha ideal para apps de voz: bundle mínimo (~1KB), sem boilerplate, acesso síncrono ao estado:

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

const mmkvStorage = {
  getItem: (name) => storage.getString(name) ?? null,
  setItem: (name, value) => storage.set(name, value),
  removeItem: (name) => storage.delete(name)
};

export const useVoiceStore = create(
  persist(
    (set) => ({
      isRecording: false,
      transcript: '',
      conversations: [],
      
      startRecording: () => set({ isRecording: true }),
      setTranscript: (text) => set({ transcript: text }),
      addConversation: (conv) => set((s) => ({ 
        conversations: [...s.conversations, conv] 
      }))
    }),
    {
      name: 'voice-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (state) => ({ conversations: state.conversations })
    }
  )
);
```

**⚠️ Evite Realm:** MongoDB anunciou descontinuação do Atlas Device Sync + Realm SDKs em setembro 2024. Serviço termina em **30 de setembro de 2025**.

---

## Considerações de performance e bateria

### Hermes Engine otimizações

Hermes é o engine JS padrão desde RN 0.73 e oferece:

- **30-50% cold starts mais rápidos**
- **Compilação AOT** — JavaScript compilado para bytecode no build
- **Garbage collector geracional** — menos pausas durante gravação
- **49MB redução de memória** em benchmarks reais

Para áudio, a compilação prévia elimina overhead de parsing JS, mas o bridge tradicional ainda adiciona ~5-10ms por chamada nativa. Use bibliotecas JSI-based (`react-native-mmkv`, `react-native-fast-tflite`) para operações críticas.

### Background audio e tarefas

```typescript
// Configurar sessão de áudio para background
import { Audio } from 'expo-av';

await Audio.setAudioModeAsync({
  allowsRecordingIOS: true,
  staysActiveInBackground: true,  // Crítico
  playsInSilentModeIOS: true,
});
```

Para tarefas em background (sincronização de conversas), use `react-native-background-fetch`. **Limitações iOS:** ~30 segundos de execução, frequência determinada por machine learning do sistema.

### Comparativo React Native vs Nativo

| Aspecto | React Native | Nativo Swift |
|---------|--------------|--------------|
| **Latência de áudio** | +50-100ms | ~10-30ms |
| **Cold start** | 800-1200ms | 400-600ms |
| **Memória** | +20-40% overhead | Baseline |
| **Tempo dev** | 30-50% mais rápido | Baseline |
| **Watch integration** | Limitada | Completa |
| **Siri/App Intents** | Parcial | Completa |

**Veredicto:** Para este projeto específico, a latência de áudio de ~50-100ms é aceitável para um assistente de voz conversacional. O ganho em velocidade de desenvolvimento e manutenção de codebase único justifica React Native para o app iPhone.

---

## Ecossistema de bibliotecas necessárias

### Pacotes essenciais com versões

```json
{
  "dependencies": {
    "expo": "~52.0.0",
    "expo-audio": "~1.1.1",
    "expo-av": "~14.0.0",
    "expo-file-system": "~17.0.0",
    "react-native-watch-connectivity": "^1.1.0",
    "react-native-mmkv": "^4.0.0",
    "react-native-sse": "^1.2.0",
    "react-native-siri-shortcut": "^3.2.4",
    "@react-native-voice/voice": "^4.0.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.0.0"
  },
  "devDependencies": {
    "@config-plugins/react-native-siri-shortcut": "latest",
    "detox": "^20.0.0"
  }
}
```

### Expo vs Bare React Native

| Característica | Expo Managed | Expo Bare/Dev Build |
|---------------|--------------|---------------------|
| Watch connectivity | ❌ | ✅ (requer native code) |
| Siri Shortcuts | ❌ | ✅ |
| Custom native modules | ❌ | ✅ |
| Over-the-air updates | ✅ | ✅ |
| EAS Build | ✅ | ✅ |

**Recomendação:** Use **Expo com Development Builds** (não Expo Go). Permite usar todos os pacotes nativos necessários enquanto mantém benefícios do ecossistema Expo (EAS Build, expo-updates, config plugins).

---

## Roadmap de desenvolvimento adaptado

### Fase 1: Fundação (Semanas 1-3)
- Setup Expo bare workflow com EAS Build
- Configurar `expo-audio` para gravação
- Implementar integração Whisper API via backend proxy
- Setup `react-native-mmkv` e Zustand

### Fase 2: Fluxo de voz completo (Semanas 4-6)
- Streaming GPT com `react-native-sse`
- Reprodução TTS
- UI de gravação/transcrição
- Gerenciamento de presets no iPhone

### Fase 3: Watch App nativo (Semanas 7-10)
- Criar Watch target em Swift/SwiftUI
- Implementar UI de gravação no Watch
- Configurar `react-native-watch-connectivity`
- Testar comunicação bidirecional

### Fase 4: Siri e polimento (Semanas 11-13)
- Integrar `react-native-siri-shortcut`
- Implementar App Intents em Swift (se necessário)
- Otimizar performance e bateria
- Testes E2E com Detox

**Ajuste de timeline:** +3-4 semanas comparado a desenvolvimento 100% nativo, principalmente devido à fase 3 que requer código Swift para o Watch.

---

## Análise de trade-offs: React Native vs Nativo

### Quando escolher React Native (este projeto)

✅ Time tem experiência JavaScript/TypeScript
✅ App iPhone é a experiência principal
✅ Latência de 50-100ms é aceitável
✅ Deseja código compartilhado para futuro Android
✅ Ciclos de desenvolvimento mais rápidos são prioritários

### Quando escolher 100% Nativo

❌ Watch é a experiência principal
❌ Requer integração profunda com App Intents/SiriKit
❌ Latência de áudio <10ms é crítica
❌ Time já domina Swift

### Deal-breakers identificados

| Feature | Status em React Native |
|---------|----------------------|
| UI do Watch em React | ❌ **IMPOSSÍVEL** |
| App Intents completos | ❌ Requer código Swift |
| SiriKit Domain Intents | ❌ Requer Intent Extension nativa |
| Background audio contínuo | ⚠️ Limitado vs nativo |
| Custom complications | ❌ Requer código SwiftUI |

---

## Limitações conhecidas e workarounds

### Comunicação Watch ↔ iPhone

**Limitação:** Latência de mensagens pode chegar a 2 minutos em simulador. Em dispositivos reais, tipicamente <1 segundo quando Watch está acessível.

**Workaround:** Use `updateApplicationContext()` para dados que precisam persistir mesmo quando apps não estão em foreground. Design o Watch app para funcionar independentemente quando iPhone não está acessível.

### Siri Shortcuts em cold launch

**Limitação:** Quando app não está rodando e Siri aciona shortcut, deep links podem ser "perdidos" pois RCTLinkingManager não está inicializado.

**Workaround:** Patch no `RCTLinkingManager.mm` para capturar links pendentes, ou armazene em UserDefaults no AppDelegate e leia no JS.

### Transcrição on-device

**Limitação:** `@react-native-voice/voice` não expõe todas features do SFSpeechRecognizer (hints, custom vocabulary).

**Workaround:** Use `expo-speech-recognition` que oferece `requiresOnDeviceRecognition: true` e `contextualStrings` para vocabulário customizado. Ou use `whisper.rn` para transcrição local completa.

---

## Conclusão e veredicto final

**A implementação React Native é VIÁVEL com uma arquitetura híbrida.** O app iPhone pode ser 100% React Native com excelente suporte para gravação de áudio, integração OpenAI e gerenciamento de estado. O Apple Watch **obrigatoriamente** requer código Swift/SwiftUI, comunicando-se via `react-native-watch-connectivity`.

Para Siri integration básica (Shortcuts), bibliotecas existentes atendem. Para App Intents completos (iOS 16+), prepare-se para escrever ~200-500 linhas de Swift. A escolha entre esta abordagem híbrida e desenvolvimento 100% nativo deve considerar:

- **Escolha React Native híbrido** se o time domina JavaScript, o app iPhone é o foco principal, e 3-4 semanas extras de desenvolvimento são aceitáveis
- **Escolha 100% nativo** se o Watch é a experiência central, integração Siri profunda é crítica, ou o time já domina Swift/SwiftUI

O ecossistema React Native para apps de voz em 2025 está maduro: `expo-audio` e `react-native-nitro-sound` são robustos, `react-native-sse` funciona bem para streaming, `whisper.rn` oferece transcrição offline, e `@react-native-ai/apple` já disponibiliza acesso aos Foundation Models. O principal trabalho adicional está na camada Watch e integrações Siri avançadas.