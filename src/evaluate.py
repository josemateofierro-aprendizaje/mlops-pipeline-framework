
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_model(config_path="configs/iris.json"):

    # Cargar configuración
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    dataset_name = config["dataset_name"]

    # Cargar modelo correspondiente al dataset
    model_path = Path("models") / f"{dataset_name}_model.joblib"
    model = joblib.load(model_path)

    # Cargar datos de prueba correspondientes
    test_path = Path("data/processed") / f"{dataset_name}_test.csv"
    test_data = pd.read_csv(test_path)

    target = config["target"]

    features = (
        config["numeric_features"]
        + config["categorical_features"]
    )

    X_test = test_data[features]
    y_test = test_data[target]

    # Generar predicciones
    predictions = model.predict(X_test)

    # Calcular métricas
    if config["task"] == "classification":

        metrics = {
            "accuracy": float(
                accuracy_score(y_test, predictions)
            ),
            "precision_macro": float(
                precision_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0
                )
            ),
            "recall_macro": float(
                recall_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0
                )
            ),
            "f1_macro": float(
                f1_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0
                )
            )
        }

    elif config["task"] == "regression":

        metrics = {
            "mae": float(
                mean_absolute_error(y_test, predictions)
            ),
            "rmse": float(
                mean_squared_error(y_test, predictions) ** 0.5
            ),
            "r2": float(
                r2_score(y_test, predictions)
            )
        }

    else:
        raise ValueError("Tipo de tarea no soportado.")

    # Crear carpeta de reportes
    report_path = Path("reports")
    report_path.mkdir(parents=True, exist_ok=True)

    # Guardar métricas independientes por dataset
    metrics_file = report_path / f"{dataset_name}_metrics.json"

    with open(metrics_file, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    print("\nEVALUACIÓN FINALIZADA")
    print(f"Dataset: {dataset_name}")
    print(json.dumps(metrics, indent=4))

    return metrics


if __name__ == "__main__":
    evaluate_model()
