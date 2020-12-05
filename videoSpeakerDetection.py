# USAGE
# python getOpenFrames.py -v video.mp4
# or 
# python getOpenFrames.py --video video.mp4

# import the necessary packages
from imutils.video import FileVideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import csv
import os, sys

def get_luminosity_of_masked_image(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # In the frame, there will be black pixels representing the masked portions, do not count those in the average
    luminosity = 0
    nonMaskPixels = 0
    luminosity = grayFrame.sum()
    nonMaskPixels = np.array(np.nonzero(grayFrame)).size
    # print('L: {}, Total: {}, Avg: {}'.format(luminosity, nonMaskPixels, round(luminosity/(nonMaskPixels))))
    # return round(luminosity/(nonMaskPixels))
    return luminosity/(nonMaskPixels)


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default="",
                    help="video path input")
    ap.add_argument("-t", "--threshold", default="65.0",
                    help="Luminosity threhold value")
    args = vars(ap.parse_args())

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    # grab the indexes of the facial landmarks for the mouth
    (mStart, mEnd) = (49, 68)

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    try:
        fvs = FileVideoStream(path=args["video"]).start()
    except:
        print('Cannot open file!')
        sys.exit(1)

    frame_width = 640
    frame_height = 360

    framerate = 25
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    fileName, fileExt = os.path.splitext(args["video"])
    out = cv2.VideoWriter(fileName+'_mouth.avi',cv2.VideoWriter_fourcc('M','J','P','G'), framerate, (frame_width,frame_height))

    # Read the csv files from the first pass
    # Calculate the threshold value
    with open(mouthLumCsvName, 'r') as mouthLumCsv:
        mouthLumCsvReader = csv.reader(mouthLumCsv)
        luminosityList = []
        for row in mouthLumCsvReader:
            if row != []:
                luminosityList.append(row[1])
        threshold = np.mean(luminosityList) + (0.75*np.sqrt(np.var(luminosityList)))
        

    # Have the mouth landmark coordinates ready so that you can draw the convex hull easily
    mouthCoorCsvName = fileName+'_mouthCoor.csv'
    with open(mouthCoorCsvName, 'r') as mouthCoorCsv:
        # mouthCoorCsvWriter = csv.writer(mouthCoorCsv)

    # loop over frames from the video stream
    frameNum = 0
    while True:
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = fvs.read()
        if not (frame is None):
            frame = imutils.resize(frame, width=frame_width)
            
            # Write the frame into the file 'output.avi'
            out.write(frame)
            frameNum+=1
        else:
            break

    print('Finished!')
    print('Closing everything.')

    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()
    sys.exit(0)
