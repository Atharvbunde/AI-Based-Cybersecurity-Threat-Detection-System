from src.data_loader import load_dataset
from src.preprocess import prepare_data
from src.train_model import train_models, save_best_model
from src.evaluate import evaluate_model, plot_confusion_matrix, plot_feature_importance
from src.detect_threat import generate_threat_alerts
import os


def main() -> None:
    raw_data_path = os.path.join("data", "raw", "nsl_kdd.csv")

    print("Loading dataset...")
    df = load_dataset(raw_data_path)
    print(f"Dataset loaded: {df.shape}")

    print("Preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor, feature_names = prepare_data(df)

    print("Training models...")
    models, results = train_models(X_train, X_test, y_train, y_test)

    print("\nModel Results:")
    for model_name, metrics in results.items():
        print(f"\n{model_name}")
        for metric_name, value in metrics.items():
            print(f"{metric_name}: {value:.4f}")

    best_model_name = max(results, key=lambda name: results[name]["f1_score"])
    best_model = models[best_model_name]
    print(f"\nBest model selected: {best_model_name}")

    os.makedirs("models", exist_ok=True)
    save_best_model(best_model, preprocessor, best_model_name, "models")

    print("\nEvaluating best model...")
    y_pred = best_model.predict(X_test)
    evaluate_model(y_test, y_pred, best_model_name)

    print("\nGenerating confusion matrix...")
    plot_confusion_matrix(y_test, y_pred, best_model_name, save_dir=os.path.join("outputs", "graphs"))

    if hasattr(best_model, "feature_importances_"):
        print("Generating feature importance plot...")
        plot_feature_importance(
            best_model=best_model,
            feature_names=feature_names,
            model_name=best_model_name,
            save_dir=os.path.join("outputs", "graphs"),
            top_n=15
        )

    print("Generating threat alerts...")
    generate_threat_alerts(
        model=best_model,
        X_test=X_test,
        y_test=y_test,
        save_dir=os.path.join("outputs", "predictions")
    )

    print("\nProject execution completed successfully.")


if __name__ == "__main__":
    main()