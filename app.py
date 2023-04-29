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
        width=700,
        height=800
    )
    return choropleth

# Generate county choropleths
# state_id is state name, used to generate id
# data is the feature we are looking at
# scheme_name is the color scheme name
def gen_county_choro(state_id, data, scheme_name):
    counties_last = counties_data

    # Group the dataframe by the qualitative columns.
    counties_last = counties_last.groupby(['county', 'state', 'fips']).last().reset_index()

    # Reset the index of the dataframe.
    counties_last = counties_last.reset_index()
    counties_last = counties_last.dropna()

    # Convert 'fips' column to integer data type
    counties_last['fips'] = counties_last['fips'].astype(int)

    # Generates choropleth
    choropleth  = alt.Chart(counties).mark_geoshape(
    ).encode(
        color=alt.Color(data+':Q', scale=alt.Scale(scheme=scheme_name)),
        tooltip=['county:O', data+':Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(counties_last, 'fips', [data,'county'])
    ).transform_calculate(state_id = "(datum.id / 1000)|0"
    ).transform_filter(
    (alt.datum.state_id)==state_data[state_data["State"] == state_id]["id"].iloc[0].item()
    ).properties(
    width= 1400,
    height= 500
    )

    return choropleth

# Load the data
# countiesData =  pd.read_csv('us-counties.csv')
vaccinations = pd.read_csv('us_state_vaccinations.csv')
# countiesData = countiesData.sample(n=4999)

# Define pages as functions
def page1():
    
    st.title("Mapping COVID-19 and Age Demographics: Insights for Each State")
    
    
    #Split up into columns
    col1, col2 = st.columns(2)
    with col1:        
        
        # Initializing dropdown menu        
        dropdownChoro = st.selectbox("Choropleth Options",('Covid 19 Deaths Per State','Covid Infections Per State','Physicians Per State','Avaiable ICU Beds Per State', 'Smoking Rate Per State', 'Population Per State', 'Health Spending Per State'))         
        
        # Dropdown buttons for selection
        if dropdownChoro == 'Covid 19 Deaths Per State':
            st.title("COVID19 Deaths")
            st.write(generate_choropleth(states, 'State', 'Deaths','reds'))
            
        elif dropdownChoro == 'Covid Infections Per State':
            st.title("Covid Infections Per State")
            st.write(generate_choropleth(states, 'State', 'Infected','greens'))  
        
        elif dropdownChoro == 'Physicians Per State':
            st.title("Physicians Per State")
            st.write(generate_choropleth(states, 'State', 'Physicians','warmgreys')) 
            
        elif dropdownChoro == 'Avaiable ICU Beds Per State':
            st.title("ICU Beds Avaiable per State")
            st.write(generate_choropleth(states, 'State', 'ICU Beds','tealblues'))
        elif dropdownChoro == 'Smoking Rate Per State':
            st.title("Smoking Rate Per State")
            st.write(generate_choropleth(states, 'State', 'Smoking Rate','browns'))
        elif dropdownChoro == 'Population Per State' :
            st.title("Population Per State")
            st.write(generate_choropleth(states, 'State', 'Population','oranges'))
        else:
            st.title("Health Spending Per State")
            st.write(generate_choropleth(states, 'State', 'Health Spending','purples'))
            
        dropdown = st.selectbox("Select an Age Demographic to Explore",("Ages 0-25","Ages 26-54","Ages 55+"))     
    
        if dropdown == "Ages 0-25":
            st.header("Age Distribution: Proportion of Total Population For Ages 0-25 ")
            st.write(generate_choropleth(states, 'State', 'Age 0-25','blues'))
        elif dropdown == "Ages 26-54":
            st.header("Age Distribution: Proportion of Total Population For Ages 26-54 ")
            st.write(generate_choropleth(states, 'State', 'Age 26-54','blues'))
        else:
            st.header("Age Distribution: Proportion of Total Population For Ages 55+ ")
            st.write(generate_choropleth(states, 'State', 'Age 55+','blues'))        
            
    with col2:        
        dropdownChoro2 = st.selectbox("Second Choropleth Options",('Covid 19 Deaths Per State','Covid Infections Per State','Physicians Per State','Avaiable ICU Beds Per State', 'Smoking Rate Per State', 'Population Per State', 'Health Spending Per State')) 
        
        # Radio buttons for selection
        if dropdownChoro2 == 'Covid 19 Deaths Per State':
            st.title("COVID19 Deaths")
            st.write(generate_choropleth(states, 'State', 'Deaths','reds'))
        elif dropdownChoro2 == 'Covid Infections Per State':
            st.title("Covid Infections Per State")
            st.write(generate_choropleth(states, 'State', 'Infected','greens'))  
        elif dropdownChoro2 == 'Physicians Per State':
            st.title("Physicians Per State")
            st.write(generate_choropleth(states, 'State', 'Physicians','warmgreys')) 
        elif dropdownChoro2 == 'Avaiable ICU Beds Per State':
            st.title("ICU Beds Avaiable per State")
            st.write(generate_choropleth(states, 'State', 'ICU Beds','tealblues'))
        elif dropdownChoro2 == 'Smoking Rate Per State':
            st.title("Smoking Rate Per State")
            st.write(generate_choropleth(states, 'State', 'Smoking Rate','browns'))
        elif dropdownChoro2 == 'Population Per State' :
            st.title("Population Per State")
            st.write(generate_choropleth(states, 'State', 'Population','oranges'))
        else:
            st.title("Health Spending Per State")
            st.write(generate_choropleth(states, 'State', 'Health Spending','purples'))
            
        dropdown2 = st.selectbox("Select an Second Age Demographic to Explore",("Ages 0-25","Ages 26-54","Ages 55+"))     
    
        if dropdown2 == "Ages 0-25":
            st.header("Age Distribution: Proportion of Total Population For Ages 0-25 ")
            st.write(generate_choropleth(states, 'State', 'Age 0-25','blues'))
        elif dropdown2 == "Ages 26-54":
            st.header("Age Distribution: Proportion of Total Population For Ages 26-54 ")
            st.write(generate_choropleth(states, 'State', 'Age 26-54','blues'))
        else:
            st.header("Age Distribution: Proportion of Total Population For Ages 55+ ")
            st.write(generate_choropleth(states, 'State', 'Age 55+','blues'))
            
    # Data set for state covid data
    #st.write(state_data)
    
def vaccinationPage():
    
    st.title("Compare Vaccination Data")
    col1, col2 = st.columns(2)  
    
    
    location = st.sidebar.selectbox("First Location", vaccinations["location"].unique())
    location2 = st.sidebar.selectbox("Second Location", vaccinations["location"].unique())

    # Filter the data based on the State
    filtered_data = vaccinations[vaccinations["location"] == location]
    filtered_data2 = vaccinations[vaccinations["location"] == location2]
    
    grouped_data = vaccinations.groupby("location").sum().reset_index()
    grouped_data = grouped_data[grouped_data["location"] != "United States"]
    
    usTotalData = vaccinations[vaccinations["location"] == "United States"]
    
    chart = alt.Chart(filtered_data).mark_line(color="blue",interpolate="basis").encode(
    x= alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("total_vaccinations", axis = alt.Axis(title='Total Vaccinations')),
    )
    
    chart2 =  alt.Chart(filtered_data2).mark_line(color="red",interpolate="basis").encode(
    x=alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("total_vaccinations", axis = alt.Axis(title='Total Vaccinations')),
    )
     
    barchart = alt.Chart(grouped_data).mark_bar().encode(
    x= alt.X("location", axis = alt.Axis(title='State')),
    y= alt.Y("total_vaccinations", axis = alt.Axis(title='Total Vaccinations')),
    tooltip=["location", "total_vaccinations"]
    )
    
    fullyVaccinated =  alt.Chart(filtered_data).mark_line(color="blue",interpolate="basis").encode(
    x=alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("people_fully_vaccinated", axis = alt.Axis(title='Amount of People Fully Vaccinated ')),
    )
    
    fullyVaccinated2 =  alt.Chart(filtered_data2).mark_line(color="red",interpolate="basis").encode(
    x=alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("people_fully_vaccinated", axis = alt.Axis(title='Amount of People Fully Vaccinated ')),
    )
    
    totalvaccinatedOverTime =  alt.Chart(usTotalData).mark_line(color="green",interpolate="basis").encode(
    x=alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("total_vaccinations", axis = alt.Axis(title='Total Vaccinations')),
    )
    
    fullyvaccinatedOverTime =  alt.Chart(usTotalData).mark_line(color="purple",interpolate="basis").encode(
    x=alt.X("date", axis = alt.Axis(title='Date')),
    y= alt.Y("people_fully_vaccinated", axis = alt.Axis(title='Amount of People Fully Vaccinated')),
    )
    
    
    with col1:
        st.header(" Total Vaccinations: "+ location)
        st.altair_chart(chart, use_container_width=True)
        st.header("Amount of People Fully Vaccinated: " + location)
        st.altair_chart(fullyVaccinated, use_container_width=True) 
    
    with col2:
        st.header(" Total Vaccinations: "+ location2)
        st.altair_chart(chart2, use_container_width=True) 
        st.header("Amount of People Fully Vaccinated: " + location2)
        st.altair_chart(fullyVaccinated2, use_container_width=True)
    
    st.header("Total Vaccinations by State in the U.S.")
    st.altair_chart(barchart, use_container_width=True)
    
    st.header("Total Vaccinations Over Time in the U.S. ")
    st.altair_chart(totalvaccinatedOverTime, use_container_width=True)
    
    st.header("Amount of People Fully Vaccinated Over Time in the U.S. ")
    st.altair_chart(fullyvaccinatedOverTime, use_container_width=True)
    
    # Display Vaccination Data uncomment if you want 
    #st.write(vaccinations)   

def page2():
    st.title("Visualizing County-Level COVID-19 Data: Cases and Deaths") 

    state = st.sidebar.selectbox("State", counties_data["state"].unique())

    # Define radio buttons
    button = st.radio(
    "Choropleth Options",
        ('Deaths','Cases')
    )

    # Displays appropriate choropleth from selection
    if button == 'Deaths':
        st.header("Covid " + button + " in " + state + " by County")
        st.write(gen_county_choro(state, 'deaths', 'tealblues'))
    else:
        st.header("Covid " + button + " in " + state + " by County")
        st.write(gen_county_choro(state, 'cases', 'purples'))
    
    col1, col2 = st.columns(2)
    # Data transforming to get the county to only show up for the State its in
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

    #st.write(counties_data)

# Dictionary to map page names to their corresponding functions
pages = {
    "State Data Choropleths": page1,
    "County Data Choropleth & Charts": page2,
    "Vaccination Information Charts": vaccinationPage
}

# Add a sidebar to the Streamlit app
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Call the selected page function
pages[selected_page]()