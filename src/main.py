from train_models import create_ANN, get_model_performance_minimal, get_predicted
from prepare_data import load_model, load_csv
from datetime import date
import tensorflow as tf
import pandas as pd
from preprocess_data import preprocess_data

def initialize_ANN(df, output_dir=f'/artifacts/model_{date.today()}.pkl'):
    categorical_columns = ['gender', 'married', 'dependents', 'education', 'self_employed', 'credit_history', 'property_area']
    numeric_columns = ['applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term']
    (model, _, _, X_test, _, y_test) = create_ANN(
        df,
        tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(len(categorical_columns + numeric_columns),)),
        tf.keras.layers.Dense(11, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(7, activation='relu'),
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]), output_dir)
    get_model_performance_minimal(model, X_test, y_test)
    return output_dir
    


def main():
    validation_df = load_csv('data/validation.csv')
    training_df = load_csv('data/raw_data.csv')

    # model_2_dir = initialize_ANN(training_df, output_dir="artifacts/model_2.pkl")
    model_2 = load_model("artifacts/model_2.pkl")
    # get_predicted(validation_df, model_2, 'artifacts/predictions_2.csv')


if __name__ == '__main__':
    main()