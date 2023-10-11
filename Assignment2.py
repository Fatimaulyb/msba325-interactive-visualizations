# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Create a Streamlit app title
st.title('Largest Companies Visualization')

# Load the dataset (assuming 'Largest_Companies.csv' is in your Colab environment)
largest_companies = pd.read_csv('Largest_Companies.csv')

# Cleaning the Dataset
missing_values = largest_companies.isnull().sum()
largest_companies.dropna(inplace=True)
duplicate_rows = largest_companies.duplicated()
largest_companies.drop_duplicates(keep='first', inplace=True)
largest_companies['Revenue (USD millions)'] = largest_companies['Revenue (USD millions)'].str.replace(',', '').astype(float)

# Creating a Mini Dataframe for visualizations
top_10_revenue = largest_companies.sort_values(by='Revenue (USD millions)', ascending=False).head(10)

# Visualization 4: Barplot of Distribution of Revenue Growth
st.header('Distribution of Revenue Growth')
st.plotly_chart(px.box(largest_companies, y='Revenue growth', title='Distribution of Revenue Growth'))

# Visualization 5: Treemap of Revenue Distribution by Industry
st.header('Revenue Distribution by Industry (Treemap)')
st.plotly_chart(px.treemap(largest_companies,
                           path=['Industry', 'Name'],
                           values='Revenue (USD millions)',
                           title='Revenue Distribution by Industry (Treemap)'))

# Interaction 1: Dropdown Selection for Industries with a Bar Plot
st.header('Top 10 Companies by Revenue in Selected Industry')
selected_industry = st.selectbox("Select an Industry", largest_companies["Industry"].unique())
filtered_data = largest_companies[largest_companies["Industry"] == selected_industry]
top_companies_in_industry = filtered_data.nlargest(10, 'Revenue (USD millions)')
st.plotly_chart(px.bar(top_companies_in_industry,
                       x='Revenue (USD millions)',
                       y='Name',
                       title=f"Top 10 Companies in {selected_industry} by Revenue",
                       orientation='h'))

st.write("Here is a dropdown menu where users can select an industry and view the top 10 companies in that industry by revenue in a horizontal bar plot")

# Interaction 2: Distribution of Employees by Headquarters
st.header('Distribution of Employees by Headquarters')
selected_headquarters = st.multiselect("Select Headquarters", largest_companies["Headquarters"].unique())
if not selected_headquarters:
    selected_headquarters = largest_companies["Headquarters"].unique()
filtered_by_headquarters = largest_companies[largest_companies["Headquarters"].isin(selected_headquarters)]
st.plotly_chart(px.histogram(filtered_by_headquarters,
                             x='Employees',
                             color='Headquarters',
                             title='Distribution of Employees by Headquarters',
                             nbins=30))
st.write("And here is a multiselect box where users can select multiple company headquarters and view the distribution of employees for companies headquartered in the selected locations. If no headquarters are selected, the histogram will show distributions for all headquarters.")
