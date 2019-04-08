import random
from clasifieur import *

from tests.affichage import *

base=[]
for i in range(1000):
    base.append([0, random.uniform(0,100), random.uniform(0,100)])

c=kmeans()
c.getKclass(base,7)

affichebase(base)
finaffichage()