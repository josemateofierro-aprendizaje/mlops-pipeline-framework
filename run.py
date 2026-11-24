
import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def run_step(description, command):

    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)

    result = subprocess.run(
        command,
        cwd=PROJECT_DIR
    )

    if result.returncode != 0:
        print(f"\nERROR: Falló la etapa: {description}")
        sys.exit(result.returncode)

    print(f"\nEtapa completada: {description}")


def main():

    parser = argparse.ArgumentParser(
        description="Framework genérico de automatización MLOps"
    )

    parser.add_argument(
        "--config",
        default="configs/iris.json",
        help="Ruta del archivo de configuración JSON"
    )

    args = parser.parse_args()

    config_path = PROJECT_DIR / args.config

    if not config_path.exists():
        print(f"ERROR: No existe el archivo {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    dataset_name = config["dataset_name"]

    print("\nFRAMEWORK GENERICO DE MLOPS")
    print(f"DATASET SELECCIONADO: {dataset_name}")
    print("INICIO DE EJECUCION AUTOMATIZADA")

    # 1. Preparación del dataset
    run_step(
        "PREPARACION DEL DATASET",
        [
            sys.executable,
            "-m",
            "src.prepare_data",
            "--dataset",
            dataset_name
        ]
    )

    # 2. Validación, entrenamiento y evaluación
    run_step(
        "PIPELINE DE MACHINE LEARNING",
        [
            sys.executable,
            "-m",
            "src.pipeline",
            "--config",
            args.config
        ]
    )

    # 3. Pruebas automáticas
    run_step(
        "PRUEBAS AUTOMATICAS DE CALIDAD",
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-v"
        ]
    )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETADO CORRECTAMENTE")
    print(f"DATASET PROCESADO: {dataset_name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
