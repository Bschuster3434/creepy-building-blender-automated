// FIXED ROTATION - move position only, camera direction stays same
import { chromium } from 'playwright';
import { config } from './capture-config.js';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function testCameras() {
  console.log('Step 1: Get rotation from original camera...\n');

  const testDir = path.join(__dirname, 'test-views');
  if (!fs.existsSync(testDir)) {
    fs.mkdirSync(testDir, { recursive: true });
  }

  const existing = fs.readdirSync(testDir).filter(f => f.endsWith('.png'));
  for (const file of existing) {
    fs.unlinkSync(path.join(testDir, file));
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--use-gl=egl']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();
  const testModel = 'building_phase_1b_iter_015.glb';

  // First, load with original settings and extract the camera rotation
  const originalPos = [28, 20, 28];
  const originalTarget = [0, 4, 0];

  let url = `${config.serverUrl}?model=${testModel}&capture=true&camPos=${originalPos.join(',')}&camTarget=${originalTarget.join(',')}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForFunction(() => window.__MODEL_LOADED__ === true, { timeout: 60000 });
  await page.waitForTimeout(1500);

  // Extract the camera rotation after lookAt was applied
  const rotation = await page.evaluate(() => {
    // Access Three.js camera through the canvas
    const canvas = document.querySelector('canvas');
    if (canvas && canvas.__three_camera__) {
      const cam = canvas.__three_camera__;
      return [cam.rotation.x, cam.rotation.y, cam.rotation.z];
    }
    // Try alternate method - look for global reference
    if (window.__THREE_CAMERA_ROTATION__) {
      return window.__THREE_CAMERA_ROTATION__;
    }
    return null;
  });

  console.log('Extracted rotation:', rotation);

  // Take reference screenshot
  await page.screenshot({ path: path.join(testDir, '00_original.png'), type: 'png' });
  console.log('Saved: 00_original.png\n');

  // If we couldn't get rotation, calculate it manually
  // Camera at [28, 20, 28] looking at [0, 4, 0]
  // Direction: [-28, -16, -28] normalized
  // For a camera looking from +X+Z quadrant toward origin:
  // yaw (Y rotation) = atan2(-28, -28) + PI = atan2(1, 1) = PI/4...
  // Actually let's use the known working values from typical Three.js setup

  // Since we can't easily extract rotation, let's compute it:
  // The camera is at 45 degrees in XZ plane (equal X and Z)
  // Looking toward origin, so yaw should be about -135 degrees = -2.356 radians
  // Pitch is looking down, about -20 degrees = -0.35 radians

  // Actually, let's just use camTarget and move the camera around a MUCH larger area
  // The issue before was the offsets weren't big enough

  console.log('Step 2: Testing positions with LARGE offsets...\n');

  // Move camera position in much larger steps
  const X_OFFSETS = [-60, -30, 0, 30, 60];
  const Z_OFFSETS = [-60, -30, 0, 30, 60];

  let frameNum = 1;
  for (const zOff of Z_OFFSETS) {
    for (const xOff of X_OFFSETS) {
      const pos = [originalPos[0] + xOff, originalPos[1], originalPos[2] + zOff];
      const target = [originalTarget[0] + xOff, originalTarget[1], originalTarget[2] + zOff];

      console.log(`[${String(frameNum).padStart(2, '0')}/25] pos=[${pos.join(',')}]`);

      await page.evaluate(() => { window.__MODEL_LOADED__ = false; });

      url = `${config.serverUrl}?model=${testModel}&capture=true&camPos=${pos.join(',')}&camTarget=${target.join(',')}`;
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForFunction(() => window.__MODEL_LOADED__ === true, { timeout: 60000 });
      await page.waitForTimeout(1000);

      const filename = `${String(frameNum).padStart(2, '0')}_x${xOff >= 0 ? '+' : ''}${xOff}_z${zOff >= 0 ? '+' : ''}${zOff}.png`;
      await page.screenshot({ path: path.join(testDir, filename), type: 'png' });

      frameNum++;
    }
  }

  await browser.close();
  console.log('\nDone! Check test-views/');
  console.log('The building should appear in one of these frames as we sweep across the scene.');
}

testCameras().catch(console.error);
