#main.py
from pathlib import Path
from reconciliation.loader import load_erp_transactions,load_bank_transactions
from reconciliation.validation import validate_erp_records, validate_bank_records
from reconciliation.duplicate import find_duplicates, remove_duplicates
from reconciliation.matcher import build_transaction_lookup, reconcile_erp_records, find_bank_only_records, build_duplicate_results,build_invalid_results
from reconciliation.reporting import generate_summary

file_location = Path("Data")

erp = load_erp_transactions(file_location)
bank = load_bank_transactions(file_location)


valid_erp, invalid_erp = validate_erp_records(erp)
valid_bank, invalid_bank = validate_bank_records(bank)


erp_duplicates, erp_duplicate_ids = find_duplicates(valid_erp)
bank_duplicates, bank_duplicate_ids = find_duplicates(valid_bank)

clean_erp = remove_duplicates(valid_erp, erp_duplicate_ids)
clean_bank = remove_duplicates(valid_bank, bank_duplicate_ids)

erp_lookup = build_transaction_lookup(clean_erp)
bank_lookup = build_transaction_lookup(clean_bank)

erp_results = reconcile_erp_records(clean_erp, bank_lookup, bank_duplicate_ids)

bank_only_results = find_bank_only_records(clean_bank, erp_lookup, erp_duplicate_ids)

erp_duplicate_results = build_duplicate_results(erp_duplicates, "ERP")
bank_duplicate_results = build_duplicate_results(bank_duplicates, "BANK")

erp_invalid_results = build_invalid_results(invalid_erp, "ERP")
bank_invalid_results = build_invalid_results(invalid_bank, "BANK")

reconciliation_results = erp_results + bank_only_results
duplicate_results = erp_duplicate_results + bank_duplicate_results
invalid_results = erp_invalid_results + bank_invalid_results

summary = generate_summary(erp, bank, reconciliation_results, duplicate_results, invalid_results)

print(summary)