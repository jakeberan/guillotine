import streamlit as st
import pandas as pd
import numpy as np
import json
from pandas import json_normalize
import requests

# title
st.header('Cedarburg Guillotine')

# return week slider
week_tuple = st.slider('Select Week',
                   value=[7,8], 
                   min_value = 1,
                   max_value = 18)

st.write('Weeks Selected:', week_tuple)

# input week numbers
weeks = ['5', '6']

weeks = [str(i) for i in range(week_tuple[0], week_tuple[1] + 1)]

# eliminated owners
# cut_owners = ['TheEvilNarwhal', 'reinbow']
cut_owners = []

# grab owner mapping
guill_owners = pd.read_csv('guillotine_owners.csv')

# grab sleeper league id
league_id = '1004524946262958080'

# initialize merged_df
merged_df = pd.DataFrame()

# grab weekly data and aggrergate into df
for week in weeks:

    # grab weekly scoring from Sleeper API
    df = pd.DataFrame(requests.get('https://api.sleeper.app/v1/league/' + league_id + '/matchups/' + week + '').json())

    # merge on pick_by to grab owner names
    df = pd.merge(df, guill_owners, 
                    on='roster_id', 
                    how='left')
    # add week column
    df['week'] = week

    # add weekly data to merged df
    merged_df = pd.concat([merged_df, df[['username', 'points', 'week']]], ignore_index=True)

# summarize standings, remove cut owners, and add rank column
rank_df = merged_df[~merged_df.username.isin(cut_owners)].groupby('username')['points'].sum().reset_index()
rank_df['rank'] = rank_df['points'].rank(ascending=False).astype(int)

# if len(weeks) == 1:
#     # print single week standings with bold title
#     st.subheader('Week', weeks[0], 'Standings')
  
# else:
#     # print double week standings with bold title
#     st.subheader('Weeks', weeks[0], '-', weeks[1], 'Standings')

st.subheader('Standings')

# print rankings
final = rank_df[['rank', 'username', 'points']].sort_values(by='rank')

st.table(final[ final['points'] > 0])



# # faab 
# st.subheader('FAAB Spend by Week')

# # Function to extract the 'waiver_bid' value from the 'settings' dictionary
# def extract_waiver_bid(settings):
#     return settings['waiver_bid']

# # Function to extract the first key from the 'adds' dictionary
# def extract_first_key(adds):
#     return next(iter(adds))

# # grab players data
# players = pd.DataFrame(requests.get('https://api.sleeper.app/v1/players/nfl').json()).T

# # reset index player_id and assign to 'player_id' column
# players.rename(columns={'index': 'player_id'}, inplace=True)

# # return players
# players = players[['player_id', 'full_name', 'position', 'team']]

# # initialize merged_df
# faab_df = pd.DataFrame()

# # create a list of all weeks
# all_weeks =  [str(i) for i in range(1, 18)]

# # grab weekly data and aggrergate into df
# for week in all_weeks:
#     try:
#         # grab weekly scoring from Sleeper API
#         df = pd.DataFrame(requests.get('https://api.sleeper.app/v1/league/' + league_id + '/transactions/' + week + '').json())

#         df = df [ (df['status'] == 'complete') &
#             (df['type'] == 'waiver')
#             ]

#         # Add a new column 'faab' with the extracted 'waiver_bid' values
#         df['faab'] = df['settings'].apply(lambda x: extract_waiver_bid(x))

#         # Add a new column 'player_id' with the extracted 'adds' keys
#         df['player_id'] = df['adds'].apply(lambda x: extract_first_key(x))

#         # grab roster id from list
#         df['roster_id'] = df['roster_ids'].apply(lambda x: x[0])

#         # merge on pick_by to grab owner names
#         df = pd.merge(df, guill_owners, 
#                         on='roster_id', 
#                         how='left')
        
#         df = pd.merge(df, players, 
#                     on='player_id', 
#                     how='left')
#         # add week column
#         df['week'] = week

#         # add weekly data to merged df
#         faab_df = pd.concat([faab_df, df[['full_name', 'position', 'team', 'username', 'faab', 'week']]], ignore_index=True)

#     except KeyError:
#         continue

# st.table(faab_df [faab_df ['faab'] > 0].sort_values(by=['week','faab']))


