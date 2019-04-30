import random

from Distence.distense import distence

class kmeans:

    def __init__(self):
        self.kmoy = []

    def getKclass(self,base,K):
        self.kmoy=[]

        for i in range(len(base)):
            base[i]=[0]+base[i]

        for i in range(K):
            elem=random.choice(base)

            while elem in self.kmoy:
                elem=random.choice(base)

            elem[0] = i
            self.kmoy.append(elem)


        stop=False

        while not stop :
          stop=True
          for i in base:
             kp=self.class_plus_proche(i)
             if(i[0]!=kp):
              i[0]=kp
              stop=False

          for i in range(K):
              m=self.moyclasse(base, i)
              if m!=[]:
               self.kmoy[i]=m

        self.nb=[0]*K
        for i in base:
            self.nb[i[0]]+=1
            i.pop(0)

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

    def class_plus_proche(self,i):
        calcdis = distence()
        kmin = self.kmoy[0]
        mindis = calcdis.cartesienne(kmin, i)
        for k in self.kmoy:
            dis = calcdis.cartesienne(i, k)
            if (dis < mindis):
                mindis = dis
                kmin = k
        return kmin[0]

    def raffiner(self,X):
        X=[0]+X
        k=self.class_plus_proche(X)
        self.kmoy[k]=[k]+[((self.kmoy[k][i]*self.nb[k])+X[i])/(self.nb[k]+1)for i in range(1,len(self.kmoy[k]))]
        self.nb[k]+=1
        X.pop(0)

    def prediction(self,x):
        return self.class_plus_proche([0]+x)