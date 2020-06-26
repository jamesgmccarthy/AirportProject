import copy


def trip_fuelcapacity_checking(ordered_trips, aircraft):
    """Checks trips ordered by distance to find a trip suitable for the aircraft

    input: ordered list of tuples of trip objects and distances
    returns: list of accessible trip objects 
    """
    accesible_routes = []
    for i in ordered_trips:
        a = aircraft.check_flight(i[0])
        if a is True:
            accesible_routes.append(i)

        elif a is False:
            pass

    if len(accesible_routes) > 0:
        return accesible_routes
    else:
        pass


def create_sorted_fuel_cost_list(airports_list):
    """Returns a list of aiports ordered in increasing order of exchange rate,
    home airport is first and last always.
    """
    sorted_fuel_cost = sorted(airports_list,
                              key=lambda airport: airport.exchange_rate)

    return sorted_fuel_cost


def fuel_calc(aircraft, permutations, sorted_fuel_cost):
    """Calculates the cheapest route

    input:  aircraft object
            trip permutations object
            list of airports sorted by exchange rate

    """
    temp_aircraft = copy.deepcopy(aircraft)
    fuel_list = []
    trip_and_cost = {}
    for trip in permutations:
        temp_aircraft.fuel = 0
        fuel_list = copy.deepcopy(sorted_fuel_cost)
        fuel_list.append(fuel_list[0])
        purchased_fuel = 0
        if aircraft.check_flight(trip[0]):
            remaining_distance = trip[0].distance
            for leg in trip[0].leg_list:
                if temp_aircraft.fuel > leg.distance:
                    remaining_distance -= leg.distance
                    temp_aircraft.fuel -= leg.distance
                elif leg.start_airport.name == fuel_list[0].name:
                    minimum = min(temp_aircraft.max_fuel,
                                  (remaining_distance+temp_aircraft.min_fuel)-temp_aircraft.fuel)
                    purchased_fuel += temp_aircraft.add_fuel(minimum) * \
                        leg.start_airport.exchange_rate
                    remaining_distance -= leg.distance
                    temp_aircraft.fuel -= leg.distance
                    fuel_list.pop(0)

                else:
                    purchased_fuel += temp_aircraft.add_fuel(temp_aircraft.min_fuel + leg.distance - temp_aircraft.fuel) *\
                        leg.start_airport.exchange_rate
                    temp_aircraft.fuel -= leg.distance
                    remaining_distance -= leg.distance
                    fuel_list.pop(0)
            trip_and_cost[trip] = purchased_fuel
        else:
            pass
    if aircraft.capacity_clearance is True:
        lowest_trip_cost = min(trip_and_cost.values())
        for key, value in trip_and_cost.items():
            if value == lowest_trip_cost:
                cheapest_trip_object = key
    trip_and_cost = []
    trip_and_cost.append(cheapest_trip_object)
    trip_and_cost.append(lowest_trip_cost)
    return trip_and_cost
