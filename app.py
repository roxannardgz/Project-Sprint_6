import streamlit as st
import pandas as pd
import plotly.express as px

# Import necessary data
vehicles_data = pd.read_csv('notebook/vehicles_clean.csv')

st.set_page_config(page_title='Vehicle Explorer', page_icon=':car:', layout="wide", initial_sidebar_state="auto", menu_items=None)

# Header -----------------------------------------------------
st.title("Vehicle Explorer")


with st.expander(('About this app')):
    st.markdown((
        '''
    Sprint 6: Software Development Tools - Tripleten
    
    This application is based on a dataset containing information about car sales advertisements.
    Use the controls in the sidebar to update the charts.
    '''
    ))


# Sidebar ----------------------------------------------------
st.sidebar.header('Select the features your interested in')

# Sidebar - year selection
# Get distinct values of 'model_year' and sort them 
distinct_years = sorted(vehicles_data['model_year'].unique(), reverse=True)

selected_year = st.sidebar.selectbox('Year', distinct_years)

# Sidebar - make selection
# Get distinct values of 'make' and sort them
distinct_make = sorted(vehicles_data['make'].unique())
selected_make = st.sidebar.multiselect('Make/Manufacturer', distinct_make, default=distinct_make)

# Sidebar - condition selection
# Create list with distunct values for condition
distinct_condition = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
selected_condition = st.sidebar.multiselect('Condition', distinct_condition, default=distinct_condition)

# Sidebar - transmission filter
automatic = st.sidebar.checkbox('Show only Automatic Transmission')

# Filter data based on selections
filtered_data_prev = vehicles_data[(vehicles_data['model_year']==selected_year) & (vehicles_data['make'].isin(selected_make)) & (vehicles_data['condition'].isin(selected_condition))]

# Apply filter for transmision
if automatic:
    filtered_data = filtered_data_prev[filtered_data_prev['transmission']=='automatic']
else:
    filtered_data = filtered_data_prev

# Body -------------------------------------------------------
hist_section, scatter_section = st.columns(2)
bars1_section, bars2_section, bars3_section = st.columns(3)

# Body - histogram
# Create histogram without outliers
lower_bound = filtered_data['price'].quantile(0.05)
upper_bound = filtered_data['price'].quantile(0.95)

vehicles_data_upd = filtered_data[(filtered_data['price'] < upper_bound) & (filtered_data['price'] > lower_bound)]

with hist_section:
    st.header('Distribution of Prices')
    st.markdown(f'Distribution by make for the **year {selected_year}**.')

    st.write(px.histogram(vehicles_data_upd, x='price', nbins=50))


# Body - scatterplot
with scatter_section:
    st.header('Days Listed vs Price')
    st.markdown(f'complete')

    st.write(px.scatter(vehicles_data_upd, x='price', y='days_listed',  hover_name='make', hover_data='condition', color='condition'))

# Body - fuel bars
# Create barchart fuel
by_fuel = filtered_data.groupby('fuel').size().reset_index(name='count')
by_fuel = by_fuel.sort_values(by='count').reset_index(drop=True)

bar_fuel = px.bar(by_fuel, x='fuel', y='count', width=300)

# Display barchart fuel
with bars1_section:
    st.header('Fuel')
    st.write(bar_fuel)


# Body - type bars
# Create barchart type
by_type = filtered_data.groupby('type').size().reset_index(name='count')
by_type = by_type.sort_values(by='count').reset_index(drop=True)
bar_type = px.bar(by_type, x='type', y='count', width=280)

# Display barchart type
with bars2_section:
    st.header('Type')
    st.write(bar_type)


# Body - color bars
# Create barchart color
by_color = filtered_data.groupby('paint_color').size().reset_index(name='count')
by_color = by_color.sort_values(by='count')
bar_color = px.bar(by_color, x='paint_color', y='count', width=280)

# Display barchart color
with bars3_section:
    st.header('Color')
    st.write(bar_color)
    
