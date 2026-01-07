import React, { Suspense, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF, Environment, Grid } from '@react-three/drei'

const MODELS = [
  { name: 'Iteration 3 (Latest)', file: '/building_iter_003.glb' },
  { name: 'Iteration 2', file: '/building_iter_002.glb' },
  { name: 'Iteration 1', file: '/building_iter_001.glb' }
]

function Model({ url }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

function Scene({ modelUrl }) {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
      <directionalLight position={[-10, 10, -5]} intensity={0.5} />

      <Suspense fallback={null}>
        <Model url={modelUrl} />
      </Suspense>

      <Grid
        infiniteGrid
        cellSize={1}
        sectionSize={5}
        fadeDistance={50}
        cellColor="#666666"
        sectionColor="#888888"
      />

      <OrbitControls
        makeDefault
        minDistance={5}
        maxDistance={100}
        target={[0, 5, 0]}
      />

      <Environment preset="city" />
    </>
  )
}

export default function App() {
  const [selectedModel, setSelectedModel] = useState(0)

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        shadows
        camera={{ position: [20, 15, 20], fov: 50 }}
        style={{ background: '#1a1a2e' }}
      >
        <Scene modelUrl={MODELS[selectedModel].file} />
      </Canvas>

      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        background: 'rgba(0, 0, 0, 0.7)',
        padding: '15px 20px',
        borderRadius: 8,
        color: 'white'
      }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: 14 }}>Building Viewer</h3>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(Number(e.target.value))}
          style={{
            padding: '8px 12px',
            borderRadius: 4,
            border: 'none',
            background: '#333',
            color: 'white',
            fontSize: 14,
            cursor: 'pointer',
            width: '100%'
          }}
        >
          {MODELS.map((model, i) => (
            <option key={model.file} value={i}>{model.name}</option>
          ))}
        </select>
        <p style={{ margin: '10px 0 0 0', fontSize: 12, opacity: 0.7 }}>
          Drag to rotate | Scroll to zoom
        </p>
      </div>
    </div>
  )
}
