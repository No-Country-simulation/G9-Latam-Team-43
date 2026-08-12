import joblib
from src.text_cleaner import TextCleaner

class TechMindPredictor:
    """
    Carga el pipeline entrenado y predice la categoría de nuevos textos.
    """
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
        self.cleaner = TextCleaner()

    def predict(self, text: str) -> dict:
        clean_text = self.cleaner.clean(text)
        category = self.model.predict([clean_text])[0]
        response = {
            "texto_limpio": clean_text,
            "categoria_predicha": category
        }

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba([clean_text])[0]
            classes = self.model.classes_
            top_results = sorted(
                zip(classes, probabilities),
                key=lambda item: item[1],
                reverse=True
            )[:3]
            response["top_categorias"] = [
                {
                    "categoria": category_name,
                    "probabilidad": round(float(probability), 4)
                }
                for category_name, probability in top_results
            ]
            response["confianza"] = response["top_categorias"][0]["probabilidad"]

        return response
