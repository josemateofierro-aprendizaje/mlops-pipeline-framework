
from pathlib import Path
import argparse

import pandas as pd
from sklearn.datasets import load_iris, load_wine


DATA_DIR = Path("data/raw")


def prepare_iris():
    """Descarga y prepara el conjunto de datos Iris."""

    dataset = load_iris(as_frame=True)
    df = dataset.frame.copy()

    df["target"] = df["target"].map(
        dict(enumerate(dataset.target_names))
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / "iris.csv"
    df.to_csv(output_path, index=False)

    print("Dataset Iris preparado correctamente.")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")


def prepare_wine():
    """Descarga y prepara el conjunto de datos Wine."""

    dataset = load_wine(as_frame=True)
    df = dataset.frame.copy()

    df["target"] = df["target"].map(
        dict(enumerate(dataset.target_names))
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / "wine.csv"
    df.to_csv(output_path, index=False)

    print("Dataset Wine preparado correctamente.")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Preparación de datasets del framework MLOps"
    )

    parser.add_argument(
        "--dataset",
        choices=["iris", "wine"],
        required=True
    )

    args = parser.parse_args()

    if args.dataset == "iris":
        prepare_iris()

    elif args.dataset == "wine":
        prepare_wine()
