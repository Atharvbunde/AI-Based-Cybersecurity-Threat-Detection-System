import os
import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load dataset from CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at: {file_path}\n"
            "Put your dataset file inside data/raw/ and name it nsl_kdd.csv"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("Loaded dataset is empty.")

    return df