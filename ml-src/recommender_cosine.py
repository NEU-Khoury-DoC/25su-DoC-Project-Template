# import statements
import numpy as np
import pandas as pd

def make_full_df(filepath):
    """
    Creating full DataFrame of MEP info from CSV
    
    Args:
        filepath (str): filepath for csv
    
    Returns:
        df (DataFrame): DataFrame of member info from CSV
    """
    
    df = pd.read_csv(filepath)
    return df

def get_metrics(df, party_name, **kwargs):
    """
    Returns DataFrame with just metrics for recommender, standardizing values from 0-1 scale
    
    Args:
        df (DataFrame): full DataFrame of member info
        party_name (str): inputter's party
        **kwargs (dictionary): optional parameters
            - party (bool): whether to include party in recommender data (default: False)
            - country (bool): whether to include country in recommender data (default: False)
    Returns:
        df_metrics (DataFrame): DataFrame of standardized metrics for recommender
    """
    
    # turning percent columns into decimals so all values are standardized - between 0 and 1
    columns_to_decimals = ['percent_agree_current', 'percent_show_up', 'European People’s Party percentage', 'Renew Europe percentage',
     'Progressive Alliance of Socialists and Democrats percentage',
     'European Conservatives and Reformists percentage',
     'Non-attached Members percentage',
     'Europe of Sovereign Nations percentage',
     'The Left in the European Parliament – GUE/NGL percentage',
     'Greens/European Free Alliance percentage',
     'Patriots for Europe percentage', 'Identity and Democracy percentage']
    
    df[columns_to_decimals] = df[columns_to_decimals] / 100

    # accounting for kwargs and creating DataFrame accordingly
    if 'party' in kwargs and 'country' in kwargs:
        df_metrics = df[['party', 'percent_agree_current', 'percent_show_up', 'country', f'{party_name} percentage']]

    elif 'party' in kwargs:
        df_metrics = df[['party', 'percent_agree_current', 'percent_show_up', f'{party_name} percentage']]

    elif 'country' in kwargs:
        df_metrics = df[['percent_agree_current', 'percent_show_up', 'country', f'{party_name} percentage']]

    else:
        df_metrics = df[['percent_agree_current', 'percent_show_up', f'{party_name} percentage']]
    
    return df_metrics

def get_encoded_df(df):
    """
    Returns DataFrame of comparison metrics with one-hot encoded categorical variables
  
    Args:
        df (DataFrame): DataFrame with standardized metrics for filtering
  
    Returns:
        df (DataFrame): DataFrame with one-hot encoded categorical metrics
    """
    # getting column names
    columns = df.columns

    # accounting for optional party and/or country parameters and creating encoded df accordingly
    if 'party' in columns and 'country' in columns:
        party_dummies = pd.get_dummies(df, columns=['party'], dtype='int', drop_first = True)
        df_encoded = pd.get_dummies(party_dummies, columns=['country'], dtype='int', drop_first = True)
        return df_encoded

    elif 'party' in columns:
        party_dummies = pd.get_dummies(df, columns=['party'], dtype='int', drop_first = True)
        return party_dummies

    elif 'country' in columns:
        country_dummies = pd.get_dummies(df, columns=['country'], dtype='int', drop_first = True)
        return country_dummies
    
    return df

def get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, **kwargs):
    """
    Returns a vector of inputter's criteria for recommender model
    
    Args:
        percent_agree_current (float): alignment rate for potential recruit's current party 
        percent_attendance (float): attendance rate for votes  
        my_party (str): inputter's party  
        my_party_percentage (float): percent aligned with the inputter's party 
        **kwargs: optional parameters
            - new_candidate_party (str): party that new candidate is from
            - new_candidate_country (str): country that new candidate is from
    
    Returns:
        vector (np array): vector of inputted criteria
    """
    
    # creating first dictionary of non-optional parameters
    nums = {'percent_agree_current': [percent_agree_current/100], 
           'percent_show_up': [percent_attendance/100], 
           f'{my_party} percentage': [my_party_percentage/100]}

    # party information dictionary if party specified in kwargs
    if 'new_candidate_party' in kwargs:
        
        parties = {'party_European Conservatives and Reformists': [0], 
               'party_European People’s Party': [0],
               'party_Greens/European Free Alliance': [0],
               'party_Identity and Democracy': [0],
               'party_Non-attached Members': [0],
               'party_Patriots for Europe': [0], 
               'party_Progressive Alliance of Socialists and Democrats': [0],
               'party_Renew Europe': [0],
               'party_The Left in the European Parliament – GUE/NGL': [0]}
    
        # specifying original candidate party in dct
        for key in parties:
            if key[key.index('_')+1:] == kwargs['new_candidate_party']:
                parties[key] = [1]            
        
        nums |= parties
    
    # country information dictionary if country specified in kwargs
    if 'new_candidate_country' in kwargs:
    
        countries = {'country_Belgium': [0], 
               'country_Bulgaria': [0], 
               'country_Croatia': [0], 
               'country_Cyprus': [0], 
               'country_Czechia': [0],
               'country_Denmark': [0], 
               'country_Estonia': [0], 
               'country_Finland': [0], 
               'country_France': [0],
               'country_Germany': [0], 
               'country_Greece': [0], 
               'country_Hungary': [0], 
               'country_Ireland': [0],
               'country_Italy': [0], 
               'country_Latvia': [0], 
               'country_Lithuania': [0], 
               'country_Luxembourg': [0],
               'country_Malta': [0], 
               'country_Netherlands': [0], 
               'country_Poland': [0], 
               'country_Portugal': [0],
               'country_Romania': [0], 
               'country_Slovakia': [0], 
               'country_Slovenia': [0], 
               'country_Spain': [0],
               'country_Sweden': [0]}
    
        # specifying candidate country in dict
        for key in countries:
            if key[key.index('_')+1:] == kwargs['new_candidate_country']:
                countries[key] = [1]

        # adding dictionary
        nums |= countries
    
    # turning nums into a 1D np array for comparison
    vector = np.array(pd.DataFrame(nums)).flatten()
    
    return vector

def get_weights_vector(percent_agree_current_weight, percent_attendance_weight, my_party, my_party_percentage_weight, **kwargs):
    """
    Returns a vector of importance value weights for recommender model
    
    Args:
        percent_agree_current_weight (float): alignment rate importance value for potential recruit's current party 
        percent_attendance_weight (float): attendance rate importance value for votes  
        my_party (str): inputter's party  
        my_party_percentage_weight (float): percent aligned with the inputter's party importance value
        **kwargs: optional parameters
            - new_candidate_party_weight (float): importance value for party that new candidate is from
            - new_candidate_country_weight (float): importance values for country that new candidate is from
    
    Returns:
        weights (np array): vector of importance value weights
    """
    # first dictionary of non-optional parameters
    nums = {'percent_agree_current_weight': [percent_agree_current_weight/100], 
           'percent_show_up_weight': [percent_attendance_weight/100], 
           f'{my_party} percentage_weight': [my_party_percentage_weight/100]}

    # creating dictionary of party weights if party specified in kwargs
    if 'new_candidate_party_weight' in kwargs:
        
        parties = {'party_European Conservatives and Reformists': [0], 
               'party_European People’s Party': [0],
               'party_Greens/European Free Alliance': [0],
               'party_Identity and Democracy': [0],
               'party_Non-attached Members': [0],
               'party_Patriots for Europe': [0], 
               'party_Progressive Alliance of Socialists and Democrats': [0],
               'party_Renew Europe': [0],
               'party_The Left in the European Parliament – GUE/NGL': [0]}
    
        # specifying current candidate party
        for key in parties:
            if key[key.index('_')+1:] == kwargs['new_candidate_party_weight']:
                parties[key] = [1*(kwargs['new_candidate_party_weight']/100)]            
        
        nums |= parties
    
    # creating dictionary of country weights if country specified in kwargs 
    if 'new_candidate_country_weight' in kwargs:
    
        countries = {'country_Belgium': [0], 
               'country_Bulgaria': [0], 
               'country_Croatia': [0], 
               'country_Cyprus': [0], 
               'country_Czechia': [0],
               'country_Denmark': [0], 
               'country_Estonia': [0], 
               'country_Finland': [0], 
               'country_France': [0],
               'country_Germany': [0], 
               'country_Greece': [0], 
               'country_Hungary': [0], 
               'country_Ireland': [0],
               'country_Italy': [0], 
               'country_Latvia': [0], 
               'country_Lithuania': [0], 
               'country_Luxembourg': [0],
               'country_Malta': [0], 
               'country_Netherlands': [0], 
               'country_Poland': [0], 
               'country_Portugal': [0],
               'country_Romania': [0], 
               'country_Slovakia': [0], 
               'country_Slovenia': [0], 
               'country_Spain': [0],
               'country_Sweden': [0]}
    
        # specifying candidate country
        for key in countries:
            if key[key.index('_')+1:] == kwargs['new_candidate_country_weight']:
                countries[key] = [1*(kwargs['new_candidate_country_weight']/100)]

        nums |= countries
    
    # turning dictionary into 1D numpy array for multiplication
    weights = np.array(pd.DataFrame(nums)).flatten()

    return weights

def get_recs_df(full_df, encoded_df, filters_vec, party_name, **kwargs):
    """
    Returns top 10 MEPs matching inputter's criteria
    
    Args:
        full_df (DataFrame): full df of MEP information 
        encoded_df (DataFrame): df of recommender criteria with encoded categorical variables  
        filters_vec (np array): vector for inputter's criteria 
        party_name (str): inputter's party name
        **kwargs: optional parameters
            - weights (np array): numpy array of feature importance weights
    
    Returns:
        recruits (DataFrame): top 10 MEPs to join the inputter's party 
    """
    # initializing lists
    mep_dot_products = []
    mep_cosines = []
    
    # checking for optional weight parameter
    if 'weights' in kwargs:
        weights = kwargs['weights']
        filters_vec *= weights
    
    # comparing inputted filters vector to every other MEP, taking weights into account if specified
    for idx in range(len(encoded_df)):
        temp_vec = np.array(encoded_df.iloc[idx]).flatten()
        if 'weights' in kwargs:
            temp_vec *= weights
        
        temp_dot = np.dot(filters_vec, temp_vec)
    
        temp_cos = temp_dot/(np.linalg.norm(filters_vec) * np.linalg.norm(temp_vec))
    
        mep_dot_products.append(temp_dot)
        mep_cosines.append(temp_cos)
    
    # dictionary of MEP info
    dict_mep = {'mep_id': full_df.id,
            'first_name': full_df.first_name,
            'last_name': full_df.last_name,
            'country': full_df.country,
            'current_party': full_df.party,
            'current_party_alignment': full_df.percent_agree_current * 100,
            f'{party_name} alignment': full_df[f'{party_name} percentage'] * 100,
            'attendance_rate': full_df.percent_show_up * 100,
            'mep_dot_product': mep_dot_products,
            'mep_cosine': mep_cosines}
    df_mep = pd.DataFrame(dict_mep)
    
    # sorts the data by the cosine score
    sorted_df_mep = df_mep.sort_values(by='mep_cosine', ascending=False)
    
    filtered_df = sorted_df_mep[sorted_df_mep['current_party'] != party_name]

    filtered_df = filtered_df.rename(columns={'mep_id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 'country': 'Country',
                        'current_party': 'Current Party', f'{party_name} alignment': f'{party_name} Alignment Rate',
                            'current_party_alignment': 'Current Party Alignment Rate', 
                            'attendance_rate': 'Attendance Rate'})

    # getting and returning top 10 MEPs matching inputter's criteria/weights
    recruits = filtered_df.head(10)
    
    return recruits

def get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, **kwargs):
    """
    Combines previous functions so user only has to input parameters in one place to get recommendations

    Args:
        full_df (DataFrame): full df of MEP information 
        encoded_df (DataFrame): df of recommender criteria with encoded categorical variables  
        filters_vec (np array): vector for inputter's criteria 
        party_name (str): inputter's party name
        **kwargs: optional parameters
            - weights (np array): numpy array of feature importance weights
    
    Returns:
        recs (DataFrame): top 10 MEPs to join the inputter's party 
    
    """
    # creating metrics df based on optional parameters specified
    if 'new_candidate_party' in kwargs and 'new_candidate_country' in kwargs:
        df_metrics = get_metrics(df, my_party, party = True, country = True)

    elif 'new_candidate_party' in kwargs:
        df_metrics = get_metrics(df, my_party, party = True)

    elif 'new_candidate_country' in kwargs:
        df_metrics = get_metrics(df, my_party, country = True)
    
    else:
        df_metrics = get_metrics(df, my_party)

    # creating df with one-hot encoded categorical variables
    df_encoded = get_encoded_df(df_metrics)

    # creating filters vector based on optional parameters specified
    if 'new_candidate_party' in kwargs and 'new_candidate_country' in kwargs:
        filters_vec = get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = kwargs['new_candidate_party'], new_candidate_country = kwargs['new_candidate_country'])

    elif 'new_candidate_party' in kwargs:
        filters_vec = get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = kwargs['new_candidate_party'])

    elif 'new_candidate_country' in kwargs:
        filters_vec = get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_country = kwargs['new_candidate_country'])

    else:
        filters_vec = get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage)

    # getting weights vector if weights specified in kwargs
    if 'weights' in kwargs:
        return get_recs_df(df, df_encoded, filters_vec, my_party, weights = kwargs['weights'])

    # getting df of recommended MEPs
    recs = get_recs_df(df, df_encoded, filters_vec, my_party)
    
    return recs
    

def get_dissenters(df, party_name):
    """
    Returns top 10 dissenting MEPs in the inputter's party
    
    Args:
        df (DataFrame): full df of MEP information
        party_name (str): inputter's party name
    
    Returns:
        dissents (DataFrame): top 10 dissenting MEPs to the inputter's party
    """
    # filtering df to only members in the party who do not have 0% alignment rates
    df = df[df['party'] == party_name]
    df = df[df['percent_agree_current'] != 0]
    
    # filtering df to only features which will be returned
    df = df[['id', 'first_name', 'last_name', 'percent_dissent_current']]

    # getting highest dissenters, renaming columns
    df = df.sort_values(by = 'percent_dissent_current', ascending = False)
    df = df.rename(columns={'id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 'percent_dissent_current': 'Dissent Rate'})
    dissents = df.head(10)
    
    return dissents

def search_mep_metrics(df, mep_id):
    """
    Returns information for a single MEP
    
    Args:
        df (DataFrame): full df of MEP information
        mep_id (int): MEP the inputter wants info for
    
    Returns:
        mep_info (DataFrame): a single df row with information about the specified MEP
    """
    # filtering df to only necessary info
    df = df[['id', 'first_name', 'last_name', 'party', 'percent_agree_current', 'percent_dissent_current',
       'percent_show_up', 'country', 'European People’s Party percentage',
       'Renew Europe percentage',
       'Progressive Alliance of Socialists and Democrats percentage',
       'European Conservatives and Reformists percentage',
       'Non-attached Members percentage',
       'Europe of Sovereign Nations percentage',
       'The Left in the European Parliament – GUE/NGL percentage',
       'Greens/European Free Alliance percentage',
       'Patriots for Europe percentage',
       'Identity and Democracy percentage']]

    # renaming columns for organization on UI
    df = df.rename(columns={'id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 
                            'percent_agree_current': 'Current Party Alignment Rate', 
                            'percent_dissent_current': 'Current Party Dissent Rate', 'percent_show_up': 'Attendance Rate',
                            'country': 'Country'})

    # getting and returning the MEP's info
    mep_info = df[df['MEP ID'] == mep_id]
    
    return mep_info

def main():
    """
    Main function
    
    Args:
        None
    
    Returns:
        None
    """
    
    # NOTE: my_party for get_weights_vector and get_recommendations 
    # parameters should be the *SAME*!

    # active_members.csv is data in a SQL table
    df = make_full_df('active_members.csv')
    # parameters: percent_agree_current, percent_attendance, my_party, my_party_percentage, **kwargs (party and/or country)
    
    # testing!
    weights = get_weights_vector(5, 90,'Patriots for Europe', 4, new_candidate_country_weight = 1)
    recs = get_recommendations(df, 70, 80, 'Patriots for Europe', 80, new_candidate_country = 'France', weights = weights)

if __name__ == '__main__':
    main()