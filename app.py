import streamlit as st
import pandas as pd
import numpy as np
import json
from pandas import json_normalize
import requests

# input week numbers
weeks = ['5', '6']

# eliminated owners
cut_owners = ['TheEvilNarwhal', 'reinbow']

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

if len(weeks) == 1:
    # print single week standings with bold title
    st.write('Week', weeks[0], 'Standings')
  
else:
    # print double week standings with bold title
    st.write('Weeks', weeks[0], '-', weeks[1], 'Standings')

# print rankings
final = rank_df[['rank', 'username', 'points']].sort_values(by='rank')

st.table(final)
