import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


def load_config(config_path):

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_model(config):

    numeric_features = config["numeric_features"]
    categorical_features = config["categorical_features"]

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    transformers = []

    if numeric_features:
        transformers.append(
            ("numeric", numeric_pipeline, numeric_features)
        )

    if categorical_features:
        transformers.append(
            ("categorical", categorical_pipeline, categorical_features)
        )

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    if config["task"] == "classification":

        estimator = RandomForestClassifier(
            n_estimators=100,
            random_state=config["random_state"]
        )

    elif config["task"] == "regression":

        estimator = RandomForestRegressor(
            n_estimators=100,
            random_state=config["random_state"]
        )

    else:
        raise ValueError("Tipo de tarea no soportado.")

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("estimator", estimator)
    ])

    return model


def train_model(config_path):

    config = load_config(config_path)

    dataset_name = config["dataset_name"]
    data = pd.read_csv(config["data_path"])

    target = config["target"]

    features = (
        config["numeric_features"]
        + config["categorical_features"]
    )

    X = data[features]
    y = data[target]

    stratify = y if config["task"] == "classification" else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["test_size"],
        random_state=config["random_state"],
        stratify=stratify
    )

    model = build_model(config)

    model.fit(X_train, y_train)

    # Guardar modelo
    model_path = Path("models")
    model_path.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        model,
        model_path / f"{dataset_name}_model.joblib"
    )

    # Guardar datos de prueba para evaluación
    test_path = Path("data/processed")
    test_path.mkdir(parents=True, exist_ok=True)

    test_data = X_test.copy()
    test_data[target] = y_test

    test_data.to_csv(
        test_path / f"{dataset_name}_test.csv",
        index=False
    )

    print("Entrenamiento finalizado correctamente.")
    print("Registros de entrenamiento:", len(X_train))
    print("Registros de prueba:", len(X_test))


if __name__ == "__main__":

    train_model("configs/iris.json")