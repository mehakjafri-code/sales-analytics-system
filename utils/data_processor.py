def clean_and_validate(lines):
    valid = []
    invalid = 0
    total = 0

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        total += 1
        parts = line.split("|")

        if len(parts) != 8:
            invalid += 1
            continue

        tid, date, pid, name, qty, price, cid, region = parts

        name = name.replace(",", "")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        if not tid.startswith("T"):
            invalid += 1
            continue
        if not cid or not region:
            invalid += 1
            continue

        try:
            qty = int(qty)
            price = float(price)
        except:
            invalid += 1
            continue

        if qty <= 0 or price <= 0:
            invalid += 1
            continue

        valid.append({
            "tid": tid,
            "product": name,
            "qty": qty,
            "price": price,
            "customer": cid,
            "region": region
        })

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    return valid
def parse_transactions(raw_lines):
    """
    Parses raw lines into a clean list of dictionaries
    """
    transactions = []

    for line in raw_lines[1:]:  # skip header
        line = line.strip()
        if not line:
            continue

        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "")

        # Clean numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines[1:]:  # skip header
        line = line.strip()
        if not line:
            continue

        fields = line.split("|")

        # Skip rows with incorrect number of fields
        if len(fields) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields

        # Handle commas in product name
        product_name = product_name.replace(",", "")

        # Clean numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip rows where conversion fails
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    summary = {
        "total_input": len(transactions),
        "invalid": 0,
        "filtered_by_region": 0,
        "filtered_by_amount": 0,
        "final_count": 0
    }

    # Display available regions
    available_regions = sorted(set(t.get("Region") for t in transactions if t.get("Region")))
    print("Available regions:", available_regions)

    # Display transaction amount range
    amounts = [
        t["Quantity"] * t["UnitPrice"]
        for t in transactions
        if isinstance(t.get("Quantity"), int) and isinstance(t.get("UnitPrice"), (int, float))
    ]
    if amounts:
        print(f"Transaction amount range: {min(amounts)} - {max(amounts)}")

    for t in transactions:
        # Required fields check
        required_fields = [
            "TransactionID", "Date", "ProductID", "ProductName",
            "Quantity", "UnitPrice", "CustomerID", "Region"
        ]

        if not all(field in t for field in required_fields):
            invalid_count += 1
            continue

        # Business validation rules
        if (
            t["Quantity"] <= 0 or
            t["UnitPrice"] <= 0 or
            not t["TransactionID"].startswith("T") or
            not t["ProductID"].startswith("P") or
            not t["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        # Apply region filter
        if region and t["Region"] != region:
            summary["filtered_by_region"] += 1
            continue

        amount = t["Quantity"] * t["UnitPrice"]

        # Apply amount filters
        if min_amount is not None and amount < min_amount:
            summary["filtered_by_amount"] += 1
            continue

        if max_amount is not None and amount > max_amount:
            summary["filtered_by_amount"] += 1
            continue

        valid_transactions.append(t)

    summary["invalid"] = invalid_count
    summary["final_count"] = len(valid_transactions)

    return valid_transactions, invalid_count, summary
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float
    """
    total = 0.0
    for t in transactions:
        total += t["qty"] * t["price"]
    return total
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary sorted by total_sales (descending)
    """
    region_data = {}
    overall_total = 0.0

    # Step 1: Aggregate sales and count
    for t in transactions:
        region = t["region"]
        revenue = t["qty"] * t["price"]
        overall_total += revenue

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Step 2: Calculate percentage contribution
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / overall_total) * 100, 2
        )

    # Step 3: Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions
