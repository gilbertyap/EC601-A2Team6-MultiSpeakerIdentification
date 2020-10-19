# Copies the original rttms to match all the audio files

import os, shutil
genList = os.listdir('../audio/')
genList.sort()

for file in genList:
    print('Making {}'.format(file))
    filename, fileext, = os.path.splitext(file)
    if 'dvngl' in filename:
        try:
            shutil.copy('dvngl.rttm', filename+'.rttm')
            lines = []
            with open(filename+'.rttm', 'r') as f:
                lines = f.readlines()
            for i in range(0, len(lines)-1):
                lines[i] = lines[i].replace('dvngl', filename)
            with open(filename+'.rttm', 'w') as f:
                f.writelines(lines)
        except:
            print('Could not copy dvngl.rttm to make {}'.format(filename+'.rttm'))
            continue

    if 'hycgx' in file:
        try:
            shutil.copy('hycgx.rttm', filename+'.rttm')
            lines = []
            with open(filename+'.rttm', 'r') as f:
                lines = f.readlines()
            for i in range(0, len(lines)-1):
                lines[i] = lines[i].replace('hycgx', filename)
            with open(filename+'.rttm', 'w') as f:
                f.writelines(lines)
        except:
            print('Could not copy dvngl.rttm to make {}'.format(filename+'.rttm'))
            continue
