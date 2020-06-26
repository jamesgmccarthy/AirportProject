class Trip:
    """Entire trip, consists of 5 main TripLeg objects, 1 possible TripLeg
    object
    Calculates combined Distance of all legs
    """

    def __init__(self, trip_list):
        self.distance = 0
        self.trip_list = trip_list
        self.leg_list = []
        self.airports_list = []
        for i in trip_list:
            self.airports_list.append(i)

        # create list of names of the airports in airport_list
        self.airports_list_names = []
        for i in self.airports_list:
            self.airports_list_names.append(i.name)

    def Total_Distance(self, func):
        """Calculates the distance of a given airport list
        """
        for i in range(len(self.airports_list)-1):
            trip_leg = func(
                self.airports_list[i], self.airports_list[i+1])
            self.leg_list.append(trip_leg)
            self.trip_distance = trip_leg.Distance()
            self.distance += self.trip_distance
        return self.distance
