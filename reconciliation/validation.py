currency_supp = ["OMR", "USD"]
status_supp = ["PAID", "PENDING"]



def validate_erp_record(record):
    errors = []
    if not record["transaction_id"]:
        errors.append("transaction_id is required")
    if not record["customer"]:
        errors.append("customer is required")
    if not isinstance(record["amount"], float):
        errors.append("amount must be numeric")
    elif not record["amount"] > 0 :
        errors.append("Amount should be greater than zero")
    if record["currency"] not in currency_supp:
        errors.append("Unsupported Currency")
    if record["status"] not in status_supp:
        errors.append("Unknown Status")

    
    return errors





def validate_bank_record(record):
    errors = []
    if not record["bank_reference"]:
        errors.append("bank_reference is required")
    if not record["transaction_id"]:
        errors.append("transaction_id is required")
    if not isinstance(record["amount"], float):
        errors.append("amount must be numeric")
    elif not record["amount"] > 0:
        errors.append("Amount should be greater than zero")
    if record["currency"] not in currency_supp:
        errors.append("Unsupported Currency")

    return errors


