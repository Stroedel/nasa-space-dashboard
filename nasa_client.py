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

        except requests.RequestException:
            print("API fout: er ging iets mis bij het ophalen van data.")
            return None

    def get_apod(self):
        return self.get("/planetary/apod")

    def get_mars_photos(self, rover, date):
        return self.get(
            f"/mars-photos/api/v1/rovers/{rover}/photos",
            {"earth_date": date}
        )

    def get_asteroids(self, date):
        return self.get(
            "/neo/rest/v1/feed",
            {
                "start_date": date,
                "end_date": date
            }
        )
    