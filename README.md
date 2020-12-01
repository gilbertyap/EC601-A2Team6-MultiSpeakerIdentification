# EC601-A2Team6-MultiSpeakerIdentification

## Summary
GitHub repository for EC601 Product Design Section A2 Team 6 project.

## Contributors:
* Gilbert Yap - gilberty@bu.edu
* Xinyue Zhou - zhoux17@bu.edu

## Requirements
1. Python >= 3.8.5
1. Linux System

## Installation
1. `git clone https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification.git`
1. `pip install -r requirements.txt`
1. `./setup.sh`
1. `source a2team6-env/bin/activate`
1. `./setup2.sh`

## Instructions
1. `source a2team6-env/bin/activate`
1. `downloadVideos.py`
1. `convertVideos.py`
1. `generateUEM.py`
1. `generateUEMasRttm.py`
1. `getMouthLuminosity.py -v /path/to/videofile.ext`
1. Use `getVals.m` on the video
1. (Optional) Rerun `getMouthLuminosity.py -v /path/to/videofile.ext -t 123.456` but replace the last number with the final printed value from `getVals.m`
1. Use `genFrameNums.m` on the video
1. `convertCsvToRttm -f /path/to/csvfile.csv` 
1. `ThirdPartyTools/dscore/score.py -r ./convertedFiles/uem/yourreference.rttm -s /path/to/generated/rttm.rttm`

## TODO
* Convert the matlab scripts into python
* Fill out this readme
* Swap out links in the links file for single speakers

## Project Details