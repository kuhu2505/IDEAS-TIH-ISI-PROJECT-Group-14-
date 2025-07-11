#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np


# In[14]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D

# Title
st.title("Electoral Analysis Dashboard - Constituency Wise Insights")

# Load data
file_path = file_path = "District-Profile.xlsx"
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

# Party Volatility (Standard Deviation of Vote %)
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

# Convert age to numeric for binning
df[age_col] = pd.to_numeric(df[age_col], errors='coerce')

# Create age group bins
bins = [0, 20, 30, 40, 50, 60, float('inf')]
labels = ['<20', '20-30', '30-40', '40-50', '50-60', '>60']
df['Age Group'] = pd.cut(df[age_col], bins=bins, labels=labels, right=False)

# 2D Scatter Plot with Age Groups
fig3 = px.scatter(df, x='Age Group', y=party_for_plot, color=gender_col,
                  title=f'{party_for_plot} vs Age Group Colored by {gender_col}',
                  labels={'Age Group': "Age Group", party_for_plot: "Vote %", gender_col: "Gender"})
st.plotly_chart(fig3)

# 3D Scatter Plot with Age Groups
st.subheader("3D Scatter: Age, Gender & Party Preference")

fig4 = px.scatter_3d(df, x='Age Group', y=gender_col, z=party_for_plot,
                     color=party_for_plot,
                     title="3D Scatter of Party Preference by Age Group and Gender",
                     labels={'Age Group': "Age Group", gender_col: "Gender Count", party_for_plot: "Vote %"})
st.plotly_chart(fig4)

