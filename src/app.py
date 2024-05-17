from flask import Flask, request
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from preprocess_data import preprocess_data
from flask_cors import CORS
import pandas as pd
import joblib
import plotly.express as px

load_dotenv()

app = Flask(__name__)
CORS(app, origins='*')

model = joblib.load('artifacts/model_2.pkl')

mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client['loan_prediction_db']
collection = db['loan_predictions']

@app.route('/predict', methods=['POST'])
def predict_loan_approval():

    latest_loan = collection.find_one(sort=[('loan_id', -1)])
    loan_id = f"LP00{int(latest_loan['loan_id'][2:]) + 1}"

    input_data = request.get_json() 
    input_data['applicant_income'] = float(input_data['applicant_income'])
    input_data['coapplicant_income'] = float(input_data['coapplicant_income'])
    input_data['loan_amount'] = float(input_data['loan_amount'])
    input_data['loan_amount_term'] = float(input_data['loan_amount_term'])
    
    input_df = pd.DataFrame({key: [input_data[key]] for key in input_data.keys()})
    preprocessed_df = preprocess_data(raw_df=input_df, predict=True)
    y_pred_proba = model.predict(preprocessed_df)
    prediction = ["Approved" if val > 0.5 else "Rejected" for val in y_pred_proba]
    input_df['loan_status'] = prediction
    input_df['loan_id'] = [loan_id]

    for _, row in input_df.iterrows():
        collection.insert_one(row.to_dict())
    
    return input_df.to_json(orient='records')

def get_full_df():
    col = collection.find()
    col_list = list(col)
    df = pd.DataFrame(col_list)
    df.drop(columns=['_id'], inplace=True)
    return df

@app.route('/loans', methods=['GET'])
def get_loans():
    df = pd.DataFrame()
    try:
        df = get_full_df()
    except:
        pass
    return df.to_json(orient='records')

@app.route('/analytics/loan_status_hist', methods=['GET'])
def get_loan_status_hist():
    df = pd.DataFrame()
    try:
        df = get_full_df()
    except:
        pass
    fig = px.histogram(x=df['loan_status'])
    fig.update_layout(xaxis_title='Loan Status', yaxis_title='Frequency',
                height=600, width=800, title={
                    'text': "Application Outcomes",
                    'x': 0.5,
                    'xanchor': 'center' 
                })
    return fig.to_json()

@app.route('/analytics/feature_importance_bar', methods=['GET'])
def get_feature_importance_bar():
    df = pd.DataFrame()
    try:
        df = get_full_df()
    except:
        pass
    fig = px.bar(df, x='importance', y='attribute',
             orientation='h',
             labels={'importance': 'Importance', 'attribute': 'Attribute'})
    fig.update_layout(xaxis_title='Importance', yaxis_title='Attribute',
                    yaxis_categoryorder='total ascending',
                    height=600, width=800, title={
                    'text': "Feature Importance",
                    'x': 0.5,
                    'xanchor': 'center' 
                })
    return fig.to_json()

if __name__ == '__main__':
    app.run(debug=True)
