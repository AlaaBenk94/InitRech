"""
programme principale
"""

import time as t
import cv2
import imutils
from caracterestique.caracterestique import caracterestique
from landmark import landmarks

print("[INFO SYS] chargement du predicteur des points de saillances...")
lmk = landmarks()

# instantiation du features extractor
print("[INFO SYS] chargement d'extracteur des caracteristiques...")
car = caracterestique()

# initialisation de flux video
print("[INFO SYS] preparation de la camera...")
vs = cv2.VideoCapture(0)

# recuperation du FPS de la camera
fps = vs.get(cv2.CAP_PROP_FPS)
print("[INFO] FPS = {}".format(fps))

print("[INFO SYS] En cours d'execution...")
while True:
    start = int(round(t.time() * 1000))

    # recuperation d'une image du flux video,
    _, frame = vs.read()

    # redimensionner l'image pour avoir une largeur de 400 pixels
    frame = imutils.resize(frame, width=400)

    # convertir l'image en grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # appliquer une egalisation d'histogramme.
    # gray = cv2.equalizeHist(gray)

    # extraction des points de saillances
    ret, face, rect = lmk.extract_landmarks(gray)

    # on fait le traitement si au moins un visage est detecte
    if ret:
        caracterestique.print_features(car.extract_features(face, frame.shape, rect))
        # dessiner les points de saillances
        for k, pt in face.items():
            if k == "facepos":
                [(x1, y1, x2, y2)] = pt
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255))
                continue
            for (x, y) in pt:
                cv2.circle(frame, (x, y), 1, landmarks.COLORS[k], -1)

    # dissiner le numero de frame
    end = (int(round(t.time() * 1000)) - start)
    cv2.putText(frame, "Process Time : {:.2f} ms".format(end), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # affichage de l'image
    cv2.imshow('BeCHa', frame)

    # Attendre la touche q pour sortir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("[INFO SYS] Sortir du programme...")

# cleaning up
cv2.destroyAllWindows()
vs.release()