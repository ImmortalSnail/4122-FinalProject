import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from vega_datasets import data

# Retreiving geographical data
counties = alt.topo_feature(data.us_10m.url, 'counties')
states = alt.topo_feature(data.us_10m.url, feature='states')

# Define pages as functions
def page1():
    # Page title and data initialization
    st.title("State Data & Choropleth")
    stateData = pd.read_csv('COVID19_state.csv')
    
    # Title of choropleth selection
    st.title( "What choropleth would you like to see regarding COVID-19 Stats")

    # Initializing radio button
    radioBTN = st.radio(
    "Choropleth Options",
        ('Covid 19 Deaths Per State','Avaiable ICU Beds Per State', 'Smoking Rate Per State', 'Population Per State', 'Health Spending Per State')
    )


    #Map showing covid Rate
    covid_Death_State = alt.Chart(states).mark_geoshape(
    ).encode(
        color=alt.Color('Deaths:Q', scale=alt.Scale(scheme='reds')),
        tooltip=['State:O', 'Deaths:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(stateData, 'id', ['Deaths','State'])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )

    # Map showing ICU beds data
    state_ICU  = alt.Chart(states).mark_geoshape(
    ).encode(
        color=alt.Color('ICU Beds:Q', scale=alt.Scale(scheme='tealblues')),
        tooltip=['State:O', 'ICU Beds:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(stateData, 'id', ['ICU Beds','State'])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )

    # Map showing smoking rates
    state_Smoking  = alt.Chart(states).mark_geoshape(
    ).encode(
        color=alt.Color('Smoking Rate:Q', scale=alt.Scale(scheme='browns')),
        tooltip=['State:O', 'Smoking Rate:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(stateData, 'id', ['Smoking Rate','State'])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )

    # Map showing population
    pop_Density  = alt.Chart(states).mark_geoshape(
    ).encode(
        color=alt.Color('Population:Q', scale=alt.Scale(scheme='oranges')),
        tooltip=['State:O', 'Population:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(stateData, 'id', ['Population','State'])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )

    # Map showing healthcare expenditures
    health_spend  = alt.Chart(states).mark_geoshape(
    ).encode(
        color=alt.Color('Health Spending:Q', scale=alt.Scale(scheme='purples')),
        tooltip=['State:O', 'Health Spending:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(stateData, 'id', ['Health Spending','State'])
    ).project('albersUsa').properties(
        width=800,
        height=800
    )

    # Radio buttons for selection
    if radioBTN == 'Covid 19 Deaths Per State':
        st.title("Total Covid19 Death Rate (State) 100k")
        st.write(covid_Death_State)
    elif radioBTN == 'Avaiable ICU Beds Per State':
        st.title("Total ICUS Avaiable per State")
        st.write(state_ICU)
    elif radioBTN == 'Smoking Rate Per State':
        st.title("Smoking Rate Per State")
        st.write(state_Smoking)
    elif radioBTN == 'Population Per State' :
        st.title("Population Per State")
        st.write(pop_Density)
    else:
        st.title("Health Spending Per State")
        st.write(health_spend)
        
        
        
        
    #Data set for state covid data
    st.write(stateData)

def page2():
    st.title("County Data & Choropleth")

    # Initializing county dataset
    countiesData =  pd.read_csv('us-counties.csv')
    countiesData = countiesData.sample(n=4999)

def page3():
    st.title("Modelling/Predictions")
    # Add content for page 3

def page4():
    st.title("GPT Integration")
    # Add content for page 4

# Dictionary to map page names to their corresponding functions
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