import random

from Distence.distense import distence

class kmeans:
    def getKclass(self,base,K):
        kmoy=[]
        calcdis = distence()

        for i in range(K):
            elem=random.choice(base)

            while elem in kmoy:
                elem=random.choice(base)

            elem[0] = i
            kmoy.append(elem)


        stop=False

        while not stop :
          stop=True
          for i in base:
             kmin=kmoy[0]
             mindis=calcdis.cartesienne(kmin,i)
             for k in kmoy :
                 dis=calcdis.cartesienne(i,k)
                 if(dis<mindis):
                     mindis=dis
                     kmin=k
             if(i[0]!=kmin[0]):
              i[0]=kmin[0]
              stop=False

          for i in range(K):
              m=self.moyclasse(base, i)
              if m!=[]:
               kmoy[i]=m

    def moyclasse(self,base,y):
        moy=[]
        nby=0.0
        for elm in base :
            if elm[0] == y :
              if(moy==[]):
                  moy=elm.copy()
                  nby=1
              else:
                  for j in range(1,len(elm)):
                      moy[j]=moy[j]+elm[j]
                  nby=nby+1

        if nby==0 :
            return []
        else:
          for i in range(1,len(moy)):
            moy[i]=moy[i]/nby

          return moy