def clean_and_validate(lines):
    total = 0
    invalid = 0
    valid_records = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("TransactionID"):
            continue

        total += 1
        parts = line.split("|")
        if len(parts) != 8:
            invalid += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        if not tid.startswith("T") or not cid or not region:
            invalid += 1
            continue

        try:
            qty = int(qty)
            price = float(price.replace(",", ""))
        except:
            invalid += 1
            continue

        if qty <= 0 or price <= 0:
            invalid += 1
            continue

        valid_records.append({
            "quantity": qty,
            "unit_price": price
        })

    return valid_records, {
        "Total records parsed": total,
        "Invalid records removed": invalid,
        "Valid records after cleaning": len(valid_records)
    }

def analyze_sales(records):
    total_revenue = sum(r["quantity"] * r["unit_price"] for r in records)
    return {
        "Total Revenue": round(total_revenue, 2),
        "Total Transactions": len(records)
    }
    
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    parsed_records = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean ProductName (remove commas)
        product_name = product_name.replace(",", "")

        # Clean numeric fields
        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            continue

        record = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        parsed_records.append(record)

    return parsed_records

