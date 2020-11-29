# This file is for manually making reference rttms files
# This process uses the most aggressive setting of webrtcvad with a 30ms window
# to detect voice in an audio file. The user is then responsible for giving
# an identity to each audio clip.

import contextlib, os, simpleaudio, webrtcvad, wave

# Returns the quantized signal of an audio file
def getAudioFileData(filePath):
    file_data = None
    print('Getting frames of {}'.format(filePath))
    with contextlib.closing(wave.open(filePath,'rb')) as wf:
        file_data = wf.readframes(wf.getnframes())

    return file_data

# Function for documenting the speaker
def pickSpeaker(speakerList):
    if len(speakerList) == 0:
        print('Please give speaker an identity (1,2,3...,etc.).')
        print('You can use multiple numbers for overlap (12, 13, etc.).')
        print('Please use NA for non-speech.')
        speaker = input()
        print('')
        speakerList.append(speaker)
    else:
        print('Current speaker list: {}'.format(speakerList))
        print('Please pick a speaker identity or add a new one.')
        print('You can use multiple numbers for overlap (12, 13, etc.).')
        print('Please use NA for non-speech.')
        speaker = input()
        print('')
        if not (speaker in speakerList):
            speakerList.append(speaker)
    return (speaker, speakerList)

if __name__ == '__main__':
    # Initiate VAD
    vad = webrtcvad.Vad(3)

    convertAudioFolder = './convertedFiles/audio/'
    uemFolder = './convertedFiles/uem/'
    referenceRttmsFolder = './convertedFiles/referenceRttms/'
    tempFolder = './tempFolder/'
    if not os.path.isdir(uemFolder):
        os.mkdir(uemFolder)
    if not os.path.isdir(referenceRttmsFolder):
        os.mkdir(referenceRttmsFolder)
    fileList = os.listdir(convertAudioFolder)
    if not os.path.isdir(tempFolder):
        os.mkdir(tempFolder)

    sample_rate = 16000
    frame_duration = 10  # ms

    for file in fileList:
        fileBytes = getAudioFileData(convertAudioFolder+file)
        fileName, fileExt = os.path.splitext(file)
        with open(referenceRttmsFolder+fileName+'.rttm','w') as f:
            i=0
            isSpeechTurn = False
            speakerList=[]
            currentTurnDuration = 0.0
            startTime = 0.0
            # Frame is bytes per frame_duration, sample is 2 bytes
            frameSize = 2*int(sample_rate * frame_duration / 1000)
            
            print('Generating reference rttm for {}...'.format(file))
            for i in range(0, int(len(fileBytes)/frameSize)):
                frame = fileBytes[frameSize*i:(frameSize*i)+frameSize]
                if (vad.is_speech(frame, sample_rate) != isSpeechTurn):
                    if isSpeechTurn:
                        # Create a blank wave file
                        with open(tempFolder+fileName+'.wav', mode='w') as f2:
                            pass

                        # Temporarily save the wave file
                        # TODO: Could probably find a library that reads the bytes from Python directly
                        with contextlib.closing(wave.open(tempFolder+fileName+'.wav', mode='wb')) as wf:
                                wf.setnchannels(1)
                                wf.setsampwidth(2)
                                wf.setframerate(sample_rate)
                                wf.writeframes(fileBytes[frameSize*(i-int(currentTurnDuration/frame_duration)):(frameSize*i)+frameSize])

                        # Playback the sound and have the user give the speaker an id
                        print('Playing voice clip found at {}'.format(startTime))
                        waveObj = simpleaudio.WaveObject.from_wave_file(tempFolder+fileName+'.wav')
                        playObj = waveObj.play()
                        playObj.wait_done()
                        (speaker, speakerList) = pickSpeaker(speakerList)
                        f.write('SPEAKER {} 1 {} {} <NA> <NA> {} <NA> <NA>\n'.format(fileName, startTime, round(currentTurnDuration / 1000,3), speaker))

                    startTime = round((i * frame_duration)/(1000), 3)
                    currentTurnDuration = 0.0
                    isSpeechTurn = vad.is_speech(frame, sample_rate)
                else:
                    currentTurnDuration += frame_duration
            # TODO: If the file cannot be divided into an integer amount of frame sizes,
            # process the last samples separately
        print('Finished with {}'.format(file))