# Apple Intelligence developer capabilities: A complete technical reference

The most significant development for iOS and watchOS developers is Apple's announcement of the **Foundation Models framework** in iOS 26, which provides free, direct access to Apple's on-device 3-billion parameter language model—a dramatic shift from the limited integration points in iOS 18.1. For offline-first development, particularly on Apple Watch, developers should understand that while Core ML, Natural Language, and Sound Analysis frameworks work fully offline on watchOS, the **Vision and Speech frameworks are entirely unavailable** on the watch platform. Apple Intelligence features require an A17 Pro or M1+ chip with 8GB RAM, meaning only iPhone 15 Pro and newer support these capabilities.

The practical implication for app development strategy is clear: traditional ML frameworks (Core ML, Vision, Natural Language) offer robust, fully offline capabilities across most devices, while Apple Intelligence APIs require the latest hardware and operate on a hybrid on-device/cloud model. Developers targeting Apple Watch must design around significant framework gaps by either pre-processing data on iPhone or using Core ML directly without Vision framework wrappers.

## Core ML powers on-device inference across all Apple platforms

Core ML remains the foundational framework for deploying machine learning models on Apple devices, supporting neural networks, tree ensembles, SVMs, and pipeline models. The framework runs entirely on-device with **zero cloud dependency**, automatically leveraging CPU, GPU, and Neural Engine based on workload and device capabilities.

The modern **MLPackage format** (replacing legacy .mlmodel) is required for ML Programs and stateful models introduced in iOS 18. Key classes include `MLModel` for inference, `MLModelConfiguration` for compute unit selection, and the new `MLTensor` type in iOS 18 for NumPy-style tensor operations. Developers can specify compute units via `MLComputeUnits` options: `.all` (recommended default), `.cpuOnly`, `.cpuAndGPU`, or `.cpuAndNeuralEngine` (iOS 16+).

Neural Engine performance varies significantly by chip generation. The **A17 Pro delivers 35 TOPS** compared to 17 TOPS on A16, while the S9/S10 chips in Apple Watch Series 9+ feature a 4-core Neural Engine that's twice as fast as the S8. Memory constraints matter critically for model deployment: iPhone Pro models with 8GB RAM can run larger models, while older 4GB devices require aggressive quantization and ANE-only execution for models like Stable Diffusion.

| Chip | Device | Neural Engine Cores | Performance (TOPS) |
|------|--------|--------------------|--------------------|
| A17 Pro | iPhone 15 Pro | 16 | 35 |
| A18 | iPhone 16 | 16 | 38+ |
| M4 | iPad Pro 2024 | 16 | 38 |
| S9/S10 | Watch Series 9+ | 4 | ~2x faster than S8 |

Model optimization through **coremltools 8** supports weight palettization (1-8 bit), linear quantization (INT4/INT8), and pruning. For LLMs, 4-bit block quantization with stateful KV-cache (iOS 18+) enables running models like Llama 3.1 8B at ~33 tokens/second on M1 Max. Create ML enables custom model training on Mac with deployment across all platforms, supporting image classification, object detection, activity classification, sound classification, and text classification tasks.

## Foundation Models framework transforms developer access in iOS 26

The **Foundation Models framework**, announced at WWDC 2025, represents Apple's most significant AI developer offering. It provides direct, programmatic access to Apple's on-device language model without requiring the user to interact with system UI—and critically, at **no cost per request**.

The framework centers on `SystemLanguageModel` and `LanguageModelSession` classes. Basic usage is straightforward: create a session, call `respond(to:)` with a prompt, and receive generated text. The model excels at summarization, entity extraction, classification, and short dialog rather than world knowledge or complex reasoning tasks.

```swift
import FoundationModels
let session = LanguageModelSession()
let response = try await session.respond(to: "Summarize: \(text)")
```

Structured output generation uses the `@Generable` macro to define Swift types that the model populates directly, combined with `@Guide` for output constraints. The framework supports streaming responses for real-time UI updates and tool calling for model-invoked app functions. Most importantly for offline development, **Foundation Models operates entirely on-device by default** with no Private Cloud Compute fallback unless explicitly configured with `.automatic` mode.

The framework requires Apple Intelligence-compatible devices (A17 Pro/M1+) and iOS 26, iPadOS 26, macOS 26, or visionOS 26. It explicitly **excludes watchOS**, meaning developers cannot access the language model directly on Apple Watch.

## Writing Tools and Image Playground integrate automatically

Writing Tools provide system-wide text rewriting, proofreading, and summarization capabilities that integrate automatically into standard text views. Any `UITextView`, `NSTextView`, or SwiftUI `TextEditor` gains Writing Tools support without code changes, though developers can configure behavior via the `writingToolsBehavior` property (`.complete`, `.limited`, or `.none`).

TextKit 2 is required for the full inline replacement experience; TextKit 1 apps fall back to limited mode showing results in a popover. Delegate methods (`textViewWritingToolsWillBegin`, `textViewWritingToolsDidEnd`) enable apps to respond to user interactions. Note that **no programmatic API exists** to invoke Writing Tools without user interaction until the Foundation Models framework in iOS 26.

Image Playground exposes image generation through `ImagePlaygroundViewController` (UIKit) or the `.imagePlaygroundSheet` modifier (SwiftUI). Developers provide concepts via `.text()` or `.extracted(from:title:)` types and receive a URL to the generated image. The framework supports Animation, Illustration, and Sketch styles. Device availability checking uses `ImagePlaygroundViewController.isAvailable`. iOS 26 adds `ImageCreator` for programmatic generation without presenting UI.

**Genmoji cannot be programmatically generated** by third-party apps. However, apps can display and store Genmoji received through user input using `NSAdaptiveImageGlyph`, which requires TextKit 2 and `supportsAdaptiveImageGlyph = true` on text views.

## Vision and Natural Language frameworks deliver full offline capability

The Vision framework provides comprehensive computer vision capabilities that run **entirely on-device** across iOS 11+. All `VNRequest` subclasses process locally without network requirements, making them ideal for offline-first app architecture.

Face detection (`VNDetectFaceRectanglesRequest`) and 76-point landmark analysis (`VNDetectFaceLandmarksRequest`) work from iOS 11+. Text recognition (`VNRecognizeTextRequest`) supports 18+ languages with `.accurate` and `.fast` modes, with automatic language detection added in iOS 16. Body pose estimation provides **19 2D joints** (iOS 14+) or **17 3D joints** (iOS 17+), while hand pose detection tracks 21 points per hand with left/right chirality identification.

Person segmentation (`VNGeneratePersonSegmentationRequest`) generates pixel-buffer masks with quality levels from `.fast` to `.accurate`, with instance masks supporting up to 4 individuals in iOS 17+. Document-focused features include rectangle detection, barcode/QR recognition across 12+ symbologies, and document boundary segmentation.

The Natural Language framework (iOS 12+, watchOS 6+) handles all NLP tasks on-device:

- **NLTokenizer**: Word, sentence, paragraph segmentation
- **NLTagger**: Part-of-speech tagging, named entity recognition (person, place, organization), lemmatization, sentiment analysis
- **NLLanguageRecognizer**: 50+ language identification with probability hypotheses
- **NLEmbedding**: Word vectors for semantic similarity (7 languages)
- **NLContextualEmbedding** (iOS 17+): BERT-based transformer embeddings with 512-dimension context-aware vectors

Speech recognition through `SFSpeechRecognizer` supports **on-device processing for ~22 languages** when `requiresOnDeviceRecognition = true` (iOS 13+, A9+). On-device mode removes duration limits and daily request quotas while ensuring complete privacy. AVSpeechSynthesizer provides text-to-speech with 150+ voices across 50+ languages, all processing locally, including Personal Voice (iOS 17+) for user-created AI voices.

## watchOS imposes critical framework limitations for ML apps

Apple Watch development requires understanding significant framework gaps compared to iOS. **Vision framework is entirely unavailable** on watchOS—no `VNImageRequestHandler`, no image analysis requests. Similarly, **SFSpeechRecognizer is not available**, and the new SpeechAnalyzer API in iOS 26 explicitly excludes watchOS.

Core ML works fully on watchOS 4+ with Neural Engine support starting from Series 4 (S4 chip). The Series 9, 10, and Ultra 2/3 feature a **4-core Neural Engine** delivering 2x faster ML processing than the S8. However, models must be pre-compiled—`MLModel.compileModel(at:)` is not available on watchOS.

Available watchOS frameworks for ML development include:
- **Core ML**: Full inference, all model types
- **Natural Language**: NLTagger, NLTokenizer, NLEmbedding (watchOS 6+)
- **SoundAnalysis**: Audio classification
- **Core Motion**: Accelerometer/gyroscope at up to 100Hz for activity classification
- **HealthKit**: Health data access for ML analysis

For image and speech processing, the workaround is **WatchConnectivity** to transfer data to the paired iPhone for analysis, then return results to the watch. Model size constraints recommend keeping watchOS models under 50-100MB with aggressive quantization due to limited RAM (1-2GB depending on model).

Apple Intelligence features on watchOS are **limited and require a paired iPhone nearby**. Smart Replies, notification prioritization, and the new Workout Buddy feature (watchOS 26) all depend on the connected iPhone's Apple Intelligence capabilities. Standalone Apple Intelligence processing is not available on any Apple Watch model.

| Framework | watchOS Availability | Offline Capable |
|-----------|---------------------|-----------------|
| Core ML | ✅ watchOS 4+ | ✅ Full |
| Natural Language | ✅ watchOS 6+ | ✅ Full |
| SoundAnalysis | ✅ Available | ✅ Full |
| Vision | ❌ Not available | N/A |
| SFSpeechRecognizer | ❌ Not available | N/A |
| Foundation Models | ❌ Not available | N/A |

## Offline capabilities matrix for development planning

Apple's ML infrastructure operates on three tiers: fully on-device (traditional frameworks), hybrid on-device/PCC (Apple Intelligence), and cloud-required (ChatGPT integration). Understanding this architecture is essential for offline-first design.

**Fully offline frameworks** include Core ML inference, all Vision framework requests, Natural Language processing, on-device speech recognition (select languages), AVSpeechSynthesizer, VisionKit document scanning, DataScannerViewController, and Foundation Models framework operations (iOS 26+). These work without any network connectivity on supported devices.

**Hybrid Apple Intelligence features** use on-device models for basic tasks but escalate to Private Cloud Compute for complex requests. Writing Tools handle basic proofreading and short rewrites locally but send longer text to PCC. Image Playground generates simple prompts on-device while complex scenes require cloud processing. Notification summarization runs on-device. The system automatically manages this escalation transparently.

Private Cloud Compute provides privacy guarantees distinct from traditional cloud: custom Apple Silicon servers with hardened OS, **zero data retention**, end-to-end encryption, no logging, cryptographic attestation, and publicly auditable software. Users can view PCC requests in Settings → Privacy & Security → Apple Intelligence Report.

| Capability | Offline Status | Device Requirement | Notes |
|------------|---------------|-------------------|-------|
| Core ML inference | ✅ Full | Any supported | All processing local |
| Vision requests | ✅ Full | iOS 11+ | No cloud calls |
| Natural Language | ✅ Full | iOS 12+ | All NLP local |
| Speech recognition | ✅ Full* | A12+, iOS 13+ | *~22 languages only |
| Text-to-speech | ✅ Full | iOS 7+ | All voices local |
| Foundation Models | ✅ Full | A17 Pro/M1+, iOS 26 | On-device only |
| Writing Tools | ⚠️ Partial | A17 Pro/M1+, iOS 18 | Basic offline |
| Image Playground | ⚠️ Partial | A17 Pro/M1+, iOS 18.1 | Simple prompts offline |
| Siri (advanced) | ❌ Cloud | A17 Pro/M1+ | Requires PCC |
| ChatGPT integration | ❌ Cloud | A17 Pro/M1+ | Requires internet |

## First-party versus third-party API access gaps persist

Several Apple Intelligence capabilities remain exclusive to first-party apps. **Mail Smart Reply**, **notification prioritization algorithms**, **full Siri personal context**, **Photos Memory creation**, and **phone call recording/transcription** are not exposed to third-party developers through any API.

Third-party developers gain full access to: text summarization (via Foundation Models in iOS 26), Writing Tools (automatic in text views), Image Playground UI and programmatic generation (iOS 26), Genmoji display and storage (not creation), Siri actions through App Intents, Visual Intelligence integration as search providers, and automatic notification summarization for their apps.

The App Intents framework enables deep Siri integration through **Assistant Schemas**—predefined intent structures that Apple's models recognize. Developers conforming to these schemas gain natural language understanding for their app's actions without training custom models. Visual Intelligence on iPhone 16 allows third-party apps to register as search providers but doesn't expose the underlying computer vision capabilities to developers.

## Implementation recommendations by developer profile

**Indie developers** should prioritize Core ML and Vision frameworks for maximum device compatibility and fully offline operation. Create ML enables training custom models without ML expertise. For text intelligence, Natural Language framework covers most needs without Apple Intelligence hardware requirements. The Foundation Models framework (iOS 26+) opens powerful capabilities but limits audience to newest devices.

**Enterprise developers** must consider that Apple Intelligence data processed via PCC meets strong privacy guarantees but still leaves the device temporarily. For maximum compliance, restrict to Core ML/Vision/NLP frameworks which guarantee all processing remains local. MDM can control Apple Intelligence availability on managed devices. Document retention policies should account for Foundation Models framework outputs.

**Performance-conscious developers** should profile models using Xcode's Performance Reports and Core ML Instrument. Neural Engine provides best power efficiency; avoid forcing CPU-only execution on supported devices. For watchOS, aggressive model optimization (4-8 bit quantization, pruning) is essential given memory constraints. Use `MLComputeUnits.all` unless specific compute unit behavior is required.

**Accessibility-focused developers** benefit from system-level Apple Intelligence integration in standard UI controls. Personal Voice (iOS 17+) enables apps to speak with user-created voices via AVSpeechSynthesizer. VoiceOver gains enhanced descriptions from Apple Intelligence but these aren't developer-accessible. App Intents enable voice-driven app control for users with motor impairments.

## Conclusion

Apple's ML developer landscape has evolved from inference-only Core ML to comprehensive AI platform access with Foundation Models framework. The key strategic insight is **architectural bifurcation**: traditional frameworks (Core ML, Vision, Natural Language) offer universal, fully offline capabilities, while Apple Intelligence APIs provide powerful but hardware-restricted features with hybrid cloud architecture.

For Apple Watch development, the absence of Vision and Speech frameworks means image and voice processing must flow through the paired iPhone. Foundation Models framework exclusion from watchOS confirms the watch remains a sensor and notification platform rather than an AI processing device.

The Foundation Models framework in iOS 26 represents the most significant capability expansion, enabling developers to build custom AI features using Apple's on-device model at no cost. However, the A17 Pro/M1+ requirement limits immediate deployment. Developers should architect apps with graceful degradation: Core ML for broad compatibility, Foundation Models for enhanced experiences on supported hardware.