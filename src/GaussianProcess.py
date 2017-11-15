from math import sqrt, ceil
import numpy as np
from sklearn import gaussian_process as gp
from sklearn.gaussian_process.kernels import WhiteKernel, Matern, RBF
import matplotlib.pyplot as plt
import random


class GP:
    def __init__(self, rows):
        kernal = WhiteKernel(noise_level=50) + RBF([500.0, 100.0])
        self.clf = gp.GaussianProcessClassifier(kernel=kernal)
        self.dataX = [(0, 64), (1, 0)]
        self.dataY = [1, 0]
        self.bound_f = None
        self.bound_r = None
        self.res = 200
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
        r, _ = position
        self.dataX.append((r, size), )
        self.dataY.append(score)
        self._update()

    def _update(self):
        self.X = np.array(self.dataX)
        self.y = np.array(self.dataY)
        self.clf.fit(self.X, self.y)

    def draw(self, r):
        y_min, y_max = 4, self.X[:, 1].max() * 1.2
        X = np.c_[r * np.ones(self.res), np.linspace(y_min, y_max, self.res)]
        Z = self.clf.predict_proba(X)
        ind = np.argmax(abs(np.diff(Z[:, 0])))
        class_bound = X[ind, 1]
        return ceil(np.random.gamma(2, class_bound))

    def get_bound(self):
        if self.bound_f != None and self.bound_r != None:
            return self.bound_r, self.bound_f
        else:
            raise AttributeError

    def plot(self):
        x_min, x_max = 0, self.X[:, 0].max() * 1.1
        y_min, y_max = 0, 151
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, self.res),
            np.linspace(y_min, y_max, self.res))
        X = np.c_[xx.ravel(), yy.ravel()]
        Z = self.clf.predict_proba(X)
        Z = Z.reshape((xx.shape[0], xx.shape[1], 2))
        Z = np.lib.pad(Z, ((0, 0), (0, 0), (0, 1)),
                       'constant',
                       constant_values=0)
        #plotting

        plt.imshow(Z, aspect='auto', origin="lower")

        #ind = np.argmax(abs(np.diff(Z[:, :, 0], axis=0)), axis=0)
        ind = np.argmin(abs(Z[:, :, 0] - 0.5), axis=0)
        self.bound_f = np.linspace(y_min, y_max, self.res)[ind]
        self.bound_r = np.linspace(x_min, x_max, self.res)
        plt.plot(self.bound_r * self.res / x_max, self.bound_f)

        # Plot also the training points
        plt.scatter(
            self.X[:, 0] * self.res / x_max,
            self.X[:, 1] * self.res / y_max,
            c=np.array(["r", "g", "b"])[self.y],
            edgecolors=(0, 0, 0))
        plt.xlabel('radial distance')
        plt.ylabel('fontsize')
        plt.xlim(0, self.res)
        plt.ylim(0, self.res)
        plt.xticks(
            np.arange(0, self.res, 100 * self.res / x_max),
            np.arange(0, x_max, 100))
        plt.yticks(
            np.arange(0, self.res, 10 * self.res / y_max),
            np.arange(0, y_max, 10))
        plt.show()