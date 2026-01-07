import React, { Suspense, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF, Environment, Grid } from '@react-three/drei'

const MODELS = {
  'Phase 1B (With Details)': [
    { name: 'Phase 1B - Iter 030 (Latest)', file: '/building_phase_1b_iter_030.glb' },
    { name: 'Phase 1B - Iter 013', file: '/building_phase_1b_iter_013.glb' },
  ],
  'Phase 1A (Base Structure)': [
    { name: 'Phase 1A - Iter 049', file: '/building_phase_1a_iter_049.glb' },
    { name: 'Phase 1A - Iter 048', file: '/building_phase_1a_iter_048.glb' },
    { name: 'Phase 1A - Iter 047', file: '/building_phase_1a_iter_047.glb' },
    { name: 'Phase 1A - Iter 046', file: '/building_phase_1a_iter_046.glb' },
    { name: 'Phase 1A - Iter 045', file: '/building_phase_1a_iter_045.glb' },
    { name: 'Phase 1A - Iter 044', file: '/building_phase_1a_iter_044.glb' },
    { name: 'Phase 1A - Iter 043', file: '/building_phase_1a_iter_043.glb' },
    { name: 'Phase 1A - Iter 042', file: '/building_phase_1a_iter_042.glb' },
    { name: 'Phase 1A - Iter 041', file: '/building_phase_1a_iter_041.glb' },
    { name: 'Phase 1A - Iter 040', file: '/building_phase_1a_iter_040.glb' },
    { name: 'Phase 1A - Iter 039', file: '/building_phase_1a_iter_039.glb' },
    { name: 'Phase 1A - Iter 038', file: '/building_phase_1a_iter_038.glb' },
    { name: 'Phase 1A - Iter 037', file: '/building_phase_1a_iter_037.glb' },
    { name: 'Phase 1A - Iter 036', file: '/building_phase_1a_iter_036.glb' },
    { name: 'Phase 1A - Iter 035', file: '/building_phase_1a_iter_035.glb' },
    { name: 'Phase 1A - Iter 017', file: '/building_phase_1a_iter_017.glb' },
    { name: 'Phase 1A - Iter 016', file: '/building_phase_1a_iter_016.glb' },
    { name: 'Phase 1A - Iter 015', file: '/building_phase_1a_iter_015.glb' },
    { name: 'Phase 1A - Iter 014', file: '/building_phase_1a_iter_014.glb' },
    { name: 'Phase 1A - Iter 013', file: '/building_phase_1a_iter_013.glb' },
    { name: 'Phase 1A - Iter 012', file: '/building_phase_1a_iter_012.glb' },
    { name: 'Phase 1A - Iter 011', file: '/building_phase_1a_iter_011.glb' },
    { name: 'Phase 1A - Iter 010', file: '/building_phase_1a_iter_010.glb' },
    { name: 'Phase 1A - Iter 009', file: '/building_phase_1a_iter_009.glb' },
    { name: 'Phase 1A - Iter 008', file: '/building_phase_1a_iter_008.glb' },
    { name: 'Phase 1A - Iter 007', file: '/building_phase_1a_iter_007.glb' },
    { name: 'Phase 1A - Iter 006', file: '/building_phase_1a_iter_006.glb' },
    { name: 'Phase 1A - Iter 005', file: '/building_phase_1a_iter_005.glb' },
    { name: 'Phase 1A - Iter 004', file: '/building_phase_1a_iter_004.glb' },
  ],
  'Work Iterations': [
    { name: 'Work - Iter 026', file: '/building_iteration_026.glb' },
    { name: 'Work - Iter 025', file: '/building_iteration_025.glb' },
    { name: 'Work - Iter 024', file: '/building_iteration_024.glb' },
    { name: 'Work - Iter 023', file: '/building_iteration_023.glb' },
    { name: 'Work - Iter 022', file: '/building_iteration_022.glb' },
    { name: 'Work - Iter 021', file: '/building_iteration_021.glb' },
    { name: 'Work - Iter 020', file: '/building_iteration_020.glb' },
    { name: 'Work - Iter 019', file: '/building_iteration_019.glb' },
    { name: 'Work - Iter 018', file: '/building_iteration_018.glb' },
  ],
  'Early Iterations': [
    { name: 'Iter 003', file: '/building_iter_003.glb' },
    { name: 'Iter 002', file: '/building_iter_002.glb' },
    { name: 'Iter 001', file: '/building_iter_001.glb' },
  ],
}

// Flatten for indexing
const ALL_MODELS = Object.values(MODELS).flat()

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
        <Scene modelUrl={ALL_MODELS[selectedModel].file} />
      </Canvas>

      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        background: 'rgba(0, 0, 0, 0.85)',
        padding: '15px 20px',
        borderRadius: 8,
        color: 'white',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: 14 }}>Building Viewer</h3>
        <p style={{ margin: '0 0 10px 0', fontSize: 11, opacity: 0.6 }}>
          {ALL_MODELS.length} models available
        </p>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(Number(e.target.value))}
          style={{
            padding: '8px 12px',
            borderRadius: 4,
            border: 'none',
            background: '#333',
            color: 'white',
            fontSize: 13,
            cursor: 'pointer',
            width: '100%',
            maxWidth: 280
          }}
        >
          {(() => {
            let globalIndex = 0
            return Object.entries(MODELS).map(([group, models]) => (
              <optgroup key={group} label={group}>
                {models.map((model) => {
                  const idx = globalIndex++
                  return <option key={model.file} value={idx}>{model.name}</option>
                })}
              </optgroup>
            ))
          })()}
        </select>
        <p style={{ margin: '10px 0 0 0', fontSize: 11, opacity: 0.7 }}>
          Drag to rotate | Scroll to zoom
        </p>
      </div>
    </div>
  )
}
