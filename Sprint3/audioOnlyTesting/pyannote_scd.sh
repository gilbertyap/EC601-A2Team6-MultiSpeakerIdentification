#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=24:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_scd_training

#$ -j y

#$ -o pyannote_scd_log.qlog
#$ -e pyannote_scd_error_log.qlog

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

echo "---------SCD Training---------"
# SCD training
export EXP_DIR=./scd/ 
pyannote-audio scd train --gpu --subset=train --to=335 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SCD Validation---------"
# SCD validation
export TRN_DIR=${EXP_DIR}/train/VoxConverse.SpeakerDiarization.voxconverse.train
pyannote-audio scd validate --gpu --subset=development --from=110 --to=335 --every=45 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SCD Application---------"
# SCD application
export VAL_DIR=${TRN_DIR}/validate_segmentation_fscore/VoxConverse.SpeakerDiarization.voxconverse.development
pyannote-audio scd apply --gpu --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse
