from configparser import ConfigParser
from gas_price_api import GasPriceAPI
import unittest

config = ConfigParser()
config.read("./config.ini")

api_token = config["API"]["TOKEN"]
api_url = config["API"]["URL"]

api = GasPriceAPI(api_token, api_url)

class TestGasPriceAPI(unittest.TestCase):
    """Tests for gas_price_api.py"""

    def test_get_station_details(self):
        """Test for getting the gas station details"""
      
        #The station ID is OK and exists
        details = api.get_station_details("24a381e3-0d72-416d-bfd8-b2f65f6e5802")
        self.assertEqual("brand" in details, True)

        #The station ID is OK but does not exist
        details = api.get_station_details("24a381e3-0d72-416d-bfd8-b2f65f6e5804")
        self.assertEqual(details, {})

        #The station ID has a wrong format
        details = api.get_station_details("24a381e3-0d72-416d-bfd8")
        self.assertEqual(details, {}) 
   
    def test_get_gas_prices(self):
        """Test for getting the gas prices of the gas stations"""
    
        #Station ID is OK and exists
        gas_prices = api.get_gas_prices(["24a381e3-0d72-416d-bfd8-b2f65f6e5802"])
        for station_id in gas_prices:
                if gas_prices[station_id]["status"] == "open":
                    self.assertEqual("e5" in gas_prices[station_id], True)
                    self.assertEqual("e10" in gas_prices[station_id], True)
                    self.assertEqual("diesel" in gas_prices[station_id], True)

        #Station ID is OK but does not exist
        gas_prices = api.get_gas_prices(["24a381e3-0d72-416d-bfd8-b2f65f6e5804"])
        self.assertEqual(gas_prices["xxx"]["status"], "no stations")

        #Station ID has a wrong format
        gas_prices = api.get_gas_prices(["24a381e3-0d72-416d-bfd8"])
        self.assertEqual(gas_prices, {})

if __name__ == "__main__":
    unittest.main()