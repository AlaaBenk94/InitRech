import random
from clasifieur import *

from tests.affichage import *

c=kmeans()
base=[]
for i in range(10):
    base.append([random.uniform(0,100), random.uniform(0,100)])
c.getKclass(base,7)
for i in range(len(base)):
    base[i]=[c.prediction(base[i])]+base[i]
affichepetitpbase(base)
update(4)
for i in range(100):
    x=[random.uniform(0,100), random.uniform(0,100)]
    k=c.prediction(x)
    base.append([k]+x)
    affichepetitpbase(base)
    c.raffiner(x)
    affichebase(c.kmoy)
    update(0.000000000000000000000000001)
