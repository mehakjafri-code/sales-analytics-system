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
