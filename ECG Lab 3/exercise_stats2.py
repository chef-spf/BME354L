import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm

# Load data
data = pd.read_excel('exercise_data.xlsx')

# Convert 'caffeine' from yes/no to 1/0
data['caffeine'] = data['caffeine'].map({'yes': 1, 'no': 0})

# Ensure 'exercise_duration' is treated as a categorical variable with 'rest' as the reference
data['exercise_duration'] = pd.Categorical(data['exercise_duration'], categories=['rest', '5s', '15s', '30s', '60s', '120s'], ordered=True)



#%%

# Drop rows with any missing values
cleaned_data = data.dropna()

# Define the model with a simpler random effects structure
md = mixedlm("heart_rate ~ C(exercise_duration) + exercise_level + sleep_level + caffeine", cleaned_data, 
             groups=cleaned_data["subject"])
mdf = md.fit()

# Print the results
print(mdf.summary())