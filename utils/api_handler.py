import requests

def get_usd_rate():
    try:
        url = "https://open.er-api.com/v6/latest/INR"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["rates"]["USD"]
    except Exception as e:
        print("API error:", e)
        return None
import requests

def fetch_products(limit=100):
    """
    Fetches products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = f"https://dummyjson.com/products?limit={limit}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except Exception as e:
        print("API Error:", e)
        return []
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        print("Successfully fetched products from DummyJSON API")
        return data.get("products", [])

    except Exception as e:
        print("Failed to fetch products:", e)
        return []
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched = []

    for t in transactions:
        enriched_txn = {
            "TransactionID": t.get("tid"),
            "Date": t.get("date"),
            "ProductID": None,
            "ProductName": t.get("product"),
            "Quantity": t.get("qty"),
            "UnitPrice": t.get("price"),
            "CustomerID": t.get("customer"),
            "Region": t.get("region"),
            "API_Category": None,
            "API_Brand": None,
            "API_Rating": None,
            "API_Match": False
        }

        # Extract numeric product ID from ProductID like P101 → 101
        product_id_raw = t.get("tid")

        try:
            if t.get("tid") and t.get("tid").startswith("T"):
                numeric_id = int(t.get("tid")[1:])

                if numeric_id in product_mapping:
                    api_product = product_mapping[numeric_id]
                    enriched_txn["API_Category"] = api_product.get("category")
                    enriched_txn["API_Brand"] = api_product.get("brand")
                    enriched_txn["API_Rating"] = api_product.get("rating")
                    enriched_txn["API_Match"] = True
        except Exception:
            pass  # Graceful failure

        enriched.append(enriched_txn)

    return enriched
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "")),
                str(t.get("API_Brand", "")),
                str(t.get("API_Rating", "")),
                str(t.get("API_Match", False))
            ]

            f.write("|".join(row) + "\n")
