import time
from collections import OrderedDict

from matplotlib.font_manager import FontProperties
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

    def __init__(self, _n=9, _f=8):
        """
        constructeur par default
        """
        super(drawer, self).__init__()

        # params
        self.n = _n
        self.f = _f

        # preparing figures
        # self.main_fig, self.ax = plt.subplots(figsize=(5, 4))
        self.dim_fig, self.dim_ax = plt.subplots(self.f, 1, True)

        # initialization
        self.sc = StandardScaler()
        self.pca = PCA(n_components=2)
        self.queue = None
        self.file = None
        self.last = None

        # plotting data
        self.neurones = np.array([]).reshape((-1, self.n, self.f))
        self.inputs = np.array([[]]).reshape((-1, self.f))
        self.targets = np.array([])

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

        def main_animation(i):
            mat = self.get_data()
            return self.plot_matrix(mat["data"], mat["target"])  # self.plot_matrix(self.data, "r", mark="x")

        def dim_animation(i):
            mat = self.get_data()

            fontP = FontProperties()
            fontP.set_size('small')
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            self.dim_ax[-1].legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.01, 5), loc=2, borderaxespad=0.)

            return self.plot_dimensions(mat["data"][:self.n], mat["target"])

        # ani = animation.FuncAnimation(self.main_fig, main_animation, frames=None, blit=True, interval=30, repeat=False)
        ani2 = animation.FuncAnimation(self.dim_fig, dim_animation, frames=None, blit=True, interval=30, repeat=False)
        plt.show()

    def plot_dimensions(self, neurones, target):
        """
        dessinateur des neurones
        :param t: le temps
        :param neurones: la matrice des neurones
        """

        # adding current data to datasets
        self.neurones = np.append(self.neurones, neurones.reshape((-1, self.n, self.f)), 0)
        self.targets = np.append(self.targets, target)

        plots = np.array([])
        for n in range(self.n):
            for i in range(self.f):
                plots = np.append(plots, self.dim_ax[i].plot(range(self.neurones.shape[0]), self.neurones[:, n, i], "C{}".format(n), label="N{}".format(n)))

        return tuple(plots)

    def plot_matrix(self, mat, target):
        """
        dessinateur des neurones
        :param mat: matrice des donnee (codebook et data)
        """

        mat = self.convert2d(mat)
        plots = self.anotations(mat[:self.n])
        plots = np.append(plots, self.links(mat[:self.n]))
        plots = np.append(plots, self.ax.scatter(mat[:self.n, 0], mat[:self.n, 1], c="b", label="clusters", marker="o"))
        plots = np.append(plots,
                          self.ax.scatter(mat[target, 0], mat[target, 1], c=("r", "b")[target == -1], label="target",
                                          marker="o"))
        plots = np.append(plots, self.ax.scatter(mat[self.n, 0], mat[self.n, 1], c="r", label="data", marker="x"))

        return tuple(plots)

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
