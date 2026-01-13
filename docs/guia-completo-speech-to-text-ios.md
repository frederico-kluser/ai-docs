# Guia Completo: Speech-to-Text nativo no iOS (Apple Speech Framework)
<!-- Arquivo renomeado para: guia-completo-speech-to-text-ios.md -->

Apple's Speech framework provides **production-ready speech recognition** since iOS 10, with on-device processing available from iOS 13. The framework centers on `SFSpeechRecognizer`, which delivers real-time transcription through either server-based or on-device recognition. For privacy-sensitive applications, on-device recognition eliminates data transmission to Apple servers entirely, though with slightly reduced accuracy and limited language support (**~22 languages on-device vs. 50+ server-based**).

The most significant recent evolution is **iOS 17's custom language model support** (`SFCustomLanguageModelData`), enabling domain-specific vocabulary boosting with custom pronunciations—critical for medical, legal, or technical applications. iOS 26 introduces the entirely new `SpeechAnalyzer` API with improved offline-first architecture.

---

## Framework architecture and class hierarchy

The Speech framework follows a straightforward request-task-result pattern. Understanding this hierarchy is essential for proper implementation.

### Core classes and their relationships

**SFSpeechRecognizer** serves as the primary controller, managing locale-specific recognition and authorization. It creates recognition tasks from requests and delivers results through completion handlers or delegates.

```swift
// Core initialization pattern
let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
speechRecognizer?.delegate = self  // Monitor availability changes
```

**SFSpeechRecognitionRequest** is an abstract base class with two concrete implementations:
- `SFSpeechAudioBufferRecognitionRequest` — for real-time microphone input via AVAudioEngine
- `SFSpeechURLRecognitionRequest` — for pre-recorded audio files

**SFSpeechRecognitionTask** represents an active recognition session with states: `.starting`, `.running`, `.finishing`, `.canceling`, `.completed`. Tasks can be cancelled mid-recognition and report errors through their `error` property.

**SFSpeechRecognitionResult** contains transcription results with:
- `bestTranscription: SFTranscription` — highest confidence result
- `transcriptions: [SFTranscription]` — alternatives sorted by confidence
- `isFinal: Bool` — indicates recognition completion

**SFTranscription** provides `formattedString` (the complete text) and `segments: [SFTranscriptionSegment]` containing individual words with timestamps, duration, confidence scores (**0.0–1.0**), and alternative interpretations.

### Data flow from microphone to text

```
Microphone → AVAudioEngine.inputNode → Audio Tap → AVAudioPCMBuffer
                                                         ↓
                                    SFSpeechAudioBufferRecognitionRequest.append()
                                                         ↓
                                         SFSpeechRecognizer.recognitionTask()
                                                         ↓
                                    SFSpeechRecognitionResult (partial/final)
```

For file-based recognition, the flow simplifies to `Audio File URL → SFSpeechURLRecognitionRequest → SFSpeechRecognizer → Results`.

---

## Required configuration and permissions

### Info.plist keys (mandatory)

Both keys below are **required**—omitting them causes immediate app crashes:

```xml
<key>NSSpeechRecognitionUsageDescription</key>
<string>This app uses speech recognition to transcribe your voice for [specific feature].</string>

<key>NSMicrophoneUsageDescription</key>
<string>This app needs microphone access to record your voice for transcription.</string>
```

Apple automatically appends to the speech recognition prompt: *"Speech data from this app will be sent to Apple to process your requests."* (for server-based recognition only).

### Authorization flow implementation

```swift
import Speech

func requestSpeechAuthorization(completion: @escaping (Bool) -> Void) {
    SFSpeechRecognizer.requestAuthorization { status in
        DispatchQueue.main.async {
            switch status {
            case .authorized:
                completion(true)
            case .denied:
                // User denied—must enable in Settings manually
                self.promptSettingsNavigation()
                completion(false)
            case .restricted:
                // Device policy prevents usage (MDM, parental controls)
                completion(false)
            case .notDetermined:
                completion(false)
            @unknown default:
                completion(false)
            }
        }
    }
}

func promptSettingsNavigation() {
    if let url = URL(string: UIApplication.openSettingsURLString) {
        UIApplication.shared.open(url)
    }
}
```

**Critical limitation**: iOS shows the permission dialog **only once**. After denial, users must manually enable speech recognition in Settings > Privacy > Speech Recognition.

### Audio session configuration

```swift
func configureAudioSession() throws {
    let audioSession = AVAudioSession.sharedInstance()
    try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
    try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
}
```

The `.measurement` mode minimizes system signal processing, improving recognition accuracy. Register for interruption notifications to handle phone calls and Siri activations gracefully:

```swift
NotificationCenter.default.addObserver(
    forName: AVAudioSession.interruptionNotification,
    object: nil,
    queue: .main
) { [weak self] notification in
    guard let type = notification.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt,
          let interruptionType = AVAudioSession.InterruptionType(rawValue: type) else { return }
    
    if interruptionType == .began {
        self?.pauseRecognition()
    }
}
```

---

## Complete implementation with working Swift code

### Real-time speech recognition (live audio)

```swift
import Speech
import AVFoundation

class SpeechRecognitionManager: NSObject, SFSpeechRecognizerDelegate {
    
    // MARK: - Properties
    private let speechRecognizer: SFSpeechRecognizer?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    
    var onTranscriptionUpdate: ((String, Bool) -> Void)?  // (text, isFinal)
    var onError: ((Error) -> Void)?
    
    // MARK: - Initialization
    override init() {
        self.speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
        super.init()
        self.speechRecognizer?.delegate = self
    }
    
    // MARK: - Start Recognition
    func startRecording() throws {
        // Cancel any existing task
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // Configure audio session
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        
        // Create recognition request
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        
        guard let recognitionRequest = recognitionRequest,
              let speechRecognizer = speechRecognizer else {
            throw NSError(domain: "SpeechRecognition", code: -1, 
                         userInfo: [NSLocalizedDescriptionKey: "Speech recognizer unavailable"])
        }
        
        // Configure request
        recognitionRequest.shouldReportPartialResults = true
        
        // Enable on-device recognition if available (iOS 13+)
        if #available(iOS 13, *) {
            recognitionRequest.requiresOnDeviceRecognition = speechRecognizer.supportsOnDeviceRecognition
        }
        
        // Enable automatic punctuation (iOS 16+)
        if #available(iOS 16, *) {
            recognitionRequest.addsPunctuation = true
        }
        
        // Custom vocabulary for domain-specific terms
        recognitionRequest.contextualStrings = ["your", "custom", "terms"]
        
        // Start recognition task
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            var isFinal = false
            
            if let result = result {
                let transcription = result.bestTranscription.formattedString
                isFinal = result.isFinal
                self.onTranscriptionUpdate?(transcription, isFinal)
            }
            
            if let error = error {
                self.onError?(error)
                self.stopRecording()
            } else if isFinal {
                self.stopRecording()
            }
        }
        
        // Configure audio engine input
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            self.recognitionRequest?.append(buffer)
        }
        
        audioEngine.prepare()
        try audioEngine.start()
    }
    
    // MARK: - Stop Recognition
    func stopRecording() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        
        recognitionRequest?.endAudio()
        recognitionRequest = nil
        
        recognitionTask?.cancel()
        recognitionTask = nil
        
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
    }
    
    // MARK: - SFSpeechRecognizerDelegate
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        if !available {
            stopRecording()
        }
    }
}
```

### Pre-recorded audio file transcription

```swift
func transcribeAudioFile(url: URL, completion: @escaping (Result<String, Error>) -> Void) {
    guard let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")),
          speechRecognizer.isAvailable else {
        completion(.failure(NSError(domain: "Speech", code: -1, 
                                   userInfo: [NSLocalizedDescriptionKey: "Recognizer unavailable"])))
        return
    }
    
    let request = SFSpeechURLRecognitionRequest(url: url)
    request.shouldReportPartialResults = false  // Only final result for files
    
    // Prefer on-device for privacy (iOS 13+)
    if #available(iOS 13, *) {
        request.requiresOnDeviceRecognition = speechRecognizer.supportsOnDeviceRecognition
    }
    
    if #available(iOS 16, *) {
        request.addsPunctuation = true
    }
    
    speechRecognizer.recognitionTask(with: request) { result, error in
        DispatchQueue.main.async {
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let result = result, result.isFinal else { return }
            completion(.success(result.bestTranscription.formattedString))
        }
    }
}
```

### Accessing detailed transcription segments

```swift
func processSegments(from result: SFSpeechRecognitionResult) {
    let transcription = result.bestTranscription
    
    for segment in transcription.segments {
        print("Word: \(segment.substring)")
        print("  Timestamp: \(segment.timestamp)s")
        print("  Duration: \(segment.duration)s")
        print("  Confidence: \(segment.confidence)")  // 0.0 to 1.0
        print("  Alternatives: \(segment.alternativeSubstrings)")
        
        // Voice analytics (iOS 13+)
        if #available(iOS 13, *), let analytics = segment.voiceAnalytics {
            print("  Pitch values: \(analytics.pitch.acousticFeatureValuePerFrame)")
        }
    }
}
```

---

## On-device versus server-based recognition

The choice between on-device and server-based recognition involves critical trade-offs:

| Factor | On-Device (iOS 13+) | Server-Based |
|--------|---------------------|--------------|
| **Privacy** | Audio never leaves device | Audio sent to Apple |
| **Network** | Not required | Required |
| **Audio duration** | **Unlimited** | ~1 minute maximum |
| **Request limits** | None | 1,000/hour per device |
| **Languages** | ~22 languages | 50+ languages |
| **Accuracy** | Good, slightly lower | Higher (continuous learning) |
| **Latency** | Lower | Network-dependent |
| **Hardware** | A9 processor or newer | Any iOS 10+ device |

```swift
// Force on-device recognition for privacy-critical apps
if #available(iOS 13, *) {
    if speechRecognizer.supportsOnDeviceRecognition {
        request.requiresOnDeviceRecognition = true
    } else {
        // Handle: on-device not available for this locale
        // Either fall back to server or show user message
    }
}
```

**Note**: `supportsOnDeviceRecognition` may return `false` initially and `true` after a few seconds on some iOS versions. On-device models must be downloaded via Settings > General > Keyboard > Dictation Languages.

---

## Rate limits and audio duration constraints

### Hard limits (server-based)

- **1,000 requests per hour** per device (across all apps)
- **~1 minute maximum audio** per recognition request
- Recognition tasks terminate after **~22 seconds of silence**

### Detection and handling

```swift
// Rate limit error detection
func handleRecognitionError(_ error: Error) {
    let nsError = error as NSError
    
    if nsError.domain == "kAFAssistantErrorDomain" {
        switch nsError.code {
        case 203: // Retry error
            retryWithExponentialBackoff()
        case 209: // Recognition failed
            restartRecognition()
        case 216: // Multiple request conflict
            cancelExistingAndRestart()
        default:
            showGenericError(nsError.localizedDescription)
        }
    } else if nsError.domain == "SiriSpeechErrorDomain" {
        // Quota limit reached
        showQuotaExceededMessage()
    }
}
```

### Workaround for long audio

For audio exceeding one minute, use **on-device recognition** (unlimited duration) or segment audio at silence boundaries:

```swift
// Segment long audio into ~55 second chunks with overlap handling
func transcribeLongAudio(url: URL) async throws -> String {
    // Prefer on-device for unlimited duration
    if speechRecognizer.supportsOnDeviceRecognition {
        request.requiresOnDeviceRecognition = true
        // No duration limit with on-device
    } else {
        // Implement chunking with timestamp tracking
    }
}
```

---

## Supported languages and locale handling

Check language availability programmatically:

```swift
// All supported locales
let allLocales = SFSpeechRecognizer.supportedLocales()
print("Supported locales: \(allLocales.count)")  // 50+

// Check specific locale
if let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP")) {
    print("Japanese available: \(recognizer.isAvailable)")
    
    if #available(iOS 13, *) {
        print("Japanese on-device: \(recognizer.supportsOnDeviceRecognition)")
    }
}
```

**On-device supported languages** (iOS 15+, ~22 locales): English variants, Spanish variants, French, German, Italian, Portuguese (BR), Russian, Chinese (Simplified, Traditional, Cantonese), Japanese, Korean, Arabic, Dutch, Turkish, and others. The exact list varies by iOS version—always check `supportsOnDeviceRecognition` at runtime.

---

## Advanced features for production apps

### Custom vocabulary (iOS 10+) and language models (iOS 17+)

Basic custom vocabulary uses `contextualStrings`:

```swift
request.contextualStrings = ["Kubernetes", "PostgreSQL", "GraphQL"]  // Max ~100 phrases
```

For iOS 17+, `SFCustomLanguageModelData` provides robust customization:

```swift
@available(iOS 17.0, *)
func prepareCustomLanguageModel() async throws {
    let customData = SFCustomLanguageModelData(locale: .init(identifier: "en-US")) {
        PhraseCount(phrase: "kubectl apply", count: 50)
        PhraseCount(phrase: "docker compose", count: 50)
        // Custom pronunciations via X-SAMPA for technical terms
    }
    
    // Prepare model (CPU-intensive—do off main thread)
    let dataURL = FileManager.default.temporaryDirectory.appendingPathComponent("training.bin")
    let modelURL = FileManager.default.temporaryDirectory.appendingPathComponent("custom.model")
    
    try customData.write(to: dataURL)
    try await SFSpeechLanguageModel.prepareCustomLanguageModel(
        for: dataURL,
        clientIdentifier: "com.yourapp.speechmodel",
        configuration: SFSpeechLanguageModel.Configuration()
    )
}
```

### Automatic punctuation (iOS 16+)

```swift
if #available(iOS 16, *) {
    request.addsPunctuation = true  // Adds periods, commas, question marks
}
```

Effectiveness varies by language—most reliable in English. Users can also speak punctuation commands ("comma", "period", "new line").

### Task hints for context optimization

```swift
request.taskHint = .dictation     // Long-form text entry
// or .search                     // Short search queries  
// or .confirmation               // Yes/no responses
```

---

## Comprehensive error handling

```swift
class RobustSpeechManager {
    private var retryCount = 0
    private let maxRetries = 3
    
    func handleError(_ error: Error) {
        let nsError = error as NSError
        
        switch (nsError.domain, nsError.code) {
        case ("kAFAssistantErrorDomain", 203):
            // Transient error—retry with backoff
            retryWithBackoff()
            
        case ("kAFAssistantErrorDomain", 209):
            // Recognition failed—check audio input
            validateAudioInputAndRetry()
            
        case ("kAFAssistantErrorDomain", 216):
            // Concurrent request conflict
            cancelAllTasksAndRestart()
            
        case ("kAFAssistantErrorDomain", 1101), ("kAFAssistantErrorDomain", 1107):
            // System service issues—retry later
            scheduleDelayedRetry(delay: 5.0)
            
        case ("SiriSpeechErrorDomain", _):
            // Rate limit exceeded
            handleQuotaExceeded()
            
        default:
            // Fallback: attempt on-device if available
            attemptOnDeviceFallback()
        }
    }
    
    private func retryWithBackoff() {
        guard retryCount < maxRetries else {
            notifyUserOfPersistentFailure()
            return
        }
        
        retryCount += 1
        let delay = pow(2.0, Double(retryCount))
        
        DispatchQueue.main.asyncAfter(deadline: .now() + delay) { [weak self] in
            self?.restartRecognition()
        }
    }
}
```

---

## Privacy and enterprise compliance

### HIPAA/GDPR considerations

For healthcare or privacy-regulated applications:

```swift
// Enforce on-device only—no data transmission
if #available(iOS 13, *) {
    guard speechRecognizer.supportsOnDeviceRecognition else {
        // Fail gracefully—don't fall back to server
        throw PrivacyComplianceError.onDeviceRequired
    }
    request.requiresOnDeviceRecognition = true
}
```

**Compliance checklist**:
- ✅ Set `requiresOnDeviceRecognition = true` (iOS 13+)
- ✅ Implement transcript deletion for right-to-erasure requests
- ✅ Document data handling in privacy policy
- ✅ iOS encrypts data at rest when device is locked
- ⚠️ Apple's Speech framework has no specific HIPAA certification—consult legal counsel

### What Apple collects (server-based only)

When using server-based recognition: transcripts, device specifications, approximate location, performance metrics. Data associated with rotating device identifier (not Apple ID). Retained up to **2 years** for service improvement. Users can delete via Settings > Siri & Search > Siri & Dictation History.

---

## Performance optimization for production

### Battery impact mitigation

1. **Prefer on-device recognition** when privacy requirements allow
2. **Implement voice activity detection** to avoid continuous processing
3. **Set `shouldReportPartialResults = false`** if real-time feedback unnecessary
4. **Remove audio taps promptly** when recognition completes:

```swift
func cleanup() {
    audioEngine.stop()
    audioEngine.inputNode.removeTap(onBus: 0)  // Critical for memory
    recognitionRequest?.endAudio()
    try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
}
```

### Memory management

- Use `[weak self]` in all completion handlers
- Cancel tasks explicitly before creating new ones
- Remove input node taps after stopping audio engine
- Set request/task references to `nil` after completion

---

## iOS version compatibility matrix

| Feature | Minimum iOS | Notes |
|---------|-------------|-------|
| Speech framework (core) | iOS 10 | Basic server-based recognition |
| On-device recognition | iOS 13 | A9+ processor required |
| `supportsOnDeviceRecognition` | iOS 13 | Check before requiring |
| SFVoiceAnalytics | iOS 13 | Pitch, jitter, shimmer analysis |
| SFSpeechRecognitionMetadata | iOS 14 | Speaking rate, pause duration |
| `addsPunctuation` | iOS 16 | Automatic punctuation |
| SFCustomLanguageModelData | iOS 17 | Custom vocabulary with pronunciations |
| SpeechAnalyzer (new API) | iOS 26 | Offline-first, modular architecture |

---

## Accessibility best practices

```swift
// Provide clear accessibility labels
recordButton.accessibilityLabel = "Start recording"
recordButton.accessibilityHint = "Double tap to begin speech recognition"

// Announce state changes
UIAccessibility.post(notification: .announcement, argument: "Recording started")

// Update transcript accessibility
transcriptLabel.accessibilityValue = currentTranscript
UIAccessibility.post(notification: .layoutChanged, argument: transcriptLabel)
```

Ensure visual feedback accompanies audio recording states for users with hearing impairments.

---

## Configuration checklist

**Before coding**:
- [ ] Add `NSSpeechRecognitionUsageDescription` to Info.plist
- [ ] Add `NSMicrophoneUsageDescription` to Info.plist
- [ ] Set deployment target (iOS 13+ recommended for on-device)
- [ ] Import Speech and AVFoundation frameworks

**Runtime setup**:
- [ ] Request authorization with `SFSpeechRecognizer.requestAuthorization()`
- [ ] Handle all authorization states including `.denied` and `.restricted`
- [ ] Configure AVAudioSession with `.record` category, `.measurement` mode
- [ ] Register for audio interruption notifications
- [ ] Check `isAvailable` and `supportsOnDeviceRecognition` before recognition

**Cleanup**:
- [ ] Cancel recognition task
- [ ] Stop audio engine
- [ ] Remove tap on input node (after stopping engine)
- [ ] End audio on request
- [ ] Deactivate audio session with `.notifyOthersOnDeactivation`

---

## Conclusion

Apple's Speech framework provides **robust, production-ready speech recognition** with clear trade-offs between server-based accuracy and on-device privacy. For most production applications, **targeting iOS 13+ with on-device recognition** offers the best balance of privacy, unlimited duration, and no rate limits. iOS 17's custom language model support addresses the historic weakness in domain-specific vocabulary.

Key technical decisions:
- **Privacy-critical apps**: Require on-device recognition exclusively
- **Maximum accuracy**: Use server-based with custom vocabulary hints
- **Long-form transcription**: On-device recognition eliminates the 1-minute limit
- **Enterprise/healthcare**: On-device only with explicit compliance documentation

The upcoming iOS 26 `SpeechAnalyzer` API signals Apple's continued investment in offline-first speech recognition, with promised improvements matching mid-tier Whisper model performance while maintaining full privacy.