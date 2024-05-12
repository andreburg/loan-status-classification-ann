from skimpy import clean_columns
import pandas as pd
import pickle

load_csv = lambda dir: clean_columns(pd.read_csv(dir))

def prepare_data(raw_df):
    df = raw_df.copy()
    df = clean_columns(df)
    categorical_columns = ['gender', 'married', 'dependents', 'education', 'self_employed', 'credit_history', 'property_area']
    numeric_columns = ['applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term']

    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())
    return df[categorical_columns + numeric_columns]

def load_model(dir):
    with open(dir, 'rb') as file:
        return pickle.load(file)
    
def dump_model(dir, model):
    with open(dir, 'wb') as file:
        pickle.dump(model, file)