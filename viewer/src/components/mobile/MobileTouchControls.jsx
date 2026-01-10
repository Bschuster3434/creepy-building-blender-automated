import React, { useRef, useCallback, useEffect, useState } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Virtual joystick for mobile movement control
 * Rendered outside of Canvas as HTML overlay
 */
export function VirtualJoystick({ onMove, size = 120 }) {
  const joystickRef = useRef(null)
  const knobRef = useRef(null)
  const [isActive, setIsActive] = useState(false)
  const touchIdRef = useRef(null)
  const centerRef = useRef({ x: 0, y: 0 })

  const maxDistance = size / 2 - 20 // Max knob movement from center

  const handleTouchStart = useCallback((e) => {
    if (touchIdRef.current !== null) return // Already tracking a touch

    const touch = e.touches[0]
    const rect = joystickRef.current.getBoundingClientRect()
    centerRef.current = {
      x: rect.left + rect.width / 2,
      y: rect.top + rect.height / 2
    }
    touchIdRef.current = touch.identifier
    setIsActive(true)

    // Initial position
    handleTouchMove(e)
  }, [])

  const handleTouchMove = useCallback((e) => {
    if (touchIdRef.current === null) return

    const touch = Array.from(e.touches).find(t => t.identifier === touchIdRef.current)
    if (!touch) return

    e.preventDefault()

    const dx = touch.clientX - centerRef.current.x
    const dy = touch.clientY - centerRef.current.y
    const distance = Math.sqrt(dx * dx + dy * dy)
    const clampedDistance = Math.min(distance, maxDistance)

    // Normalize direction
    const angle = Math.atan2(dy, dx)
    const clampedX = Math.cos(angle) * clampedDistance
    const clampedY = Math.sin(angle) * clampedDistance

    // Update knob position
    if (knobRef.current) {
      knobRef.current.style.transform = `translate(${clampedX}px, ${clampedY}px)`
    }

    // Send normalized movement (-1 to 1)
    const normalizedX = clampedX / maxDistance
    const normalizedY = -clampedY / maxDistance // Invert Y for forward movement

    onMove({ x: normalizedX, y: normalizedY })
  }, [maxDistance, onMove])

  const handleTouchEnd = useCallback((e) => {
    const touch = Array.from(e.changedTouches).find(t => t.identifier === touchIdRef.current)
    if (!touch) return

    touchIdRef.current = null
    setIsActive(false)

    // Reset knob position
    if (knobRef.current) {
      knobRef.current.style.transform = 'translate(0px, 0px)'
    }

    onMove({ x: 0, y: 0 })
  }, [onMove])

  return (
    <div
      ref={joystickRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      style={{
        position: 'absolute',
        bottom: 30,
        left: 30,
        width: size,
        height: size,
        borderRadius: '50%',
        background: 'rgba(255, 255, 255, 0.15)',
        border: '2px solid rgba(255, 255, 255, 0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        touchAction: 'none',
        userSelect: 'none',
        WebkitUserSelect: 'none',
      }}
    >
      <div
        ref={knobRef}
        style={{
          width: 50,
          height: 50,
          borderRadius: '50%',
          background: isActive
            ? 'rgba(74, 111, 165, 0.9)'
            : 'rgba(255, 255, 255, 0.5)',
          border: '2px solid rgba(255, 255, 255, 0.6)',
          transition: isActive ? 'none' : 'transform 0.2s ease-out',
          boxShadow: isActive ? '0 0 15px rgba(74, 111, 165, 0.5)' : 'none',
        }}
      />
    </div>
  )
}

/**
 * Touch look area for camera rotation
 * Takes up most of the screen for easy look-around
 */
export function TouchLookArea({ onLook, sensitivity = 0.003 }) {
  const areaRef = useRef(null)
  const lastTouchRef = useRef(null)
  const touchIdRef = useRef(null)

  const handleTouchStart = useCallback((e) => {
    // Ignore if touch started on UI elements
    if (e.target !== areaRef.current) return
    if (touchIdRef.current !== null) return

    const touch = e.touches[0]
    touchIdRef.current = touch.identifier
    lastTouchRef.current = { x: touch.clientX, y: touch.clientY }
  }, [])

  const handleTouchMove = useCallback((e) => {
    if (touchIdRef.current === null) return

    const touch = Array.from(e.touches).find(t => t.identifier === touchIdRef.current)
    if (!touch || !lastTouchRef.current) return

    const dx = touch.clientX - lastTouchRef.current.x
    const dy = touch.clientY - lastTouchRef.current.y

    lastTouchRef.current = { x: touch.clientX, y: touch.clientY }

    // Send rotation delta
    onLook({ x: -dx * sensitivity, y: -dy * sensitivity })
  }, [sensitivity, onLook])

  const handleTouchEnd = useCallback((e) => {
    const touch = Array.from(e.changedTouches).find(t => t.identifier === touchIdRef.current)
    if (!touch) return

    touchIdRef.current = null
    lastTouchRef.current = null
  }, [])

  return (
    <div
      ref={areaRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      style={{
        position: 'absolute',
        top: 80,
        left: 0,
        right: 0,
        bottom: 180,
        touchAction: 'none',
        userSelect: 'none',
        WebkitUserSelect: 'none',
      }}
    />
  )
}

/**
 * First-person movement controller for mobile
 * Uses touch inputs instead of keyboard/mouse
 */
export function MobileFirstPersonMovement({
  speed = 5,
  collisionMeshes = [],
  moveInput,
  lookInput
}) {
  const { camera } = useThree()
  const raycaster = useRef(new THREE.Raycaster())
  const euler = useRef(new THREE.Euler(0, 0, 0, 'YXZ'))

  const COLLISION_DISTANCE = 1.5
  const PUSH_BACK_DISTANCE = 0.8

  // Initialize camera rotation from current orientation
  useEffect(() => {
    euler.current.setFromQuaternion(camera.quaternion)
  }, [camera])

  // Check collision in a given direction
  const checkCollision = useCallback((directionVec, distance = COLLISION_DISTANCE) => {
    if (collisionMeshes.length === 0) return { blocked: false, closest: Infinity }

    const heights = [0.3, 0.8, 1.4]
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
  }, [camera, collisionMeshes])

  useFrame((_, delta) => {
    // Apply look rotation
    if (lookInput.x !== 0 || lookInput.y !== 0) {
      euler.current.y += lookInput.x
      euler.current.x += lookInput.y

      // Clamp vertical rotation
      euler.current.x = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, euler.current.x))

      camera.quaternion.setFromEuler(euler.current)
    }

    // Get movement direction based on camera orientation
    const cameraDirection = new THREE.Vector3()
    camera.getWorldDirection(cameraDirection)
    cameraDirection.y = 0
    cameraDirection.normalize()

    const cameraRight = new THREE.Vector3()
    cameraRight.crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0))

    // Push back if too close to walls
    const directions = [
      { dir: cameraDirection.clone(), name: 'forward' },
      { dir: cameraDirection.clone().negate(), name: 'backward' },
      { dir: cameraRight.clone(), name: 'right' },
      { dir: cameraRight.clone().negate(), name: 'left' },
    ]

    for (const { dir } of directions) {
      const { closest } = checkCollision(dir, PUSH_BACK_DISTANCE)
      if (closest < PUSH_BACK_DISTANCE) {
        const pushStrength = Math.max(0.1, (PUSH_BACK_DISTANCE - closest) * 0.5)
        const pushBack = dir.clone().negate().multiplyScalar(pushStrength)
        camera.position.add(pushBack)
      }
    }

    // Apply movement from joystick
    if (moveInput.x !== 0 || moveInput.y !== 0) {
      const moveSpeed = speed * delta

      // Forward/backward (joystick Y)
      if (Math.abs(moveInput.y) > 0.1) {
        const moveDir = moveInput.y > 0
          ? cameraDirection.clone()
          : cameraDirection.clone().negate()
        const { blocked } = checkCollision(moveDir)
        if (!blocked) {
          camera.position.add(moveDir.multiplyScalar(moveSpeed * Math.abs(moveInput.y)))
        }
      }

      // Strafe left/right (joystick X)
      if (Math.abs(moveInput.x) > 0.1) {
        const moveDir = moveInput.x > 0
          ? cameraRight.clone()
          : cameraRight.clone().negate()
        const { blocked } = checkCollision(moveDir)
        if (!blocked) {
          camera.position.add(moveDir.multiplyScalar(moveSpeed * Math.abs(moveInput.x)))
        }
      }
    }

    // Keep camera at eye level
    camera.position.y = 1.7
  })

  return null
}

/**
 * Action button for mobile interactions (doors, etc.)
 */
export function MobileActionButton({ label, onPress, visible = true }) {
  if (!visible) return null

  return (
    <button
      onTouchStart={(e) => {
        e.preventDefault()
        onPress()
      }}
      style={{
        position: 'absolute',
        bottom: 30,
        right: 30,
        width: 80,
        height: 80,
        borderRadius: '50%',
        background: 'rgba(74, 111, 165, 0.9)',
        border: '3px solid rgba(255, 255, 255, 0.5)',
        color: 'white',
        fontSize: 14,
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        touchAction: 'none',
        userSelect: 'none',
        WebkitUserSelect: 'none',
        boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)',
        cursor: 'pointer',
      }}
    >
      {label}
    </button>
  )
}
