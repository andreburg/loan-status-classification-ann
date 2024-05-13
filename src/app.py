from flask import Flask, jsonify, request
from preprocess_data import preprocess_data
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load('artifacts/model_3.pkl')

@app.route('/predict', methods=['POST'])
def predict_loan_approval():
    # Receive input data as JSON
    input_data = request.get_json()
    print(input_data)    
    # Extract features from input
    # gender = input_data['gender']
    # married = input_data['married']
    # dependents = input_data['dependents']
    # education = input_data['education']
    # self_employed = input_data['self_employed']
    # applicant_income = float(input_data['applicant_income'])
    # coapplicant_income = float(input_data['coapplicant_income'])
    # loan_amount = float(input_data['loan_amount'])
    # loan_amount_term = float(input_data['loan_amount_term'])
    # property_area = input_data['property_area']
    # credit_history = input_data['credit_history']

    input_data['applicant_income'] = float(input_data['applicant_income'])
    input_data['coapplicant_income'] = float(input_data['coapplicant_income'])
    input_data['loan_amount'] = float(input_data['loan_amount'])
    input_data['loan_amount_term'] = float(input_data['loan_amount_term'])
    
    input_df = pd.DataFrame({key: [input_data[key]] for key in input_data.keys()})
    print(input_df)
    preprocessed_df = preprocess_data(raw_df=input_df, predict=True)
    y_pred_proba = model.predict(preprocessed_df)
    prediction = ["Y" if val > 0.5 else "N" for val in y_pred_proba]

    if prediction[0] == "Y":
        result = {'loan_status': 'Approved'}
    else:
        result = {'loan_status': 'Not Approved'}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
