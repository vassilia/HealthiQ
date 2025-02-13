import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = 'data_raw.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')  # Ensure this line loads the data as a DataFrame

# Calculate age based on birth year
current_year = 2025
data['Age'] = current_year - data['BIRTH']

# Define age groups
age_bins = [18, 39, 65, 75, 85, 90, np.inf]
age_labels = ['19-39', '40-65', '66-75', '76-85', '86-90', '90+']
data['Age Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels, right=False)

# Extract discharge reasons columns
discharge_columns = [col for col in data.columns if 'DischargeReason' in col]

# Add a gender label for clarity
data['Gender'] = data['gender Male -1 Female 0'].replace({1: 'Male', 0: 'Female'})


# Function to create a heatmap for a specific gender
def create_heatmap(data, gender, title):
    # Filter data for the specific gender
    gender_data = data[data['Gender'] == gender]

    # Calculate percentages of discharge reasons for each age group
    heatmap_data = (
            gender_data.groupby('Age Group')[discharge_columns].mean() * 100
    ).round(2)

    # Create heatmap
    plt.figure(figsize=(16, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Percentage (%)'})
    plt.title(f'{title} - {gender}', fontsize=16)
    plt.xlabel('Discharge Reasons', fontsize=12)
    plt.ylabel('Age Groups', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Create heatmaps for males and females
create_heatmap(data, 'Male', 'Discharge Reasons Heatmap')
create_heatmap(data, 'Female', 'Discharge Reasons Heatmap')


# Function to create a stacked bar plot
def create_stacked_bar(data, gender, title):
    # Filter data for the specific gender
    gender_data = data[data['Gender'] == gender]

    # Calculate counts for each discharge reason grouped by age group
    stacked_data = (
            gender_data.groupby('Age Group')[discharge_columns]
            .sum()
            .div(gender_data.groupby('Age Group')[discharge_columns].sum().sum(axis=1), axis=0) * 100
    )

    # Create a stacked bar plot
    ax = stacked_data.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title(f'{title} - {gender}', fontsize=16)
    plt.xlabel('Age Groups', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.legend(title='Discharge Reasons', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Create stacked bar plots for males and females
create_stacked_bar(data, 'Male', 'Discharge Reasons Stacked Bar Plot')
create_stacked_bar(data, 'Female', 'Discharge Reasons Stacked Bar Plot')


def create_combined_stacked_bar(data, title):
    # Calculate the distribution of discharge reasons by gender and age group
    male_data = data[data['Gender'] == 'Male'].groupby('Age Group')[discharge_columns].sum()
    female_data = data[data['Gender'] == 'Female'].groupby('Age Group')[discharge_columns].sum()

    # Normalize to percentages
    male_data = male_data.div(male_data.sum(axis=1), axis=0) * 100
    female_data = female_data.div(female_data.sum(axis=1), axis=0) * 100

    # Combine male and female data for plotting
    combined_data = pd.concat(
        {'Male': male_data, 'Female': female_data}, axis=1
    ).swaplevel(axis=1)

    # Plot the combined stacked bar chart
    ax = combined_data.plot(
        kind='bar',
        stacked=True,
        figsize=(14, 8),
        colormap='tab10',
        width=0.8
    )
    plt.title(f'{title}', fontsize=16)
    plt.xlabel('Age Groups', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Discharge Reasons', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Create the combined stacked bar plot
create_combined_stacked_bar(data, 'Discharge Reasons Stacked Bar Plot (Male & Female)')


def create_side_by_side_bar(data, title):
    # Calculate percentages for males and females separately
    male_data = data[data['Gender'] == 'Male'].groupby('Age Group')[discharge_columns].sum()
    female_data = data[data['Gender'] == 'Female'].groupby('Age Group')[discharge_columns].sum()

    # Normalize to percentages
    male_data = male_data.div(male_data.sum(axis=1), axis=0) * 100
    female_data = female_data.div(female_data.sum(axis=1), axis=0) * 100

    # Prepare data for side-by-side plotting
    x = np.arange(len(male_data.index))  # Age group positions
    bar_width = 0.35  # Width of each bar

    # Plot each discharge reason for males and females
    fig, ax = plt.subplots(figsize=(14, 8))

    for i, column in enumerate(discharge_columns):
        ax.bar(
            x - bar_width / 2 + i * bar_width / len(discharge_columns),  # Adjust position for males
            male_data[column],
            width=bar_width / len(discharge_columns),
            label=f'Male - {column}'
        )
        ax.bar(
            x + bar_width / 2 + i * bar_width / len(discharge_columns),  # Adjust position for females
            female_data[column],
            width=bar_width / len(discharge_columns),
            label=f'Female - {column}'
        )

    # Formatting the plot
    ax.set_title(f'{title}', fontsize=16)
    ax.set_xlabel('Age Groups', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(male_data.index, rotation=45)
    ax.legend(title='Discharge Reasons', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Create the side-by-side bar plot
create_side_by_side_bar(data, 'Discharge Reasons Side-by-Side Bar Plot (Male & Female)')

def create_gender_ratio_heatmap(data, title):
    # Calculate gender ratio for each discharge reason across age groups
    male_data = data[data['Gender'] == 'Male'].groupby('Age Group')[discharge_columns].sum()
    female_data = data[data['Gender'] == 'Female'].groupby('Age Group')[discharge_columns].sum()
    gender_ratio = male_data.div(female_data.replace(0, np.nan))  # Avoid division by zero

    # Create heatmap
    plt.figure(figsize=(16, 10))
    sns.heatmap(gender_ratio, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Male/Female Ratio'})
    plt.title(f'{title}', fontsize=16)
    plt.xlabel('Discharge Reasons', fontsize=12)
    plt.ylabel('Age Groups', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Create gender ratio heatmap
create_gender_ratio_heatmap(data, 'Male/Female Ratio by Discharge Reason Across Age Groups')

# Function to create faceted stacked bar plots
def create_faceted_stacked_bars(data, title):
    # Calculate percentages for males and females separately
    male_data = data[data['Gender'] == 'Male'].groupby('Age Group')[discharge_columns].sum()
    female_data = data[data['Gender'] == 'Female'].groupby('Age Group')[discharge_columns].sum()

    # Normalize to percentages
    male_data = male_data.div(male_data.sum(axis=1), axis=0) * 100
    female_data = female_data.div(female_data.sum(axis=1), axis=0) * 100

    # Combine data into a single DataFrame for plotting
    male_data['Gender'] = 'Male'
    female_data['Gender'] = 'Female'
    combined_data = pd.concat([male_data, female_data]).reset_index()
    combined_data_melted = combined_data.melt(
        id_vars=['Age Group', 'Gender'],
        value_vars=discharge_columns,
        var_name='Discharge Reason',
        value_name='Percentage'
    )

    # Create the faceted stacked bar plots
    g = sns.catplot(
        data=combined_data_melted,
        x='Gender',
        y='Percentage',
        hue='Discharge Reason',
        col='Age Group',
        kind='bar',
        col_wrap=4,
        height=5,
        aspect=1.2,
        palette='tab10'
    )
    g.set_titles("{col_name} Age Group")
    g.set_axis_labels("Gender", "Percentage (%)")
    g.set_xticklabels(rotation=45)
    g._legend.set_title('Discharge Reasons')
    g.fig.suptitle(title, fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

# Create faceted stacked bar plots
create_faceted_stacked_bars(data, 'Faceted Stacked Bar Plots by Age Group and Gender')

