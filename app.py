import altair as alt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st
from vega_datasets import data

# Loading relevant data
counties = alt.topo_feature(data.us_10m.url, 'counties')
states = alt.topo_feature(data.us_10m.url, feature='states')
state_data = pd.read_csv('COVID19_state.csv')
counties_data = pd.read_csv('us-counties.csv')
counties_data = counties_data.sample(n=4999)

# Choropleth generating function
# topo is the feature the choropleth is focusing on, like either states or counties
# lookup is the feature in your dataset that is used to encode the choropleth, always ordinal
# data is the desired piece of data to map onto the generated choropleth, always quantitative
# color is the color encoding to use in this instance
def generate_choropleth(topo, lookup, data, color):
    choropleth  = alt.Chart(topo).mark_geoshape(
    ).encode(
        color=alt.Color(data+':Q', scale=alt.Scale(scheme=color)),
        tooltip=[lookup+':O', data+':Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(state_data, 'id', [data,lookup])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )
    return choropleth

# Define pages as functions
def page1():
    # Page title and data initialization
    st.title("State Data & Choropleth")
    
    # Title of choropleth selection
    st.title( "What choropleth would you like to see regarding COVID-19 Stats")

    # Initializing radio button
    radio_btn = st.radio(
    "Choropleth Options",
        ('Covid 19 Deaths Per State','Avaiable ICU Beds Per State', 'Smoking Rate Per State', 'Population Per State', 'Health Spending Per State')
    )

    # Radio buttons for selection
    if radio_btn == 'Covid 19 Deaths Per State':
        st.title("Total Covid19 Death Rate (State) 100k")
        st.write(generate_choropleth(states, 'State', 'Deaths','reds'))
    elif radio_btn == 'Avaiable ICU Beds Per State':
        st.title("Total ICUS Avaiable per State")
        st.write(generate_choropleth(states, 'State', 'ICU Beds','tealblues'))
    elif radio_btn == 'Smoking Rate Per State':
        st.title("Smoking Rate Per State")
        st.write(generate_choropleth(states, 'State', 'Smoking Rate','browns'))
    elif radio_btn == 'Population Per State' :
        st.title("Population Per State")
        st.write(generate_choropleth(states, 'State', 'Population','oranges'))
    else:
        st.title("Health Spending Per State")
        st.write(generate_choropleth(states, 'State', 'Health Spending','purples'))
         
    #Data set for state covid data
    st.write(state_data)

def page2():
    st.title("County Data & Choropleth")

    st.write(counties_data)

def page3():
    st.title("Modelling/Predictions")
    # Add content for page 3

def page4():
    st.title("GPT Integration")
    # Add content for page 4

# Dictionary to map page names to their corresponding
pages = {
    "State Data & Choropleth": page1,
    "County Data & Choropleth": page2,
    "Modelling/Predictions": page3,
    "GPT Integration": page4
}

# Add a sidebar to the Streamlit app
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Call the selected page function
pages[selected_page]()
