# Three.js com React: Tutorial Completo para Aplicações 3D Modernas

React Three Fiber (R3F) revoluciona o desenvolvimento 3D na web ao transformar a API imperativa do Three.js em componentes React declarativos, permitindo que desenvolvedores criem experiências 3D complexas usando padrões familiares de React. Este tutorial cobre desde a configuração inicial até técnicas avançadas de produção, usando **Three.js r181**, **React Three Fiber v9**, e **Drei v10.7**, compatíveis com React 19 e Vite 6.

O R3F funciona como um renderer React personalizado que traduz componentes JSX em objetos Three.js. Cada `<mesh>` torna-se um `new THREE.Mesh()`, cada `<boxGeometry args={[1,1,1]}>` cria um `new THREE.BoxGeometry(1,1,1)`. O sistema gerencia automaticamente a criação, atualização e descarte de objetos, além de configurar câmera, renderer e loop de animação.

---

## 1. Configuração do projeto com Vite

### Instalação e dependências

```bash
# Criar projeto
npm create vite@latest meu-projeto-3d -- --template react-ts
cd meu-projeto-3d

# Instalar dependências principais
npm install three @react-three/fiber @react-three/drei

# Tipos TypeScript
npm install -D @types/three
```

### Estrutura de arquivos recomendada

```
src/
├── components/
│   ├── canvas/
│   │   ├── Experience.tsx      # Componente principal da cena
│   │   └── Scene.tsx           # Wrapper do Canvas
│   └── meshes/
│       └── Box.tsx             # Componentes 3D individuais
├── hooks/
│   └── useAnimation.ts         # Hooks customizados
├── models/
│   └── Character.tsx           # Modelos GLTF
├── assets/
│   ├── models/                 # Arquivos .glb/.gltf
│   └── textures/               # Texturas
└── App.tsx
```

### Configuração do Vite (vite.config.ts)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
  assetsInclude: ['**/*.glb', '**/*.gltf', '**/*.hdr', '**/*.exr'],
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three'],
          r3f: ['@react-three/fiber', '@react-three/drei']
        }
      }
    }
  }
})
```

### CSS para Canvas em tela cheia

```css
/* index.css */
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #root { width: 100%; height: 100%; }
body { overflow: hidden; }
```

---

## 2. Primeiro Canvas 3D com cubo interativo

O componente `Canvas` é o ponto de entrada do R3F, criando automaticamente um **WebGLRenderer** com antialiasing, uma **PerspectiveCamera** na posição `[0, 0, 5]`, e um loop de renderização otimizado.

```tsx
// src/App.tsx
import { Canvas } from '@react-three/fiber'
import Experience from './components/canvas/Experience'

export default function App() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 75 }}
      shadows
      dpr={[1, 2]}
    >
      <Experience />
    </Canvas>
  )
}
```

```tsx
// src/components/canvas/Experience.tsx
import { useRef, useState } from 'react'
import { useFrame, ThreeElements } from '@react-three/fiber'
import * as THREE from 'three'

function Box(props: ThreeElements['mesh']) {
  const meshRef = useRef<THREE.Mesh>(null!)
  const [hovered, setHover] = useState(false)
  const [active, setActive] = useState(false)

  // Hook de animação - executa a cada frame
  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta
    meshRef.current.rotation.y += delta * 0.5
  })

  return (
    <mesh
      {...props}
      ref={meshRef}
      scale={active ? 1.5 : 1}
      onClick={() => setActive(!active)}
      onPointerOver={() => setHover(true)}
      onPointerOut={() => setHover(false)}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : '#2f74c0'} />
    </mesh>
  )
}

export default function Experience() {
  return (
    <>
      {/* Iluminação básica */}
      <ambientLight intensity={Math.PI / 2} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={Math.PI} />
      <pointLight position={[-10, -10, -10]} intensity={Math.PI} />
      
      {/* Objetos 3D */}
      <Box position={[-1.2, 0, 0]} />
      <Box position={[1.2, 0, 0]} />
    </>
  )
}
```

---

## 3. Geometrias e formas primitivas

Three.js oferece **16 tipos de geometrias** built-in. No R3F, os argumentos do construtor são passados via prop `args` como array.

### Tabela de geometrias principais

| Geometria | Sintaxe R3F | Parâmetros Principais |
|-----------|-------------|----------------------|
| **BoxGeometry** | `<boxGeometry args={[1, 1, 1]} />` | width, height, depth |
| **SphereGeometry** | `<sphereGeometry args={[1, 32, 16]} />` | radius, widthSegments, heightSegments |
| **PlaneGeometry** | `<planeGeometry args={[1, 1]} />` | width, height |
| **CylinderGeometry** | `<cylinderGeometry args={[1, 1, 2, 32]} />` | radiusTop, radiusBottom, height |
| **ConeGeometry** | `<coneGeometry args={[1, 2, 32]} />` | radius, height, radialSegments |
| **TorusGeometry** | `<torusGeometry args={[1, 0.4, 16, 48]} />` | radius, tube, radialSegments |
| **TorusKnotGeometry** | `<torusKnotGeometry args={[1, 0.4, 100, 16]} />` | radius, tube, p, q |

### Galeria completa de geometrias

```tsx
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

function GeometryShowcase() {
  return (
    <Canvas camera={{ position: [0, 0, 12] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      
      {/* Linha 1 - Formas básicas */}
      <mesh position={[-4, 2, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="orange" />
      </mesh>
      
      <mesh position={[-2, 2, 0]}>
        <sphereGeometry args={[0.6, 32, 32]} />
        <meshStandardMaterial color="royalblue" />
      </mesh>
      
      <mesh position={[0, 2, 0]}>
        <cylinderGeometry args={[0.4, 0.6, 1.2, 32]} />
        <meshStandardMaterial color="green" />
      </mesh>
      
      <mesh position={[2, 2, 0]}>
        <coneGeometry args={[0.6, 1.2, 32]} />
        <meshStandardMaterial color="purple" />
      </mesh>
      
      {/* Linha 2 - Toroides e poliedros */}
      <mesh position={[-4, 0, 0]}>
        <torusGeometry args={[0.5, 0.2, 16, 48]} />
        <meshStandardMaterial color="red" />
      </mesh>
      
      <mesh position={[-2, 0, 0]}>
        <torusKnotGeometry args={[0.4, 0.15, 100, 16]} />
        <meshStandardMaterial color="cyan" />
      </mesh>
      
      <mesh position={[0, 0, 0]}>
        <dodecahedronGeometry args={[0.6, 0]} />
        <meshStandardMaterial color="yellow" />
      </mesh>
      
      <mesh position={[2, 0, 0]}>
        <icosahedronGeometry args={[0.6, 0]} />
        <meshStandardMaterial color="pink" />
      </mesh>
      
      {/* Linha 3 - Formas 2D */}
      <mesh position={[-2, -2, 0]}>
        <circleGeometry args={[0.6, 32]} />
        <meshStandardMaterial color="lime" side={THREE.DoubleSide} />
      </mesh>
      
      <mesh position={[0, -2, 0]}>
        <ringGeometry args={[0.3, 0.6, 32]} />
        <meshStandardMaterial color="gold" side={THREE.DoubleSide} />
      </mesh>
      
      <OrbitControls />
    </Canvas>
  )
}
```

### BufferGeometry personalizado

Para geometrias customizadas, crie um `BufferGeometry` com atributos de posição e UV:

```tsx
import { useMemo } from 'react'
import * as THREE from 'three'

function CustomTriangle() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    
    // Posições dos vértices (x, y, z para cada vértice)
    const vertices = new Float32Array([
      -1, -1, 0,   // Vértice 1
       1, -1, 0,   // Vértice 2
       0,  1, 0,   // Vértice 3
    ])
    
    // Coordenadas UV para textura
    const uvs = new Float32Array([
      0, 0,        // UV do vértice 1
      1, 0,        // UV do vértice 2
      0.5, 1,      // UV do vértice 3
    ])
    
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2))
    geo.computeVertexNormals()
    
    return geo
  }, [])
  
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="coral" side={THREE.DoubleSide} />
    </mesh>
  )
}
```

### Text3D com Drei

```tsx
import { Text3D, Center } from '@react-three/drei'

function Text3DExample() {
  return (
    <Center>
      <Text3D
        font="/fonts/helvetiker_regular.typeface.json"
        size={0.75}
        height={0.2}
        curveSegments={12}
        bevelEnabled
        bevelThickness={0.02}
        bevelSize={0.02}
        bevelSegments={5}
      >
        Hello 3D!
        <meshStandardMaterial color="orange" />
      </Text3D>
    </Center>
  )
}
```

---

## 4. Materiais e texturas

### Hierarquia de materiais por performance

| Material | Performance | Características | Uso Ideal |
|----------|-------------|-----------------|-----------|
| **MeshBasicMaterial** | ⚡ Mais rápido | Não reage à luz | Wireframes, UI |
| **MeshLambertMaterial** | ⚡⚡ Rápido | Superfície fosca | Madeira, pedra |
| **MeshPhongMaterial** | ⚡⚡⚡ Médio | Brilho especular | Plástico |
| **MeshStandardMaterial** | ⚡⚡⚡⚡ PBR | Fisicamente correto | Uso geral |
| **MeshPhysicalMaterial** | ⚡⚡⚡⚡⚡ Mais lento | PBR avançado | Vidro, verniz |

### Comparação visual de materiais

```tsx
function MaterialComparison() {
  return (
    <Canvas camera={{ position: [0, 0, 8] }}>
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={100} />
      
      {/* MeshBasicMaterial - cor sólida, ignora luz */}
      <mesh position={[-4, 0, 0]}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshBasicMaterial color="red" />
      </mesh>
      
      {/* MeshLambertMaterial - fosco */}
      <mesh position={[-2, 0, 0]}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshLambertMaterial color="red" />
      </mesh>
      
      {/* MeshPhongMaterial - brilhante */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshPhongMaterial color="red" shininess={100} />
      </mesh>
      
      {/* MeshStandardMaterial - PBR */}
      <mesh position={[2, 0, 0]}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshStandardMaterial color="red" metalness={0.5} roughness={0.3} />
      </mesh>
      
      {/* MeshPhysicalMaterial - verniz */}
      <mesh position={[4, 0, 0]}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshPhysicalMaterial color="red" clearcoat={1} clearcoatRoughness={0} />
      </mesh>
      
      <OrbitControls />
    </Canvas>
  )
}
```

### Carregando texturas com useTexture (Drei)

```tsx
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'

function TexturedBox() {
  // Carregamento de múltiplas texturas como objeto
  const textures = useTexture({
    map: '/textures/brick/color.jpg',
    normalMap: '/textures/brick/normal.jpg',
    roughnessMap: '/textures/brick/roughness.jpg',
    aoMap: '/textures/brick/ao.jpg',
  })
  
  // Configurar repetição da textura
  Object.values(textures).forEach(texture => {
    texture.wrapS = texture.wrapT = THREE.RepeatWrapping
    texture.repeat.set(2, 2)
  })
  
  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial {...textures} />
    </mesh>
  )
}
```

### MeshPhysicalMaterial para efeitos avançados

```tsx
// Vidro com refração
<meshPhysicalMaterial
  color="#ffffff"
  transmission={1}        // Transparência física
  thickness={0.5}         // Espessura do vidro
  roughness={0}
  ior={1.5}               // Índice de refração (vidro = 1.5)
/>

// Pintura automotiva com verniz
<meshPhysicalMaterial
  color="#cc0000"
  metalness={0.9}
  roughness={0.1}
  clearcoat={1}           // Camada de verniz
  clearcoatRoughness={0.1}
/>

// Tecido com sheen
<meshPhysicalMaterial
  color="#4a4a8a"
  roughness={1}
  sheen={1}               // Brilho de tecido
  sheenColor="#8888ff"
  sheenRoughness={0.5}
/>
```

---

## 5. Sistema de iluminação completo

### Tipos de luz disponíveis

```tsx
function LightingSetup() {
  return (
    <>
      {/* AmbientLight - ilumina tudo igualmente */}
      <ambientLight intensity={0.3} color="#ffffff" />
      
      {/* DirectionalLight - luz do sol, raios paralelos */}
      <directionalLight
        position={[5, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />
      
      {/* PointLight - lâmpada, emite em todas direções */}
      <pointLight
        position={[0, 5, 0]}
        intensity={50}
        distance={20}
        decay={2}
        color="#ff9900"
      />
      
      {/* SpotLight - holofote, cone de luz */}
      <spotLight
        position={[5, 10, 0]}
        angle={Math.PI / 6}
        penumbra={0.5}
        intensity={100}
        castShadow
      />
      
      {/* HemisphereLight - céu + chão */}
      <hemisphereLight
        skyColor="#87CEEB"
        groundColor="#362907"
        intensity={0.5}
      />
    </>
  )
}
```

### Configuração completa de sombras

```tsx
function ShadowScene() {
  return (
    <Canvas shadows camera={{ position: [5, 5, 5] }}>
      {/* Luz que projeta sombra */}
      <directionalLight
        castShadow
        position={[5, 8, 5]}
        intensity={1.5}
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-near={0.5}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-bias={-0.0001}
      />
      
      <ambientLight intensity={0.3} />
      
      {/* Objeto que projeta sombra */}
      <mesh castShadow position={[0, 1, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>
      
      {/* Chão que recebe sombra */}
      <mesh receiveShadow rotation-x={-Math.PI / 2} position={[0, 0, 0]}>
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="#404040" />
      </mesh>
      
      <OrbitControls />
    </Canvas>
  )
}
```

### Environment maps e iluminação HDR

```tsx
import { Environment } from '@react-three/drei'

function HDRLighting() {
  return (
    <Canvas>
      {/* Presets disponíveis: apartment, city, dawn, forest, 
          lobby, night, park, studio, sunset, warehouse */}
      <Environment
        preset="sunset"
        background                    // Mostra como fundo
        backgroundBlurriness={0.5}    // Desfoque do fundo
      />
      
      {/* Ou carregue arquivo HDR customizado */}
      {/* <Environment files="/hdri/studio.hdr" /> */}
      
      {/* Esfera metálica reflete o environment */}
      <mesh>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial metalness={1} roughness={0} />
      </mesh>
      
      <OrbitControls />
    </Canvas>
  )
}
```

---

## 6. Câmeras e controles de navegação

### PerspectiveCamera vs OrthographicCamera

```tsx
import { PerspectiveCamera, OrthographicCamera, OrbitControls } from '@react-three/drei'
import { useState } from 'react'

function CameraDemo() {
  const [ortho, setOrtho] = useState(false)
  
  return (
    <Canvas>
      {/* Câmera perspectiva - simula visão humana */}
      <PerspectiveCamera
        makeDefault={!ortho}
        position={[5, 5, 5]}
        fov={50}              // Campo de visão em graus
        near={0.1}
        far={1000}
      />
      
      {/* Câmera ortográfica - sem perspectiva, ideal para 2D/isométrico */}
      <OrthographicCamera
        makeDefault={ortho}
        position={[5, 5, 5]}
        zoom={50}
        near={0.1}
        far={1000}
      />
      
      <OrbitControls />
      
      {/* Botão HTML para alternar */}
      <Html>
        <button onClick={() => setOrtho(!ortho)}>
          {ortho ? 'Perspectiva' : 'Ortográfica'}
        </button>
      </Html>
    </Canvas>
  )
}
```

### OrbitControls - controle mais comum

```tsx
import { OrbitControls } from '@react-three/drei'

function ControlledScene() {
  return (
    <Canvas>
      <OrbitControls
        makeDefault
        enableDamping              // Movimento suave
        dampingFactor={0.05}
        
        // Limites de rotação
        minPolarAngle={0}          // Não permite ver por baixo
        maxPolarAngle={Math.PI / 2} // Máximo 90° vertical
        
        // Limites de zoom
        minDistance={2}
        maxDistance={20}
        
        // Habilitar/desabilitar recursos
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        
        // Rotação automática
        autoRotate={false}
        autoRotateSpeed={2}
        
        // Alvo do controle
        target={[0, 0, 0]}
      />
      
      {/* Cena */}
    </Canvas>
  )
}
```

### Animação de câmera programática

```tsx
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

function AnimatedCamera() {
  const { camera } = useThree()
  
  useFrame(({ clock }) => {
    const time = clock.elapsedTime
    
    // Movimento circular ao redor da cena
    camera.position.x = Math.sin(time * 0.5) * 5
    camera.position.z = Math.cos(time * 0.5) * 5
    camera.lookAt(0, 0, 0)
  })
  
  return null
}
```

---

## 7. Animações com useFrame, React Spring e GSAP

### useFrame - loop de animação nativo

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function AnimatedMesh() {
  const meshRef = useRef<THREE.Mesh>(null!)
  
  useFrame((state, delta) => {
    // state.clock - relógio da cena
    // state.camera - câmera atual
    // delta - tempo desde último frame (para animação independente de FPS)
    
    // Rotação constante
    meshRef.current.rotation.y += delta
    
    // Movimento senoidal
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.5
    
    // Escala pulsante
    const scale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
    meshRef.current.scale.setScalar(scale)
  })
  
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="coral" />
    </mesh>
  )
}
```

### React Spring para animações suaves

```tsx
import { useSpring, animated } from '@react-spring/three'
import { useState } from 'react'

function SpringAnimatedBox() {
  const [active, setActive] = useState(false)
  
  const springs = useSpring({
    scale: active ? 1.5 : 1,
    position: active ? [0, 1, 0] : [0, 0, 0],
    rotation: active ? [0, Math.PI, 0] : [0, 0, 0],
    color: active ? '#ff6b6b' : '#4ecdc4',
    config: { mass: 1, tension: 170, friction: 26 }
  })
  
  return (
    <animated.mesh
      scale={springs.scale}
      position={springs.position}
      rotation={springs.rotation}
      onClick={() => setActive(!active)}
    >
      <boxGeometry />
      <animated.meshStandardMaterial color={springs.color} />
    </animated.mesh>
  )
}
```

### GSAP para timelines complexas

```tsx
import { useRef, useLayoutEffect } from 'react'
import gsap from 'gsap'
import * as THREE from 'three'

function GSAPTimeline() {
  const meshRef = useRef<THREE.Mesh>(null!)
  const timeline = useRef<gsap.core.Timeline>()
  
  useLayoutEffect(() => {
    timeline.current = gsap.timeline({ repeat: -1, yoyo: true })
    
    timeline.current
      .to(meshRef.current.position, { x: 2, duration: 1, ease: 'power2.out' })
      .to(meshRef.current.rotation, { y: Math.PI, duration: 0.8 }, '-=0.5')
      .to(meshRef.current.scale, { x: 1.5, y: 1.5, z: 1.5, duration: 0.5 })
      .to(meshRef.current.position, { y: 2, duration: 1 })
    
    return () => timeline.current?.kill()
  }, [])
  
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="purple" />
    </mesh>
  )
}
```

---

## 8. Interatividade e eventos de ponteiro

### Sistema de eventos do R3F

```tsx
import { useState } from 'react'
import { useCursor } from '@react-three/drei'

function InteractiveObject() {
  const [hovered, setHovered] = useState(false)
  const [clicked, setClicked] = useState(false)
  
  // Muda cursor para "pointer" quando hover
  useCursor(hovered)
  
  return (
    <mesh
      onClick={(e) => {
        e.stopPropagation() // Previne propagação para objetos atrás
        setClicked(!clicked)
        console.log('Ponto de clique:', e.point)
        console.log('Face clicada:', e.face)
        console.log('Coordenadas UV:', e.uv)
      }}
      onPointerOver={(e) => {
        e.stopPropagation()
        setHovered(true)
      }}
      onPointerOut={() => setHovered(false)}
      onPointerMove={(e) => {
        // Chamado enquanto move sobre o objeto
        console.log('Posição:', e.point)
      }}
      scale={clicked ? 1.2 : 1}
    >
      <boxGeometry />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  )
}
```

### Drag and Drop com DragControls

```tsx
import { DragControls } from '@react-three/drei'
import { useState } from 'react'

function DraggableObject() {
  const [isDragging, setIsDragging] = useState(false)
  
  return (
    <DragControls
      axisLock="y"                              // Trava movimento no eixo Y
      dragLimits={[[-5, 5], [0, 10], [-5, 5]]}  // Limites [x, y, z]
      onDragStart={() => setIsDragging(true)}
      onDragEnd={() => setIsDragging(false)}
    >
      <mesh>
        <sphereGeometry args={[0.5]} />
        <meshStandardMaterial color={isDragging ? 'hotpink' : 'royalblue'} />
      </mesh>
    </DragControls>
  )
}
```

---

## 9. Física com @react-three/rapier

A biblioteca **@react-three/rapier** integra o motor de física Rapier ao R3F, oferecendo simulação de corpos rígidos de alta performance.

```bash
npm install @react-three/rapier
```

### Configuração básica de física

```tsx
import { Canvas } from '@react-three/fiber'
import { Physics, RigidBody } from '@react-three/rapier'
import { Suspense, useRef } from 'react'

function PhysicsScene() {
  return (
    <Canvas shadows camera={{ position: [5, 5, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} castShadow />
      
      <Suspense fallback={null}>
        <Physics debug gravity={[0, -9.81, 0]}>
          {/* Cubo que cai */}
          <RigidBody position={[0, 5, 0]} restitution={0.7}>
            <mesh castShadow>
              <boxGeometry />
              <meshStandardMaterial color="orange" />
            </mesh>
          </RigidBody>
          
          {/* Esfera que quica */}
          <RigidBody position={[1, 8, 0]} colliders="ball" restitution={0.9}>
            <mesh castShadow>
              <sphereGeometry args={[0.5]} />
              <meshStandardMaterial color="royalblue" />
            </mesh>
          </RigidBody>
          
          {/* Chão fixo */}
          <RigidBody type="fixed">
            <mesh receiveShadow position={[0, -1, 0]}>
              <boxGeometry args={[20, 0.5, 20]} />
              <meshStandardMaterial color="lightgreen" />
            </mesh>
          </RigidBody>
        </Physics>
      </Suspense>
      
      <OrbitControls />
    </Canvas>
  )
}
```

### Aplicando forças e impulsos

```tsx
import { RigidBody, RapierRigidBody } from '@react-three/rapier'
import { useRef } from 'react'

function JumpingCube() {
  const rigidBodyRef = useRef<RapierRigidBody>(null)
  
  const jump = () => {
    if (rigidBodyRef.current) {
      // Impulso instantâneo (pulo)
      rigidBodyRef.current.applyImpulse({ x: 0, y: 5, z: 0 }, true)
      
      // Rotação
      rigidBodyRef.current.applyTorqueImpulse({ x: 1, y: 0, z: 0 }, true)
    }
  }
  
  return (
    <RigidBody ref={rigidBodyRef} restitution={0.5}>
      <mesh onClick={jump}>
        <boxGeometry />
        <meshStandardMaterial color="coral" />
      </mesh>
    </RigidBody>
  )
}
```

### Detecção de colisões e sensores

```tsx
import { RigidBody, CuboidCollider } from '@react-three/rapier'
import { useState } from 'react'

function CollisionDetection() {
  const [isColliding, setIsColliding] = useState(false)
  
  return (
    <>
      {/* Objeto com detecção de colisão */}
      <RigidBody
        position={[0, 5, 0]}
        onCollisionEnter={({ manifold }) => {
          console.log('Colidiu! Ponto:', manifold.solverContactPoint(0))
          setIsColliding(true)
        }}
        onCollisionExit={() => setIsColliding(false)}
      >
        <mesh>
          <boxGeometry />
          <meshStandardMaterial color={isColliding ? 'red' : 'green'} />
        </mesh>
      </RigidBody>
      
      {/* Sensor (trigger zone) - não bloqueia movimento */}
      <RigidBody type="fixed">
        <CuboidCollider
          args={[2, 2, 0.5]}
          sensor
          onIntersectionEnter={() => console.log('Entrou na zona!')}
          onIntersectionExit={() => console.log('Saiu da zona!')}
        />
      </RigidBody>
    </>
  )
}
```

---

## 10. Carregamento de modelos 3D

### useGLTF para modelos GLB/GLTF

```tsx
import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef } from 'react'
import * as THREE from 'three'

function Model({ url }: { url: string }) {
  const group = useRef<THREE.Group>(null!)
  const { nodes, materials, animations } = useGLTF(url)
  const { actions, names } = useAnimations(animations, group)
  
  // Tocar primeira animação
  useEffect(() => {
    if (names.length > 0) {
      actions[names[0]]?.reset().fadeIn(0.5).play()
    }
  }, [actions, names])
  
  return (
    <group ref={group} dispose={null}>
      <primitive object={nodes.Scene || nodes.root} />
    </group>
  )
}

// Preload para carregamento mais rápido
useGLTF.preload('/models/character.glb')
```

### Indicador de progresso de carregamento

```tsx
import { Html, useProgress } from '@react-three/drei'
import { Suspense } from 'react'

function Loader() {
  const { progress, loaded, total } = useProgress()
  
  return (
    <Html center>
      <div style={{
        width: '200px',
        background: '#333',
        borderRadius: '10px',
        padding: '10px'
      }}>
        <div style={{
          width: `${progress}%`,
          height: '10px',
          background: '#4ecdc4',
          borderRadius: '5px',
          transition: 'width 0.3s'
        }} />
        <p style={{ color: 'white', textAlign: 'center', marginTop: '5px' }}>
          {progress.toFixed(0)}% ({loaded}/{total})
        </p>
      </div>
    </Html>
  )
}

function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model url="/models/character.glb" />
      </Suspense>
    </Canvas>
  )
}
```

---

## 11. Pós-processamento e efeitos visuais

```bash
npm install @react-three/postprocessing postprocessing
```

### EffectComposer com múltiplos efeitos

```tsx
import {
  EffectComposer,
  Bloom,
  DepthOfField,
  Vignette,
  ChromaticAberration,
  Noise,
  ToneMapping
} from '@react-three/postprocessing'
import { ToneMappingMode } from 'postprocessing'

function PostProcessingScene() {
  return (
    <Canvas>
      <Scene />
      
      <EffectComposer>
        {/* Bloom - brilho em áreas claras */}
        <Bloom
          intensity={1.5}
          luminanceThreshold={0.9}
          luminanceSmoothing={0.025}
          mipmapBlur
        />
        
        {/* Profundidade de campo */}
        <DepthOfField
          focusDistance={0}
          focalLength={0.02}
          bokehScale={2}
        />
        
        {/* Vinheta nas bordas */}
        <Vignette offset={0.1} darkness={1.1} />
        
        {/* Aberração cromática */}
        <ChromaticAberration offset={[0.002, 0.002]} />
        
        {/* Ruído de filme */}
        <Noise opacity={0.02} />
        
        {/* Tone mapping cinematográfico */}
        <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      </EffectComposer>
    </Canvas>
  )
}
```

### Materiais emissivos com Bloom

```tsx
// Para fazer objetos "brilharem" com Bloom
<meshStandardMaterial
  color="white"
  emissive="#ff0000"
  emissiveIntensity={2}
  toneMapped={false}  // Importante para cores acima de 1.0
/>
```

---

## 12. Performance e otimização

### Instancing para milhares de objetos

```tsx
import { Instances, Instance } from '@react-three/drei'

function InstancedScene() {
  const positions = Array.from({ length: 1000 }, () => [
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20
  ])
  
  return (
    <Instances limit={1000}>
      <boxGeometry args={[0.2, 0.2, 0.2]} />
      <meshStandardMaterial />
      
      {positions.map((pos, i) => (
        <Instance
          key={i}
          position={pos as [number, number, number]}
          color={`hsl(${(i / 1000) * 360}, 70%, 50%)`}
        />
      ))}
    </Instances>
  )
}
```

### Monitoramento de performance com r3f-perf

```tsx
import { Perf } from 'r3f-perf'

function Scene() {
  return (
    <Canvas>
      <Perf position="top-left" />
      {/* Resto da cena */}
    </Canvas>
  )
}
```

### Metas de performance recomendadas

| Métrica | Alvo | Atenção |
|---------|------|---------|
| **Draw calls** | < 100-200 | > 1000 |
| **Triângulos** | < 500k | > 2M |
| **FPS Desktop** | 60 | < 30 |
| **FPS Mobile** | 30-60 | < 24 |
| **Texturas GPU** | < 50MB | > 200MB |

### Boas práticas de performance

- **Reutilize geometrias e materiais** criando-os fora dos componentes
- **Use `visible={false}`** em vez de desmontar componentes para alternar visibilidade
- **Evite criar objetos dentro do `useFrame`** - crie-os uma vez e reutilize
- **Use `frameloop="demand"`** para cenas estáticas que só precisam renderizar quando há mudanças
- **Comprima modelos com Draco** - redução de 70-90% no tamanho
- **Use texturas KTX2** para menor uso de memória GPU

---

## 13. Projeto prático: Visualizador de produto 3D

```tsx
import { Canvas } from '@react-three/fiber'
import { 
  OrbitControls, 
  Environment, 
  ContactShadows,
  useGLTF,
  Html
} from '@react-three/drei'
import { Suspense, useState } from 'react'

const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7']

function Product({ color }: { color: string }) {
  const { nodes, materials } = useGLTF('/models/shoe.glb')
  
  return (
    <group dispose={null}>
      <mesh geometry={nodes.shoe.geometry} castShadow>
        <meshStandardMaterial
          color={color}
          roughness={0.3}
          metalness={0.1}
        />
      </mesh>
    </group>
  )
}

function Loader() {
  return (
    <Html center>
      <div className="loader">Carregando...</div>
    </Html>
  )
}

export default function ProductViewer() {
  const [selectedColor, setSelectedColor] = useState(colors[0])
  
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Canvas shadows camera={{ position: [0, 0, 4], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <spotLight
          position={[10, 10, 10]}
          angle={0.15}
          penumbra={1}
          intensity={1}
          castShadow
        />
        
        <Suspense fallback={<Loader />}>
          <Product color={selectedColor} />
          <Environment preset="studio" />
        </Suspense>
        
        <ContactShadows
          position={[0, -0.8, 0]}
          opacity={0.5}
          scale={10}
          blur={2}
        />
        
        <OrbitControls
          enablePan={false}
          minPolarAngle={Math.PI / 4}
          maxPolarAngle={Math.PI / 2}
          minDistance={2}
          maxDistance={6}
        />
      </Canvas>
      
      {/* Seletor de cores */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '10px'
      }}>
        {colors.map((color) => (
          <button
            key={color}
            onClick={() => setSelectedColor(color)}
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              background: color,
              border: selectedColor === color ? '3px solid white' : 'none',
              cursor: 'pointer',
              boxShadow: '0 2px 10px rgba(0,0,0,0.2)'
            }}
          />
        ))}
      </div>
    </div>
  )
}

useGLTF.preload('/models/shoe.glb')
```

---

## 14. Checklist de produção

### Antes do deploy

- [ ] **Comprimir modelos** com gltf-transform (Draco/Meshopt)
- [ ] **Otimizar texturas** - redimensionar para potências de 2, usar WebP/KTX2
- [ ] **Implementar Suspense** com fallback para loading states
- [ ] **Testar em dispositivos móveis** - ajustar DPR e desabilitar efeitos pesados
- [ ] **Adicionar fallback para WebGL** não suportado
- [ ] **Code-splitting** de componentes 3D pesados com `lazy()`
- [ ] **Preload de assets críticos** com `useGLTF.preload()`
- [ ] **Monitorar performance** - manter draw calls < 200, FPS > 30

### Configuração mobile-friendly

```tsx
<Canvas
  dpr={[1, 2]}                           // Limita pixel ratio
  gl={{ antialias: false }}              // Desabilita antialiasing no mobile
  performance={{ min: 0.5 }}             // Permite degradação de qualidade
  fallback={<div>WebGL não suportado</div>}
>
  <AdaptiveDpr pixelated />              // Ajusta DPR dinamicamente
  <PerformanceMonitor
    onDecline={() => setQuality('low')}
    onIncline={() => setQuality('high')}
  />
</Canvas>
```

---

## Conclusão e próximos passos

Este tutorial cobriu os fundamentos e técnicas avançadas para criar aplicações 3D com React Three Fiber. Os conceitos apresentados - desde geometrias básicas até otimização de performance - formam uma base sólida para desenvolver experiências 3D interativas de produção.

Para aprofundamento, explore o **Three.js Journey** de Bruno Simon para técnicas avançadas de shader, o repositório **pmndrs/examples** para padrões de código, e a documentação oficial do R3F em **docs.pmnd.rs** para APIs atualizadas. A comunidade Discord do Poimandres oferece suporte ativo para dúvidas específicas.

O ecossistema continua evoluindo rapidamente - R3F v9 adicionou suporte a WebGPU, e bibliotecas como **@react-three/xr** expandem possibilidades para realidade virtual e aumentada. Mantenha as dependências atualizadas e experimente os exemplos oficiais para descobrir novas possibilidades.