import cv2
import time

import numpy as np

from detection_point import *
from caracterestique import *
from clasifieur import *

cap = cv2.VideoCapture(0)
ret, img = cap.read()
imgsize=img.shape
fdet= facedetection()
car=caracterestique(imgsize)
seuil=10
while(True):
    ret, img = cap.read()
    imgdet=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgdeteg=cv2.equalizeHist(imgdet)
    #imgdet = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #kernel = np.ones((12, 12), np.float32) / 144
    #imgdeteg = cv2.filter2D(imgdet, -1, kernel)


    #vect,imgdet = fdet.get_vecteur(imgdet)
    vect,imgdeteg=fdet.get_vecteur(imgdeteg)

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
        print("ouverture de bouche",car.overture_bouche(vect))

    #cv2.imshow('',imgdet)
    cv2.imshow('eg',imgdeteg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

cap.release()
cv2.destroyAllWindows()