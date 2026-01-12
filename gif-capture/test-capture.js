// Quick test script - captures just the first and last frames
import { chromium } from 'playwright';
import { config } from './capture-config.js';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function testCapture() {
  console.log('Running test capture (first and last frames only)...');

  const framesDir = path.join(__dirname, 'frames');
  if (!fs.existsSync(framesDir)) {
    fs.mkdirSync(framesDir, { recursive: true });
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

  // Test first milestone
  const firstMilestone = config.milestones[0];
  console.log(`\nTesting: ${firstMilestone.file}`);

  try {
    const url = `${config.serverUrl}?model=${firstMilestone.file}&capture=true`;
    console.log(`URL: ${url}`);

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    console.log('Waiting for model load signal...');
    await page.waitForFunction(
      () => window.__MODEL_LOADED__ === true,
      { timeout: 60000 }
    );

    console.log('Model loaded! Waiting for render stabilization...');
    await page.waitForTimeout(config.captureStabilizationMs);

    await page.screenshot({
      path: path.join(framesDir, 'test_first.png'),
      type: 'png'
    });
    console.log('Saved: test_first.png');

  } catch (error) {
    console.error(`Error: ${error.message}`);
  }

  // Test last milestone
  const lastMilestone = config.milestones[config.milestones.length - 1];
  console.log(`\nTesting: ${lastMilestone.file}`);

  try {
    await page.evaluate(() => { window.__MODEL_LOADED__ = false; });

    const url = `${config.serverUrl}?model=${lastMilestone.file}&capture=true`;
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    await page.waitForFunction(
      () => window.__MODEL_LOADED__ === true,
      { timeout: 60000 }
    );

    await page.waitForTimeout(config.captureStabilizationMs);

    await page.screenshot({
      path: path.join(framesDir, 'test_last.png'),
      type: 'png'
    });
    console.log('Saved: test_last.png');

  } catch (error) {
    console.error(`Error: ${error.message}`);
  }

  await browser.close();
  console.log('\nTest capture complete!');
  console.log(`Check ${framesDir} for test_first.png and test_last.png`);
}

testCapture().catch(console.error);
