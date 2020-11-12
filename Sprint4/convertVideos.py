# Download YouTube videos from a text file of youtube links
# Then separate out the audio file and video file
from moviepy.editor import *
import os, random

# Make video folder
downloadPath = './downloaded_videos/'

# Make conversion folder
convertFolder = './convertedFiles/'
audioFolder = convertFolder+'audio/'
videoFolder = convertFolder+'video/'
if not os.path.isdir(convertFolder):
    os.mkdir(convertFolder)
if not os.path.isdir(audioFolder):
    os.mkdir(audioFolder)
if not os.path.isdir(videoFolder):
    os.mkdir(videoFolder)

videoList = os.listdir(downloadPath)
for video in videoList:
    (fileName, fileExt) = os.path.splitext(video)
    try:
        convertVideo = VideoFileClip(downloadPath+video)
        convertAudio = convertVideo.audio
        convertAudio = convertAudio.fx(afx.audio_normalize)
        convertAudio.write_audiofile(audioFolder+fileName+'.wav', fps=48000, nbytes=2, codec='pcm_s16le')
        convertVideo.write_videofile(videoFolder+fileName+'.mp4',fps=25)
        convertVideo.close()
        convertVideo.close()
    except:
        print('Could not convert {}'.format(video))
        continue

print('Finished converting all videos.')