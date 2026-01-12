@echo off
echo Creating GIF from frames...

cd /d "%~dp0"
if not exist output mkdir output

echo Step 1: Generating color palette...
ffmpeg -y -framerate 2.5 -i "frames/frame_%%03d.png" -vf "fps=2.5,scale=1920:1080:flags=lanczos,palettegen=max_colors=256:stats_mode=diff" "output/palette.png"

echo Step 2: Creating GIF...
ffmpeg -y -framerate 2.5 -i "frames/frame_%%03d.png" -i "output/palette.png" -lavfi "fps=2.5,scale=1920:1080:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" "output/building_evolution.gif"

echo Step 3: Cleaning up...
del "output\palette.png"

echo.
echo Done! GIF saved to: output\building_evolution.gif
echo.
pause
