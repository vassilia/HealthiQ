import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file to examine its structure and content
file_path = 'data_raw.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
print(excel_data.sheet_names)

# Load the data from the first sheet into a DataFrame
data = excel_data.parse('Sheet1')

# Display the first few rows of the dataset to understand its structure and content
print(data.head())

#calculate the frequency of each value in the 'Primary Diagnosis' column
diagnosis_freq = data['Primary Diagnosis'].value_counts()
#print(diagnosis_freq)

#put the diagnosis frequency into a bar chart (first 10)

diagnosis_freq[:10].plot(kind='bar')
plt.xlabel('Primary Diagnosis')
plt.ylabel('Frequency')
plt.title('Frequency of Primary Diagnosis')
#plt.show()


# Calculate the number of surgical DRGs
surgical_drg_count = data['Surgical \nDRG (1-yes/0-no)'].sum()
print(surgical_drg_count)

# Calculate the percentage of surgical DRGs out of the total cases
total_cases = len(data)
surgical_drg_percentage = (surgical_drg_count / total_cases) * 100

# Display the results
surgical_drg_stats = {
    "Total Cases": total_cases,
    "Surgical DRG Cases": surgical_drg_count,
    "Percentage of Surgical DRG Cases": surgical_drg_percentage
}

print(surgical_drg_stats)

# Create a new column for age
current_year = 2024
data['Age'] = current_year - data['BIRTH']

# Define age groups
bins = [0, 18, 35, 50, 65, 80, 100]
labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81+']
data['Age Group'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

# Filter only surgical DRG cases
surgical_drg_data = data[data['Surgical \nDRG (1-yes/0-no)'] == 1]

# Count the number of surgical DRG cases in each age group
age_group_counts = surgical_drg_data['Age Group'].value_counts().sort_index()

# Visualize the age group distribution for surgical DRG cases
plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar')
plt.title('Surgical DRG Cases by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Number of Cases', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Filter only medical DRG cases
medical_drg_data = data[data['Medical\nDRG (1-yes/0-no)'] == 1]

# Count the number of medical DRG cases in each age group
medical_age_group_counts = medical_drg_data['Age Group'].value_counts().sort_index()

# Visualize the age group distribution for medical DRG cases
plt.figure(figsize=(10, 6))
medical_age_group_counts.plot(kind='bar', color='orange')
plt.title('Medical DRG Cases by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Number of Cases', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Prepare data for comparison
surgical_vs_medical = pd.DataFrame({
    'Surgical DRG': surgical_drg_data['Age Group'].value_counts().sort_index(),
    'Medical DRG': medical_drg_data['Age Group'].value_counts().sort_index()
})

# Plot the comparison
surgical_vs_medical.plot(kind='bar', figsize=(10, 6))
plt.title('Comparison of Surgical and Medical DRG Cases by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Number of Cases', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='DRG Type')
plt.tight_layout()
plt.show()

# Calculate the average length of stay for surgical and medical DRG cases
surgical_avg_los = surgical_drg_data['LoS'].mean()
medical_avg_los = medical_drg_data['LoS'].mean()
print(surgical_avg_los, medical_avg_los)

# Calculate the average total length of stay for surgical and medical DRG cases per age group
avg_los_by_age_group = data.groupby(['Age Group', 'Surgical \nDRG (1-yes/0-no)'])['LoS'].mean().unstack()
print(avg_los_by_age_group)
#make it a bar chart
avg_los_by_age_group.plot(kind='bar', figsize=(10, 6))
plt.title('Average Length of Stay by Age Group and DRG Type', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Average Length of Stay', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Surgical DRG', labels=['Non-Surgical', 'Surgical'])
plt.tight_layout()
plt.show()


# Recreate the 'Age' and 'Age Group' columns
current_year = 2024
data['Age'] = current_year - data['BIRTH']

# Define age groups
bins = [0, 18, 35, 50, 65, 80, 100]
labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81+']
data['Age Group'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

# Filter cases where discharge reason is death
death_cases = data[data['DischargeReason Death (1-yes/0-no)'] == 1]

# Calculate the average length of stay (LoS) for each age group among death cases
avg_los_death_by_age_group = death_cases.groupby('Age Group')['LoS'].mean()

plt.figure(figsize=(10, 6))
avg_los_death_by_age_group.plot(kind='bar', color='red', edgecolor='black')
plt.title('Average Length of Stay for Discharge due to Death Cases by Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Average Length of Stay (LoS)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#calculate average LoS for each age group for all reasons
# List of discharge reason columns to analyze
discharge_reason_columns = [
    'DischargeReason Normal treatment completion (1-yes/0-no)',
    'DischargeReason Normal treatment completion, follow-up after hospitalization, unspecified (1-yes/0-no)',
    'DischargeReason Discontinuation of treatment for other reasons (1-yes/0-no)',
    'DischargeReason Discontinuation of treatment against  medical advice (1-yes/0-no)',
    'DischargeReason Transfer to another hospital (1-yes/0-no)',
    'DischargeReason Death (1-yes/0-no)',
    'DischargeReason Discharge/transfer in a rehabilitation facility (1-yes/0-no)',
    'DischargeReason Case closure when switching between full and daily inpatient treatment (1-yes/0-no)'
]

# Calculate average LoS for each discharge reason by age group
avg_los_by_discharge_and_age = {}

for column in discharge_reason_columns:
    # Filter cases where the discharge reason is 'yes' (1)
    filtered_cases = data[data[column] == 1]
    # Calculate the average LoS by age group
    avg_los_by_discharge_and_age[column] = filtered_cases.groupby('Age Group')['LoS'].mean()

# Convert to DataFrame for easier comparison and visualization
avg_los_by_discharge_and_age_df = pd.DataFrame(avg_los_by_discharge_and_age)

# Display the DataFrame
print(avg_los_by_discharge_and_age_df)


import matplotlib.pyplot as plt
import seaborn as sns

# Adjust the heatmap to improve readability, especially for age group labels
plt.figure(figsize=(14, 8))
sns.heatmap(avg_los_by_discharge_and_age_df, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Average Length of Stay (LoS)'})
plt.title('Average Length of Stay by Age Group and Discharge Reason', fontsize=16)
plt.xlabel('Discharge Reason', fontsize=12)
plt.ylabel('Age Group', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)  # Ensure age groups are horizontal
plt.tight_layout()
plt.show()

##Proportion of Deaths by LoS

# Define Length of Stay (LoS) intervals
los_bins = [0, 3, 7, float('inf')]
los_labels = ['<3 days', '3-7 days', '>7 days']
data['LoS Interval'] = pd.cut(data['LoS'], bins=los_bins, labels=los_labels, right=False)

# Calculate total cases and death cases for each age group and LoS interval
total_cases_by_age_los = data.groupby(['Age Group', 'LoS Interval']).size()
death_cases_by_age_los = data[data['DischargeReason Death (1-yes/0-no)'] == 1].groupby(['Age Group', 'LoS Interval']).size()

# Calculate the proportion of death cases within each LoS interval for each age group
proportion_deaths_by_age_los = (death_cases_by_age_los / total_cases_by_age_los * 100).unstack()

# Display the proportions
proportion_deaths_by_age_los.fillna(0, inplace=True)  # Fill NaN with 0 for intervals with no deaths
print(proportion_deaths_by_age_los)

# Visualize the proportion of deaths by LoS interval and age group using a grouped bar chart
plt.figure(figsize=(12, 8))
proportion_deaths_by_age_los.plot(kind='bar', stacked=False, edgecolor='black', colormap='coolwarm', width=0.8)
plt.title('% of Deaths by (LoS) Interval and Age Group', fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Proportion of Deaths (%)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='LoS Interval', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
