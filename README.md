# Boston University EC601 (A2) Team6: Video Speaker Detection

# Project Summary

## Contributors:
* Gilbert Yap - gilberty@bu.edu
* Xinyue Zhou - zhoux17@bu.edu

## Requirements
1. Python >= 3.8.5
1. Linux System
1. Installation of the `requirements.txt` file

## Installation
1. `git clone https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification.git`
1. `pip install -r requirements.txt`
1. `python3 -m venv a2team6-env`
1. `source a2team6-env/bin/activate`
1. `./setup.sh`

## Instructions
1. `source a2team6-env/bin/activate` (If venv has not been activated)
1. Unzip the `ref_rttms.zip` file and place `ref_rttms` folder into project directory.
1. Download the demo YouTube videos with `downloadVideos.py`.
1. Use `convertVideos.py` to setup video and audio in `convertedFiles` as needed by project
1. Run `./getVsdRttms.sh` to run `findMouthThresholdValue.py` on each of the videos in `/convertedFiles/video/`. Resulting `rttm` files will be in `/convertedFiles/video/` for each video.
1. Use `score.py -r ./convertedFiles/uem/yourreference.rttm -s /path/to/generated/rttm.rttm` in `ThirdPartyTools/dscore/` for scoring the Video Speaker Detection against a reference file.

## TODO
* Compile a table of results for the README based on the video links provided in this repository
* Finish updating instructions

## Stretch Goals
* Implement facial recognition in `videoSpeakerDetection.py` to track multiple mouths in videos

## Project Details

GitHub repository for EC601 Product Design Section A2 Team 6 project. Will insert project summary here prior to poster presentations.


## Citations

```
@inproceedings{Bredin2020,
  Title = {{pyannote.audio: neural building blocks for speaker diarization}},
  Author = {{Bredin}, Herv{\'e} and {Yin}, Ruiqing and {Coria}, Juan Manuel and {Gelly}, Gregory and {Korshunov}, Pavel and {Lavechin}, Marvin and {Fustes}, Diego and {Titeux}, Hadrien and {Bouaziz}, Wassim and {Gill}, Marie-Philippe},
  Booktitle = {ICASSP 2020, IEEE International Conference on Acoustics, Speech, and Signal Processing},
  Address = {Barcelona, Spain},
  Month = {May},
  Year = {2020},
}
```

```
@misc{khan_mahmood_ahmed_gotoh_2009, 
  Title={Visual speech detection using OpenCV}, 
  url={https://www.uet.edu.pk/Conferences/icosst2009/presentations_2009/Research_Papers/Visual_speech_detection_using_OpenCV.pdf}, 
  Journal={Third International Conference on Open-Source Systems and Technologies 19-22 December 2009, Lahore, Pakistan.}, 
  Publisher={University of Engineering &amp; Technology Lahore}, author={Khan, Muhammad Usman Ghani and Mahmood, Sajid and Ahmed, Mahmood and Gotoh, Yoshihiko}, 
  Year={2009}, 
  Month={Dec}
}
```

```
@misc{ryant_2019, 
  Title={nryant/dscore}, 
  url={https://github.com/nryant/dscore}, 
  Journal={dscore}, 
  Publisher={GitHub}, 
  Author={Ryant, Neville}, 
  Year={2019}, 
  Month={Mar}
}
```

```
@misc{snyder2015musan,
      title={MUSAN: A Music, Speech, and Noise Corpus}, 
      author={David Snyder and Guoguo Chen and Daniel Povey},
      year={2015},
      eprint={1510.08484},
      archivePrefix={arXiv},
      primaryClass={cs.SD}
}
```