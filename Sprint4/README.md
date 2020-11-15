# Sprint 4

## Summary

In Sprint4, we focused on collecting data from the "[VoxCeleb dataset](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/)", processing the videos, and performing tests on example videos through the "[mouth-open](https://github.com/mauckc/mouth-open/)" repo. Additionally, some tests for `pyannote-audio` were rerun after the author of the library helped remedy the training issue from Sprint 2 and 3. 

At the end of Sprint 3, we set up a three main goals: 

1. Gather videos from the VoxCeleb dataset (Specifically their `VoxCeleb1` subset) and manually find videos of interest.

1. Switch testing to the `mouth-open` repo from the `lip-reading-deeplearning` repo to see if it can visually detect when a person is speaking with accuracy that matches the VoxCeleb timestamps.

1. If time allowed, start working on expanding the system architecture of our project. This would involve beginning to develop the algorithm that would pick between prioritizing `pyannote-audio` or the open mouth detection of `mouth-open`.

For the first goal, we created a script (`downloadVideos.py`) that would randomly download any number of videos from the `VoxCeleb` dataset directly from YoutTube. As we discovered in Sprint 3, videos with video quality of <= 480p could cause issues, so we opted to download videos that were 720p quality. Some of the `VoxCeleb` videos did not reach this requirement, but luckily the dataset has about 11,000 video links in just the `VoxCeleb1` subset. There are even more in the `VoxCeleb2` subset.

The timestamps provided with the `VoxCeleb` dataset are specified with frame numbers when the video is played at 25 fps, so after downloading videos, processing of the video and audio was required. "[MoviePy](https://github.com/Zulko/moviepy)" was used to get the audio from the video and adjust its sampling rate to 48,000KHz (requirement for `pyannote-audio`). The video was then converted to 25 fps. Both the converted video and audio are saved to separate folders from the original video. The original videos can probably be deleted once we have converted all of our desired videos.

Once we had downloaded a few videos, we started to run tests with `mouth-open`. First, we wanted to check if the repo would be able to detect multiple faces in one frame. Contrary to what we believed in Sprint 3, the library is able to detect multiple faces in a frame. However, it does not distinguish each face when calculating the Mouth Aspect Ratio (MAR), which tells us if a mouth is open. This is one shortcoming we may need to overcome in future tests. Additionally, we found that `mouth-open` does not deal well with side profiles of faces. This issue is due to the face profile used by `dlib`, which tracks 68 facial landmarks, it cannot deal with faces that are turned more than about ~45 degrees. We learned of an open-source library called "[face-alignment](https://github.com/1adrianb/face-alignment)", a deep-learning based facial landmark network, that is able to track facial landmarks in three dimensions. We may consider adapting the MAR algorithm for this library to improve mouth tracking in side profiles. Since side profiles are less frequently used in media, this is a low priority.

We also heard back from the author of `pyannote-audio` regarding our issue with training the Speaker Embedding module. It turned out that the `VoxConverse` dataset contained audio files that contained only 1 speaker in them. There was a prerequisite with using the Speaker Embedding module that required there be at least 2 or more speakers per audio file. This allowed us to finish validating the Speaker Embedding module that we custom trained, as well as train a speaker diarization pipeline based on all of our custom trained models. The results of the pipeline were still not better than the pretrained models, but we believe that this is due to the lack of training time. Each module was trained within a 24-hour period and the pipeline was initially trained with only 100 epochs (as opposed to letting it run "forever" until the loss value was "good enough", according to `pyannote-audio`'s tutorials). We did see though that rerunning the training with 135 epochs gave a 4% decrease in the total DER value of our test set. We hope to rerun the training with about 300 epochs to prove that increasing the number of epochs should get us closer to the DER values from the pre-trained model. The following is a link to our test result comparisons between our three pipelines:

https://docs.google.com/spreadsheets/d/1d31OD8tU7RA9N4BaHeTrPBjyTb50P18-OOX3IEhfE6k/edit?usp=sharing

These results show us that with our constraints while using the SCC, we may not be able to get the same results as the pre-trained models. Since we are using the VoxCeleb1 dataset, we may be better off using the pre-trained model provided by `pyannote-audio` through Torch Hub. However, our above results show that continued training of the network does yeild better results.

## Next Steps
