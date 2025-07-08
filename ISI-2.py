#!/usr/bin/env python
# coding: utf-8

# In[51]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Set up Streamlit page
st.set_page_config(page_title="Election Dashboard", layout="wide")
st.title("🗳️ Election Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("D:/District-Trend.xlsx", sheet_name=None)
    return df

data_dict = load_data()

# Sidebar filters
st.sidebar.header("📌 Filter Options")
constituencies = list(data_dict.keys())
selected_ac = st.sidebar.selectbox("Select Constituency", constituencies)

# Prepare the data
raw_df = data_dict[selected_ac]
raw_df = raw_df.dropna(how='all').dropna(axis=1, how='all')

# Melt data into long format
df_long = raw_df.melt(id_vars=[raw_df.columns[0]], var_name="Party-Year", value_name="VoteShare")
df_long[['Party', 'Year']] = df_long['Party-Year'].astype(str).str.extract(r'(.+)-(\d+)', expand=True)
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
df_long['VoteShare'] = pd.to_numeric(df_long['VoteShare'], errors='coerce')
df_long = df_long.dropna(subset=['VoteShare'])

# Party selector
party_options = sorted(df_long['Party'].dropna().unique())
selected_party = st.sidebar.selectbox("Select Party", party_options)
party_df = df_long[df_long['Party'] == selected_party]

# Line chart
st.subheader(f"📈 Vote Share Over Time for {selected_party} in {selected_ac}")
fig_line = px.line(party_df, x='Year', y='VoteShare', title="Vote Share Trend", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# Histogram
st.subheader(f"📊 Vote Share Histogram for {selected_party}")
fig_hist = px.histogram(party_df, x='VoteShare', nbins=10, title="Vote Share Distribution")
st.plotly_chart(fig_hist, use_container_width=True)

# Winner by year
st.subheader(f"🏆 Yearly Winner in {selected_ac}")
winner_df = df_long.groupby(['Year', 'Party'])['VoteShare'].sum().reset_index()
winner_idx = winner_df.groupby('Year')['VoteShare'].idxmax()
winner_table = winner_df.loc[winner_idx].sort_values('Year')
st.dataframe(winner_table.reset_index(drop=True))

# Raw data
with st.expander("🔍 View Raw Data"):
    st.dataframe(df_long)


# In[ ]:




