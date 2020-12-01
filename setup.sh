#!/usr/bin/bash
echo "Upgrading pip"
pip3 install --upgrade pip

echo "Initializing submodules"
git submodule init

echo "Creating submodule folders"
git submodule update

echo "Creating a2team6-env virtual environment for Python"
python3 -m venv a2team6-env
