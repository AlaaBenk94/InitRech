class regression:

 def moy(self,X):
     moyx = 0.0
     for i in X:
         moyx = moyx + i
     return moyx/float(len(X))

 def var(self,X):
     moy=self.moy(X)
     variance=0.0
     for i in X :
         variance=variance+(i-moy)*(i-moy)
     return  variance/float(len(X))

 def cov(self,X,Y):
     covariance=0.0
     moyx=self.moy(X)
     moyy=self.moy(Y)
     for i in range(len(X)):
         covariance=covariance+(X[i]-moyx)*(Y[i]-moyy)
     return covariance/float(len(X))

 def getparam(self,X,Y):
     a=self.cov(X,Y)/self.var(X)
     b=self.moy(Y)-a*self.moy(X)
     return a,b
