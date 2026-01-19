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
    
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # Collect available regions and transaction amounts
    regions = set()
    amounts = []

    for tx in transactions:
        # Check required fields
        required_fields = [
            'TransactionID', 'Date', 'ProductID', 'ProductName',
            'Quantity', 'UnitPrice', 'CustomerID', 'Region'
        ]

        if not all(field in tx for field in required_fields):
            invalid_count += 1
            continue

        # Validation rules
        if (
            not tx['TransactionID'].startswith('T') or
            not tx['ProductID'].startswith('P') or
            not tx['CustomerID'].startswith('C') or
            tx['Quantity'] <= 0 or
            tx['UnitPrice'] <= 0
        ):
            invalid_count += 1
            continue

        amount = tx['Quantity'] * tx['UnitPrice']

        regions.add(tx['Region'])
        amounts.append(amount)

        valid_transactions.append(tx)

    # Display available regions and amount range
    if regions:
        print(f"Available regions: {sorted(regions)}")

    if amounts:
        print(f"Transaction amount range: {min(amounts)} - {max(amounts)}")

    # Apply region filter
    filtered_by_region = 0
    if region:
        before = len(valid_transactions)
        valid_transactions = [
            tx for tx in valid_transactions if tx['Region'] == region
        ]
        filtered_by_region = before - len(valid_transactions)
        print(f"Records after region filter: {len(valid_transactions)}")

    # Apply amount filters
    filtered_by_amount = 0
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)
        filtered = []

        for tx in valid_transactions:
            amount = tx['Quantity'] * tx['UnitPrice']
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            filtered.append(tx)

        filtered_by_amount = before - len(filtered)
        valid_transactions = filtered
        print(f"Records after amount filter: {len(valid_transactions)}")

    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
    
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Total Revenue = sum of (Quantity * UnitPrice) for each transaction
    """

    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx['Quantity'] * tx['UnitPrice']

    return round(total_revenue, 2)



