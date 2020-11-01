import torch
from pyannote.database import get_protocol
from pyannote.database import FileFinder
from pyannote.audio.pipeline import SpeakerDiarization

SAD_PATH = '/projectnb2/ece601/A2-Team6/gilbert_folder/EC601-A2Team6-MultiSpeakerIdentification/ThirdPartyTools/sad/train/VoxConverse.SpeakerDiarization.voxconverse.train/weights/0120.pt'
SCD_PATH = '/projectnb2/ece601/A2-Team6/gilbert_folder/EC601-A2Team6-MultiSpeakerIdentification/ThirdPartyTools/scd/train/VoxConverse.SpeakerDiarization.voxconverse.train/weights/0110.pt'
REF_RTTM_PATH = '/projectnb2/ece601/A2-Team6/gilbert_folder/EC601-A2Team6-MultiSpeakerIdentification/ThirdPartyTools/voxconverse/dev/'
GEN_RTTM_PATH = '/projectnb2/ece601/A2-Team6/gilbert_folder/EC601-A2Team6-MultiSpeakerIdentification/Sprint3/gen/'
AUDIO_PATH = '/projectnb2/ece601/A2-Team6/VoxConverse/test/audio/'
PARAMS_YML = './training/params.yml'

import os, sys, time
from warnings import simplefilter
# The 'FutureWarnings' from sklearn are quite intrusive in the console, so let's suppress them
simplefilter(action='ignore', category=FutureWarning)

def diarizeFiles(fileList, pipeline, test_name):
    print('Running test \'{}\' '.format(test_name))
    start_time = time.time()
    for file in fileList:
        print('Attempting to diarize {}'.format(file))
        filename, fileext = os.path.splitext(file)
        if os.path.exists(GEN_RTTM_PATH+'/'+test_name+'/'+filename+'_'+test_name+'.rttm'):
            print('This files .rttm file already was generated (maybe in a previous run?). Skipping...')
            continue
        else:
            test_file = {'uri': filename, 'audio': AUDIO_PATH+file}
            try:
                diarization = pipeline(test_file)
                with open(GEN_RTTM_PATH+'/'+test_name+'/'+filename+'_'+test_name+'.rttm', 'w') as f:
                    diarization.write_rttm(f)
            except:
                print('Could not perform speaker diarization on {}'.format(test_file))
                continue

    exec_time = round(time.time () - start_time, 3)
    print('Diarization of all files completed in {} seconds.'.format(exec_time))

    print('Generating \'score_'+test_name+'.scp\' and \'reference_'+test_name+'.scp\' for use with dscore...')

    # Once done with diarization, create the '.scp' files for dscore
    # .scp file for generated files
    tempRttmFileList = os.listdir(GEN_RTTM_PATH+'/'+test_name+'/')
    if 'donotdelete' in tempRttmFileList:
        tempRttmFileList.remove('donotdelete')
    if '.gitignore' in tempRttmFileList:
        tempRttmFileList.remove('.gitignore')
    finalRttmFileList = []
    for file in tempRttmFileList:
        finalRttmFileList.append(os.path.abspath(GEN_RTTM_PATH+'/'+test_name)+'/'+file)
    with open('score_'+test_name+'.scp', 'w') as f:
        for line in finalRttmFileList:
            f.write(line+'\n')

    # .scp file for the reference files
    # Make sure that we are only checking against the audio files
    finalRttmFileList = []
    for file in os.listdir(AUDIO_PATH):
        finalRttmFileList.append(os.path.abspath(REF_RTTM_PATH)+'/'+file)
    with open('reference_'+test_name+'.scp', 'w') as f:
        for line in finalRttmFileList:
            f.write(line+'\n')

    print('Generation finished!')

if __name__ == "__main__":
    fileList = os.listdir(AUDIO_PATH)

    # Baseline pipeline
    basePipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')

    diarizeFiles(fileList, basePipeline, 'base')

    # Use the fine-tuned validation models to make a pipeline
    finePipeline = SpeakerDiarization(sad_scores = SAD_PATH,
                                    scd_scores = SCD_PATH,
                                    embedding = 'emb',
                                    method='affinity_propagation')

    finePipeline.load_params(PARAMS_YML)
    diarizeFiles(fileList, finePipeline, 'fine')

    sys.exit(0)
