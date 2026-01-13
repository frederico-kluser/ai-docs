# Guia Completo: Capacidades Nativas do iPhone com React Native CLI (Bare Workflow)

O React Native CLI oferece acesso a **mais de 500 capacidades nativas** do iPhone através de bibliotecas de terceiros e módulos nativos personalizados. Este guia documenta todas as 10 categorias de funcionalidades iOS, incluindo bibliotecas recomendadas, configuração, exemplos de código e limitações conhecidas.

---

## Contexto técnico e arquitetura

O React Native em **bare workflow** (sem Expo gerenciado) permite acesso direto às APIs nativas do iOS através de duas arquiteturas: a **Legacy Bridge** (módulos nativos tradicionais) e a **New Architecture** (Turbo Modules, Fabric e JSI). A partir do React Native **0.76+**, a Nova Arquitetura vem habilitada por padrão, oferecendo chamadas síncronas e melhor performance.

A comunicação com APIs nativas acontece através de **native modules** escritos em Swift ou Objective-C, que podem ser criados manualmente ou utilizados via bibliotecas npm. Cada capacidade requer configurações específicas no **Info.plist** (descrições de uso), **entitlements** (permissões especiais) e capacidades no **Xcode**.

---

## Categoria 1: Controles de dispositivo e sistema

### Informações do dispositivo

A biblioteca **react-native-device-info** (v15.0.1) é o padrão da indústria para acessar dados do dispositivo, com **6.6k stars** no GitHub e atualizações ativas. Ela fornece modelo do iPhone, versão do iOS, ID único (IDFV), nome do dispositivo, operadora e informações de bateria e armazenamento.

```typescript
import DeviceInfo from 'react-native-device-info';

const modelo = DeviceInfo.getModel(); // "iPhone 14 Pro"
const versaoOS = DeviceInfo.getSystemVersion(); // "17.0"
const bateria = await DeviceInfo.getBatteryLevel(); // 0.75
const espacoLivre = await DeviceInfo.getFreeDiskStorage(); // bytes
```

**Instalação**: `npm install react-native-device-info && cd ios && pod install`

**Limitações**: Endereço MAC sempre retorna "02:00:00:00:00:00" (restrição iOS desde v7), número de série indisponível, e no iOS 16+ o nome do dispositivo definido pelo usuário requer entitlements específicos.

### Brilho da tela

A biblioteca **@adrianso/react-native-device-brightness** permite ler e ajustar o brilho da tela (valores de 0 a 1). Porém, **Night Shift**, **True Tone** e **Always-On Display** são configurações de sistema inacessíveis por apps de terceiros.

### Feedback háptico

O **react-native-haptic-feedback** (v2.3.3) expõe os três tipos de feedback do iOS: `UIImpactFeedbackGenerator` (light, medium, heavy), `UISelectionFeedbackGenerator` e `UINotificationFeedbackGenerator` (success, warning, error). Para padrões de vibração customizados via **Core Haptics** (CHHapticEngine), é necessário criar um módulo nativo.

```typescript
import { trigger } from 'react-native-haptic-feedback';
trigger('impactMedium', { enableVibrateFallback: true });
```

### Bateria e modo de baixo consumo

O react-native-device-info fornece hooks para monitorar estado da bateria em tempo real:

```typescript
import { useBatteryLevel, usePowerState } from 'react-native-device-info';

const nivel = useBatteryLevel(); // 0.759
const estado = usePowerState(); // { batteryLevel, batteryState, lowPowerMode }
```

**Limitação crítica**: Apps não podem **ativar ou desativar** o Low Power Mode programaticamente – apenas detectar seu estado.

### Acessibilidade

O React Native inclui a API **AccessibilityInfo** para detectar configurações de acessibilidade:

```typescript
const screenReader = await AccessibilityInfo.isScreenReaderEnabled();
const reduceMotion = await AccessibilityInfo.isReduceMotionEnabled();
const boldText = await AccessibilityInfo.isBoldTextEnabled();
```

Apps não podem habilitar/desabilitar VoiceOver ou outras funcionalidades de acessibilidade – apenas detectá-las.

---

## Categoria 2: Conectividade

### Monitoramento de rede

O **@react-native-community/netinfo** (v11.4.1, ~750k downloads semanais) é a solução padrão para detectar conectividade:

```typescript
import NetInfo, { useNetInfo } from '@react-native-community/netinfo';

const netInfo = useNetInfo();
console.log('Tipo:', netInfo.type); // wifi, cellular, none
console.log('Conectado:', netInfo.isConnected);
console.log('SSID:', netInfo.details?.ssid); // requer permissão location no iOS 13+
console.log('Geração celular:', netInfo.details?.cellularGeneration); // 4g, 5g
```

**Info.plist**: Para acessar SSID do WiFi, adicione o entitlement `com.apple.developer.networking.wifi-info`.

### WiFi

O **react-native-wifi-reborn** (v4.13.6) permite conectar a redes WiFi usando `NEHotspotConfiguration` (iOS 11+):

```typescript
import WifiManager from 'react-native-wifi-reborn';

await WifiManager.connectToProtectedSSID('MinhaRede', 'senha123', false, false);
const ssidAtual = await WifiManager.getCurrentWifiSSID();
```

**Limitações**: iOS **não permite escanear redes disponíveis** (restrição da Apple), não fornece intensidade do sinal, e a conexão persiste apenas enquanto o app está em foreground.

### Bluetooth Low Energy

O **react-native-ble-plx** (v3.5.0, 3k stars) é a biblioteca mais completa para BLE:

```typescript
import { BleManager } from 'react-native-ble-plx';

const manager = new BleManager();

manager.startDeviceScan(null, null, (error, device) => {
  if (device?.name?.includes('MeuDispositivo')) {
    manager.stopDeviceScan();
    conectar(device);
  }
});
```

**Info.plist**: Adicione `NSBluetoothAlwaysUsageDescription`. Para modo background, habilite "Uses Bluetooth LE accessories" nas Background Modes.

**Limitações**: Suporta apenas BLE (não Bluetooth Classic), não permite criar bonds/pareamentos programaticamente, e funciona apenas como central (não peripheral).

### AirDrop

**Não é possível** controlar AirDrop programaticamente. Apps podem apenas usar `UIActivityViewController` (via `Share` do React Native) para oferecer compartilhamento, onde AirDrop aparece como opção.

---

## Categoria 3: Casa Inteligente (HomeKit)

### Status: Requer módulo nativo personalizado

Não existe biblioteca React Native **ativamente mantida** para HomeKit. A biblioteca `react-native-homekit` está abandonada há mais de 4 anos e oferece funcionalidade mínima.

**Solução recomendada**: Criar módulo nativo em Swift seguindo o exemplo do tutorial BravoLT:

```swift
// HomeKitModule.swift
import HomeKit

@objc(HomeKitModule)
class HomeKitModule: RCTEventEmitter {
  var homeManager = HMHomeManager()
  
  @objc func addAndSetupAccessories(_ resolve: @escaping RCTPromiseResolveBlock,
                                     reject: @escaping RCTPromiseRejectBlock) {
    homeManager.homes[0].addAndSetupAccessories { error in
      if let error = error { reject("error", error.localizedDescription, error) }
      else { resolve("") }
    }
  }
}
```

**Configuração**: Adicione `NSHomeKitUsageDescription` ao Info.plist e habilite a capability HomeKit no Xcode. Funciona apenas em dispositivo físico.

### Protocolo Matter

A biblioteca `@matter/react-native` (v0.11.0-alpha) está em estado **experimental** e não é recomendada para produção. O processo de commissioning não foi testado com sucesso pela comunidade.

---

## Categoria 4: Saúde e Bem-estar (HealthKit)

### Biblioteca recomendada: @kingstinct/react-native-healthkit

Esta biblioteca (v12.1.2, dezembro 2025) oferece a API mais moderna com suporte completo a TypeScript, hooks React, e usa **Nitro Modules** para melhor performance.

```typescript
import { 
  useHealthkitAuthorization,
  useMostRecentQuantitySample,
  saveQuantitySample 
} from '@kingstinct/react-native-healthkit';

// Autorização
const [status, requestAuth] = useHealthkitAuthorization({
  toRead: ['HKQuantityTypeIdentifierHeartRate', 'HKQuantityTypeIdentifierStepCount'],
  toShare: ['HKQuantityTypeIdentifierStepCount']
});

// Leitura com hooks (atualização em tempo real)
const heartRate = useMostRecentQuantitySample('HKQuantityTypeIdentifierHeartRate');
const steps = useMostRecentQuantitySample('HKQuantityTypeIdentifierStepCount');

// Gravação
await saveQuantitySample('HKQuantityTypeIdentifierStepCount', 'count', 1000);
```

**Info.plist obrigatório**:
```xml
<key>NSHealthShareUsageDescription</key>
<string>Precisamos ler seus dados de saúde</string>
<key>NSHealthUpdateUsageDescription</key>
<string>Precisamos gravar dados de saúde</string>
```

**Xcode**: Adicione a capability HealthKit em Signing & Capabilities.

**Tipos de dados suportados**: 100+ tipos de quantidade (passos, frequência cardíaca, glicose, etc.), 63 tipos de categoria (sono, mindfulness), 75+ tipos de treino.

### Alternativa: react-native-health

Biblioteca mais estabelecida (1.1k stars, ~8.2k downloads semanais) mas com API baseada em callbacks:

```typescript
import AppleHealthKit from 'react-native-health';

AppleHealthKit.initHealthKit(permissions, (error) => {
  if (error) return;
  
  AppleHealthKit.getStepCount({ date: new Date().toISOString() }, (err, results) => {
    console.log(`Passos hoje: ${results.value}`);
  });
});
```

**Registros clínicos**: Ambas as bibliotecas suportam Clinical Records, mas requer aprovação especial da Apple.

---

## Categoria 5: Comunicação

### CallKit (VoIP)

O **react-native-callkeep** (v4.3.16) é a única opção robusta para integração com CallKit:

```typescript
import RNCallKeep from 'react-native-callkeep';

RNCallKeep.setup({ ios: { appName: 'MeuApp', supportsVideo: true } });

// Exibir chamada recebida
RNCallKeep.displayIncomingCall(uuid, numero, nomeContato, 'generic', true);

// Eventos
RNCallKeep.addEventListener('answerCall', ({ callUUID }) => {
  // Atender chamada
});
```

**Configuração crítica**: No Info.plist, adicione `UIBackgroundModes` com `voip` e `audio`. No iOS 13+, apps **devem** reportar pushes VoIP ao CallKit imediatamente ou serão terminados.

### Contatos

O **react-native-contacts** (v8.0.7, ~52k downloads semanais) oferece CRUD completo:

```typescript
import Contacts from 'react-native-contacts';

await Contacts.requestPermission();
const contatos = await Contacts.getAll();

await Contacts.addContact({
  givenName: 'João',
  familyName: 'Silva',
  phoneNumbers: [{ label: 'mobile', number: '11999999999' }],
});
```

**Limitação iOS 14+**: O modo "Acesso Limitado" permite que usuários selecionem apenas alguns contatos para compartilhar.

### Notificações locais

O **@notifee/react-native** (v9.0.0, by Invertase) é a solução mais completa:

```typescript
import notifee, { TriggerType, TimestampTrigger } from '@notifee/react-native';

await notifee.displayNotification({
  title: 'Reunião',
  body: 'Começa em 10 minutos',
  ios: {
    sound: 'default',
    interruptionLevel: 'timeSensitive', // Bypass Focus Mode no iOS 15+
  },
});

// Agendar notificação
const trigger: TimestampTrigger = {
  type: TriggerType.TIMESTAMP,
  timestamp: Date.now() + 60000,
};
await notifee.createTriggerNotification(notification, trigger);
```

### Push Notifications (APNs)

Use **@react-native-community/push-notification-ios** para APNs nativo:

```typescript
import PushNotificationIOS from '@react-native-community/push-notification-ios';

await PushNotificationIOS.requestPermissions({ alert: true, badge: true, sound: true });

PushNotificationIOS.addEventListener('register', (deviceToken) => {
  console.log('Token:', deviceToken);
});
```

**Xcode**: Habilite Push Notifications e Background Modes → Remote notifications.

### SMS

**Limitação fundamental**: iOS **não permite** enviar SMS programaticamente em background ou ler mensagens. A única opção é abrir o compositor de SMS pré-preenchido:

```typescript
import SendSMS from 'react-native-sms';

SendSMS.send({
  body: 'Olá!',
  recipients: ['11999999999'],
}, (completed, cancelled, error) => {});
```

---

## Categoria 6: Automação e Atalhos

### Siri Shortcuts

O **react-native-siri-shortcut** permite doar atalhos baseados em NSUserActivity:

```typescript
import { donateShortcut, SiriShortcutsEvent } from 'react-native-siri-shortcut';

donateShortcut({
  activityType: 'com.meuapp.pedirCafe',
  title: 'Pedir Café',
  suggestedInvocationPhrase: 'Pedir meu café',
  isEligibleForSearch: true,
  isEligibleForPrediction: true,
});

SiriShortcutsEvent.addListener('SiriShortcutListener', ({ activityType }) => {
  // Executar ação do atalho
});
```

**Info.plist**: Adicione `NSSiriUsageDescription`.

### App Intents (iOS 16+)

Não existe biblioteca React Native para App Intents. É necessário implementar em Swift nativo e comunicar com o React Native via deep links ou App Groups.

### Spotlight Search

O **react-native-spotlight-search** permite indexar conteúdo para busca do sistema:

```typescript
import SpotlightSearch from 'react-native-spotlight-search';

await SpotlightSearch.indexItems([{
  title: 'Notas da Reunião',
  contentDescription: 'Reunião de equipe',
  uniqueIdentifier: 'nota-123',
  keywords: ['reunião', 'equipe', 'notas'],
}]);
```

### Widgets

**Limitação crítica**: Widgets iOS **devem** ser escritos em Swift/SwiftUI. React Native não pode rodar em widget extensions devido ao limite de 16MB de memória.

A biblioteca **react-native-widgetkit** serve para comunicação entre o app React Native e o widget nativo:

```typescript
import { reloadAllTimelines, setItem } from 'react-native-widgetkit';

// Compartilhar dados com widget via App Groups
await setItem('widgetData', JSON.stringify({ count: 5 }), 'group.com.meuapp');
await reloadAllTimelines();
```

### Background Fetch

O **react-native-background-fetch** (by Transistor Software) usa BGTaskScheduler do iOS 13+:

```typescript
import BackgroundFetch from 'react-native-background-fetch';

await BackgroundFetch.configure({
  minimumFetchInterval: 15, // mínimo 15 minutos
  stopOnTerminate: false,
}, async (taskId) => {
  await sincronizarDados();
  BackgroundFetch.finish(taskId);
});
```

**Info.plist**: Adicione `fetch` e `processing` em `UIBackgroundModes`.

**Limitações iOS**: O intervalo mínimo é 15 minutos (mas iOS pode estender para horas), não há garantia de execução, e o sistema para de agendar se o usuário não abre o app por muito tempo.

---

## Categoria 7: Mídia e Conteúdo

### Câmera

O **react-native-vision-camera** (v4+, 7k stars) é o padrão atual, substituindo o deprecated react-native-camera:

```typescript
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';

const device = useCameraDevice('back');
const { hasPermission, requestPermission } = useCameraPermission();
const cameraRef = useRef<Camera>(null);

const tirarFoto = async () => {
  const foto = await cameraRef.current?.takePhoto({ qualityPrioritization: 'quality' });
  console.log('Caminho:', foto?.path);
};

const gravarVideo = () => {
  cameraRef.current?.startRecording({
    onRecordingFinished: (video) => console.log('Vídeo:', video.path),
    onRecordingError: console.error,
  });
};
```

**Info.plist**: `NSCameraUsageDescription`, `NSMicrophoneUsageDescription`.

### Galeria de fotos

O **@react-native-camera-roll/camera-roll** (v7.10.2) oferece acesso à biblioteca de fotos:

```typescript
import { CameraRoll } from '@react-native-camera-roll/camera-roll';

const fotos = await CameraRoll.getPhotos({ first: 20, assetType: 'Photos' });
await CameraRoll.save(uri, { type: 'photo', album: 'MeuApp' });
```

### Áudio profissional

O **react-native-track-player** (3.4k stars) é essencial para apps de música/podcast com suporte a background audio:

```typescript
import TrackPlayer, { useProgress, Capability } from 'react-native-track-player';

await TrackPlayer.setupPlayer();
await TrackPlayer.updateOptions({
  capabilities: [Capability.Play, Capability.Pause, Capability.SkipToNext],
});

await TrackPlayer.add([{
  id: '1',
  url: 'https://exemplo.com/musica.mp3',
  title: 'Minha Música',
  artist: 'Artista',
  artwork: 'https://exemplo.com/capa.jpg',
}]);

await TrackPlayer.play();
```

**Info.plist**: Adicione `audio` em `UIBackgroundModes` para reprodução em background.

### Gravação de áudio

Use **react-native-nitro-sound** (sucessor do react-native-audio-recorder-player):

```typescript
import AudioRecorderPlayer from 'react-native-nitro-sound';

const recorder = new AudioRecorderPlayer();

const uri = await recorder.startRecorder('gravacao.m4a', {
  AVEncoderAudioQualityKeyIOS: AVEncoderAudioQualityIOSType.high,
});

await recorder.stopRecorder();
await recorder.startPlayer(uri);
```

### Scanner de documentos

O **react-native-document-scanner-plugin** (v2.0.4) usa VNDocumentCameraViewController do iOS:

```typescript
import DocumentScanner from 'react-native-document-scanner-plugin';

const { scannedImages } = await DocumentScanner.scanDocument({
  maxNumDocuments: 5,
  quality: 0.9,
});
```

---

## Categoria 8: Localização e Navegação

### Localização básica

O **react-native-geolocation-service** (1.7k stars) oferece acesso ao Core Location:

```typescript
import Geolocation from 'react-native-geolocation-service';

Geolocation.getCurrentPosition(
  (position) => {
    console.log(position.coords.latitude, position.coords.longitude);
    console.log('Precisão:', position.coords.accuracy);
  },
  (error) => console.log(error),
  { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
);
```

### Geofencing e localização em background

O **react-native-background-geolocation** (Transistor Software) é a solução enterprise para rastreamento robusto:

```typescript
import BackgroundGeolocation from 'react-native-background-geolocation';

// Configurar geofence
await BackgroundGeolocation.addGeofence({
  identifier: 'Casa',
  radius: 200,
  latitude: -23.5505,
  longitude: -46.6333,
  notifyOnEntry: true,
  notifyOnExit: true,
});

BackgroundGeolocation.onGeofence((event) => {
  console.log('[geofence]', event.identifier, event.action);
});

await BackgroundGeolocation.ready({
  desiredAccuracy: BackgroundGeolocation.DESIRED_ACCURACY_HIGH,
  distanceFilter: 10,
  stopOnTerminate: false,
});

await BackgroundGeolocation.start();
```

**Info.plist**: `NSLocationAlwaysAndWhenInUseUsageDescription`, `UIBackgroundModes` com `location`.

**Licenciamento**: Gratuito para iOS, licença paga ($299/app) para Android em produção.

### Mapas

O **react-native-maps** (14k stars) suporta Apple Maps e Google Maps:

```typescript
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';

// Apple Maps (padrão, sem API key)
<MapView style={{ flex: 1 }} showsUserLocation={true}>
  <Marker coordinate={{ latitude: -23.5505, longitude: -46.6333 }} />
</MapView>

// Google Maps (requer API key)
<MapView provider={PROVIDER_GOOGLE} ... />
```

### Navegação turn-by-turn

O **@pawan-pk/react-native-mapbox-navigation** oferece navegação completa com Mapbox:

```typescript
import MapboxNavigation from '@pawan-pk/react-native-mapbox-navigation';

<MapboxNavigation
  startOrigin={{ latitude: -23.55, longitude: -46.63 }}
  destination={{ latitude: -23.58, longitude: -46.66 }}
  onArrive={() => console.log('Chegou!')}
/>
```

### iBeacon

O **react-native-beacons-manager** detecta beacons BLE:

```typescript
import Beacons from 'react-native-beacons-manager';

Beacons.startRangingBeaconsInRegion({
  identifier: 'Loja',
  uuid: 'B9407F30-F5F8-466E-AFF9-25556B57FE6D',
});

DeviceEventEmitter.addListener('beaconsDidRange', (data) => {
  console.log('Beacons:', data.beacons);
});
```

---

## Categoria 9: Controles financeiros e identidade

### Apple Pay

O **@stripe/stripe-react-native** integra Apple Pay via Stripe:

```typescript
import { StripeProvider, isPlatformPaySupported, confirmPlatformPayPayment } from '@stripe/stripe-react-native';

// Verificar suporte
const suportado = await isPlatformPaySupported();

// Processar pagamento
const { error } = await confirmPlatformPayPayment(clientSecret, {
  applePay: {
    cartItems: [{ label: 'Total', amount: '10.99' }],
    merchantCountryCode: 'BR',
    currencyCode: 'BRL',
  },
});
```

**Configuração**: Registre Merchant ID no Apple Developer Portal, habilite Apple Pay no Xcode, e configure certificado no Dashboard Stripe.

### In-App Purchases

O **react-native-iap** (v14.7.1) suporta StoreKit 2:

```typescript
import { useIAP } from 'react-native-iap';

const { connected, products, fetchProducts, requestPurchase, finishTransaction } = useIAP({
  onPurchaseSuccess: async (purchase) => {
    await finishTransaction({ purchase, isConsumable: true });
  },
});

useEffect(() => {
  if (connected) fetchProducts({ skus: ['premium_monthly'] });
}, [connected]);

await requestPurchase({ request: { apple: { sku: 'premium_monthly' } } });
```

**Alternativa**: **react-native-purchases** (RevenueCat) oferece backend gerenciado para validação de recibos.

### Sign in with Apple

O **@invertase/react-native-apple-authentication** implementa ASAuthorizationController:

```typescript
import appleAuth, { AppleButton } from '@invertase/react-native-apple-authentication';

const onLogin = async () => {
  const response = await appleAuth.performRequest({
    requestedOperation: appleAuth.Operation.LOGIN,
    requestedScopes: [appleAuth.Scope.FULL_NAME, appleAuth.Scope.EMAIL],
  });
  
  const { identityToken, user, email, fullName } = response;
  // Enviar token para backend
};

<AppleButton buttonStyle={AppleButton.Style.BLACK} onPress={onLogin} />
```

**Importante**: Apple só retorna nome/email no primeiro login.

### Keychain e biometria

O **react-native-keychain** oferece armazenamento seguro com proteção biométrica:

```typescript
import * as Keychain from 'react-native-keychain';

// Salvar com proteção Face ID/Touch ID
await Keychain.setGenericPassword('usuario', 'senha', {
  accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY,
});

// Recuperar com prompt biométrico
const credentials = await Keychain.getGenericPassword({
  authenticationPrompt: { title: 'Autentique para acessar' },
});
```

---

## Categoria 10: Produtividade e dados

### Calendário

O **react-native-calendar-events** (v2.2.0) oferece CRUD completo para EventKit:

```typescript
import RNCalendarEvents from 'react-native-calendar-events';

await RNCalendarEvents.requestPermissions();

const eventos = await RNCalendarEvents.fetchAllEvents(
  '2024-01-01T00:00:00.000Z',
  '2024-12-31T23:59:59.000Z'
);

await RNCalendarEvents.saveEvent('Reunião', {
  startDate: '2024-06-15T10:00:00.000Z',
  endDate: '2024-06-15T11:00:00.000Z',
  alarms: [{ date: -15 }], // 15 minutos antes
});
```

**Info.plist**: `NSCalendarsUsageDescription`, `NSCalendarsFullAccessUsageDescription` (iOS 17+).

### Document Picker

O **@react-native-documents/picker** (v12.0.0) acessa arquivos e iCloud Drive:

```typescript
import { pick, types } from '@react-native-documents/picker';

const resultado = await pick({ type: [types.pdf, types.images] });
console.log('URI:', resultado[0].uri);
console.log('Nome:', resultado[0].name);
```

### Armazenamento local

- **AsyncStorage**: `@react-native-async-storage/async-storage` para key-value simples
- **SQLite**: `react-native-sqlite-storage` para banco relacional
- **Realm**: `realm` + `@realm/react` para objeto-documento (sync deprecated em 2025)

### iCloud

O **react-native-cloud-store** permite acessar o container iCloud do app:

```typescript
import { isICloudAvailable, writeFile, readFile } from 'react-native-cloud-store';

const disponivel = await isICloudAvailable();
await writeFile(`${defaultICloudContainerPath}/notas.txt`, 'Conteúdo');
```

### Clipboard

O **@react-native-clipboard/clipboard** acessa a área de transferência:

```typescript
import Clipboard from '@react-native-clipboard/clipboard';

Clipboard.setString('Texto copiado');
const texto = await Clipboard.getString();
```

---

## Desenvolvimento de módulos nativos

### Arquitetura Legacy (Objective-C)

```objectivec
// MeuModulo.m
#import <React/RCTBridgeModule.h>

@interface MeuModulo : NSObject <RCTBridgeModule>
@end

@implementation MeuModulo

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(minhaFuncao:(NSString *)param
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject) {
  resolve(@"Sucesso");
}

@end
```

### Arquitetura Legacy (Swift)

```swift
// MeuModulo.swift
@objc(MeuModulo)
class MeuModulo: NSObject {
  
  @objc static func requiresMainQueueSetup() -> Bool { false }
  
  @objc func minhaFuncao(_ param: String, 
                         resolver resolve: @escaping RCTPromiseResolveBlock,
                         rejecter reject: @escaping RCTPromiseRejectBlock) {
    resolve("Sucesso")
  }
}
```

```objectivec
// MeuModuloBridge.m
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(MeuModulo, NSObject)
RCT_EXTERN_METHOD(minhaFuncao:(NSString *)param
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)
@end
```

### Nova Arquitetura (Turbo Modules)

Spec TypeScript em `specs/NativeMeuModulo.ts`:

```typescript
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  minhaFuncao(param: string): Promise<string>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeMeuModulo');
```

O Codegen gera automaticamente os bindings quando você executa `pod install`.

---

## O que NÃO é possível acessar

### Bloqueios absolutos do iOS

Estas funcionalidades são **completamente bloqueadas** pela Apple para todos os apps de terceiros:

- **Ler SMS/iMessage**: Não existe API no iOS
- **Gravar chamadas telefônicas**: Bloqueado no nível do sistema
- **Acessar histórico de chamadas**: Não existe API
- **Ligar/desligar WiFi, Bluetooth ou dados móveis**: Apenas configurações de sistema
- **Acessar dados de outros apps**: Sandboxing impede
- **Controlar AirDrop**: Sem API disponível
- **Acessar Safari, Notas ou Mail de outros apps**: Sandboxed
- **Modificar interface do sistema**: Causa rejeição na App Store
- **Executar continuamente em background**: iOS suspende apps

### Entitlements que requerem aprovação da Apple

- **CarPlay**: Áudio, navegação, comunicação
- **Family Controls/Screen Time**: Apps de controle parental
- **Network Extensions**: VPNs e filtros de conteúdo
- **Clinical Records (HealthKit)**: Dados médicos detalhados

### Privacy Manifest (iOS 17+)

Desde maio de 2024, apps devem declarar em `PrivacyInfo.xcprivacy` o uso de:

- UserDefaults (`NSPrivacyAccessedAPICategoryUserDefaults`)
- APIs de timestamp de arquivos
- APIs de espaço em disco
- APIs de tempo de boot do sistema

React Native usa UserDefaults internamente, então todos os apps precisam incluir esta declaração.

---

## Tabela de referência rápida

| Categoria | Biblioteca Principal | TypeScript | Mantida |
|-----------|---------------------|------------|---------|
| Info Dispositivo | react-native-device-info | ✅ | ✅ |
| Rede/WiFi | @react-native-community/netinfo | ✅ | ✅ |
| Bluetooth BLE | react-native-ble-plx | ✅ | ✅ |
| HomeKit | Módulo nativo customizado | - | - |
| HealthKit | @kingstinct/react-native-healthkit | ✅ | ✅ |
| CallKit | react-native-callkeep | ✅ | ⚠️ |
| Contatos | react-native-contacts | ✅ | ✅ |
| Notificações | @notifee/react-native | ✅ | ✅ |
| Siri Shortcuts | react-native-siri-shortcut | ✅ | ✅ |
| Câmera | react-native-vision-camera | ✅ | ✅ |
| Galeria | @react-native-camera-roll/camera-roll | ✅ | ✅ |
| Áudio | react-native-track-player | ✅ | ✅ |
| Mapas | react-native-maps | ✅ | ✅ |
| Localização BG | react-native-background-geolocation | ✅ | ✅ |
| Apple Pay | @stripe/stripe-react-native | ✅ | ✅ |
| IAP | react-native-iap | ✅ | ✅ |
| Sign in Apple | @invertase/react-native-apple-authentication | ✅ | ✅ |
| Keychain | react-native-keychain | ✅ | ✅ |
| Calendário | react-native-calendar-events | ✅ | ✅ |
| Files | @react-native-documents/picker | ✅ | ✅ |

Este guia cobre as principais capacidades acessíveis via React Native CLI bare workflow. Para funcionalidades não cobertas por bibliotecas existentes, a criação de módulos nativos personalizados em Swift ou Objective-C permite acessar qualquer API pública do iOS.