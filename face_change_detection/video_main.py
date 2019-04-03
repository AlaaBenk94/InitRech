import cv2
import time

from face_change_detection.detection_point import *
from face_change_detection.caracterestique import *
from face_change_detection.clasifieur import *

cap = cv2.VideoCapture(0)
ret, img = cap.read()
imgsize=img.shape
fdet= facedetection()
car=caracterestique(imgsize)
seuil=10
while(True):
    ret, img = cap.read()
    vect,imgdet=fdet.get_vecteur(img)
    if(vect!={}):
        print(" la distence =",car.distence(vect))
        difx, dify, dis=car.mov(vect)
        if (difx > seuil):
            print("move gauche")
        if (difx < -seuil):
            print("move droite")
        if (dify < -seuil):
            print("move bas")
        if (dify > seuil):
            print("move haut")
    cv2.imshow('',imgdet)
    #time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

cap.release()
cv2.destroyAllWindows()