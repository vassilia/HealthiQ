import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel file (update 'your_file.xlsx' with the actual filename)
file_path = "main.xlsx"
df = pd.read_excel(file_path)

# Convert 'BIRTH' (year of birth) to Age
current_year = 2024  # Adjust to the current year
df["Age"] = current_year - df["BIRTH"]

# Check data types and missing values
print(df.info())
