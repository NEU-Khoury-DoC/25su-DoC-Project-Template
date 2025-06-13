# Cleaned and consolidated version of the recommender_cosine.py logic
import numpy as np
import pandas as pd

# Load the full MEP info DataFrame from a CSV
def make_df(filepath):
    """
    Creates a DataFrame from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_csv(filepath)

# Standardize numerical columns and extract relevant metrics
def get_metrics(df, party_name):
    """
    Extracts and standardizes metrics for recommender input.

    Args:
        df (pd.DataFrame): Raw MEP data.
        party_name (str): The user's preferred party.

    Returns:
        pd.DataFrame: Standardized metric subset.
    """
    percentage_cols = [
        'percent_agree_current', 'percent_show_up',
        'European People’s Party percentage', 'Renew Europe percentage',
        'Progressive Alliance of Socialists and Democrats percentage',
        'European Conservatives and Reformists percentage',
        'Non-attached Members percentage', 'Europe of Sovereign Nations percentage',
        'The Left in the European Parliament – GUE/NGL percentage',
        'Greens/European Free Alliance percentage',
        'Patriots for Europe percentage', 'Identity and Democracy percentage'
    ]
    df[percentage_cols] = df[percentage_cols] / 100
    return df[['party', 'percent_agree_current', 'percent_show_up', 'country', f'{party_name} percentage']]

# Encode categorical columns (party and country)
def get_encoded_df(df):
    """
    One-hot encodes party and country fields.

    Args:
        df (pd.DataFrame): Standardized metrics DataFrame.

    Returns:
        pd.DataFrame: Encoded features DataFrame.
    """
    df = pd.get_dummies(df, columns=['party', 'country'], dtype=int, drop_first=True)
    return df

# Build an input vector from user criteria
def get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party, new_candidate_country):
    """
    Constructs a filter vector from user inputs.

    Returns:
        np.ndarray: Input vector.
    """
    # Base numeric metrics
    base = {
        'percent_agree_current': [percent_agree_current],
        'percent_show_up': [percent_attendance],
        f'{my_party} percentage': [my_party_percentage]
    }

    # One-hot for party
    parties = {
        'party_European Conservatives and Reformists': [0],
        'party_European People’s Party': [0],
        'party_Greens/European Free Alliance': [0],
        'party_Identity and Democracy': [0],
        'party_Non-attached Members': [0],
        'party_Patriots for Europe': [0],
        'party_Progressive Alliance of Socialists and Democrats': [0],
        'party_Renew Europe': [0],
        'party_The Left in the European Parliament – GUE/NGL': [0]
    }
    for key in parties:
        if key.split('_', 1)[1] == new_candidate_party:
            parties[key] = [1]

    # One-hot for country
    countries = {
        f'country_{country}': [0] for country in [
            'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland',
            'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
            'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
            'Slovenia', 'Spain', 'Sweden'
        ]
    }
    countries[f'country_{new_candidate_country}'] = [1]

    # Combine and convert to vector
    full_input = base | parties | countries
    return np.array(pd.DataFrame(full_input))

# Recommend top 10 matching MEPs
def get_recommendations(full_df, encoded_df, filters_vec, party_name):
    """
    Returns top 10 recommended MEPs based on cosine similarity.

    Returns:
        pd.DataFrame: Top 10 recommended MEPs.
    """
    dot_scores = []
    cosine_scores = []

    for idx in range(len(encoded_df)):
        row_vec = np.array(encoded_df.iloc[idx]).reshape(-1, 1)
        dot = np.dot(filters_vec, row_vec)
        cosine = dot / (np.linalg.norm(filters_vec) * np.linalg.norm(row_vec))
        dot_scores.append(dot[0])
        cosine_scores.append(cosine[0])

    # Build output DataFrame
    results = pd.DataFrame({
        'MEP ID': full_df.id,
        'First Name': full_df.first_name,
        'Last Name': full_df.last_name,
        'Country': full_df.country,
        'Current Party': full_df.party,
        'Current Party Alignment Rate': full_df.percent_agree_current,
        f'{party_name} Alignment': full_df[f'{party_name} percentage'],
        'Attendance Rate': full_df.percent_show_up,
        'Cosine Score': cosine_scores
    })

    # Filter and return top 10 outside inputter's party
    filtered = results[results['Current Party'] != party_name]
    return filtered.sort_values(by='Cosine Score', ascending=False).head(10)

# Get top dissenters within a party
def get_dissenters(df, party_name):
    """
    Returns the top 10 most dissenting MEPs in a given party.
    """
    filtered = df[(df['party'] == party_name) & (df['percent_agree_current'] != 0)]
    filtered = filtered[['id', 'first_name', 'last_name', 'percent_dissent_current']]
    filtered = filtered.rename(columns={
        'id': 'MEP ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'percent_dissent_current': 'Dissent Rate'
    })
    return filtered.sort_values(by='Dissent Rate', ascending=False).head(10)

# Return info for a specific MEP by ID
def search_mep_metrics(df, mep_id):
    """
    Gets detailed metric breakdown for a specific MEP.
    """
    df = df.rename(columns={
        'id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name',
        'percent_agree_current': 'Current Party Alignment Rate',
        'percent_dissent_current': 'Current Party Dissent Rate',
        'percent_show_up': 'Attendance Rate',
        'country': 'Country'
    })
    return df[df['MEP ID'] == mep_id]

    #series object. probably a numpy. how to convert a array to json
