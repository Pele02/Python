from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

sheet_data = DataManager()
flight = FlightSearch()

for flight_info in sheet_data.get_sheet()["prices"]:
    #Verify if the flight has an iata code
    if len(flight_info["iataCode"]) == 0:
        flight.get_IATA(flight_info)
        id_info = flight_info["id"]
        updated_data = {"price": flight_info}
        sheet_data.put_sheet(id_info, updated_data)

#pprint(sheet_data.get_sheet())
