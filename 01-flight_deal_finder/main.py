import os
from dotenv import load_dotenv
from flight_data import FlightData
from flight_search import FlightSearch


load_dotenv()

sheety_token = os.getenv("DATA_SHEETY_TOKEN")

flight_search_service = FlightSearch()
flight_data_service = FlightData(flight_search_service)

origin_code = "LON"  # Default origin

months_ahead = int(input("How many months ahead do you want to search? "))

search_dates = flight_data_service.generate_last_days_of_months(months_ahead)

print(f"Dates generated successfully\n------------------------\n{search_dates}")

flight_data_service.update_missing_iata_codes()

flight_data_service.update_lowest_prices(origin_code, search_dates)
