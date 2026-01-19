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

def calculate_region_wise_sales(transactions):
    """
    Calculates total sales revenue for each region

    Parameters:
    - transactions: list of transaction dictionaries

    Returns:
    - dictionary with region as key and total revenue as value

    Example Output:
    {
        'North': 250000.0,
        'South': 180000.5,
        'East': 320000.0,
        'West': 210000.75
    }
    """

    region_sales = {}

    for tx in transactions:
        region = tx['Region']
        amount = tx['Quantity'] * tx['UnitPrice']

        if region in region_sales:
            region_sales[region] += amount
        else:
            region_sales[region] = amount

    # Optional: round values to 2 decimals
    for region in region_sales:
        region_sales[region] = round(region_sales[region], 2)

    return region_sales

def get_top_selling_products(transactions, top_n=5):
    """
    Identifies top selling products based on total revenue

    Parameters:
    - transactions: list of transaction dictionaries
    - top_n: number of top products to return (default 5)

    Returns:
    - list of tuples (ProductName, total_revenue) sorted in descending order

    Example Output:
    [
        ('Laptop', 350000.0),
        ('Monitor', 210000.5),
        ('Keyboard', 120000.0)
    ]
    """

    product_sales = {}

    for tx in transactions:
        product = tx['ProductName']

def analyze_customer_purchases(transactions):
    """
    Analyzes customer purchase behavior

    Parameters:
    - transactions: list of transaction dictionaries

    Returns:
    - dictionary with CustomerID as key and summary as value

    Example Output:
    {
        'C001': {
            'total_spent': 120000.0,
            'transaction_count': 3,
            'average_order_value': 40000.0
        },
        'C002': {
            'total_spent': 85000.0,
            'transaction_count': 2,
            'average_order_value': 42500.0
        }
    }
    """

    customer_summary = {}

    for tx in transactions:
        customer_id = tx['CustomerID']
        amount = tx['Quantity'] * tx['UnitPrice']

        if customer_id not in customer_summary:
            customer_summary[customer_id] = {
                'total_spent': 0.0,
                'transaction_count': 0
            }

        customer_summary[customer_id]['total_spent'] += amount
        customer_summary[customer_id]['transaction_count'] += 1

    # Calculate average order value
    for customer_id, data in customer_summary.items():
        data['total_spent'] = round(data['total_spent'], 2)
        data['average_order_value'] = round(
            data['total_spent'] / data['transaction_count'], 2
        )

    return customer_summary

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns:
    - dictionary sorted by date with daily metrics
    """

    daily_data = {}

    for tx in transactions:
        date = tx['Date']
        amount = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)

    # Prepare final output (sorted by date)
    daily_trend = {}

    for date in sorted(daily_data.keys()):
        daily_trend[date] = {
            'revenue': round(daily_data[date]['revenue'], 2),
            'transaction_count': daily_data[date]['transaction_count'],
            'unique_customers': len(daily_data[date]['customers'])
        }

    return daily_trend


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns:
    - tuple (date, revenue, transaction_count)

    Example:
    ('2024-12-15', 185000.0, 12)
    """

    daily_summary = {}

    for tx in transactions:
        date = tx['Date']
        amount = tx['Quantity'] * tx['UnitPrice']

        if date not in daily_summary:
            daily_summary[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_summary[date]['revenue'] += amount
        daily_summary[date]['transaction_count'] += 1

    # Find peak sales day
    peak_date = None
    peak_revenue = 0.0
    peak_transactions = 0

    for date, data in daily_summary.items():
        if data['revenue'] > peak_revenue:
            peak_revenue = data['revenue']
            peak_date = date
            peak_transactions = data['transaction_count']

    return peak_date, round(peak_revenue, 2), peak_transactions

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Parameters:
    - transactions: list of transaction dictionaries
    - threshold: minimum total quantity threshold

    Returns:
    - list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """

    product_summary = {}

    for tx in transactions:
        product = tx['ProductName']
        quantity = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if product not in product_summary:
            product_summary[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_summary[product]['total_quantity'] += quantity
        product_summary[product]['total_revenue'] += revenue

    # Identify low performing products
    low_products = []

    for product, data in product_summary.items():
        if data['total_quantity'] < threshold:
            low_products.append(
                (
                    product,
                    data['total_quantity'],
                    round(data['total_revenue'], 2)
                )
            )

    # Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products



