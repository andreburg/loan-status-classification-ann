from flask import Flask, request
from preprocess_data import preprocess_data
from flask_cors import CORS
import pandas as pd
import joblib
from prepare_data import load_csv
from train_models import get_predicted
import plotly.express as px

app = Flask(__name__)
CORS(app)

model = joblib.load('artifacts/model_2.pkl')

@app.route('/predict', methods=['POST'])
def predict_loan_approval():

    df = load_csv('artifacts/predictions_web.csv')

    loan_id = f"LP00{max([int(loan_id[2:]) for loan_id in df['loan_id']]) + 1}"
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
    df = pd.concat([df, input_df])

    file_path = 'artifacts/predictions_web.csv'

    df.to_csv(file_path, index=False)
    
    return input_df.to_json(orient='records')

@app.route('/loans/predict', methods=['GET'])
def get_predict_loans():
    df = load_csv('artifacts/predictions_web.csv')
    df = get_predicted(df, model,'artifacts/predictions_web.csv')

    return df.to_json(orient='records')

@app.route('/loans', methods=['GET'])
def get_loans():
    df = load_csv('artifacts/predictions_web.csv')
    return df.to_json(orient='records')

@app.route('/analytics/loan_status_hist', methods=['GET'])
def get_loan_status_hist():
    df = load_csv('artifacts/predictions_web.csv')
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
    df = load_csv('artifacts/feature_importance.csv')
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
