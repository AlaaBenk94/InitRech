import matplotlib.pyplot as plt
from matplotlib import gridspec
gs = gridspec.GridSpec(3,1)
plt.figure(facecolor='#008080',figsize=(10,10))
plt.subplots_adjust(
    bottom =0.05,top = 0.95,
    left  = 0.05 ,right = 0.95,
    wspace = 0.2,hspace = 0.3)

colclass=['red', 'green', 'blue','yellow','violet','grey','orange']
colline=[]


def affichepoint(x,y,col):
    plt.scatter(x, y, c=col, s=100.0)

def affichebase(base):
    for i in base:
       col=colclass[i[0]]
       affichepoint(i[1],i[2],col)
    plt.show()
