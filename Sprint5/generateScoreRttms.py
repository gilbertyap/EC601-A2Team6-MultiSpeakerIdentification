# load pipeline
import torch
import os

audioFileList = os.listdir('./convertedFiles/audio/')
scoresFileList = os.listdir('./convertedFiles/scoreRttms/')

pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')

for file in audioFileList:
    fileName, fileExt = os.path.splitext(file)
    scoreFileName = fileName+'_score.rttm'
    if not (scoreFileName in scoresFileList):
        print('Diarizing {}'.format(file))
        # apply diarization pipeline on your audio file
        diarization = pipeline({'audio': './convertedFiles/audio/'+file})

        # dump result to disk using RTTM format
        with open('./convertedFiles/audio/'+scoreFileName, 'w') as f:
            diarization.write_rttm(f)
