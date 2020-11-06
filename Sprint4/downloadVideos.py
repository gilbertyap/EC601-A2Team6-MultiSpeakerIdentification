# Download YouTube videos from a text file of youtube links

from pytube import YouTube
import random

print('Getting all VoxCeleb1 links...')
videoLinks = []
with open('voxCeleb1_links.txt','r') as f:
    videoLinks = f.readlines()

numVideos = 10
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
                    stream.download()
                    break
            i += 1
            history.append(randIndex)
            print('Download succeeded!')
        except:
            print('Unable to download this video.')
            continue

print('Finished downloading all videos')