# Noise Testing

## Installation

After cloning this repo
`cd EC601-A2Team6-MultiSpeakerIdentification/Sprint2/audioOnlyTesting`
`pip install -r requirements.txt`

Note that `pyannote-audio` does not perform well in Windows. Please use Linux or Mac OS for testing.

## Instructions

Below is a sample run of this folder.
* `python addRecordedNoise.py ./audio/dvngl.wav ./noise/gwn.wav`
* `python ./ref/copyRttms.py`
* `python generateRttms.py`
* `python ../../ThirdPartyTools/dscore/score.py -R reference.scp -S score.scp`

`addRecordedNoise.py` takes two parameters: 1. reference audio file path 2. noise audio file path. The script will then generate a number of audio files in `./audio/` of the reference audio file with the noise placed on top at varying scales. The generated file name follows the convention of `(reference file name)_(noise file name)_(scale).rttm`.

`copyRttms.py` generates copies of the base RTTM file for use with dscore

`generateRttms.py` runs the diarization against the DIHARD pre-trained diarization pipeline from `pyannote-audio`.

`python ../../ThirdPartyTools/dscore/score.py -R reference.scp -S score.scp` will display the DER scores in the command window. Please see `reference_scores.txt` to see that your values match.

## Test

This folder was used to place noise, mainly from the [MUSAN dataset](http://www.openslr.org/17/), on top of two sample audio files from the [VoxConverse](http://www.robots.ox.ac.uk/~vgg/data/voxconverse/index.html) dataset.

Our hypothesis was that an audio-only speaker identification system would struggle in the presence of noise. Using `pyannote-audio`'s pre-trained pipiline (based on the DIHARD dataset) we tested against four forms of audio noise. We randomly chose and used two files for testing from the `VoxConverse` dataset: `hycgx.wav` and `dvngl.wav`. The four forms of noise (which were also randomly chosen) are as follows:

* 10 Seconds of Gaussian white noise - Generated in Python using NumPy
* `music-hd-0000.wav` from the MUSAN dataset. This file is a solo piano piece.
* `music-jamendo-0000.wav` from the MUSAN dataset. This file is recording of jazz music.
* `noise-free-sound-0042.wav` from the MUSAN dataset. This file is a recording of outdoor rain noise.

## Results

Both `hycgx.wav` and `dvngl.wav` were tested against the four forms of noise while varying the Signal to Noise Ratio (SNR). There were 6 trials for each noise file, and each trial the noise was scaled down by a factor of two (1/2). Below are the results:

### Gaussian White Noise
[dvngl_gwn](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'dvngl.wav'%20with%20GWN.png)

[hycgx_gwn](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'hycgx.wav'%20with%20GWN.png)

For GWN, there appeared to be an logarithmically decaying relationship between DER and SNR. As the SNR increased by 6dB, the DER would exponentially decay at first and then hover at one value. Additional tests were run to include scales of 1/64, 1/128, and 1/256, but the DER did not converge to the base DER value without noise.

### music-hd-0000.wav
[dvngl_hd-0000](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'dvngl.wav'%20with%20'music-hd-000.wav'.png)

[hycgx_hd-0000](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'hycgx.wav'%20with%20'music-hd-000.wav'.png)

The file `music-hd-0000.wav` appeared to only slightly affect the two sample audio files' DER value. There is a decreasing relationship between the DER and the SNR, but it does not quite fit a linear relationship.

### music-jamendo-0000.wav
[dvngl_jamendo-0000](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'dvngl.wav'%20with%20'noise-free-sound-0042.wav'.png)

[hycgx_jamendo-0000](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'hycgx.wav'%20with%20'music-jamendo-000.wav'.png)

For `music-jamendo-0000.wav`, there appears to be an exponentially decaying relationship between DER and SNR.

### noise-free-sound-0042.wav
[dvngl_noise-0042](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'dvngl.wav'%20with%20'noise-free-sound-0042.wav'.png)

[hycgx_noise-0042](https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/gilbert_sprint2/Sprint2/audioOnlyTesting/charts/SNR%20and%20DER%20for%20'hycgx.wav'%20with%20'noise-free-sound-0042.wav'.png)

For `noise-free-sound-0042.wav`, the DER did not follow the same trend for `dvngl.wav` as it did for `hycgx.wav`. `hycgx.wav` had a trend of decreasing DER as SNR went up, but `dvngl.wav` did not.

## Observations

With our limited reference file and noise testing, we empirically found that in most scenarios, the DER values calculated for our files would decrease as the SNR increased. Not all of our tests converged to the base DER value, so we cannot say that there is a specific SNR value for all files such that the DER value is the same as the reference file's original DER.

Since we only tested with two sample files, it may be of interest to test against a few more audio files to see if the results are consistent.

One interesting fact is that the `pyannote-audio` library uses the MUSAN dataset to train its neural network blocks in a similar process; it randomly picks a file and alters the SNR between 5 and 20 dB during the training process. This ensures that meaingful  filters and embeddings are created.

## Citations:
VoxConverse Dataset
```
@article{chung2020spot,
  title={Spot the conversation: speaker diarisation in the wild},
  author={Chung, Joon Son and Huh, Jaesung and Nagrani, Arsha and Afouras, Triantafyllos and Zisserman, Andrew},
  journal={arXiv preprint arXiv:2007.01216},
  year={2020}
}
```

MUSAN Dataset
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
