import cv2
import time

import numpy as np

from detection_point import *
from caracterestique import *
import affichage_car

cap = cv2.VideoCapture(0)
ret, img = cap.read()
imgsize=img.shape
fdet= facedetection()
car=caracterestique(imgsize)
seuil=10
aff= affichage_car.affichage()
while(True):
    ret, img = cap.read()
    #imgdet=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #imgdeteg=cv2.equalizeHist(img)
    vect,imgdeteg=fdet.get_vecteur(img)

    if(vect!={}):
        zdis=car.distence(vect)
        print(" la distence =",zdis)
        difx, dify, dis=car.mov(vect)
        if (difx > seuil):
            print("move gauche")
        if (difx < -seuil):
            print("move droite")
        if (dify < -seuil):
            print("move bas")
        if (dify > seuil):
            print("move haut")
        o=car.overture_bouche(vect)
        print("ouverture de bouche",o)
        #s=car.sourir(vect)
        #print("sourir",s)
        rot=car.h_rotation(vect)
        eyesopen=car.eyes(vect)
        print("rot",rot)
        #print("eye",eyesopen[0])
        imgdeteg = aff.aff(imgdeteg,[o,zdis,dis,rot[0],rot[1]])
    #cv2.imshow('',imgdet)


    cv2.imshow('eg',imgdeteg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

cap.release()
cv2.destroyAllWindows()