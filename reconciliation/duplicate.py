def find_duplicates(records):
    seen_records = {}
    duplicates = []
    duplicate_ids = set()
    for data in records:
        if data["transaction_id"] not in seen_records:
            seen_records[data["transaction_id"]] = data
        else:
            if data["transaction_id"] not in duplicate_ids:
                duplicate_ids.add(data["transaction_id"])
                duplicates.append(seen_records[data["transaction_id"]])
            duplicates.append(data)

    return duplicates, duplicate_ids

def remove_duplicates(records, duplicate_ids):
    result = []

    for record in records:
        if record["transaction_id"] not in duplicate_ids:
            result.append(record)
    return result
