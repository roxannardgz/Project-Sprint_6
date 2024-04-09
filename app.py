import streamlit as st
import pandas as pd
import plotly.express as px

# Import necessary data - (data after changing data types, adding new columns and filling null values)
vehicles_data = pd.read_csv('vehicles_clean.csv')

st.set_page_config(page_title='Vehicle Explorer', page_icon=':car:', layout="wide", initial_sidebar_state="auto", menu_items=None)

# Header -----------------------------------------------------
st.title("Vehicle Data Explorer")


with st.expander(('About this app.')):
    st.markdown((
        '''
    Sprint 6: Software Development Tools - Tripleten
    
    This application is based on a dataset containing information about car sales advertisements.
    Use the controls in the sidebar to update the charts.
    '''
    ))


# Sidebar ----------------------------------------------------
st.sidebar.header("Select the features you're interested in:")

# Sidebar - year selection
# Get distinct values of 'model_year' and sort them 
distinct_years = sorted(vehicles_data['model_year'].unique(), reverse=True)

selected_year = st.sidebar.selectbox('Year', distinct_years)

# Sidebar - make selection
# Get distinct values of 'make' and sort them
distinct_make = sorted(vehicles_data['make'].unique())
selected_make = st.sidebar.multiselect('Make/Manufacturer', distinct_make, default=distinct_make)

# Sidebar - condition selection
# Create list with distinct values of condition
distinct_condition = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
selected_condition = st.sidebar.multiselect('Condition', distinct_condition, default=distinct_condition)

# Sidebar - transmission filter
automatic = st.sidebar.checkbox('Show only Automatic Transmission')


# Filter data based on selections
filtered_data_prev = vehicles_data[(vehicles_data['model_year']==selected_year) & (vehicles_data['make'].isin(selected_make)) & (vehicles_data['condition'].isin(selected_condition))]

# Apply filter for transmision
if automatic:
    filtered_data = filtered_data_prev[filtered_data_prev['transmission']=='automatic']
    selected_transmission = ['automatic']
else:
    filtered_data = filtered_data_prev
    selected_transmission = ['automatic', 'mechanic']

# Selected Make and Condition
make_list = ', '.join(selected_make)
condition_list = ', '.join(selected_condition)
transmission_list = ', '.join(selected_transmission)


# Body -------------------------------------------------------
#Body structure
hist_section, scatter_section = st.columns(2,gap='medium')
bars1_section, bars2_section, bars3_section = st.columns(3)
bottom_container = st.container(border=True)


# Body - histogram
# Create histogram without outliers
lower_bound = filtered_data['price'].quantile(0.05)
upper_bound = filtered_data['price'].quantile(0.95)

vehicles_data_upd = filtered_data[(filtered_data['price'] < upper_bound) & (filtered_data['price'] > lower_bound)]

with hist_section:
    st.header('Distribution of Prices')

    hist = px.histogram(vehicles_data_upd, x='price', nbins=50, width=450, labels={'price': 'Price ($)'})
    hist.update_yaxes(title=None)

    st.write(hist)


# Body - scatterplot
with scatter_section:
    st.header('Days Listed vs Price')

    scatter = px.scatter(vehicles_data_upd, x='price', y='days_listed',  hover_name='make', hover_data='condition', color='condition', width=500, labels={'price': 'Price ($)', 'days_listed': 'Days Listed'})
    scatter.update_layout(legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0.01))


    st.write(scatter)

# Body - fuel bars
# Create barchart fuel
by_fuel = filtered_data.groupby('fuel').size().reset_index(name='count')
by_fuel = by_fuel.sort_values(by='count', ascending=False).reset_index(drop=True)

bar_fuel = px.bar(by_fuel, x='fuel', y='count', width=300, labels={'fuel': 'Fuel'})
bar_fuel.update_yaxes(title=None)

# Display barchart fuel
with bars1_section:
    st.header('Fuel')
    st.write(bar_fuel)


# Body - type bars
# Create barchart type
by_type = filtered_data.groupby('type').size().reset_index(name='count')
by_type = by_type.sort_values(by='count', ascending=False).reset_index(drop=True)

bar_type = px.bar(by_type, x='type', y='count', width=280, labels={'type': 'Type'})
bar_type.update_yaxes(title=None)

# Display barchart type
with bars2_section:
    st.header('Type')
    st.write(bar_type)


# Body - color bars
# Create barchart color
by_color = filtered_data.groupby('paint_color').size().reset_index(name='count')
by_color = by_color.sort_values(by='count', ascending=False)

bar_color = px.bar(by_color, x='paint_color', y='count', width=280, labels={'paint_color': 'Color'})
bar_color.update_yaxes(title=None)

# Display barchart color
with bars3_section:
    st.header('Color')
    st.write(bar_color)


# Bottom Containes - Selected parameters
with bottom_container:
    st.markdown((
            f'''
        ##### **Showing data for:**
        
        **Year:** {selected_year}
        
        **Make/Manufacturer:** {make_list}
        
        **Condition:** {condition_list}

        **Transmission:** {transmission_list}
        '''
        ))
