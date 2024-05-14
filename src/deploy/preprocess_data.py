from sklearn.preprocessing import StandardScaler, LabelEncoder
from prepare_data import prepare_data
import pickle

def preprocess_data(raw_df, predict=False):
    df = raw_df.copy()
    df = prepare_data(df)
    
    categorical_columns = ['gender', 'married', 'dependents', 'education', 'self_employed', 'credit_history', 'property_area']
    numeric_columns = ['applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term']

    label_encoders = {column: LabelEncoder() for column in categorical_columns}
    standard_scaler = StandardScaler()

    if predict:   
        with open('artifacts/label_encoder.pkl', 'rb') as le_file:
            label_encoders = pickle.load(le_file)

        with open('artifacts/standard_scaler.pkl', 'rb') as ss_file:
            standard_scaler = pickle.load(ss_file)
        
        for col in categorical_columns:
            df[col] = label_encoders[col].transform(df[col].copy())


        df[numeric_columns] = standard_scaler.transform(df[numeric_columns].copy())

    else:
        for col in categorical_columns:
            df[col] = label_encoders[col].fit_transform(df[col].copy())

        df[numeric_columns] = standard_scaler.fit_transform(df[numeric_columns].copy())

        with open('artifacts/label_encoder.pkl', 'wb') as le_file:
            pickle.dump(label_encoders, le_file)

        with open('artifacts/standard_scaler.pkl', 'wb') as ss_file:
            pickle.dump(standard_scaler, ss_file)

    return df