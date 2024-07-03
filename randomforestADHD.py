import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
import joblib


df = pd.read_csv('training_data/adhd_year_excluded.csv')

# Features are age groups, sex, race, ethnicity, Target is Diagnosis with ADHD
features = df.drop(columns=['Total Individuals with Diagnosis of ADHD'])
target = df['Total Individuals with Diagnosis of ADHD']

model = RandomForestClassifier(random_state=15)
model.fit(features, target)

# Save model to a file so that it doesn't have to reran
# joblib.dump(model, 'adhd_diagnosis_prediction_model.pkl')

# Example data for a single individual
single_individual_data = {
    'Male': 1,  # Example: 1 for Male, 0 for Female
    'Female': 0,  # Example: 0 for Female, 1 for Male
    '0-11 Years': 0,  # Example: Age group feature values
    '12-14 Years': 0,
    '15-17 Years': 0,
    '18-20 Years': 0,
    '21-24 Years': 0,
    '25-29 Years': 0,
    '30-34 Years': 1,
    '35-39 Years': 0,
    '40-44 Years': 0,
    '45-49 Years': 0,
    '50-54 Years': 0,
    '55-59 Years': 0,
    '60-64 Years': 0,
    '65 Years and Older': 0,
    'American Indian or Alaska Native': 0,  # Example: Race feature values
    'Asian': 0,
    'Black or African American': 0,
    'Native Hawaiian or Other Pacific Islander': 1,
    'White': 0,
    'Other': 0,
    'Not of Hispanic or Latino Origin': 1,  # Example: Ethnicity feature values
    'Hispanic or Latino Origin': 0
}

# Convert single individual data to DataFrame
single_df = pd.DataFrame([single_individual_data])

# Make prediction using the loaded model
likelihood_of_diagnosis = model.predict_proba(single_df)[:, 1]  # Predict probability of positive class

print(f"Likelihood of ADHD diagnosis: {likelihood_of_diagnosis[0]:.2%}")