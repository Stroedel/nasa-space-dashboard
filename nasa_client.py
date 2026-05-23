import os
import requests
from dotenv import load_dotenv


class NasaClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov"

    def get(self, endpoint, params=None):
        if params is None:
            params = {}

        params["api_key"] = self.api_key

        try:
            response = requests.get(
                self.base_url + endpoint,
                params=params,
                timeout=10
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as error:
            print(f"API fout: {error}")
            return None

    def get_apod(self):
        return self.get("/planetary/apod")