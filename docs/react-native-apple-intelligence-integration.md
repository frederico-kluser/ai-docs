# React Native meets Apple Intelligence: A complete integration guide

**The React Native ecosystem for Apple ML frameworks has matured significantly, though significant gaps remain.** The most important development is `@react-native-ai/apple`, which provides first-class support for Apple's Foundation Models (iOS 26+) on-device LLM, maintained by Callstack with ~1,450 weekly downloads. For camera-based ML, `react-native-vision-camera` dominates with **383,000 weekly downloads** and full New Architecture support. However, dedicated Core ML and Natural Language framework bridges are largely abandoned—most haven't been updated in 6+ years—requiring custom native modules for deep integration.

The practical reality: production apps needing Apple ML capabilities should plan for native module development using Expo Modules API or Turbo Modules, supplemented by actively maintained community packages where available. Cross-platform alternatives like `react-native-fast-tflite` offer compelling performance with CoreML delegates, providing a middle path between pure-Apple and fully cross-platform solutions.

---

## The library landscape is polarized between thriving and abandoned

React Native packages for Apple ML fall into two distinct categories: a handful of actively maintained, high-quality libraries, and a graveyard of abandoned packages from 2018-2019.

### Actively maintained packages worth using

| Package | Purpose | Weekly Downloads | New Architecture | Expo Compatible |
|---------|---------|------------------|------------------|-----------------|
| `react-native-vision-camera` | Camera + Frame Processors | 383,000 | ✅ | ✅ |
| `@react-native-ai/apple` | Foundation Models, Embeddings | 1,449 | ✅ Required | ✅ |
| `@react-native-voice/voice` | Speech Recognition | 20,131 | ⚠️ Limited | ✅ |
| `expo-speech-recognition` | Speech (Expo-native) | Active | ✅ | ✅ |
| `@react-native-ml-kit/*` | Face/Text/Barcode | Active | ✅ | ✅ |
| `react-native-fast-tflite` | TensorFlow Lite | Active | ✅ | ✅ |

The standout performer is **react-native-vision-camera** by Marc Rousavy (Margelo). It provides JSI-based frame processors that run ML inference synchronously in the camera pipeline, supporting 30-240 FPS with custom C++/GPU-accelerated processing. Plugin ecosystem includes text recognition, face detection, pose estimation, and barcode scanning—all leveraging Apple's Vision framework under the hood.

For **Apple Intelligence and Foundation Models** (iOS 26+), `@react-native-ai/apple` is the definitive choice. It integrates with Vercel's AI SDK v5, providing streaming responses, structured outputs via Zod schemas, tool calling, and **NLContextualEmbedding** for text embeddings (iOS 17+). Requirements include React Native 0.80+ with New Architecture enabled and an Apple Intelligence-capable device (iPhone 15 Pro or later, M1+ iPad/Mac).

### Abandoned packages to avoid

| Package | Last Update | Notes |
|---------|-------------|-------|
| `react-native-coreml` | 2018 (6 years) | 36 downloads/week, no New Architecture |
| `react-native-core-ml-image` | 2018 | Camera classification, abandoned |
| `react-native-vision` (rhdeck) | 2017 | Vision/CoreML wrapper, abandoned |
| `react-native-sfspeechrecognizer` | 2016 | Direct SFSpeechRecognizer bridge, abandoned |

**Critical gap**: No actively maintained package directly exposes Apple's **Natural Language framework** (NLTagger) for tokenization, lemmatization, named entity recognition, or part-of-speech tagging. The only NLP coverage comes through `@react-native-ai/apple`'s embedding support. Production apps needing these features must build custom native modules.

---

## Native module development requires choosing your architecture path

Building custom bridges to Apple ML frameworks demands understanding React Native's evolving module system. The choice between Turbo Modules and Expo Modules API significantly impacts development complexity and performance characteristics.

### Turbo Modules deliver maximum performance for ML workloads

Turbo Modules use JSI (JavaScript Interface) for direct communication between JavaScript and native code, eliminating the serialization overhead of the legacy bridge. For ML applications, this matters enormously: transferring an **8MB image payload** drops from ~666ms (base64 over bridge) to ~1ms (direct ArrayBuffer via JSI).

**Creating a Turbo Module for Core ML requires three components:**

First, a TypeScript specification defining the interface:
```typescript
// specs/NativeMLModule.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  classifyImage(imagePath: string): Promise<{
    label: string;
    confidence: number;
  }>;
  loadModel(modelPath: string): Promise<boolean>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeMLModule');
```

Second, the native implementation in Objective-C++ (Swift requires a thin ObjC wrapper):
```objc
// RCTNativeMLModule.mm
@implementation RCTNativeMLModule

- (void)classifyImage:(NSString *)imagePath
              resolve:(RCTPromiseResolveBlock)resolve
               reject:(RCTPromiseRejectBlock)reject {
  dispatch_async(dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0), ^{
    // Core ML inference on background thread
    VNCoreMLRequest *request = [[VNCoreMLRequest alloc] initWithModel:self.model];
    // ... perform inference
    dispatch_async(dispatch_get_main_queue(), ^{
      resolve(@{@"label": topResult.identifier, @"confidence": @(topResult.confidence)});
    });
  });
}

@end
```

Third, Codegen configuration in package.json for type-safe code generation at build time.

### Expo Modules API offers simpler Swift development

Expo Modules API provides a dramatically simpler path for teams comfortable with Expo's ecosystem. It supports **100% Swift** without bridging headers and generates JSI bindings automatically:

```swift
// ios/ExpoCoreMlModule.swift
import ExpoModulesCore
import CoreML
import Vision

public class ExpoCoreMlModule: Module {
  public func definition() -> ModuleDefinition {
    Name("ExpoCoreMl")
    
    AsyncFunction("classifyImage") { (imagePath: String) -> [String: Any] in
      return try await self.runClassification(imagePath: imagePath)
    }
    
    Events("onInferenceProgress")
  }
  
  private func runClassification(imagePath: String) async throws -> [String: Any] {
    guard let modelURL = Bundle.main.url(forResource: "MyModel", withExtension: "mlmodelc"),
          let model = try? VNCoreMLModel(for: MLModel(contentsOf: modelURL)) else {
      throw Exception(name: "MODEL_ERROR", description: "Failed to load model")
    }
    // Vision framework inference...
    return ["label": "cat", "confidence": 0.95]
  }
}
```

Create the module scaffold with `npx create-expo-module@latest --local`, which generates the complete iOS/Android structure in a `modules/` directory.

**Performance is equivalent**: Both Turbo Modules and Expo Modules execute hundreds of thousands of native calls per second via JSI. Choose Expo Modules for simpler development; choose Turbo Modules for C++ interop or maximum control.

---

## Framework-by-framework integration approaches

Each Apple ML framework presents distinct integration challenges and available solutions in the React Native ecosystem.

### Core ML requires native modules for production use

All dedicated Core ML packages (`react-native-coreml`, `react-native-core-ml-image`) are abandoned. Production integration requires custom native modules. The workflow:

1. **Bundle compiled models**: Place `.mlmodelc` files (not `.mlmodel`) in iOS bundle resources via Xcode or config plugin
2. **Load lazily**: Models can be 50MB-2GB+; load on demand, not at startup
3. **Configure compute units**: Enable Neural Engine via `config.computeUnits = .all`
4. **Process on background threads**: Use `DispatchQueue.global(qos: .userInitiated)` to avoid UI blocking

**Alternative approach**: Use `react-native-fast-tflite` with CoreML delegate for cross-platform model deployment:
```javascript
const model = await loadTensorflowModel(require('model.tflite'), 'core-ml');
const result = await model.run(inputTensor);
```

This leverages Apple's Neural Engine through TensorFlow Lite's CoreML delegate, achieving **3-5x speedup** over CPU-only inference while maintaining Android compatibility.

### Vision framework shines through VisionCamera

`react-native-vision-camera` provides the cleanest Vision framework integration. Frame processors run as JSI worklets, enabling real-time inference:

```javascript
const frameProcessor = useFrameProcessor((frame) => {
  'worklet';
  const faces = detectFaces(frame);  // Vision framework under the hood
  const texts = recognizeText(frame); // VNRecognizeTextRequest
  runOnJS(updateResults)({ faces, texts });
}, []);

return <Camera frameProcessor={frameProcessor} device={device} isActive={true} />;
```

Available frame processor plugins cover most Vision framework capabilities:
- **Text recognition**: `react-native-vision-camera-text-recognition`, `@bear-block/vision-camera-ocr`
- **Face detection**: Custom plugins or ML Kit integration
- **Pose estimation**: `@scottjgilroy/react-native-vision-camera-v4-pose-detection`
- **Barcode scanning**: Built into VisionCamera

Creating custom frame processor plugins enables direct VNRequest access for any Vision capability not covered by existing plugins.

### Natural Language framework access is limited

The ecosystem gap here is significant. `@react-native-ai/apple` provides **NLContextualEmbedding** for text embeddings (512-dimensional BERT-based vectors, iOS 17+), but full NLTagger access—tokenization, lemmatization, named entity recognition, sentiment analysis—requires custom native modules.

For cross-platform NLP, consider `node-nlp-rn`, a pure JavaScript implementation supporting 40 languages with offline capability. It handles intent classification, named entity recognition, and sentiment analysis without native dependencies.

### Speech recognition has solid coverage

`@react-native-voice/voice` remains the most widely used option (20K downloads/week) despite limited recent updates. It wraps iOS SFSpeechRecognizer with a straightforward API:

```javascript
import Voice from '@react-native-voice/voice';

Voice.onSpeechResults = (e) => setTranscript(e.value[0]);
await Voice.start('en-US');
```

**Expo users** should prefer `expo-speech-recognition` (by @jamsch), which provides Expo-native integration with additional features: audio file transcription, volume metering, and explicit on-device recognition control.

**iOS 26 introduces SpeechAnalyzer**, accessible through `@react-native-ai/apple`, offering improved on-device transcription with system-managed language models.

### Foundation Models open new possibilities on iOS 26

Apple's on-device LLM (~3B parameters) becomes available through Foundation Models framework. `@react-native-ai/apple` provides complete access:

```javascript
import { apple } from '@react-native-ai/apple';
import { generateText, streamText } from 'ai';

// Simple generation
const { text } = await generateText({
  model: apple(),
  prompt: 'Explain quantum entanglement simply'
});

// Streaming
const stream = await streamText({ model: apple(), prompt: 'Write a haiku' });
for await (const chunk of stream) {
  appendToUI(chunk);
}
```

**Structured outputs** work via Zod schemas, enabling type-safe JSON generation. **Tool calling** allows the LLM to invoke JavaScript functions you define. Always check availability first—Foundation Models requires Apple Intelligence-enabled devices:

```javascript
const { status, reasonCode } = await getTextModelAvailability();
if (status !== 'available') {
  // Handle: deviceNotEligible, appleIntelligenceNotEnabled, modelNotReady
}
```

---

## Architecture decisions determine ML app performance

Threading, memory management, and data transfer patterns critically impact React Native ML application performance.

### Threading must keep UI responsive

React Native operates across multiple threads: UI (native rendering), JavaScript (JS execution), Native Modules (native code), and Shadow (layout). ML inference belongs on **background threads only**:

```swift
// ✅ Correct: Background processing with main thread callback
@objc func runInference(_ data: String,
                        resolver resolve: @escaping RCTPromiseResolveBlock,
                        rejecter reject: @escaping RCTPromiseRejectBlock) {
  DispatchQueue.global(qos: .userInitiated).async {
    let result = self.heavyMLOperation(data)
    DispatchQueue.main.async {
      resolve(result)
    }
  }
}
```

For VisionCamera frame processors, use `runAsync()` for heavy ML operations to avoid blocking the camera pipeline:

```javascript
const frameProcessor = useFrameProcessor((frame) => {
  'worklet';
  runAsync(frame, () => {
    'worklet';
    const result = heavyInference(frame); // Won't block camera
  });
}, []);
```

### Memory requires active management with large models

ML models consume significant memory—Core ML models range from 50MB to 2GB+. Best practices:

- **Lazy loading**: Load models only when needed, not at app startup
- **Explicit unloading**: Set model references to `nil` when inactive
- **Increased Memory capability**: Enable in Xcode for large model support
- **Cache compiled models**: Avoid recompilation by storing `.mlmodelc` in documents directory

### Data transfer patterns impact latency dramatically

The method of passing image/tensor data between JavaScript and native code creates the largest performance differential:

| Method | 8MB Payload Latency | Use Case |
|--------|---------------------|----------|
| File path reference | ~1ms | Large images, video frames |
| ArrayBuffer via JSI | ~1ms | Tensor data, processed frames |
| Base64 string | ~666ms | Legacy compatibility only |

**Always prefer file paths** for image data—let native code load from disk directly rather than transferring pixels through JavaScript.

---

## Expo requires development builds for ML features

Expo Go cannot execute custom native code, making it incompatible with any direct Apple ML framework access. However, **Expo Development Builds** provide full native capability while maintaining Expo's developer experience advantages.

### What works in Expo Go versus Development Builds

| Feature | Expo Go | Development Build |
|---------|---------|-------------------|
| expo-speech (TTS) | ✅ | ✅ |
| expo-camera (basic) | ✅ | ✅ |
| Core ML inference | ❌ | ✅ |
| Vision framework | ❌ | ✅ |
| Speech recognition | ❌ | ✅ |
| Foundation Models | ❌ | ✅ |
| VisionCamera frame processors | ❌ | ✅ |

### Config plugins enable native configuration

For ML apps, `expo-build-properties` is essential for setting deployment targets:

```json
{
  "expo": {
    "plugins": [
      ["expo-build-properties", {
        "ios": {
          "deploymentTarget": "17.0"
        }
      }]
    ]
  }
}
```

Custom config plugins can add Core ML models to bundle resources:

```javascript
const { withXcodeProject } = require('@expo/config-plugins');

module.exports = function withCoreMLModel(config, { modelPath }) {
  return withXcodeProject(config, async (config) => {
    config.modResults.addResourceFile(modelPath);
    return config;
  });
};
```

Build via EAS: `eas build --profile development --platform ios`

---

## Third-party alternatives offer cross-platform trade-offs

Cross-platform ML solutions provide Android compatibility at the cost of Apple-specific optimizations.

### react-native-fast-tflite delivers strong iOS performance

The best cross-platform option for custom models. Version 1.6.1 (April 2025) provides:
- **JSI-powered** inference with zero-copy memory access
- **CoreML delegate** for Neural Engine acceleration on iOS
- **GPU/NNAPI delegates** for Android acceleration
- **VisionCamera integration** for real-time camera inference

Performance with CoreML delegate approaches native Core ML—benchmarks show MobileNet V2 inference at **~6ms on iPhone 11 Pro** with CoreML delegate versus ~8ms for native Core ML (difference largely in delegate initialization overhead).

### ONNX Runtime provides universal model format

`onnxruntime-react-native` (v1.23.2, Microsoft) offers a single model format deployable across platforms:
- Convert from PyTorch, TensorFlow, or Core ML
- CoreML backend available for iOS
- ~2,073 weekly downloads

### MediaPipe covers common vision tasks

For pre-built pose detection, face mesh, and hand tracking, MediaPipe packages provide ready-to-use implementations:
- `@thinksys/react-native-mediapipe`: 33 BlazePose landmarks, camera integration
- `react-native-mediapipe-posedetection`: New Architecture only, world coordinates

These match Apple Vision framework capabilities for common use cases without custom model training.

---

## Recommendations by use case

### Building an iOS-only app with maximum ML performance
Use custom Expo Modules or Turbo Modules wrapping Core ML and Vision frameworks directly. Leverage Neural Engine through `MLModelConfiguration.computeUnits = .all`. Consider `@react-native-ai/apple` for Foundation Models (iOS 26+) and embeddings (iOS 17+).

### Building a cross-platform app with ML features
Start with `react-native-fast-tflite` for custom models—CoreML delegate provides near-native iOS performance while maintaining Android compatibility. Use `@react-native-ml-kit/*` for pre-built features (face detection, text recognition, barcode scanning). Use VisionCamera with frame processors for real-time camera ML.

### Adding on-device LLM capabilities (iOS 26+)
`@react-native-ai/apple` is the definitive choice. Requires New Architecture, Apple Intelligence-enabled device. Implement comprehensive fallback logic for unsupported devices—cloud API fallback or cached responses.

### Quick prototyping with Expo
Use Expo Development Builds, not Expo Go. Create local Expo modules for Apple ML integration. Leverage `expo-speech` (TTS), `expo-camera` (basic detection), and community packages like `expo-speech-recognition`. Build with EAS for seamless native compilation.

### Real-time camera-based ML
`react-native-vision-camera` is mandatory. Use frame processor plugins for text recognition, face detection, or create custom plugins for specific Vision framework capabilities. Enable New Architecture for optimal JSI performance. Target 30 FPS for most ML workloads; use `runAsync()` for inference exceeding 16ms.

---

## Conclusion

The React Native ecosystem for Apple ML frameworks has crystallized around a few essential packages: **react-native-vision-camera** for camera-based ML, **@react-native-ai/apple** for Foundation Models and embeddings, and **react-native-fast-tflite** for cross-platform model deployment. The abandoned state of dedicated Core ML packages means production apps requiring deep Apple ML integration must invest in custom native module development—Expo Modules API significantly reduces this burden with pure Swift support.

Foundation Models integration represents the most exciting development, bringing on-device LLM capabilities to React Native apps for the first time. The requirement for iOS 26+ and Apple Intelligence-enabled devices limits immediate adoption, but establishes the foundation for sophisticated AI features without cloud dependencies.

Teams should embrace the New Architecture—it's required for Foundation Models and dramatically improves ML data transfer performance. The JSI-based approach eliminates serialization overhead that historically made React Native challenging for real-time ML applications. Combined with VisionCamera's frame processors, React Native now supports production-grade computer vision applications with performance approaching native implementations.