import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from FileReaders import CountryCurrencyDict, CurrencyRateDict

class Airport:
    """Airport class
    No class attributes

    Instance attribues:     code
                            name
                            city
                            country
                            latitude
                            longitude
                            altitude
                            time_zone
                            exchange_rate

    Methods:                exchangeRateFinder()
    """

    def __init__(self, code, list):
        self.code = code
        self.name = list[code][0]
        self.city = list[code][1]
        self.country = list[code][2]
        self.latitude = float(list[code][3])
        self.longitude = float(list[code][4])
        self.altitude = float(list[code][5])
        self.time_zone = list[code][6]
        # Add error handling for this
        currency = CountryCurrencyDict('Files/countrycurrency.csv')
        rates = CurrencyRateDict("Files/currencyrates.csv")
        self.exchage_rate_finder(currency.currency_dict, rates.rate_dict)

    def exchage_rate_finder(self, currencies, rates):
        """Finds the airport's exchange rate and sets its as
        the attribute exchange_rate.
        """
        self.exchange_rate = float(rates[currencies[self.country]])

    def __eq__(self, other):
        return self.name == other.name
