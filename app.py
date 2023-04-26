import altair as alt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
import streamlit as st
from vega_datasets import data

st.set_page_config(page_title="My Streamlit App", page_icon=":syringe:", layout="wide")


# Loading relevant data
counties = alt.topo_feature(data.us_10m.url, feature='counties')
states = alt.topo_feature(data.us_10m.url, feature='states')
state_data = pd.read_csv('COVID19_state.csv')
counties_data = pd.read_csv('us-counties.csv')

#limits dataset to 5000 samples uncomment if you want it 
#counties_data = counties_data.sample(n=4999)

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


# Load the data
#countiesData =  pd.read_csv('us-counties.csv')
stateData = pd.read_csv('COVID19_state.csv')
vaccinations = pd.read_csv('us_state_vaccinations.csv')
#countiesData = countiesData.sample(n=4999)

# Define pages as functions
def page1():
    # Page title and data initialization
    st.title("State Data & Choropleth")

    
    # Title of choropleth selection
    st.header( "What choropleth would you like to see regarding COVID-19 Stats")

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
    
def vaccinationPage():
    
    col1, col2 = st.columns(2)
    
    st.title("Compare Vaccination Data")
    location = st.sidebar.selectbox("First Location", vaccinations["location"].unique())
    location2 = st.sidebar.selectbox("Second Location", vaccinations["location"].unique())

    # Filter the data based on the State
    filtered_data = vaccinations[vaccinations["location"] == location]
    filtered_data2 = vaccinations[vaccinations["location"] == location2]
    
    grouped_data = vaccinations.groupby("location").sum().reset_index()

    
    chart = alt.Chart(filtered_data).mark_line(color="blue",interpolate="basis").encode(
    x="date",
    y= "total_vaccinations"
    )
    
    chart2 =  alt.Chart(filtered_data2).mark_line(color="red",interpolate="basis").encode(
    x="date",
    y= "total_vaccinations"
    )
    
     
    barchart = alt.Chart(grouped_data).mark_bar().encode(
    x="location",
    y="total_vaccinations",
    tooltip=["location", "total_vaccinations"]
    )
    
    with col1:
        st.header(location + " Total Vaccinations")
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        st.header(location2 + " Total Vaccinations")
        st.altair_chart(chart2, use_container_width=True) 
    
    
    
    st.altair_chart(barchart, use_container_width=True)
    
    #Display Vaccination Data
    st.write(vaccinations)   

def page2():
    st.title("County Data Choropleth & Graphs") 
    
    col1, col2 = st.columns(2)
    
    state = st.sidebar.selectbox("State", counties_data["state"].unique())
    
    #Data transforming to get the county to only show up for the State its in
    counties_list = list(counties_data[counties_data["state"] == state]["county"].unique())
    
    county = st.sidebar.selectbox("County", counties_list)

    # Filter the data based on the State
    filtered_data = counties_data[ (counties_data["state"] == state) & (counties_data["county"] == county) ]
    
    
    deathChart = alt.Chart(filtered_data).mark_line(color="blue",interpolate="basis").encode(
    x="date",
    y= "deaths"
    )
    
    caseChart =  alt.Chart(filtered_data).mark_line(color="red",interpolate="basis").encode(
    x="date",
    y= "cases"
    )
   
    with col1:
        st.header("COVID-19 Deaths in " + county + " County, " + state  )
        st.altair_chart(deathChart, use_container_width=True)
    
    with col2:
        st.header("COVID-19 Cases in "  + county + " County, " + state )
        st.altair_chart(caseChart, use_container_width=True)


    map_georgia =(
    alt.Chart(data = counties)
    .mark_geoshape(
        stroke='black',
        strokeWidth=1
    )
    .transform_calculate(state_id = "(datum.id / 1000)|0")
    .transform_filter((alt.datum.state_id)==13)
    )

    map_georgia

    st.write(counties_data)

def page3():
    st.title("Modelling/Predictions")
    # Add polynomial features to Deaths column
    poly_features = PolynomialFeatures(degree=2)  # You can choose the degree of polynomial regression
    X = stateData['Deaths'].values.reshape(-1, 1)  # Input feature
    X_poly = poly_features.fit_transform(X)  # Transformed feature with polynomial features
    stateData['Deaths_poly'] = X_poly[:, 1]  # Add transformed feature to stateData DataFrame
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_poly, stateData['Deaths'], test_size=0.2, random_state=42)

    # Fit polynomial regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on testing data
    y_pred = model.predict(X_test)

    # Calculate mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)

    # Make prediction for a new input value
    new_input = np.array([[1000]])  # Example input value
    new_input_poly = poly_features.transform(new_input)
    prediction = model.predict(new_input_poly)
    print('Prediction for new input value:', prediction)

def page4():
    st.title("GPT Integration")
    # Add content for page 4   
    
# Dictionary to map page names to their corresponding functions

pages = {
    "State Data Choropleths": page1,
    "County Data Choropleth & Charts": page2,
    "Vaccination Information Charts": vaccinationPage,
    "Modelling/Predictions": page3,
    "GPT Integration": page4
}

# Add a sidebar to the Streamlit app
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Call the selected page function
pages[selected_page]()