import requests

class GasPriceAPI():
    """Represents a class to access the gas price API"""

    def __init__(self, token, url):
        self._api_key = token
        self._url = url
    
    def get_station_details(self, station_id: str) -> dict:
        """Return the details of the gas station as a dictionary"""
        url = self._url + "/json/detail.php"
        payload = {"id": station_id, "apikey": self._api_key}
        response = requests.get(url, params=payload)

        gas_station_details = {}

        if response.status_code == 200:
            response = response.json()
    
            if response["ok"]:
                gas_station_details = response["station"]
            else:
                print(response["message"])

        return gas_station_details

    def get_gas_prices(self, station_ids: list) -> dict:
        """Return the gas prices of the gas stations as a dictionary"""
        url = self._url + "/json/prices.php"
        station_ids = ",".join(station_ids)
        payload = {"ids": station_ids, "apikey": self._api_key}
        response = requests.get(url, params=payload)

        prices = {}

        if response.status_code == 200:
            response = response.json()
            
            if response["ok"]:
                prices = response["prices"]
            else:
                print(response["message"])
        return prices
        
if __name__ == "__main__":
    api = GasPriceAPI()

    print(api.get_gas_prices(["24a381e3-0d72-416d-bfd8-b2f65f6e5802"]))
    print(api.get_station_details("24a381e3-0d72-416d-bfd8-b2f65f6e5804"))
    
        