# Download YouTube videos from a text file of youtube links
# Then separate out the audio file and video file
from pytube import YouTube
from moviepy.editor import *
import os, random

print('Getting all VoxCeleb1 links...')
videoLinks = []
with open('voxCeleb1_links.txt','r') as f:
    videoLinks = f.readlines()

# Make video folder
downloadPath = './downloaded_videos/'
if not os.path.isdir(downloadPath):
    os.mkdir(downloadPath)

numVideos = 2
print('Downloading {} random links...'.format(numVideos))
i = 0
history = []
while i < numVideos:
    randIndex = random.randint(0, len(videoLinks)-1)
    if not randIndex in history:
        link = videoLinks[randIndex]
        try:
            # Initiate the download of the combined video/audio mp4
            print('Attempting to download video from {}'.format(link))
            yt = YouTube(link)
            # Try to download video at 720p quality if possible
            for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
                if stream.resolution ==  '720p':
                    stream.download(downloadPath)
                    break
            i += 1
            history.append(randIndex)
            print('Download succeeded!')
        except:
            print('Unable to download this video.')
            continue

print('Finished downloading all videos')

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