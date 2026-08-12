import json
import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os # Import the os module
from src.dataset_loader import DatasetLoader
from src.model_trainer import ModelTrainer
from src.model_factory import ModelFactory
from src.text_cleaner import TextCleaner
from src.config import (
    DATASET_PATH, CLEAN_TEXT_COLUMN, TARGET_COLUMN,
    TEST_SIZE, RANDOM_STATE, MODEL_PATH,
    METRICS_PATH, CONFUSION_MATRIX_PATH
)

def main():
    print("--- 1. Carga y Preparación del Dataset ---")
    loader = DatasetLoader(DATASET_PATH)
    X, y = loader.prepare()

    # Use a dummy trainer to get cleaned text and split data
    config_for_trainer = {
        'clean_text_column': CLEAN_TEXT_COLUMN,
        'category_column': TARGET_COLUMN,
        'test_size': TEST_SIZE,
        'random_state': RANDOM_STATE
    }
    trainer_dummy = ModelTrainer(config_for_trainer) # Pass a valid config
    X_train, X_test, y_train, y_test = trainer_dummy.split_data(X, y)

    text_cleaner = TextCleaner()
    X_train_cleaned = X_train.apply(text_cleaner.clean)
    X_test_cleaned = X_test.apply(text_cleaner.clean)

    print("--- 2. Definición del Modelo Base y Espacio de Hiperparámetros ---")
    pipeline = ModelFactory.build_logistic_regression_pipeline() # Get the base pipeline

    # Define the parameter grid for GridSearchCV
    param_grid = {
        'tfidf__ngram_range': [(1, 1), (1, 2)], # Uni-grams and bi-grams
        'tfidf__max_df': [0.75, 1.0],
        'model__C': [0.1, 1, 10] # Regularization parameter, changed from logreg__C
    }

    print("--- 3. Optimización de Hiperparámetros (Grid Search) ---")
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, verbose=2, n_jobs=-1, scoring='accuracy') # Changed cv back to 5
    grid_search.fit(X_train_cleaned, y_train)

    best_pipeline = grid_search.best_estimator_
    print(f"Mejores parámetros encontrados: {grid_search.best_params_}")

    print("--- 4. Evaluación del Modelo Optimizado ---")
    y_pred = best_pipeline.predict(X_test_cleaned)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f"Precisión del modelo optimizado: {accuracy:.4f}")
    print("Reporte de Clasificación:\n", report)

    # Guardar métricas de optimización
    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    metrics = {
        "best_params": grid_search.best_params_,
        "optimized_accuracy": accuracy,
        "classification_report": report
    }
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Métricas de optimización guardadas en {METRICS_PATH}")

    # Guardar matriz de confusión como imagen
    os.makedirs(os.path.dirname(CONFUSION_MATRIX_PATH), exist_ok=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=best_pipeline.classes_, yticklabels=best_pipeline.classes_)
    plt.title('Matriz de Confusión del Modelo Optimizado')
    plt.ylabel('Etiqueta Verdadera')
    plt.xlabel('Etiqueta Predicha')
    plt.savefig(CONFUSION_MATRIX_PATH)
    print(f"Matriz de confusión guardada en {CONFUSION_MATRIX_PATH}")

    print("--- 5. Guardado del Modelo Optimizado ---")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)
    print(f"Modelo optimizado guardado en {MODEL_PATH}")

if __name__ == "__main__":
    main()
