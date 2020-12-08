# Generates the webrtcvad files in UEM format

import contextlib, os, webrtcvad, wave

# Returns the quantized signal of an audio file
def getAudioFileData(filePath):
    file_data = None
    print('Getting frames of {}'.format(filePath))
    with contextlib.closing(wave.open(filePath,'rb')) as wf:
        file_data = wf.readframes(wf.getnframes())

    return file_data

if __name__ == '__main__':
    # Initiate VAD
    vad = webrtcvad.Vad()
    vad.set_mode(3)

    convertAudioFolder = './convertedFiles/audio/'
    uemFolder = './convertedFiles/uem/'
    if not os.path.isdir(uemFolder):
        os.mkdir(uemFolder)
    fileList = os.listdir(convertAudioFolder)

    sample_rate = 16000
    frame_duration = 10  # ms

    for file in fileList:
        fileBytes = getAudioFileData(convertAudioFolder+file)
        fileName, fileExt = os.path.splitext(file)
        with open(uemFolder+fileName+'.uem','w') as f:
            i=0
            isSpeechTurn = False
            currentTurnDuration = 0.0
            startTime = 0.0
            # Frame is bytes per 10ms 
            frameSize = 2*int(sample_rate * frame_duration / 1000)
            
            print('Generating turns for {}...'.format(file))
            for i in range(0, int(len(fileBytes)/frameSize)):
                frame = fileBytes[frameSize*i:(frameSize*i)+frameSize]
                if (vad.is_speech(frame, sample_rate) != isSpeechTurn):
                    if isSpeechTurn:
                        # Check for audio "chunks" that are only greater than 2 seconds long
                        # if round(currentTurnDuration / 1000,3) >= 1:
                        f.write('{} 1 {} {}\n'.format(fileName, round(startTime,2), round(startTime+round(currentTurnDuration / 1000,3),2)))
                        # Export the frame to a wav file
                        # with contextlib.closing(wave.open(uemFolder+fileName+'_'+str(i)+'.wav', 'wb')) as wf:
                            # wf.setnchannels(1)
                            # wf.setsampwidth(2)
                            # wf.setframerate(sample_rate)
                            # wf.writeframes(fileBytes[frameSize*(i-int(currentTurnDuration/10)):(frameSize*i)+frameSize])
                    startTime = round((i * frame_duration)/(1000), 3)
                    currentTurnDuration = 0.0
                    isSpeechTurn = vad.is_speech(frame, sample_rate)
                else:
                    currentTurnDuration += frame_duration
        print('Finished with {}'.format(file))