import { chromium } from 'playwright';
import { config } from './capture-config.js';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureFrame(milestone, frameNumber, framesDir) {
  const camera = milestone.camera || config.defaultCamera;

  console.log(`\n[${frameNumber}/${config.milestones.length}] Capturing: ${milestone.file}`);
  console.log(`  Phase: ${milestone.phase} - ${milestone.description}`);
  console.log(`  Camera: pos=[${camera.position.join(',')}] target=[${camera.target.join(',')}] fov=${camera.fov}`);

  // Fresh browser for each frame to ensure camera params are applied
  const browser = await chromium.launch({
    headless: true,
    args: ['--use-gl=egl']
  });

  const context = await browser.newContext({
    viewport: {
      width: config.viewport.width,
      height: config.viewport.height
    },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();

  try {
    const camPos = camera.position.join(',');
    const camTarget = camera.target.join(',');
    const url = `${config.serverUrl}?model=${milestone.file}&capture=true&camPos=${camPos}&camTarget=${camTarget}&camFov=${camera.fov}`;

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    console.log('  Waiting for model to load...');
    await page.waitForFunction(
      () => window.__MODEL_LOADED__ === true,
      { timeout: 60000 }
    );

    console.log('  Waiting for render to stabilize...');
    await page.waitForTimeout(config.captureStabilizationMs);

    const paddedNumber = String(frameNumber).padStart(3, '0');
    const screenshotPath = path.join(framesDir, `frame_${paddedNumber}.png`);
    await page.screenshot({
      path: screenshotPath,
      type: 'png'
    });

    console.log(`  Saved: frame_${paddedNumber}.png`);

  } catch (error) {
    console.error(`  ERROR capturing ${milestone.file}: ${error.message}`);
  } finally {
    await browser.close();
  }
}

async function captureFrames() {
  console.log('Starting frame capture...');
  console.log(`Total frames to capture: ${config.milestones.length}`);

  const framesDir = path.join(__dirname, 'frames');
  if (!fs.existsSync(framesDir)) {
    fs.mkdirSync(framesDir, { recursive: true });
  }

  // Clear existing frames
  const existingFrames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png'));
  for (const frame of existingFrames) {
    fs.unlinkSync(path.join(framesDir, frame));
  }
  console.log(`Cleared ${existingFrames.length} existing frames`);

  // Capture each milestone with fresh browser
  for (let i = 0; i < config.milestones.length; i++) {
    await captureFrame(config.milestones[i], i + 1, framesDir);
  }

  // Summary
  const capturedFrames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png')).length;
  console.log(`\n${'='.repeat(50)}`);
  console.log(`Capture complete!`);
  console.log(`Frames captured: ${capturedFrames}/${config.milestones.length}`);
  console.log(`Output directory: ${framesDir}`);
  console.log(`\nRun 'make-gif.bat' to create the GIF`);
}

captureFrames().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
