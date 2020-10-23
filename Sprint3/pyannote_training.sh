#!/bin/bash -l

# Set project
#$ -P ece601

# Specify time limit
#$ -l h_rt=24:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N pyannote_training_1

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
export PYANNOTE_DATABASE_CONFIG=./database.yml

# Start SAD, SCD, and EMB training
echo "---------SAD---------"
mkdir sad
cp ./pyannote-audio/tutorials/models/speech_activity_detection/config.yml ./sad/config.yml

echo "---------SAD Training---------"

# SAD training
export EXP_DIR = ./sad 
pyannote-audio sad train --gpu --subset=train --to=200 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SAD Validation---------"

# SAD validation
export TRN_DIR=${EXP_DIR}/train/AMI.SpeakerDiarization.MixHeadset.train
pyannote-audio sad validate --gpu --subset=development --from=10 --to=200 --every=10 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SAD Application---------"

# SAD application
export VAL_DIR=${TRN_DIR}/validate_detection_fscore/VoxConverse.SpeakerDiarization.voxconverset.development
pyannote-audio sad apply --gpu --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SCD---------"
mkdir scd
cp ./pyannote-audio/tutorials/models/speaker_change_detection/config.yml ./scd/config.yml

echo "---------SCD Training---------"

# SCD training
export EXP_DIR = ./sad 
pyannote-audio scd train --gpu --subset=train --to=1000 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SCD Validation---------"

# SCD validation
export TRN_DIR=${EXP_DIR}/train/AMI.SpeakerDiarization.MixHeadset.train
pyannote-audio scd validate --gpu --subset=development --from=200 --to=1000 --every=100 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------SCD Application---------"

# SCD application
export VAL_DIR=${TRN_DIR}/validate_detection_fscore/VoxConverse.SpeakerDiarization.voxconverset.development
pyannote-audio scd apply --gpu --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------EMD---------"
mkdir emd
cp ./pyannote-audio/tutorials/models/speaker_embedding/config.yml ./scd/config.yml

echo "---------EMD Training---------"

# EMB training
export EXP_DIR = ./emb 
pyannote-audio emb train --gpu --subset=train --to=250 --parallel=8 ${EXP_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------EMD Validation---------"

# EMB validation
export TRN_DIR=${EXP_DIR}/train/AMI.SpeakerDiarization.MixHeadset.train
pyannote-audio emb validate --gpu --subset=development --to=250 --every=5 ${TRN_DIR} VoxConverse.SpeakerDiarization.voxconverse

echo "---------EMD Application---------"

# EMB application
export VAL_DIR=${TRN_DIR}/validate_detection_fscore/VoxConverse.SpeakerDiarization.voxconverset.development
pyannote-audio emb apply --gpu ---step=0.1 --subset=test ${VAL_DIR} VoxConverse.SpeakerDiarization.voxconverse
