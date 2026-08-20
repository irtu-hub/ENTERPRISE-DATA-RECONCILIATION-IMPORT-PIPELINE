from pathlib import Path 
import csv,json

def generate_summary(
    raw_erp_records,
    raw_bank_records,
    reconciliation_results,
    duplicate_results,
    invalid_results
):

    matched_count = 0
    erp_only_count = 0
    bank_only_count = 0
    amount_mismatch_count = 0
    currency_mismatch_count = 0
    total_erp_amount = 0
    reconciled_amount = 0
    unmatched_erp_amount = 0

    for erp_record in raw_erp_records:
        if isinstance(erp_record["amount"], float):
            total_erp_amount += erp_record["amount"]

    for reconciliation_result in reconciliation_results:
        if reconciliation_result["status"] == "ERP_ONLY":
            erp_only_count += 1
            unmatched_erp_amount += reconciliation_result["erp_record"]["amount"]

        elif reconciliation_result["status"] == "AMOUNT_MISMATCH":
            amount_mismatch_count += 1
            unmatched_erp_amount += reconciliation_result["erp_record"]["amount"]

        elif reconciliation_result["status"] == "CURRENCY_MISMATCH":
            currency_mismatch_count += 1
            unmatched_erp_amount += reconciliation_result["erp_record"]["amount"]

        elif reconciliation_result["status"] == "MATCHED":
            matched_count += 1
            reconciled_amount += reconciliation_result["erp_record"]["amount"] 

        elif reconciliation_result["status"] == "BANK_ONLY":
            bank_only_count += 1

    

    return{
    "total_erp_transactions": len(raw_erp_records),
    "total_bank_transactions": len(raw_bank_records),

    "matched": matched_count,
    "erp_only": erp_only_count,
    "bank_only": bank_only_count,
    "amount_mismatches": amount_mismatch_count,
    "currency_mismatches": currency_mismatch_count,
    "duplicates": len(duplicate_results),
    "invalid_records": len(invalid_results),

    "total_erp_amount": total_erp_amount,
    "reconciled_amount": reconciled_amount,
    "unmatched_erp_amount": unmatched_erp_amount
}

def prepare_reconciliation_row(result):
    comb_status = ["AMOUNT_MISMATCH" ,"CURRENCY_MISMATCH", "MATCHED"]

    if result["status"] == "ERP_ONLY":
        return {
            "transaction_id" : result["transaction_id"],
            "status" : result["status"],
            "source" : None,
            "erp_amount" : result["erp_record"]["amount"],
            "bank_amount" : None,
            "erp_currency" : result["erp_record"]["currency"],
            "bank_currency" : None,
            "customer" : result["erp_record"]["customer"],
            "bank_reference" : None
        }
    elif result["status"] in comb_status:
        return {
            "transaction_id" : result["transaction_id"],
            "status" : result["status"],
            "source" : None,
            "erp_amount" : result["erp_record"]["amount"],
            "bank_amount" : result["bank_record"]["amount"],
            "erp_currency" : result["erp_record"]["currency"],
            "bank_currency" : result["bank_record"]["currency"],
            "customer" : result["erp_record"]["customer"],
            "bank_reference" : result["bank_record"]["bank_reference"]
        }
    elif result["status"] == "BANK_ONLY":
        return {
            "transaction_id" : result["transaction_id"],
            "status" : result["status"],
            "source" : None,
            "erp_amount" : None,
            "bank_amount" : result["bank_record"]["amount"],
            "erp_currency" : None,
            "bank_currency" : result["bank_record"]["currency"],
            "customer" : None,
            "bank_reference" : result["bank_record"]["bank_reference"]
        }  
    elif result["status"] == "DUPLICATE":
        return {
            "transaction_id" : result["transaction_id"],
            "status" : result["status"],
            "source" : result["source"],
            "erp_amount" : result["record"]["amount"] if result["source"]== "ERP" else None,
            "bank_amount" : result["record"]["amount"] if result["source"]== "BANK" else None,
            "erp_currency" : result["record"]["currency"] if result["source"]== "ERP" else None,
            "bank_currency" : result["record"]["currency"] if result["source"]== "BANK" else None,
            "customer" : result["record"]["customer"] if result["source"]== "ERP" else None,
            "bank_reference" : result["record"]["bank_reference"] if result["source"]== "BANK" else None
        }    


def write_reconciliation_results(results, file_path):
    
    file_loc = Path(file_path) / "reconciliation_results.csv"
    header = ["transaction_id","status","source","erp_amount","bank_amount","erp_currency","bank_currency","customer","bank_reference"]
    

    with file_loc.open("w", newline="", encoding= "utf-8") as file:

        writer = csv.DictWriter(file, fieldnames = header)

        writer.writeheader()
        prepared_rows = []

        for result in results:
            row = prepare_reconciliation_row(result)
            prepared_rows.append(row)
        writer.writerows(prepared_rows)
    

def prepare_invalid_row(result):

    return {
        "transaction_id" : result["transaction_id"],
        "source" : result["source"],
        "amount" : result["record"]["amount"],
        "currency" : result["record"]["currency"],
        "errors" : "; ".join(result["errors"])
    }


def write_invalid_records(records, file_path):
    file_loc = Path(file_path) / "invalid_records.csv"
    header = ["transaction_id","source","amount","currency","errors"]
   
    with file_loc.open("w", newline="", encoding= "utf-8") as file:

        writer = csv.DictWriter(file, fieldnames = header)

        writer.writeheader()
        prepared_rows = []

        for record in records:
            row = prepare_invalid_row(record)
            prepared_rows.append(row)
        writer.writerows(prepared_rows)


def write_summary(summary, file_path):
    file_loc = Path(file_path)/"reconciliation_summary.json"

    with file_loc.open("w", encoding= "utf-8") as file:
        json.dump(summary, file, indent= 4)

def build_duplicate_results(records, source):
    results = []
    for record in records:
        results.append({
            "transaction_id": record["transaction_id"],
             "status" : "DUPLICATE",
             "source" : source,
             "record" : record
        })
    return results


def build_invalid_results(records, source):
    results = []
    for record in records:
        inv_record = record["record"]
        results.append({
            "transaction_id": inv_record["transaction_id"],
             "status" : "INVALID",
             "source" : source,
             "record" : record["record"],
             "errors" : record["errors"]
        })
    return results   