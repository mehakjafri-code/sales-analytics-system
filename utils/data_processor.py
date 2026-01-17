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
            "date": date,
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
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}

    # Step 1: Aggregate quantity and revenue per product
    for t in transactions:
        product = t["product"]
        qty = t["qty"]
        revenue = qty * t["price"]

        if product not in product_data:
            product_data[product] = {
                "total_qty": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_qty"] += qty
        product_data[product]["total_revenue"] += revenue

    # Step 2: Convert to list of tuples
    product_list = [
        (product, data["total_qty"], data["total_revenue"])
        for product, data in product_data.items()
    ]

    # Step 3: Sort by total quantity sold (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n
    return product_list[:n]
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    """
    customers = {}

    # Step 1: Aggregate data per customer
    for t in transactions:
        customer = t["customer"]
        product = t["product"]
        amount = t["qty"] * t["price"]

        if customer not in customers:
            customers[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[customer]["total_spent"] += amount
        customers[customer]["purchase_count"] += 1
        customers[customer]["products_bought"].add(product)

    # Step 2: Calculate average order value + clean product list
    for customer, data in customers.items():
        data["avg_order_value"] = round(
            data["total_spent"] / data["purchase_count"], 2
        )
        data["products_bought"] = list(data["products_bought"])

    # Step 3: Sort customers by total_spent (descending)
    sorted_customers = dict(
        sorted(
            customers.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns dictionary sorted by date
    """
    daily_data = {}

    for t in transactions:
        date = t["date"]
        revenue = t["qty"] * t["price"]
        customer = t["customer"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["unique_customers"].add(customer)

    # convert sets → counts
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(
            daily_data[date]["unique_customers"]
        )

    # sort by date
    return dict(sorted(daily_data.items()))
