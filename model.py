import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from vega_datasets import data
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import ElasticNet, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import pickle

# Load dataset
state_data = pd.read_csv('COVID19_state.csv')
state_data = state_data.drop(['State', 'Unnamed: 26'], axis=1)
state_data = state_data.dropna()


# Separate features from target variable
X = state_data.drop(['Deaths'], axis=1)
y = state_data['Deaths']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the training and testing data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Perform feature selection
kbest = SelectKBest(f_regression, k=10)
enet = ElasticNet(alpha=0.01, l1_ratio=0.9, max_iter=10000)
feature_selection_model = make_pipeline(kbest, enet)
feature_selection_model.fit(X_train_scaled, y_train)
selected_features_indices = feature_selection_model.named_steps['selectkbest'].get_support(indices=True)
selected_features_names = X_train.columns[selected_features_indices]

print("Best features: " + selected_features_names)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

param_grid = {
    'n_estimators': [50, 100, 300, 500],
    'max_depth': [3, 5, 7, 9, 11],
    'min_samples_split': [2, 5, 10, 15, 20]
}

# Create the grid search object
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, cv=kf, scoring='neg_mean_squared_error')

# Fit the grid search object to the training data
grid_search.fit(X_train_scaled[:, selected_features_indices], y_train)

# Print the best hyperparameters found
print(f"Best hyperparameters: {grid_search.best_params_}")

# Regularize selected features with random forest regression
rf_model = grid_search.best_estimator_
rf_model.fit(X_train_scaled[:, selected_features_indices], y_train)

# Test the model on the testing set and evaluate performance
y_pred = rf_model.predict(X_test_scaled[:, selected_features_indices])
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model in a pickle file
filename = 'model.pkl'
with open(filename, 'wb') as file:
    pickle.dump(rf_model, file)