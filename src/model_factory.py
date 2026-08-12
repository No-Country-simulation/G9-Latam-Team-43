from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

class ModelFactory:
    """
    Construye pipelines de clasificación de texto.
    """
    @staticmethod
    def build_logistic_regression_pipeline() -> Pipeline:
        return Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                    sublinear_tf=True
                )
            ),
            (
                "model",
                LogisticRegression(
                    C=2.0,
                    class_weight="balanced",
                    solver="lbfgs",
                    max_iter=1000,
                    random_state=42,
                    n_jobs=-1
                )
            )
        ])

    @staticmethod
    def build_linear_svc_pipeline() -> Pipeline:
        return Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                    sublinear_tf=True
                )
            ),
            (
                "model",
                LinearSVC(
                    C=1.0,
                    loss="squared_hinge",
                    class_weight="balanced",
                    max_iter=3000,
                    random_state=42
                )
            )
        ])

    @staticmethod
    def build_ensemble_pipeline() -> Pipeline:
        logistic_model = LogisticRegression(
            C=2.0,
            class_weight="balanced",
            solver="lbfgs",
            max_iter=1000,
            random_state=42,
            n_jobs=-1
        )
        svm_model = CalibratedClassifierCV(
            LinearSVC(
                C=1.0,
                loss="squared_hinge",
                class_weight="balanced",
                max_iter=3000,
                random_state=42
            ),
            cv=3
        )
        random_forest_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features="sqrt",
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
        ensemble = VotingClassifier(
            estimators=[
                ("lr", logistic_model),
                ("svm", svm_model),
                ("rf", random_forest_model)
            ],
            voting="soft",
            weights=[1.5, 2.0, 1.0],
            n_jobs=-1
        )
        return Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                    sublinear_tf=True
                )
            ),
            ("model", ensemble)
        ])
