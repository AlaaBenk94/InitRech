from math import sqrt
class distence:

    def cartesienne(self,vect1,vect2):
        dist=0.0
        for i in range(1,len(vect1)):
            dist=dist+(vect1[i]-vect2[i])*(vect1[i]-vect2[i])
        return sqrt(dist)
