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
