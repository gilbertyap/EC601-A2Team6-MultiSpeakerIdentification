# Audio-Only Testing Continued

## Installation
Note that `pyannote-audio` does not perform well in Windows. Please use Linux or Mac OS for testing.

After cloning this repo
* `git clone https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification.git`
* `cd EC601-A2Team6-MultiSpeakerIdentification`
* `chmod +X setup.sh
* `./setup.sh`
* `cd Sprint3/audioOnlyTesting/`

## Summary

This folder `audioOnlyTesting` contains a series of bash scripts that were used to train the `pyannote-audio` neural network for speaker diarization. [This folder](https://github.com/pyannote/pyannote-audio/tree/develop/tutorials/) from the repository was used as a starting point for training the neural network. The goal for Sprint 3 was to complete training of the neural network on the VoxConverse dataset and observe how DER scores improved. 

When training each module in the `pyannote-audio` neural network, a `config.yml` file is used to configure the training process. For example, in training Speech Activity Detection (SAD), developers can configure the audio "chunk" size to train against, the min and max SNR of additional background noise, the LSTM  size and layers, etc. For simplicity, the default settings for SAD, SCD, and EMB were used. The reason that OVL was not trained was because it is not part of the speaker diarization pipeline. The VoxConverse dataset was broken up into 3 different sets at random: `train`, `development`, and `test`. The `test` set is double the size of `train` and `development`.

The process for training for each of the neural network modules is `train`, `validate`, and then `apply`. The training process of `pyannote-audio` starts with performing feature extraction with a sinc function convolution (like SincNet) on the `train` dataset. Then the features are fed into a RNN to generate the loss values. Each epoch of training also saves the "hyper-parameter" configuration, which is the set of parameters that the epoch used. For something like SAD, this includes values like the minimum duration of speech and non-speech, as well as the amplitude threshold value. The `validate` portion then goes through each of the epochs and finds the best epoch for the `development` dataset. Finally, the `apply` portion uses the optimal parameters and runs it on the `test` dataset. This generates scores/embeddings that will be used in the speaker diarization pipeline.

After each module has gone through these three steps, the pipeline needs to be trained in a similar manner. The training process is broken up into only 2 parts: `train` and `apply`. Another `config.yml` file is used for the pipeline to direct the pipeline training commands to the applied SAD, SCD, and EMB models. In this file, developers may choose to freeze some of the settings so that they are not altered in the pipeline training. The default tutorial recommends freezing the SAD hyper-parameters. After running `train`, a `params.yml` file will be generated. This parameter file gives further tunings of each of the modules in the pipeline. You will values for minimum chunk duration, speech turn assignment, speech turn clustering, speech turn segmetnation, and speech activity detection. Once developers are satisified with amount of training run, they can run the `apply` stage against the `test` dataset. At this point, the DER values are output for each file tested.

## Observations/Results

In testing this audio-only solution, we believed that we had run each portion of this training correctly. We were able to generate the scores for SAD and SCD without any issues. However, we ran into issues with training the speaker embedding portion of the neural network. The `validate` stage continued to return an error, which we [reported to the authors](https://github.com/pyannote/pyannote-audio/issues/463) of `pyannote-audio`. As of November 1st 2020, there has been no response. 

Since this issue occured about a week before Sprint 3's deadline, an alternate approach was taken to check new DER scores. Rather than having all three modules trained on VoxConverse, we attempted to train the speaker diarization pipeline with only the SAD and SCD modules trained and used the EMB model that was pretrained on the VoxCeleb1 dataset. Below we outline the results of the pipeline that uses all pre-trained modules vs ours that had 2 of the 3 trained on VoxConverse:

**Pretrained**
**This is where you would put pre-trained**

**Custom Trained**
**This is where you would put custom trained**

As seen from the DER scores...**results here**.

## Next Steps

As of today, it is unclear if the errors with the training arose from the VoxConverse dataset or from the `pyannote-audio` library itself. In the next sprint, we are considering gather new videos and audio that better simulate the conditions we are hoping to optimize against - noisy audio samples from sub-optimal recording conditions.

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
