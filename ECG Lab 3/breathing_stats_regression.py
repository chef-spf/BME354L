import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.formula.api as smf

# Load the data
data = pd.read_excel('breathing_data.xlsx')

# Convert 'caffeine' from yes/no to 1/0
data['caffeine'] = data['caffeine'].map({'yes': 1, 'no': 0})

# Drop rows with any missing values
cleaned_data = data.dropna()
#%%
# Filtering data for 'resting' treatment
resting_data = cleaned_data[cleaned_data['treatment'] == 'resting']

#%% Linear regression models
# Model 1: Resting Heart Rate as a function of Exercise Hours
model_exercise = smf.ols('heart_rate ~ exercise', data=resting_data).fit()

# Model 2: Resting Heart Rate as a function of Sleep Hours
model_sleep = smf.ols('heart_rate ~ sleep', data=resting_data).fit()

# Print the summaries of both models
print("Regression Model: Resting Heart Rate vs. Exercise Hours")
print(model_exercise.summary())
print("\nRegression Model: Resting Heart Rate vs. Sleep Hours")
print(model_sleep.summary())

# Data for plots
resting_data = data[data['treatment'] == 'resting']

# Setting up the visualization environment
plt.figure(figsize=(14, 6))

# Plot 1: Resting Heart Rate vs. Exercise Hours
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
sns.regplot(x='exercise', y='heart_rate', data=resting_data, color='b', line_kws={'label':"y={0:.1f}x+{1:.1f}\n$R^2$={2:.2f}".format(model_exercise.params['exercise'], model_exercise.params['Intercept'], model_exercise.rsquared)})
plt.title('Resting Heart Rate vs. Exercise Hours')
plt.xlabel('Exercise (hrs/week)')
plt.ylabel('Heart Rate (BPM)')
plt.legend()

# Plot 2: Resting Heart Rate vs. Sleep Hours
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
sns.regplot(x='sleep', y='heart_rate', data=resting_data, color='g', line_kws={'label':"y={0:.1f}x+{1:.1f}\n$R^2$={2:.2f}".format(model_sleep.params['sleep'], model_sleep.params['Intercept'], model_sleep.rsquared)})
plt.title('Resting Heart Rate vs. Sleep Hours')
plt.xlabel('Sleep (hrs over 72hr period)')
plt.ylabel('Heart Rate (BPM)')
plt.legend()
plt.show()
