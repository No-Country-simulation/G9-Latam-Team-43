import json
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from src.config import RANDOM_STATE
from src.model_factory import ModelFactory
from src.model_evaluator import ModelEvaluator

class GridSearchOptimizer:
    """
    Realiza búsqueda de hiperparámetros mediante GridSearchCV 
    maximizando F1 Macro para TF-IDF y el clasificador.
    """
    def __init__(self, cv=5, scoring="f1_macro", n_jobs=-1):
        self.cv = cv
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.evaluator = ModelEvaluator()

    def optimize_logistic_regression(self, X_train, y_train):
        pipeline = ModelFactory.build_logistic_regression_pipeline()
        
        param_grid = {
            "tfidf__max_features": [2500, 5000, 8000],
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "tfidf__sublinear_tf": [True, False],
            "tfidf__min_df": [1, 2],
            "model__C": [0.5, 1.0, 2.0, 5.0],
            "model__class_weight": ["balanced", None]
        }

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            verbose=1
        )
        grid_search.fit(X_train, y_train)
        return grid_search

    def optimize_linear_svc(self, X_train, y_train):
        pipeline = ModelFactory.build_linear_svc_pipeline()
        
        param_grid = {
            "tfidf__max_features": [2500, 5000, 8000],
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "tfidf__sublinear_tf": [True, False],
            "model__C": [0.1, 0.5, 1.0, 2.0],
            "model__loss": ["squared_hinge", "hinge"],
            "model__class_weight": ["balanced", None]
        }

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            verbose=1
        )
        grid_search.fit(X_train, y_train)
        return grid_search
