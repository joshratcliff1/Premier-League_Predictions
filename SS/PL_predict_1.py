import pandas as pd
import numpy as np


''' https://fixturedownload.com/results/epl-2020 '''

# show complete records by changing rules
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Load the dataset into the dataframe
df = pd.read_csv('epl-2020-GMTStandardTime.csv')

# Split into results and fixtures
df_r = df[df['Result'].notna()]
df_f = df[df['Result'].isna()]


# Create Home and Away Result Columns
splits = df_r['Result'].str.split()
df_r['Home_Score'] = splits.str[0]
df_r['Away_Score'] = splits.str[2]

df_r['Home_Result'] = ['win' if x > y else 'loss' if y > x else 'draw'
                       for x,y in zip(df_r['Home_Score'],df_r['Away_Score'])]
df_r['Away_Result'] = ['win' if x > y else 'loss' if y > x else 'draw'
                       for x,y in zip(df_r['Away_Score'],df_r['Home_Score'])]

# Print dataframes for viewing
print(df_r)
print('---------------')
print(df_f)

# The set of stats that will be recorded for all teams
stats = {'Home_games': 0,
         'Away_games': 0,
         'Home_points': 0,
         'Away_points': 0,
         'Total_points': 0,
         'Game_mp': 0,
         'Home_mp': 0,}

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
    elif row['Home_Result'] == 'loss':
        teams[row['Home Team']]['Home_games'] += 1
        teams[row['Home Team']]['Home_points'] += 0
        teams[row['Away Team']]['Away_games'] += 1
        teams[row['Away Team']]['Away_points'] += 3
        teams[row['Away Team']]['Total_points'] += 3
    else:
        teams[row['Home Team']]['Home_games'] += 1
        teams[row['Home Team']]['Home_points'] += 1
        teams[row['Away Team']]['Away_games'] += 1
        teams[row['Away Team']]['Away_points'] += 1
        teams[row['Home Team']]['Total_points'] += 1
        teams[row['Away Team']]['Total_points'] += 1

# Calculate the Game multiplayer and home/away multiplier for each team
for team, stats in teams.items():
    stats['Game_mp'] = stats['Total_points'] / (stats['Home_games'] + stats['Away_games'])
    stats['Home_mp'] = stats['Home_points'] / stats['Home_games'] * stats['Away_games'] / stats['Away_points']

avg_points = 0

# Print stats for viewing
print("Current Standings after Fixtures")
for team, stats in teams.items():
    print(team, ': ', stats)
    avg_points += stats['Game_mp']

avg_points /= 10
print('\navg_points', avg_points)

# Update stats for fixtures
for index, row in df_r.iterrows():
    home_temp = teams[row['Home Team']]['Game_mp'] * teams[row['Home Team']]['Home_mp']
    away_temp = teams[row['Away Team']]['Game_mp'] / teams[row['Away Team']]['Home_mp']
    point_update_h = teams[row['Home Team']]['Game_mp'] * avg_points / (home_temp + away_temp)
    point_update_a = avg_points - point_update_h

    # Update Stats for Home team
    teams[row['Home Team']]['Home_games'] += 1
    teams[row['Home Team']]['Home_points'] += point_update_h
    teams[row['Home Team']]['Total_points'] += point_update_h
    # Update Stats for Away team
    teams[row['Away Team']]['Home_games'] += 1
    teams[row['Away Team']]['Home_points'] += point_update_a
    teams[row['Away Team']]['Total_points'] += point_update_a


# Print stats for viewing after all games
print("\nFinal Standings at end of Season")

result_list = []

for team, stats in teams.items():
    result_list.append((team, round(stats['Total_points'])))

result_list.sort(key=lambda x: x[1], reverse=True)

for item in result_list:
    print(item)