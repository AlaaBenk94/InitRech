"""
programme principale
"""

import time as t
from multiprocessing import Queue

import cv2
import imutils
from caracterestique.caracterestique import caracterestique
from clasifieur.network import DSOM_MODEL
from draw.drawer import drawer
from landmark import landmarks


if __name__ == '__main__':
	print("[INFO] chargement du predicteur des points de saillances...")
	lmk = landmarks()
	Q = Queue()
	dr = drawer(Q)
	dr.start()

	# instantiation du features extractor
	print("[INFO] chargement d'extracteur des caracteristiques...")
	car = caracterestique()

	print("[INFO] chargement de classifieur...")
	N = 3 # order of net matrix
	FCount = 8 # number of features
	net = DSOM_MODEL((N, N, FCount))

	# initialisation de flux video
	print("[INFO] preparation de la camera...")
	vs = cv2.VideoCapture(0)

	# recuperation du FPS de la camera
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
	    # gray = cv2.equalizeHist(gray)

	    # extraction des points de saillances
	    ret, face, rect = lmk.extract_landmarks(gray)

	    vect = []

	    # on fait le traitement si au moins un visage est detecte
	    if ret:
	        vect = car.extract_features(face, frame.shape)[1]
	        cluster = net.cluster(vect)
	        net.learn_data(vect)

	        # dessiner les points de saillances
	        for k, pt in face.items():
	            if k == "facepos":
	                [(x1, y1, x2, y2)] = pt
	                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255))
	                cv2.rectangle(frame, (x1, y1), (x1+100, y1-18), (0, 0, 255), -1)
	                cv2.putText(frame, "Cluster #{}".format(cluster), (x1, y1-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
	                continue
	            for (x, y) in pt:
	                cv2.circle(frame, (x, y), 1, landmarks.COLORS[k], -1)

	    # dessiner le numero de frame
	    end = (int(round(t.time() * 1000)) - start)
	    cv2.putText(frame, "Process Time : {:.2f} ms".format(end), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

	    # affichage de l'image
	    cv2.imshow('BeCHa', frame)

	    # print(net.codebook)
	    Q.put(net.codebook.reshape((N*N, FCount)))

	    if cv2.waitKey(1) & 0xFF == ord('p'):
	        while True:
	        	if cv2.waitKey(1) & 0xFF == ord('p'):
	        		break
	 
	    # Attendre la touche q pour sortir
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	print("[INFO] Sortir du programme...")

	dr.terminate()

	# cleaning up
	cv2.destroyAllWindows()
	vs.release()
