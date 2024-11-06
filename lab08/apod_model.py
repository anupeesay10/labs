import requests
from datetime import datetime

NASA_API_KEY = 'DEMO_KEY'  # Replace with your API key if you registered


def get_apod(date=None):
    """Fetches the APOD data from NASA's API."""
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        'api_key': NASA_API_KEY,
        'date': date if date else datetime.today().strftime('%Y-%m-%d')
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}")