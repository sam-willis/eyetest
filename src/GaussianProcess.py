from math import sqrt
import numpy as np
from sklearn import gaussian_process as gp
from sklearn.gaussian_process.kernels import WhiteKernel, Matern, RBF
import matplotlib.pyplot as plt
import random


class GP:
    def __init__(self, rows):
        kernal = 1.0 * RBF([1.0, 1.0])
        self.clf = gp.GaussianProcessClassifier(kernel=kernal)
        self.dataX = [(0, 64), (1, 0)]
        self.dataY = [1, 0]
        for row in rows:
            position, msg, msg_guess, size = row
            score = 1 if msg_guess == msg else 0
            x, y = position
            r = sqrt(x**2 + y**2)
            self.dataX.append((r, size), )
            self.dataY.append(score)
        self._update()

    def update(self, position, msg, msg_guess, size):
        score = 1 if msg_guess == msg else 0
        x, y = position
        r = sqrt(x**2 + y**2)
        self.dataX.append((r, size), )
        self.dataY.append(score)
        self._update()

    def _update(self):
        self.X = np.array(self.dataX)
        self.y = np.array(self.dataY)
        self.clf.fit(self.X, self.y)

    def draw(self, position):
        x, y = position
        r = sqrt(x**2 + y**2)
        #self.clf.predict_proba(self.X)
        return random.randint(10, 100)

    def plot(self):
        x_min, x_max = 0, self.X[:, 0].max() * 1.2
        y_min, y_max = 0, self.X[:, 1].max() * 1.2
        h = 100
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, h), np.linspace(y_min, y_max, h))
        X = np.c_[xx.ravel(), yy.ravel()]
        Z = self.clf.predict_proba(X)
        Z = Z.reshape((xx.shape[0], xx.shape[1], 2))
        Z = np.lib.pad(Z, ((0, 0), (0, 0), (0, 1)),
                       'constant',
                       constant_values=0)
        #plotting

        plt.imshow(Z, aspect='auto', origin="lower")

        # Plot also the training points
        plt.scatter(
            self.X[:, 0] * h / x_max,
            self.X[:, 1] * h / y_max,
            c=np.array(["r", "g", "b"])[self.y],
            edgecolors=(0, 0, 0))
        plt.xlabel('radial distance')
        plt.ylabel('fontsize')
        plt.xlim(0, h)
        plt.ylim(0, h)
        plt.xticks(np.arange(0, h, 500 * h / x_max), np.arange(0, x_max, 500))
        plt.yticks(np.arange(0, h, 10 * h / y_max), np.arange(0, y_max, 10))
        #plt.tight_layout()
        plt.show()
