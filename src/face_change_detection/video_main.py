"""
programme principale
"""

import cv2
import time
import imutils
from imutils.video import VideoStream
from landmark import landmarks

print("[INFO] chargement du predicteur des points de saillances...")
# lmk = LM(args["shape_predictor"])
lmk = landmarks()

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] preparation de la camera...")
vs = VideoStream().start()
time.sleep(2.0)

seuil=10
print("[INFO] En cours d'execution...")
while(True):
    # récupération d'une image du flux video, la redimensionner
    # pour avoir une largeur de 400 pixels, la convertir en
    # grayscale, et y appliquer une égalisation d'histogramme.
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # car = caracterestique(frame.shape)

    face, _ = lmk.extract_landmarks(gray)

    # déssiner les points de saillances
    for pt in face.values():
        for (x, y) in pt:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    # if(vect!={}):
    #     print(" la distence =",car.distence(vect))
    #     difx, dify, dis=car.mov(vect)
    #     if (difx > seuil):
    #         print("move gauche")
    #     if (difx < -seuil):
    #         print("move droite")
    #     if (dify < -seuil):
    #         print("move bas")
    #     if (dify > seuil):
    #         print("move haut")
    #     print("ouverture de bouche", car.overture_bouche(vect))

    # affichage de l'image
    cv2.imshow('BeCHa', frame)

    # Attendre la touche q pour sortir
    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

print("[INFO] Sortir du programme...")

# cleaning up
cv2.destroyAllWindows()
vs.stop()
