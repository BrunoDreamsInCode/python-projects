import os
import requests
import calendar
from datetime import datetime
from dotenv import load_dotenv


load_dotenv("config.env")


class FlightData:

    def __init__(self, flight_search_service):
        self.sheety_token = os.getenv("DATA_SHEETY_TOKEN")
        self.base_url = "https://api.sheety.co/22c8adecdb2dabd241715da64c96c0de/flightDeals/prices"
        self.flight_search = flight_search_service

        self.headers = {
            "Authorization": f"Bearer {self.sheety_token}",
            "Content-Type": "application/json"
        }

    # ----------------------------
    # SHEETY DATA
    # ----------------------------

    def fetch_sheet_data(self):
        response = requests.get(self.base_url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["prices"]

    def update_missing_iata_codes(self):
        print("Fetching sheet data...")
        sheet_data = self.fetch_sheet_data()
        print("Success\n")

        for row in sheet_data:
            if not row.get("iataCode"):
                city_name = row["city"]
                row_id = row["id"]

                print(f"Missing IATA for {city_name}. Searching...")

                iata_code = self.flight_search.get_iata_code(city_name)

                if iata_code:
                    self.update_iata_code(row_id, iata_code)
                    print(f"IATA '{iata_code}' added to '{city_name}'\n")
                else:
                    self.update_iata_code(row_id, "")
                    print("IATA not found. Field left empty.\n")

        print("IATA update process finished.\n")

    # ----------------------------
    # DATE GENERATION
    # ----------------------------

    def generate_last_days_of_months(self, months_ahead):
        today = datetime.today()
        current_month = today.month
        current_year = today.year

        search_dates = []

        for i in range(months_ahead):
            month = current_month + i
            year = current_year + (month - 1) // 12
            month = ((month - 1) % 12) + 1

            last_day = calendar.monthrange(year, month)[1]
            target_date = datetime(year, month, last_day)

            search_dates.append(target_date.strftime("%Y-%m-%d"))

        return search_dates

    # ----------------------------
    # UPDATE METHODS
    # ----------------------------

    def update_iata_code(self, row_id, iata_code):
        url = f"{self.base_url}/{row_id}"

        body = {
            "price": {
                "iataCode": iata_code
            }
        }

        response = requests.put(url=url, json=body, headers=self.headers)
        response.raise_for_status()

        print(f"IATA updated | Status: {response.status_code}")

    def update_lowest_prices(self, origin_code, search_dates):
        print("\nFetching sheet data to update lowest prices...")
        sheet_data = self.fetch_sheet_data()
        print("Success\n")

        for row in sheet_data:
            if not row.get("lowestPrice"):
                city_name = row["city"]
                destination_code = row["iataCode"]
                row_id = row["id"]

                print(f"No price found for {city_name}. Searching...")

                lowest_price = self.flight_search.lowest_price(
                    origin_code,
                    destination_code,
                    search_dates
                )

                if lowest_price is None:
                    print("No flights found for this route.\n")
                    continue

                url = f"{self.base_url}/{row_id}"

                body = {
                    "price": {
                        "lowestPrice": lowest_price
                    }
                }

                response = requests.put(url=url, json=body, headers=self.headers)
                response.raise_for_status()

                print(f"Lowest price ({lowest_price}) updated successfully.\n")
