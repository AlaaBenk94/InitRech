# USAGE
# python main.py --predictor haarcascade_frontalface_default.xml
# python main.py --predictor haarcascade_frontalface_default.xml --camera 0

from imutils import face_utils
import dlib
import cv2
import argparse
import numpy as np 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--predictor", required=True,
	help="path to facial detector")
ap.add_argument("-r", "--camera", type=int, default=0,
	help="choosing the camera that should be used")
args = vars(ap.parse_args())

# initializing the camera
cap = cv2.VideoCapture(args["camera"])

while True:
	_, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	'''cv2.imshow('frame', frame)'''

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	cv2.namedWindow('color',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('color', 600,400 )
	cv2.imshow('color', img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()