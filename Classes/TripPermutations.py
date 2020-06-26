from itertools import permutations
import operator
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))


class TripPermutations:

    def __init__(self, original_trip):
        self.best_trip_distance = 0
        self.trip_permutations = []
        self.trip_listings_dict = {}
        self.original_trip = original_trip
        self.ordered_trips = []

        self.accessible_routes_dict = {}

    def Trip_Permutations(self):
        """Generates the permutations of a 5 airport route and an 
        optional 6th airport route
        """
        # temp trip is assinged to all airports but home airport
        temp_trip = self.original_trip[1:]
        temp_permutations = permutations(temp_trip)
        for i in temp_permutations:
            i = list(i)
            i.insert(0, self.original_trip[0])
            i.append(self.original_trip[0])
            self.trip_permutations.append(i)

        # adding extra stop for refuelling
        # airport changes each iteration
        new_temp_permutations = []
        for airport in temp_trip:
            new_temp_trip = temp_trip[:]
            new_temp_trip.append(airport)
            for iteration in permutations(new_temp_trip):
                iteration = list(iteration)
                new_temp_permutations.append(iteration)

        copy_temp_permutations = new_temp_permutations[:]
        for l in new_temp_permutations:
            for i in range(len(l)-1):
                if i == 0:
                    if l[i] == l[i+1]:
                        copy_temp_permutations.remove(l)
                        break
                else:
                    if l[i] == l[i+1] or l[i] == l[i-1]:
                        copy_temp_permutations.remove(l)
                        break
        new_temp_permutations = None
        for i in copy_temp_permutations:
            i.insert(0, self.original_trip[0])
            i.append(self.original_trip[0])
            self.trip_permutations.append(i)

    def Route_Distances(self):
        """Calculate distance for each trips in permutations and add it to a dictionary
        dict[Trip_object] = distance
        """
        for i, y in enumerate(self.trip_permutations):
            i = trip.Trip(y)
            i.Total_Distance()
            self.trip_listings_dict[i] = i.distance

    def sort_trip_permuatations(self):
        """ returns ordered list of tuples where 0th element of tuple is trip object
        and 1th element of tuple is that trip objects distance
        """
        self.ordered_trips = sorted(
            self.trip_listings_dict.items(), key=operator.itemgetter(1))
        return self.ordered_trips

    def Best_Distance(self, aircraft):
        """Generates a list of accessible routes and finds the
         shortest trip from these routes
        """

        self.accessible_routes = fc.trip_fuelcapacity_checking(
            self.ordered_trips, aircraft)
        if self.accessible_routes is not None:
            for trip in self.accessible_routes:
                self.accessible_routes_dict[trip[0]] = trip[0].distance

            self.best_trip_distance = min(self.accessible_routes_dict.values())

            for key, value in self.trip_listings_dict.items():
                if value == self.best_trip_distance:
                    self.best_trip = key.airports_list
            self.best_trip_airport_names = []
            self.shortest_trip = Trip(self.best_trip)
            # create list with airport names in best trip
            for i in self.best_trip:
                self.best_trip_airport_names.append(i.name)

        elif self.accessible_routes is None:
            pass
