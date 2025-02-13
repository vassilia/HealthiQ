from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd


# Load the Excel file
file_path = 'Final_Combined_ICD10_Codes_for_Analysis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Load data from sheets
icd10_data = excel_data.parse('ICD10')
raw_data = excel_data.parse('Raw data')

from datetime import datetime

# Convert 'BIRTH' to Age
current_year = 2024
raw_data['Age'] = current_year - pd.to_numeric(raw_data['BIRTH'], errors='coerce')
raw_data = raw_data[raw_data['BIRTH'] != 1900]  # Remove invalid birth year

# Map ICD10 codes to Health Risks using ICD10 sheet
icd10_mapping = icd10_data.set_index('ICD10 Code')['Health Risk'].to_dict()
raw_data['Health Risk'] = raw_data['Primary Diagnosis'].map(icd10_mapping)

# Define age groups
age_bins = [0, 18, 35, 50, 65, 100]
age_labels = ['0-18', '19-35', '36-50', '51-65', '66+']
raw_data['Age Group'] = pd.cut(raw_data['Age'], bins=age_bins, labels=age_labels, right=False)

# Encode gender and age group
raw_data['Gender'] = raw_data['gender Male -1 Female 0'].replace({-1: 'Male', 0: 'Female'})
raw_data = raw_data.dropna(subset=['Health Risk', 'Primary Diagnosis'])

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Select features and target
features = raw_data[['Primary Diagnosis', 'Age Group', 'Gender']]
target = raw_data['Health Risk']

# Ensure categorical columns are strings to avoid encoding issues
features['Primary Diagnosis'] = features['Primary Diagnosis'].astype(str)
features['Age Group'] = features['Age Group'].astype(str)
features['Gender'] = features['Gender'].astype(str)

# Define the column transformer for encoding
column_transformer = ColumnTransformer([
    ('icd10_encoder', OneHotEncoder(handle_unknown='ignore'), ['Primary Diagnosis']),
    ('age_encoder', OneHotEncoder(handle_unknown='ignore'), ['Age Group']),
    ('gender_encoder', OneHotEncoder(handle_unknown='ignore'), ['Gender'])
])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Define the pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', column_transformer),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Set hyperparameter grid for tuning
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [10, 20, None],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Use GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=2)

# Train the optimized pipeline
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Evaluate the best model
y_pred = best_model.predict(X_test)
print("Best Model Parameters:")
print(grid_search.best_params_)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))