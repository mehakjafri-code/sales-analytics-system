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
