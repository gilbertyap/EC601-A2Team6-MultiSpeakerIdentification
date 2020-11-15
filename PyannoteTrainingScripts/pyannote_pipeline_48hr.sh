#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=48:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_pipeline_training

#$ -j y

#$ -o pipeline_48_log.qlog
#$ -e pipeline_48_error_log.qlog

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

cd ../

# Activate venv
source ./a2team6-env/bin/activate

# Move to the ThirdPartyTools directory
cd ThirdPartyTools

# Export database environment variable
export PYANNOTE_DATABASE_CONFIG=./database.yml

echo "---------PIPELINE TRAINING---------"
export EXP_DIR=./pipeline/
pyannote-pipeline train --subset=development --iterations=300 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------PIPELINE Application---------"
export TRN_DIR=${EXP_DIR}/train/VoxConverse.SpeakerDiarization.voxconverse.development
pyannote-pipeline apply --subset=test ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse
