import datetime
import time
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from pprint import pprint

sheet_data = DataManager()
flight = FlightSearch()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

for flight_info in sheet_data.get_sheet()["prices"]:
    flight_info["iataCode"] = flight.get_destination_code(flight_info["city"])
    id_info = flight_info["id"]
    updated_data = {"price": flight_info}
    sheet_data.put_sheet(id_info, updated_data)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data.get_sheet()["prices"]:
    print(f"Getting flights for {destination['city']}...")
    flights = flight.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)