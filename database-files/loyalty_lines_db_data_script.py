import pandas as pd

csv_path = 'ml-src/members_cleaned.csv'

df = pd.read_csv(csv_path)

print()
mep_data = pd.concat([df.iloc[:,:5], df['country']], axis=1)
mep_data = pd.concat([mep_data, df['percent_agree_current']], axis=1)
print(mep_data)


with open('output.txt', 'w', encoding='utf-8') as f:
    for index, row in mep_data.iterrows():
        
        party = ""
        if row['party'][0:15] + row['party'][16:] == "European Peoples Party":
            party = 1
        elif row['party'] == "Progressive Alliance of Socialists and Democrats":
            party = 2
        elif row['party'] == "European Conservatives and Reformists":
            party = 4
        elif row['party'] == "Patriots for Europe":
            party = 3
        elif row['party'] == "Renew Europe":
            party = 5
        elif row['party'] == "Greens/European Free Alliance":
            party = 6
        elif row['party'] == "The Left in the European Parliament – GUE/NGL":
            party = 7
        elif row['party'] == "Europe of Sovereign Nations":
            party = 8      
        elif row['party'] == "Non-attached Members":
            party = 9
        elif row['party'] == "Identity and Democracy":
            party = 11
        else:
            print(row['party'].strip()) 
            

        f.write(f"INSERT INTO mep(mepID, name, countryOfOrigin, loyaltyScore, partyID, photoURL) VALUES({row['id']}, \"{row['first_name']} {row['last_name']}\", \"{row['country']}\", {str(row['percent_agree_current'])[0:4]}, {party}, \"https://www.europarl.europa.eu/mepphoto/{row['id']}.jpg\");\n")
