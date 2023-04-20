import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, 'counties')

states = alt.topo_feature(data.us_10m.url, feature='states')


# Load the data
countiesData =  pd.read_csv('us-counties.csv')

stateData = pd.read_csv('COVID19_state.csv')

countiesData = countiesData.sample(n=4999)



st.title( "What choropleth would you like to see regarding COVID-19 Stats")

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
