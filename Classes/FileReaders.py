import os
import csv


class AircraftDict():
    """
    Generates a dictionary of aircrafts and its corresponding information
    """
    aircraft_dict = {}

    def __init__(self, filename):
        with open(os.path.join(os.getcwd(), filename)) as fin:
            reader = csv.reader(fin)
            next(reader, None)
            for line in reader:
                # assigning aircraft code (key) the values manufacturer,
                # range and units
                self.aircraft_dict[line[0]] = (line[3:4]+line[4:5]+line[2:3])


class AirportAtlas:
    """
    Generates a dictionary of airport codes (key) and its corresponding 
    information (values)
    """
    airport_dict = {}
    # error handling for invalid filenames

    def __init__(self, filename):
        try:
            with open(os.path.join(os.getcwd(), filename),
                      encoding='utf-8') as fin:
                reader = csv.reader(fin)
                next(reader, None)
                for line in reader:
                    self.airport_dict[line[4]] = line[1:4] + line[6:10]
        except FileNotFoundError:
            # allows user to re-enter file name
            print("The filename was wrong," +
                  "please re-enter the correct filename")


class CountryCurrencyDict:
    """
    Generates a dictionary of currencies used by different cou
    """
    currency_dict = {}

    def __init__(self, filename):
        with open(os.path.join(os.getcwd(), filename),
                  encoding='utf-8') as fin:
            reader = csv.reader(fin)
            next(reader, None)
            for line in reader:
                self.currency_dict[line[0]] = line[14]


class CurrencyRateDict:
    """
    Generates a dictionary of currency rates
    """
    rate_dict = {}

    def __init__(self, filename):
        with open(os.path.join(os.getcwd(), filename),
                  encoding='utf-8') as fin:
            reader = csv.reader(fin)
            next(reader, None)
            for line in reader:
                self.rate_dict[line[1]] = line[2]
