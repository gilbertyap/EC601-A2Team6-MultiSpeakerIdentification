# Boston University EC601 (A2) Team6: Visual Speaker Identification in Noisy Environments

## Contributors:
* Gilbert Yap - gilberty@bu.edu
* Xinyue Zhou - zhoux17@bu.edu

# Project Summary

This repository contains the code done for research done on detecting speakers in a noisy environment through visual detection. This research was done for EC601 "Product Design in Electrical and Computer Engineering" at Boston University during Fall 2020. Going forward, the abbreviation for visual speaker identification, VSI, will be used to describe the algorithm used.

The VSI method calculates the average luminosity of a speaker's mouth to determine if their mouth is open. Using OpenCV, we process every frame of the video and record the average luminosity of the mouth region based on the facial landmarks of the [dlib](http://dlib.net/face_detector.py.html) face detector. These luminosity values are stored and are processed once all frames have been examined. Once all frames of the video have been processed, the mean of the luminosity value plus the standard deviation is used as the threshold value. The output of the library is a "Rich Transcription Time Marked (RTTM)" formatted text file that can be used with [dscore](https://github.com/nryant/dscore) for scoring against a reference file.

In the six videos tested, the algorithm had about 50% accuracy on average. Reference files were handmade by utilizing [webrtcvad](https://github.com/wiseman/py-webrtcvad) to verify speech in single-speaker videos. Additional testing was done to compare the reference files against the VSI algorithm when only the segments of video that had a face were consider. The accuracy of the VSI method increased to about 60% on average in this situation. Below is the performance of `webrtcvad`'s VAD method vs our VSI method when additional audio from the MUSAN noise dataset was added on top of the video's audio.

![PerformanceChart](https://raw.githubusercontent.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/master/examples/PerformanceChart.png)

As seen above, the situations where the VSI method performed better than the VAD method was when white noise-types of audio were added on top of the video's audio. For music, the VSI method's worst performance was still 7% better than VAD when only segments where a face was presented was considered. We noticed that there were cases of false positives (see `/examples/false_positive.jpg`) where speakers were smiling or had their mouth slightly open while not speaking that tricked the system. We also noticed some shortcomings of the facial landmark tracking when speakers with beards were given larger mouth areas than non-beared speakers. If the beard hair color was dark, this tricked the VSI method into thinking the speaker's mouth was open more often than it actually was. One way of navigating around this issue would be to implement a weighting system that places more emphasis in the center of the detected mouth so that instances were the mouth is over estimated can be compensated for.

The VSI algorithm is based on the paper ["Visual speech detection using OpenCV"](https://www.uet.edu.pk/Conferences/icosst2009/presentations_2009/Research_Papers/Visual_speech_detection_using_OpenCV.pdf), which claimed an accuracy of 60-75% when the luminosity thresholding was combined with other learning and statistical methods. In our (rather) small dataset of 6 videos, the average performance was 50-60% accuracy. Going forward, it would be beneficial to increase this dataset to increase our confidence in this accuracy. Of course, the dataset should contain a diverse set of speakers of different genders, backgrounds, and speaking styles. 

## Requirements
1. Python >= 3.8.5
1. Linux System

## Installation
1. `git clone https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification.git`
1. `pip install -r requirements.txt`
1. `python3 -m venv a2team6-env`
1. `source a2team6-env/bin/activate`
1. `./setup.sh`

## Demo Instructions
1. `source a2team6-env/bin/activate` (If venv has not been activated)
1. Unzip the `ref_rttms.zip` to get access to the reference rttm files. 
1. Download the demo YouTube videos with `downloadVideos.py`. There are a total of 6 videos.
1. Use `convertVideos.py` to setup video and audio in `convertedFiles` as needed by project. This converts the videos into 25 FPS and the audio into 16000 Hz sampled, 16-bit PCM wav files.
1. Run `./getVsdRttms.sh` to run `findMouthThresholdValue.py` on each of the videos in `/convertedFiles/video/`. Resulting `rttm` files will be in `/convertedFiles/video/` for each video.
1. Use `/ThirdPartyTools/dscore/score.py -r ./convertedFiles/uem/yourreference.rttm -s /path/to/generated/rttm.rttm` in `ThirdPartyTools/dscore/` for scoring the Video Speaker Detection against a reference file.

## Citations
Khan, Muhammad Usman Ghani ; Mahmood, Sajid ; Ahmed, Mahmood ; Gotoh, Yoshihiko . **Visual speech detection using OpenCV**. _Third International Conference on Open-Source Systems and Technologies_. University of Engineering & Technology Lahore. December 2009. https://www.uet.edu.pk/Conferences/icosst2009/presentations_2009/Research_Papers/Visual_speech_detection_using_OpenCV.pdf. 

Ryant, Neville. **dscore**. _GitHub_. 2019. https://github.com/nryant/dscore

Snyder, David; Chen, Guoguo; Povey, Daniel; **MUSAN: A Music, Speech, and Noise Corpus**. _arXiv_. 2015. https://www.openslr.org/17/