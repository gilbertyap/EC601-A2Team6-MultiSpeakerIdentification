import torch
import os, sys, time

import warnings
from warnings import simplefilter
# The 'FutureWarnings' from sklearn are quite intrusive in the console, so let's suppress them
simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":
    audioPath = './audio/'
    refRttmPath = './ref/'
    genRttmPath = './gen/'

    # Load a pretrained pipeline that was trained on the DIHARD Challenge Set
    start_time = time.time()
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')

    # Get all of the wav files in the audio folder
    fileList = os.listdir(audioPath)
    fileList.sort()

    wavList = []
    for file in fileList:
        if not ('rttm' in file):
            wavList.append(file)

    totalFiles = len(wavList)
    i = 1

    for file in wavList:
        # Double check to see if you have already generated the .rttm file for the particular audio file
        (fileName, fileExt) = os.path.splitext(file)
        if os.path.exists(genRttmPath+fileName+'.rttm'):
            print('The .rttm file for {} already was generated (maybe in a previous run?). Skipping...'.format(genRttmPath+fileName+'.rttm'))
            continue
        else:
            pyannote_test_file_dict = {'uri': fileName, 'audio': audioPath+file}
            print('Running diarization on {}, file {}/{}...'.format(file, i, totalFiles))
            try:
                diarization = pipeline(pyannote_test_file_dict)
                # Output the rttm to the local folder
                with open(genRttmPath+fileName+'.rttm', 'w') as f:
                    diarization.write_rttm(f)
            except:
                print('Error, could not perform diarization on {}.'.format(file))
            finally:
                i+=1
    exec_time = round(time.time () - start_time, 3)
    print('Diarization of all files completed in {} seconds.'.format(exec_time))

    print('Generating \'score.scp\' and \'reference.scp\' for use with dscore...')
    # Once done with diarization, create the '.scp' files for dscore
    # .scp file for generated files
    tempRttmFileList = os.listdir(genRttmPath)
    if 'donotdelete' in tempRttmFileList:
        tempRttmFileList.remove('donotdelete')
    finalRttmFileList = []
    for file in tempRttmFileList:
        finalRttmFileList.append(os.path.abspath(genRttmPath)+'/'+file)
    with open('score.scp', 'w') as f:
        for line in finalRttmFileList:
            f.write(line+'\n')

    # .scp file for the reference files
    tempRttmFileList = os.listdir(refRttmPath)
    finalRttmFileList = []
    for file in tempRttmFileList:
        finalRttmFileList.append(os.path.abspath(refRttmPath)+'/'+file)
    with open('reference.scp', 'w') as f:
        for line in finalRttmFileList:
            f.write(line+'\n')

    print('Generation finished!')
    sys.exit(0)
