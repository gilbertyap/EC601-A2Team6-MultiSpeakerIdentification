# ************************************************************
# Author: Gilbert Yap
# Date: October 18, 2020
# filename: addRecordedNoise.py
# Summary: Combines two files while scaling the max amplitude of the noise file
# Command Arguements: addGWN.py reference/file/path noise/file/path noise_scale_integer
# ************************************************************
import audioop, contextlib, numpy, os, struct, sys, wave

bins = numpy.array(numpy.linspace(-1,1,numpy.power(2,16)))

# Returns the quantized signal of an audio file
def getAudioFileData(filePath):
    file_data = None
    print('Getting frames of {}'.format(filePath))
    with contextlib.closing(wave.open(filePath,'rb')) as wf:
        # print('*****Params: '+ str(wf.getparams()))
        file_data = wf.readframes(wf.getnframes())

    return file_data

# Returns signal in magntitude scale:
def dequantizeFile(file_data):
    # De-quantization
    # Go through every two bytes and convert it into a magnitude value b/w -1 and 1
    file_mag = []
    i = 0
    while i < int(len(file_data)-1):
        file_2_bytes = (file_data[i+1] << 8) + (file_data[i])
        file_mag.append(bins[file_2_bytes])
        i+=2

    return numpy.array(file_mag)

# arg 0 - refFilePath
# arg 1 - noiseFilePath
# arg 2 - 1/(arg 2) max amplitude of noise
# Generate the corresponding audio files with the noise scaled by 1, 1/2, 1/4, 1/8, 1/16, and 1/32
def main(refFilePath, noiseFilePath, minimumScale):
    scaleList = []
    i = 1
    while i <= minimumScale:
      scaleList.append(i)
      i *= 2

    for scale in scaleList:
        if (('.wav' in refFilePath) and ('.wav' in noiseFilePath) ):
            # Get reference file frames
            sampwidth = 2
            wave_data = getAudioFileData(refFilePath)
            ref_frames_num = len(wave_data)

            # Get noise file frames
            noise_data = getAudioFileData(noiseFilePath)

            #  Scale the noise to a smaller magnitude, 1/scale
            print('Reducing magntitude of noise by 1/{}'.format(scale))
            noise_data = audioop.mul(noise_data, sampwidth, 1/scale)

            # De-quantizate the noise file
            noise_mag = dequantizeFile(noise_data)

            print('Scaling the noise to fit the reference file')
            # Numpy takes care of repeating "noise_mag" when it resizes
            scaled_noise_mag = noise_mag
            scaled_noise_mag = numpy.resize(noise_mag, int(ref_frames_num/2))
            scaled_noise_data = bytearray()
            for index in numpy.digitize(scaled_noise_mag, bins).tolist():
                scaled_noise_data.append(index & 0x00FF)
                scaled_noise_data.append((index & 0xFF00) >> 8)

            # Get the RMS of each
            wave_rms = audioop.rms(wave_data, sampwidth)
            noise_rms = audioop.rms(scaled_noise_data, sampwidth)

            # dB and SNR calculation
            wave_db = 20 * numpy.log10(wave_rms)
            noise_db = 20 * numpy.log10(noise_rms)
            snr = wave_db - noise_db
            print('Audio:{} dB, Noise:{} dB, SNR:{} dB'.format(wave_db, noise_db, snr))

            # Combine two signals and clip
            print('Combining signals')
            new_wave_bytes = audioop.add(wave_data, scaled_noise_data, sampwidth)

            print('Creating new wav file')
            refFileName, refFileExt = os.path.splitext(refFilePath)
            noiseDir, noiseFullName = os.path.split(noiseFilePath)
            noiseFileName, noiseFileExt = os.path.splitext(noiseFullName)
            finalFileName = refFileName+'_'+noiseFileName+'_'+str(scale).zfill(3)+'.wav'
            with contextlib.closing(wave.open(finalFileName, 'wb')) as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(bytes(new_wave_bytes))
            print('File created. Location is {}'.format(finalFileName))

            # print('Generating log file')
            with open('snr.txt','a') as f:
                f.write('File:{} , Scale: 1/{}, SNR:{}\n'.format(finalFileName, scale, round(snr,2)))

            # Make gap between trials
            print('')
        else:
            print('Error! Can only execute on .wav files with sampling rate 16,000KHz and 16-bit depth.')
            sys.exit(1)

if __name__ == '__main__':
    args = sys.argv[1:]
    refFilePath = str(args[0])
    noiseFilePath = str(args[1])
    minimumScale = int(args[2])
    try:
      main(refFilePath, noiseFilePath, minimumScale)
      sys.exit(0)
    except:
      print('Could not add noise to all files correctly.')
      sys.exit(1)
