# USAGE
# python image_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --image myimg.jpg

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
	help="the image you want to process")
args = vars(ap.parse_args())
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the image in grayscale mode and resize it to
# have a maximum width of 400 pixels, and convert it to
print("[INFO] Loading the image..")
frame = cv2.imread(args["image"], cv2.IMREAD_UNCHANGED)
frame = imutils.resize(frame, width=400)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale frame
rects = detector(gray, 0)

# loop over the face detections
for rect in rects:
	# determine the facial landmarks for the face region, then
	# convert the facial landmark (x, y)-coordinates to a NumPy
	# array
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)

	# loop over the (x, y)-coordinates for the facial landmarks
	# and draw them on the image
	for (x, y) in shape:
		cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

# show the frame
cv2.imshow("Frame", frame)

# if the `q` key was pressed, exit
if cv2.waitKey(0) & 0xFF == ord("q") :
	exit()