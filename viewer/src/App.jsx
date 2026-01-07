import React, { Suspense, useState, useRef, useEffect, useCallback, useMemo } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF, Sky, PointerLockControls } from '@react-three/drei'
import * as THREE from 'three'

const MODELS = {
  'Phase 1C (Interior)': [
    { name: 'Phase 1C - Iter 006 (Latest)', file: '/building_phase_1c_iter_006.glb' },
    { name: 'Phase 1C - Iter 005', file: '/building_phase_1c_iter_005.glb' },
    { name: 'Phase 1C - Iter 004', file: '/building_phase_1c_iter_004.glb' },
    { name: 'Phase 1C - Iter 003', file: '/building_phase_1c_iter_003.glb' },
    { name: 'Phase 1C - Iter 002', file: '/building_phase_1c_iter_002.glb' },
    { name: 'Phase 1C - Iter 001', file: '/building_phase_1c_iter_001.glb' },
  ],
  'Phase 1B (With Details)': [
    { name: 'Phase 1B - Iter 030 (Latest)', file: '/building_phase_1b_iter_030.glb' },
    { name: 'Phase 1B - Iter 029', file: '/building_phase_1b_iter_029.glb' },
    { name: 'Phase 1B - Iter 028', file: '/building_phase_1b_iter_028.glb' },
    { name: 'Phase 1B - Iter 027', file: '/building_phase_1b_iter_027.glb' },
    { name: 'Phase 1B - Iter 026', file: '/building_phase_1b_iter_026.glb' },
    { name: 'Phase 1B - Iter 025', file: '/building_phase_1b_iter_025.glb' },
    { name: 'Phase 1B - Iter 024', file: '/building_phase_1b_iter_024.glb' },
    { name: 'Phase 1B - Iter 023', file: '/building_phase_1b_iter_023.glb' },
    { name: 'Phase 1B - Iter 022', file: '/building_phase_1b_iter_022.glb' },
    { name: 'Phase 1B - Iter 021', file: '/building_phase_1b_iter_021.glb' },
    { name: 'Phase 1B - Iter 020', file: '/building_phase_1b_iter_020.glb' },
    { name: 'Phase 1B - Iter 019', file: '/building_phase_1b_iter_019.glb' },
    { name: 'Phase 1B - Iter 018', file: '/building_phase_1b_iter_018.glb' },
    { name: 'Phase 1B - Iter 017', file: '/building_phase_1b_iter_017.glb' },
    { name: 'Phase 1B - Iter 016', file: '/building_phase_1b_iter_016.glb' },
    { name: 'Phase 1B - Iter 015', file: '/building_phase_1b_iter_015.glb' },
    { name: 'Phase 1B - Iter 014', file: '/building_phase_1b_iter_014.glb' },
    { name: 'Phase 1B - Iter 013', file: '/building_phase_1b_iter_013.glb' },
    { name: 'Phase 1B - Iter 012', file: '/building_phase_1b_iter_012.glb' },
    { name: 'Phase 1B - Iter 011', file: '/building_phase_1b_iter_011.glb' },
    { name: 'Phase 1B - Iter 010', file: '/building_phase_1b_iter_010.glb' },
    { name: 'Phase 1B - Iter 009', file: '/building_phase_1b_iter_009.glb' },
    { name: 'Phase 1B - Iter 008', file: '/building_phase_1b_iter_008.glb' },
    { name: 'Phase 1B - Iter 007', file: '/building_phase_1b_iter_007.glb' },
    { name: 'Phase 1B - Iter 006', file: '/building_phase_1b_iter_006.glb' },
    { name: 'Phase 1B - Iter 005', file: '/building_phase_1b_iter_005.glb' },
    { name: 'Phase 1B - Iter 004', file: '/building_phase_1b_iter_004.glb' },
    { name: 'Phase 1B - Iter 003', file: '/building_phase_1b_iter_003.glb' },
    { name: 'Phase 1B - Iter 002', file: '/building_phase_1b_iter_002.glb' },
    { name: 'Phase 1B - Iter 001', file: '/building_phase_1b_iter_001.glb' },
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

const ALL_MODELS = Object.values(MODELS).flat()

function Model({ url, onLoad }) {
  const { scene } = useGLTF(url)

  useEffect(() => {
    if (onLoad && scene) {
      // Collect all meshes for collision detection, hide Cutter objects
      const collisionMeshes = []
      scene.traverse((child) => {
        if (child.isMesh) {
          const name = child.name || ''
          // Hide Boolean modifier cutter objects (used for window/door cutouts)
          if (name.includes('Cutter') || name.includes('_Cutter')) {
            child.visible = false
          } else {
            collisionMeshes.push(child)
          }
        }
      })
      onLoad(collisionMeshes)
    }
  }, [scene, onLoad])

  return <primitive object={scene} />
}

// Simple low-poly tree
function Tree({ position, scale = 1, trunkHeight = 2, foliageRadius = 1.5, onTrunkRef }) {
  const actualTrunkHeight = trunkHeight * scale
  const actualFoliageRadius = foliageRadius * scale
  const trunkRef = useRef()

  useEffect(() => {
    if (onTrunkRef && trunkRef.current) {
      onTrunkRef(trunkRef.current)
    }
  }, [onTrunkRef])

  return (
    <group position={position}>
      {/* Trunk */}
      <mesh ref={trunkRef} position={[0, actualTrunkHeight / 2, 0]} castShadow>
        <cylinderGeometry args={[0.15 * scale, 0.25 * scale, actualTrunkHeight, 8]} />
        <meshStandardMaterial color="#5D4037" roughness={0.9} />
      </mesh>
      {/* Foliage - layered cones for fuller look */}
      <mesh position={[0, actualTrunkHeight + actualFoliageRadius * 0.3, 0]} castShadow>
        <coneGeometry args={[actualFoliageRadius, actualFoliageRadius * 2, 8]} />
        <meshStandardMaterial color="#2E7D32" roughness={0.8} />
      </mesh>
      <mesh position={[0, actualTrunkHeight + actualFoliageRadius * 1.0, 0]} castShadow>
        <coneGeometry args={[actualFoliageRadius * 0.7, actualFoliageRadius * 1.5, 8]} />
        <meshStandardMaterial color="#388E3C" roughness={0.8} />
      </mesh>
      <mesh position={[0, actualTrunkHeight + actualFoliageRadius * 1.5, 0]} castShadow>
        <coneGeometry args={[actualFoliageRadius * 0.4, actualFoliageRadius * 1, 8]} />
        <meshStandardMaterial color="#43A047" roughness={0.8} />
      </mesh>
    </group>
  )
}

// Tree positions based on reference photos - trees behind and around the building
const TREE_POSITIONS = [
  // Large tree to the left (prominent in reference)
  { pos: [-15, 0, -5], scale: 2.5, trunk: 4, foliage: 3 },
  // Trees behind building
  { pos: [-20, 0, -20], scale: 1.8, trunk: 3, foliage: 2.5 },
  { pos: [-10, 0, -25], scale: 2.0, trunk: 3.5, foliage: 2.8 },
  { pos: [0, 0, -30], scale: 1.5, trunk: 2.5, foliage: 2 },
  { pos: [12, 0, -25], scale: 2.2, trunk: 4, foliage: 3 },
  { pos: [25, 0, -20], scale: 1.7, trunk: 3, foliage: 2.3 },
  // Trees to the right
  { pos: [20, 0, -8], scale: 1.9, trunk: 3.5, foliage: 2.5 },
  { pos: [28, 0, 5], scale: 1.6, trunk: 2.8, foliage: 2 },
  // Scattered background trees
  { pos: [-30, 0, -15], scale: 1.4, trunk: 2.5, foliage: 2 },
  { pos: [35, 0, -15], scale: 1.5, trunk: 2.8, foliage: 2.2 },
  { pos: [-25, 0, 10], scale: 1.3, trunk: 2.2, foliage: 1.8 },
  { pos: [30, 0, -30], scale: 2.0, trunk: 3.5, foliage: 2.8 },
  { pos: [-35, 0, -30], scale: 1.8, trunk: 3, foliage: 2.5 },
]

// First-person movement controller with collision detection
function FirstPersonMovement({ speed = 5, collisionMeshes = [] }) {
  const { camera } = useThree()
  const moveState = useRef({ forward: false, backward: false, left: false, right: false })
  const raycaster = useRef(new THREE.Raycaster())

  const COLLISION_DISTANCE = 1.5 // How close before stopping
  const PUSH_BACK_DISTANCE = 0.8 // If closer than this, push back

  useEffect(() => {
    const handleKeyDown = (e) => {
      switch (e.code) {
        case 'KeyW': case 'ArrowUp': moveState.current.forward = true; break
        case 'KeyS': case 'ArrowDown': moveState.current.backward = true; break
        case 'KeyA': case 'ArrowLeft': moveState.current.left = true; break
        case 'KeyD': case 'ArrowRight': moveState.current.right = true; break
      }
    }
    const handleKeyUp = (e) => {
      switch (e.code) {
        case 'KeyW': case 'ArrowUp': moveState.current.forward = false; break
        case 'KeyS': case 'ArrowDown': moveState.current.backward = false; break
        case 'KeyA': case 'ArrowLeft': moveState.current.left = false; break
        case 'KeyD': case 'ArrowRight': moveState.current.right = false; break
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('keyup', handleKeyUp)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('keyup', handleKeyUp)
    }
  }, [])

  // Check collision in a given direction at multiple heights
  const checkCollision = (directionVec, distance = COLLISION_DISTANCE) => {
    if (collisionMeshes.length === 0) return { blocked: false, closest: Infinity }

    const heights = [0.3, 0.8, 1.4] // Check at knee, waist, chest height
    let closestDist = Infinity

    for (const heightOffset of heights) {
      const rayOrigin = camera.position.clone()
      rayOrigin.y = heightOffset

      raycaster.current.set(rayOrigin, directionVec.clone().normalize())
      const intersects = raycaster.current.intersectObjects(collisionMeshes, true)

      if (intersects.length > 0 && intersects[0].distance < closestDist) {
        closestDist = intersects[0].distance
      }
    }

    return { blocked: closestDist < distance, closest: closestDist }
  }

  useFrame((_, delta) => {
    const { forward, backward, left, right } = moveState.current

    // Get world directions
    const cameraDirection = new THREE.Vector3()
    camera.getWorldDirection(cameraDirection)
    cameraDirection.y = 0
    cameraDirection.normalize()

    const cameraRight = new THREE.Vector3()
    cameraRight.crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0))

    // Check all 4 directions and push back if too close
    const directions = [
      { dir: cameraDirection.clone(), name: 'forward' },
      { dir: cameraDirection.clone().negate(), name: 'backward' },
      { dir: cameraRight.clone(), name: 'right' },
      { dir: cameraRight.clone().negate(), name: 'left' },
    ]

    for (const { dir } of directions) {
      const { closest } = checkCollision(dir, PUSH_BACK_DISTANCE)
      if (closest < PUSH_BACK_DISTANCE) {
        // Push back away from wall - stronger push to prevent getting stuck
        const pushStrength = Math.max(0.1, (PUSH_BACK_DISTANCE - closest) * 0.5)
        const pushBack = dir.clone().negate().multiplyScalar(pushStrength)
        camera.position.add(pushBack)
      }
    }

    // Calculate intended movement
    const moveSpeed = speed * delta

    // Forward/backward
    if (forward || backward) {
      const moveDir = forward ? cameraDirection.clone() : cameraDirection.clone().negate()
      const { blocked } = checkCollision(moveDir.clone())
      if (!blocked) {
        camera.position.add(moveDir.multiplyScalar(moveSpeed))
      }
    }

    // Left/right
    if (left || right) {
      const moveDir = right ? cameraRight.clone() : cameraRight.clone().negate()
      const { blocked } = checkCollision(right ? cameraRight : cameraRight.clone().negate())
      if (!blocked) {
        camera.position.add(moveDir.multiplyScalar(moveSpeed))
      }
    }

    // Keep camera at eye level
    camera.position.y = 1.7
  })

  return null
}

function Scene({ modelUrl, isFirstPerson, onExitFirstPerson }) {
  const controlsRef = useRef()
  const { camera } = useThree()
  const [buildingMeshes, setBuildingMeshes] = useState([])
  const [treeMeshes, setTreeMeshes] = useState([])

  // Combine building and tree meshes for collision
  const collisionMeshes = useMemo(() => {
    return [...buildingMeshes, ...treeMeshes]
  }, [buildingMeshes, treeMeshes])

  // Handle model load - collect meshes for collision
  const handleModelLoad = useCallback((meshes) => {
    setBuildingMeshes(meshes)
  }, [])

  // Handle tree trunk registration
  const handleTreeTrunk = useCallback((mesh) => {
    setTreeMeshes(prev => {
      if (prev.includes(mesh)) return prev
      return [...prev, mesh]
    })
  }, [])

  // Position camera for first-person view (in front of building, looking at it)
  useEffect(() => {
    if (isFirstPerson) {
      camera.position.set(0, 1.7, 15)
      camera.lookAt(0, 3, 0)
    } else {
      camera.position.set(20, 15, 20)
    }
  }, [isFirstPerson, camera])

  // Sun position for natural daylight (late morning sun)
  const sunPosition = [50, 30, 50]

  return (
    <>
      {/* Natural daylight lighting */}
      <ambientLight intensity={0.4} color="#87CEEB" />
      <directionalLight
        position={sunPosition}
        intensity={1.5}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-far={100}
        shadow-camera-left={-30}
        shadow-camera-right={30}
        shadow-camera-top={30}
        shadow-camera-bottom={-30}
        color="#FFF5E1"
      />
      <hemisphereLight
        skyColor="#87CEEB"
        groundColor="#3d5c3d"
        intensity={0.5}
      />

      <Suspense fallback={null}>
        <Model url={modelUrl} onLoad={handleModelLoad} />
      </Suspense>

      {/* Realistic sky */}
      <Sky
        distance={450000}
        sunPosition={sunPosition}
        inclination={0.6}
        azimuth={0.25}
        mieCoefficient={0.005}
        mieDirectionalG={0.8}
        rayleigh={0.5}
        turbidity={10}
      />

      {/* Ground System - layered for realism */}

      {/* Base grass field */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.02, 0]}
        receiveShadow
      >
        <planeGeometry args={[150, 150]} />
        <meshStandardMaterial
          color="#5a7a4a"
          roughness={1}
          metalness={0}
        />
      </mesh>

      {/* Concrete/asphalt parking pad in front of building */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.01, 8]}
        receiveShadow
      >
        <planeGeometry args={[25, 12]} />
        <meshStandardMaterial
          color="#8a8a8a"
          roughness={0.95}
          metalness={0}
        />
      </mesh>

      {/* Worn dirt/gravel transition around concrete */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.015, 8]}
        receiveShadow
      >
        <planeGeometry args={[30, 16]} />
        <meshStandardMaterial
          color="#7a7060"
          roughness={1}
          metalness={0}
        />
      </mesh>

      {/* Road strip at front */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.005, 20]}
        receiveShadow
      >
        <planeGeometry args={[80, 8]} />
        <meshStandardMaterial
          color="#3a3a3a"
          roughness={0.8}
          metalness={0}
        />
      </mesh>

      {/* Trees around the property */}
      {TREE_POSITIONS.map((tree, i) => (
        <Tree
          key={i}
          position={tree.pos}
          scale={tree.scale}
          trunkHeight={tree.trunk}
          foliageRadius={tree.foliage}
          onTrunkRef={handleTreeTrunk}
        />
      ))}

      {isFirstPerson ? (
        <>
          <PointerLockControls
            ref={controlsRef}
            onUnlock={onExitFirstPerson}
          />
          <FirstPersonMovement speed={8} collisionMeshes={collisionMeshes} />
        </>
      ) : (
        <OrbitControls
          makeDefault
          minDistance={5}
          maxDistance={100}
          target={[0, 5, 0]}
        />
      )}
    </>
  )
}

export default function App() {
  const [selectedModel, setSelectedModel] = useState(0)
  const [isFirstPerson, setIsFirstPerson] = useState(false)

  // Toggle mode with F key
  const toggleMode = useCallback(() => {
    setIsFirstPerson(prev => !prev)
  }, [])

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'KeyF' && !e.repeat) {
        toggleMode()
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [toggleMode])

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        shadows
        camera={{ position: [20, 15, 20], fov: 50 }}
        style={{ background: 'linear-gradient(to bottom, #87CEEB, #E0F6FF)' }}
      >
        <Scene
          modelUrl={ALL_MODELS[selectedModel].file}
          isFirstPerson={isFirstPerson}
          onExitFirstPerson={() => setIsFirstPerson(false)}
        />
      </Canvas>

      {/* Controls Panel - Always visible */}
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

        <p style={{ margin: '12px 0 0 0', fontSize: 11, opacity: 0.7 }}>
          {isFirstPerson ? 'Drag to rotate | Scroll to zoom' : 'WASD to move | Mouse to look'}
        </p>
      </div>

      {/* Mode Indicator - Always visible */}
      <div style={{
        position: 'absolute',
        top: 20,
        right: 20,
        background: isFirstPerson ? 'rgba(74, 111, 165, 0.9)' : 'rgba(0, 0, 0, 0.85)',
        padding: '12px 20px',
        borderRadius: 8,
        color: 'white',
        textAlign: 'center'
      }}>
        <p style={{ margin: 0, fontSize: 14, fontWeight: 'bold' }}>
          {isFirstPerson ? 'First-Person Mode' : 'Orbit Mode'}
        </p>
        <p style={{ margin: '6px 0 0 0', fontSize: 12, opacity: 0.8 }}>
          Press <span style={{
            background: 'rgba(255,255,255,0.2)',
            padding: '2px 8px',
            borderRadius: 4,
            fontFamily: 'monospace',
            fontWeight: 'bold'
          }}>F</span> to switch
        </p>
      </div>

      {/* First-Person Controls Help */}
      {isFirstPerson && (
        <div style={{
          position: 'absolute',
          bottom: 20,
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(0, 0, 0, 0.85)',
          padding: '12px 24px',
          borderRadius: 8,
          color: 'white',
          textAlign: 'center'
        }}>
          <p style={{ margin: 0, fontSize: 13 }}>
            <strong>WASD</strong> to move | <strong>Mouse</strong> to look | <strong>ESC</strong> to unlock mouse
          </p>
          <p style={{ margin: '5px 0 0 0', fontSize: 11, opacity: 0.7 }}>
            Click to enable mouse look
          </p>
        </div>
      )}
    </div>
  )
}
