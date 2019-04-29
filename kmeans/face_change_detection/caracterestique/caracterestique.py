from normalisation.normalisation import normalisation
from Distence.distense import distence
from numpy import around as rd
import math


class caracterestique :
    def __init__(self,img_size):
     self.surface=img_size[0]*img_size[1];
     self.pos_precd=None;

    def moy(self,v):
        m=[0]*len(v[0])
        for i in v:
            for j in range(len(i)):
             m[j]=m[j]+i[j]

        for i in range(len(m)):
            m[i]=m[i]/len(v)
        return m

    def distence(self,vecteur):
        facepos=vecteur['facepos']
        facesurface=(facepos[0][2]-facepos[0][0])*(facepos[0][1]-facepos[0][3])
        n=normalisation()
        return n.val01(self.surface/(float(facesurface)*5))

    def mov(self,vecteur):
        facepos = vecteur['facepos']
        dis=0
        difx=0
        dify=0
        pos=(facepos[0][0] + (facepos[0][2] - facepos[0][0]) / 2
         , facepos[0][0] + (facepos[0][1] - facepos[0][3]) / 2)
        if(self.pos_precd!=None):
            difx = (self.pos_precd[0] - pos[0])
            dify = (self.pos_precd[1] - pos[1])
            dis=math.sqrt((difx*difx)+(dify*dify))

        self.pos_precd=pos
        n=normalisation()
        return n.val01(difx),n.val01(dify),n.val01(dis/10)

    def overture_bouche(self,vecteur):
        d=distence()
        eyel = vecteur['left_eye']
        eyer = vecteur['right_eye']
        facetl = vecteur['top_lip']
        facebl = vecteur['bottom_lip']
        disv=d.cartesienne(facebl[3],facetl[3])
        disv2=d.cartesienne(facebl[9],facetl[9])
        if(disv2==0 or disv==0):return 0
        diseyes=d.cartesienne(eyel[3],eyer[0])
        dis=(disv*disv2+0.000001)/(diseyes*100+0.000001) #(dish+1)
        n=normalisation()
        return n.val01(dis)

    '''
    def sourir(self,vecteur):
        d=distence()
        facetl = vecteur['top_lip']
        facebl = vecteur['bottom_lip']
        sommedx=0
        for i in range(6):
            sommedx=sommedx+(facebl[i][0]-facebl[i+1][0])*(facebl[i][0]-facebl[i+1][0])
            sommedx=sommedx+(facetl[i][0]-facetl[i+1][0])*(facetl[i][0]-facetl[i+1][0])
        sommedx=sommedx/12
        eyel = vecteur['left_eye']
        eyer = vecteur['right_eye']
        diseyes = d.cartesienne(eyel[3], eyer[0])
        print("/////////////",sommedx ,diseyes)
        dis=sommedx/(diseyes*20)

        n=normalisation()
        return n.val01(dis)
        
    '''


    def h_rotation(self, vector):
        d = distence()
        """
        extraire le taux de rotation du visage
        valeur positive -> rotation droite,
        valeur negative -> rotation gauche
        :param vector:  points de saillances
        :return: valeurs de rotation
        """

        # calculer les distances entre le cote droite/gauche du menton et le nez
        nose = vector["nose_bridge"][0]
        rt = d.cartesienne(vector["chin"][16] , nose)
        lt = d.cartesienne(vector["chin"][0], nose)
        if(rt==0 or lt==0):
            return 0,0
        n=normalisation()
        return n.val01((rt+0.00001)/(lt+0.00001)),n.val01((lt+0.00001)/(rt+0.00001))


    def eyes(self, vector):
        d = distence()
        """
        extraire le taux d'ouverture des yeux
        :param vector: points de saillances
        :return: tuple d'ouveture des yeux (droite, gauche)
        """

        # recuperation des points des yeux
        lt = vector["right_eye"]
        rt = vector["left_eye"]
        div=d.cartesienne(rt[3] , rt[0])
        n=normalisation()
        if(div==0):
            return 0,0
        return (
                n.val01(rd(d.cartesienne(self.moy(rt[1:3]) , self.moy(rt[4:6])) / div)),
                n.val01(rd(d.cartesienne(self.moy(lt[1:3]) , self.moy(lt[4:6])) / div))
        )

