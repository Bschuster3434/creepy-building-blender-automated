// Quick capture - first 5 frames only
import { chromium } from 'playwright';
import { config } from './capture-config.js';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureFrames() {
  const FRAME_COUNT = 5;
  console.log(`Capturing first ${FRAME_COUNT} frames...`);

  const framesDir = path.join(__dirname, 'frames');
  if (!fs.existsSync(framesDir)) {
    fs.mkdirSync(framesDir, { recursive: true });
  }

  // Clear existing frames
  const existingFrames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png'));
  for (const frame of existingFrames) {
    fs.unlinkSync(path.join(framesDir, frame));
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--use-gl=egl']
  });

  const context = await browser.newContext({
    viewport: {
      width: config.viewport.width,
      height: config.viewport.height
    }
  });

  const page = await context.newPage();

  for (let i = 0; i < FRAME_COUNT; i++) {
    const milestone = config.milestones[i];
    const frameNumber = String(i + 1).padStart(3, '0');

    console.log(`\n[${i + 1}/${FRAME_COUNT}] ${milestone.file}`);
    console.log(`  Phase ${milestone.phase}: ${milestone.description}`);

    try {
      const url = `${config.serverUrl}?model=${milestone.file}&capture=true`;
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

      await page.waitForFunction(
        () => window.__MODEL_LOADED__ === true,
        { timeout: 60000 }
      );

      await page.waitForTimeout(config.captureStabilizationMs);

      await page.screenshot({
        path: path.join(framesDir, `frame_${frameNumber}.png`),
        type: 'png'
      });
      console.log(`  Saved: frame_${frameNumber}.png`);

      await page.evaluate(() => { window.__MODEL_LOADED__ = false; });

    } catch (error) {
      console.error(`  ERROR: ${error.message}`);
    }
  }

  await browser.close();

  console.log(`\n${'='.repeat(40)}`);
  console.log(`Done! ${FRAME_COUNT} frames captured.`);
  console.log(`Frames: ${framesDir}`);
}

captureFrames().catch(console.error);
