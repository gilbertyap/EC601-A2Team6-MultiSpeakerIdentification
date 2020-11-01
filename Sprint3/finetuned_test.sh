#!/bin/bash -l

# Set Project
#$ -P ece601

# Specify time limit
#$ -l h_rt=12:00:00

# Send an email for all possible events
#$ -m beas

# Job name
#$ -N generate_rttms

#$ -j y

#$ -o rttm_log.qlog
#$ -e rttm_error_log.qlog

# Keep track of information related to the current job
echo "=========================================================="
echo "Start date : $(date)"
echo "Job name : $JOB_NAME"
echo "Job ID : $JOB_ID  $SGE_TASK_ID"
echo "=========================================================="

# Request node with 4 CPUs
#$ -pe omp 8

# Request number of GPUs
#$ -l gpus=1

# Choose a GPU minimum capability
#$ -l gpu_c=6.0

# Need Python 3.7 for pyannote
module load python3/3.7.7

# Activate venv
source ../a2team6-env/bin/activate

echo "**********Running finetunedTest.py**********"

python3 finetunedTest.py

if -e reference.scp
then
  if -e score.scp
  then
    echo "**********Running dscore**********"
    python3 ../../ThirdPartyTools/dscore/score.py -R reference.scp -S score.scp
  else
  fi
else
    echo "**********.scp files were not generated, probably due to error above**********"
fi