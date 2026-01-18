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
