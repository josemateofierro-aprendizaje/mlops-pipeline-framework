import csv
import json
import sys

from pathlib import Path


def load_contract(contract_path):

    with open(contract_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_data(csv_path, contract_path):

    contract = load_contract(contract_path)

    errors = []

    # Leer archivo CSV
    with open(csv_path, "r", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        headers = reader.fieldnames or []

        # Validar columnas obligatorias
        required_columns = contract["required_columns"]

        for column in required_columns:

            if column not in headers:
                errors.append(
                    f"Falta la columna obligatoria: {column}"
                )

        if errors:
            return errors

        # Validar registros
        for row_number, row in enumerate(reader, start=2):

            for column, rules in contract["columns"].items():

                value = row[column].strip()

                # Validar valores nulos
                if value == "":

                    if not rules.get("nullable", True):
                        errors.append(
                            f"Fila {row_number}: valor nulo en {column}"
                        )

                    continue

                expected_type = rules["type"]

                # Validar números
                if expected_type == "number":

                    try:
                        numeric_value = float(value)

                    except ValueError:

                        errors.append(
                            f"Fila {row_number}: {column} debe ser numérico"
                        )

                        continue

                    # Validar rango mínimo
                    if "min" in rules:

                        if numeric_value < rules["min"]:
                            errors.append(
                                f"Fila {row_number}: {column} "
                                f"está por debajo del mínimo"
                            )

                    # Validar rango máximo
                    if "max" in rules:

                        if numeric_value > rules["max"]:
                            errors.append(
                                f"Fila {row_number}: {column} "
                                f"supera el máximo"
                            )

                # Validar enteros
                elif expected_type == "integer":

                    try:
                        numeric_value = float(value)

                        if not numeric_value.is_integer():
                            raise ValueError

                    except ValueError:

                        errors.append(
                            f"Fila {row_number}: {column} debe ser entero"
                        )

                        continue

                # Validar texto
                elif expected_type == "string":

                    if not isinstance(value, str):
                        errors.append(
                            f"Fila {row_number}: {column} debe ser texto"
                        )

                # Validar categorías permitidas
                if "allowed_values" in rules:

                    if value not in rules["allowed_values"]:
                        errors.append(
                            f"Fila {row_number}: valor no permitido "
                            f"en {column}: {value}"
                        )

    return errors


if __name__ == "__main__":

    csv_path = Path("data/raw/iris.csv")
    contract_path = Path("contracts/iris_contract.json")

    validation_errors = validate_data(
        csv_path,
        contract_path
    )

    if validation_errors:

        print("VALIDACIÓN FALLIDA")

        for error in validation_errors:
            print("-", error)

        sys.exit(1)

    else:

        print("VALIDACIÓN EXITOSA")
        print("Los datos cumplen el contrato establecido.")