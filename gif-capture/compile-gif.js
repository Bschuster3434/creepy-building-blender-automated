import { execSync } from 'child_process';
import { config } from './capture-config.js';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function compileGif() {
  const framesDir = path.join(__dirname, 'frames');
  const outputDir = path.join(__dirname, 'output');

  // Check frames exist
  if (!fs.existsSync(framesDir)) {
    console.error('Error: frames directory does not exist. Run capture first.');
    process.exit(1);
  }

  const frames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png')).sort();
  if (frames.length === 0) {
    console.error('Error: No PNG frames found in frames directory.');
    process.exit(1);
  }

  console.log(`Found ${frames.length} frames to compile`);

  // Create output directory
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Calculate FPS from frame delay (400ms = 2.5 fps)
  const fps = 1000 / config.frameDelay;
  console.log(`Frame rate: ${fps} fps (${config.frameDelay}ms per frame)`);

  const paletteFile = path.join(outputDir, 'palette.png');
  const outputFile = path.join(outputDir, 'building_evolution.gif');
  const inputPattern = path.join(framesDir, 'frame_%03d.png');

  try {
    // Check if ffmpeg is available
    try {
      execSync('ffmpeg -version', { stdio: 'pipe' });
    } catch {
      console.error('Error: ffmpeg is not installed or not in PATH.');
      console.error('Please install ffmpeg: https://ffmpeg.org/download.html');
      process.exit(1);
    }

    console.log('\nStep 1: Generating optimized color palette...');

    // Pass 1: Generate palette for best quality
    // Using palettegen with stats_mode=diff for better animation quality
    const paletteCmd = `ffmpeg -y -framerate ${fps} -i "${inputPattern}" -vf "fps=${fps},scale=1920:1080:flags=lanczos,palettegen=max_colors=256:stats_mode=diff" "${paletteFile}"`;

    execSync(paletteCmd, { stdio: 'inherit' });

    console.log('\nStep 2: Creating GIF with optimized palette...');

    // Pass 2: Create GIF using the palette
    // Using paletteuse with dither=bayer for smooth gradients
    const gifCmd = `ffmpeg -y -framerate ${fps} -i "${inputPattern}" -i "${paletteFile}" -lavfi "fps=${fps},scale=1920:1080:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" "${outputFile}"`;

    execSync(gifCmd, { stdio: 'inherit' });

    // Get file size
    const stats = fs.statSync(outputFile);
    const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);

    // Calculate duration
    const durationSeconds = (frames.length * config.frameDelay / 1000).toFixed(1);

    console.log(`\n${'='.repeat(50)}`);
    console.log('GIF compilation complete!');
    console.log(`\nOutput: ${outputFile}`);
    console.log(`Size: ${fileSizeMB} MB`);
    console.log(`Duration: ${durationSeconds} seconds`);
    console.log(`Frames: ${frames.length}`);
    console.log(`Resolution: 1920x1080`);

    // Clean up palette file
    if (fs.existsSync(paletteFile)) {
      fs.unlinkSync(paletteFile);
      console.log('\nCleaned up temporary palette file.');
    }

  } catch (error) {
    console.error('Error during GIF compilation:', error.message);
    process.exit(1);
  }
}

// Run
compileGif();
