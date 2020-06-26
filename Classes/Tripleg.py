import copy
import math


class TripLeg():
    """Single leg of the entire journey. Distance calculated
    """

    def __init__(self, start, end):
        self.start_airport = copy.deepcopy(start)
        self.end_airport = copy.deepcopy(end)
        self.distance = 0
        self.leg_cost = 0
        # self.start_airport = copy.deepcopy(self.start_airport)
        # self.end_airport = copy.deepcopy(self.end_airport)

    def convert_to_radians(self, deg):
        rad = deg*((2*math.pi)/360)
        return rad

    def Distance(self):
        """Calculates the distance between two aiports using the great
        Circle formula
        """
        self.start_airport.latitude = 90 - self.start_airport.latitude
        self.end_airport.latitude = 90 - self.end_airport.latitude

        inputs = [self.start_airport.latitude,
                  self.start_airport.longitude,
                  self.end_airport.latitude,
                  self.end_airport.longitude]

        for i, deg in enumerate(inputs):
            inputs[i] = self.convert_to_radians(deg)

        (self.start_airport.latitude, self.start_airport.longitude,
         self.end_airport.latitude, self.end_airport.longitude
         ) = inputs

        # radius of earth assumed to be 6371 km
        r_earth = 6371
        calc_1 = (math.sin(self.start_airport.latitude)) *\
            (math.sin(self.end_airport.latitude)) *\
            (math.cos(self.start_airport.longitude-self.end_airport.longitude))

        calc_2 = (math.cos(self.start_airport.latitude)) *\
            (math.cos(self.end_airport.latitude))

        self.distance = (math.acos(calc_1+calc_2))*r_earth
        return self.distance
