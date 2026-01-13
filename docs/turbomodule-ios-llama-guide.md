# TurboModule iOS Nativo para llama.cpp: Guia Completo

**React Native New Architecture + Swift + llama.cpp**

O llama.rn parou de funcionar no iOS 26, mas seu código Swift/llama.cpp nativo ainda funciona. Este tutorial completo ensina como criar um **TurboModule nativo** que conecta Swift ao React Native, permitindo que você use llama.cpp diretamente no seu app.

## Visão geral da arquitetura

A Nova Arquitetura do React Native usa **TurboModules** com JSI (JavaScript Interface) para comunicação síncrona entre JavaScript e código nativo. Porém, TurboModules são escritos em **Objective-C++**, não Swift diretamente.

A solução é uma arquitetura em camadas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    JavaScript/TypeScript                        │
│                   (NativeLlama.ts - API)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Codegen Spec (NativeLlamaSpec.ts)                 │
│           Define tipos, métodos e eventos                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           Objective-C++ TurboModule (RCTNativeLlama.mm)        │
│         Wrapper fino que chama a camada Swift                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Swift Manager (LlamaManager.swift)                │
│           Lógica de negócio e gerenciamento de estado          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         Objective-C++ Wrapper (LlamaContextWrapper.mm)         │
│            Expõe a API C++ para Swift                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   llama.xcframework (C++)                      │
│              Biblioteca llama.cpp compilada                    │
└─────────────────────────────────────────────────────────────────┘
```

Swift não pode chamar C++ diretamente em TurboModules porque React Native usa Objective-C++ como camada de interface. A solução é o **padrão Adapter**: Objective-C++ serve como ponte entre Swift e C++.

---

## Parte 1: Estrutura do projeto

Crie a seguinte estrutura de diretórios no seu projeto React Native:

```
MeuApp/
├── src/
│   └── specs/
│       └── NativeLlamaSpec.ts          # Codegen spec
│   └── modules/
│       └── llama/
│           └── index.ts                # API JavaScript/TypeScript
├── ios/
│   ├── MeuApp/
│   │   ├── MeuApp-Bridging-Header.h    # Header para Swift usar ObjC
│   │   └── AppDelegate.mm              # Já existe
│   ├── LlamaModule/
│   │   ├── RCTNativeLlama.h            # Header do TurboModule
│   │   ├── RCTNativeLlama.mm           # Implementação TurboModule
│   │   ├── LlamaManager.swift          # Gerenciador Swift
│   │   ├── LlamaContextWrapper.h       # Header público (sem C++)
│   │   ├── LlamaContextWrapperPrivate.h # Header privado (com C++)
│   │   └── LlamaContextWrapper.mm      # Wrapper ObjC++ para llama.cpp
│   └── Frameworks/
│       └── llama.xcframework/          # Framework compilado
├── package.json                         # Com codegenConfig
└── react-native.config.js               # Configuração do módulo
```

---

## Parte 2: Codegen Spec (TypeScript)

O Codegen gera código nativo a partir de especificações TypeScript. O arquivo deve ter prefixo `Native`.

**Arquivo: `src/specs/NativeLlamaSpec.ts`**

```typescript
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

// Tipos para configuração do modelo
export type ModelConfig = Readonly<{
  contextLength: number;
  gpuLayers: number;
  seed: number;
  useMlock: boolean;
}>;

// Tipos para configuração de geração
export type GenerationConfig = Readonly<{
  maxTokens: number;
  temperature: number;
  topP: number;
  topK: number;
  repeatPenalty: number;
  stopSequences: ReadonlyArray<string>;
}>;

// Payload do evento de token
export type TokenPayload = Readonly<{
  token: string;
  tokenId: number;
  isComplete: boolean;
  tokensGenerated: number;
}>;

// Especificação do módulo
export interface Spec extends TurboModule {
  // Carrega um modelo GGUF
  loadModel(path: string, config: ModelConfig): Promise<boolean>;
  
  // Gera texto (não-streaming)
  generateText(prompt: string, config: GenerationConfig): Promise<string>;
  
  // Inicia geração com streaming
  startStreaming(prompt: string, config: GenerationConfig): void;
  
  // Para a geração em andamento
  stopStreaming(): void;
  
  // Descarrega o modelo da memória
  unloadModel(): Promise<void>;
  
  // Verifica se há modelo carregado
  isModelLoaded(): boolean;
  
  // Obtém informações do modelo
  getModelInfo(): Promise<string>;
  
  // Métodos para eventos (requerido para NativeEventEmitter legado)
  addListener(eventName: string): void;
  removeListeners(count: number): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeLlama');
```

**Configure o Codegen no `package.json`:**

```json
{
  "name": "meuapp",
  "version": "1.0.0",
  "codegenConfig": {
    "name": "NativeLlamaSpec",
    "type": "modules",
    "jsSrcsDir": "src/specs",
    "ios": {
      "modulesConformingToProtocol": {
        "RCTTurboModule": ["NativeLlama"]
      }
    },
    "android": {
      "javaPackageName": "com.meuapp.llama"
    }
  }
}
```

---

## Parte 3: Implementação nativa

### 3.1 Bridging Header para Swift

**Arquivo: `ios/MeuApp/MeuApp-Bridging-Header.h`**

```objc
//
//  MeuApp-Bridging-Header.h
//  Expõe headers Objective-C para Swift
//

#ifndef MeuApp_Bridging_Header_h
#define MeuApp_Bridging_Header_h

// React Native (se necessário)
#import <React/RCTBridgeModule.h>

// Wrapper do llama.cpp (header público sem C++)
#import "LlamaContextWrapper.h"

#endif /* MeuApp_Bridging_Header_h */
```

Configure no Xcode: **Build Settings** → **Swift Compiler - General** → **Objective-C Bridging Header**: `$(SRCROOT)/MeuApp/MeuApp-Bridging-Header.h`

### 3.2 Wrapper Objective-C++ para llama.cpp

O wrapper expõe a API C++ para Swift usando headers separados (público e privado).

**Arquivo: `ios/LlamaModule/LlamaContextWrapper.h`** (Header público - SEM tipos C++)

```objc
//
//  LlamaContextWrapper.h
//  Header público que Swift pode importar
//  NÃO inclua headers C++ aqui!
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

// Callback para streaming de tokens
typedef void (^LlamaTokenCallback)(NSString *token, NSInteger tokenId, BOOL isComplete, NSInteger tokensGenerated);

@interface LlamaContextWrapper : NSObject

// Inicialização
- (nullable instancetype)initWithModelPath:(NSString *)modelPath
                             contextLength:(int)contextLength
                                 gpuLayers:(int)gpuLayers
                                      seed:(int)seed
                                  useMlock:(BOOL)useMlock;

// Geração de texto (síncrona)
- (NSString *)generateWithPrompt:(NSString *)prompt
                       maxTokens:(int)maxTokens
                     temperature:(float)temperature
                            topP:(float)topP
                            topK:(int)topK
                   repeatPenalty:(float)repeatPenalty
                   stopSequences:(NSArray<NSString *> *)stopSequences;

// Geração com streaming
- (void)generateStreamingWithPrompt:(NSString *)prompt
                          maxTokens:(int)maxTokens
                        temperature:(float)temperature
                               topP:(float)topP
                               topK:(int)topK
                      repeatPenalty:(float)repeatPenalty
                      stopSequences:(NSArray<NSString *> *)stopSequences
                      tokenCallback:(LlamaTokenCallback)callback;

// Controle
- (void)stopGeneration;
- (void)freeContext;

// Status
@property (nonatomic, readonly) BOOL isValid;
@property (nonatomic, readonly) BOOL isGenerating;
@property (nonatomic, readonly, nullable) NSString *modelInfo;

@end

NS_ASSUME_NONNULL_END
```

**Arquivo: `ios/LlamaModule/LlamaContextWrapperPrivate.h`** (Header privado - COM tipos C++)

```objc
//
//  LlamaContextWrapperPrivate.h
//  Header privado com tipos C++ - NÃO importar no bridging header!
//

#import "LlamaContextWrapper.h"
#include "llama.h"
#include <atomic>

@interface LlamaContextWrapper ()

@property (nonatomic, assign) llama_model *model;
@property (nonatomic, assign) llama_context *ctx;
@property (nonatomic, assign) llama_sampler *sampler;
@property (nonatomic, assign) std::atomic<bool> shouldStop;

@end
```

**Arquivo: `ios/LlamaModule/LlamaContextWrapper.mm`** (Implementação)

```objc
//
//  LlamaContextWrapper.mm
//  Implementação do wrapper llama.cpp
//

#import "LlamaContextWrapperPrivate.h"
#include "llama.h"
#include <string>
#include <vector>
#include <thread>

@implementation LlamaContextWrapper {
    std::atomic<bool> _shouldStop;
    std::atomic<bool> _isGenerating;
}

#pragma mark - Inicialização

+ (void)initialize {
    if (self == [LlamaContextWrapper class]) {
        // Inicializa o backend llama.cpp uma única vez
        static dispatch_once_t onceToken;
        dispatch_once(&onceToken, ^{
            llama_backend_init();
            llama_numa_init(GGML_NUMA_STRATEGY_DISABLED);
        });
    }
}

- (nullable instancetype)initWithModelPath:(NSString *)modelPath
                             contextLength:(int)contextLength
                                 gpuLayers:(int)gpuLayers
                                      seed:(int)seed
                                  useMlock:(BOOL)useMlock {
    self = [super init];
    if (self) {
        _shouldStop.store(false);
        _isGenerating.store(false);
        
        // Configurar parâmetros do modelo
        llama_model_params modelParams = llama_model_default_params();
        modelParams.n_gpu_layers = gpuLayers;
        modelParams.use_mlock = useMlock;
        
        // Carregar modelo
        const char *cPath = [modelPath UTF8String];
        _model = llama_load_model_from_file(cPath, modelParams);
        
        if (!_model) {
            NSLog(@"[LlamaWrapper] Falha ao carregar modelo: %@", modelPath);
            return nil;
        }
        
        // Configurar parâmetros do contexto
        llama_context_params ctxParams = llama_context_default_params();
        ctxParams.n_ctx = contextLength;
        ctxParams.n_batch = 512;
        ctxParams.n_ubatch = 512;
        ctxParams.n_threads = (int)std::thread::hardware_concurrency();
        ctxParams.n_threads_batch = ctxParams.n_threads;
        
        if (seed > 0) {
            // Seed é configurado no sampler, não no contexto
        }
        
        // Criar contexto
        _ctx = llama_new_context_with_model(_model, ctxParams);
        
        if (!_ctx) {
            NSLog(@"[LlamaWrapper] Falha ao criar contexto");
            llama_free_model(_model);
            _model = nullptr;
            return nil;
        }
        
        // Criar sampler padrão
        _sampler = llama_sampler_chain_init(llama_sampler_chain_default_params());
        llama_sampler_chain_add(_sampler, llama_sampler_init_temp(0.7f));
        llama_sampler_chain_add(_sampler, llama_sampler_init_dist(seed > 0 ? seed : LLAMA_DEFAULT_SEED));
        
        NSLog(@"[LlamaWrapper] Modelo carregado com sucesso");
    }
    return self;
}

#pragma mark - Geração de Texto

- (NSString *)generateWithPrompt:(NSString *)prompt
                       maxTokens:(int)maxTokens
                     temperature:(float)temperature
                            topP:(float)topP
                            topK:(int)topK
                   repeatPenalty:(float)repeatPenalty
                   stopSequences:(NSArray<NSString *> *)stopSequences {
    
    if (!_ctx || !_model) {
        return @"Erro: Modelo não carregado";
    }
    
    __block NSMutableString *result = [NSMutableString string];
    
    [self generateStreamingWithPrompt:prompt
                            maxTokens:maxTokens
                          temperature:temperature
                                 topP:topP
                                 topK:topK
                        repeatPenalty:repeatPenalty
                        stopSequences:stopSequences
                        tokenCallback:^(NSString *token, NSInteger tokenId, BOOL isComplete, NSInteger tokensGenerated) {
        [result appendString:token];
    }];
    
    return result;
}

- (void)generateStreamingWithPrompt:(NSString *)prompt
                          maxTokens:(int)maxTokens
                        temperature:(float)temperature
                               topP:(float)topP
                               topK:(int)topK
                      repeatPenalty:(float)repeatPenalty
                      stopSequences:(NSArray<NSString *> *)stopSequences
                      tokenCallback:(LlamaTokenCallback)callback {
    
    if (!_ctx || !_model) {
        if (callback) {
            callback(@"Erro: Modelo não carregado", -1, YES, 0);
        }
        return;
    }
    
    _shouldStop.store(false);
    _isGenerating.store(true);
    
    // Reconfigurar sampler com novos parâmetros
    if (_sampler) {
        llama_sampler_free(_sampler);
    }
    
    _sampler = llama_sampler_chain_init(llama_sampler_chain_default_params());
    llama_sampler_chain_add(_sampler, llama_sampler_init_top_k(topK));
    llama_sampler_chain_add(_sampler, llama_sampler_init_top_p(topP, 1));
    llama_sampler_chain_add(_sampler, llama_sampler_init_temp(temperature));
    llama_sampler_chain_add(_sampler, llama_sampler_init_dist(LLAMA_DEFAULT_SEED));
    
    // Tokenizar prompt
    std::string promptStr = [prompt UTF8String];
    int n_prompt_tokens = -llama_tokenize(_model, promptStr.c_str(), (int)promptStr.length(), nullptr, 0, true, true);
    
    std::vector<llama_token> tokens(n_prompt_tokens);
    llama_tokenize(_model, promptStr.c_str(), (int)promptStr.length(), tokens.data(), (int)tokens.size(), true, true);
    
    // Limpar contexto anterior
    llama_kv_cache_clear(_ctx);
    
    // Processar prompt
    llama_batch batch = llama_batch_init(512, 0, 1);
    
    for (size_t i = 0; i < tokens.size(); i++) {
        llama_batch_add(batch, tokens[i], (int)i, { 0 }, false);
    }
    batch.logits[batch.n_tokens - 1] = true;
    
    if (llama_decode(_ctx, batch) != 0) {
        NSLog(@"[LlamaWrapper] Falha ao processar prompt");
        llama_batch_free(batch);
        _isGenerating.store(false);
        if (callback) {
            callback(@"Erro: Falha ao processar prompt", -1, YES, 0);
        }
        return;
    }
    
    llama_batch_free(batch);
    
    // Converter stop sequences
    std::vector<std::string> stopSeqs;
    for (NSString *seq in stopSequences) {
        stopSeqs.push_back([seq UTF8String]);
    }
    
    // Gerar tokens
    int n_cur = (int)tokens.size();
    int n_generated = 0;
    std::string generatedText;
    
    while (n_generated < maxTokens && !_shouldStop.load()) {
        // Amostrar próximo token
        llama_token new_token = llama_sampler_sample(_sampler, _ctx, -1);
        
        // Verificar fim de sequência
        if (llama_token_is_eog(_model, new_token)) {
            break;
        }
        
        // Converter token para texto
        char buf[256];
        int n = llama_token_to_piece(_model, new_token, buf, sizeof(buf), 0, true);
        
        if (n < 0) {
            break;
        }
        
        std::string piece(buf, n);
        generatedText += piece;
        n_generated++;
        
        // Verificar stop sequences
        bool shouldBreak = false;
        for (const auto& stopSeq : stopSeqs) {
            if (generatedText.find(stopSeq) != std::string::npos) {
                shouldBreak = true;
                break;
            }
        }
        
        if (shouldBreak) {
            break;
        }
        
        // Callback com token
        if (callback) {
            NSString *tokenStr = [NSString stringWithUTF8String:piece.c_str()];
            callback(tokenStr ?: @"", new_token, NO, n_generated);
        }
        
        // Preparar para próxima iteração
        batch = llama_batch_init(1, 0, 1);
        llama_batch_add(batch, new_token, n_cur, { 0 }, true);
        
        if (llama_decode(_ctx, batch) != 0) {
            llama_batch_free(batch);
            break;
        }
        
        llama_batch_free(batch);
        n_cur++;
    }
    
    _isGenerating.store(false);
    
    // Callback final
    if (callback) {
        callback(@"", -1, YES, n_generated);
    }
}

#pragma mark - Controle

- (void)stopGeneration {
    _shouldStop.store(true);
}

- (void)freeContext {
    _shouldStop.store(true);
    
    // Aguardar geração parar
    while (_isGenerating.load()) {
        [NSThread sleepForTimeInterval:0.01];
    }
    
    if (_sampler) {
        llama_sampler_free(_sampler);
        _sampler = nullptr;
    }
    
    if (_ctx) {
        llama_free(_ctx);
        _ctx = nullptr;
    }
    
    if (_model) {
        llama_free_model(_model);
        _model = nullptr;
    }
}

#pragma mark - Properties

- (BOOL)isValid {
    return _ctx != nullptr && _model != nullptr;
}

- (BOOL)isGenerating {
    return _isGenerating.load();
}

- (NSString *)modelInfo {
    if (!_model) {
        return nil;
    }
    
    char desc[256];
    llama_model_desc(_model, desc, sizeof(desc));
    
    return [NSString stringWithFormat:@"Modelo: %s, Contexto: %d tokens",
            desc, _ctx ? llama_n_ctx(_ctx) : 0];
}

#pragma mark - Cleanup

- (void)dealloc {
    [self freeContext];
}

@end
```

### 3.3 Swift Manager

**Arquivo: `ios/LlamaModule/LlamaManager.swift`**

```swift
import Foundation

/// Protocolo para notificar eventos de streaming
@objc(LlamaManagerDelegate)
public protocol LlamaManagerDelegate: AnyObject {
    func onToken(token: String, tokenId: Int, isComplete: Bool, tokensGenerated: Int)
}

/// Gerenciador Swift para llama.cpp
@objc(LlamaManager)
@objcMembers
public class LlamaManager: NSObject {
    
    // MARK: - Singleton
    
    @objc public static let shared = LlamaManager()
    
    // MARK: - Properties
    
    private var contextWrapper: LlamaContextWrapper?
    public weak var delegate: LlamaManagerDelegate?
    
    // MARK: - Initialization
    
    private override init() {
        super.init()
    }
    
    // MARK: - Model Loading
    
    /// Carrega um modelo GGUF
    /// - Parameters:
    ///   - path: Caminho para o arquivo .gguf
    ///   - contextLength: Tamanho do contexto em tokens
    ///   - gpuLayers: Número de camadas para GPU (0 = CPU only)
    ///   - seed: Seed para reprodutibilidade (0 = aleatório)
    ///   - useMlock: Bloquear memória para evitar swap
    /// - Returns: true se carregou com sucesso
    @objc public func loadModel(
        path: String,
        contextLength: Int32,
        gpuLayers: Int32,
        seed: Int32,
        useMlock: Bool
    ) -> Bool {
        // Descarregar modelo anterior se existir
        unloadModel()
        
        contextWrapper = LlamaContextWrapper(
            modelPath: path,
            contextLength: contextLength,
            gpuLayers: gpuLayers,
            seed: seed,
            useMlock: useMlock
        )
        
        return contextWrapper?.isValid ?? false
    }
    
    /// Descarrega o modelo da memória
    @objc public func unloadModel() {
        contextWrapper?.freeContext()
        contextWrapper = nil
    }
    
    // MARK: - Text Generation
    
    /// Gera texto de forma síncrona (bloqueia)
    @objc public func generateText(
        prompt: String,
        maxTokens: Int32,
        temperature: Float,
        topP: Float,
        topK: Int32,
        repeatPenalty: Float,
        stopSequences: [String]
    ) -> String {
        guard let wrapper = contextWrapper, wrapper.isValid else {
            return "Erro: Modelo não carregado"
        }
        
        return wrapper.generate(
            withPrompt: prompt,
            maxTokens: maxTokens,
            temperature: temperature,
            topP: topP,
            topK: topK,
            repeatPenalty: repeatPenalty,
            stopSequences: stopSequences
        )
    }
    
    /// Inicia geração com streaming de tokens
    @objc public func startStreaming(
        prompt: String,
        maxTokens: Int32,
        temperature: Float,
        topP: Float,
        topK: Int32,
        repeatPenalty: Float,
        stopSequences: [String]
    ) {
        guard let wrapper = contextWrapper, wrapper.isValid else {
            delegate?.onToken(token: "Erro: Modelo não carregado", tokenId: -1, isComplete: true, tokensGenerated: 0)
            return
        }
        
        // Executar em background thread
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            wrapper.generateStreaming(
                withPrompt: prompt,
                maxTokens: maxTokens,
                temperature: temperature,
                topP: topP,
                topK: topK,
                repeatPenalty: repeatPenalty,
                stopSequences: stopSequences
            ) { [weak self] token, tokenId, isComplete, tokensGenerated in
                // Notificar delegate na main thread
                DispatchQueue.main.async {
                    self?.delegate?.onToken(
                        token: token ?? "",
                        tokenId: Int(tokenId),
                        isComplete: isComplete,
                        tokensGenerated: Int(tokensGenerated)
                    )
                }
            }
        }
    }
    
    /// Para a geração em andamento
    @objc public func stopStreaming() {
        contextWrapper?.stopGeneration()
    }
    
    // MARK: - Status
    
    /// Verifica se há modelo carregado
    @objc public func isModelLoaded() -> Bool {
        return contextWrapper?.isValid ?? false
    }
    
    /// Obtém informações do modelo
    @objc public func getModelInfo() -> String? {
        return contextWrapper?.modelInfo
    }
}
```

### 3.4 TurboModule Header

**Arquivo: `ios/LlamaModule/RCTNativeLlama.h`**

```objc
//
//  RCTNativeLlama.h
//  TurboModule para llama.cpp
//

#import <Foundation/Foundation.h>

// Import do spec gerado pelo Codegen
// O nome vem do codegenConfig.name no package.json
#ifdef RCT_NEW_ARCH_ENABLED
#import <NativeLlamaSpec/NativeLlamaSpec.h>
#endif

NS_ASSUME_NONNULL_BEGIN

#ifdef RCT_NEW_ARCH_ENABLED
@interface RCTNativeLlama : NSObject <NativeLlamaSpec>
#else
@interface RCTNativeLlama : NSObject
#endif

@end

NS_ASSUME_NONNULL_END
```

### 3.5 TurboModule Implementation

**Arquivo: `ios/LlamaModule/RCTNativeLlama.mm`**

```objc
//
//  RCTNativeLlama.mm
//  Implementação do TurboModule
//

#import "RCTNativeLlama.h"

// Import do header Swift gerado automaticamente
// O nome é: [TargetName]-Swift.h (substitua hífens por underscores)
#import "MeuApp-Swift.h"

#import <React/RCTLog.h>
#import <React/RCTUtils.h>

#ifdef RCT_NEW_ARCH_ENABLED
#import <React/RCTBridge+Private.h>
#import <ReactCommon/RCTTurboModule.h>
#endif

@interface RCTNativeLlama () <LlamaManagerDelegate>

@property (nonatomic, assign) BOOL hasListeners;

@end

@implementation RCTNativeLlama {
    LlamaManager *_manager;
}

RCT_EXPORT_MODULE(NativeLlama)

#pragma mark - Initialization

- (instancetype)init {
    self = [super init];
    if (self) {
        _manager = [LlamaManager shared];
        _manager.delegate = self;
        _hasListeners = NO;
    }
    return self;
}

#pragma mark - TurboModule

#ifdef RCT_NEW_ARCH_ENABLED
- (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:
    (const facebook::react::ObjCTurboModule::InitParams &)params {
    return std::make_shared<facebook::react::NativeLlamaSpecJSI>(params);
}
#endif

#pragma mark - Event Emitter Support

- (NSArray<NSString *> *)supportedEvents {
    return @[@"onToken"];
}

- (void)startObserving {
    _hasListeners = YES;
}

- (void)stopObserving {
    _hasListeners = NO;
}

- (void)addListener:(NSString *)eventName {
    // Necessário para Codegen
}

- (void)removeListeners:(double)count {
    // Necessário para Codegen
}

#pragma mark - LlamaManagerDelegate

- (void)onTokenWithToken:(NSString *)token
                 tokenId:(NSInteger)tokenId
              isComplete:(BOOL)isComplete
         tokensGenerated:(NSInteger)tokensGenerated {
    if (_hasListeners) {
        [self sendEventWithName:@"onToken" body:@{
            @"token": token ?: @"",
            @"tokenId": @(tokenId),
            @"isComplete": @(isComplete),
            @"tokensGenerated": @(tokensGenerated)
        }];
    }
}

// Método auxiliar para enviar eventos
- (void)sendEventWithName:(NSString *)name body:(NSDictionary *)body {
    // Para TurboModules com New Architecture, usamos o bridge
    // Em produção, considere usar o padrão de EventEmitter tipado
    [[NSNotificationCenter defaultCenter] 
        postNotificationName:name 
        object:nil 
        userInfo:body];
}

#pragma mark - Module Methods

- (void)loadModel:(NSString *)path 
           config:(JS::NativeLlama::ModelConfig &)config 
          resolve:(RCTPromiseResolveBlock)resolve 
           reject:(RCTPromiseRejectBlock)reject {
    
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        BOOL success = [self->_manager loadModelWithPath:path
                                          contextLength:(int32_t)config.contextLength()
                                              gpuLayers:(int32_t)config.gpuLayers()
                                                   seed:(int32_t)config.seed()
                                               useMlock:config.useMlock()];
        
        dispatch_async(dispatch_get_main_queue(), ^{
            resolve(@(success));
        });
    });
}

- (void)generateText:(NSString *)prompt 
              config:(JS::NativeLlama::GenerationConfig &)config 
             resolve:(RCTPromiseResolveBlock)resolve 
              reject:(RCTPromiseRejectBlock)reject {
    
    // Converter stopSequences
    NSMutableArray<NSString *> *stopSeqs = [NSMutableArray array];
    if (config.stopSequences().has_value()) {
        for (const auto &seq : config.stopSequences().value()) {
            [stopSeqs addObject:[NSString stringWithUTF8String:seq.c_str()]];
        }
    }
    
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        NSString *result = [self->_manager generateTextWithPrompt:prompt
                                                        maxTokens:(int32_t)config.maxTokens()
                                                      temperature:(float)config.temperature()
                                                             topP:(float)config.topP()
                                                             topK:(int32_t)config.topK()
                                                    repeatPenalty:(float)config.repeatPenalty()
                                                    stopSequences:stopSeqs];
        
        dispatch_async(dispatch_get_main_queue(), ^{
            resolve(result);
        });
    });
}

- (void)startStreaming:(NSString *)prompt 
                config:(JS::NativeLlama::GenerationConfig &)config {
    
    // Converter stopSequences
    NSMutableArray<NSString *> *stopSeqs = [NSMutableArray array];
    if (config.stopSequences().has_value()) {
        for (const auto &seq : config.stopSequences().value()) {
            [stopSeqs addObject:[NSString stringWithUTF8String:seq.c_str()]];
        }
    }
    
    [_manager startStreamingWithPrompt:prompt
                             maxTokens:(int32_t)config.maxTokens()
                           temperature:(float)config.temperature()
                                  topP:(float)config.topP()
                                  topK:(int32_t)config.topK()
                         repeatPenalty:(float)config.repeatPenalty()
                         stopSequences:stopSeqs];
}

- (void)stopStreaming {
    [_manager stopStreaming];
}

- (void)unloadModel:(RCTPromiseResolveBlock)resolve 
             reject:(RCTPromiseRejectBlock)reject {
    [_manager unloadModel];
    resolve(nil);
}

- (NSNumber *)isModelLoaded {
    return @([_manager isModelLoaded]);
}

- (void)getModelInfo:(RCTPromiseResolveBlock)resolve 
              reject:(RCTPromiseRejectBlock)reject {
    NSString *info = [_manager getModelInfo];
    resolve(info ?: @"Nenhum modelo carregado");
}

@end
```

---

## Parte 4: Wrapper JavaScript/TypeScript

**Arquivo: `src/modules/llama/index.ts`**

```typescript
import {
  NativeEventEmitter,
  NativeModules,
  Platform,
} from 'react-native';
import NativeLlama from '../../specs/NativeLlamaSpec';
import type { ModelConfig, GenerationConfig, TokenPayload } from '../../specs/NativeLlamaSpec';

// Re-exportar tipos
export type { ModelConfig, GenerationConfig, TokenPayload };

// Verificar se o módulo existe
const LINKING_ERROR =
  `O módulo 'NativeLlama' não foi linkado. Verifique:\n\n` +
  `- Você executou 'pod install' no diretório ios?\n` +
  `- Você reconstruiu o app após instalar o módulo?\n` +
  `- O New Architecture está habilitado?\n`;

// Proxy para mostrar erro se módulo não existir
const LlamaModule = NativeLlama
  ? NativeLlama
  : new Proxy(
      {},
      {
        get() {
          throw new Error(LINKING_ERROR);
        },
      }
    );

// Event emitter para streaming
const eventEmitter = new NativeEventEmitter(LlamaModule as any);

// Tipos para callbacks
type TokenCallback = (payload: TokenPayload) => void;
type UnsubscribeFunction = () => void;

/**
 * API de alto nível para llama.cpp
 */
class LlamaAPI {
  private tokenListeners: Map<string, TokenCallback> = new Map();
  private subscription: ReturnType<typeof eventEmitter.addListener> | null = null;

  constructor() {
    this.setupEventListener();
  }

  private setupEventListener() {
    this.subscription = eventEmitter.addListener('onToken', (payload: TokenPayload) => {
      this.tokenListeners.forEach((callback) => {
        callback(payload);
      });
    });
  }

  /**
   * Carrega um modelo GGUF
   * @param modelPath Caminho para o arquivo .gguf
   * @param config Configuração opcional do modelo
   */
  async loadModel(
    modelPath: string,
    config: Partial<ModelConfig> = {}
  ): Promise<boolean> {
    const fullConfig: ModelConfig = {
      contextLength: config.contextLength ?? 2048,
      gpuLayers: config.gpuLayers ?? 0, // 0 = CPU only, 99 = todas para GPU
      seed: config.seed ?? 0, // 0 = aleatório
      useMlock: config.useMlock ?? true,
    };

    return LlamaModule.loadModel(modelPath, fullConfig);
  }

  /**
   * Gera texto (não-streaming)
   * @param prompt O prompt de entrada
   * @param config Configuração de geração
   */
  async generateText(
    prompt: string,
    config: Partial<GenerationConfig> = {}
  ): Promise<string> {
    const fullConfig: GenerationConfig = {
      maxTokens: config.maxTokens ?? 256,
      temperature: config.temperature ?? 0.7,
      topP: config.topP ?? 0.9,
      topK: config.topK ?? 40,
      repeatPenalty: config.repeatPenalty ?? 1.1,
      stopSequences: config.stopSequences ?? [],
    };

    return LlamaModule.generateText(prompt, fullConfig);
  }

  /**
   * Inicia geração com streaming de tokens
   * @param prompt O prompt de entrada
   * @param onToken Callback chamado para cada token
   * @param config Configuração de geração
   * @returns Função para cancelar o streaming
   */
  startStreaming(
    prompt: string,
    onToken: TokenCallback,
    config: Partial<GenerationConfig> = {}
  ): UnsubscribeFunction {
    const fullConfig: GenerationConfig = {
      maxTokens: config.maxTokens ?? 256,
      temperature: config.temperature ?? 0.7,
      topP: config.topP ?? 0.9,
      topK: config.topK ?? 40,
      repeatPenalty: config.repeatPenalty ?? 1.1,
      stopSequences: config.stopSequences ?? [],
    };

    // Gerar ID único para este listener
    const listenerId = `${Date.now()}-${Math.random()}`;
    this.tokenListeners.set(listenerId, onToken);

    // Iniciar streaming
    LlamaModule.startStreaming(prompt, fullConfig);

    // Retornar função de cleanup
    return () => {
      this.tokenListeners.delete(listenerId);
      this.stopStreaming();
    };
  }

  /**
   * Para a geração em andamento
   */
  stopStreaming(): void {
    LlamaModule.stopStreaming();
  }

  /**
   * Descarrega o modelo da memória
   */
  async unloadModel(): Promise<void> {
    return LlamaModule.unloadModel();
  }

  /**
   * Verifica se há modelo carregado
   */
  isModelLoaded(): boolean {
    return LlamaModule.isModelLoaded();
  }

  /**
   * Obtém informações do modelo carregado
   */
  async getModelInfo(): Promise<string> {
    return LlamaModule.getModelInfo();
  }

  /**
   * Limpa recursos ao desmontar
   */
  cleanup(): void {
    this.tokenListeners.clear();
    this.subscription?.remove();
  }
}

// Exportar instância singleton
export const Llama = new LlamaAPI();

// Exportar classe para casos que precisam de múltiplas instâncias
export { LlamaAPI };

// Hook para React
export function useLlama() {
  return Llama;
}
```

**Exemplo de uso em um componente React:**

```typescript
// App.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, ScrollView } from 'react-native';
import { Llama, TokenPayload } from './src/modules/llama';

export default function App() {
  const [prompt, setPrompt] = useState('Olá, como você está?');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isModelLoaded, setIsModelLoaded] = useState(false);

  useEffect(() => {
    loadModel();
    return () => Llama.cleanup();
  }, []);

  const loadModel = async () => {
    setIsLoading(true);
    try {
      const modelPath = 'file:///path/to/model.gguf';
      const success = await Llama.loadModel(modelPath, {
        contextLength: 2048,
        gpuLayers: 99, // Usar Metal no iOS
      });
      setIsModelLoaded(success);
      console.log('Modelo carregado:', success);
    } catch (error) {
      console.error('Erro ao carregar modelo:', error);
    }
    setIsLoading(false);
  };

  const generateWithStreaming = () => {
    setResponse('');
    setIsLoading(true);
    
    const cancel = Llama.startStreaming(
      prompt,
      (payload: TokenPayload) => {
        if (!payload.isComplete) {
          setResponse(prev => prev + payload.token);
        } else {
          setIsLoading(false);
          console.log(`Gerados ${payload.tokensGenerated} tokens`);
        }
      },
      {
        maxTokens: 256,
        temperature: 0.7,
      }
    );

    // Para cancelar: cancel();
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text>Status: {isModelLoaded ? 'Modelo carregado' : 'Sem modelo'}</Text>
      
      <TextInput
        value={prompt}
        onChangeText={setPrompt}
        placeholder="Digite seu prompt..."
        multiline
        style={{ borderWidth: 1, padding: 10, marginVertical: 10 }}
      />
      
      <Button
        title={isLoading ? 'Gerando...' : 'Gerar'}
        onPress={generateWithStreaming}
        disabled={isLoading || !isModelLoaded}
      />
      
      <ScrollView style={{ flex: 1, marginTop: 20 }}>
        <Text>{response}</Text>
      </ScrollView>
    </View>
  );
}
```

---

## Parte 5: Configuração de build

### 5.1 Podspec

**Arquivo: `ios/LlamaModule/LlamaModule.podspec`**

```ruby
require "json"

package = JSON.parse(File.read(File.join(__dir__, "..", "..", "package.json")))

# Flags do Folly necessárias para TurboModules
folly_compiler_flags = '-DFOLLY_NO_CONFIG -DFOLLY_MOBILE=1 -DFOLLY_USE_LIBCPP=1 -Wno-comma -Wno-shorten-64-to-32'

Pod::Spec.new do |s|
  s.name         = "LlamaModule"
  s.version      = package["version"]
  s.summary      = "TurboModule nativo para llama.cpp"
  s.homepage     = "https://github.com/seu-usuario/seu-repo"
  s.license      = package["license"]
  s.authors      = package["author"]

  s.platforms    = { :ios => "15.0" }
  s.source       = { :git => ".git", :tag => "#{s.version}" }

  # Arquivos fonte
  s.source_files = [
    "*.{h,m,mm,swift}",
    "**/*.{h,m,mm,swift}"
  ]
  
  # Headers
  s.public_header_files = [
    "RCTNativeLlama.h",
    "LlamaContextWrapper.h"
  ]
  
  s.private_header_files = [
    "LlamaContextWrapperPrivate.h"
  ]
  
  # XCFramework do llama.cpp
  s.vendored_frameworks = "../Frameworks/llama.xcframework"
  s.preserve_paths = "../Frameworks/llama.xcframework"
  
  # Configurações de build para C++
  s.pod_target_xcconfig = {
    # C++ standard
    "CLANG_CXX_LANGUAGE_STANDARD" => "c++17",
    "CLANG_CXX_LIBRARY" => "libc++",
    
    # Header search paths
    "HEADER_SEARCH_PATHS" => [
      "\"$(PODS_ROOT)/boost\"",
      "\"$(PODS_TARGET_SRCROOT)\"",
      "\"$(PODS_ROOT)/RCT-Folly\"",
      "\"$(PODS_ROOT)/Headers/Private/React-Core\""
    ].join(" "),
    
    # Compiler flags
    "OTHER_CPLUSPLUSFLAGS" => "-DFOLLY_NO_CONFIG -DFOLLY_MOBILE=1 -DFOLLY_USE_LIBCPP=1",
    
    # Swift interop
    "SWIFT_OBJC_INTEROP_MODE" => "objcxx",
    
    # Enable C++ exceptions
    "GCC_ENABLE_CPP_EXCEPTIONS" => "YES",
    
    # Preprocessor definitions
    "GCC_PREPROCESSOR_DEFINITIONS" => "$(inherited) RCT_NEW_ARCH_ENABLED=1"
  }
  
  # User target settings
  s.user_target_xcconfig = {
    "CLANG_CXX_LANGUAGE_STANDARD" => "c++17"
  }
  
  # Compiler flags
  s.compiler_flags = folly_compiler_flags + " -DRCT_NEW_ARCH_ENABLED=1 -fno-objc-arc"
  
  # Link libraries
  s.library = "c++"
  
  # Frameworks necessários para llama.cpp com Metal
  s.frameworks = [
    "Accelerate",
    "Metal", 
    "MetalKit",
    "MetalPerformanceShaders",
    "Foundation"
  ]
  
  # Dependências React Native
  if respond_to?(:install_modules_dependencies, true)
    install_modules_dependencies(s)
  else
    s.dependency "React-Core"
    s.dependency "React-Codegen"
    s.dependency "RCT-Folly"
    s.dependency "RCTRequired"
    s.dependency "RCTTypeSafety"
    s.dependency "ReactCommon/turbomodule/core"
  end
end
```

### 5.2 Podfile do app

Adicione ao `ios/Podfile`:

```ruby
require_relative '../node_modules/react-native/scripts/react_native_pods'
require_relative '../node_modules/@react-native-community/cli-platform-ios/native_modules'

platform :ios, '15.0'

prepare_react_native_project!

# Forçar New Architecture
ENV['RCT_NEW_ARCH_ENABLED'] = '1'

target 'MeuApp' do
  config = use_native_modules!

  use_react_native!(
    :path => config[:reactNativePath],
    :app_path => "#{Pod::Config.instance.installation_root}/.."
  )
  
  # Incluir o módulo Llama
  pod 'LlamaModule', :path => './LlamaModule'

  target 'MeuAppTests' do
    inherit! :complete
  end

  post_install do |installer|
    react_native_post_install(
      installer,
      config[:reactNativePath],
      :mac_catalyst_enabled => false
    )
    
    # Configurações adicionais para C++
    installer.pods_project.targets.each do |target|
      target.build_configurations.each do |config|
        config.build_settings['CLANG_CXX_LANGUAGE_STANDARD'] = 'c++17'
        config.build_settings['GCC_ENABLE_CPP_EXCEPTIONS'] = 'YES'
      end
    end
  end
end
```

### 5.3 Entitlements (Importante para modelos grandes)

**Arquivo: `ios/MeuApp/MeuApp.entitlements`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Permite endereçamento virtual estendido (modelos > 4GB) -->
    <key>com.apple.developer.kernel.extended-virtual-addressing</key>
    <true/>
    
    <!-- Aumenta limite de memória do app -->
    <key>com.apple.developer.kernel.increased-memory-limit</key>
    <true/>
</dict>
</plist>
```

---

## Parte 6: Integração no projeto

### Passo a passo completo

**1. Criar a estrutura de diretórios:**

```bash
# Na raiz do projeto React Native
mkdir -p src/specs
mkdir -p src/modules/llama
mkdir -p ios/LlamaModule
mkdir -p ios/Frameworks
```

**2. Copiar o llama.xcframework:**

```bash
# Assumindo que você já compilou o xcframework
cp -R /path/to/llama.xcframework ios/Frameworks/
```

**3. Criar todos os arquivos conforme as partes anteriores**

**4. Adicionar ao Xcode:**

1. Abra `ios/MeuApp.xcworkspace` no Xcode
2. Clique com botão direito no projeto → **Add Files to "MeuApp"**
3. Selecione a pasta `LlamaModule` inteira
4. Marque **Create groups** e **Add to targets: MeuApp**
5. Repita para `Frameworks/llama.xcframework`

**5. Configurar bridging header no Xcode:**

1. Build Settings → **Swift Compiler - General**
2. **Objective-C Bridging Header**: `$(SRCROOT)/MeuApp/MeuApp-Bridging-Header.h`

**6. Habilitar New Architecture:**

```bash
# No arquivo .env ou diretamente
export RCT_NEW_ARCH_ENABLED=1
```

**7. Instalar pods e buildar:**

```bash
cd ios
RCT_NEW_ARCH_ENABLED=1 pod install
cd ..

# Buildar o app
npx react-native run-ios
```

**8. Gerar código do Codegen:**

```bash
# O Codegen roda automaticamente no build, mas pode forçar:
cd ios
RCT_NEW_ARCH_ENABLED=1 pod install

# Ou manualmente:
node node_modules/react-native/scripts/generate-codegen-artifacts.js \
    --path . \
    --outputPath ios/build/generated/ios \
    --targetPlatform ios
```

---

## Parte 7: Streaming de tokens (implementação detalhada)

O streaming já está implementado nas partes anteriores, mas aqui está um resumo da arquitetura:

### Fluxo de eventos

```
LlamaContextWrapper.mm (callback block)
         │
         ▼
LlamaManager.swift (delegate method)
         │
         ▼
RCTNativeLlama.mm (sendEventWithName)
         │
         ▼
NativeEventEmitter (JavaScript)
         │
         ▼
Seu componente React
```

### Hook customizado para streaming

**Arquivo: `src/modules/llama/useLlamaStream.ts`**

```typescript
import { useState, useCallback, useRef, useEffect } from 'react';
import { Llama, TokenPayload, GenerationConfig } from './index';

interface StreamState {
  text: string;
  isStreaming: boolean;
  tokensGenerated: number;
  error: string | null;
}

export function useLlamaStream() {
  const [state, setState] = useState<StreamState>({
    text: '',
    isStreaming: false,
    tokensGenerated: 0,
    error: null,
  });
  
  const cancelRef = useRef<(() => void) | null>(null);
  const textRef = useRef('');

  // Cleanup ao desmontar
  useEffect(() => {
    return () => {
      cancelRef.current?.();
    };
  }, []);

  const startStream = useCallback((
    prompt: string,
    config?: Partial<GenerationConfig>
  ) => {
    // Cancelar stream anterior
    cancelRef.current?.();
    
    // Reset state
    textRef.current = '';
    setState({
      text: '',
      isStreaming: true,
      tokensGenerated: 0,
      error: null,
    });

    cancelRef.current = Llama.startStreaming(
      prompt,
      (payload: TokenPayload) => {
        if (payload.isComplete) {
          setState(prev => ({
            ...prev,
            isStreaming: false,
            tokensGenerated: payload.tokensGenerated,
          }));
        } else {
          textRef.current += payload.token;
          setState(prev => ({
            ...prev,
            text: textRef.current,
            tokensGenerated: payload.tokensGenerated,
          }));
        }
      },
      config
    );
  }, []);

  const stopStream = useCallback(() => {
    cancelRef.current?.();
    cancelRef.current = null;
    setState(prev => ({ ...prev, isStreaming: false }));
  }, []);

  return {
    ...state,
    startStream,
    stopStream,
  };
}
```

---

## Parte 8: Testando a integração

### Checklist de verificação

1. **Verificar se o módulo foi registrado:**

```typescript
import { TurboModuleRegistry } from 'react-native';

const module = TurboModuleRegistry.get('NativeLlama');
console.log('Módulo existe:', !!module);
```

2. **Testar carregamento do modelo:**

```typescript
try {
  const success = await Llama.loadModel('file:///path/to/model.gguf', {
    contextLength: 512,
    gpuLayers: 0, // Comece com CPU para teste
  });
  console.log('Modelo carregado:', success);
  
  const info = await Llama.getModelInfo();
  console.log('Info:', info);
} catch (error) {
  console.error('Erro:', error);
}
```

3. **Testar geração simples:**

```typescript
const response = await Llama.generateText('Olá!', {
  maxTokens: 50,
  temperature: 0.7,
});
console.log('Resposta:', response);
```

4. **Testar streaming:**

```typescript
Llama.startStreaming(
  'Conte uma história curta.',
  (payload) => {
    process.stdout.write(payload.token);
    if (payload.isComplete) {
      console.log('\n--- FIM ---');
    }
  },
  { maxTokens: 100 }
);
```

### Debugging no Xcode

1. Adicione breakpoints nos arquivos `.mm` e `.swift`
2. Use `NSLog` e `print` para logs
3. Verifique o console do Xcode para erros de linkagem
4. Use **Product → Scheme → Edit Scheme → Run → Arguments** para adicionar flags de debug

---

## Solução de problemas

### Erro: "Module 'NativeLlamaSpec' not found"

**Causa:** Codegen não gerou os arquivos.

**Solução:**
```bash
cd ios
rm -rf Pods build
RCT_NEW_ARCH_ENABLED=1 pod install
```

### Erro: "Cannot find 'LlamaManager' in scope"

**Causa:** Header Swift não foi gerado.

**Solução:**
1. Verifique se o arquivo Swift está no target correto
2. Build o projeto uma vez para gerar `MeuApp-Swift.h`
3. Verifique o nome correto do header (substitua hífens por underscores)

### Erro: "llama.h file not found"

**Causa:** XCFramework não está linkado corretamente.

**Solução:**
1. Verifique se `vendored_frameworks` no Podspec aponta para o caminho correto
2. Adicione o framework manualmente no Xcode se necessário
3. Verifique **Build Phases → Link Binary With Libraries**

### Erro: "Undefined symbols for architecture arm64"

**Causa:** Bibliotecas C++ não estão linkadas.

**Solução:**
```ruby
# No Podspec
s.library = "c++"
s.pod_target_xcconfig = {
  "CLANG_CXX_LANGUAGE_STANDARD" => "c++17"
}
```

### Erro: "Failed to load model"

**Causas possíveis:**
- Caminho do arquivo incorreto
- Modelo GGUF corrompido ou incompatível
- Memória insuficiente

**Solução:**
1. Use caminho absoluto começando com `file://`
2. Teste com modelo menor primeiro
3. Adicione entitlements de memória

### Crash no iOS 26 com Metal

**Causa:** Bug conhecido no llama.cpp com versões recentes do iOS.

**Solução temporária:**
```typescript
await Llama.loadModel(path, {
  gpuLayers: 0, // Usar apenas CPU
});
```

### Performance lenta

**Otimizações:**
1. Use `gpuLayers: 99` para Metal (quando funcionar)
2. Aumente `n_batch` no contexto
3. Use modelos quantizados (Q4_K_M ou Q5_K_M)
4. Habilite `useMlock: true`

---

## Compatibilidade

| React Native | Status | Notas |
|--------------|--------|-------|
| 0.76+ | ✅ Suportado | Recomendado |
| 0.74-0.75 | ⚠️ Parcial | Pode funcionar com ajustes |
| < 0.74 | ❌ Não suportado | Falta suporte a TurboModules |

| iOS | Status | Notas |
|-----|--------|-------|
| 18.x | ✅ Funciona | Metal pode ter issues |
| 26 beta | ⚠️ Parcial | Use CPU mode |
| < 15 | ❌ Não suportado | |

| Xcode | Status |
|-------|--------|
| 16+ | ✅ Recomendado |
| 15.3+ | ✅ Funciona |
| < 15 | ❌ Não suportado |

---

## Considerações finais

Este tutorial cobriu a criação completa de um TurboModule nativo para iOS que integra Swift com llama.cpp no React Native New Architecture. Os pontos-chave são:

- **Swift não pode ser usado diretamente** em TurboModules devido à incompatibilidade com C++. Use o padrão Adapter com Objective-C++ como ponte.
- **Headers privados** são essenciais para esconder tipos C++ do Swift.
- **Codegen** gera automaticamente o código de interface a partir das especificações TypeScript.
- **Streaming** usa o padrão delegate em Swift que notifica o TurboModule, que por sua vez emite eventos para JavaScript.
- **Metal** pode ter problemas em versões recentes do iOS; tenha um fallback para CPU.

Com esta base, você pode expandir o módulo para incluir mais funcionalidades como chat templates, grammar sampling, embedding generation, e outros recursos do llama.cpp.