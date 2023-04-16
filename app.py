import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('data.csv')
    return data

data = load_data()

st.write(data)