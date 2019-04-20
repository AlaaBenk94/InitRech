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

    def run(self):
        """
        la tache principale du Processus
        a savoir : lancez une animation
        :return:
        """

        def animate(i):
            mat = self.queue.get()
            return self.plot_matrix(mat["codebook"], "b"), self.plot_matrix(mat["data"], "r")

        ani = animation.FuncAnimation(self.fig, animate, frames=100, blit=True, interval=20, repeat=True)
        plt.show()



    def plot_matrix(self, mat, col):
        """
        dessinateur des neurones
        :param mat: matrice des donnee (codebook ou data)
        """

        if not np.all(mat[0]):
            return self.ax.scatter(0, 0, c=col, alpha=0.6, label="clusters", marker="x")
        mat = self.convert2d(mat)
        return self.ax.scatter(mat[:, 0], mat[:, 1], c=col, alpha=0.6, label="clusters")

    def convert2d(self, data):
        """
        reduction des dimensions en utilisant l'acp
        :param data: donnees avec dimension n
        :return: les memes donnee en dimension 2
        """

        return self.pca.fit_transform(self.sc.fit_transform(data))
