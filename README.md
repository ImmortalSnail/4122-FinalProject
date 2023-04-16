# COVID Data Exploration with Streamlit, Altair, and Scikit-learn

This project is a Streamlit app that allows users to explore COVID-19 data using Altair and Scikit-learn. 
The app provides interactive visualizations and predictive models to analyze the spread of the virus within the United States.

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Data Sources](#Data-Sources)
- [Technologies Used](#Technologies-Used)

## Installation

To run this app locally, you will need to have Python 3 installed. 
Clone this repository and then install the required Python packages by running the following command in your terminal:

```
pip install -r requirements.txt
```

## Usage

To launch the Streamlit app, run the following command in your terminal:

```
streamlit run app.py
```

After selecting a dataset, the app will display various visualizations and predictions based on the selected data set. 
You can use the interactive widgets provided by Streamlit to modify the visualizations and models.

## Data Sources

The COVID-19 data used in this app is sourced from Our World in Data as well as the NYT, 
which provides up-to-date and reliable data on COVID-19 cases, deaths, and vaccination rates from around the world.
Note, if running this locally you will need a copy of the data sets from Our World in Data/ NYT, otherwise the app will not work.

## Technologies Used

This app was built using the following technologies:

- Streamlit: an open-source app framework for building interactive data apps in Python
- Altair: a Python library for declarative visualization in a grammar of graphics style
- Scikit-learn: a Python library for machine learning built on NumPy, SciPy, and matplotlib
- Pandas: a Python library for data manipulation and analysis
- NumPy: a Python library for numerical computing

## Heroku Link

This app will be deployed on Heroku once it is finished. This is so it can be used without needing to fetch the data sets.
