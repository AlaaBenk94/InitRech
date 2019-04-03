class normalisation:
    def __init__(self):
        return None

    def moynormalise(self,vecteur):
        moy=0.0
        for elem in vecteur:
            moy+=elem

        res=[]
        for elem in vecteur:
            res.append(elem/moy)

        return res

    def maxnormalise(self, vecteur):
        maxi=max(vecteur)
        res=[]
        for elem in vecteur:
            res.append(elem/maxi)

        return res