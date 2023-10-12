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
# Sidebar for filtering
st.sidebar.header("Filter Data")
selected_companies = st.sidebar.multiselect("Select Companies", largest_companies['Name'].unique())

st.write("The boxplot illustrating the distribution of revenue growth holds a pivotal role in financial analysis and strategic decision-making. Its importance stems from its ability to provide a concise yet comprehensive overview of key characteristics within the revenue growth dataset. By presenting statistics such as the median (indicating the typical growth rate), quartiles (depicting the spread of data), and potential outliers (highlighting extreme values), the boxplot simplifies complex financial data. This simplification is invaluable for stakeholders and decision-makers, as it allows for quick and accurate data interpretation.")

# Visualization 5: Treemap of Revenue Distribution by Industry
st.header('Revenue Distribution by Industry (Treemap)')
st.plotly_chart(px.treemap(largest_companies,
                           path=['Industry', 'Name'],
                           values='Revenue (USD millions)',
                           title='Revenue Distribution by Industry (Treemap)'))

st.write("This treemap provides an insightful representation of revenue distribution by industry, offering a comprehensive view of how revenue is allocated across various sectors. In this visualization, each rectangle represents an industry, with the size of the rectangle corresponding to the industry's revenue proportion. The color-coding of the rectangles enhances the visual impact, making it easier to distinguish between different sectors.The treemap allows viewers to quickly identify the largest and smallest revenue contributors within the dataset, making it a powerful tool for assessing the relative significance of different industries to the overall revenue picture. Moreover, the hierarchical structure of the treemap can reveal subcategories within industries, providing even finer granularity in revenue analysis.")

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

st.write("This interactive bar plot is a powerful tool for exploring and comparing the top companies within various industries. With a user-friendly dropdown menu, users can select specific industries and instantly view the top companies that lead in each sector. The bar plot displays the companies as horizontal bars, with the length of each bar representing the company's relative performance within its respective industry. By selecting an industry from the dropdown menu, users can quickly identify the dominant players in that sector. This feature simplifies the process of tracking and comparing top performers, making it a valuable resource for investors, analysts, and decision-makers. The ability to toggle between industries provides a dynamic view of how different companies excel in their respective markets. This not only helps in identifying industry leaders but also supports informed decision-making, whether it's for investment opportunities, market analysis, or strategic partnerships.")



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
st.write("This interactive visualization introduces a multiselect box, allowing users to choose multiple company headquarters. It empowers users to explore the distribution of employees for companies headquartered in the selected locations. Notably, if no headquarters are chosen, the histogram will display the employee distributions for all headquarters. The importance of this tool lies in its ability to provide a tailored perspective on employee distribution, considering the geographic locations of company headquarters. By selecting specific headquarters, users can gain valuable insights into how employee numbers are spread across different regions or cities.")
