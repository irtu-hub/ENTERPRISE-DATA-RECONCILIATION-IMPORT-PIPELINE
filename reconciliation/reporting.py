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