import numpy as np
import pandas as pd
from models import log_regress
from models import lin_regress
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from datetime import datetime

megaframe = pd.read_csv('datasets/MEGAFRAME_CLEANEDV2.csv')


X_df = pd.get_dummies(megaframe, columns=['Region'], dtype=int)
X_df = X_df.drop(labels=['TIME_PERIOD', 'Reference area', 'REF_AREA', 'Gini index'], axis=1)
describe = X_df.describe().loc[['mean', 'std']].to_numpy()

# # Assume X is your full NumPy array
# num_exclude = 4

# # Split the array
# X_main = X[:, :-num_exclude]   # Columns to standardize
# X_last = X[:, -num_exclude:]   # Columns to leave untouched

# # Standardize the first part
# mean = X_main.mean(axis=0)
# std = X_main.std(axis=0)
# std[std == 0] = 1  # Avoid division by zero
# X_main_standardized = (X_main - mean) / std

# # Concatenate back together
# X = np.hstack([X_main_standardized, X_last])
# print(X)

X = np.array([78.699997,28.0,0.0734319847255705,0.0631525528524754,0.0057497428086187,0.0025634702523358,5.1075,5.825,8895960.0,27259.4806735435,2.40595834145438,0,1,0,0])

def predict_gini(X, describe, weights, model='logistic'):
    X = np.hstack([[(X[i] - describe[0,i]) / describe[1,i] for i in range(len(X)-4)], X[-4:]])
    if model == 'linear':
        gini = np.dot(X, weights)
    elif model == 'logistic':
        gini = 1 / (1 + np.exp(-np.dot(X, weights)))
    return gini

print(predict_gini(X, describe))