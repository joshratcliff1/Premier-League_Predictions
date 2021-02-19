import pandas as pd
from datetime import datetime

now = datetime.now() # current date and time
today = now.strftime('%Y-%m-%d')

''' https://fixturedownload.com/results/epl-2020 '''

# show complete records by changing rules
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def triangle(n):
    """Calculates the triangle number. ie. 1+2+...+n"""
    return sum([x for x in range(n+1)])



# Scrape tables from the webpage
dfs = pd.read_html('https://fixturedownload.com/results/epl-2020')

# Load the dataset into the dataframe
df = dfs[0]

# Split into results and fixtures
df_r = df.copy()[df['Result'].str.contains(" - ")]
df_f = df.copy()[~df['Result'].str.contains(" - ")]

# Create Home and Away Result Columns
splits = df_r['Result'].str.split()
df_r['Home_Score'] = splits.str[0]
df_r['Away_Score'] = splits.str[2]

df_r['Home_Result'] = ['win' if x > y else 'loss' if y > x else 'draw'
                       for x,y in zip(df_r['Home_Score'],df_r['Away_Score'])]
df_r['Away_Result'] = ['win' if x > y else 'loss' if y > x else 'draw'
                       for x,y in zip(df_r['Away_Score'],df_r['Home_Score'])]

# Print dataframes for viewing
# print(df_r)
# print('---------------')
# print(df_f)

# The set of stats that will be recorded for all teams
stats = {'Home_games': 0,
         'Away_games': 0,
         'Home_points': 0,
         'Away_points': 0,
         'Total_points': 0,
         'Game_mp': 0,
         'Home_mp': 0,
         'Away_mp': 0,
         'H_form_mp': 0,
         'A_form_mp': 0,
         'Home_form': 0,
         'Away_form': 0}

# Each of the teams as key to a dictionary holding their respective stats
teams = {'Arsenal': stats.copy(),
         'Aston Villa': stats.copy(),
         'Brighton': stats.copy(),
         'Burnley': stats.copy(),
         'Chelsea': stats.copy(),
         'Crystal Palace': stats.copy(),
         'Everton': stats.copy(),
         'Fulham': stats.copy(),
         'Leeds': stats.copy(),
         'Leicester': stats.copy(),
         'Liverpool': stats.copy(),
         'Newcastle': stats.copy(),
         'Man City': stats.copy(),
         'Man Utd': stats.copy(),
         'Sheffield Utd': stats.copy(),
         'Southampton': stats.copy(),
         'Spurs': stats.copy(),
         'West Brom': stats.copy(),
         'West Ham': stats.copy(),
         'Wolves': stats.copy()}

# Update the stats as per the results dataframe
for index, row in df_r.iterrows():
    if row['Home_Result'] == 'win':
        teams[row['Home Team']]['Home_games'] += 1
        teams[row['Home Team']]['Home_points'] += 3
        teams[row['Away Team']]['Away_games'] += 1
        teams[row['Away Team']]['Away_points'] += 0
        teams[row['Home Team']]['Total_points'] += 3
        teams[row['Home Team']]['Home_form'] += teams[row['Home Team']]['Home_games'] * 3   # Home Form
    elif row['Home_Result'] == 'loss':
        teams[row['Home Team']]['Home_games'] += 1
        teams[row['Home Team']]['Home_points'] += 0
        teams[row['Away Team']]['Away_games'] += 1
        teams[row['Away Team']]['Away_points'] += 3
        teams[row['Away Team']]['Total_points'] += 3
        teams[row['Away Team']]['Away_form'] += teams[row['Away Team']]['Away_games'] * 3   # Away Form
    else:
        teams[row['Home Team']]['Home_games'] += 1
        teams[row['Home Team']]['Home_points'] += 1
        teams[row['Away Team']]['Away_games'] += 1
        teams[row['Away Team']]['Away_points'] += 1
        teams[row['Home Team']]['Total_points'] += 1
        teams[row['Away Team']]['Total_points'] += 1
        teams[row['Home Team']]['Home_form'] += teams[row['Home Team']]['Home_games'] * 1   # Home Form
        teams[row['Away Team']]['Away_form'] += teams[row['Away Team']]['Away_games'] * 1   # Away Form

# Calculate the Game, home/away and form multipliers for each team
for team, stats in teams.items():
    stats['Game_mp'] = stats['Total_points'] / (stats['Home_games'] + stats['Away_games'])
    stats['Home_mp'] = stats['Home_points'] / stats['Home_games']
    stats['Away_mp'] = stats['Away_points'] / stats['Away_games']
    stats['H_form_mp'] = stats['Home_form'] * stats['Home_games'] / triangle(stats['Home_games']) / stats['Home_points']
    stats['A_form_mp'] = stats['Away_form'] * stats['Away_games'] / triangle(stats['Away_games']) / stats['Away_points']

avg_points = 0

# Print stats for viewing
for team, stats in teams.items():
    # print(team, ': ', stats)
    avg_points += stats['Game_mp']

# This calculates the average points per game for the season
avg_points /= 10

# Update stats for fixtures
for index, row in df_f.iterrows():
    home_temp = 0.5 * teams[row['Home Team']]['H_form_mp'] * (
                      teams[row['Home Team']]['Game_mp'] + teams[row['Home Team']]['Home_mp'])
    away_temp = 0.5 * teams[row['Home Team']]['H_form_mp'] * (
                      teams[row['Away Team']]['Game_mp'] + teams[row['Away Team']]['Away_mp'])
    point_update_h = teams[row['Home Team']]['Game_mp'] * avg_points / (home_temp + away_temp)
    # print('point_update_h: ', point_update_h)
    point_update_a = avg_points - point_update_h
    # print('point_update_a: ', point_update_a)

    # Update Stats for Home team
    teams[row['Home Team']]['Home_games'] += 1
    teams[row['Home Team']]['Home_points'] += point_update_h
    teams[row['Home Team']]['Total_points'] += point_update_h
    # Update Stats for Away team
    teams[row['Away Team']]['Away_games'] += 1
    teams[row['Away Team']]['Away_points'] += point_update_a
    teams[row['Away Team']]['Total_points'] += point_update_a

result_list = []

for team, stats in teams.items():
    result_list.append((team, round(stats['Total_points'])))

print('PL predictions on ', today, '\n')

result_list.sort(key = lambda x: x[1], reverse=True)

for team, pts in result_list:
    print(team, pts)

result_list.sort()

df_output = pd.DataFrame(result_list, columns=['team', today])

df_output = df_output.drop(['team'], axis=1)

df_output = df_output.transpose()

df_output.to_csv('predict.csv', mode='a', header=False)

print('\n PL Predictions have been written to csv')