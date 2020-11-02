#!/usr/bin/bash

echo "Initializing submodules"
git submodule init

echo "Creating submodule folders"
git submodule update

echo "Creating a2team6-env virtual environment for Python"
python3 -m venv a2team6-env

echo "Activating virtual environment"
source a2team6-env/bin/activate

echo "Installing requirements for dscore"
cd ThirdPartyTools/dscore
pip3 install -r requirements.txt
echo "Installation complete"

echo "Installing pyannote-audio"
cd ../pyannote-audio
pip3 install .
echo "Installation complete"

echo "Install PyTorch"
pip3 install torch torchvision
echo "Installation complete"
