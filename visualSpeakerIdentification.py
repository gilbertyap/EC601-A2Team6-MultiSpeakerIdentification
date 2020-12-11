# visualSpeakerIdentification.py
# https://github.com/gilbertyap/EC601-A2Team6-MultiSpeakerIdentification/blob/master/visualSpeakerIdentification.py
# Script to detect speaker within a video based on a luminosity mask around the speaker's mouth
# Code based on detect_videofile_mouth.py from https://github.com/mauckc/mouth-open/

from imutils.video import FileVideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import csv, os, sys

# Generate average luminosity value for a frame
# TODO: Should this be normalized?
def get_luminosity(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    luminosity = grayFrame.sum()
    nonMaskPixels = np.array(np.nonzero(grayFrame)).size
    # print('L: {}, Total: {}, Avg: {}'.format(luminosity, nonMaskPixels, round(luminosity/(nonMaskPixels))))
    return luminosity/(nonMaskPixels)

# Generates the rttm of the video based on the mouth luminosity values of the whole video
def generate_video_speaker_detection_rttm(frameAndLumList, fileName):
    newFrameAndLum = []
    threshold = np.mean(frameAndLumList[1]) + (0.75*np.sqrt(np.var(frameAndLumList[1])))
    print('Threshold is {}'.format(threshold))
    for i in range(0, len(frameAndLumList[0])):
        if frameAndLumList[1][i] <= threshold:
            newFrameAndLum.append(frameAndLumList[0][i])

    # Generate the offsets of each sections where the mouth is open
    offsets = [[],[]]
    startIndex = 0
    for i in range(0, len(newFrameAndLum)-1):
        if (newFrameAndLum[i] != (newFrameAndLum[i+1])-1):
            # Sum all of the previous frames into one offset
            offsets[0].append(newFrameAndLum[startIndex]/25)
            offsets[1].append((newFrameAndLum[i]-newFrameAndLum[startIndex]+1)/25)
            startIndex = i+1

    with open(fileName+'_vsd.rttm','w') as f:
        for i in range(0, len(offsets[0])):
            f.write('SPEAKER {} 1 {} {} <NA> <NA> 1 <NA> <NA>\n'.format(fileName, offsets[0][i], offsets[1][i]))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default="",
                    help="video path input")
    args = vars(ap.parse_args())

    # Initialize dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    # Indices of mouth in dlib detector
    (mStart, mEnd) = (49, 68)

    try:
        fvs = FileVideoStream(path=args["video"]).start()
    except:
        print('Cannot open file!')
        sys.exit(1)

    frame_width = 640
    frame_height = 360

    framerate = 25
    frameAndLumList = [[],[]]

    # Create CSV file for the pixel coordinates of the outline
    fileName, fileExt = os.path.splitext(args["video"])
    faceDetectFile = fileName+'_faceDetectFile.csv'
    with open(faceDetectFile, 'w') as f:
        writer = csv.writer(f)

    frameNum = 0
    faceCounter = 0
    while True:
        # Read the frames of the video and stop loop when there are no more frames
        frame = fvs.read()
        if not (frame is None):
            if(frameNum % 100) == 0:
                print('Frame num : {}'.format(frameNum))

            # Resize video and change to grayscale
            frame = imutils.resize(frame, width=frame_width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray, 0)

            imgMask = np.zeros(frame.shape, np.uint8)
            imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

            # Go through all faces
            for face in faces:
                # TODO: Should we be using ML to track faces?
                shape = predictor(gray, face)
                shape = face_utils.shape_to_np(shape)
                mouth = shape[mStart:mEnd]

                # Create a line around the mouth of the speaker based on landmarks
                mouthHull = cv2.convexHull(mouth)
                
                # Generate a mask for each mouth
                mask = np.zeros(frame.shape, np.uint8)
                mask = cv2.drawContours(mask, [mouthHull], -1, (255,255,255), -1)
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                imgMask = cv2.bitwise_or(imgMask, mask)
                maskedImage = cv2.bitwise_and(frame, frame, mask=mask)
                frameAndLumList[0].append(frameNum)
                frameAndLumList[1].append(get_luminosity(maskedImage))
                faceCounter+=1
                
            with open(faceDetectFile, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([frameNum, faceFound])
            frameNum+=1
        else:
            break

    print('Finished!')
    print('Closing everything.')
    print('Face found in {}  of {} frames'.format(faceCounter, frameNum))
    cv2.destroyAllWindows()
    fvs.stop()
    
    try:
        print('Creating vsd -based rttm.')
        generate_video_speaker_detection_rttm(frameAndLumList, fileName)
    except:
        sys.exit(1)
    sys.exit(0)
