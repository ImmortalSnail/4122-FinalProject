import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, 'counties')

states = alt.topo_feature(data.us_10m.url, feature='states')


# Load the data
#countiesData =  pd.read_csv('us-counties.csv')
# Load the data
stateData = pd.read_csv('COVID19_state.csv')

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


#countiesData = countiesData.sample(n=4999)



st.title( "What choropleth would you like to see regarding COVID-19 Stats")

radioBTN = st.radio(
   "Choropleth Options",
    ('Covid 19 Deaths Per State','Avaiable ICU Beds Per State', 'Smoking Rate Per State', 'Population Per State', 'Health Spending Per State')
)


#Map showing covid Rate
# Map showing covid Rate with polynomial features
covid_Death_State = alt.Chart(states).mark_geoshape(
).encode(
    color=alt.Color('Deaths_poly:Q', scale=alt.Scale(scheme='reds')),  # Update the column to use polynomial feature
    tooltip=['State:O', 'Deaths:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(stateData, 'id', ['Deaths_poly','State'])  # Update the column to use polynomial feature
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
