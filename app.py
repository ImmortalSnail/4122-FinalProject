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


#Map showing covid Rate
ch_unemployment = alt.Chart(states).mark_geoshape(
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

st.title("Dataset Used, this is just for development purposes to easily see")
st.write(stateData)

st.title("Total Covid19 Death Rate (State) 100k")
st.write(ch_unemployment)

st.title("Total ICUS Avaiable per State")
st.write(state_ICU)