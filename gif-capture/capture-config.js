// Configuration for GIF capture - key milestones showing building evolution

// Camera presets
export const CAMERAS = {
  // 3/4 elevated view - good for overall building shape
  corner: {
    position: [28, 20, 28],
    target: [0, 4, 0],
    fov: 42
  },
  // Front view - good for window/door details
  front: {
    position: [0, 2, 17],
    target: [0, 4, -5],
    fov: 45
  }
};

export const config = {
  // Default camera (used if milestone doesn't specify one)
  defaultCamera: CAMERAS.corner,

  // Viewport settings
  viewport: {
    width: 1920,
    height: 1080
  },

  // Timing settings
  frameDelay: 400,           // 0.4 seconds per frame in final GIF
  captureStabilizationMs: 1200,  // Wait for render to stabilize after load

  // Server settings
  serverUrl: 'http://localhost:5173',

  // Key milestones - 30 frames total
  milestones: [
    // === CORNER VIEW: Early & Phase 1A (8 frames) ===
    { file: 'building_iter_001.glb', phase: 'Early', description: 'Initial geometry', camera: CAMERAS.corner },
    { file: 'building_iter_003.glb', phase: 'Early', description: 'Base form established', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_004.glb', phase: '1A', description: 'Phase 1A begins', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_010.glb', phase: '1A', description: 'Walls developing', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_017.glb', phase: '1A', description: 'Wall cutouts', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_038.glb', phase: '1A', description: 'Canopy/parapet', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_043.glb', phase: '1A', description: 'Chimney added', camera: CAMERAS.corner },
    { file: 'building_phase_1a_iter_049.glb', phase: '1A', description: 'Phase 1A complete', camera: CAMERAS.corner },

    // === FRONT VIEW: Phase 1B & 1C (10 frames) ===
    { file: 'building_phase_1b_iter_001.glb', phase: '1B', description: 'Window frames begin', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_005.glb', phase: '1B', description: 'Frames progressing', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_010.glb', phase: '1B', description: 'More windows filled', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_013.glb', phase: '1B', description: 'All openings filled', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_015.glb', phase: '1B', description: 'Window trim detail', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_020.glb', phase: '1B', description: 'Door hardware', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_025.glb', phase: '1B', description: 'Hardware refinement', camera: CAMERAS.front },
    { file: 'building_phase_1b_iter_030.glb', phase: '1B', description: 'Phase 1B complete', camera: CAMERAS.front },
    { file: 'building_phase_1c_iter_001.glb', phase: '1C', description: 'Interior begins', camera: CAMERAS.front },
    { file: 'building_phase_1c_iter_007.glb', phase: '1C', description: 'Phase 1C complete', camera: CAMERAS.front },

    // === CORNER VIEW: Phase 2 & 3 (5 frames) ===
    { file: 'building_phase_2_iter_001.glb', phase: '2', description: 'Materials begin', camera: CAMERAS.corner },
    { file: 'building_phase_2_iter_008.glb', phase: '2', description: 'Mid-materials', camera: CAMERAS.corner },
    { file: 'building_phase_2_iter_015.glb', phase: '2', description: 'Phase 2 complete', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_001.glb', phase: '3', description: 'Environment begins', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final version', camera: CAMERAS.corner },

    // === HOLD FINAL FRAME (7 frames = ~3 seconds) ===
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
    { file: 'building_phase_3_iter_004.glb', phase: '3', description: 'Final (hold)', camera: CAMERAS.corner },
  ]
};

export default config;
