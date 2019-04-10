"""
programme principale
"""

import cv2
import dlib
import imutils
from imutils.video import VideoStream, FPS
from caracterestique.caracterestique import caracterestique
from landmark import landmarks
import time as t

print("[INFO] chargement du predicteur des points de saillances...")
# lmk = LM(args["shape_predictor"])
lmk = landmarks()

# instantiation du features extractor
car = caracterestique()

# initialisation de flux video
print("[INFO] preparation de la camera...")
vs = cv2.VideoCapture(0)
seuil = 10

# recupération du FPS de la camera
fps = vs.get(cv2.CAP_PROP_FPS)
print("[INFO] FPS = {}".format(fps))

print("[INFO] En cours d'execution...")
while True:
    start = int(round(t.time() * 1000))

    # recuperation d'une image du flux video,
    _, frame = vs.read()

    # redimensionner l'image pour avoir une largeur de 400 pixels
    frame = imutils.resize(frame, width=400)

    # convertir l'image en grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # appliquer une egalisation d'histogramme.
    gray = cv2.equalizeHist(gray)

    # extraction des points de saillances
    ret, face, rect = lmk.extract_landmarks(gray)

    # on fait le traitement si au moins un visage est detecte
    if ret:
        # print(car.extract_features(face, frame.shape, rect))
        # dessiner les points de saillances
        for k, pt in face.items():
            i = 0
            for (x, y) in pt:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), lineType=cv2.LINE_AA)
                i += 1

    # affichage de l'image
    cv2.imshow('BeCHa', frame)

    # le temps de traitement d'une image
    end = int(round(t.time() * 1000))
    # print("TIME : {}".format(end - start))

    # Attendre la touche q pour sortir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("[INFO] Sortir du programme...")

# cleaning up
cv2.destroyAllWindows()
vs.release()
