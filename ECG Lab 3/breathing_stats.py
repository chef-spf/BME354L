import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_excel('breathing_data.xlsx')

# Filter data for resting treatment
resting_data = data[data['treatment'] == 'resting']

# Convert caffeine to binary (1 for yes, 0 for no)
resting_data['caffeine'] = resting_data['caffeine'].map({'yes': 1, 'no': 0})

# Setup the regression model
model = smf.ols('heart_rate ~ exercise + caffeine + sleep', data=resting_data).fit()

# Print the summary of the regression model
print(model.summary())
