from multiprocessing import Process
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

class drawer:
    """
    la class qui gere l'affichage des donnees et du model en temps reel
    """

    def __init__(self, q=None):
        # super(drawer, self).__init__()
        self.fig, self.ax = plt.subplots()
        self.queue = q
        self.sc = StandardScaler()
        self.pca = PCA(n_components = 2)

    def run(self):
        print("run")

    def plot_matrix(self, mat):
        print"plot matrix"

    def convert2d(self, data):
        return self.pca.fit_transform(self.sc.fit_transform(data))
