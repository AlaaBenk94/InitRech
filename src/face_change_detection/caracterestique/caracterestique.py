import math

from normalisation.normalisation import normalisation
from Distence.distense import distence


class caracterestique :
    def __init__(self,img_size):
     self.surface=img_size[0]*img_size[1];
     self.pos_precd=None;

    def distence(self,vecteur):
        facepos=vecteur['facepos']
        facesurface=(facepos[0][2]-facepos[0][0])*(facepos[0][1]-facepos[0][3])
        return self.surface/facesurface

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

        return difx,dify,dis

    def overture_bouche(self,vecteur):
        d=distence()
        facetl = vecteur['top_lip']
        facebl = vecteur['bottom_lip']
        disv=d.cartesienne(facebl[5],facetl[5])
        dish=d.cartesienne(facebl[0],facetl[0])
        dis=(disv+1)/(dish+1)
        return dis
