class affichage :
    def __init__(self):
     self.col = [[255, 0, 0],[0, 0, 255],[0, 255, 0],[255, 255, 0], [0, 255, 255],[255, 0, 255]]

    def aff(self,img,vects):

        for i in range(len(vects)):
            cnt=0
            c=self.col[i]
            while(vects[i]*50>cnt):
                for j in range(8):
                  img[50-cnt,10+i*8+j]=c
                cnt=cnt+1

        return img
