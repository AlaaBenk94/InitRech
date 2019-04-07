import random
from clasifieur import *
from tests.affichage import*

def col(m, i):
    return [c[i] for c in m]

base=[]
a=random.uniform(-2,2)
b=random.uniform(-2,2)

for i in range(10):
    y=(i*a+random.uniform(-0.5,0.5))+b+random.uniform(-0.5,0.5)
    base.append([0,i,y])

reg=regression()
a,b=reg.getparam(col(base,1),col(base,2))

x1=range(0,10)
y1=[]
for i in x1:
    y1.append(a*i+b)

afficheline(x1,y1)
affichebase(base)
finaffichage()