from src.config import MODEL_PATH
from src.predictor import TechMindPredictor

def main():
    predictor = TechMindPredictor(MODEL_PATH)

    text = """
    I am writing a complex SQL query with multiple JOINs in PostgreSQL,
    but my window function is returning duplicate rows and slowing down the database.
    """

    result = predictor.predict(text)
    print("Resultado de clasificación")
    print(result)

if __name__ == "__main__":
    main()
