# Apple Speech-to-Text in React Native: The Complete Implementation Guide

**iOS speech recognition in React Native requires bridging Apple's SFSpeechRecognizer framework through either existing libraries or custom native modules.** The two production-ready approaches are: using `expo-speech-recognition` (actively maintained, feature-rich) or `@react-native-voice/voice` (widely adopted but stagnant since 2022). For maximum control, teams can build custom native modules that directly interface with SFSpeechRecognizer. All approaches require iOS 10+ for basic functionality and iOS 13+ for on-device recognition, with mandatory Info.plist permissions for both microphone and speech recognition access.

... (continua)