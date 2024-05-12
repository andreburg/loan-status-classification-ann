import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
from preprocess_data import preprocess_data

model = joblib.load('artifacts/model_2.pkl')

app = dash.Dash(__name__)

gender_options = [{'label': str(i), 'value': i} for i in ['Male', 'Female']]
married_options = [{'label': str(i), 'value': i} for i in ['Yes', 'No']]
dependents_options = [{'label': str(i), 'value': i} for i in ['0', '1', '2', '3+']]
education_options = [{'label': str(i), 'value': i} for i in ['Graduate', 'Not Graduate']]
self_employed_options = [{'label': str(i), 'value': i} for i in ['Yes', 'No']]
property_area_options = [{'label': str(i), 'value': i} for i in ['Rural', 'Semi-Urban', 'Urban']]


[{'label': str(i), 'value': i} for i in ['Rural', 'Semi-Urban', 'Urban']]

app.layout = html.Div([
    html.H1("Loan Approval Prediction"),

    # Input form
    html.Div([
        html.Label("Gender:"),
        dcc.Dropdown(id='input-gender', options=gender_options, value='Male'),
        html.Label("Marital Status:"),
        dcc.Dropdown(id='input-married', options=married_options, value='Yes'),
        html.Label("Dependents:"),
        dcc.Dropdown(id='input-dependents', options=dependents_options, value='0'),
        html.Label("Education:"),
        dcc.Dropdown(id='input-education', options=education_options, value='Graduate'),
        html.Label("Self Employed:"),
        dcc.Dropdown(id='input-self-employed', options=self_employed_options, value='No'),
        html.Label("Applicant Income:"),
        dcc.Input(id='input-applicant-income', type='number', value=5000),
        html.Label("Coapplicant Income:"),
        dcc.Input(id='input-coapplicant-income', type='number', value=0),
        html.Label("Loan Amount:"),
        dcc.Input(id='input-loan-amount', type='number', value=50000),
        html.Label("Loan Amount Term:"),
        dcc.Input(id='input-loan-amount-term', type='number', value=360),
        html.Label("Property Area:"),
        dcc.Dropdown(id='input-property-area', options=property_area_options, value='Rural'),
        html.Label("Credit History:"),
        dcc.RadioItems(
            id='input-credit-history',
            options=[
                {'label': 'Yes', 'value': 1.0},
                {'label': 'No', 'value': 0.0}
            ],
            value=1
        ),
        html.Button('Predict', id='submit-val', n_clicks=0),
    ]),
    html.Div(id='output-prediction')
])

@app.callback(
    Output('output-prediction', 'children'),
    [Input('submit-val', 'n_clicks')],
    [
        Input('input-gender', 'value'),
        Input('input-married', 'value'),
        Input('input-dependents', 'value'),
        Input('input-education', 'value'),
        Input('input-self-employed', 'value'),
        Input('input-applicant-income', 'value'),
        Input('input-coapplicant-income', 'value'),
        Input('input-loan-amount', 'value'),
        Input('input-loan-amount-term', 'value'),
        Input('input-property-area', 'value'),
        Input('input-credit-history', 'value')
    ]
)
def update_output(n_clicks, gender, married, dependents, education, self_employed,
                  applicant_income, coapplicant_income, loan_amount, loan_amount_term,
                  property_area, credit_history):
    if n_clicks > 0:
        # Prepare input data
        input_data = {
            'gender': [gender],
            'married': [married],
            'dependents': [dependents],
            'education': [education],
            'self_employed': [self_employed],
            'applicant_income': [float(applicant_income)],
            'coapplicant_income': [float(coapplicant_income)],
            'loan_amount': [float(loan_amount)],
            'loan_amount_term': [float(loan_amount_term)],
            'property_area': [property_area],
            'credit_history': [credit_history]
        }
        input_df = pd.DataFrame(input_data)
        print(input_data)
        preprocessed_df = preprocess_data(raw_df=input_df, predict=True)
        y_pred_proba = model.predict(preprocessed_df)
        print(y_pred_proba)

        prediction = ["Y" if val > 0.5 else "N" for val in y_pred_proba]

        if prediction[0] == "Y":
            return 'Loan Approved!'
        else:
            return 'Loan Rejected.'

if __name__ == '__main__':
    app.run_server(debug=True)