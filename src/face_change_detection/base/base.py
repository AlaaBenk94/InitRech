import os
from array import array


class base :
 def __init__(self):
    if not ("vecteur.txt" in os.listdir(os.getcwd())):
        a = open("vecteur.txt", 'w')
        a.close()

 def getbase(self):
     base = []
     if "vecteur.txt" in os.listdir(os.getcwd()):
         f = []
         fich = open("vecteur.txt", 'r')
         vect = fich.read().split(",")
         if (len(vect) > 0 and vect[0] != ""):
             vect.pop()
             for i in vect:
                 e = i.split(" ")
                 e.pop()
                 f.append(e)
             for i in f:
                 for j in range(len(i)):
                     i[j] = float(i[j])
                 base.append(i)
         fich.close()
     return base

 def ajouter(self,vecteurs):
      a = open("vecteur.txt", 'a')
      for elm in vecteurs:
           s=""
           for k in elm :
             s=s+str(k)+" "
           s=s+","
           a.write(s)
      a.close()