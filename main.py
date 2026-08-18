#main.py
from pathlib import Path
from reconciliation.loader import load_erp_transactions,load_bank_transactions
from reconciliation.validation import validate_erp_record, validate_bank_record

file_location = Path("Data")

erp = load_erp_transactions(file_location)
bank = load_bank_transactions(file_location)


print(validate_erp_record(erp[0]))
print(validate_erp_record(erp[9]))
print(validate_bank_record(bank[10]))