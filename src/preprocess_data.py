from sklearn.preprocessing import StandardScaler, LabelEncoder
from prepare_data import prepare_data

label_encoder = LabelEncoder()

def preprocess_data(raw_df):
    df = raw_df.copy()
    df = prepare_data(df)
    standard_scaler = StandardScaler()
    categorical_columns = ['gender', 'married', 'dependents', 'education', 'self_employed', 'credit_history', 'property_area']
    numeric_columns = ['applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term']
    for col in categorical_columns:
        df[col] = label_encode(df[col])
    
    df = standard_scaler.fit_transform(df)
    
    return df

label_encode = lambda series: label_encoder.fit_transform(series.copy())