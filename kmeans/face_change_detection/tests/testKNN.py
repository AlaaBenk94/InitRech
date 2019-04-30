import random
from clasifieur import*

from tests.affichage import*

base=[]
for i in range(200):
    base.append([0, random.uniform(0,10), random.uniform(0,10)])

c=kmeans()
c.getKclass(base,7)

base2=[]
e=int(10/0.2)
for i in range(0,e):
    for j in range(0, e):
        base2.append([0,i*0.2,j*0.2])

predit=KNN()
for i in base2 :
  predit.prediction(i,base,6)

print( " affichage ")
affichepetitpbase(base2)
affichebase(base)
finaffichage()