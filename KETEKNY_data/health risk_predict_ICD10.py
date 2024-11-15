import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

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

# Selecting Features and Target
features = raw_data[['Primary Diagnosis', 'Age Group', 'Gender']]
target = raw_data['Health Risk']

# Ensure categorical columns are strings to avoid encoding issues
features['Primary Diagnosis'] = features['Primary Diagnosis'].astype(str)
features['Age Group'] = features['Age Group'].astype(str)
features['Gender'] = features['Gender'].astype(str)

# Define the ColumnTransformer with OneHotEncoder, setting handle_unknown to 'ignore'
column_transformer = ColumnTransformer([
    ('icd10_encoder', OneHotEncoder(handle_unknown='ignore'), ['Primary Diagnosis']),
    ('age_encoder', OneHotEncoder(handle_unknown='ignore'), ['Age Group']),
    ('gender_encoder', OneHotEncoder(handle_unknown='ignore'), ['Gender'])
])

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Applying the transformations on training and test data
X_train_encoded = column_transformer.fit_transform(X_train)
X_test_encoded = column_transformer.transform(X_test)

# Create a pipeline with preprocessing and model
pipeline = Pipeline(steps=[
    ('preprocessor', column_transformer),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)


# Predict on test data
y_pred = pipeline.predict(X_test)

# Evaluation metrics
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
