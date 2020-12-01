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
    csvFile = open(fileName+'.csv', 'w')
    csvWriter = csv.writer(csvFile)
    csvFile.close()
    # csvWriter.writerow(['Frame rate', '{} fps'.format(str(framerate))])
    # csvWriter.writerow(['Frame number', 'Luminosity'])

    # loop over frames from the video stream
    frameNum = 0
    while True:
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = fvs.read()
        if not (frame is None):
            frame = imutils.resize(frame, width=frame_width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
            faces = detector(gray, 0)

            # loop over the face detections
            imgMask = np.zeros(frame.shape, np.uint8)
            imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)
            if(frameNum % 100) == 0:
                print('Frame num : {}'.format(frameNum))
            
            i=0
            for face in faces:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, face)
                shape = face_utils.shape_to_np(shape)
                # TODO: Should we be using ML to track faces?
                
                # extract the mouth coordinates, then use the
                # coordinates to compute the mouth aspect ratio
                mouth = shape[mStart:mEnd]
                
                # compute the convex hull for the mouth, then
                # visualize the mouth
                mouthHull = cv2.convexHull(mouth)
                
                # Generate a mask for each mouth
                mask = np.zeros(frame.shape, np.uint8)
                mask = cv2.drawContours(mask, [mouthHull], -1, (255,255,255), -1)
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                imgMask = cv2.bitwise_or(imgMask, mask)
                maskedImage = cv2.bitwise_and(frame, frame, mask=mask)
                averageLuminosity = get_luminosity_of_masked_image(maskedImage)
                csvFile = open(fileName+'.csv', 'a')
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow([frameNum, averageLuminosity])
                csvFile.close()
                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, "Avg Lum: {}".format(averageLuminosity), (30+(120*i), 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Draw text if mouth is open
                try:
                    lumThresh = float(args['threshold'])
                except:
                    print('Input threhold value not valid!')
                    sys.exit(1)
                
                if averageLuminosity < lumThresh:
                  if i == 0:
                      cv2.putText(frame, "Speaker is speaking!", (30,60),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
                  else:
                      cv2.putText(frame, "Speaker is speaking!", (640-120,60),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
                  # print('Current frame num is {}. Corresponds to time {} s'.format(frameNum, frameNum/framerate))
                i+=1
                break

            # Mask the image
            # maskedImage = cv2.bitwise_and(frame, frame, mask=imgMask)
            # cv2.imwrite('./tempFolder/vid_{}.jpg'.format(frameNum), maskedImage)
            
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
