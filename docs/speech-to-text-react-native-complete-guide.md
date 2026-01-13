# Apple Speech-to-Text in React Native: The Complete Implementation Guide

**iOS speech recognition in React Native requires bridging Apple's SFSpeechRecognizer framework through either existing libraries or custom native modules.** The two production-ready approaches are: using `expo-speech-recognition` (actively maintained, feature-rich) or `@react-native-voice/voice` (widely adopted but stagnant since 2022). For maximum control, teams can build custom native modules that directly interface with SFSpeechRecognizer. All approaches require iOS 10+ for basic functionality and iOS 13+ for on-device recognition, with mandatory Info.plist permissions for both microphone and speech recognition access.

---

## Choosing the right library for your project

Three viable options exist for React Native speech recognition on iOS, each with distinct trade-offs:

| Library | Maintenance | Key Strength | Limitation |
|---------|-------------|--------------|------------|
| **expo-speech-recognition** | ✅ Active (v3.0.1, Nov 2025) | Full-featured with Expo plugin | iOS 17+ for all features |
| **@react-native-voice/voice** | ⚠️ Stagnant (v3.2.4, May 2022) | Battle-tested, 2.1k stars | Known iOS bugs unfixed |
| **Custom native module** | N/A | Complete control | Development overhead |

**expo-speech-recognition** emerges as the strongest choice for new projects. It provides on-device recognition control, audio recording persistence, volume metering, and file-based transcription—features absent from react-native-voice. The library works across Expo SDK 50-52 and requires only `npx expo prebuild` after installation.

**@react-native-voice/voice** remains functional but carries technical debt. GitHub issues document problems including recognition failures after the first run, Bluetooth headphone crashes, and intermittent Error 203 failures. Without active maintenance since 2022, these issues persist.

Both libraries use Apple's native **SFSpeechRecognizer** framework internally. The `expo-speech` package (different from expo-speech-recognition) provides Text-to-Speech only and cannot perform speech recognition.

---

## Building a custom native module from scratch

Custom native modules offer maximum flexibility for teams needing fine-grained control over recognition behavior, audio session configuration, or integration with other native components.

### Swift implementation (SpeechRecognizerModule.swift)

```swift
import Foundation
import Speech
import AVFoundation
import React

@objc(SpeechRecognizerModule)
class SpeechRecognizerModule: RCTEventEmitter {
    
    // MARK: - Private Properties
    private var speechRecognizer: SFSpeechRecognizer?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    private var isRecording = false
    private let recognizingSemaphore = DispatchSemaphore(value: 1)
    
    // MARK: - RCTEventEmitter Configuration
    override static func moduleName() -> String! { "SpeechRecognizerModule" }
    
    @objc override static func requiresMainQueueSetup() -> Bool { true }
    
    override func supportedEvents() -> [String]! {
        ["onSpeechStart", "onSpeechEnd", "onSpeechResult", 
         "onSpeechPartialResult", "onSpeechError"]
    }
    
    private var hasListeners = false
    override func startObserving() { hasListeners = true }
    override func stopObserving() { hasListeners = false }
    
    // MARK: - Authorization
    @objc(requestAuthorization:rejecter:)
    func requestAuthorization(
        _ resolve: @escaping RCTPromiseResolveBlock,
        rejecter reject: @escaping RCTPromiseRejectBlock
    ) {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                let result: [String: Any] = switch authStatus {
                case .authorized: ["status": "authorized", "granted": true]
                case .denied: ["status": "denied", "granted": false]
                case .restricted: ["status": "restricted", "granted": false]
                case .notDetermined: ["status": "not-determined", "granted": false]
                @unknown default: ["status": "unknown", "granted": false]
                }
                resolve(result)
            }
        }
    }
    
    // MARK: - Real-time Recognition
    @objc(startRecognition:resolver:rejecter:)
    func startRecognition(
        _ options: NSDictionary,
        resolver resolve: @escaping RCTPromiseResolveBlock,
        rejecter reject: @escaping RCTPromiseRejectBlock
    ) {
        guard recognizingSemaphore.wait(timeout: .now() + 5.0) == .success else {
            reject("BUSY", "Recognition is busy", nil)
            return
        }
        
        let locale = options["locale"] as? String ?? "en-US"
        let requiresOnDevice = options["requiresOnDeviceRecognition"] as? Bool ?? false
        let shouldReportPartialResults = options["interimResults"] as? Bool ?? true
        let contextualStrings = options["contextualStrings"] as? [String] ?? []
        
        speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: locale))
        
        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            recognizingSemaphore.signal()
            reject("UNAVAILABLE", "Speech recognizer unavailable for \(locale)", nil)
            return
        }
        
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // Configure audio session
        do {
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playAndRecord, mode: .measurement,
                                         options: [.defaultToSpeaker, .allowBluetooth])
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            recognizingSemaphore.signal()
            reject("AUDIO_SESSION_ERROR", error.localizedDescription, nil)
            return
        }
        
        // Create and configure recognition request
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let request = recognitionRequest else {
            recognizingSemaphore.signal()
            reject("REQUEST_ERROR", "Unable to create recognition request", nil)
            return
        }
        
        request.shouldReportPartialResults = shouldReportPartialResults
        if #available(iOS 13.0, *) {
            request.requiresOnDeviceRecognition = requiresOnDevice
        }
        if !contextualStrings.isEmpty {
            request.contextualStrings = contextualStrings
        }
        
        let inputNode = audioEngine.inputNode
        
        // Start recognition task with result handling
        recognitionTask = recognizer.recognitionTask(with: request) { [weak self] result, error in
            guard let self = self else { return }
            var isFinal = false
            
            if let result = result {
                isFinal = result.isFinal
                let transcription = result.bestTranscription.formattedString
                
                var segments: [[String: Any]] = []
                for segment in result.bestTranscription.segments {
                    segments.append([
                        "substring": segment.substring,
                        "timestamp": segment.timestamp,
                        "duration": segment.duration,
                        "confidence": segment.confidence
                    ])
                }
                
                let eventBody: [String: Any] = [
                    "transcript": transcription,
                    "isFinal": isFinal,
                    "segments": segments
                ]
                
                if self.hasListeners {
                    let eventName = isFinal ? "onSpeechResult" : "onSpeechPartialResult"
                    self.sendEvent(withName: eventName, body: eventBody)
                }
            }
            
            if error != nil || isFinal {
                self.audioEngine.stop()
                inputNode.removeTap(onBus: 0)
                self.recognitionRequest = nil
                self.recognitionTask = nil
                self.isRecording = false
                
                if let error = error, self.hasListeners {
                    self.sendEvent(withName: "onSpeechError", body: [
                        "message": error.localizedDescription,
                        "code": (error as NSError).code
                    ])
                }
                if self.hasListeners {
                    self.sendEvent(withName: "onSpeechEnd", body: nil)
                }
            }
        }
        
        // Install audio tap for streaming
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) 
            { [weak self] buffer, _ in
            self?.recognitionRequest?.append(buffer)
        }
        
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
            isRecording = true
            recognizingSemaphore.signal()
            if hasListeners { sendEvent(withName: "onSpeechStart", body: nil) }
            resolve(true)
        } catch {
            recognizingSemaphore.signal()
            reject("AUDIO_ENGINE_ERROR", error.localizedDescription, nil)
        }
    }
    
    // MARK: - File-based Transcription
    @objc(transcribeFile:options:resolver:rejecter:)
    func transcribeFile(
        _ filePath: String,
        options: NSDictionary,
        resolver resolve: @escaping RCTPromiseResolveBlock,
        rejecter reject: @escaping RCTPromiseRejectBlock
    ) {
        let locale = options["locale"] as? String ?? "en-US"
        
        guard let url = URL(string: filePath) else {
            reject("INVALID_URL", "Invalid file path", nil)
            return
        }
        
        speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: locale))
        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            reject("UNAVAILABLE", "Speech recognizer not available", nil)
            return
        }
        
        let request = SFSpeechURLRecognitionRequest(url: url)
        if #available(iOS 13.0, *) {
            request.requiresOnDeviceRecognition = options["requiresOnDeviceRecognition"] 
                as? Bool ?? true
        }
        
        recognizer.recognitionTask(with: request) { result, error in
            if let error = error {
                reject("TRANSCRIPTION_ERROR", error.localizedDescription, nil)
                return
            }
            guard let result = result, result.isFinal else { return }
            resolve(["transcript": result.bestTranscription.formattedString])
        }
    }
    
    // MARK: - Stop/Abort
    @objc(stopRecognition:rejecter:)
    func stopRecognition(_ resolve: @escaping RCTPromiseResolveBlock,
                         rejecter reject: @escaping RCTPromiseRejectBlock) {
        recognitionRequest?.endAudio()
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        isRecording = false
        resolve(true)
    }
    
    @objc(abortRecognition:rejecter:)
    func abortRecognition(_ resolve: @escaping RCTPromiseResolveBlock,
                          rejecter reject: @escaping RCTPromiseRejectBlock) {
        recognitionTask?.cancel()
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest = nil
        recognitionTask = nil
        isRecording = false
        resolve(true)
    }
    
    deinit {
        if isRecording {
            audioEngine.stop()
            audioEngine.inputNode.removeTap(onBus: 0)
        }
        recognitionTask?.cancel()
    }
}
```

### Objective-C bridge (SpeechRecognizerModuleBridge.m)

```objc
#import <React/RCTBridgeModule.h>
#import <React/RCTEventEmitter.h>

@interface RCT_EXTERN_MODULE(SpeechRecognizerModule, RCTEventEmitter)

RCT_EXTERN_METHOD(requestAuthorization:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)

RCT_EXTERN_METHOD(startRecognition:(NSDictionary *)options
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)

RCT_EXTERN_METHOD(stopRecognition:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)

RCT_EXTERN_METHOD(abortRecognition:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)

RCT_EXTERN_METHOD(transcribeFile:(NSString *)filePath
                  options:(NSDictionary *)options
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)
@end
```

---

## TypeScript interface and React hook

### SpeechRecognizer.ts

```typescript
import { NativeModules, NativeEventEmitter, Platform, EmitterSubscription } from 'react-native';

const { SpeechRecognizerModule } = NativeModules;

export interface SpeechRecognitionOptions {
  locale?: string;
  requiresOnDeviceRecognition?: boolean;
  interimResults?: boolean;
  contextualStrings?: string[];
}

export interface SpeechSegment {
  substring: string;
  timestamp: number;
  duration: number;
  confidence: number;
}

export interface SpeechResultEvent {
  transcript: string;
  isFinal: boolean;
  segments: SpeechSegment[];
}

export interface SpeechErrorEvent {
  message: string;
  code: number;
}

type SpeechEventType = 'onSpeechStart' | 'onSpeechEnd' | 'onSpeechResult' | 
                       'onSpeechPartialResult' | 'onSpeechError';

const eventEmitter = Platform.OS === 'ios' 
  ? new NativeEventEmitter(SpeechRecognizerModule) : null;

class SpeechRecognizer {
  async requestAuthorization(): Promise<{ status: string; granted: boolean }> {
    if (Platform.OS !== 'ios') throw new Error('iOS only');
    return SpeechRecognizerModule.requestAuthorization();
  }

  async startRecognition(options: SpeechRecognitionOptions = {}): Promise<boolean> {
    if (Platform.OS !== 'ios') throw new Error('iOS only');
    return SpeechRecognizerModule.startRecognition({
      locale: 'en-US',
      requiresOnDeviceRecognition: false,
      interimResults: true,
      contextualStrings: [],
      ...options,
    });
  }

  async stopRecognition(): Promise<boolean> {
    if (Platform.OS !== 'ios') return false;
    return SpeechRecognizerModule.stopRecognition();
  }

  async abortRecognition(): Promise<boolean> {
    if (Platform.OS !== 'ios') return false;
    return SpeechRecognizerModule.abortRecognition();
  }

  async transcribeFile(filePath: string, options: Partial<SpeechRecognitionOptions> = {}) {
    if (Platform.OS !== 'ios') throw new Error('iOS only');
    return SpeechRecognizerModule.transcribeFile(filePath, {
      locale: 'en-US',
      requiresOnDeviceRecognition: true,
      ...options,
    });
  }

  addEventListener(event: SpeechEventType, handler: (data: any) => void): EmitterSubscription | null {
    if (!eventEmitter) return null;
    return eventEmitter.addListener(event, handler);
  }

  removeAllListeners(): void {
    eventEmitter?.removeAllListeners('onSpeechStart');
    eventEmitter?.removeAllListeners('onSpeechEnd');
    eventEmitter?.removeAllListeners('onSpeechResult');
    eventEmitter?.removeAllListeners('onSpeechPartialResult');
    eventEmitter?.removeAllListeners('onSpeechError');
  }
}

export default new SpeechRecognizer();
```

### useSpeechRecognition hook

```typescript
import { useEffect, useState, useCallback, useRef } from 'react';
import SpeechRecognizer, { SpeechRecognitionOptions, SpeechResultEvent, SpeechErrorEvent } from './SpeechRecognizer';
import { EmitterSubscription, AppState } from 'react-native';

export function useSpeechRecognition() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [partialTranscript, setPartialTranscript] = useState('');
  const [error, setError] = useState<SpeechErrorEvent | null>(null);
  const subscriptionsRef = useRef<(EmitterSubscription | null)[]>([]);
  const isMountedRef = useRef(true);

  useEffect(() => {
    // Event listeners
    subscriptionsRef.current = [
      SpeechRecognizer.addEventListener('onSpeechStart', () => {
        if (isMountedRef.current) { setIsListening(true); setError(null); }
      }),
      SpeechRecognizer.addEventListener('onSpeechEnd', () => {
        if (isMountedRef.current) setIsListening(false);
      }),
      SpeechRecognizer.addEventListener('onSpeechResult', (e: SpeechResultEvent) => {
        if (isMountedRef.current) { setTranscript(e.transcript); setPartialTranscript(''); }
      }),
      SpeechRecognizer.addEventListener('onSpeechPartialResult', (e: SpeechResultEvent) => {
        if (isMountedRef.current) setPartialTranscript(e.transcript);
      }),
      SpeechRecognizer.addEventListener('onSpeechError', (e: SpeechErrorEvent) => {
        if (isMountedRef.current) { setError(e); setIsListening(false); }
      }),
    ];

    // Handle app background (speech recognition stops in background)
    const appStateSubscription = AppState.addEventListener('change', async (state) => {
      if (state !== 'active' && isListening) {
        await SpeechRecognizer.stopRecognition();
      }
    });

    return () => {
      isMountedRef.current = false;
      subscriptionsRef.current.forEach(sub => sub?.remove());
      appStateSubscription.remove();
      SpeechRecognizer.abortRecognition();
    };
  }, []);

  const startListening = useCallback(async (options?: SpeechRecognitionOptions) => {
    setTranscript('');
    setPartialTranscript('');
    setError(null);
    
    const auth = await SpeechRecognizer.requestAuthorization();
    if (!auth.granted) {
      setError({ message: `Permission ${auth.status}`, code: -1 });
      return false;
    }
    
    return SpeechRecognizer.startRecognition(options);
  }, []);

  const stopListening = useCallback(() => SpeechRecognizer.stopRecognition(), []);
  const abortListening = useCallback(() => SpeechRecognizer.abortRecognition(), []);

  return { isListening, transcript, partialTranscript, error, startListening, stopListening, abortListening };
}
```

---

## iOS configuration requirements

### Info.plist (mandatory)

```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app uses the microphone to recognize your speech.</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>This app uses speech recognition to convert your voice to text.</string>
```

Both keys are **required**—the app will crash without them. For Expo projects, the config plugin handles this automatically.

### Expo configuration (app.json)

```json
{
  "expo": {
    "plugins": [
      ["expo-speech-recognition", {
        "microphonePermission": "Allow $(PRODUCT_NAME) to use the microphone.",
        "speechRecognitionPermission": "Allow $(PRODUCT_NAME) to use speech recognition."
      }]
    ]
  }
}
```

After configuration: run `npx expo prebuild` then `npx expo run:ios`.

### iOS version compatibility matrix

| iOS Version | Key Features |
|-------------|--------------|
| **iOS 10** | SFSpeechRecognizer introduced, server-based recognition, 60-second limit |
| **iOS 13** | **On-device recognition** (`requiresOnDeviceRecognition`), unlimited duration offline |
| **iOS 16** | `addsPunctuation` for automatic punctuation insertion |
| **iOS 17** | Custom language model support, improved transformer-based accuracy |
| **iOS 18** | Enhanced transcription accuracy |

On-device recognition requires **iOS 13+** and an **A9 chip or newer** (iPhone 6s+). Check availability at runtime with `recognizer.supportsOnDeviceRecognition`.

---

## Common errors and their solutions

### Error 201: "Siri and Dictation are disabled"

**Cause:** iOS 15+ requires either Siri or Keyboard Dictation enabled system-wide.

**Solutions:**
- User enables: Settings → General → Keyboards → Enable Dictation
- Use `requiresOnDeviceRecognition: true` to bypass this requirement
- Display user-friendly guidance pointing to Settings

### Error 203: Recognition failed

**Cause:** Network connectivity issues or server unavailable.

**Solutions:**
- Check network connectivity before starting
- Implement retry with exponential backoff
- Fall back to on-device recognition

### Error 1700: Background mode not supported

**Cause:** SFSpeechRecognizer does not function in background.

**Solution:** Stop recognition when app enters background:

```javascript
AppState.addEventListener('change', async (state) => {
  if (state !== 'active') await SpeechRecognizer.stopRecognition();
});
```

### Recognition stops after first attempt

**Cause:** Common react-native-voice bug where resources aren't properly released.

**Solution:** Call `destroy()` before starting new sessions:

```javascript
await Voice.destroy();
await Voice.removeAllListeners();
await Voice.start('en-US');
```

### Audio session conflicts with Bluetooth

**Solution:** Configure audio session with Bluetooth options:

```swift
try audioSession.setCategory(.playAndRecord, mode: .measurement,
                             options: [.defaultToSpeaker, .allowBluetooth])
```

---

## Expo workflow compatibility

| Workflow | Speech Recognition Support |
|----------|---------------------------|
| **Expo Go** | ❌ Not supported (requires native code) |
| **Development Build** | ✅ With config plugin |
| **EAS Build** | ✅ With config plugin |
| **Bare Workflow** | ✅ Manual configuration |

The `expo-speech` package provides **Text-to-Speech only**. For Speech-to-Text in Expo, use `expo-speech-recognition` (third-party) which provides a config plugin and full SFSpeechRecognizer integration.

---

## Production usage example

```tsx
import React from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { useSpeechRecognition } from './useSpeechRecognition';

export function VoiceInput({ onTranscript }: { onTranscript: (text: string) => void }) {
  const { isListening, transcript, partialTranscript, error, startListening, stopListening } = 
    useSpeechRecognition();

  const handlePress = async () => {
    if (isListening) {
      await stopListening();
      if (transcript) onTranscript(transcript);
    } else {
      await startListening({
        locale: 'en-US',
        interimResults: true,
        requiresOnDeviceRecognition: false,
        contextualStrings: ['React Native', 'SFSpeechRecognizer'], // Improves accuracy
      });
    }
  };

  return (
    <View style={styles.container}>
      <Pressable style={[styles.button, isListening && styles.active]} onPress={handlePress}>
        <Text style={styles.buttonText}>{isListening ? '⏹ Stop' : '🎤 Start'}</Text>
      </Pressable>
      <Text style={styles.transcript}>{partialTranscript || transcript || 'Tap to speak...'}</Text>
      {error && <Text style={styles.error}>Error: {error.message}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  button: { backgroundColor: '#007AFF', padding: 16, borderRadius: 8, alignItems: 'center' },
  active: { backgroundColor: '#FF3B30' },
  buttonText: { color: 'white', fontSize: 18, fontWeight: '600' },
  transcript: { marginTop: 16, fontSize: 16, color: '#333' },
  error: { marginTop: 8, color: '#FF3B30' },
});
```

---

## Critical constraints to remember

Apple imposes hard limits on speech recognition: **1,000 requests per hour per device** for server-based recognition and a **60-second maximum duration** per request. On-device recognition (`requiresOnDeviceRecognition: true`) bypasses both limits but offers slightly lower accuracy. Recognition categorically fails in background mode—always stop recognition before the app enters background state.

For production deployments, implement automatic silence detection (stop after 2-3 seconds of no speech), handle all authorization states gracefully including the `restricted` state from MDM profiles, and always test on physical devices since simulators have unreliable speech recognition behavior.