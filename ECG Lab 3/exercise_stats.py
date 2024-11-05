import pandas as pd
import pingouin as pg
from scipy.stats import levene
from scipy.stats import shapiro
from statsmodels.stats.anova import AnovaRM
import statsmodels.formula.api as smf

#%% Load the data file
df = pd.read_excel("exercise_data.xlsx")  # Replace with your file path if different
df['heart_rate'] = pd.to_numeric(df['heart_rate'], errors='coerce')
df = df.dropna(subset=['heart_rate'])

# Categorize weekly_exercise into binary levels
df['fitness_category'] = pd.cut(df['exercise_level'], bins=[0, 4, 8], labels=['low', 'high'])

# Categorize sleep_level into levels
df['sleep_category'] = pd.cut(df['sleep_level'], bins=[15, 18, 21, 24.1], labels=['low', 'moderate', 'high'])

df['caffeine'] = df['caffeine'].astype('category')


#%% Assumptions
# Test for Sphericity
sphericity = pg.sphericity(data=df, dv='heart_rate', subject='subject', within='exercise_duration')
print(sphericity)

# Normality
normality_results = {
    exercise_duration: shapiro(df[df['exercise_duration'] == exercise_duration]['heart_rate'].dropna())
    for exercise_duration in df['exercise_duration'].unique()
}
print("Normality Results:", normality_results)

# Homogeneity of variance 
levene_result = levene(
    *[df[df['exercise_duration'] == duration]['heart_rate'].dropna() for duration in df['exercise_duration'].unique()]
)
print("Levene’s Test across exercise_duration levels:", levene_result)

# Independence of Observations ?

#%% Run the repeated measures ANOVA
aovrm = AnovaRM(df, 'heart_rate', 'subject', within=['exercise_duration'])
res = aovrm.fit()
print(res.summary())

# Posthoc testing
posthocs = pg.pairwise_tests(data=df, dv='heart_rate', within='exercise_duration', subject='subject', padjust='bonferroni')
print(posthocs)
#%% Run mixed ANOVAS, if interaction terms are significant, suggests that effect of 
# exercise_duration on heart_rate varies based on weekly_exercise or sleep_level

# Run mixed ANOVA for weekly_exercise, 
mixed_anova_exercise = pg.mixed_anova(data=df, dv='heart_rate', within='exercise_duration', between='fitness_category', subject='subject')
print("Mixed ANOVA with weekly_exercise as between-subject factor:")
print(mixed_anova_exercise)

# Run mixed ANOVA for sleep_level
mixed_anova_sleep = pg.mixed_anova(data=df, dv='heart_rate', within='exercise_duration', between='sleep_category', subject='subject')
print("Mixed ANOVA with sleep_level as between-subject factor:")
print(mixed_anova_sleep)



