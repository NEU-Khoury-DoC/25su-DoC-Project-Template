"""
* Logistic Regression Model
* Using party and procedure type to predict the percent of dissent on a vote
* Using the raw percentages - NO classification step as is typically expected of logistic regression
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm

from backend.db_connection import db
import numpy as np
# import logging

from flask import current_app

def get_data(filename):
    '''read in the necessary data from a csv'''
    # read in file, filter out unaffiliated MEPs
    df_final = pd.read_csv(filename)
    df_final = df_final[df_final['party'] != 'Non-attached']

    # convert timestamp column to a datetime object
    df_final['timestamp'] = pd.to_datetime(df_final['timestamp'], format='ISO8601')

    return df_final

def add_time(df_final):
    '''add time features to existing dataframe (probably not actually using these features)'''
    df_time = df_final.copy()

    # extract datetime features
    df_time['year'] = df_time['timestamp'].dt.year
    df_time['month'] = df_time['timestamp'].dt.month
    df_time['weekday'] = df_time['timestamp'].dt.weekday
    df_time['weekofyear'] = df_time['timestamp'].dt.isocalendar().week

    # sort and enumerate unique years
    sorted_years = sorted(df_time['year'].unique())
    year_index_map = {year: i for i, year in enumerate(sorted_years)}

    # adjust weekofyear by year index
    df_time['adjusted_week'] = df_time.apply(lambda row: row['weekofyear'] + 52 * year_index_map[row['year']], axis=1)

    return df_time

def logistic_regression(X, y, w, alpha=1, max_iter=None):
    '''takes X and y features, and initial weight, and optional alpha and
    max number of iterations, than trains the model and returns the final weights'''
    runalg = True
    i = 0
    iter = 0
    
    while runalg:
        x = X[i, :]
        yhat = 1 / (1 + np.exp(-np.dot(x, w)))

        w = w - alpha * (yhat - y[i]) * x
        i += 1

        if i == len(y):
            i = 0
            iter += 1

        if max_iter is not None and iter == max_iter:
            runalg = False
            print(f"Algorithm reached max_iter, final w = {w}")
            print(f"Total number of iterations = {iter}")
    
    return w

def train(df):
    '''trains model; returns trained weight (which is then hardcoded into the db)'''
    X_np = sm.add_constant(pd.get_dummies(df[['party', 'procedure_type']], drop_first=True)).astype(float).values

    # this one prevents us from having values of percent dissent that are exactly 0 or 1
    y_np = df['percent_dissent'].clip(lower=0.00001, upper=0.999).values

    w_init = np.random.randn(X_np.shape[1])

    w_trained = logistic_regression(X_np, y_np, w_init, alpha=0.007, max_iter=3000)
    return w_trained

def cross_validate(df):
    '''cross validate the trained model using train test split, returns the r2 value'''
    X_np = sm.add_constant(pd.get_dummies(df[['party', 'procedure_type']], drop_first=True)).astype(float).values

    # this one prevents us from having values of percent dissent that are exactly 0 or 1
    y_np = df['percent_dissent'].clip(lower=0.00001, upper=0.999).values

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X_np, y_np, test_size=0.2, random_state=42)
    w_init = np.random.randn(X_train.shape[1])
    w_trained = logistic_regression(X_train, y_train, w_init, alpha=0.007, max_iter=3000)
    y_test_pred = 1 / (1 + np.exp(-np.dot(X_test, w_trained)))
    y_pred_percent = y_test_pred * 100
    y_true_percent = y_test * 100

    r2 = r2_score(y_true_percent, y_pred_percent)
    return r2

def predict(party, procedure_type):
    '''retrieve model parameters from the database and predict percent dissent
    based on the input party and procedure_type'''
    # load latest model weights from db
    cursor = db.get_db().cursor(dictionary=True)
    query = 'SELECT weight FROM regressionWeights ORDER BY weightId'
    cursor.execute(query)

    rows = cursor.fetchall()
    params_array = np.array([row['weight'] for row in rows])

    current_app.logger.info(f'Model weights: {params_array}')

    # build input vector
    known_parties = ['EPP', 'ESN', 'GUE/NGL', 'Greens/EFA', 'ID', 'Patriots for Europe', 'Renew', 'S&D']
    known_procedures = ['APP', 'BUD', 'BUI', 'CNS', 'COD', 'DEA', 'DEC', 'INI', 'INL', 'NLE', 'REG', 'RPS', 'RSO', 'RSP']
    feature_order = ['intercept'] + [f'party_{p}' for p in known_parties] + [f'procedure_type_{p}' for p in known_procedures]

    feature_dict = {key: 0.0 for key in feature_order}
    feature_dict['intercept'] = 1.0
    feature_dict[f'party_{party}'] = 1.0
    feature_dict[f'procedure_type_{procedure_type}'] = 1.0

    input_vector = np.array([feature_dict[f] for f in feature_order])

    # predict!
    prediction = 1 / (1 + np.exp(-np.dot(params_array, input_vector)))
    return prediction * 100

#def main():
    # df = get_data('time_series_data_final.csv')
    # w = train(df)

    # store w in the db - make it so that the 'predict' function takes that weight from the db
    # and uses it to predict the percent dissent based on the inputted X array (which has
    # len 2 - a party and procedure type)

    # r2 = cross_validate(df)
    # print(r2)
    

#if __name__ == "__main__":
 #   main()