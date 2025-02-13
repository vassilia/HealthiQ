import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Example dataset of ages
# Converting the provided ages into a dataset

# List of ages from the user
ages = []


# Define age bins and labels
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']

# Create a DataFrame
df = pd.DataFrame({'Age': ages})

# Create a new column for age bins
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

# Calculate the distribution
age_distribution = df['Age Group'].value_counts().sort_index()

# Display the distribution
import ace_tools as tools; tools.display_dataframe_to_user(name="Age Distribution", dataframe=age_distribution)

# Plot the distribution
age_distribution.plot(kind='bar', figsize=(10, 6), title='Age Distribution', xlabel='Age Groups', ylabel='Frequency')
plt.xticks(rotation=45)
plt.show()
