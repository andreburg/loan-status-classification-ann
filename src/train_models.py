from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from preprocess_data import preprocess_data
from sklearn.model_selection import train_test_split
from prepare_data import dump_model
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

def create_ANN(df, model, output_dir):
    X = df.drop(columns=['loan_status'], axis=1)
    y = LabelEncoder().fit_transform(df['loan_status'])
    
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