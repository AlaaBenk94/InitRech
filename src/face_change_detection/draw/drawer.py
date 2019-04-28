from multiprocessing import Process

import cv2
from matplotlib import pyplot as plt, animation
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np


class drawer(Process):
    """
    la class qui gere l'affichage des donnees et du model en temps reel
    """

    def __init__(self, q=None):
        """
        initialisation
        :param q: la file des donnees
        """
        super(drawer, self).__init__()
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.queue = q
        self.sc = StandardScaler()
        self.pca = PCA(n_components=2)
        self.data = None

    def run(self):
        """
        la tache principale du Processus
        a savoir : lancez une animation
        :return:
        """

        def animate(i):
            mat = self.queue.get()
            return self.plot_matrix(mat["codebook"], "b") #self.plot_matrix(self.data, "r", mark="x")

        ani = animation.FuncAnimation(self.fig, animate, frames=None, blit=True, interval=40, repeat=False)
        plt.show()



    def plot_matrix(self, mat, col, mark="o"):
        """
        dessinateur des neurones
        :param mat: matrice des donnee (codebook ou data)
        """

        # if not np.all(mat[0]):
        #     return self.ax.scatter(0, 0, c=col, alpha=0.6, label="clusters", marker=mark)
        mat = self.convert2d(mat)
        anots = self.anotations(mat)
        anots = np.append(anots, self.links(mat))
        anots = np.append(anots, self.ax.scatter(mat[:, 0], mat[:, 1], c=col, alpha=0.6, label="clusters", marker=mark))

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
        dissiner les lien entre les neurones
        :return: dessin des liens
        """

        link = np.array([])
        link = np.append(link, plt.plot(data[:3, 0], data[:3, 1], color='b', linewidth=.5))
        link = np.append(link, plt.plot(data[3:6, 0], data[3:6, 1], color='b', linewidth=.5))
        link = np.append(link, plt.plot(data[6:, 0], data[6:, 1], color='b', linewidth=.5))
        link = np.append(link, plt.plot(data[(0, 3, 6), 0], data[(0, 3, 6), 1], color='b', linewidth=.5))
        link = np.append(link, plt.plot(data[(1, 4, 7), 0], data[(1, 4, 7), 1], color='b', linewidth=.5))
        link = np.append(link, plt.plot(data[(2, 5, 8), 0], data[(2, 5, 8), 1], color='b', linewidth=.5))

        return link

    def convert2d(self, data):
        """
        reduction des dimensions en utilisant l'acp
        :param data: donnees avec dimension n
        :return: les memes donnee en dimension 2
        """

        return self.pca.fit_transform(self.sc.fit_transform(data))
