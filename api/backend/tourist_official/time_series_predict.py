import pandas as pd
import numpy as np

min_trips = 658396 
max_trips = 526338516

def standardize_data(original_data):
    original_data['Tourism St.'] = (original_data['NumTrips'] - min_trips) / (max_trips - min_trips)


def unstandardize_results(st_data):
    st_data["Predicted_Tourism"] = st_data["Predicted_Tourism"] * (max_trips - min_trips) + min_trips



def get_lag_columns(country_df, lag = 3):

    country_df = country_df.sort_values('Year').reset_index(drop = True)
    country_df['Covid'] = country_df['Year'].apply(lambda x: 1 if x in [2020, 2021] else 0)
    country_df['Bias'] = 1
    min_year = country_df['Year'].min()
    
    index_country = country_df.index[country_df['Year'].astype(int) == min_year + 3]
    index = index_country[0]

    y_vector = []
    x_matrix = []
    x_list = []
    for i in range(index, len(country_df)): 
        if i - lag < 0:
            continue
        bias = 1 
        country = country_df.iloc[i]["Country"]
        lag_values = [country_df.iloc[i - j]['Tourism St.'] for j in range(1, lag + 1)]
        covid = country_df.iloc[i]['Covid']
        year = country_df.iloc[i]['Year']
        
        x_list = [bias, country, year, covid] + lag_values
        x_matrix.append(x_list)
        y_vector.append(country_df.iloc[i]["Tourism St."])

    x_matrix = pd.DataFrame(x_matrix)
    x_matrix.rename(columns={0: "Bias", 1: "Country", 2:"Year", 3:"Covid", 4:"lag1", 5:"lag2", 6:"lag3"}, inplace=True)


    return x_matrix, y_vector

def fit_regression_(X, y):
    Xt = X.T
    XtX = np.dot(Xt, X)
    XtX_inv = np.linalg.inv(XtX)
    Xt_y = np.dot(Xt, y)
    beta = np.dot(XtX_inv, Xt_y)

    return beta


def predict_next_year(beta, X):
    return np.dot(beta, X)

def get_country_years_pred(data, country, lag = 3):

    country_df = data[data['Country'] == country]
    country_df, y = get_lag_columns(country_df, lag = lag)

    lag_cols = [f'lag{i}' for i in range(1, lag + 1)]
    feature_cols = ['Bias', 'Covid'] + lag_cols
    
    X = country_df[feature_cols].values

    beta_tourism = fit_regression(X, y)

    predictions = []
    for index, row in country_df.iterrows():
        year = row['Year']
        X_year = np.array([row[col] for col in feature_cols])
        print(X_year)
        pred_tourism = predict_next_year(beta_tourism, X_year)

        predictions.append({
            'Country': country,
            'Year': year,
            'Actual_Tourism': y[index],
            'Predicted_Tourism': pred_tourism

        })

    all_years_results = pd.DataFrame(predictions)

    return all_years_results

def get_country_prediction(data, weights, country, lag=3):
    country_df = data.copy()
    # print(data)
    country_df, y = get_lag_columns(country_df, lag=lag)

    lag_cols = [f'lag{i}' for i in range(1, lag + 1)]
    feature_cols = ['Bias', 'Covid'] + lag_cols

    X = country_df[feature_cols].values
    
    last_year = country_df['Year'].max()

    last_row = country_df[country_df['Year'] == last_year].iloc[0]
    lag_values = [last_row[f'lag{i}'] for i in range(1, lag + 1)]

    tmp_x = last_row[feature_cols].to_numpy()
    x_old = np.hstack([tmp_x[:2], y[-1], tmp_x[2:4]])
    
    year_list = [last_year + 1]
    country_list = [country]
    pred_list = [predict_next_year(beta_tourism, x_old)]

    for i in range(1, lag):
        year = last_year + i + 1
        
        X_new = np.hstack([x_old[:2], pred_list[i-1], x_old[2:4]])
        pred_tourism = predict_next_year(beta_tourism, X_new)

        year_list.append(year)
        country_list.append(country)
        pred_list.append(pred_tourism)

        x_old = X_new

    predictions = {'Year': year_list,
                   'Country': country_list,
                   'Predicted_Tourism': pred_list}

    final_df = pd.DataFrame(predictions)
    final_df = unstandardize_results(final_df)
    return final_df