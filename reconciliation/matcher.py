def build_transaction_lookup(records):
    look_up = {}
    for data in records:
      look_up[data["transaction_id"]] = data
    return look_up


def reconcile_erp_records(erp_records, bank_lookup, bank_duplicate_ids):
    results = []
    for record in erp_records:
       if record["transaction_id"] not in bank_lookup:
            if record["transaction_id"] not in bank_duplicate_ids:
                results.append({
                    "transaction_id": record["transaction_id"],
                    "status": "ERP_ONLY",
                    "erp_record": record,
                    "bank_record": None
                })
            
       else:
            bank_record = bank_lookup[record["transaction_id"]]
            if record["amount"] != bank_record["amount"]:
                status = "AMOUNT_MISMATCH"
            elif record["currency"] != bank_record["currency"]:
                status = "CURRENCY_MISMATCH"
            else:
                status = "MATCHED"

            results.append({
                        "transaction_id": record["transaction_id"],
                        "status": status,
                        "erp_record": record,
                        "bank_record": bank_record
                      })
    return results

def find_bank_only_records(bank_records, erp_lookup, erp_duplicate_ids):
    results = []
    for record in bank_records:
       if record["transaction_id"] not in erp_lookup and record["transaction_id"] not in erp_duplicate_ids:
            results.append({
            "transaction_id": record["transaction_id"],
            "status": "BANK_ONLY",
            "erp_record": None,
            "bank_record": record
            })
    return results

 