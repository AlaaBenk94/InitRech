import math


class caracterestique :
    def __init__(self,img_size):
     self.surface=img_size[0]*img_size[1];
     self.pos_precd=None;

    def distence(self,vecteur):
        facepos=vecteur['facepos']
        facesurface=(facepos[0][2]-facepos[0][0])*(facepos[0][1]-facepos[0][3])
        return facesurface/self.surface

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


