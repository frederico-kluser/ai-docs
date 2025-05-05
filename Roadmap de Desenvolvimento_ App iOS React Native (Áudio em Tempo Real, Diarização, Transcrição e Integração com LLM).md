# Roadmap de Desenvolvimento: App iOS React Native (Áudio em Tempo Real, Diarização, Transcrição e Integração com LLM)

## 1. Captura de Áudio em Tempo Real
Para capturar áudio em tempo real no iOS com React Native, use módulos nativos ou bibliotecas consolidadas. Exemplos incluem *react-native-live-audio-stream* (permite obter frames de áudio ao vivo) e *react-native-audio-recorder-player* (gravação e reprodução) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=react)) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=import%20LiveAudioStream%20from%20%27react)). Se usar Expo, considere o módulo *expo-av. É essencial solicitar permissão de microfone (NSMicrophoneUsageDescription) em Info.plist ([How To Record Audio In React Native iOS? - Stack Overflow](https://stackoverflow.com/questions/76379322/how-to-record-audio-in-react-native-ios#:~:text=You%20first%20need%20to%20ask,microphone%20permission)) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=iOS)). Para melhorar performance, prefira captura contínua em buffer em vez de gravações em disco. Possíveis alternativas on-device incluem o **VoiceProcessor* da Picovoice para streaming eficiente de áudio (via @picovoice/react-native-voice-processor) ([Audio Recording | React Native Quick Start - Picovoice Docs](https://picovoice.ai/docs/quick-start/voiceprocessor-react-native/#:~:text=Access%20the%20singleton%20instance%20of,VoiceProcessor)). 

*Checklist captura áudio*:
- Configurar sessão de áudio (AVAudioSession) para gravação contínua.
- Tratar buffers de áudio (p.e., taxa de amostragem 16 ou 32 kHz, mono) compatíveis com modelos STT.
- Garantir baixa latência na amostragem (p.e., bufferSize = 2048–4096 bytes) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=const%20options%20%3D%20,%2F%2F%20default%20is%202048)).
- Validar uso de energia: desative captura quando o app não precisar, e use VAD se possível.

## 2. Diarização / Separação de Locutores
A *diarização* segmenta o áudio por locutor (Speaker A, B, etc), sem identificá-los. Em nuvem, muitas APIs oferecem isso nativamente: 
- *AssemblyAI*: ativa speaker_labels para obter segmentos (“utterances”) por locutor ([Speaker Diarization | AssemblyAI | Documentation](https://assemblyai.com/docs/speech-to-text/pre-recorded-audio/speaker-diarization#:~:text=The%20Speaker%20Diarization%20model%20lets,and%20what%20each%20speaker%20said)). 
- *Deepgram*: envie diarize=true; o retorno inclui um campo speaker para cada palavra ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)). 
- *Google Cloud Speech-to-Text*: ative enableSpeakerDiarization; cada palavra recebe um índice de locutor (p.ex. 1, 2…) ([Detect different speakers in an audio recording  |  Cloud Speech-to-Text Documentation  |  Google Cloud](https://cloud.google.com/speech-to-text/docs/multiple-voices#:~:text=When%20you%20enable%20speaker%20diarization,identify%20in%20the%20audio%20sample)). 
- *AWS Transcribe*: use ShowSpeakerLabels=true; o JSON traz speaker_labels com spk_0, spk_1, etc. para cada segmento ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9)). 
- *Azure Speech Service*: suporta diarização em tempo real, retornando campo speakerId genérico para cada trecho reconhecido ([Real-time diarization quickstart - Speech service - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization#:~:text=In%20this%20quickstart%2C%20you%20run,particular%20part%20of%20transcribed%20speech)). 
- *Rev.ai*: faz diarização por padrão, separando monólogos por locutor ([Features](https://docs.rev.ai/api/features/#:~:text=Speaker%20diarization%20is%20the%20process,will%20be%20separated%20by%20speaker)). 
- *Picovoice Falcon* (on-device): SDK que roda no iOS, detectando pontos de mudança e agrupando segmentos por características de voz ([Falcon Speaker Diarization: Transcription Diarization - Picovoice](https://picovoice.ai/platform/falcon/#:~:text=Falcon%20Speaker%20Diarization%20identifies%20speakers,based%20on%20speaker%20voice%20characteristics)). Por exemplo, Falcon.process() retorna segmentos com speakerTag. Permite processar áudio localmente (privacidade) e funciona com qualquer motor de STT ([Falcon Speaker Diarization: Transcription Diarization - Picovoice](https://picovoice.ai/platform/falcon/#:~:text=Falcon%20Speaker%20Diarization%20identifies%20speakers,based%20on%20speaker%20voice%20characteristics)) ([Falcon Speaker Diarization: Transcription Diarization - Picovoice](https://picovoice.ai/platform/falcon/#:~:text=Speaker%20Diarization%20often%20works%20with,platforms%2C%20limiting%20options%20for%20developers)).

*Resumo comparativo de diarização (exemplos)*:
| Serviço/API           | Diarização?     | Streaming/API                   | On-Device | Idiomas (ex.)      | Limite de Locutores |
|-----------------------|-----------------|---------------------------------|-----------|--------------------|---------------------|
| AssemblyAI            | Sim ([Speaker Diarization | AssemblyAI | Documentation](https://assemblyai.com/docs/speech-to-text/pre-recorded-audio/speaker-diarization#:~:text=The%20Speaker%20Diarization%20model%20lets,and%20what%20each%20speaker%20said)) | Batch e streaming (SDK/HTTP)   | Não       | Inglês, PT, etc.   | ≈ ilimitado         |
| Deepgram              | Sim ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)) | Batch e streaming (WebSocket)  | Não       | Inglês, PT_BR, etc.| ≥1 (2+)             |
| Google STT            | Sim ([Detect different speakers in an audio recording  |  Cloud Speech-to-Text Documentation  |  Google Cloud](https://cloud.google.com/speech-to-text/docs/multiple-voices#:~:text=When%20you%20enable%20speaker%20diarization,identify%20in%20the%20audio%20sample)) | Batch/streaming (REST/GRPC)    | Não       | Inglês, PT, etc.   | Detecta até X speakers (auto) |
| AWS Transcribe        | Sim ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9))  | Batch e streaming              | Não       | Inglês, PT_BR, etc.| Até 30 (spk_0..spk_29) |
| Azure Speech-to-Text  | Sim ([Real-time diarization quickstart - Speech service - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization#:~:text=In%20this%20quickstart%2C%20you%20run,particular%20part%20of%20transcribed%20speech))  | Streaming (SDK)                | Parcial*  | Inglês, PT, etc.   | ≥2 (debounce interno) |
| Rev.ai                | Sim ([Features](https://docs.rev.ai/api/features/#:~:text=Speaker%20diarization%20is%20the%20process,will%20be%20separated%20by%20speaker)) | Async (HTTP)                   | Não       | Inglês (foco)      | Não especificado    |
| Whisper (OpenAI API)  | Não (sem nativo) | Batch (HTTP)                   | Não       | 17 línguas (no API)| N/A                 |
| Whisper (local)       | Não (puro)       | Local (on-device possível)     | Sim (via ML) | ~17 línguas      | N/A                 |
| Picovoice Falcon      | Sim ([Falcon Speaker Diarization: Transcription Diarization - Picovoice](https://picovoice.ai/platform/falcon/#:~:text=Falcon%20Speaker%20Diarization%20identifies%20speakers,based%20on%20speaker%20voice%20characteristics)) | Local (SDK on-device)          | Sim       | Multilíngue**      | Ilimitado          |
\* Azure oferece transcrição de reunião com diarização em preview. **Picovoice declara suporte multilíngue mas verifique licenciamento.

## 3. Transcrição de Fala (Speech-to-Text)
Após capturar áudio e (separar locutores), transcreva cada segmento. *Opções on-device: iOS SFSpeechRecognizer (via Objective-C/Swift; não suporta diarização) ou bibliotecas RN como **react-native-voice* (usa SFSpeechRecognizer) ([GitHub - react-native-voice/voice: :microphone: React Native Voice Recognition library for iOS and Android (Online and Offline Support)](https://github.com/react-native-voice/voice#:~:text=Need%20to%20include%20permissions%20for,how%20to%20handle%20these%20cases)). Também há *Modelos ML integrados: ex. *Cheetah STT da Picovoice (offline, latência baixa) ou port do *Whisper* usando CoreML/MPS (modelos pequenos, mas consumo de CPU/energia alto). 

*Opções em nuvem*:
- AssemblyAI: alta acurácia, timestamps e etiquetas de locutor (quando habilitado) ([Speaker Diarization | AssemblyAI | Documentation](https://assemblyai.com/docs/speech-to-text/pre-recorded-audio/speaker-diarization#:~:text=The%20Speaker%20Diarization%20model%20lets,and%20what%20each%20speaker%20said)). Suporta stream ou arquivo. 
- Deepgram: boa para streaming ao vivo (WebSocket) ou arquivo, retornando palavra por palavra com timestamps e locutor ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)). 
- Google Cloud STT: suporta streaming, multilinguagem e ótima acurácia em várias línguas. Pode entregar palavra a palavra com timestamps ([Detect different speakers in an audio recording  |  Cloud Speech-to-Text Documentation  |  Google Cloud](https://cloud.google.com/speech-to-text/docs/multiple-voices#:~:text=When%20you%20enable%20speaker%20diarization,identify%20in%20the%20audio%20sample)). 
- AWS Transcribe: versão em lote ou streaming; retorna transcrição com timestamps e seção speaker_labels com segmentos por locutor ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9)). 
- Azure Speech: oferece transcription SDK com pontuações e, no modo de reunião, identificadores de locutor ([Real-time diarization quickstart - Speech service - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization#:~:text=In%20this%20quickstart%2C%20you%20run,particular%20part%20of%20transcribed%20speech)). 
- OpenAI Whisper API: modelo robusto, suporta 17 idiomas e fornece segmentos de texto com timestamps; porém, não faz diarização nativamente. 
- Rev.ai: foco em inglês, alto preço, fornece transcrições detalhadas (timestamps por palavra) e diarização padrão ([Features](https://docs.rev.ai/api/features/#:~:text=Speaker%20diarization%20is%20the%20process,will%20be%20separated%20by%20speaker)). 

Cada serviço normalmente retorna JSON com lista de palavras/frases e timestamps. Verifique limites de tempo de áudio e custo por minuto. Para reconhecimento em tempo real, use streaming (WebSocket ou SDK) quando disponível, mantendo buffers pequenos. Para áudio gravado, envie arquivos pós-captura.   

*Comparativo de APIs de Transcrição/Diarização* (exemplos de funcionalidades):

| API/Serviço      | Diarização | Streaming ao vivo | Idiomas Ex.    | Timestamps   | Saída JSON estruturada |
|------------------|------------|------------------|----------------|--------------|------------------------|
| AssemblyAI       | Sim ([Speaker Diarization | AssemblyAI | Documentation](https://assemblyai.com/docs/speech-to-text/pre-recorded-audio/speaker-diarization#:~:text=The%20Speaker%20Diarization%20model%20lets,and%20what%20each%20speaker%20said)) | Sim (SDK/Web)     | PT, EN, ES…   | Por palavra  | JSON de utterances  |
| Deepgram         | Sim ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)) | Sim (WebSocket)   | EN, PT_BR, etc.| Por palavra  | JSON words          |
| Google STT       | Sim ([Detect different speakers in an audio recording  |  Cloud Speech-to-Text Documentation  |  Google Cloud](https://cloud.google.com/speech-to-text/docs/multiple-voices#:~:text=When%20you%20enable%20speaker%20diarization,identify%20in%20the%20audio%20sample)) | Sim (gRPC)        | PT, EN, etc.   | Por palavra  | JSON de words       |
| AWS Transcribe   | Sim ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9))   | Sim (WebSocket)   | PT_BR, EN,…    | Por palavra  | JSON items + speaker_labels |
| Azure Speech     | Sim ([Real-time diarization quickstart - Speech service - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization#:~:text=In%20this%20quickstart%2C%20you%20run,particular%20part%20of%20transcribed%20speech))   | Sim (SDK)         | PT, EN,…       | Por palavra  | JSON com speakerId  |
| Whisper API      | Não        | Não (REST)        | 17 línguas     | Segmentos de frase | JSON segments    |
| Whisper local    | Não        | Sim (via modelo)  | 17 línguas     | Segmentos     | JSON custom *       |
| Picovoice Cheetah| Não        | Sim (SDK)         | EN            | n/d (foco em texto)| Texto simples (SDK) |

*Whisper local: você teria que estruturar a saída manualmente. n/d = não documentado diretamente. 

## 4. Classificação de Falas por Locutor
A classificação (etiquetagem) dos trechos é consequência da diarização. Cada segmento reconhecido recebe um label do locutor correspondente (p.ex. “Speaker 0”, “Speaker 1”, ou nomes genéricos “A”, “B”). Em muitos retornos JSON (AssemblyAI, Deepgram, AWS), já há campo de locutor por palavra ou por frase ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)) ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9)). Recomenda-se mapear números genéricos para rótulos amigáveis: por exemplo, atribuir “Locutor A/B/C” em ordem de detecção. Garanta que esse rótulo seja consistente (pode usar indexação contínua: o primeiro detected speaker = A, segundo = B, etc).  

No processamento em lote, após receber o JSON com timestamps e indices de locutor (ex: speaker_label: "spk_0"), consolide essas informações agrupando palavras consecutivas do mesmo locutor em frases. Por exemplo:

json
[
  {"start": 0.00, "end": 2.50, "speaker": "Locutor A", "text": "Olá, bom dia."},
  {"start": 2.51, "end": 5.00, "speaker": "Locutor B", "text": "Bom dia, em que posso ajudar?"}
]


Isso facilita futuros usos por LLMs ou análise posterior.

## 5. Estrutura de Output para LLM
Monte o resultado final em JSON estruturado, contendo ao menos: timestamp de início, timestamp de fim, locutor e texto. Por exemplo:  
json
[
  {"timestamp_start": 0.0,  "timestamp_end": 2.5, "speaker": "A", "text": "Primeiro locutor fala algo."},
  {"timestamp_start": 2.5,  "timestamp_end": 5.0, "speaker": "B", "text": "Segundo locutor responde."},
  ...
]
  
Esse formato facilita ingestão por LLMs. Certifique-se de que os tempos e textos sejam consistentes (ex.: sem sobreposição e com alinhamento correto). Use abreviações ou nomes curtos para locutores (A, B) para poupar tokens. 

Ao enviar para LLMs, adapte conforme necessidade: pode ser um array de objetos JSON, ou um único documento JSON. Alguns frameworks pedem strings; neste caso, converta JSON para string. Para evitar erros de formato, valide o JSON (ex. usando JSON Schema ou pydantic) antes de enviar ([Generating Perfectly Validated JSON Using LLMs — All the Time](https://python.plainenglish.io/generating-perfectly-structured-json-using-llms-all-the-time-13b7eb504240#:~:text=Generating%20Perfectly%20Validated%20JSON%20Using,Extract%20structured)). 

## 6. Integração com LLMs (Formato, Tokenização e Chunks)
Para alimentar um LLM (como GPT), envie blocos de transcrição com contexto suficiente. Considere:  
- *Tokenização: estime tokens pelo texto (padronize encoding). É comum dividir a transcrição em *chunks de, por exemplo, 500–1000 tokens (ou 1–2 minutos de fala), respeitando limites do modelo.  
- *Tamanho dos Blocos*: faça cortes em pausas naturais ou trocas de falante; prefira não cortar no meio de frases.  
- *Prompt / Instruções*: se for usar o LLM para análise, especifique função: e.g., “Dado o JSON de transcrição, responda perguntas...” ou “Resuma a conversa”.  
- *Formato Esperado*: defina claramente a estrutura de resposta. Um truque é inserir no prompt um esquema JSON desejado, evitando saídas em texto livre ([Practical Techniques to constraint LLM output in JSON format](https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670#:~:text=format%20mychen76,JSON%20Framework%20for%20LLM%20Outputs)).  
- *Armazenamento*: envie texto e metadados (timestamp/locutor) em cada requisição ou armazene em banco e envie apenas referências relevantes ao LLM.  

Exemplo de prompt: “Aqui está a transcrição de uma reunião, estruturada em JSON. Cada item tem timestamps, locutor e texto. Resuma os principais pontos de Locutor A.” Mantenha as chaves e valores claros para que o LLM não altere o formato.

## 7. Tecnologias e Pacotes RN Compatíveis (iOS)
- *Audio*: react-native-live-audio-stream (live-streaming), react-native-audio-recorder-player (gravação), expo-av ou módulos nativos (AVFoundation).  
- *Reconhecimento de voz*: @react-native-voice/voice (interface para SFSpeechRecognizer) ([GitHub - react-native-voice/voice: :microphone: React Native Voice Recognition library for iOS and Android (Online and Offline Support)](https://github.com/react-native-voice/voice#:~:text=Need%20to%20include%20permissions%20for,how%20to%20handle%20these%20cases)).  
- *Permissões*: No iOS, adicione em Info.plist as keys NSMicrophoneUsageDescription e, se usar SFSpeech, NSSpeechRecognitionUsageDescription ([GitHub - react-native-voice/voice: :microphone: React Native Voice Recognition library for iOS and Android (Online and Offline Support)](https://github.com/react-native-voice/voice#:~:text=Need%20to%20include%20permissions%20for,how%20to%20handle%20these%20cases)). No Android, permissão RECORD_AUDIO.  
- *Networking*: use fetch / Axios para enviar áudio/protocolos WebSocket das APIs cloud. Para streaming, vários SDKs (Deepgram, AssemblyAI) oferecem Node/React Native SDKs.  
- *Processamento de áudio*: se necessário, use react-native-sound ou react-native-audio-toolkit para manipular arquivos, mas cuidado com performance.  
- *Outros*: Picovoice oferece pacotes React Native (Voice Processor, Falcon via módulo nativo), e a maioria das APIs Cloud tem SDKs REST/JS que funcionam via Node.  

Sempre verifique compatibilidade de versões RN e iOS (por ex., algumas libs não suportam versões muito antigas ou iOS Simulator para áudio).

## 8. Etapas de Desenvolvimento e Testes
1. *Pesquisa e Prototipagem*: teste bibliotecas de captura e transcrição separadamente. Exemplo: capture áudio simples, envie a Google/AWS sem diarização e verifique o resultado.  
2. *Implementação da Captura*: integre o módulo de áudio no app, teste em dispositivo real (o simulador não capta microfone). Meça latência de buffer e consumo de CPU.  
3. *Integração de API STT*: envie trechos de áudio à API escolhida; valide timestamps e qualidade. Para streaming, implemente envio contínuo e recepção de resultados (ex.: WebSocket callback).  
4. *Adicionar Diarização*: habilite a opção de diarização na API (ou integre Picovoice Falcon). Teste com áudios de múltiplos falantes; verifique precisão (quem falou o quê).  
5. *Organização de Output*: aglutine palavras em frases coerentes por locutor; monte o JSON final. Teste consistência de dados (timestamps crescentes, locutores alternados corretamente).  
6. *Teste de Performance: avalie *latência (tempo do áudio até o texto), uso de rede e CPU. Para solução on-device (p.ex. Whisper local), monitore FPS e bateria. Para cloud, meça tempo de resposta e use conectividade realística (3G/4G).  
7. *Teste de Escala*: gere lotes de conversação (vários minutos, 3+ locutores) para avaliar falhas de memória ou limites de API (tamanho máximo de áudio).  
8. *Refinamento*: ajuste parâmetros (p.ex. tempo de silêncio para delimitar falas, buffer size). Adapte formatos se for usar diferentes LLMs.  
9. *Validação de Qualidade*: use métricas como WER (Word Error Rate) ou revise manualmente transcrições críticas. Compare saídas de diferentes serviços para decidir o melhor trade-off.  
10. *Preparação para Produção*: cuide de tratamento de erros de rede, repetição, chunking inteligente e atualização de tokens de API.

## 9. Considerações de Performance, Latência e Bateria
- *On-Device*: processamento local (p.ex. Whisper ou Picovoice) reduz latência de rede, mas consome muito CPU/GPU, esgotando bateria mais rápido. Modelos pequenos (Tiny Whisper, Cheetah) aliviam, mas podem perder precisão.  
- *Streaming vs. Batch*: streaming contínuo gera saída quase em tempo real, útil para apps interativos, mas mantém rede ativa. Envio em lote (após pausa) economiza energia mas introduz atraso. Equilibre conforme caso de uso.  
- *Uso de Rede*: comprima áudio (opus/PCM 16-bit) para enviar. Use protocolos eficientes (WebSocket p/ Deepgram, HTTP2). Cuidado com conexão instável: implemente reconexão.  
- *Exaurir API*: monitore chamadas para não exceder limites. Prefira variantes pagas somente se necessário.  
- *Buffer de Áudio*: cuidado para não acumular muito áudio em memória. Libere buffers/objetos após uso.  
- *Verifique Carga*: use ferramentas de profiling (Xcode Instruments) para observar uso de CPU/memória. No RN, minimize bridge overhead (envie dados binários, não JSON gigante pela ponte).  

## 10. Integração Final com LLMs
Uma vez obtida a estrutura JSON, a integração com LLM envolve: enviar esse JSON (ou seus conteúdos) junto com instruções específicas no prompt. Por exemplo: “Dada a transcrição abaixo (JSON com timestamps e falantes), faça uma sumarização.” Certifique-se de que o JSON não exceda o tamanho do prompt. Se o contexto for muito longo, resuma ou selecione as partes mais relevantes. Uma estratégia é usar um “RAG” (Recuperação + Geração) onde o LLM consulta partes do transcript conforme a pergunta. Em todos os casos, o JSON bem estruturado acelera o parse automático do LLM.

*Exemplo de Output JSON usado por LLM*:
json
[
  {"timestamp_start": 0.00, "timestamp_end": 2.50, "speaker": "A", "text": "Bom dia, estamos começando a reunião."},
  {"timestamp_start": 2.51, "timestamp_end": 5.20, "speaker": "B", "text": "Bom dia a todos. Vou apresentar as métricas do mês."},
  ...
]

No prompt, você pode inserir esse JSON diretamente ou fragmentos importantes. Muitos LLMs atuais já entendem chaves como "speaker" e "text" sem problema; se necessário, inclua instruções como “Mantenha este formato JSON” para que a resposta fique estruturada, evitando interpretações livres ([Practical Techniques to constraint LLM output in JSON format](https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670#:~:text=format%20mychen76,JSON%20Framework%20for%20LLM%20Outputs)).

## Referências
- Documentação oficial de APIs (AssemblyAI, Deepgram, Google Cloud, AWS, Azure, Rev.ai) para recursos de diarização e timestamps ([Speaker Diarization | AssemblyAI | Documentation](https://assemblyai.com/docs/speech-to-text/pre-recorded-audio/speaker-diarization#:~:text=The%20Speaker%20Diarization%20model%20lets,and%20what%20each%20speaker%20said)) ([Diarization — Deepgram | Documentation](https://developers.deepgram.com/docs/diarization#:~:text=Diarization)) ([Detect different speakers in an audio recording  |  Cloud Speech-to-Text Documentation  |  Google Cloud](https://cloud.google.com/speech-to-text/docs/multiple-voices#:~:text=When%20you%20enable%20speaker%20diarization,identify%20in%20the%20audio%20sample)) ([Partitioning speakers (diarization) - Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html#:~:text=With%20speaker%20diarization%2C%20you%20can,spk_9)) ([Features](https://docs.rev.ai/api/features/#:~:text=Speaker%20diarization%20is%20the%20process,will%20be%20separated%20by%20speaker)) ([Real-time diarization quickstart - Speech service - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization#:~:text=In%20this%20quickstart%2C%20you%20run,particular%20part%20of%20transcribed%20speech)).  
- Biblioteca React Native para captura de áudio: react-native-live-audio-stream (fluxo de áudio em tempo real) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=react)) ([GitHub - xiqi/react-native-live-audio-stream: Get live audio stream data for React Native (works for iOS and Android)](https://github.com/xiqi/react-native-live-audio-stream#:~:text=import%20LiveAudioStream%20from%20%27react)).  
- Comunicado Apple: não há suporte nativo para reconhecimento de múltiplos locutores no iOS até a data ([Speech diarization | Apple Developer Forums](https://developer.apple.com/forums/thread/766606#:~:text=Hello%20%40mjlee%2C%20thank%20you%20for,with%20the%20APIs%20currently%20available)).  
- Picovoice Falcon (diarização local): identifica change points e segmenta por locutor ([Falcon Speaker Diarization: Transcription Diarization - Picovoice](https://picovoice.ai/platform/falcon/#:~:text=Falcon%20Speaker%20Diarization%20identifies%20speakers,based%20on%20speaker%20voice%20characteristics)).