from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score
from preprocess_data import preprocess_data, label_encode
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from prepare_data import dump_model
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
import pandas as pd

def create_ANN(df, model, output_dir):
    X = df.drop(columns=['loan_status'], axis=1)
    y = label_encode(df['loan_status'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test)    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True
    )

    history = model.fit(X_train, y_train, epochs=250, batch_size=32, validation_split=0.2, callbacks=[early_stopping], verbose=0)
    dump_model(output_dir, model)

    print("done...")
    return (model, history, X_train, X_test, y_train, y_test)

def score(y_true, y_pred_proba):
    y_pred = (y_pred_proba >= 0.5).astype(int)
    accuracy = accuracy_score(y_true, y_pred)
    return accuracy

def get_feature_importance(model, X_val, y_val):
    def scoring_wrapper(estimator, X, y):
        y_pred_proba = estimator.predict(X)
        return score(y, y_pred_proba)
    
    result = permutation_importance(model, X_val, y_val, scoring=scoring_wrapper, n_repeats=10, random_state=42)
    categorical_columns = ['gender', 'married', 'dependents', 'education', 'self_employed', 'credit_history', 'property_area']
    numeric_columns = ['applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term']
    return pd.DataFrame({'attribute': categorical_columns+numeric_columns, 'importance': result.importances_mean})
    

def get_model_performance(model, history, X_test, y_test):
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = [1 if val > 0.5 else 0 for val in y_pred_proba]
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(["Loss", "Validation Loss"])
    plt.title("Binary Cross-Entropy Loss")
    plt.show()
    
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.legend(["Accuracy", "Validation Accuracy"])
    plt.title("Accuracy")
    plt.show()
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True)
    plt.xlabel('Predicted Value')
    plt.ylabel('Actual Value')
    plt.title("Confusion Matrix")
    plt.show()
    
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print("Performance Metrics:")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Loss: {loss:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")

def get_model_performance_minimal(model, X_test, y_test):
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = [1 if val > 0.5 else 0 for val in y_pred_proba]
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print("Performance Metrics:")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Loss: {loss:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")

def get_predicted(raw_df, model, output_dir='../artifacts/predictions.csv'):
    df = raw_df.copy()
    X = preprocess_data(df)
    df['loan_status'] = ['Y' if val > 0.5 else 'N' for val in model.predict(X)]
    df.to_csv(output_dir, sep=',')
    print(f'PREDICTION SAVED TO: {output_dir}')
    return df