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

