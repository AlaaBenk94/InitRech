import math
from numpy import around as rd
from numpy.linalg import norm as dist
from Distence.distense import distence
from normalisation.normalisation import normalisation


class caracterestique:

    def __init__(self):
        self.pos_precd = None
        self.surface = 0

    def distence(self, img_size, facesurface):
        self.surface = img_size[0] * img_size[1]
        # facepos = vecteur['facepos']
        # facesurface = (facepos[0][2] - facepos[0][0]) * (facepos[0][1] - facepos[0][3])
        n = normalisation()
        return n.val01(self.surface / (float(facesurface) * 5))

    def mov(self, pos):
        # facepos = vecteur['facepos']
        dis = 0
        difx = 0
        dify = 0
        # pos = (facepos[0][0] + (facepos[0][2] - facepos[0][0]) / 2
        #        , facepos[0][0] + (facepos[0][1] - facepos[0][3]) / 2)
        if (self.pos_precd != None):
            difx = (self.pos_precd[0] - pos[0])
            dify = (self.pos_precd[1] - pos[1])
            dis = math.sqrt((difx * difx) + (dify * dify))

        self.pos_precd = pos
        n = normalisation()
        return n.val01(difx), n.val01(dify), n.val01(dis / 10)

    def overture_bouche(self, vecteur):
        d = distence()
        eyel = vecteur['left_eye']
        eyer = vecteur['right_eye']
        facetl = vecteur['top_lip']
        facebl = vecteur['bottom_lip']
        disv = d.cartesienne(facebl[3], facetl[3])
        disv2 = d.cartesienne(facebl[9], facetl[9])
        dis = (disv * disv2 + 0.000001) / (d.cartesienne(eyel[3], eyer[0]) * 100 + 0.000001)  # (dish+1)
        n = normalisation()
        return n.val01(dis)

    def sourcils(self, vector):
        """
        extraire la distance entre les points de sourcils et le les yeux
        :param vector: points de saillances
        :return: tuple des distances (gauche, groite)
        """

        # recuperer les points des yeux
        l_eye = vector["left_eye"]
        r_eye = vector["right_eye"]

        # recuperer les points des sourcils
        l_brow = vector["right_eyebrow"]
        r_brow = vector["left_eyebrow"]

        return (rd(dist(l_brow[2] - l_eye[1:3].mean(0)) / dist(l_brow[0] - l_brow[4]), 2),
                rd(dist(r_brow[2] - r_eye[1:3].mean(0)) / dist(r_brow[0] - r_brow[4]), 2))

    def h_rotation(self, vector):
        """
        extraire le taux de rotation du visage
        valeur positive -> rotation droite,
        valeur negative -> rotation gauche
        :param vector:  points de saillances
        :return: valeurs de rotation
        """

        # calculer les distances entre le cote droite/gauche du menton et le nez
        nose = vector["nose_bridge"].mean(0)
        rt = dist(vector["chin"][13:17].mean(0) - nose)
        lt = dist(vector["chin"][0:4].mean(0) - nose)

        return rd(((1 - (rt / lt), -(1 - (lt / rt)))[rt > lt]), 2)

    def eyes(self, vector):
        """
        extraire le taux d'ouverture des yeux
        :param vector: points de saillances
        :return: tuple d'ouveture des yeux (gauche, droite)
        """

        # recuperation des points des yeux
        lt = vector["right_eye"]
        rt = vector["left_eye"]

        return (rd(dist(lt[1:3].mean(0) - lt[4:6].mean(0)) / dist(lt[3] - lt[0]), 2),
                rd(dist(rt[1:3].mean(0) - rt[4:6].mean(0)) / dist(rt[3] - rt[0]), 2))

    def extract_features(self, vect, imgsize, rect):
        """
        recuperer tous les caracteristiques du visage
        :return: dictionnaire des caracteristiques
        """

        return {"eyes": self.eyes(vect),
                "rotation": self.h_rotation(vect),
                "eyebrows": self.sourcils(vect),
                "bouche": self.overture_bouche(vect),
                "distance": self.distence(imgsize, rect.area()),
                "move": self.mov((rect.center().x, rect.center().y))}
