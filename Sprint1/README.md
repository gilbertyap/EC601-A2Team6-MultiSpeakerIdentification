# Team 5 - Sprint 1

Our team, Team 5, is aiming to find new improvements or implementations of multiple speaker identification for the team project. After the research done in Project 1, we saw that multiple speaker identification's main uses are in automatic transcription, forensics analysis, and AI systems. Until the recent machine learning boom, these applications had used traditional signal processing methods to perform speaker segmentation and clustering. Although these signal processing methods are continuing to advance, recent papers have shown that cross-discipline research is bringing the field to new heights.

For example, the papers (1) and (2) discuss how jointly performing Automatic Speech Recognition and Speaker Diarization leads to improve accuracy in 1-on-1 clinical transcriptions. These linguistic-based systems improve the "word diarization error rate", the percentage of words in an utterance that has been incorrectly labeled wit the wrong speaker identity, in doctor-patient roles where patients are presented with information and ask medical questions to a professional. These systems use CNN and RNN systems that are trained on thousands of hours of recordings.

Papers (3) and (4) examine the usage of video cues to aid in speaker identification. By using existing facial tracking software, systems can detect when a speaker's mouth is open or closed. Using this information along with audio thresholding and feature extracting can lead to much more accurate audio segments and speaker labels. While linguistic analysis is well-suited for identifying a low number of speakers (2 or 3), video information that clearly shows each speaker makes it easy to keep track of a higher number of speakers. In combination with speech databases, audio-visual speaker identification would be highly suited for broadcast news transcription.

## Product Mission

While we have not yet chosen which path of research we would like to continue with, we have created a product mission that broadly explains our motives.

"Our goal is to improve the multiple speaker identification system by combining traditional signal processing algorithms with environmental information, such as video and automatically generated text. We believe that by utilizing non-audio information, we can attain higher accuracy or better performance than current audio-only speaker diarization systems."

## MVP/MVP User Stories

### User Stories

The following are some example user stories that we considered:

```
With more patients opting to use telehealth during the current coronavirus pandemic, it is becoming more important for physicians and specialists to have records of the conversations that they have had with their patients. Depending on the medical office, it may not be feasible to keep audio or video records due to data storage resources or privacy concerns. Automatic transcripts would both reduce the amount of data needed to be stored and minimize personal information down from voice and facial data to plain text. Transcripts based on video calls could benefit from the increased accuracy of facial recognition algorithms that more accurately create speaking segments compared to audio-only processing.
```

```
Support call centers serve a specific role in a company's relationship with its customers. It can be important for companies to have records of the calls. While most call centers will record audio for future reference and training, it can be difficult to discern speech over the phone. Since call center employees are trained to respond to customers in very specific ways, a neural network could be trained to understand the linguistic role of a support agent and a customer based on text automatically generated from audio. Once these roles are established, labeling the identity of an utterance would become an easier task.
```

```
Body cameras and other recording devices are becoming more prevalent in police work. Like how customer support agents are trained to use certain vocabulary, so are police and other law enforcement officers. By utilizing the differences in speech style between civilians and trained police, there may be ways to improve transcriptions for later examination in police case files.
```

### MVP

Based on the user stories above, we came with the criteria for our MVP:

* Use of an existing audio-based speaker diarization system
  * Ideally, this framework would be modular. We would like to insert the facial recognition or text analysis in the part of the chain after the audio stream has been processed for feature extraction.

* An automatic text generation system.

* A linguistic analysis system such.

* A visual system capable of tracking facial features such as mouth movements.

* Various datasets for training/evaluating the system. These datasets would include audio, video, and text. The exact type of dataset will depend on the application that we decided to focus on at a later date.

* A Linux or MacOS development environment.

Here is a short list of resources that could help up accomplish the creation of our MVP:

### Text Analysis
* Python Natural Language Toolkit (NLTK) for text analysis.
* Google Cloud Natural Language Processing API

### Automatic Text Generation from Audio
* PyKaldi, a Python wrapper for the Kaldi automatic speech recognition toolkit.

### Audio-based Speaker Diarization Systems
* [pyannote-audio](https://github.com/pyannote/pyannote-audio) for Python

* [speaker-recognition](https://github.com/ppwwyyxx/speaker-recognition) for Python

### Facial Analysis Systems
* [lip-reading-deeplearning](https://github.com/astorfi/lip-reading-deeplearning)

* [mouth-open](https://github.com/mauckc/mouth-open)

### Datasets:
* [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/), which contains a collection of labeld/transcribed audio utterances and video clips taken from YouTube and verified manually.

* [DIHARD 3](https://dihardchallenge.github.io/dihard3/) speaker diarization competition. The competition provides a dataset and evaluation method to standardize the results of participants.

We are continuing to search for more open-source software libraries to aid in our product development.

---

(1) - https://arxiv.org/pdf/1907.05337.pdf

(2) - https://arxiv.org/pdf/1911.07994.pdf

(3) - https://arxiv.org/abs/2007.01216

(4) - https://www.mdpi.com/2414-4088/3/4/70