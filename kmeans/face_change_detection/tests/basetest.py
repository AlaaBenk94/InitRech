import random

from base import *

b=base()
b.ajouter([[random.randint(0,10),random.uniform(0,1),random.uniform(0,1)]])
vects=b.getbase()
print(vects)