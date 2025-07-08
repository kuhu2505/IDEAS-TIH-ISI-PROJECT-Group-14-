#!/usr/bin/env python
# coding: utf-8

# In[44]:


import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np


# In[45]:


st.set_page_config(layout="wide")
st.title("🗳️ Electoral Performance Dashboard")

# Load metrics and original data
@st.cache_data
def load_data():
    metrics = pd.read_csv("D:/district_vote_metrics.csv")
    all_sheets = pd.read_excel("D:/District-Trend.xlsx", sheet_name=None)
    return metrics, all_sheets

metrics_df, data_dict = load_data()

# Sidebar filters
st.sidebar.header("🌟 Filter Options")
sheet_names = sorted(map(str, data_dict.keys()))
selected_ac = st.sidebar.selectbox("Select Constituency", sheet_names)

# Data for selected constituency
df = data_dict[selected_ac]
df = df.dropna(how='all').dropna(axis=1, how='all')
df_long = df.melt(id_vars=[df.columns[0]], var_name='Party-Year', value_name='VoteShare')
df_long[['Party', 'Year']] = df_long['Party-Year'].astype(str).str.extract(r'(.+)-(\d+)', expand=True)
df_long['VoteShare'] = pd.to_numeric(df_long['VoteShare'], errors='coerce')
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
df_long = df_long.dropna(subset=['VoteShare'])

party_options = sorted(df_long['Party'].dropna().unique())
selected_party = st.sidebar.selectbox("Select Party", party_options)
party_df = df_long[df_long['Party'] == selected_party]

# Metrics display
mean_vote = party_df['VoteShare'].mean()
volatility = party_df['VoteShare'].std()
st.metric("📊 Mean Vote Share (%)", f"{mean_vote:.2f}")
st.metric("📉 Volatility", f"{volatility:.2f}")

# Line Chart
st.subheader(f"📈 Vote Share Trend for {selected_party} in {selected_ac}")
fig = px.line(party_df, x="Year", y="VoteShare", markers=True, title="Vote Share Over Years")
st.plotly_chart(fig, use_container_width=True)

# Prediction Widget
st.subheader("📈 Vote Share Trend & Prediction")
if len(party_df) >= 2:
    model = LinearRegression()
    X = party_df['Year'].values.reshape(-1, 1)
    y = party_df['VoteShare'].values
    model.fit(X, y)

    future_year = st.slider("Select a future year to predict", min_value=int(party_df['Year'].min()) + 1, max_value=2030, value=2026)
    prediction = model.predict([[future_year]])[0]
    st.success(f"📌 Predicted Vote Share in {future_year}: {prediction:.2f}%")

    # Show trend line
    party_df_sorted = party_df.sort_values('Year')
    trend_line = model.predict(party_df_sorted['Year'].values.reshape(-1, 1))
    party_df_sorted['Trend'] = trend_line
    fig_pred = px.line(party_df_sorted, x="Year", y=["VoteShare", "Trend"], markers=True, title="Vote Share & Trend Line")
    st.plotly_chart(fig_pred, use_container_width=True)
else:
    st.warning("Need at least 2 data points to forecast.")

# Raw data view
with st.expander("🔍 View Raw Data"):
    st.dataframe(party_df)

# Party Comparison Table
st.subheader("📊 Party Comparison Across Constituencies")
selected_metric = st.selectbox("Choose Metric", ["MeanVoteShare", "Volatility"])
comparison_df = metrics_df.pivot(index='Constituency', columns='Party', values=selected_metric)
st.dataframe(comparison_df.style.format("{:.2f}"))

# Volatility Heatmap
st.subheader("🔥 Volatility Heatmap by Constituency and Party")
vol_df = metrics_df.pivot(index='Constituency', columns='Party', values='Volatility')
fig2, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(vol_df, annot=True, cmap="YlOrRd", fmt=".2f", ax=ax)
st.pyplot(fig2)

# Export options
st.sidebar.subheader("📄 Export Data")
excel_download = metrics_df.to_excel("D:/metrics_export.xlsx", index=False)
with open("D:/metrics_export.xlsx", "rb") as f:
    st.sidebar.download_button("Download Metrics as Excel", f, file_name="metrics_export.xlsx")

csv = metrics_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download CSV", csv, file_name="metrics_export.csv", mime='text/csv')


# In[ ]:




