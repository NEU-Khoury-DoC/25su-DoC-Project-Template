"""
5/27/25
Sienna here - I wrote this code to get all the necessary data from the api that we need for our party cohesion over time
model. These functions scrape the data from the api and put it in a df, then save it in a csv which I put in the preprocessed
data folder. This is only for the last 1000 votes on distinct policies, however, because the api was taking forever to run.
I might try getting all of the data later because I was overloading the api which is why I think it's slow.
"""

import requests
import pandas as pd
import time

def fetch_and_process_vote_data(vote_id):
    '''returns lists of for, against, abstention, and no votes counts for each party for the provided vote id
    
    Args:
        vote_id: string, the id from the voting event being analyzed
        
    Returns:
        parties, votes_for, votes_against, abstentions, no_votes: a tuple of lists corresponding to the number
        of each vote type for each party within the specified voting event
    '''
    # get info from api for an individual voting event
    vote_url = f"https://howtheyvote.eu/api/votes/{vote_id}"
    vote_resp = requests.get(vote_url)
    vote_data = vote_resp.json()

    # initialize lists for parties and vote breakdowns
    parties = []
    votes_for = []
    votes_against = []
    abstentions = []
    no_votes = []

    # iterate through each party's information about that particular voting event
    for i in range(len(vote_data['stats']['by_group'])):
        # add party name, votes for, votes against, abstentions, and no votes to corresponding lists
        parties.append(vote_data['stats']['by_group'][i]['group']['label'])
        vote_dict = vote_data['stats']['by_group'][i]['stats']
        votes_for.append(vote_dict['FOR'])
        votes_against.append(vote_dict['AGAINST'])
        abstentions.append(vote_dict['ABSTENTION'])
        no_votes.append(vote_dict['DID_NOT_VOTE'])

    # return all lists of party info
    return parties, votes_for, votes_against, abstentions, no_votes


def get_all_data():
    '''gets all necessary data for party cohesion overtime from the api and stores it in a dataframe
    
    Returns:
        df: a pandas dataframe of relevant party data from the api    
    '''
    # create an empty DataFrame; specify column names
    columns_lst = ['policy_id', 'date', 'party', 'votes_for', 'votes_against', 'abstentions', 'no_votes']
    df = pd.DataFrame(columns = columns_lst)

    # read in csv for full id list
    df_csv = pd.read_csv('votes.csv')
    unique_rows = df_csv.drop_duplicates(subset='display_title', keep='first')
    filtered_rows = unique_rows.tail(1000).to_dict(orient='records')

    for row in filtered_rows:
        vote_id = str(row['id'])
        vote_url = f"https://howtheyvote.eu/api/votes/{vote_id}"

        try:
            vote_resp = requests.get(vote_url, timeout=(5, 10))
            vote_resp.raise_for_status()
            vote_data = vote_resp.json()

            timestamp = vote_data.get('timestamp')
            timestamp = pd.to_datetime(timestamp)
            for group in vote_data['stats']['by_group']:
                party = group['group']['label']
                stats = group['stats']
                vote_dict = {
                    'policy_id': vote_id,
                    'date': timestamp,
                    'party': party,
                    'votes_for': stats.get('FOR', 0),
                    'votes_against': stats.get('AGAINST', 0),
                    'abstentions': stats.get('ABSTENTION', 0),
                    'no_votes': stats.get('DID_NOT_VOTE', 0)
                }
                df = pd.concat([df, pd.DataFrame([vote_dict])], ignore_index=True)

            time.sleep(0.2)

        except requests.exceptions.ConnectTimeout:
            print(f"Connection timeout for vote ID {vote_id}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"General request error for vote ID {vote_id}: {e}")
            continue

    return df

def main():
    
    # store data from api in a df
    df = get_all_data()
    
    # make needed columns to calculate the percent of dissenters from each party on each vote
    df['majority_vote_count'] = df[['votes_for', 'votes_against', 'abstentions', 'no_votes']].max(axis=1)
    df['majority_col'] = df[['votes_for', 'votes_against', 'abstentions', 'no_votes']].idxmax(axis=1)

    # store data in a csv

if __name__ == "__main__":
    main()