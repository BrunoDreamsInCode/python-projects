import os
import time
import requests
from dotenv import load_dotenv


load_dotenv("config.env")


class FlightSearch:

    FALLBACK_IATA_CODES = {
        "TOKYO": "TYO",
        "HONG KONG": "HKG",
        "KUALA LUMPUR": "KUL"
    }

    def __init__(self):
        self.base_url = "https://test.api.amadeus.com"

        self.token_endpoint = f"{self.base_url}/v1/security/oauth2/token"
        self.locations_endpoint = f"{self.base_url}/v1/reference-data/locations"
        self.flight_offers_endpoint = f"{self.base_url}/v2/shopping/flight-offers"

        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")

        self.access_token = None
        self.token_expiration = 0


    def get_token(self):

        if self.access_token and time.time() < self.token_expiration:
            return self.access_token

        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }

        response = requests.post(self.token_endpoint, data=data)
        response.raise_for_status()

        token_data = response.json()

        self.access_token = token_data["access_token"]

        # Grace time of 60 seconds before expiration
        self.token_expiration = time.time() + token_data["expires_in"] - 60

        return self.access_token


    def get_iata_code(self, city_name):

        token = self.get_token()

        params = {
            "keyword": city_name,
            "subType": "AIRPORT,CITY"
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(self.locations_endpoint, params=params, headers=headers)
        response.raise_for_status()

        results = response.json().get("data", [])

        # Prefer CITY first
        for item in results:
            if item.get("subType") == "CITY":
                return item["iataCode"]

        # Then fallback to AIRPORT
        for item in results:
            if item.get("subType") == "AIRPORT":
                return item["iataCode"]

        # Manual fallback dictionary
        return self.FALLBACK_IATA_CODES.get(city_name.strip().upper())


    def lowest_price(self, origin_code, destination_code, search_dates):

        token = self.get_token()

        lowest_price_overall = float("inf")

        for departure_date in search_dates:

            lowest_price_for_date = float("inf")

            params = {
                "originLocationCode": origin_code,
                "destinationLocationCode": destination_code,
                "departureDate": departure_date,
                "nonStop": "true",
                "adults": 1,
            }

            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.get(self.flight_offers_endpoint, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            flights = data.get("data", [])

            if not flights:
                print(f"{departure_date} | No flights found")
                continue

            for flight in flights:
                price = float(flight["price"]["grandTotal"])

                if price < lowest_price_for_date:
                    lowest_price_for_date = price

                if price < lowest_price_overall:
                    lowest_price_overall = price

            print(f"{departure_date} | Lowest price for date: {lowest_price_for_date}")

        if lowest_price_overall == float("inf"):
            print("\nNo flights found in the entire period.\n")
            return None

        print(f"\nBest price in full range: {lowest_price_overall}")
        return lowest_price_overall
