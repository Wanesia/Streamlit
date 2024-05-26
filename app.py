import streamlit as st
import pandas as pd
import altair as alt
from utils.data_preprocessor import load_data

data = load_data()

# Group by year and sum total sales for each year
yearly_sales = data.groupby(data['year'].dt.year).agg({'total sales new': 'sum', 'total sales used': 'sum'}).reset_index()

# Create Streamlit app title
st.title("Car Data by Year")

if data.empty:
    st.warning("No data to display. Please check your data file.")
else:

    line_chart_data = yearly_sales[['year', 'total sales new', 'total sales used']]

    line_chart_data = line_chart_data.melt('year', var_name='Sales Type', value_name='Sales')

    # Rename the sales types for the legend
    line_chart_data['Sales Type'] = line_chart_data['Sales Type'].replace({
        'total sales new': 'New Sales',
        'total sales used': 'Used Sales'
    })

    line_chart = alt.Chart(line_chart_data).mark_line().encode(
        x='year:O',
        y='Sales:Q',
        color='Sales Type:N'
    ).properties(
        title='Total Sales of New and Used Cars Over the Years'
    ).interactive()

    # Display the line chart in Streamlit
    st.altair_chart(line_chart, use_container_width=True)

# Prepare data for the bar chart
bar_chart_data = yearly_sales[['year', 'total sales new', 'total sales used']]
bar_chart_data = bar_chart_data.melt('year', var_name='Sales Type', value_name='Sales')

# Rename the sales types for the legend
bar_chart_data['Sales Type'] = bar_chart_data['Sales Type'].replace({
    'total sales new': 'New Sales',
    'total sales used': 'Used Sales'
})

bar_chart = alt.Chart(bar_chart_data).mark_bar().encode(
    x='year:O',
    y='Sales:Q',
    color='Sales Type:N'
).properties(
    title='Total Monetary Value',
    width=600,
    height=400
).interactive()

st.altair_chart(bar_chart, use_container_width=True)

# Format columns for proper display
data_display = data.copy()
data_display['year'] = pd.to_datetime(data_display['year'], format='%Y').dt.year.astype(str)
data_display['month'] = pd.to_datetime(data_display['month'], format='%b').dt.strftime('%B')

# Print scrollable data
with st.expander("View All Data"):
    st.write(data_display)