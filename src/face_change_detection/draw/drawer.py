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
            return self.plot_matrix(mat),

        ani = animation.FuncAnimation(self.fig, animate, frames=100, blit=True, interval=20, repeat=True)
        plt.show()



    def plot_matrix(self, mat):
        mat = self.convert2d(mat)
        return self.ax.scatter(mat[:, 0], mat[:, 1], c='b', alpha=0.6, label="clusters")

    def convert2d(self, data):
        return self.pca.fit_transform(self.sc.fit_transform(data))
