import numpy as np
import math

import pandas as pd


def log_regress(X, y, w, alpha = 0.5, max_iter = 1000):
    runalg = True
    i = 0
    iter = 0

    while runalg:
        x = X[i,:]
        dot_prod = np.dot(x, w)
        y_hat = 1 / (1 + np.exp(-dot_prod))
        gradient = (y_hat - y[i]) * x
        w = w - alpha * gradient
        i += 1
        if i >= len(y):
            i = 0
            iter += 1
        if iter > max_iter:
            runalg = False
            break
    
    return w

def lin_regress(X,y,bias_col=False):
    if bias_col:
        X = np.hstack([np.ones(len(y)).reshape(-1,1), X])
    XTXinv = np.linalg.inv(np.dot(X.T,X))
    XTy = np.dot(X.T, y)
    c = np.dot(XTXinv, XTy)
    return c