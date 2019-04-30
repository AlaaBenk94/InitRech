"""
programme principale
"""

import pickle as pk
import time as t

import cv2
import imutils
import numpy as np
from sklearn.cluster import KMeans

from caracterestique.caracterestique import caracterestique
from draw.drawer import drawer
from landmark import landmarks

f = "/tmp/data.plt"

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


def send_ploting_data(f, codebook, vect, cluster, FCount):
    """
    envoyer les donnees au processus du plotting
    :param net: codebook
    :param vect: la nouvelle donnee
    :param FCount: nombre des features
    """
    mat = {"data": np.concatenate((codebook.reshape((-1, FCount)), np.reshape(vect, (-1, FCount)))),
           "target": cluster}
    with open(f, "wb") as plot_data:
        pk.dump(mat, plot_data)
        plot_data.close()

def read_precessing(vs):
    """
    recuperation d'une image du flux video, la redimensionner pour avoir une largeur de 400 pixels
    ensuite la convertir l'image en grayscale et y appliquer une egalisation d'histogramme.
    :param vs: le flux video
    :return: l'image (RGB, Greyscale)
    """
    _, frm = vs.read()
    frm = imutils.resize(frm, width=400)
    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return frm, gray


if __name__ == '__main__':
    print("[INFO] chargement du predicteur des points de saillances...")
    lmk = landmarks()

    print("[INFO] chargement d'extracteur des caracteristiques...")
    car = caracterestique()

    print("[INFO] chargement de classifieur...")
    N = 3  # order of net matrix
    FCount = 8  # number of features
    kmeans = KMeans(n_clusters=N*N, random_state=0)


    print("[INFO] preparation de la camera...")
    vs = cv2.VideoCapture(0)


    fps = vs.get(cv2.CAP_PROP_FPS)
    print("[INFO] FPS = {}".format(fps))

    print("[INFO] En cours d'execution...")
    vect = [0, 0, 0, 0, 0, 0, 0, 0]
    cluster = -1

    print("[INFO] lancement de plotter")
    dr = drawer.fromFile(f)
    off = True

    base = np.array([])
    dbsize = 20
    while True:
        start = int(round(t.time() * 1000))

        frame, gray = read_precessing(vs)

        # extraction des points de saillances
        ret, face, rect = lmk.extract_landmarks(gray)

        # on fait le traitement si au moins un visage est detecte
        if ret:
            vect = np.array(car.extract_features(face, frame.shape)[1])
            vect = np.around(vect, 2)

            # batch learning
            if off and base.shape[0] < dbsize:
                base = np.append(base, vect)
                base = base.reshape((-1, FCount))
            else:
                if base.shape[0] % dbsize == 0:
                    kmeans = kmeans.fit(base)
                    base = np.array([])
                cluster = kmeans.predict(vect.reshape(-1, FCount))[0]
                print(cluster)
                base = np.append(base, vect)
                base = base.reshape((-1, FCount))
                send_ploting_data(f, kmeans.cluster_centers_, vect, cluster, FCount)
                print(kmeans.cluster_centers_)
                if off:
                    dr.start()
                    off = False

            frame = update_display(frame, face, cluster)

        if not off:
            send_ploting_data(f, kmeans.cluster_centers_, vect, cluster, FCount)

        # dessiner le numero de frame
        end = (int(round(t.time() * 1000)) - start)
        cv2.putText(frame, "Process Time : {:.2f} ms".format(end), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1)

        # affichage de l'image
        cv2.imshow('BeCHa', frame)

        # Attendre la touche 'q' pour sortir
        # ou la touche 'p' pour suspendre le programme
        key = cv2.waitKey(1)
        if key == 112:
            while True:
                if cv2.waitKey(1) == 112:
                    break
        if key == 113:
            break

    print("[INFO] Sortir du programme...")

    # killing the drawer process
    print("[INFO] terminaison du processus de plotting...")
    dr.terminate()

    # cleaning up
    cv2.destroyAllWindows()
    vs.release()
