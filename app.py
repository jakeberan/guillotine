import streamlit as st
import pandas as pd
import numpy as np

url_link = "https://www.fantasypros.com/nfl/adp/overall.php"
fpros = pd.read_html(url_link)[0]

st.table(fpros)
