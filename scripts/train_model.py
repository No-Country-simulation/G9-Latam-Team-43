import argparse
import joblib

from pathlib import Path
from sklearn.metrics import f1_score

from src.dataset_loader import DatasetLoader
from src.model_trainer import ModelTrainer
from src.model_evaluator import ModelEvaluator
from src.config import (
    DATASET_PATH,
    CLEAN_TEXT_COLUMN,
    TARGET_COLUMN,
    TEST_SIZE,
    RANDOM_STATE,
    MODEL_PATH,
    METRICS_PATH0,
    CONFUSION_MATRIX_PATH0
)


def main():
    parser = argparse.ArgumentParser(
        description="Train and evaluate the text classification model."
    )

    parser.add_argument(
        "--dataset_path",
        type=str,
        default=str(DATASET_PATH),
        help="Path to the dataset CSV file."
    )

    args = parser.parse_args()

    print(
        f"--- Cargando dataset desde: "
        f"{args.dataset_path} ---"
    )

    loader = DatasetLoader(args.dataset_path)

    config = {
        "clean_text_column": CLEAN_TEXT_COLUMN,
        "category_column": TARGET_COLUMN,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE
    }

    trainer = ModelTrainer(config)

    # ModelTrainer y ModelEvaluator trabajan con objetos Path.
    model_path = Path(MODEL_PATH)
    metrics_path = Path(METRICS_PATH0)
    confusion_matrix_path = Path(CONFUSION_MATRIX_PATH0)

    # DatasetLoader.prepare() devuelve X e y.
    X, y = loader.prepare()

    # Crear el mismo conjunto de prueba utilizado por ModelTrainer.
    _, X_test, _, y_test = trainer.split_data(X, y)

    # Aplicar la misma limpieza de texto usada durante el entrenamiento.
    X_test_cleaned = X_test.apply(
        trainer.text_cleaner.clean
    )

    # Entrenar y evaluar.
    result = trainer.train_and_evaluate(X, y)

    # El modelo entrenado queda almacenado en trainer.model.
    trained_model = trainer.model

    # Predecir sobre el conjunto de prueba.
    y_pred = trained_model.predict(X_test_cleaned)

    # Construir métricas compatibles con JSON.
    metrics = {
        "accuracy": float(result["accuracy"]),
        "macro_f1": float(
            f1_score(
                y_test,
                y_pred,
                average="macro"
            )
        ),
        "report": result["report"]
    }

    print("\n--- Guardando Artefactos ---")

    # Guardar el pipeline entrenado.
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(trained_model, model_path)
    print(f"✅ Pipeline guardado en: {model_path}")

    # Guardar las métricas.
    evaluator = ModelEvaluator()
    evaluator.save_metrics(metrics, metrics_path)
    print(f"✅ Métricas guardadas en: {metrics_path}")

    # Guardar la matriz de confusión.
    evaluator.save_confusion_matrix(
        trained_model,
        X_test_cleaned,
        y_test,
        confusion_matrix_path
    )

    print(
        f"✅ Matriz de confusión guardada en: "
        f"{confusion_matrix_path}"
    )

    print("\n--- Entrenamiento Completado Exitosamente ---")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Macro: {metrics['macro_f1']:.4f}")


if __name__ == "__main__":
    main()