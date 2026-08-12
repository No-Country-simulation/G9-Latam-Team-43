import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from src.text_cleaner import TextCleaner
from src.model_factory import ModelFactory
from src.config import MODEL_PATH
import joblib # Import joblib

class ModelTrainer:
    def __init__(self, config):
        self.config = config
        self.clean_text_column = config.get('clean_text_column', 'clean_text')
        self.category_column = config.get('category_column', 'category')
        self.test_size = config.get('test_size', 0.2)
        self.random_state = config.get('random_state', 42)
        
        self.model = ModelFactory.build_logistic_regression_pipeline()
        self.text_cleaner = TextCleaner()

    def split_data(self, X, y): # Changed to accept X and y directly
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
        return X_train, X_test, y_train, y_test

    def train_and_evaluate(self, X, y):
        X_train, X_test, y_train, y_test = self.split_data(X, y)

        # Preprocess text - Apply the 'clean' method to each text in the Series
        X_train_cleaned = X_train.apply(self.text_cleaner.clean)
        X_test_cleaned = X_test.apply(self.text_cleaner.clean)
        
        # The model is a pipeline that includes TF-IDF vectorization, so no separate vectorization needed here.
        # Train model (pipeline will handle vectorization internally)
        self.model.fit(X_train_cleaned, y_train)

        # Save the trained model
        joblib.dump(self.model, MODEL_PATH)

        # Evaluate model
        y_pred = self.model.predict(X_test_cleaned)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return {"accuracy": accuracy, "report": report}
