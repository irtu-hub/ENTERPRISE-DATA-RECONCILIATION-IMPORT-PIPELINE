#loader.py
from pathlib import Path
import csv


def convert_amount(value):
    cleaned_value = value.strip()

    if cleaned_value.replace(".", "", 1).isdigit():
        return float(cleaned_value)

    return value

def load_erp_transactions(file_path):
    data = []
    file_location = Path (file_path) / "erp_transactions.csv"
    if file_location.exists():
        with file_location.open("r", newline="", encoding="utf-8") as file:
            loader = csv.DictReader(file)
            for info in loader:
                record = {
                    "transaction_id": info["transaction_id"],
                    "invoice_id": info["invoice_id"],
                    "customer" : info["customer"],
                    "amount": convert_amount(info["amount"]),
                    "currency": info["currency"],
                    "transaction_date": info["transaction_date"],
                    "status" : info["status"]

                }
                data.append(record)
    return data


def load_bank_transactions(file_path):
    data = []
    file_location = Path (file_path) / "bank_transactions.csv"
    if file_location.exists():
        with file_location.open("r", newline="", encoding="utf-8") as file:
            loader = csv.DictReader(file)
            for info in loader:
                        record = {
                            "bank_reference" : info["bank_reference"],
                            "transaction_id": info["transaction_id"],
                            "amount": convert_amount(info["amount"]),
                            "currency": info["currency"],
                            "payment_date": info["payment_date"],

                        }
                        data.append(record)
    return data