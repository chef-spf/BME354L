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

# Fit the mixed-effects model
md = mixedlm("heart_rate ~ treatment + exercise + sleep + caffeine", cleaned_data, groups=cleaned_data["subject"],
             re_formula="~treatment")
mdf = md.fit()

# Print the model results
print(mdf.summary())

#%% Data visualization
# Box plots by treatment
sns.boxplot(x='treatment', y='heart_rate', data=cleaned_data)
plt.title('Heart Rate Distribution by Treatment')
plt.xlabel('Treatment')
plt.ylabel('Heart Rate')
plt.show()

#%% Testing assumptions about our model
# Checking normality of residuals
residuals = mdf.resid
_, p_value = shapiro(residuals)
print(f'Normality test p-value: {p_value}')

# Plotting residuals to check homoscedasticity
plt.figure(figsize=(10, 6))
plt.scatter(mdf.fittedvalues, residuals)
plt.title('Residuals vs. Predicted Values')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()

# Preparing data for checking multicollinearity
# Note: This requires numerical data, so ensure the treatment variable is suitably encoded if needed, or use subset of data
predictors = cleaned_data[['exercise', 'sleep', 'caffeine']]
predictors = sm.add_constant(predictors)  # adding a constant for the VIF calculation

# Calculate and print VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = predictors.columns
vif_data["VIF"] = [variance_inflation_factor(predictors.values, i) for i in range(predictors.shape[1])]
print(vif_data)


