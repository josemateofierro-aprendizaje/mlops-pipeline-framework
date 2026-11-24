import argparse

from src.prepare_data import prepare_iris
from src.validate_data import validate_data
from src.train import train_model
from src.evaluate import evaluate_model


def run_pipeline(config_path, prepare_iris_data=False):

    print("\n========== INICIO DEL PIPELINE ==========")

    # Paso 1: Preparación inicial de Iris
    if prepare_iris_data:

        print("\n1. Preparando dataset...")
        prepare_iris()

    # Paso 2: Validación de calidad
    print("\n2. Validando datos...")

    import json

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    errors = validate_data(
        config["data_path"],
        config["contract_path"]
    )

    if errors:

        print("Pipeline detenido por errores de calidad:")

        for error in errors:
            print("-", error)

        raise SystemExit(1)

    print("Datos aprobados.")

    # Paso 3: Entrenamiento
    print("\n3. Entrenando modelo...")
    train_model(config_path)

    # Paso 4: Evaluación
    print("\n4. Evaluando modelo...")
    evaluate_model(config_path)

    print("\n========== PIPELINE FINALIZADO ==========")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        default="configs/iris.json"
    )

    parser.add_argument(
        "--prepare-iris",
        action="store_true"
    )

    args = parser.parse_args()

    run_pipeline(
        args.config,
        args.prepare_iris
    )