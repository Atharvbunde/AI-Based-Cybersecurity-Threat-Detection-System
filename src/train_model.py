import os
import joblib
from typing import Dict, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_models(X_train, X_test, y_train, y_test) -> Tuple[Dict, Dict]:
    """
    Train multiple models and return them with evaluation metrics.
    """
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=120,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        ),
    }

    trained_models = {}
    results = {}

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        trained_models[model_name] = model
        results[model_name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
        }

    # Optional anomaly model for industry-style extension
    iso = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    iso.fit(X_train)
    trained_models["Isolation Forest"] = iso

    return trained_models, results


def save_best_model(model, preprocessor, model_name: str, save_dir: str) -> None:
    """
    Save best classification model and preprocessor.
    """
    os.makedirs(save_dir, exist_ok=True)

    safe_name = model_name.lower().replace(" ", "_")
    joblib.dump(model, os.path.join(save_dir, f"{safe_name}_model.pkl"))
    joblib.dump(preprocessor, os.path.join(save_dir, "preprocessor.pkl"))