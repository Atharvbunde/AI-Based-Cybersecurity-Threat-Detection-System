import os
import matplotlib
matplotlib.use("Agg")   # important: use non-GUI backend

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix


def evaluate_model(y_true, y_pred, model_name: str) -> None:
    print(f"\nClassification Report for {model_name}:")
    print(classification_report(y_true, y_pred, target_names=["Normal", "Attack"], zero_division=0))


def plot_confusion_matrix(y_true, y_pred, model_name: str, save_dir: str) -> None:
    os.makedirs(save_dir, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(cm)

    ax.set_title(f"Confusion Matrix - {model_name}")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Normal", "Attack"])
    ax.set_yticklabels(["Normal", "Attack"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    plt.tight_layout()
    save_path = os.path.join(
        save_dir,
        f"{model_name.lower().replace(' ', '_')}_confusion_matrix.png"
    )
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_feature_importance(best_model, feature_names, model_name: str, save_dir: str, top_n: int = 15) -> None:
    os.makedirs(save_dir, exist_ok=True)

    importances = best_model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    selected_features = [feature_names[i] for i in indices]
    selected_importances = importances[indices]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(selected_features[::-1], selected_importances[::-1])
    ax.set_xlabel("Importance")
    ax.set_ylabel("Features")
    ax.set_title(f"Top {top_n} Feature Importances - {model_name}")

    plt.tight_layout()
    save_path = os.path.join(
        save_dir,
        f"{model_name.lower().replace(' ', '_')}_feature_importance.png"
    )
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)