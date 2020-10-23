#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=12:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_training_sad

#$ -j y

#$ -o pyannote_log.qlog
#$ -e pyannote_error_log.qlog

# Keep track of information related to the current job
echo "=========================================================="
echo "Start date : $(date)"
echo "Job name : $JOB_NAME"
echo "Job ID : $JOB_ID  $SGE_TASK_ID"
echo "=========================================================="

# Request node with 8 CPUs
#$ -pe omp 8

# Request number of GPUs
#$ -l gpus=1

# Choose a GPU minimum capability
#$ -l gpu_c=6.0

# Need Python 3.7 for pyannote
module load python3/3.7.7

# First move to the correct parent directory
cd ../

# Activate venv
source a2team6-env/bin/activate

# Move to the ThirdPartyTools directory
cd ThirdPartyTools

# Export database environment variable
export PYANNOTE_DATABASE_CONFIG= ./database.yml

echo "---------SAD---------"
echo "---------SAD Training---------"

# SAD training
export EXP_DIR=/sad/ 
pyannote-audio sad train --gpu --subset=train --to=200 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SAD Validation---------"

# SAD validation
export TRN_DIR=${EXP_DIR}/train/VoxConverse.SpeakerDiarization.voxconverse.train
pyannote-audio sad validate --gpu --subset=development --from=10 --to=200 --every=10 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SAD Application---------"
exportVAL_DIR=${TRN_DIR}/validate_detection_fscaore_VoxConverse.SpeakerDiarization.voxconverse.development
pyannote-audio sad apply --gpu --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse
