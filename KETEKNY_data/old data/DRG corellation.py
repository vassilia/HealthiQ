import pandas as pd

# Load the Excel file
file_path = 'Final_Combined_ICD10_Codes_for_Analysis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
excel_data.sheet_names

# Load the data from each sheet to explore the content
icd10_data = excel_data.parse('ICD10')
raw_data = excel_data.parse('Raw data')

# Display the first few rows of each sheet to understand the data
icd10_data_head = icd10_data.head()
raw_data_head = raw_data.head()

print(icd10_data_head)
print(raw_data_head)

from datetime import datetime

# Convert the 'BIRTH' column to an age based on current year (assuming the year is 2024 for calculation purposes)
raw_data['BIRTH'] = pd.to_numeric(raw_data['BIRTH'], errors='coerce')  # Ensure BIRTH is numeric
current_year = 2024
raw_data['Age'] = current_year - raw_data['BIRTH']

# # Calculate age statistics
age_stats = raw_data['Age'].describe()
print(age_stats)

#from BIRTH column remove those born at 1900
raw_data = raw_data[raw_data['BIRTH'] != 1900]

# # Calculate age statistics
age_stats = raw_data['Age'].describe()
print(age_stats)

# # Calculate gender distribution
gender_counts = raw_data['gender Male -1 Female 0'].value_counts().rename(index={-1: 'Male', 0: 'Female'})
print(gender_counts)


import matplotlib.pyplot as plt

# Plotting Gender Distribution
plt.figure(figsize=(8, 5))
gender_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")
plt.xticks(rotation=0)
plt.show()
#
# Plotting Age Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(raw_data['Age'], bins=20, color='lightgreen', edgecolor='black')
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# # ICD10 Frequency Distribution for Primary and Secondary Diagnoses
# # Merging all diagnosis columns to calculate frequency of each ICD10 code
icd10_columns = ['Primary Diagnosis', 'Secondary Diagnosis_1', 'Secondary Diagnosis_2',
                 'Secondary Diagnosis_3', 'Secondary Diagnosis_4', 'Secondary Diagnosis_5']
icd10_codes = pd.concat([raw_data[col] for col in icd10_columns]).value_counts()

# Display the top 20 ICD10 codes for simplicity in the chart
top_icd10_codes = icd10_codes.head(20)
print(top_icd10_codes)

# # Plotting ICD10 Code Frequency Distribution
plt.figure(figsize=(12, 8))
top_icd10_codes.plot(kind='bar', color='lightcoral', edgecolor='black')
plt.title("Top 20 ICD10 Code Frequency Distribution")
plt.xlabel("ICD10 Code")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

#in 'final_combined_icd10_codes_for_analysis.xlsx' file, there are 2 sheets: 'ICD10' and 'Raw data', in sheet 'Raw data' I want to go to column 'Primary Diagnosis' and for each value there, I want to search for this value in the corresponding 'ICD10' sheet and get the 'Health Risk' value for that (it's in the second column of the sheet).
#i want to prin that informatin
# # Map Primary Diagnosis to Health Risk
# # Create a dictionary to map Primary Diagnosis to Health Risk
icd10_mapping = icd10_data.set_index('ICD10 Code')['Health Risk'].to_dict()
# # Map the Primary Diagnosis to Health Risk using the dictionary
raw_data['Health Risk'] = raw_data['Primary Diagnosis'].map(icd10_mapping)
# # Display the first few rows to verify the mapping
print(raw_data[['Primary Diagnosis', 'Health Risk']].head())
print(raw_data[['Primary Diagnosis', 'Health Risk']])

# # Calculate Health Risk Distribution
health_risk_counts = raw_data['Health Risk'].value_counts()
print(health_risk_counts)

# Display all mappings of Primary Diagnosis to Health Risk
primary_diagnosis_to_health_risk = raw_data[['Primary Diagnosis', 'Health Risk']]
print(primary_diagnosis_to_health_risk)

import matplotlib.pyplot as plt

# Count the frequency of each Health Risk
health_risk_counts = primary_diagnosis_to_health_risk['Health Risk'].value_counts()

# Plotting the Health Risk frequency distribution
plt.figure(figsize=(12, 8))
health_risk_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Health Risk Frequency Distribution")
plt.xlabel("Health Risk")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Selecting the first 20 ICD10 codes from the Primary Diagnosis column in raw_data_filtered
top_20_icd10_codes = raw_data['Primary Diagnosis'].value_counts().index[:20]

# Filtering the raw_data_filtered for only the top 20 ICD10 codes
top_20_data = raw_data[raw_data['Primary Diagnosis'].isin(top_20_icd10_codes)]

# Selecting relevant columns: ICD10 code (Primary Diagnosis), corresponding Health Risk, and DRG 1
top_20_table = top_20_data[['Primary Diagnosis', 'Health Risk', 'DRG 1']].dropna()

#show top 10 ICD1- codes with their corresponding Health Risk and DRG 1
print(top_20_table.head(10))

#make age groups for the patients -10 years and categorize health risk per group
# Create age groups
age_bins = [0, 18, 35, 50, 65, 100]
age_labels = ['0-18', '19-35', '36-50', '51-65', '66+']
raw_data['Age Group'] = pd.cut(raw_data['Age'], bins=age_bins, labels=age_labels, right=False)

# Calculate Health Risk distribution per Age Group
health_risk_by_age_group = raw_data.groupby(['Age Group', 'Health Risk']).size().unstack(fill_value=0)
print(health_risk_by_age_group)

#put health risk distribution per age group in a bar chart
import matplotlib.pyplot as plt

# Plotting Health Risk Distribution per Age Group
fig, ax = plt.subplots(figsize=(12, 8))
health_risk_by_age_group.plot(
    kind='bar',
    stacked=True,
    color=['skyblue', 'lightcoral', 'lightgreen'],
    edgecolor='black',
    ax=ax
)
plt.title("Health Risk Distribution per Age Group")
plt.xlabel("Age Group")
plt.ylabel("Frequency")
plt.xticks(rotation=0)


# Adding data labels to each section of the stacked bars
for container in ax.containers:
    ax.bar_label(container, label_type='center', fmt='%.0f', fontsize=9, color="black")

plt.tight_layout()
plt.show()





