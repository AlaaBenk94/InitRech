import math

from normalisation.normalisation import normalisation
from Distence.distense import distence
from numpy.linalg import norm as dist
from numpy import around as rd


class caracterestique:

    def __init__(self, img_size=0):
        """
        constructeur
        :param img_size: taille de l'image
        """
        # self.surface=img_size[0]*img_size[1]
        self.pos_precd = None

    def distence(self, vecteur):
        facepos = vecteur['facepos']
        facesurface = (facepos[0][2] - facepos[0][0]) * (facepos[0][1] - facepos[0][3])
        return self.surface / facesurface

    def mov(self, vecteur):
        facepos = vecteur['facepos']
        dis = 0
        difx = 0
        dify = 0
        pos = (facepos[0][0] + (facepos[0][2] - facepos[0][0]) / 2
               , facepos[0][0] + (facepos[0][1] - facepos[0][3]) / 2)
        if (self.pos_precd != None):
            difx = (self.pos_precd[0] - pos[0])
            dify = (self.pos_precd[1] - pos[1])
            dis = math.sqrt((difx * difx) + (dify * dify))

        self.pos_precd = pos

        return difx, dify, dis

    def overture_bouche(self, vecteur):
        d = distence()
        mouth = vecteur['mouth']
        disv = d.cartesienne(mouth[0], mouth[6])
        dish = d.cartesienne(mouth[3], mouth[9])
        dis = (disv + 1) / (dish + 1)
        return dis

    def sourcils(self, vector):
        """
        extraire la distance entre les points de sourcils et le les yeux
        :param vector: points de saillances
        :return: tuple des distances (droite, gauche)
        """

        vector[""]

        return ()

    def h_rotation(self, vector):
        """
        extraire le taux de rotation du visage
        :param vector:  points de saillances
        :return: valeurs de rotation (positive -> rotation droite, negative -> rotation gauche)
        """

        # calculer les distances entre le coté droite/gauche du menton et le nez
        nose = vector["nose_bridge"].mean(0)
        rt = dist(vector["chin"][13:17].mean(0) - nose)
        lt = dist(vector["chin"][0:4].mean(0) - nose)

        return (rt / lt, -lt / rt)[rt > lt]

    def eyes(self, vector):
        """
        extraire le taux d'ouverture des yeux
        :param vector: points de saillances
        :return: tuple d'ouveture des yeux (droite, gauche)
        """

        # recupération des points des yeux
        lt = vector["right_eye"]
        rt = vector["left_eye"]

        return (rd(dist(rt[1:3].mean(0) - rt[4:6].mean(0)) / dist(rt[3] - rt[0]), 2),
                rd(dist(lt[1:3].mean(0) - lt[4:6].mean(0)) / dist(lt[3] - lt[0]), 2))

    def extract_features(self):
        """
        récuperer tous les caracteristiques du visage
        :return: dictionnaire des caracteristiques
        """

        return {}
