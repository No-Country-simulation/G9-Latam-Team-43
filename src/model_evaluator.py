import json
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

class ModelEvaluator:
    """
    Evalúa el desempeño del modelo y genera reportes.
    """
    def evaluate(self, model, X_test, y_test) -> dict:
        y_pred = model.predict(X_test)
        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0
        )
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "macro_precision": report["macro avg"]["precision"],
            "macro_recall": report["macro avg"]["recall"],
            "macro_f1": report["macro avg"]["f1-score"],
            "weighted_f1": report["weighted avg"]["f1-score"],
            "classification_report": report
        }
        return metrics

    def save_metrics(self, metrics: dict, output_path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4, ensure_ascii=False)

    def save_confusion_matrix(self, model, X_test, y_test, output_path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        y_pred = model.predict(X_test)
        labels = sorted(y_test.unique())
        matrix = confusion_matrix(y_test, y_pred, labels=labels)
        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix,
            display_labels=labels
        )
        fig, ax = plt.subplots(figsize=(12, 8))
        display.plot(ax=ax, xticks_rotation=45, cmap="Blues")
        plt.title("Matriz de Confusión")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
