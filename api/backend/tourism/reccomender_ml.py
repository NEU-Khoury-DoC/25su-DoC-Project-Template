import pandas as pd
import numpy as np

def standardize(df_merged):
    """
    standardize data 
    """
    df_merged["Fuel Score St."] = (df_merged["FuelPriceScore"].astype(float) - 1) / (7-1)
    df_merged["Density Score St."] = (df_merged["RoadDensityScore"].astype(float) - 1) / (7-1)

    min_trips = df_merged['NumTrips'].min()
    max_trips = df_merged['NumTrips'].max()
    df_merged['Tourism St.'] = (df_merged['NumTrips'] - min_trips) / (max_trips - min_trips)

    return df_merged

def normalize_user_input(user_input):
    """
    Takes in user preferences on a 0-10 scale for:
    - fuel: importance on saving fuel prices
    - traffic: importance avoiding traffic
    - tourism: importance of avoiding high-tourism countries

    Returns: a normalized array on a 0-1 scale
    """
    max_scale = 10
    weights = np.array([
        user_input['fuel_price'] / max_scale,
        user_input['traffic_time'] / max_scale,
        user_input['tourism_num'] / max_scale
    ])
    return weights

def compute_cosine_similarities(user_vector, country_vector):
    """
    Gets the cosine similarity between the user input and each country's vector.

    Returns: similarity score (float)
    """    
    dot_product = np.dot(user_vector, country_vector)
    user_norm = np.linalg.norm(user_vector)
    country_norm = np.linalg.norm(country_vector)

    # Prevent division by zero
    if user_norm == 0 or country_norm == 0:
        return 0

    return dot_product / (user_norm * country_norm)


def get_top_5_recommendations(user_input, recommender_data):
    """Recommends top 5 countries closest to user preferences based on cosine similarity."""

    user_vector = normalize_user_input(user_input)

    similarities = []

    recommender_data = standardize(recommender_data)

    print(recommender_data)
    for index, row in recommender_data.iterrows():
        country_vector = np.array([
            row["Fuel Score St."], 
            row["Density Score St."], 
            row["Tourism St."]
        ])

        similarity = compute_cosine_similarities(user_vector, country_vector)
        similarities.append((row["Country"], similarity))

    similarity_df = pd.DataFrame(similarities, columns=["Country", "Similarity"])
    top_5 = similarity_df.sort_values("Similarity", ascending=False).head(5)

    return top_5

    