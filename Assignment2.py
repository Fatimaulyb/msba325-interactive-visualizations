# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Create a Streamlit app title
st.title("🚀 **Exploring the World of Largest Companies** 🌐")




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


# Visualization 4: Boxplot of Revenue Growth Distribution
st.header('Boxplot of Revenue Growth Distribution')

# Sidebar for filtering by industry
selected_industry = st.selectbox("Select Industry", ["All Industries"] + list(largest_companies['Industry'].unique()))

# Filter the data based on the selected industry
if selected_industry == "All Industries":
    filtered_data = largest_companies
else:
    filtered_data = largest_companies[largest_companies['Industry'] == selected_industry]

# Sidebar for filtering by company
st.sidebar.header("Filter Data")
selected_companies = st.sidebar.multiselect("Select Companies", filtered_data['Name'].unique())

# Apply filtering by company
if selected_companies:
    filtered_data = filtered_data[filtered_data['Name'].isin(selected_companies)]

st.plotly_chart(px.box(filtered_data, y='Revenue growth', title=f'Revenue Growth Distribution ({selected_industry})'))

# Description with the box
st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore the distribution of revenue growth with this boxplot while harnessing the power of filters.</p>
    <p style="font-size:16px;">Select an industry or specific companies using the filters to customize your analysis. The boxplot unveils typical growth, data spread, and potential outliers, allowing users to uncover financial insights tailored to their preferences.</p>
    </div>""",
    unsafe_allow_html=True
)






# Visualization 5: Treemap of Revenue Distribution by Industry
st.header('Revenue Distribution by Industry (Treemap)')
st.plotly_chart(px.treemap(largest_companies,
                           path=['Industry', 'Name'],
                           values='Revenue (USD millions)',
                           title='Revenue Distribution by Industry (Treemap)'))

st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore revenue distribution by industry using this treemap.</p>
    <p style="font-size:16px;">This treemap provides an insightful representation of revenue distribution by industry, offering a comprehensive view of how revenue is allocated across various sectors. In this visualization, each rectangle represents an industry, with the size of the rectangle corresponding to the industry's revenue proportion. The color-coding of the rectangles enhances the visual impact, making it easier to distinguish between different sectors. The treemap allows viewers to quickly identify the largest and smallest revenue contributors within the dataset, making it a powerful tool for assessing the relative significance of different industries to the overall revenue picture. Moreover, the hierarchical structure of the treemap can reveal subcategories within industries, providing even finer granularity in revenue analysis.</p>
    </div>""",
    unsafe_allow_html=True
)

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

st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore top companies across industries with this interactive bar plot.</p>
    <p style="font-size:16px;">With a user-friendly dropdown menu, users can select specific industries and instantly view the top companies that lead in each sector. The bar plot displays the companies as horizontal bars, with the length of each bar representing the company's relative performance within its respective industry. By selecting an industry from the dropdown menu, users can quickly identify the dominant players in that sector. This feature simplifies the process of tracking and comparing top performers, making it a valuable resource for investors, analysts, and decision-makers. The ability to toggle between industries provides a dynamic view of how different companies excel in their respective markets. This not only helps in identifying industry leaders but also supports informed decision-making, whether it's for investment opportunities, market analysis, or strategic partnerships.</p>
    </div>""",
    unsafe_allow_html=True
)





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
st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore employee distribution by headquarters with this interactive tool.</p>
    <p style="font-size:16px;">This interactive visualization introduces a multiselect box, allowing users to choose multiple company headquarters. It empowers users to explore the distribution of employees for companies headquartered in the selected locations. Notably, if no headquarters are chosen, the histogram will display the employee distributions for all headquarters. The importance of this tool lies in its ability to provide a tailored perspective on employee distribution, considering the geographic locations of company headquarters. By selecting specific headquarters, users can gain valuable insights into how employee numbers are spread across different regions or cities.</p>
    </div>""",
    unsafe_allow_html=True
)


# Title and description
st.title('Scatter Plot Matrix with Tooltips')
st.write("Explore relationships between variables with interactive tooltips.")

# Create an interactive scatter plot matrix
fig = px.scatter_matrix(largest_companies,
                        dimensions=["Revenue (USD millions)", "Revenue growth", "Employees"],
                        color="Industry",
                        title="Scatter Plot Matrix")

st.plotly_chart(fig)

st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore relationships between variables with this interactive Scatter Plot Matrix.</p>
    <p style="font-size:16px;">The figure visually displays relationships between key variables, such as Revenue (USD millions), Revenue growth, and Employees, in the dataset. Each point in the scatter plot matrix represents a company, and the points are color-coded by the industry to provide insights into the distribution and potential correlations between these variables. Users can interact with the plot by hovering over data points to see tooltips with additional information about each company.</p>
    </div>""",
    unsafe_allow_html=True
)

