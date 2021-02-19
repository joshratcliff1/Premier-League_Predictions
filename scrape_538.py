import pandas as pd
from datetime import datetime

now = datetime.now() # current date and time
today = now.strftime('%Y-%m-%d')

# show complete records by changing rules
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# Scrape tables from the webpage
dfs = pd.read_html('https://projects.fivethirtyeight.com/soccer-predictions/premier-league/')

# Load the dataset into the dataframe
df = dfs[-1]

list_538 = []

team_dict = {'Arsenal': 'Arsenal',
             'Aston Villa': 'Aston Villa',
             'Brighton': 'Brighton',
             'Burnley': 'Burnley',
             'Chelsea': 'Chelsea',
             'Crystal Palace': 'Crystal Palace',
             'Everton': 'Everton',
             'Fulham': 'Fulham',
             'Leeds United': 'Leeds',
             'Leicester': 'Leicester',
             'Liverpool': 'Liverpool',
             'Newcastle': 'Newcastle',
             'Man. City': 'Man City',
             'Man. United': 'Man Utd',
             'Sheffield Utd': 'Sheffield Utd',
             'Southampton': 'Southampton',
             'Tottenham': 'Spurs',
             'West Brom': 'West Brom',
             'West Ham': 'West Ham',
             'Wolves': 'Wolves'}

for index, row in df.iterrows():
    list_538.append((row[('Unnamed: 0_level_0', 'team')], row[('avg. simulated season', 'proj. pts.pts.')]))
    pass

new_list = []

print('538 predictions on ', today, '\n')

for team, pts in list_538:
    team = team[0:-6]
    print(team_dict[team], pts)
    new_list.append((team_dict[team], pts))


new_list.sort()

""" Upto here. Need to start thinking about putting the 538 data and my scraped data into an append csv."""



df_output = pd.DataFrame(new_list, columns=['team', today])

df_output = df_output.drop(['team'], axis=1)

df_output = df_output.transpose()

df_output.to_csv('538.csv', mode='a', header=False)

print('\n 538 Scrape has been written to csv')







