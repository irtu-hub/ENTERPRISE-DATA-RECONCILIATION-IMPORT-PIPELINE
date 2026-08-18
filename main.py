#main.py
from pathlib import Path
from reconciliation.loader import load_erp_transactions,load_bank_transactions
from reconciliation.validation import validate_erp_records, validate_bank_records

file_location = Path("Data")

erp = load_erp_transactions(file_location)
bank = load_bank_transactions(file_location)


valid_erp, invalid_erp = validate_erp_records(erp)
valid_bank, invalid_bank = validate_bank_records(bank)
print("Valid ERP:", len(valid_erp))
print("Invalid ERP:", len(invalid_erp))

print("Valid Bank:", len(valid_bank))
print("Invalid Bank:", len(invalid_bank))

print(invalid_erp)
print(invalid_bank)