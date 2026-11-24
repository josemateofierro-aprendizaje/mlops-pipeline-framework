
import json
import csv

from src.validate_data import validate_data


def create_test_files(tmp_path, rows):

    contract = {
        "required_columns": ["edad", "categoria"],
        "columns": {
            "edad": {
                "type": "number",
                "nullable": False,
                "min": 0,
                "max": 100
            },
            "categoria": {
                "type": "string",
                "nullable": False,
                "allowed_values": ["A", "B"]
            }
        }
    }

    contract_path = tmp_path / "contract.json"
    csv_path = tmp_path / "data.csv"

    with open(contract_path, "w", encoding="utf-8") as file:
        json.dump(contract, file)

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["edad", "categoria"]
        )

        writer.writeheader()
        writer.writerows(rows)

    return csv_path, contract_path


def test_valid_data(tmp_path):

    rows = [
        {"edad": "25", "categoria": "A"},
        {"edad": "40", "categoria": "B"}
    ]

    csv_path, contract_path = create_test_files(
        tmp_path, rows
    )

    errors = validate_data(csv_path, contract_path)

    assert errors == []


def test_null_values(tmp_path):

    rows = [
        {"edad": "", "categoria": "A"}
    ]

    csv_path, contract_path = create_test_files(
        tmp_path, rows
    )

    errors = validate_data(csv_path, contract_path)

    assert any("valor nulo" in error for error in errors)


def test_invalid_range(tmp_path):

    rows = [
        {"edad": "150", "categoria": "A"}
    ]

    csv_path, contract_path = create_test_files(
        tmp_path, rows
    )

    errors = validate_data(csv_path, contract_path)

    assert any("supera el máximo" in error for error in errors)


def test_invalid_category(tmp_path):

    rows = [
        {"edad": "25", "categoria": "C"}
    ]

    csv_path, contract_path = create_test_files(
        tmp_path, rows
    )

    errors = validate_data(csv_path, contract_path)

    assert any("valor no permitido" in error for error in errors)
