import copy


class Aircraft:
    """Aircraft class
    class attribute:

    instance attributes:    aircraft_code
                            model
                            fuel
                            min_fuel
                            max_fuel
                            clearance
                            flight_list
                            purchased_fuel
                            flight_info
    """

    def __init__(self, AircraftDict, aircraft_code):
        self.aircraft_code = aircraft_code
        self.model = (
            AircraftDict.aircraft_dict[aircraft_code][0], aircraft_code)

        # initial fuel assumed to be 0
        self.fuel = 0

        # max_fuel is assumed to be equal to range of aircraft
        self.units = (AircraftDict.aircraft_dict[aircraft_code][2])
        if self.units == "metric":
            self.max_fuel = float(
                AircraftDict.aircraft_dict[aircraft_code][1])
        elif self.units == "imperial":
            self.max_fuel = float(
                AircraftDict.aircraft_dict[aircraft_code][1])*1.852
        # min_fuel assumed to be 5% of max_fuel
        self.min_fuel = self.max_fuel*0.05

        # intial state of clearance set to 0 because it has no fuel
        self.capacity_clearance = False

        self.purchased_fuel = 0

        self.flight_info = {}  # details of each leg

        self.failed_leg = ("", 99999999)  # leg and its distance

    def fuel_capacity_check(self, trip_leg):
        """
        Checks to see if the aircraft has enough fuel to complete each leg
        of the journey
        """
        if self.max_fuel >= (trip_leg.distance + self.min_fuel):
            return True
        else:
            return False

    def check_flight(self, trip):
        """Checks to see if the aircraft can fly the whole trip
        """
        self.best_trip = trip
        for i in range(len(self.best_trip.airports_list)-1):
            trip_leg = tl.TripLeg(self.best_trip.airports_list[i],
                                  self.best_trip.airports_list[i+1])
            trip_leg.Distance()
            a = self.fuel_capacity_check(trip_leg)
            if a is True:
                self.capacity_clearance = True

            elif a is False:
                temp = self.failed_leg[1]
                if temp > trip_leg.distance:
                    self.failed_leg = (trip_leg, trip_leg.distance)

                else:
                    temp = trip_leg.distance
                self.capacity_clearance = False
                return False

        if self.capacity_clearance is True:
            return True

    def add_fuel(self, quantity):
        if self.fuel + quantity > self.max_fuel:
            self.fuel = self.max_fuel
        else:
            self.fuel += quantity
        return self.fuel

    def fly_route(self, trip, sorted_fuel_trip):
        """Given the cheapest route, this breaks it down and gives info of each stop
        """
        self.trip = trip[0][0]
        temp_sorted_fuel_trip = []
        self.check_flight(self.trip)
        self.flight_info["Trip"] = self.trip.airports_list_names
        if self.capacity_clearance is True:
            temp_sorted_fuel_trip = copy.deepcopy(sorted_fuel_trip)
            temp_sorted_fuel_trip.append(temp_sorted_fuel_trip[0])
            remaining_distance = self.trip.distance
            for i, leg in enumerate(self.trip.leg_list, 1):
                self.flight_info[i] = []
                self.flight_info[i].append(
                    leg.start_airport.name)  # starting airport
                self.flight_info[i].append(
                    leg.end_airport.name)  # ending airport
                self.flight_info[i].append(leg.distance)  # leg distance
                self.flight_info[i].append(
                    leg.distance+self.min_fuel)  # Fuel required

                # No refueling required
                if self.fuel > leg.distance:
                    self.flight_info[i].append(0)  # purchased fuel
                    self.flight_info[i].append(0)  # cost

                    remaining_distance -= leg.distance
                    self.fuel -= leg.distance

                # airport is cheapest, buy min of full tank or remaining
                # distance
                elif leg.start_airport.name == temp_sorted_fuel_trip[0].name:
                    self.flight_info[i].append(
                        min(self.max_fuel, (remaining_distance + self.min_fuel)) - self.fuel)  # purchased fuel
                    leg_cost = self.add_fuel(
                        min(self.max_fuel, (remaining_distance +
                                            self.min_fuel)) -
                        self.fuel) * leg.start_airport.exchange_rate

                    self.flight_info[i].append(leg_cost)
                    self.purchased_fuel += leg_cost
                    remaining_distance -= leg.distance
                    self.fuel -= leg.distance
                    temp_sorted_fuel_trip.pop(0)

                # airport not cheapest in list, buy min fuel
                else:
                    self.flight_info[i].append(
                        self.min_fuel + leg.distance - self.fuel)  # purchased fuel
                    leg_cost = self.add_fuel(self.min_fuel +
                                             leg.distance - self.fuel) *\
                        leg.start_airport.exchange_rate

                    self.flight_info[i].append(leg_cost)  # leg cost
                    self.purchased_fuel += leg_cost
                    self.fuel -= leg.distance
                    remaining_distance -= leg.distance

        self.flight_info["Cost"] = self.purchased_fuel
        self.flight_info["Distance"] = self.trip.distance
