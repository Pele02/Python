import requests
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()


class DataManager:
    def __init__(self):
        self.data = None
        self.response = None
        self.GOOGLE_SHEET_API = "https://api.sheety.co/a6cbc8595acd1aaeb401d903a6669635/flightDeals/prices"
        self._user = os.environ["SHEETY_USRERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)


    def get_sheet(self):
        try:
            self.response = requests.get(url=self.GOOGLE_SHEET_API,auth=self._authorization)
            self.response.raise_for_status()
            self.data = self.response.json()
            return self.data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle specific HTTP errors
        except Exception as err:
            print(f"Other error occurred: {err}")  # Handle other possible errors
        return None

    def put_sheet(self, id_number: int, new_data):
        """Update a row in the Google Sheet.
        Args:
            id_number (int): The ID of the row to update.
            new_data (dict): A dictionary containing the new data for the row.
        Returns:
            dict: The updated data retrieved from the Google Sheets API, or None if the request failed.
        """
        try:
            url = f"{self.GOOGLE_SHEET_API}/{id_number}"
            self.response = requests.put(url=url, json=new_data,auth=self._authorization)
            self.response.raise_for_status()
            self.data = self.response.json()
            return self.data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle specific HTTP errors
        except Exception as err:
            print(f"Other error occurred: {err}")  # Handle other possible errors
        return None
