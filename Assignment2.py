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
    <p style="font-size:16px;">Select an industry or specific companies using the filters to customize your analysis. The boxplot unveils typical growth, data spread, and potential outliers, allowing you to uncover financial insights tailored to your preferences.</p>
    </div>""",
    unsafe_allow_html=True
)





# Visualization 5: Treemap of Revenue Distribution by Industry
st.header('Revenue Distribution by Industry (Treemap)')

# Clear widget state to prevent DuplicateWidgetID error
st.experimental_rerun()

# Sidebar for filtering by industry
selected_industry = st.selectbox("Select Industry", ["All Industries"] + list(largest_companies['Industry'].unique()))

# Filter the data based on the selected industry
if selected_industry == "All Industries":
    filtered_data = largest_companies
else:
    filtered_data = largest_companies[largest_companies['Industry'] == selected_industry]

st.plotly_chart(px.treemap(filtered_data,
                           path=['Industry', 'Name'],
                           values='Revenue (USD millions)',
                           title=f'Revenue Distribution by Industry ({selected_industry})'))

# Description with the box
st.markdown(
    """<div style="background-color:#e8f7f7;padding:20px;border-radius:10px">
    <p style="font-size:16px;color:#0d4f6c;">Explore revenue distribution by industry using this interactive treemap.</p>
    <p style="font-size:16px;">Select an industry from the dropdown to focus on specific sectors. Each rectangle in the treemap represents an industry, and its size corresponds to the revenue proportion. Color-coding enhances visual impact and distinguishes between sectors. This tool helps identify the largest and smallest revenue contributors and assess the relative significance of industries. Explore hierarchical structures for finer granularity in revenue analysis.</p>
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

# Title and description
st.title('Scatter Plot Matrix with Tooltips')
st.write("Explore relationships between variables with interactive tooltips.")

# Create an interactive scatter plot matrix
fig = px.scatter_matrix(largest_companies,
                        dimensions=["Revenue (USD millions)", "Revenue growth", "Employees"],
                        color="Industry",
                        title="Scatter Plot Matrix")

st.plotly_chart(fig)

st.write("The figure is a scatter plot matrix that visually displays relationships between key variables, such as Revenue (USD millions), Revenue growth, and Employees, in the dataset. Each point in the scatter plot matrix represents a company, and the points are color-coded by the industry to provide insights into the distribution and potential correlations between these variables. Users can interact with the plot by hovering over data points to see tooltips with additional information about each company.")
