import time

from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt, animation
from sklearn.decomposition import PCA
from multiprocessing import Process
import pickle as pk
import numpy as np


class drawer(Process):
    """
    la class qui gere l'affichage des donnees et du model en temps reel
    """

    def __init__(self):
        """
        constructeur par default
        """
        super(drawer, self).__init__()
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.sc = StandardScaler()
        self.pca = PCA(n_components=2)
        self.queue = None
        self.file = None
        self.last = None

    @classmethod
    def fromQueue(cls, q):
        """
        initialisation
        :param q: la file des donnees
        """
        draw = drawer()
        draw.queue = q
        return draw

    @classmethod
    def fromFile(cls, file):
        """
        initialisation
        :param file: fichier des donnees
        """
        draw = drawer()
        draw.file = file
        return draw

    def run(self):
        """
        la tache principale du Processus
        a savoir : lancez une animation
        :return:
        """

        time.sleep(1)

        def animate(i):
            mat = self.get_data()
            return self.plot_matrix(mat["data"], mat["target"])  # self.plot_matrix(self.data, "r", mark="x")

        ani = animation.FuncAnimation(self.fig, animate, frames=None, blit=True, interval=30, repeat=False)
        plt.show()

    def plot_matrix(self, mat, target):
        """
        dessinateur des neurones
        :param mat: matrice des donnee (codebook et data)
        """

        mat = self.convert2d(mat)
        anots = self.anotations(mat[:9])
        anots = np.append(anots, self.links(mat[:9]))
        anots = np.append(anots, self.ax.scatter(mat[:9, 0], mat[:9, 1], c="b", label="clusters", marker="o"))
        anots = np.append(anots, self.ax.scatter(mat[target, 0], mat[target, 1], c=("r", "b")[target == -1], label="data", marker="o"))
        anots = np.append(anots, self.ax.scatter(mat[9, 0], mat[9, 1], c="r", label="data", marker="x"))

        return tuple(anots)

    def anotations(self, data):
        """
        annoter les points dessines
        :param data: les coordonnees des points a annoter
        :return: annotations
        """
        i = 0
        anots = np.array([])
        for x, y in data:
            anots = np.append(anots, plt.annotate(i, xy=(x, y)))
            i = i + 1

        return anots

    def links(self, data):
        """
        dissiner les lien entre les 9 neurones
        remarque : actuellement defini que pour 9 neurones
        :return: dessin des liens
        """

        target = (1, 2, 5, 8, 7, 6, 3, 0, 1, 4, 7, 8, 5, 4, 3)
        link = np.array([])
        link = np.append(link, self.ax.plot(data[target, 0], data[target, 1], 'b', linewidth=.5))
        return link

    def convert2d(self, data):
        """
        reduction des dimensions en utilisant l'acp
        :param data: donnees avec dimension n
        :return: les memes donnee en dimension 2
        """

        return self.pca.fit_transform(self.sc.fit_transform(data))

    def get_data(self):
        """
        recupere les donnees de plotting
        :return: les donnees
        """

        if self.queue is not None:
            return self.queue.get()

        try:
            with open(self.file, "rb") as plot_data:
                self.last = pk.load(plot_data)
                return self.last
        except:
            return self.last
