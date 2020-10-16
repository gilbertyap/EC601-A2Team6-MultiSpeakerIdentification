import contextlib, numpy, os, struct, sys, wave

# arg 0 - filepath
# arg 1 - 1/(arg 1) max amplitude of noise
def main(filePath, scale):
    if ('.wav' in filePath):
        # magnitude values that corresponding to integer values
        bins = numpy.array(numpy.linspace(-1,1,numpy.power(2,16)))

        frames_num = 0
        wave_data = None
        print('Getting frames of {}'.format(filePath))
        with contextlib.closing(wave.open(filePath,'rb')) as wf:
            frames_num = wf.getnframes()
            wave_data = wf.readframes(frames_num)

        # De-quantization
        # Go through every two bytes and convert it into a magnitude value b/w -1 and 1
        print('De-quantizing')
        wave_mag = []
        i = 0
        while i < int(len(wave_data)-1):
            wave_2_bytes = (wave_data[i+1] << 8) + (wave_data[i])
            wave_mag.append(bins[wave_2_bytes])
            i+=2
        wave_mag = numpy.array(wave_mag)

        # Generate noise and scale it between -1 and 1
        print('Generating noise')
        noise_signal = numpy.random.normal(0, 1, size=frames_num)
        if abs(numpy.max(noise_signal)) >= abs(numpy.min(noise_signal)):
            noise_signal = noise_signal / numpy.abs(numpy.max(noise_signal))
        else:
            noise_signal = noise_signal / numpy.abs(numpy.min(noise_signal))

        #  Scale the noise to a smaller magnitude
        noise_signal = 1/int(scale) * noise_signal

        # Get the RMS of each
        wave_rms = numpy.sqrt(numpy.sum(numpy.power(wave_mag,2))/frames_num)
        noise_rms = numpy.sqrt(numpy.sum(numpy.power(noise_signal,2))/frames_num)

        # dB and SNR calculation
        wave_db = 20 * numpy.log10(wave_rms)
        noise_db = 20 * numpy.log10(noise_rms)
        snr = wave_db - noise_db
        print('Audio:{} dB, Noise:{} dB, SNR:{} dB'.format(wave_db, noise_db, snr))

        # Combine two signals and clip
        print('Combining signals')
        new_wave = wave_mag + noise_signal

        print('Clipping values')
        numpy.clip(new_wave, -1, 1, new_wave)
        new_wave = numpy.digitize(new_wave, bins)

        python_list = new_wave.tolist()
        new_wave_bytes = []
        print('Constructing new bytes')
        for val in python_list:
            new_wave_bytes.append(val & 0x00FF)
            new_wave_bytes.append((val & 0xFF00)>>8)

        print('Creating new wav file')
        fileName, fileExt = os.path.splitext(filePath)
        with contextlib.closing(wave.open(fileName+'_noise_'+str(scale).zfill(3)+'.wav', 'wb')) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(bytes(new_wave_bytes))

        # print('Generating log file')
        with open('snr.txt','a') as f:
            f.write('File:{} , Scale: 1/{}, SNR:{}'.format(filePath, scale, round(snr,2)))
            f.write()


if __name__ == '__main__':
    args = sys.argv[1:]
    filePath = str(args[0])
    scale = int(args[1])
    main(filePath, scale)
    sys.exit(0)
