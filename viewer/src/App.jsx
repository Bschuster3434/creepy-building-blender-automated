import React, { Suspense, useState, useRef, useEffect, useCallback, useMemo } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF, Sky, PointerLockControls, useProgress, Environment } from '@react-three/drei'
import { EffectComposer, SSAO, Vignette } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'
import * as THREE from 'three'

const MODELS = {
  'Phase 3 (Environment)': [
    { name: 'Phase 3 - Iter 002 (Latest)', file: '/building_phase_3_iter_002.glb' },
    { name: 'Phase 3 - Iter 001', file: '/building_phase_3_iter_001.glb' },
  ],
  'Phase 2 (Materials)': [
    { name: 'Phase 2 - Iter 015', file: '/building_phase_2_iter_015.glb' },
    { name: 'Phase 2 - Iter 014', file: '/building_phase_2_iter_014.glb' },
    { name: 'Phase 2 - Iter 013', file: '/building_phase_2_iter_013.glb' },
    { name: 'Phase 2 - Iter 012', file: '/building_phase_2_iter_012.glb' },
    { name: 'Phase 2 - Iter 011', file: '/building_phase_2_iter_011.glb' },
    { name: 'Phase 2 - Iter 010', file: '/building_phase_2_iter_010.glb' },
    { name: 'Phase 2 - Iter 009', file: '/building_phase_2_iter_009.glb' },
    { name: 'Phase 2 - Iter 008', file: '/building_phase_2_iter_008.glb' },
    { name: 'Phase 2 - Iter 007', file: '/building_phase_2_iter_007.glb' },
    { name: 'Phase 2 - Iter 006', file: '/building_phase_2_iter_006.glb' },
    { name: 'Phase 2 - Iter 005', file: '/building_phase_2_iter_005.glb' },
    { name: 'Phase 2 - Iter 004', file: '/building_phase_2_iter_004.glb' },
    { name: 'Phase 2 - Iter 003', file: '/building_phase_2_iter_003.glb' },
    { name: 'Phase 2 - Iter 002', file: '/building_phase_2_iter_002.glb' },
    { name: 'Phase 2 - Iter 001', file: '/building_phase_2_iter_001.glb' },
  ],
  'Phase 1C (Interior)': [
    { name: 'Phase 1C - Iter 007 (Latest)', file: '/building_phase_1c_iter_007.glb' },
    { name: 'Phase 1C - Iter 006', file: '/building_phase_1c_iter_006.glb' },
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

// Reference images organized by category
const REFERENCES = {
  'Exterior': {
    description: 'External views of the building',
    subcategories: {
      'Generated Views': [
        { name: 'Front View', file: '/references/exterior/front-view.png' },
        { name: 'Back View', file: '/references/exterior/back-view.png' },
        { name: 'Left Side', file: '/references/exterior/left-side-view.png' },
        { name: 'Right Side', file: '/references/exterior/right-side-view.png' },
        { name: 'Corner View', file: '/references/exterior/corner-view.jpg' },
        { name: 'Corner View 2', file: '/references/exterior/corner-view-2.png' },
        { name: 'Birdseye View', file: '/references/exterior/birdseye-view.png' },
        { name: 'Roof Angle', file: '/references/exterior/roof-angle-view.png' },
        { name: 'Cross Section', file: '/references/exterior/cross-section.png' },
      ],
      'Google Maps': [
        { name: 'Street View 1', file: '/references/exterior/google-maps-01.png' },
        { name: 'Street View 2', file: '/references/exterior/google-maps-02.png' },
        { name: 'Street View 3', file: '/references/exterior/google-maps-03.png' },
        { name: 'Street View 4', file: '/references/exterior/google-maps-04.png' },
        { name: 'Street View 5', file: '/references/exterior/google-maps-05.png' },
        { name: 'Street View 6', file: '/references/exterior/google-maps-06.png' },
        { name: 'Street View 7', file: '/references/exterior/google-maps-07.png' },
        { name: 'Street View 8', file: '/references/exterior/google-maps-08.png' },
        { name: 'Overhead', file: '/references/exterior/google-maps-overhead.png' },
      ],
    }
  },
  'Interior': {
    description: 'Internal views and layout concepts',
    subcategories: {
      'Concepts': [
        { name: 'Interior Concept', file: '/references/interior/interior-concept.jpg' },
      ],
    }
  },
  'Details': {
    description: 'Doors, windows, and architectural details',
    subcategories: {
      'Doors': [
        { name: 'French Door 1', file: '/references/details/french-door-1.png' },
        { name: 'French Door 2', file: '/references/details/french-door-2.png' },
        { name: 'French Door 3', file: '/references/details/french-door-3.webp' },
        { name: 'French Door 4', file: '/references/details/french-door-4.webp' },
        { name: 'Back Door', file: '/references/details/back-door.png' },
        { name: 'Front Entry Door', file: '/references/details/front-entry-door.webp' },
      ],
      'Windows': [
        { name: 'Front Window', file: '/references/details/front-window.png' },
        { name: 'Alcove Window', file: '/references/details/alcove-window.jpg' },
      ],
    }
  },
}

// Flatten all references for easy navigation
const ALL_REFERENCES = Object.entries(REFERENCES).flatMap(([category, data]) =>
  Object.entries(data.subcategories).flatMap(([subcategory, images]) =>
    images.map(img => ({ ...img, category, subcategory }))
  )
)

function Model({ url, onLoad, onDoorsFound }) {
  const { scene } = useGLTF(url)

  useEffect(() => {
    if (scene) {
      // Collect all meshes for collision detection, hide Cutter objects
      const collisionMeshes = []
      const doorPivots = []

      scene.traverse((child) => {
        const name = child.name || ''
        const nameLower = name.toLowerCase()

        // Find door pivot objects (empties that control door rotation)
        if (name.includes('_Pivot') && nameLower.includes('door')) {
          doorPivots.push({
            name: name,
            object: child,
            isOpen: false,
            targetRotation: 0,
            // Determine door type and open direction
            type: name.includes('Front_Entry_Door_Left') ? 'front_left' :
                  name.includes('Front_Entry_Door_Right') ? 'front_right' :
                  name.includes('Rear_Service') ? 'rear' : 'unknown',
            // Open direction: positive = outward swing
            openAngle: name.includes('Front_Entry_Door_Left') ? Math.PI / 2 :
                       name.includes('Front_Entry_Door_Right') ? -Math.PI / 2 :
                       name.includes('Rear_Service') ? Math.PI / 2 : Math.PI / 2,
          })
        }

        if (child.isMesh) {
          // Hide Boolean modifier cutter objects (used for window/door cutouts)
          if (name.includes('Cutter') || name.includes('_Cutter')) {
            child.visible = false
          }
          // Exclude door objects from collision (so player can walk through)
          else if (nameLower.includes('door')) {
            // Door is visible but not collidable - don't add to collision meshes
            // But doors should still cast and receive shadows
            child.castShadow = true
            child.receiveShadow = true
          }
          else {
            collisionMeshes.push(child)
            // Enable shadow casting and receiving for realistic lighting
            child.castShadow = true
            child.receiveShadow = true
          }
        }
      })

      if (onLoad) {
        onLoad(collisionMeshes)
      }
      if (onDoorsFound && doorPivots.length > 0) {
        onDoorsFound(doorPivots)
      }
    }
  }, [scene, onLoad, onDoorsFound])

  return <primitive object={scene} />
}


// Tone mapping and renderer configuration for realistic lighting
function ToneMapping() {
  const { gl } = useThree()

  useEffect(() => {
    // ACESFilmic tone mapping for cinematic, realistic lighting
    gl.toneMapping = THREE.ACESFilmicToneMapping
    gl.toneMappingExposure = 1.0
    // Ensure proper color space for realistic colors
    gl.outputColorSpace = THREE.SRGBColorSpace
  }, [gl])

  return null
}


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

// Door animation controller - handles proximity detection and smooth rotation
function DoorController({ doors, isFirstPerson, onNearDoorChange }) {
  const { camera } = useThree()
  const doorStates = useRef({})
  const INTERACTION_DISTANCE = 3.0 // How close to interact with door

  // Initialize door states
  useEffect(() => {
    doors.forEach(door => {
      if (!doorStates.current[door.name]) {
        doorStates.current[door.name] = {
          isOpen: false,
          currentRotation: 0,
          targetRotation: 0,
          openAngle: door.openAngle,
        }
      }
    })
  }, [doors])

  // Handle E key to toggle nearest door
  useEffect(() => {
    if (!isFirstPerson) return

    const handleKeyDown = (e) => {
      if (e.code === 'KeyE' && !e.repeat) {
        // Find nearest door within interaction distance
        let nearestDoor = null
        let nearestDist = Infinity

        doors.forEach(door => {
          const doorPos = new THREE.Vector3()
          door.object.getWorldPosition(doorPos)
          const dist = camera.position.distanceTo(doorPos)
          if (dist < INTERACTION_DISTANCE && dist < nearestDist) {
            nearestDist = dist
            nearestDoor = door
          }
        })

        if (nearestDoor) {
          const state = doorStates.current[nearestDoor.name]
          state.isOpen = !state.isOpen
          state.targetRotation = state.isOpen ? state.openAngle : 0
        }
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [doors, camera, isFirstPerson])

  // Animate doors and detect proximity
  useFrame((_, delta) => {
    let nearestDoorName = null
    let nearestDist = Infinity

    doors.forEach(door => {
      const state = doorStates.current[door.name]
      if (!state) return

      // Smooth rotation animation
      const rotationSpeed = 3.0 // radians per second
      const diff = state.targetRotation - state.currentRotation
      if (Math.abs(diff) > 0.01) {
        const step = Math.sign(diff) * Math.min(Math.abs(diff), rotationSpeed * delta)
        state.currentRotation += step
        door.object.rotation.y = state.currentRotation
      }

      // Check proximity for UI feedback (only in first-person)
      if (isFirstPerson) {
        const doorPos = new THREE.Vector3()
        door.object.getWorldPosition(doorPos)
        const dist = camera.position.distanceTo(doorPos)
        if (dist < INTERACTION_DISTANCE && dist < nearestDist) {
          nearestDist = dist
          nearestDoorName = door.type === 'front_left' ? 'Front Left Door' :
                           door.type === 'front_right' ? 'Front Right Door' :
                           door.type === 'rear' ? 'Rear Service Door' : 'Door'
        }
      }
    })

    // Report nearest door for UI
    if (onNearDoorChange) {
      onNearDoorChange(nearestDoorName)
    }
  })

  return null
}

function Scene({ modelUrl, isFirstPerson, onExitFirstPerson, onNearDoorChange }) {
  const controlsRef = useRef()
  const { camera } = useThree()
  const [buildingMeshes, setBuildingMeshes] = useState([])
  const [doorPivots, setDoorPivots] = useState([])

  // Building meshes for collision
  const collisionMeshes = useMemo(() => {
    return buildingMeshes
  }, [buildingMeshes])

  // Handle model load - collect meshes for collision
  const handleModelLoad = useCallback((meshes) => {
    setBuildingMeshes(meshes)
  }, [])

  // Handle door pivots found in model
  const handleDoorsFound = useCallback((doors) => {
    setDoorPivots(doors)
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
      {/* Configure renderer for realistic tone mapping */}
      <ToneMapping />

      {/*
        Minimal ambient light - kept very low so interiors stay dark.
        This represents only indirect sky light that bounces everywhere.
      */}
      <ambientLight intensity={0.08} color="#87CEEB" />

      {/* Main sun light - the primary light source that casts shadows */}
      <directionalLight
        position={sunPosition}
        intensity={2.2}
        castShadow
        shadow-mapSize={[4096, 4096]}
        shadow-camera-far={80}
        shadow-camera-near={0.1}
        shadow-camera-left={-25}
        shadow-camera-right={25}
        shadow-camera-top={25}
        shadow-camera-bottom={-25}
        shadow-bias={-0.0001}
        shadow-normalBias={0.02}
        color="#FFF8E7"
      />

      {/* Secondary fill light - very subtle sky bounce */}
      <directionalLight
        position={[-40, 20, -30]}
        intensity={0.15}
        color="#B4D4E7"
      />

      {/*
        Hemisphere light kept minimal - this doesn't respect geometry
        so we keep it low to avoid unrealistic interior lighting.
      */}
      <hemisphereLight
        skyColor="#87CEEB"
        groundColor="#3a5a3a"
        intensity={0.15}
      />

      {/* Atmospheric fog for depth and realism */}
      <fog attach="fog" args={['#c8d8e8', 60, 200]} />

      {/* Environment map for realistic reflections on surfaces */}
      <Environment preset="sunset" background={false} />

      <Suspense fallback={null}>
        <Model key={modelUrl} url={modelUrl} onLoad={handleModelLoad} onDoorsFound={handleDoorsFound} />
      </Suspense>

      {/* Door animation controller */}
      {doorPivots.length > 0 && (
        <DoorController
          doors={doorPivots}
          isFirstPerson={isFirstPerson}
          onNearDoorChange={onNearDoorChange}
        />
      )}

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

      {/* Ground and trees are now included in the GLB model */}

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

      {/* Post-processing effects for enhanced realism */}
      <EffectComposer>
        {/* Screen-space ambient occlusion - darkens corners and crevices */}
        <SSAO
          blendFunction={BlendFunction.MULTIPLY}
          samples={21}
          radius={7}
          intensity={40}
          luminanceInfluence={0.6}
          color="black"
        />
        {/* Subtle vignette for cinematic look */}
        <Vignette
          offset={0.3}
          darkness={0.4}
          blendFunction={BlendFunction.NORMAL}
        />
      </EffectComposer>
    </>
  )
}

// Lightbox component for full-screen image viewing
function Lightbox({ image, allImages, onClose, onNavigate }) {
  const currentIndex = allImages.findIndex(img => img.file === image.file)

  const goNext = useCallback(() => {
    if (currentIndex < allImages.length - 1) {
      onNavigate(allImages[currentIndex + 1])
    }
  }, [currentIndex, allImages, onNavigate])

  const goPrev = useCallback(() => {
    if (currentIndex > 0) {
      onNavigate(allImages[currentIndex - 1])
    }
  }, [currentIndex, allImages, onNavigate])

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Escape') onClose()
      if (e.code === 'ArrowRight') goNext()
      if (e.code === 'ArrowLeft') goPrev()
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose, goNext, goPrev])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.95)',
        zIndex: 1000,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      onClick={onClose}
    >
      {/* Header */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        right: 20,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        color: 'white',
      }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 18 }}>{image.name}</h3>
          <p style={{ margin: '5px 0 0 0', fontSize: 13, opacity: 0.7 }}>
            {image.category} → {image.subcategory}
          </p>
        </div>
        <div style={{ fontSize: 14, opacity: 0.7 }}>
          {currentIndex + 1} / {allImages.length}
        </div>
      </div>

      {/* Close button */}
      <button
        onClick={onClose}
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
          background: 'rgba(255, 255, 255, 0.1)',
          border: 'none',
          color: 'white',
          fontSize: 24,
          width: 40,
          height: 40,
          borderRadius: 20,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        ×
      </button>

      {/* Image */}
      <img
        src={image.file}
        alt={image.name}
        style={{
          maxWidth: '90%',
          maxHeight: '80%',
          objectFit: 'contain',
          borderRadius: 4,
        }}
        onClick={(e) => e.stopPropagation()}
      />

      {/* Navigation arrows */}
      {currentIndex > 0 && (
        <button
          onClick={(e) => { e.stopPropagation(); goPrev() }}
          style={{
            position: 'absolute',
            left: 20,
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'rgba(255, 255, 255, 0.1)',
            border: 'none',
            color: 'white',
            fontSize: 32,
            width: 50,
            height: 80,
            borderRadius: 8,
            cursor: 'pointer',
          }}
        >
          ‹
        </button>
      )}
      {currentIndex < allImages.length - 1 && (
        <button
          onClick={(e) => { e.stopPropagation(); goNext() }}
          style={{
            position: 'absolute',
            right: 20,
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'rgba(255, 255, 255, 0.1)',
            border: 'none',
            color: 'white',
            fontSize: 32,
            width: 50,
            height: 80,
            borderRadius: 8,
            cursor: 'pointer',
          }}
        >
          ›
        </button>
      )}

      {/* Keyboard hints */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        color: 'white',
        fontSize: 12,
        opacity: 0.6,
      }}>
        <span style={{ marginRight: 20 }}>← → Navigate</span>
        <span>ESC Close</span>
      </div>
    </div>
  )
}

// Reference Panel - compact bottom-right panel
function ReferencePanel({ onClose, onOpenGallery, onSelectImage }) {
  const [activeCategory, setActiveCategory] = useState('Exterior')
  const categoryData = REFERENCES[activeCategory]

  return (
    <div style={{
      position: 'absolute',
      bottom: 20,
      right: 20,
      background: 'rgba(0, 0, 0, 0.9)',
      borderRadius: 8,
      color: 'white',
      width: 320,
      maxHeight: '60vh',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '12px 15px',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <h3 style={{ margin: 0, fontSize: 14 }}>Reference Images</h3>
        <div>
          <button
            onClick={onOpenGallery}
            style={{
              background: 'rgba(255,255,255,0.1)',
              border: 'none',
              color: 'white',
              padding: '4px 10px',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 11,
              marginRight: 8,
            }}
          >
            View All
          </button>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              fontSize: 18,
              cursor: 'pointer',
              padding: '0 4px',
            }}
          >
            ×
          </button>
        </div>
      </div>

      {/* Category tabs */}
      <div style={{
        display: 'flex',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
      }}>
        {Object.keys(REFERENCES).map(category => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            style={{
              flex: 1,
              background: activeCategory === category ? 'rgba(74, 111, 165, 0.8)' : 'transparent',
              border: 'none',
              color: 'white',
              padding: '10px 8px',
              cursor: 'pointer',
              fontSize: 12,
              transition: 'background 0.2s',
            }}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Thumbnails */}
      <div style={{
        padding: 10,
        overflowY: 'auto',
        flex: 1,
      }}>
        {Object.entries(categoryData.subcategories).map(([subcategory, images]) => (
          <div key={subcategory} style={{ marginBottom: 15 }}>
            <p style={{ margin: '0 0 8px 0', fontSize: 11, opacity: 0.6 }}>{subcategory}</p>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: 6,
            }}>
              {images.map(image => (
                <div
                  key={image.file}
                  onClick={() => onSelectImage({ ...image, category: activeCategory, subcategory })}
                  style={{
                    aspectRatio: '4/3',
                    borderRadius: 4,
                    overflow: 'hidden',
                    cursor: 'pointer',
                    position: 'relative',
                  }}
                >
                  <img
                    src={image.file}
                    alt={image.name}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                    }}
                    loading="lazy"
                  />
                  <div style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    background: 'linear-gradient(transparent, rgba(0,0,0,0.8))',
                    padding: '15px 4px 4px 4px',
                    fontSize: 9,
                    textAlign: 'center',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                  }}>
                    {image.name}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Footer hint */}
      <div style={{
        padding: '8px 15px',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        fontSize: 11,
        opacity: 0.5,
        textAlign: 'center',
      }}>
        Press <span style={{ fontFamily: 'monospace', background: 'rgba(255,255,255,0.1)', padding: '1px 5px', borderRadius: 3 }}>R</span> to toggle
      </div>
    </div>
  )
}

// Full-screen Reference Gallery
function ReferenceGallery({ onClose, onSelectImage }) {
  const [activeCategory, setActiveCategory] = useState('Exterior')

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.95)',
      zIndex: 900,
      display: 'flex',
      flexDirection: 'column',
      color: 'white',
    }}>
      {/* Header */}
      <div style={{
        padding: '20px 30px',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 22 }}>Reference Images</h2>
          <p style={{ margin: '5px 0 0 0', fontSize: 13, opacity: 0.6 }}>
            Compare the 3D model with original reference images
          </p>
        </div>
        <button
          onClick={onClose}
          style={{
            background: 'rgba(255,255,255,0.1)',
            border: 'none',
            color: 'white',
            fontSize: 16,
            padding: '8px 16px',
            borderRadius: 6,
            cursor: 'pointer',
          }}
        >
          Close (ESC)
        </button>
      </div>

      {/* Category tabs */}
      <div style={{
        display: 'flex',
        padding: '0 30px',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
      }}>
        {Object.entries(REFERENCES).map(([category, data]) => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            style={{
              background: activeCategory === category ? 'rgba(74, 111, 165, 0.8)' : 'transparent',
              border: 'none',
              color: 'white',
              padding: '15px 25px',
              cursor: 'pointer',
              fontSize: 14,
              borderBottom: activeCategory === category ? '2px solid #4a6fa5' : '2px solid transparent',
              marginBottom: -1,
            }}
          >
            {category}
            <span style={{ fontSize: 11, opacity: 0.6, marginLeft: 8 }}>
              {Object.values(data.subcategories).flat().length}
            </span>
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: 30,
      }}>
        <p style={{ margin: '0 0 20px 0', fontSize: 14, opacity: 0.7 }}>
          {REFERENCES[activeCategory].description}
        </p>

        {Object.entries(REFERENCES[activeCategory].subcategories).map(([subcategory, images]) => (
          <div key={subcategory} style={{ marginBottom: 30 }}>
            <h4 style={{ margin: '0 0 15px 0', fontSize: 16, opacity: 0.8 }}>{subcategory}</h4>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
              gap: 15,
            }}>
              {images.map(image => (
                <div
                  key={image.file}
                  onClick={() => onSelectImage({ ...image, category: activeCategory, subcategory })}
                  style={{
                    aspectRatio: '4/3',
                    borderRadius: 8,
                    overflow: 'hidden',
                    cursor: 'pointer',
                    position: 'relative',
                    background: '#1a1a1a',
                  }}
                >
                  <img
                    src={image.file}
                    alt={image.name}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                      transition: 'transform 0.2s',
                    }}
                    loading="lazy"
                    onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                    onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
                  />
                  <div style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    background: 'linear-gradient(transparent, rgba(0,0,0,0.9))',
                    padding: '25px 12px 12px 12px',
                    fontSize: 13,
                  }}>
                    {image.name}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Loading screen component - styled to match the outdoor scene
// Uses delayed appearance to avoid flashing for quick loads
const LOADER_DELAY = 300 // ms before showing loader
const LOADER_MIN_DISPLAY = 500 // minimum ms to show loader once visible

function Loader() {
  const { progress, active } = useProgress()
  const [visible, setVisible] = useState(false) // Whether loader is rendered
  const [fadeOut, setFadeOut] = useState(false)
  const showTimerRef = useRef(null)
  const visibleSinceRef = useRef(null)
  const isInitialLoad = useRef(true)

  useEffect(() => {
    // Initial page load - show immediately (no delay for first load)
    if (isInitialLoad.current && active) {
      setVisible(true)
      setFadeOut(false)
      visibleSinceRef.current = Date.now()
      isInitialLoad.current = false
      return
    }

    // When loading starts (model switch), set delayed show timer
    if (active) {
      setFadeOut(false)
      showTimerRef.current = setTimeout(() => {
        setVisible(true)
        visibleSinceRef.current = Date.now()
      }, LOADER_DELAY)

      return () => {
        if (showTimerRef.current) {
          clearTimeout(showTimerRef.current)
          showTimerRef.current = null
        }
      }
    }

    // When loading completes
    if (!active && progress === 100) {
      // Clear any pending show timer (load finished before delay)
      if (showTimerRef.current) {
        clearTimeout(showTimerRef.current)
        showTimerRef.current = null
      }

      // If loader is visible, ensure minimum display time before fading
      if (visible && visibleSinceRef.current) {
        const elapsed = Date.now() - visibleSinceRef.current
        const remaining = Math.max(0, LOADER_MIN_DISPLAY - elapsed)

        const fadeTimer = setTimeout(() => {
          setFadeOut(true)
          // Hide completely after fade animation
          setTimeout(() => {
            setVisible(false)
            visibleSinceRef.current = null
          }, 500)
        }, remaining)

        return () => clearTimeout(fadeTimer)
      }
    }
  }, [active, progress, visible])

  if (!visible) return null

  // Simple tree silhouette component
  const TreeSilhouette = ({ left, height, scale = 1 }) => (
    <div style={{
      position: 'absolute',
      bottom: 80,
      left: `${left}%`,
      transform: 'translateX(-50%)',
    }}>
      {/* Trunk */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 8 * scale,
        height: height * 0.3 * scale,
        background: '#4a5d3a',
        borderRadius: 2,
      }} />
      {/* Foliage layers */}
      <div style={{
        position: 'absolute',
        bottom: height * 0.2 * scale,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 0,
        height: 0,
        borderLeft: `${25 * scale}px solid transparent`,
        borderRight: `${25 * scale}px solid transparent`,
        borderBottom: `${height * 0.5 * scale}px solid #3d5c3d`,
      }} />
      <div style={{
        position: 'absolute',
        bottom: height * 0.4 * scale,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 0,
        height: 0,
        borderLeft: `${20 * scale}px solid transparent`,
        borderRight: `${20 * scale}px solid transparent`,
        borderBottom: `${height * 0.4 * scale}px solid #4a6b4a`,
      }} />
      <div style={{
        position: 'absolute',
        bottom: height * 0.55 * scale,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 0,
        height: 0,
        borderLeft: `${14 * scale}px solid transparent`,
        borderRight: `${14 * scale}px solid transparent`,
        borderBottom: `${height * 0.3 * scale}px solid #5a7a5a`,
      }} />
    </div>
  )

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'linear-gradient(to bottom, #87CEEB 0%, #a8d8ea 40%, #E0F6FF 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 2000,
        opacity: fadeOut ? 0 : 1,
        transition: 'opacity 0.5s ease-out',
        pointerEvents: fadeOut ? 'none' : 'auto',
        overflow: 'hidden',
      }}
    >
      {/* Sun glow */}
      <div style={{
        position: 'absolute',
        top: '15%',
        right: '20%',
        width: 80,
        height: 80,
        background: 'radial-gradient(circle, rgba(255,245,225,0.9) 0%, rgba(255,245,225,0.3) 40%, transparent 70%)',
        borderRadius: '50%',
      }} />

      {/* Building silhouette */}
      <div style={{
        position: 'absolute',
        bottom: 80,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}>
        {/* Roof */}
        <div style={{
          width: 0,
          height: 0,
          borderLeft: '90px solid transparent',
          borderRight: '90px solid transparent',
          borderBottom: '50px solid #5a6a7a',
        }} />
        {/* Building body */}
        <div style={{
          width: 160,
          height: 70,
          background: '#6a7a8a',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'flex-end',
          gap: 15,
          paddingBottom: 10,
        }}>
          {/* Windows */}
          <div style={{ width: 20, height: 25, background: '#4a5a6a', borderRadius: 2 }} />
          <div style={{ width: 25, height: 40, background: '#4a5a6a', borderRadius: '2px 2px 0 0' }} />
          <div style={{ width: 20, height: 25, background: '#4a5a6a', borderRadius: 2 }} />
        </div>
      </div>

      {/* Trees - scattered around */}
      <TreeSilhouette left={12} height={100} scale={1.2} />
      <TreeSilhouette left={22} height={80} scale={0.9} />
      <TreeSilhouette left={78} height={90} scale={1.0} />
      <TreeSilhouette left={88} height={110} scale={1.3} />
      <TreeSilhouette left={8} height={70} scale={0.7} />
      <TreeSilhouette left={92} height={75} scale={0.8} />

      {/* Ground layers */}
      {/* Road */}
      <div style={{
        position: 'absolute',
        bottom: 60,
        left: 0,
        right: 0,
        height: 20,
        background: '#4a4a4a',
      }} />
      {/* Dirt/gravel */}
      <div style={{
        position: 'absolute',
        bottom: 30,
        left: 0,
        right: 0,
        height: 30,
        background: '#7a7060',
      }} />
      {/* Grass */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 30,
        background: '#5a7a4a',
      }} />

      {/* Title - positioned in the sky area */}
      <div style={{
        position: 'absolute',
        top: '25%',
        textAlign: 'center',
      }}>
        <h1 style={{
          color: '#2a4a6a',
          fontSize: 36,
          fontWeight: 300,
          margin: '0 0 8px 0',
          letterSpacing: 3,
          textShadow: '0 2px 10px rgba(255,255,255,0.5)',
        }}>
          Building Viewer
        </h1>

        <p style={{
          color: '#4a6a8a',
          fontSize: 14,
          margin: 0,
        }}>
          Loading 3D Model...
        </p>
      </div>

      {/* Progress container - positioned above the scene */}
      <div style={{
        position: 'absolute',
        top: '45%',
        width: 280,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}>
        {/* Progress bar background */}
        <div style={{
          width: '100%',
          height: 6,
          background: 'rgba(42, 74, 106, 0.2)',
          borderRadius: 3,
          overflow: 'hidden',
          boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.1)',
        }}>
          {/* Progress bar fill */}
          <div style={{
            width: `${progress}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #4a6fa5, #5a8fc7)',
            borderRadius: 3,
            transition: 'width 0.3s ease-out',
            boxShadow: '0 0 10px rgba(74, 111, 165, 0.5)',
          }} />
        </div>

        {/* Progress percentage */}
        <p style={{
          color: '#3a5a7a',
          fontSize: 14,
          marginTop: 12,
          fontFamily: 'monospace',
          fontWeight: 500,
        }}>
          {Math.round(progress)}%
        </p>
      </div>

      {/* Hint text - on the grass */}
      <p style={{
        position: 'absolute',
        bottom: 8,
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 11,
        textShadow: '0 1px 2px rgba(0,0,0,0.3)',
      }}>
        Use orbit controls to explore the building
      </p>
    </div>
  )
}

export default function App() {
  const [selectedModel, setSelectedModel] = useState(0)
  const [isFirstPerson, setIsFirstPerson] = useState(false)
  const [showReferencePanel, setShowReferencePanel] = useState(false)
  const [showReferenceGallery, setShowReferenceGallery] = useState(false)
  const [lightboxImage, setLightboxImage] = useState(null)
  const [nearDoor, setNearDoor] = useState(null)

  // Toggle mode with F key
  const toggleMode = useCallback(() => {
    setIsFirstPerson(prev => !prev)
  }, [])

  // Toggle reference panel with R key, gallery with Shift+R
  const toggleReferencePanel = useCallback(() => {
    setShowReferencePanel(prev => !prev)
  }, [])

  const openReferenceGallery = useCallback(() => {
    setShowReferencePanel(false)
    setShowReferenceGallery(true)
  }, [])

  const handleImageSelect = useCallback((image) => {
    setLightboxImage(image)
  }, [])

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't handle keys when lightbox or gallery is open (they handle their own keys)
      if (lightboxImage) return

      if (e.code === 'KeyF' && !e.repeat) {
        toggleMode()
      }
      if (e.code === 'KeyR' && !e.repeat) {
        if (e.shiftKey) {
          openReferenceGallery()
        } else {
          if (showReferenceGallery) {
            setShowReferenceGallery(false)
          } else {
            toggleReferencePanel()
          }
        }
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [toggleMode, toggleReferencePanel, openReferenceGallery, showReferenceGallery, lightboxImage])

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        shadows="soft"
        gl={{
          antialias: true,
          shadowMap: { type: THREE.PCFSoftShadowMap }
        }}
        camera={{ position: [20, 15, 20], fov: 50 }}
        style={{ background: 'linear-gradient(to bottom, #87CEEB, #E0F6FF)' }}
      >
        <Scene
          modelUrl={ALL_MODELS[selectedModel].file}
          isFirstPerson={isFirstPerson}
          onExitFirstPerson={() => setIsFirstPerson(false)}
          onNearDoorChange={setNearDoor}
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
          {isFirstPerson ? 'WASD to move | Mouse to look' : 'Drag to rotate | Scroll to zoom'}
        </p>
        <p style={{ margin: '8px 0 0 0', fontSize: 11, opacity: 0.5 }}>
          Press <span style={{ fontFamily: 'monospace', background: 'rgba(255,255,255,0.1)', padding: '1px 5px', borderRadius: 3 }}>R</span> for references
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

      {/* Door Interaction Indicator */}
      {isFirstPerson && nearDoor && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'rgba(0, 0, 0, 0.8)',
          padding: '15px 25px',
          borderRadius: 8,
          color: 'white',
          textAlign: 'center',
          border: '2px solid rgba(74, 111, 165, 0.8)',
          pointerEvents: 'none',
        }}>
          <p style={{ margin: 0, fontSize: 14, fontWeight: 'bold' }}>
            {nearDoor}
          </p>
          <p style={{ margin: '8px 0 0 0', fontSize: 13 }}>
            Press <span style={{
              background: 'rgba(74, 111, 165, 0.8)',
              padding: '3px 10px',
              borderRadius: 4,
              fontFamily: 'monospace',
              fontWeight: 'bold',
              marginLeft: 4,
              marginRight: 4,
            }}>E</span> to open/close
          </p>
        </div>
      )}

      {/* Reference Panel - Bottom right */}
      {showReferencePanel && !showReferenceGallery && (
        <ReferencePanel
          onClose={() => setShowReferencePanel(false)}
          onOpenGallery={openReferenceGallery}
          onSelectImage={handleImageSelect}
        />
      )}

      {/* Reference Gallery - Full screen modal */}
      {showReferenceGallery && (
        <ReferenceGallery
          onClose={() => setShowReferenceGallery(false)}
          onSelectImage={handleImageSelect}
        />
      )}

      {/* Lightbox - Full screen image viewer */}
      {lightboxImage && (
        <Lightbox
          image={lightboxImage}
          allImages={ALL_REFERENCES}
          onClose={() => setLightboxImage(null)}
          onNavigate={setLightboxImage}
        />
      )}

      {/* Loading screen overlay */}
      <Loader />
    </div>
  )
}
