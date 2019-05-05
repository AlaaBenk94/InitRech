import pickle as pk
import time
from collections import OrderedDict
from multiprocessing import Process

import numpy as np
from matplotlib import pyplot as plt, animation
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class drawer(Process):
    """
    la class qui gere l'affichage des donnees et du model en temps reel
    """

    def __init__(self, _n, _f, n_first, _speed, _disp):
        """
        constructeur par default
        """
        super(drawer, self).__init__()

        # params
        self.n = _n  # nombre de clusters
        self.f = _f  # dimension des entrees
        self.n_first = n_first  # plage de plotting
        self.speed = _speed  # vitesse de plotting
        self.paused = False  # state of plotting process
        self.disp = _disp # les figures a afficher

        # preparing figures
        # self.main_fig, self.ax = plt.subplots(figsize=(5, 4), num='Main Plot')
        # self.dim_fig, self.dim_ax = plt.subplots(self.f, 1, True, num='Neurones Dimensions')
        # self.hist_fig, self.hist_ax = plt.subplots(3, 1, num='Histogram Distances Inputs')

        self.main_fig, self.ax = None, None
        self.dim_fig, self.dim_ax = None, None
        self.hist_fig, self.hist_ax = None, None

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
        self.dists = np.array([])
        self.hist = [0] * self.n

    @classmethod
    def fromQueue(cls, q, _n=9, _f=8, n_first=20, _speed=30, _disp="001"):
        """
        initialisation
        :param q: la file des donnees
        :param _n: nombre de clusters
        :param _f: dimension des entrees
        :param n_first: plage de plotting
        :param _speed: vitesse de plotting
        :param _disp: les figures a afficher
        """
        draw = drawer(_n, _f, n_first, _speed, _disp)
        draw.queue = q
        return draw

    @classmethod
    def fromFile(cls, file, _n=9, _f=8, n_first=20, _speed=30, _disp="001"):
        """
        initialisation
        :param file: fichier des donnees
        :param _n: nombre de clusters
        :param _f: dimension des entrees
        :param n_first: plage de plotting
        :param _speed: vitesse de plotting
        :param _disp: les figures a afficher
        """
        draw = drawer(_n, _f, n_first, _speed, _disp)
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
            self.paused = mat["pause"]
            return self.plot_matrix(mat["data"], mat["target"])  # self.plot_matrix(self.data, "r", mark="x")

        def dim_animation(i):
            mat = self.get_data()
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            self.dim_ax[-1].legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.01, 5), loc=2,
                                   borderaxespad=0.)
            self.paused = mat["pause"]
            return self.plot_dimensions(mat["data"][:self.n], mat["target"])

        def hist_animation(i):
            mat = self.get_data()
            self.paused = mat["pause"]
            return self.plot_histogram(mat["data"][-1], mat["dist"], mat["target"])

        if self.disp[0] == "1":
            self.main_fig, self.ax = plt.subplots(figsize=(5, 4), num='Main Plot')
            main_ani = animation.FuncAnimation(self.main_fig, main_animation, frames=None, blit=True, interval=self.speed, repeat=False)
        if self.disp[1] == "1":
            self.dim_fig, self.dim_ax = plt.subplots(self.f, 1, True, num='Neurones Dimensions')
            dim_ani = animation.FuncAnimation(self.dim_fig, dim_animation, frames=None, blit=True, interval=self.speed, repeat=False)
        if self.disp[2] == "1":
            self.hist_fig, self.hist_ax = plt.subplots(3, 1, num='Histogram Distances Inputs')
            hist_ani = animation.FuncAnimation(self.hist_fig, hist_animation, frames=None, blit=True, interval=self.speed, repeat=False)

        plt.show()

    def plot_histogram(self, input, dist, target):
        """
        dessinateur d'histogramme
        :param input: vecteur d'entree
        :param dist: la distance entre l'entree et le gangant
        :param target: l'indice du gagnant
        """

        # adding current data to datasets
        if not self.paused:
            self.inputs = np.append(self.inputs, input.reshape(-1, self.f), 0)
            self.dists = np.append(self.dists, dist)
            self.targets = np.append(self.targets, target)
            if target != -1:
                self.hist[target] = self.hist[target] + 1

        # checking range
        if self.inputs.shape[0] > self.n_first:
            self.inputs = np.delete(self.inputs, 0, 0)
            self.dists = np.delete(self.dists, 0)
            self.targets = np.delete(self.targets, 0, 0)

        # plotting winners
        plots = np.array([])
        plots = np.append(plots, self.hist_ax[0].vlines(range(self.targets.shape[0]), -2, 2,
                                                        ["C{}".format(i) for i in self.targets.astype('int32')],
                                                        alpha=0.8))
        plots = np.append(plots, self.hist_ax[1].vlines(range(self.targets.shape[0]), 0, np.max(self.dists, initial=20),
                                                        ["C{}".format(i) for i in self.targets.astype('int32')],
                                                        alpha=0.8))

        # plotting inputs
        for i in range(self.f):
            plots = np.append(plots,
                              self.hist_ax[0].plot(range(self.inputs.shape[0]), self.inputs[:, i], "C{}".format(i)))

        # plotting distances
        plots = np.append(plots, self.hist_ax[1].plot(range(self.dists.shape[0]), self.dists, "C0"))

        # plotting histogram
        plots = np.append(plots,
                          self.hist_ax[2].bar(range(self.n), self.hist, color=["C{}".format(c) for c in range(self.n)]))

        return tuple(plots)

    def plot_dimensions(self, neurones, target):
        """
        dessinateur des neurones
        :param t: le temps
        :param neurones: la matrice des neurones
        """

        # adding current data to datasets
        self.neurones = np.append(self.neurones, neurones.reshape((-1, self.n, self.f)), 0)
        self.targets = np.append(self.targets, target)

        # checking range
        if self.targets.shape[0] > self.n_first:
            self.neurones = np.delete(self.neurones, 0, 0)
            self.targets = np.delete(self.targets, 0, 0)

        # plotting winners
        plots = np.array([])
        for i in range(self.f):
            plots = np.append(plots, self.dim_ax[i].vlines(range(self.neurones.shape[0]), -2, 2,
                                                           ["C{}".format(i) for i in self.targets.astype('int32')],
                                                           alpha=0.3))
        # plotting neurones dimensions
        for n in range(self.n):
            for i in range(self.f):
                plots = np.append(plots, self.dim_ax[i].plot(range(self.neurones.shape[0]), self.neurones[:, n, i],
                                                             "C{}".format(n), label="N{}".format(n)))

        return tuple(plots)

    def plot_matrix(self, mat, target):
        """
        dessinateur des neurones
        :param mat: matrice des donnee (codebook et data)
        """

        # dimension reduction using PCA
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
