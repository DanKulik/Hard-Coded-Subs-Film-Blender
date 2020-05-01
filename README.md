# Hard-Coded-Subs-Film-Blender
This python script is meant to blend HC subs into the background

The way this script works is by user defining an aperture size and an RGB pixel range to mask. The script will then get an average RGB color for the aperture and apply this color to the masked region.

It has been set up as a kwarg input function that requires at the very least the input & output file names.
a docstring has been provided in the script to specify all the other parameters. And default parameters have also been
set if none were initialized in the function call (except file names). An example function call exists at the bottom of the script as a guide, however the values are easily adjustable. Two parameters have not been added to the kwargs and these include the values used for both the mask Guassian blur (blurs the pixels around of the mask and surrounding area, therefore greater values means a wider area blurred), and the aperture Guassian blur (which is less sensative {essentially a secondary text blur} and the current input values should tend to work). The output is audio and subless and will require those components to be added with other software (eg: ffmpeg)

Obviously the bigger the input file the longer it will take for this script to run. Eg: a 1.8h movie of 25fps will take about 3.5h to render. This can be sped up with the conv_rate param which controls the cpu output by using the time.sleep() function. The default value should use around 1 core/ or 25% cpu of processing power. Also mkv files seem to process much faster tha other video file types.

#####Additional Info#########

If ffmpeg is available here are handy commands to add the audio and subs
[Extracting audio from video]
ffmpeg -i input.mkv -vn -acodec copy output-audio.aac (for a direct input fps to output fps)

Change audio tempo only
ffmpeg -i input.mkv -filter:a "atempo=output_fps/input_fps" -vn output-audio.aac (change tempo pace for audio with fps adjustment... note output_fps/input_fps must be the calculated value)

Change audio tempo and pitch
ffmpeg -i input.mkv -filter:a "asetrate=48000*output_fps/input_fps,aresample=48000" output-audio.aac
(change tempo pace for audio with fps adjustment... note output_fps/input_fps must be the calculated value)

[Combining audio to new video]
ffmpeg -i output.mp4 -i output-audio.acc -c copy -map 0:v:0 -map 1:a:0 output_new.mp4

[Softcode subs to the video]
ffmpeg -i output_new.mp4 -i input.ass -c copy -c:s mov_text final.mp4 (ass or srt sub file for direct fps converion)

for a framerate change between the input and output files the fix the sub 
pip install pysub2 and run in terminal:

import pysubs2
subs = pysubs2.load("input2.ass", encoding="utf-8")
subs.transform_framerate(input_fps, output_fps)
subs.save("my_subtitles_edited.ass")

After this the fixed subs can be softcoded.

Hope this will help when encoding films with hardcoded subs. Even though it is not the most elegant solution it is 
still available. Greater minds may come up/ already have with better methods. Anyways... all the best and thank you 
for your patronage, Severian-desu-ga
