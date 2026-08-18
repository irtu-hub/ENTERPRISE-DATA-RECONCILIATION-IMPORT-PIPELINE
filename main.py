#main.py
from pathlib import Path
from reconciliation.loader import load_erp_transactions,load_bank_transactions

file_location = Path("Data")

erp = load_erp_transactions(file_location)
bank = load_bank_transactions(file_location)
print(erp)
print(bank)

