#!/bin/bash -l

# Set Project
#$ -P ece601

# Specify time limit
#$ -l h_rt=1:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N generate_all_files

#$ -j y

#$ -o log.qlog
#$ -e error_log.qlog

# Keep track of information related to the current job
echo "=========================================================="
echo "Start date : $(date)"
echo "Job name : $JOB_NAME"
echo "Job ID : $JOB_ID  $SGE_TASK_ID"
echo "=========================================================="

# Request node with 4 CPUs
#$ -pe omp 4

# Request number of GPUs
#$ -l gpus=1

# Choose a GPU minimum capability
#$ -l gpu_c=6.0

# Need Python 3.7 for pyannote
module load python3/3.7.7

# Activate venv
source ../a2team6-env/bin/activate

# Move to the correct directory first
cd ../Sprint2/audioOnlyTesting/

# Generate all audio files
echo "Generating noise files for dvngl.wav with min scale of 1/1024"
python3 addRecordedNoise.py ./audio/dvngl.wav ./noise/gwn.wav 1024

python3 addRecordedNoise.py ./audio/dvngl.wav ./noise/music-hd-0000.wav 1024

python3 addRecordedNoise.py ./audio/dvngl.wav ./noise/music-jamendo-0000.wav 1024

python3 addRecordedNoise.py ./audio/dvngl.wav ./noise/noise-free-sound-0042.wav 1024

echo "Done generating dvngl files"
echo "Generating noise files for hycgx.wav with min scale of 1/1024"

python3 addRecordedNoise.py ./audio/hycgx.wav ./noise/gwn.wav 1024

python3 addRecordedNoise.py ./audio/hycgx.wav ./noise/music-hd-0000.wav 1024

python3 addRecordedNoise.py ./audio/hycgx.wav ./noise/music-jamendo-0000.wav 1024

python3 addRecordedNoise.py ./audio/hycgx.wav ./noise/noise-free-sound-0042.wav 1024

echo "Done generating hycgx files"
echo "Generating rttms"

python3 generateRttms.py

echo "Finished generating rttms"
echo "Running dscore"

python3 ../../ThirdPartyTools/dscore/score.py -R reference.scp -S score.scp
