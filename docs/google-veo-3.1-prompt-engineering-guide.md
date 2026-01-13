# Guia Definitivo de Prompt Engineering para Google VEO 3.1

O **Google VEO 3.1**, lançado em outubro de 2025, representa o estado da arte em geração de vídeo por IA, oferecendo áudio nativo, resolução até 1080p e controle cinematográfico avançado. Este guia sintetiza documentação oficial do Google/DeepMind, técnicas validadas pela comunidade e descobertas de power users para criar um manual completo de engenharia de prompts—com foco especial em geração de vídeo em **primeira pessoa (POV)** e técnicas de **chromakey** para workflows de composição.

A descoberta mais crítica documentada aqui: a sintaxe **"(thats where the camera is)"** posiciona a câmera com precisão dramática, transformando resultados genéricos em shots profissionalmente enquadrados. Combinada com a fórmula oficial de cinco partes do Google e as técnicas de green screen da comunidade, esta metodologia permite aos criadores gerar footage verdadeiramente compositable.

---

## 1. Capacidades e especificações técnicas do modelo

O VEO 3.1 opera através de APIs (Gemini API e Vertex AI), Google Flow e o app Gemini. Cada plataforma oferece acesso às mesmas capacidades core, mas com interfaces distintas.

### Especificações confirmadas oficialmente

| Parâmetro | VEO 3.1 / VEO 3.1 Fast |
|-----------|------------------------|
| **Resolução** | 720p e 1080p (1080p apenas para 8 segundos) |
| **Frame rate** | 24 fps |
| **Aspect ratios** | 16:9 (landscape), 9:16 (portrait) |
| **Duração** | 4, 6 ou 8 segundos por clip |
| **Extensão máxima** | Até **148 segundos** via extensões encadeadas (20x) |
| **Áudio nativo** | Diálogos, SFX, ambient noise integrados |

Os identificadores de modelo para a API são `veo-3.1-generate-preview` (Gemini API) e `veo-3.1-generate-001` (Vertex AI). O modelo inclui watermarking SynthID invisível em todas as gerações para rastreabilidade.

### Recursos exclusivos do VEO 3.1

O VEO 3.1 introduziu três capacidades transformadoras não disponíveis em versões anteriores: **Ingredients to Video** (até 3 imagens de referência para consistência de personagem), **First and Last Frame** (interpolação entre dois frames com áudio), e **Scene Extension** (extensão de cenas mantendo continuidade). Estas features operam apenas em clips de 8 segundos e aspect ratio 16:9, uma limitação técnica importante para planejar workflows.

---

## 2. Arquitetura fundamental do prompt

A documentação oficial do Google Cloud estabelece uma fórmula de cinco componentes que a comunidade expandiu para sete partes para máxima eficácia.

### Fórmula oficial do Google (5 partes)

```
[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
```

Esta estrutura determina como o modelo prioriza informação. **VEO pesa as primeiras palavras mais fortemente**—o shot type e subject devem vir primeiro, seguidos por ação, depois estilo e câmera.

### Fórmula expandida da comunidade (7 partes)

Usuários avançados convergeram em uma estrutura mais detalhada:

```
[Shot Composition] + [Subject] + [Action] + [Setting] + [Aesthetics] + [Audio] + [Negative Prompts]
```

O comprimento ideal fica entre **100-150 palavras** ou 3-6 sentenças. Prompts muito curtos geram output genérico; prompts excessivamente longos (500+ palavras) sofrem ignorância parcial, onde o modelo descarta instruções intermediárias.

### Princípios de priorização

Mantenha cada prompt focado em **uma ação principal por clip de 8 segundos**. O modelo interpreta estrutura literalmente, então elementos mencionados primeiro recebem peso maior. Para diálogos, use sintaxe com dois-pontos (`Character says: "dialogue"`) ao invés de aspas diretas para evitar legendas automáticas—esta técnica tem **95% de taxa de sucesso** segundo relatórios da comunidade.

---

## 3. Domínio de geração POV em primeira pessoa

A geração de vídeo em primeira pessoa requer sintaxe específica que vai além de termos genéricos. A descoberta mais importante da comunidade é a frase **"(thats where the camera is)"**, que posiciona a câmera com precisão dramática.

### 3.1 Trigger words confirmados para POV

Terminologia oficial do Google inclui `"POV shot"`, `"point-of-view shot"`, e `"eye-level perspective"`. A comunidade expandiu com frases de maior eficácia:

| Frase | Eficácia | Fonte |
|-------|----------|-------|
| `"first-person POV"` | ✅ Alta | Documentação oficial |
| `"POV shot from [position]"` | ✅ Alta | Google Cloud Guide |
| `"(thats where the camera is)"` | ✅ **Crítica** | GitHub snubroot, Superprompt |
| `"selfie video of"` | ✅ Alta | Community consensus |
| `"handheld POV"` | ✅ Alta | Skywork.ai |
| `"Phone camera POV"` | ✅ Alta | GodOfPrompt.ai |

A sintaxe de posicionamento é essencial. Compare:

```
❌ Genérico: "POV camera of chef cooking"
✅ Preciso: "Chef is holding a selfie stick (thats where the camera is) while cooking"
```

### 3.2 Vocabulário de movimento de câmera

Para walking POV, combine triggers com descritores de movimento específicos:

**Movimento básico:**
- `"walking forward"` / `"camera moves forward at walking pace"`
- `"running POV"` / `"camera sprints forward"`
- `"slight head bob"` / `"natural head movement"`
- `"occasionally looking into the camera before [action]"`

**Estabilização:**
- `"smooth gimbal movement"` — estabilização profissional
- `"handheld with subtle shake"` — autenticidade documental
- `"gentle micro-sway"` — balanço humano sutil

Evite instruções de movimento conflitantes no mesmo prompt. Comandos de câmera simples como `"slow pan"` ou `"gentle dolly-in"` funcionam melhor que instruções compostas.

### 3.3 Interação ambiental e visibilidade corporal

O VEO não inclui automaticamente partes do corpo em shots POV. Você deve solicitar explicitamente:

```
"His long, powerful arm is clearly visible in the frame"
"The cyclist's gloved hands grip the handlebars"
"Your hands enter frame from below"
```

Para áudio POV-apropriado, especifique sons da perspectiva do personagem: `"Audio: footsteps from the walker's perspective, breathing sounds, wind past ears"`.

### 3.4 Falhas comuns em POV e correções

| Problema | Causa | Solução |
|----------|-------|---------|
| VEO gera terceira pessoa | Termos genéricos sem posicionamento | Sempre inclua `"(thats where the camera is)"` |
| Movimento robótico/tremido | Instruções de movimento conflitantes | Use `"gentle sway"` ao invés de `"handheld"` |
| Partes do corpo ausentes | Falta de especificação explícita | Descreva braços/mãos visíveis no frame |
| Drift de perspectiva | Âncoras POV insuficientes | Use imagens de referência com first/last frame |
| Legendas indesejadas | Sintaxe de diálogo incorreta | Use dois-pontos + `"no subtitles"` |

### 3.5 Templates de prompt POV prontos para uso

**Template 1: Walking POV urbano**
```
Point-of-view handheld shot walking through busy city street during rush hour, 
camera moves forward as pedestrians part around viewpoint, slight head bob, 
natural human movement, dynamic urban energy with blurred motion of passing people.
Audio: city traffic sounds, footsteps, crowd chatter.
Style: documentary, natural daylight.
Technical: no subtitles, no third-person view.
```

**Template 2: Vlog selfie style**
```
A selfie video of [CHARACTER DESCRIPTION], holding a selfie stick (thats where the camera is).
[His/Her] arm is clearly visible in the frame, occasionally looking into the camera 
before [ACTION]. [ENVIRONMENT DESCRIPTION]. The image is slightly grainy, looks very film-like.
[Character] speaks in a [ACCENT] accent and says: "[DIALOGUE]"
Audio: ambient environment sounds. No subtitles.
```

**Template 3: Ciclismo/esporte POV**
```
A first-person POV video of a mountain cyclist riding along [TERRAIN].
The cyclist's gloved hands grip the handlebars tightly as the camera shakes 
slightly with each pedal stroke. Camera moves forward at a steady but tense pace.
Audio: wind, bike chain, tires on surface, breathing.
Style: GoPro aesthetic, action camera feel.
```

**Template 4: Despertar/ambiente íntimo**
```
From a first-person point of view, your vision gradually clears, as if waking from sleep. 
Morning sunlight filters gently through pale curtains, casting a soft golden hue.
Camera slowly pushes in toward [FOCAL POINT]. Natural head movement, slight focus adjustment.
Audio: quiet morning ambiance, distant birds.
```

**Template 5: POV com posicionamento preciso**
```
POV shot from the camera positioned at eye level (thats where the camera is) 
as [CHARACTER] explains [TOPIC]. [SCENE DESCRIPTION].
Close-up shot with camera positioned at [HEIGHT] level (thats where the camera is) 
as [ACTION]. Maintaining first-person perspective throughout.
Audio: [SPECIFIC SOUNDS]. No subtitles, no captions.
```

---

## 4. Controle de chromakey e composição

O VEO 3.1 **não possui geração nativa de chromakey** como feature built-in, mas técnicas descobertas pela comunidade permitem workflows eficazes de green screen para composição VFX.

### 4.1 Requisição direta de green/blue screen

A frase mais confiável para backgrounds keyáveis é **"on a plain solid green background"**. Variações eficazes incluem:

- `"against a green screen backdrop"`
- `"uniform green chroma key background"`
- `"clean studio green screen behind subject"`
- `"on a plain solid white background"` (para keying white)

### 4.2 Controle de iluminação para keys limpas

Iluminação é crítica para footage compositable. Use estas frases para evitar sombras problemáticas:

| Tipo de luz | Frase de prompt | Propósito |
|-------------|-----------------|-----------|
| Flat/even | `"bright, even, shadowless studio lighting"` | Key limpa, sem gradientes |
| Three-point | `"three-point lighting with warm key light"` | Separação profissional |
| Soft key | `"soft key light from camera-left; negative fill on right"` | Reduz spill |
| High-key | `"high-key, professional studio lighting setup"` | Sombras mínimas |

Para preservar detalhes de cabelo, especifique: `"soft key 60%, fill 30%, skin-tone friendly grade, avoid green contamination"`.

### 4.3 Técnica de isolamento de sujeito

A técnica mais poderosa para composição usa **Image-to-Video com substituição de background**:

1. Crie imagem do personagem contra green screen
2. No editor de imagem, coloque o background desejado em um canto
3. Upload esta imagem composta para VEO
4. Prompt: `"Replace the green screen with the background image provided"`

Segundo testes da Arsturn, resultados são "shockingly good"—exemplos incluem pessoas em treadmills green screen transportadas seamlessly para paisagens marcianas.

### 4.4 Otimização de qualidade de borda

Para bordas limpas que facilitam keying em pós-produção:

```
"rim lighting to separate subject from background"
"back rim light at 25% to create edge separation around hair"
"sharp subject edges, no shadows on background"
```

**Negative prompts para keying:**
- `"no harsh shadows"`
- `"no green contamination"`
- `"no colored spill on subject"`
- `"no background variations"`

### 4.5 Templates de prompt chromakey prontos para uso

**Template 1: Talking head para keying**
```
Medium close-up of [CHARACTER DESCRIPTION], looking directly at camera.
On a plain solid green background with professional studio lighting.
Soft key light from camera-left, even fill, rim lighting to separate subject.
Static camera on tripod. [Character] says: "[DIALOGUE]" No subtitles.
```

**Template 2: Full body para composição**
```
Full-body shot of [CHARACTER] in [CLOTHING], performing [ACTION].
Against a uniform bright green screen backdrop, evenly lit.
Clean studio lighting, no shadows on background, sharp subject edges.
[CAMERA MOVEMENT], [DURATION] seconds. No audio.
```

**Template 3: Produto isolado**
```
Close-up of [PRODUCT] rotating slowly on a transparent display stand.
Plain solid white background, infinite white studio backdrop.
High-key even lighting, soft shadows beneath product only.
360-degree slow rotation, 8 seconds, clean edges.
```

**Template 4: Substituição de background**
```
[Upload image: character on green screen + desired background in corner]
Replace the green screen background with the background image provided.
Maintain character position and lighting. Smooth transition, 6 seconds.
Character walks forward confidently, maintaining position center frame.
```

**Template 5: Múltiplos sujeitos para keying**
```
[NUMBER] people standing [ARRANGEMENT] in [ATTIRE].
Plain solid green chroma key background, evenly lit backdrop.
Professional three-point lighting setup, no colored spill.
Medium wide shot, static camera, 8 seconds.
```

**Template 6: Dança/performance para composição**
```
Full body shot of dancer in flowing [COLOR] dress mid-movement.
On perfectly even bright green chroma key screen, no wrinkles visible.
Flat shadowless studio lighting, 5600K daylight balanced.
Rim lighting to separate subject from background.
Camera: wide static shot, 6 seconds.
```

**Template 7: Portrait com detalhes de cabelo**
```
Close-up portrait of person with [HAIR DESCRIPTION] against solid green background.
Soft diffused lighting from large softbox, even fill to minimize shadows.
Back rim light at 25% to create edge separation around hair.
Static camera, shallow depth of field on face, 4 seconds.
```

---

## 5. Técnicas avançadas

### Timestamp prompting para sequências multi-shot

O Google oficialmente suporta prompting baseado em timestamps para controle de shots sequenciais:

```
[00:00-00:02] Medium shot from behind explorer surveying ancient ruins
[00:02-00:04] Reverse shot of explorer's face showing awe
[00:04-00:06] Tracking shot following explorer's footsteps
[00:06-00:08] Wide, high-angle crane shot revealing full landscape
```

Esta técnica permite planejamento preciso de micro-beats dentro de um único clip de 8 segundos.

### JSON prompting para consistência de marca

Segundo @mikefutia e repositórios GitHub, estruturar prompts em formato JSON aumenta consistência em **300%+** para conteúdo de marca:

```json
{
  "camera_angle": "medium shot, eye level",
  "brand_elements": "logo visible in corner",
  "lighting": "soft box from 45 degrees",
  "scene_transitions": "slow dolly in"
}
```

O raciocínio: IA entende esta estrutura de dados melhor que parágrafos descritivos longos.

### Combinando POV + chromakey

Para shots POV compositable, combine as técnicas:

```
First-person POV shot (thats where the camera is) held at chest height.
[CHARACTER] extends arm toward camera showing [OBJECT].
On a plain solid green chroma key background with even studio lighting.
Rim lighting around arm for edge separation.
Audio: ambient room tone. No subtitles.
```

### Character consistency com técnica "Character Bible"

Crie uma descrição detalhada do personagem e **copie-cole verbatim em cada prompt**:

```
[NAME], a [AGE] [ETHNICITY] [GENDER] with [SPECIFIC_HAIR_DETAILS], 
[EYE_COLOR] eyes, [DISTINCTIVE_FACIAL_FEATURES], 
wearing [DETAILED_CLOTHING_DESCRIPTION]
```

Exemplo:
```
Sarah Chen, a 32-year-old Asian-American woman with shoulder-length black hair 
in a professional bob, warm brown eyes behind wire-rimmed glasses, 
wearing a charcoal gray blazer over a white collared shirt
```

Use o recurso **Ingredients to Video** com até 3 imagens de referência para manter consistência visual. Segundo usuários da comunidade, esta combinação atinge **90%+ de consistência**.

### Técnica "This Then That" para progressão emocional

```
"The character starts confused and uncertain, then gradually becomes confident, 
finally ending with a satisfied smile"
```

Esta estrutura temporal ajuda VEO a criar arcos emocionais dentro de clips curtos.

---

## 6. Biblioteca de templates modulares

### Componentes modulares para mix-and-match

**Shot types:**
- `Wide establishing shot` | `Medium shot` | `Close-up` | `Extreme close-up`
- `Two-shot` | `Over-the-shoulder` | `Low angle` | `High angle` | `Dutch angle`

**Camera movements:**
- `Static tripod shot` | `Slow pan left/right` | `Gentle dolly in/out`
- `Tracking shot following subject` | `Crane shot rising` | `Orbit around subject`
- `Handheld with gentle sway` | `Smooth gimbal movement`

**Lighting setups:**
- `Natural daylight` | `Golden hour backlight` | `Blue hour ambiance`
- `Three-point studio lighting` | `Rembrandt lighting` | `High-key even lighting`
- `Rim lighting for separation` | `Chiaroscuro dramatic shadows`

**Style modifiers:**
- `Photorealistic` | `Cinematic` | `Documentary style` | `Commercial production`
- `Film noir` | `Wes Anderson style` | `35mm film aesthetic`
- `Shallow depth of field` | `Deep focus` | `Anamorphic lens feel`

**Audio templates:**
```
Audio: [SPECIFIC SOUNDS], [AMBIENT], [BACKGROUND ELEMENTS].
SFX: [SOUND EFFECT DESCRIPTION].
Ambient noise: [ENVIRONMENT SOUND].
```

**Negative prompt additions:**
```
No subtitles, no captions, no text overlays.
No harsh shadows, no lens flare, no floating camera.
No green contamination, no colored spill.
```

### Template universal completo

```
[SHOT TYPE] of [DETAILED SUBJECT DESCRIPTION] [ACTION WITH VERB].
[ENVIRONMENT/SETTING DESCRIPTION].
[CAMERA MOVEMENT] with [STABILIZATION STYLE].
[LIGHTING SETUP], [COLOR TEMPERATURE/MOOD].
Style: [AESTHETIC], [FILM REFERENCE IF APPLICABLE].
Audio: [SPECIFIC SOUNDS]. [DIALOGUE WITH COLON SYNTAX IF NEEDED].
Technical: [DURATION], [ASPECT RATIO], [RESOLUTION].
[NEGATIVE PROMPTS].
```

---

## 7. Guia de troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| **Vídeo sem áudio** | Upscaling para 1080p ou uso de SceneBuilder | Exporte em 720p; use Text-to-Video mode; selecione "Highest Quality (Experimental Audio)" |
| **Legendas indesejadas** | Sintaxe de diálogo incorreta | Use `says:` com dois-pontos; adicione `"(no subtitles)"` |
| **Personagem inconsistente** | Descrição simplificada entre prompts | Copie Character Bible completo em cada prompt; use Ingredients feature |
| **Diálogo incoerente** | Fala muito longa ou múltiplos speakers | Limite a 20 palavras, 1-2 speakers; repita identificadores |
| **Edge shimmer/artefatos** | Movimento de câmera muito rápido | Reduza velocidade de movimento; tente outro seed |
| **Composição drifting** | Falta de âncoras visuais | Trave first/last frames; adicione imagem de referência |
| **Pacing flutuante** | Beats muito longos | Encurte para 2-3 segundos; defina landing frame |
| **Output genérico** | Prompt vago | Seja ultra-específico sobre setting, lighting, mood |
| **Green screen inconsistente** | Variações de background | Gere múltiplas versões; mantenha câmera estática |
| **Falha de geração** | Violação de policy ou complexidade | Reformule prompt; reduza complexidade; limpe cache do browser |

### Bug confirmado: audio perdido no upscaling

Upscaling de 720p para 1080p **remove o áudio**. Se áudio é crítico, aceite 720p ou planeje adicionar áudio em pós-produção.

### Latência e retenção

- **Latência de request:** Mínimo 11 segundos; máximo 6 minutos em horários de pico
- **Retenção de vídeo:** 2 dias no servidor—faça download imediatamente

---

## 8. Recursos e comunidade

### Documentação oficial
- **Google Cloud Ultimate Prompting Guide:** cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- **Vertex AI Docs:** docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate
- **DeepMind Veo Page:** deepmind.google/models/veo/

### Repositórios GitHub essenciais
- **snubroot/Veo-3-Prompting-Guide** (147+ stars) — Guia mais completo da comunidade, fonte da descoberta "(thats where the camera is)"
- **SamurAIGPT/awesome-veo3** — Recursos curados e biblioteca de prompts
- **shijincai/veo3-prompt-generator** — Gerador com presets de estilo

### Power users para acompanhar (Twitter/X)
- **@TheoMediaAI** — Breakdowns técnicos, Fast Mode discovery
- **@Diesol (Dave Clark)** — "The Dave Clark Way" para cinematografia
- **@AllaAisling** — Short films completos com workflows
- **@Ror_Fly** — Base Prompt Structure (290K+ views)
- **@DanScalco** — Técnicas POV vlog
- **@ninja_prompt** — "Ingredients" prompting

### Ferramentas complementares
- **GLIF Master Prompter** (glif.app) — Gerador gratuito de prompts VEO 3.1
- **Topaz Video AI** — Upscaling para 4K/60fps
- **RunwayML Green Screen Beta** — AI keying para footage VEO
- **DaVinci Resolve Neural Engine** — Denoise e edge refinement

### Comunidades ativas
- Reddit: r/aiVideo, r/StableDiffusion, r/singularity, r/mediasynthesis
- Replicate Blog: replicate.com/blog (tutoriais regulares)
- Leonardo.ai Community: Guias específicos para VEO

---

## Conclusão: Framework unificado de prompt engineering

A engenharia de prompts para VEO 3.1 requer uma abordagem sistemática que combina a fórmula oficial do Google com descobertas validadas pela comunidade. Os três insights mais transformadores documentados neste guia são:

**Primeiro**, a sintaxe de posicionamento **"(thats where the camera is)"** resolve o problema histórico de câmeras flutuantes e perspectivas genéricas—uma descoberta da comunidade que deveria ser padrão em todo prompt com requisitos específicos de enquadramento.

**Segundo**, chromakey no VEO 3.1 funciona através de workflows indiretos: gere em backgrounds sólidos, use Image-to-Video para substituição, e planeje keying em pós-produção com ferramentas AI como RunwayML. O modelo não produz alpha channels, mas footage keyável é absolutamente alcançável.

**Terceiro**, consistência de personagem depende de repetição obsessiva. A técnica Character Bible—copiar descrições verbatim em cada prompt—combinada com o recurso Ingredients de até 3 imagens de referência, atinge consistência de 90%+ segundo relatórios da comunidade.

O VEO 3.1 ainda está em evolução ativa. Técnicas marcadas como 🔶 (Likely) ou ⚠️ (Experimental) neste guia devem ser testadas e validadas em seu workflow específico. A comunidade continua descobrindo capacidades não documentadas—acompanhe os repositórios GitHub e power users listados para manter-se atualizado com as práticas emergentes.
