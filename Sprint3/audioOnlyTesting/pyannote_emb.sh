#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=24:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_emb_training

#$ -j y

#$ -o pyannote_emb_log.qlog
#$ -e pyannote_emb_error_log.qlog

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
cd ../../

# Activate venv
source a2team6-env/bin/activate

# Move to the ThirdPartyTools directory
cd ThirdPartyTools

# Export database environment variable
export PYANNOTE_DATABASE_CONFIG=./database.yml

echo "---------EMD Training---------"
# EMB training
export EXP_DIR=./emb/
pyannote-audio emb train --gpu --subset=train --to=65 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------EMD Validation---------"
# EMB validation
export TRN_DIR=${EXP_DIR}/train/VoxConverse.SpeakerDiarization.voxconverse.train
pyannote-audio emb validate --gpu --subset=development --to=65 --every=5 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------EMD Application---------"
# EMB application
export VAL_DIR=${TRN_DIR}/validate_diarization_fscore/VoxConverse.SpeakerDiarization.voxconverse.development
pyannote-audio emb apply --gpu ---step=0.1 --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse