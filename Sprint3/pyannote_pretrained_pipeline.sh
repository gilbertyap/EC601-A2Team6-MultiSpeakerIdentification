#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=24:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_pretrained

#$ -j y

#$ -o pyannote_pretrained_log.qlog
#$ -e pyannote_pretrained_error_log.qlog

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

# Activate venv
source ../a2team6-env/bin/activate

# Move to the ThirdPartyTools directory
cd ../ThirdPartyTools

# Export database environment variable
export PYANNOTE_DATABASE_CONFIG=./database.yml

echo "-----APPLYING PRETRAINED MODELS-----"
# Applies the pretrained models against the test and development sets
export EXP_DIR=./pretrained/

for SUBSET in development test
  do
  for TASK in sad scd
    do
      pyannote-audio ${TASK} apply --gpu --step=0.1 --pretrained=${TASK}_ami --subset=${SUBSET} ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse
    done
  done

for SUBSET in development test
  do
    pyannote-audio ${TASK} apply --gpu --step=0.1 --pretrained=emb_voxceleb--subset=${SUBSET} ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse
  done

echo "----------PIPELINE TRAINING----------"
# Trains the pipeline sing the applied models
pyannote-pipeline train --subset=development --iterations=100 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------PIPELINE Application---------"
# Applies pipline to test set
export TRN_DIR=${EXP_DIR}/train/VoxConverse.SpeakerDiarization.voxconverse.development
pyannote-pipeline apply --subset=test ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse
