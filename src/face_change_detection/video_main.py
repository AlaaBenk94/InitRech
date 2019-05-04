"""
programme principale
"""

import pickle as pk
import time as t

import cv2
import imutils
import numpy as np

from caracterestique.caracterestique import caracterestique
from clasifieur.network import DSOM_MODEL
from draw.drawer import drawer
from landmark import landmarks


def update_display(frame, face, cluster):
    """
    dessiner les points de saillances, le cadre du visage et le cluster
    :param frame: l'image
    :param face: les points de saillances
    :param cluster: le resultat de clustering
    :return: l'image modifie
    """
    for k, pt in face.items():
        if k == "facepos":
            [(x1, y1, x2, y2)] = pt
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255))
            cv2.rectangle(frame, (x1, y1), (x1 + 100, y1 - 18), (0, 0, 255), -1)
            cv2.putText(frame, "Cluster #{}".format(cluster), (x1, y1 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                        (255, 255, 255), 1)
            continue
        for (x, y) in pt:
            cv2.circle(frame, (x, y), 1, landmarks.COLORS[k], -1)

    return frame


def send_ploting_data(codebook, vect, FCount, dist, pause=False):
    """
    envoyer les donnees au processus du plotting
    :param net: codebook
    :param vect: la nouvelle donnee
    :param FCount: nombre des features
    """
    mat = {"data": np.concatenate((codebook.reshape((-1, FCount)), np.reshape(vect, (-1, FCount)))),
           "target": winner,
           "dist": dist,
           "pause": pause}
    with open(f, "wb") as plot_data:
        pk.dump(mat, plot_data)


if __name__ == '__main__':
    print("[INFO] chargement du predicteur des points de saillances...")
    lmk = landmarks()
    f = "/tmp/data.plt"
    dr = drawer.fromFile(f)

    print("[INFO] chargement d'extracteur des caracteristiques...")
    car = caracterestique()

    print("[INFO] chargement de classifieur...")
    N = 3  # order of net matrix
    FCount = 8  # number of features
    net = DSOM_MODEL((N, N, FCount), init_method='regular', elasticity=1.0)

    print("[INFO] preparation de la camera...")
    vs = cv2.VideoCapture(0)

    fps = vs.get(cv2.CAP_PROP_FPS)
    print("[INFO] FPS = {}".format(fps))

    print("[INFO] En cours d'execution...")
    vect = np.zeros((1, FCount))
    vcc = np.zeros((1, FCount))
    winner = -1
    win_dist = 0
    pred = None # le frame (l'image) precedent
    i = 0 # compteur de frame
    delta = 5 # l'intervale entre les 2 frame a prendre
    coef = 10 # coefficient pour normaliser le vecteur d'entree
    minidisp = np.full((150, 400, 3), 200, np.uint8) # remplissage avant le debut de detection.
    started = False

    while True:
        start = int(round(t.time() * 1000))

        # recuperation d'une image du flux video, la redimensionner pour avoir une largeur de 400 pixels
        # ensuite la convertir l'image en grayscale et y appliquer une egalisation d'histogramme.
        _, frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # extraction des points de saillances
        ret, face, rect = lmk.extract_landmarks(gray)

        # on fait le traitement si au moins un visage est detecte
        if ret:
            vect = np.array(car.extract_features(face, frame.shape)[1])
            if i % delta == 0:
                if pred is None:
                    pred = vect
                    predimg = np.copy(frame)
                else:
                    vcc = caracterestique.calculate_vcc(pred, vect)
                    vcc = vcc*coef
                    winner, win_dist = net.cluster(vcc)
                    net.learn_data(vcc, lrate=5, sigma=1)
                    minidisp = imutils.resize(np.hstack((predimg, np.copy(frame))), width=400)
                    pred = None
                    predimg = None

            i = i + 1
            # print("VCC[{}] : {}".format(i, vcc))

            frame = update_display(frame, face, winner)
            send_ploting_data(net.codebook, vcc, FCount, win_dist)
            if not started:
                dr.start()
                started = True

        # dessiner le numero de frame
        end = (int(round(t.time() * 1000)) - start)
        cv2.putText(frame, "Process Time : {:.2f} ms".format(end), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)

        # affichage de l'image
        cv2.imshow('BeCHa', np.vstack((frame, minidisp)))

        # Attendre la touche 'q' pour sortir
        # ou la touche 'p' pour suspendre le programme
        key = cv2.waitKey(1)
        if key == 112:
            send_ploting_data(net.codebook, vcc, FCount, win_dist, True)
            while True:
                if cv2.waitKey(1) == 112:
                    break
            send_ploting_data(net.codebook, vcc, FCount, win_dist)
        if key == 113:
            break

    print("[INFO] Sortir du programme...")

    # killing the drawer process
    print("[INFO] terminaison du processus de plotting...")
    dr.terminate()

    # cleaning up
    cv2.destroyAllWindows()
    vs.release()
