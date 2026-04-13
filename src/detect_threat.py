import os
import pandas as pd
import numpy as np


def generate_threat_alerts(model, X_test, y_test, save_dir: str) -> None:
    """
    Generate CSV of suspicious predictions.
    """
    os.makedirs(save_dir, exist_ok=True)

    predictions = model.predict(X_test)

    results_df = pd.DataFrame({
        "actual_label": np.array(y_test),
        "predicted_label": predictions
    })

    results_df["alert"] = results_df["predicted_label"].apply(
        lambda x: "Suspicious Activity Detected" if x == 1 else "Normal Activity"
    )

    suspicious_df = results_df[results_df["predicted_label"] == 1]

    all_results_path = os.path.join(save_dir, "all_predictions.csv")
    suspicious_path = os.path.join(save_dir, "threat_alerts.csv")

    results_df.to_csv(all_results_path, index=False)
    suspicious_df.to_csv(suspicious_path, index=False)

    print(f"Saved all predictions to: {all_results_path}")
    print(f"Saved threat alerts to: {suspicious_path}")
    print(f"Total suspicious records detected: {len(suspicious_df)}")
    