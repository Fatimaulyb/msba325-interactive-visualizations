# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px

# Create a Streamlit app title
st.title('Largest Companies Visualization')
st.markdown("---")

# Section 1: Data Cleaning
st.header('Data Cleaning')
st.write("Cleaning and preprocessing the dataset for analysis.")

# Load the dataset (assuming 'Largest_Companies.csv' is in your Colab environment)
largest_companies = pd.read_csv('Largest_Companies.csv')

missing_values = largest_companies.isnull().sum()
largest_companies.dropna(inplace=True)
duplicate_rows = largest_companies.duplicated()
largest_companies.drop_duplicates(keep='first', inplace=True)
largest_companies['Revenue (USD millions)'] = largest_companies['Revenue (USD millions)'].str.replace(',', '').astype(float)

# Section 2: Visualizations

## Visualization 1: Boxplot of Distribution of Revenue Growth
st.header('Distribution of Revenue Growth')
st.plotly_chart(px.box(largest_companies, y='Revenue growth', title='Distribution of Revenue Growth'))

st.write("The boxplot illustrating the distribution of revenue growth holds a pivotal role in financial analysis and strategic decision-making. Its importance stems from its ability to provide a concise yet comprehensive overview of key characteristics within the revenue growth dataset...")

## Visualization 2: Treemap of Revenue Distribution by Industry
st.header('Revenue Distribution by Industry (Treemap)')
st.plotly_chart(px.treemap(largest_companies,
                           path=['Industry', 'Name'],
                           values='Revenue (USD millions)',
                           title='Revenue Distribution by Industry (Treemap)'))

st.write("This treemap provides an insightful representation of revenue distribution by industry, offering a comprehensive view of how revenue is allocated across various sectors...")

# Interaction 1: Dropdown Selection for Industries with a Bar Plot
st.header('Top 10 Companies by Revenue in Selected Industry')
selected_industry = st.selectbox("Select an Industry", largest_companies["Industry"].unique())
filtered_data = largest_companies[largest_companies["Industry"] == selected_industry]
top_companies_in_industry = filtered_data.nlargest(10, 'Revenue (USD millions')
st.plotly_chart(px.bar(top_companies_in_industry,
                       x='Revenue (USD millions',
                       y='Name',
                       title=f"Top 10 Companies in {selected_industry} by Revenue",
                       orientation='h'))

st.write("This interactive bar plot is a powerful tool for exploring and comparing the top companies within various industries...")

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

st.write("This interactive visualization introduces a multiselect box, allowing users to choose multiple company headquarters...")

# Section 3: Scatter Plot Matrix
st.header('Scatter Plot Matrix with Tooltips')
st.write("Explore relationships between variables with interactive tooltips.")
fig = px.scatter_matrix(largest_companies,
                        dimensions=["Revenue (USD millions)", "Revenue growth", "Employees"],
                        color="Industry",
                        title="Scatter Plot Matrix")
st.plotly_chart(fig)

st.write("The figure is a scatter plot matrix that visually displays relationships between key variables, such as Revenue (USD millions), Revenue growth, and Employees, in the dataset...")
