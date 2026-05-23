import os
import requests
from dotenv import load_dotenv


class NasaClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov"
