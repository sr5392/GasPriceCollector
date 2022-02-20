from configparser import ConfigParser
from db_context_manager import Database
from gas_price_api import GasPriceAPI
from datetime import datetime
import time

def main() -> None:
    """Main function"""
    config = ConfigParser()
    config.read("./config.ini")

    api_token = config["API"]["TOKEN"]
    api_url = config["API"]["URL"]
    db_path = config["DATABASE"]["PATH"]

    api = GasPriceAPI(api_token, api_url)

    with Database(db_path) as db:
        while True:
            print("-Start import-")

            try:
                insert_date = datetime.now().date()
                insert_time = datetime.now().time().strftime("%H:%M:%S")

                station_ids = get_station_ids()
                for station_id in station_ids:
                    if not db.gas_station_exists(station_id):
                        station_details = api.get_station_details(station_id)
                        if station_details:
                            db.insert_gas_station(station_id, station_details)

                gas_prices = api.get_gas_prices(station_ids)
                if gas_prices:
                    db.insert_gas_prices(gas_prices, insert_date, insert_time)

            except Exception as e:
                print(repr(e))
                
            print("-End import-")
            time.sleep(60*15)

def get_station_ids() -> list:
    """Get all stations ids from the configuration file"""
    station_ids = []
    with open("./gas_station_list.txt", "r") as file:
        for line in file:
            line = line.lstrip()
            line = line.rstrip()
                
            if line:
                station_ids.append(line)

    return station_ids

if __name__ == "__main__":
    main()