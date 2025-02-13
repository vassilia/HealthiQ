import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Example Data
data = pd.DataFrame({
    "Age Group": ["0-12", "13-18", "19-39", "40-65", "65+"],
    "Discharge Reason A": [10, 20, 30, 40, 50],
    "Discharge Reason B": [15, 25, 35, 45, 55],
    "Gender": ["Male", "Female", "Male", "Female", "Male"]
})

# Ensure the Gender column is valid
genders = data["Gender"].unique()
if len(genders) == 0:
    raise ValueError("No unique genders found in the data.")

# Update function for animation
def update(frame):
    plt.clf()
    heatmap_data = data[data["Gender"] == genders[frame]].drop(columns=["Gender"])
    heatmap_data = heatmap_data.set_index("Age Group")  # Set Age Group as index
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm")
    plt.title(f"Heatmap for {genders[frame]}")

# Animation
fig, ax = plt.subplots(figsize=(8, 6))
anim = FuncAnimation(fig, update, frames=len(genders), interval=2000, repeat=True)

# Save animation
anim.save("animated_heatmap.gif", writer="pillow")
