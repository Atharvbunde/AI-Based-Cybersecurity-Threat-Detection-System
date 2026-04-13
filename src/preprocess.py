from typing import Tuple, List
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def _find_target_column(df: pd.DataFrame) -> str:
    possible_targets = ["label", "attack", "class", "target"]
    for col in possible_targets:
        if col in df.columns:
            return col
    raise ValueError("Target column not found")


def _convert_target_to_binary(y: pd.Series) -> pd.Series:
    y_str = y.astype(str).str.lower().str.strip()
    normal_values = {"normal", "normal.", "benign", "0"}
    return y_str.apply(lambda value: 0 if value in normal_values else 1)


def prepare_data(df: pd.DataFrame) -> Tuple:
    df = df.copy()

    target_col = _find_target_column(df)
    df = df.dropna(subset=[target_col])

    y = _convert_target_to_binary(df[target_col])

    drop_cols = [target_col]
    if "difficulty_level" in df.columns:
        drop_cols.append("difficulty_level")

    X = df.drop(columns=drop_cols)

    X = X.drop_duplicates()
    y = y.loc[X.index]

    categorical_cols: List[str] = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols: List[str] = X.select_dtypes(exclude=["object"]).columns.tolist()

    numeric_transformer = Pipeline([
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    feature_names = []
    feature_names.extend(numeric_cols)

    if categorical_cols:
        encoder = preprocessor.named_transformers_["cat"].named_steps["onehot"]
        encoded_feature_names = encoder.get_feature_names_out(categorical_cols).tolist()
        feature_names.extend(encoded_feature_names)

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor, feature_names