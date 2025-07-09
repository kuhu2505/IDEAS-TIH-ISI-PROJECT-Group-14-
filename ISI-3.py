#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D

# Title
st.title("Electoral Analysis Dashboard - Constituency Wise Insights")

# Load data
file_path = "District-Profile.xlsx"
sheet_names = pd.ExcelFile(file_path).sheet_names
selected_sheet = st.sidebar.selectbox("Select Constituency Sheet", sheet_names)
df = pd.read_excel(file_path, sheet_name=selected_sheet)

st.subheader(f"Data Preview: {selected_sheet}")
st.dataframe(df.head())

# Clean and preprocess data
df = df.dropna()
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

# Correlation heatmap
st.subheader("Correlation Heatmap (Numeric Variables)")
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Volatility (Standard deviation of party vote %)
st.subheader("Party Volatility (Standard Deviation of Vote %)")
party_columns = [col for col in df.columns if '%' in col or 'Vote' in col]

if party_columns:
    vol_df = df[party_columns].std().reset_index()
    vol_df.columns = ['Party', 'Volatility']

    fig2 = px.bar(vol_df, x='Party', y='Volatility', title='Volatility by Party')
    st.plotly_chart(fig2)
else:
    st.warning("No party percentage columns found to compute volatility.")

# Age vs Gender vs Party Preference
st.subheader("2D Scatter: Age vs Vote % per Party")
age_col = st.selectbox("Select Age Column", [col for col in df.columns if 'AGE' in col.upper()])
gender_col = st.selectbox("Select Gender Column", [col for col in df.columns if 'MALE' in col.upper() or 'FEMALE' in col.upper()])
party_for_plot = st.selectbox("Select Party Vote % Column", party_columns)

fig3 = px.scatter(df, x=age_col, y=party_for_plot, color=gender_col,
                  title=f'{party_for_plot} vs {age_col} Colored by {gender_col}',
                  labels={age_col: "Average Age", party_for_plot: "Vote %", gender_col: "Gender"})
st.plotly_chart(fig3)

# 3D Scatter Plot
st.subheader("3D Scatter: Age, Gender & Party Preference")

fig4 = px.scatter_3d(df, x=age_col, y=gender_col, z=party_for_plot,
                     color=party_for_plot,
                     title="3D Scatter of Party Preference by Age and Gender",
                     labels={age_col: "Age", gender_col: "Gender Count", party_for_plot: "Vote %"})
st.plotly_chart(fig4)


# In[ ]:




