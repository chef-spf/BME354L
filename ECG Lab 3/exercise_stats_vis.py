import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_excel('exercise_data.xlsx')

# Convert 'exercise_duration' to numeric, treating "rest" as 0 seconds
data['exercise_duration_numeric'] = pd.to_numeric(data['exercise_duration'].replace('rest', '0').str.replace('s', ''), errors='coerce')

# Plot heart rate over exercise duration for each subject with a unique color
plt.figure(figsize=(12, 6))
sns.lineplot(x='exercise_duration_numeric', y='heart_rate', hue='subject', data=data, 
             marker='o', palette='tab20', linewidth=1)

# Remove the legend
plt.legend().remove()

# Add labels and title
plt.title('Heart Rate by Exercise Duration for Each Subject')
plt.xlabel('Exercise Duration (seconds)')
plt.ylabel('Heart Rate (BPM)')

# Set specific x-axis ticks
plt.xticks([0, 5, 15, 30, 60, 120])

plt.tight_layout()
plt.show()
