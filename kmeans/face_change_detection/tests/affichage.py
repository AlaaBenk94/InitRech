import matplotlib.pyplot as plt
from matplotlib import gridspec

gs = gridspec.GridSpec(3,1)
plt.figure(facecolor='#008080',figsize=(50,50))
plt.subplots_adjust(
    bottom =0.05,top = 0.95,
    left  = 0.05 ,right = 0.95,
    wspace = 0.2,hspace = 0.3)

plt.ion()
colclass=['red', 'green', 'blue','yellow','violet','grey','orange']
colline=[]


def affichepoint(x,y,col):
    plt.scatter(x, y, c=col, s=100.0)

def affichepetitpoin(x,y,col):
    plt.scatter(x, y, c=col, s=10.0)

def affichepetitpbase(base):
    for i in base:
       col=colclass[i[0]]
       affichepetitpoin(i[1],i[2],col)

def affichebase(base):
    for i in base:
       col=colclass[i[0]]
       affichepoint(i[1],i[2],col)

def afficheline(x,y):
    plt.plot(x,y, color='blue', linestyle='-', linewidth=2)

def finaffichage():
    plt.show()

def update(s):
        plt.draw()
        plt.pause(s)
        plt.clf()