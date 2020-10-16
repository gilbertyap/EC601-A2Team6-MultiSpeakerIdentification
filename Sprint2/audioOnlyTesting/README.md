# Noise Testing

## Summary

This folder was used to generate noise on top of two sample audio files from the [VoxConverse](http://www.robots.ox.ac.uk/~vgg/data/voxconverse/index.html) dataset.

Our hypothesis was that an audio-only speaker identification system would struggle in the presence of noise. Using `pyannote-audio`'s pre-trained pipiline (based on the DIHARD dataset) we tested initially with generated white noise with mean 0 and standard deviation of 1. We used two files for testing from the `VoxConverse` dataset: `hycgx.wav` and `dvngl.wav`. Below are the tabulated results for this initial test:

|File | DER (%)| Noise SNR (dB)|
|-----|-----|-----|
|hycgx|11.22|N/A|
|hycgx_noise_001|27.20|14.47|
|hycgx_noise_002|26.89|20.42|
|hycgx_noise_004|27.00|26.53|
|hycgx_noise_008|27.04|32.22|
|hycgx_noise_016|12.05|38.23|
|hycgx_noise_032|28.10|43.83|
|hycgx_noise_064|11.45|51.43|
|dvngl| 21.07 |N/A|
|dvngl_noise_001| 32.18 | 15.23 |
|dvngl_noise_002| 25.17 | 20.08 |
|dvngl_noise_004| 24.50 | 25.81 |
|dvngl_noise_008| 24.98 | 31.98 |
|dvngl_noise_016| 26.89 | 38.29 |
|dvngl_noise_032| 26.87 | 44.45 |
|dvngl_noise_064| 22.15 | 50.39 |

As seen from the above table and charts, the DER was affected once the SNR dropped below 50 dB. DER in `hycgx.wav` did not continually increase in DER if the 1/16 trial is considered an outlier. However, `dvngl` did see a significant increase in DER once the noise amplitude maximum was allowed to be 1. For all other trials, the value of the DER hovered between 24% and 26%.

The next trial that was run was using random noise samples from the MUSAN dataset. White/Gaussian noise, while technically random, does not accurately simulate the types of noise that might be part of a recorded audio file. For example, in news broadcasting, a variety of environmental noises may appear and disappear throughout a recording such as car noises, wind, rain, background speech, etc.

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
