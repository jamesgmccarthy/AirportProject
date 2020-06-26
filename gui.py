import sys
import os
import tkinter
import Classes.FuelCalcs as fc
import Classes.TripPermutations as tp
import Classes.Airport as ap
import Classes.Aircraft as ac
import Classes.Trip as trip
import Classes.FileReaders as fr


class Gui:
    def __init__(self, master):
        self.master = master
        self.aircraft_info = {}
        self.failed_flight_info = None
        self.scrollbar = tkinter.Scrollbar(master)
        master.title("airports_list Route Cost-calculator")
        master.geometry("800x8000")

        # Load Aircraft and airport lists
        self.aircraft_list = fr.AircraftDict("./Files/aircraft.csv")
        self.airlist = fr.AirportAtlas("./Files/airport.csv")

        # Error notifications

        self.error = "No Errors"
        self.error_label_text = tkinter.StringVar()
        self.error_label_text.set(self.error)
        self.error_label = tkinter.Label(
            master, textvariable=self.error_label_text)
        self.label_error = tkinter.Label(master, text="Error: ")

        # AIRPORT INPUT
        self.airports_list = []
        self.entered_airport = ""

        self.Airport_label_text = tkinter.StringVar()
        self.Airport_label_text.set(self.airports_list)
        self.Airport_label = tkinter.Label(
            master, textvariable=self.Airport_label_text, )

        self.label_airports = tkinter.Label(
            master, text="Airport List: ")
        vcmd_airport = master.register(self.validate_airports)
        self.entry_airports = tkinter.Entry(
            master, validate="key", validatecommand=(vcmd_airport, "%P"))
        self.entry_airports.bind(
            "<Return>", lambda event: self.update_airports("add"))

        self.add_button_airport = tkinter.Button(
            master, text="Add Airport",
            command=lambda: self.update_airports("add"))
        self.subtract_button_airport = tkinter.Button(
            master, text="Remove Last Airport",
            command=lambda: self.update_airports("subtract"))
        self.reset_button_airport = tkinter.Button(
            master, text="Reset", command=lambda: self.update_airports("reset"))

        # aircraft INPUT
        self.aircraft_code = ""
        self.entered_aircraft = ""

        self.aircraft_label_text = tkinter.StringVar()
        self.aircraft_label_text.set(self.aircraft_code)
        self.aircraft_label = tkinter.Label(
            master, textvariable=self.aircraft_label_text)
        vcmd_aircraft = master.register(self.validate_aircraft)
        self.label_aircraft = tkinter.Label(master, text="Aircraft: ")
        self.entry_aircraft = tkinter.Entry(
            master, validate="key", validatecommand=(vcmd_aircraft, "%P"))
        self.entry_aircraft.bind(
            "<Return>", lambda event: self.update_aircraft("add"))

        self.add_button_aircraft = tkinter.Button(
            master, text="Add Aircraft",
            command=lambda: self.update_aircraft("add"))
        self.reset_button_aircraft = tkinter.Button(
            master, text="Reset",
            command=lambda: self.update_aircraft("reset"))

        # CALCULATION BUTTONS
        self.calc_cost_button = tkinter.Button(
            master, text="Calculate Cost Of Cheapest Route",
            command=self.lowest_cost)
        self.calc_best_distance = tkinter.Button(
            master, text="Calculate Cost Of Shortest Route",
            command=self.shortest_trip_cost)

        # TEXTBOX - OUTPUT GOES HERE

        self.text_box = tkinter.Text(master, height=25, width=100)
        self.scrollbar.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=self.scrollbar.set)

        # LAYOUT

        # AIRPORTS
        self.Airport_label.grid(
            row=0, column=1, sticky=tkinter.W)
        self.label_airports.grid(
            row=0, column=0, pady=20)
        self.entry_airports.grid(
            row=1, column=1)
        self.add_button_airport.grid(
            row=2, column=0, pady=20)
        self.subtract_button_airport.grid(
            row=2, column=1, pady=20)
        self.reset_button_airport.grid(
            row=2, column=2, pady=20)

        # aircraft
        self.aircraft_label.grid(row=4, column=1,
                                 pady=20, sticky=tkinter.W)
        self.label_aircraft.grid(row=4, column=0)
        self.entry_aircraft.grid(row=5, column=1)
        self.add_button_aircraft.grid(row=6, column=1, pady=20)
        self.reset_button_aircraft.grid(
            row=6, column=2, pady=20)

        # Error notifications
        self.error_label.grid(row=7, column=1, columnspan=2,  sticky=tkinter.W)
        self.label_error.grid(row=7, column=0)
        # CALCULATIONS
        self.calc_cost_button.grid(
            row=8, column=0, columnspan=3, pady=30, padx=30,
            sticky=tkinter.W+tkinter.E)
        self.calc_best_distance.grid(
            row=9, column=0, columnspan=3, pady=30, padx=30,
            sticky=tkinter.W+tkinter.E)

        # TEXT
        self.text_box.grid(row=10, column=0, columnspan=3, padx=30)

    def validate_airports(self, new_text):
        if not new_text:
            self.entered_airport = ""
            return True

        try:
            self.entered_airport = str(new_text)
            self.entered_airport = self.entered_airport.upper()
            return True
        except ValueError:
            return False

    def update_airports(self, method):
        if method == "add":
            if self.entered_airport in self.airlist.airport_dict:
                self.airports_list.append(self.entered_airport)
                self.error = "No Errors"
            if len(self.entered_airport) == 0:
                self.error = "You must enter an Airport Code"
            elif self.entered_airport not in self.airlist.airport_dict:
                self.error = "You have entered the wrong Airport Code"

        elif method == "subtract":
            self.airports_list.remove(
                self.airports_list[len(self.airports_list)-1])

        else:  # reset
            self.airports_list = []

        self.Airport_label_text.set(self.airports_list)
        self.entry_airports.delete(0, tkinter.END)
        self.error_label_text.set(self.error)

    def validate_aircraft(self, new_text):
        if not new_text:
            self.entered_aircraft = ""
            return True
        try:
            self.entered_aircraft = str(new_text)
            self.entered_aircraft = self.entered_aircraft.upper()
            return True

        except ValueError:
            return False

    def update_aircraft(self, method):
        if method == "add":
            self.aircraft_code = (self.entered_aircraft)

            if self.aircraft_code in self.aircraft_list.aircraft_dict:
                self.error = "No Errors"
                pass
            if len(self.aircraft_code) == 0:
                self.error = "You must enter a aircraft"
                self.aircraft_code = ""
            elif self.aircraft_code not in self.aircraft_list.aircraft_dict:
                self.error = f"{self.aircraft_code} is not an available aircraft"
                self.aircraft_code = ""

        elif method == "reset":
            self.aircraft_code = ""

        self.aircraft_label_text.set(self.aircraft_code)
        self.entry_aircraft.delete(0, tkinter.END)
        self.error_label_text.set(self.error)

    def display_info(self, trip):

        if self.failed_flight_info is None:
            self.text_box.delete('1.0', tkinter.END)

            self.text_box.insert(
                tkinter.END, "The %s route is: \n%s\n" % (
                    trip, self.aircraft_info["Trip"]))
            self.text_box.insert(tkinter.END, "\nIt's distance is: %s\n" %
                                 self.aircraft_info["Distance"])
            for i in range(1, len(self.aircraft_info)-2):
                self.text_box.insert(tkinter.END, "\nStart airport: %s\n" %
                                     self.aircraft_info[i][0])
                self.text_box.insert(
                    tkinter.END,
                    "End Airport: %s\n" % self.aircraft_info[i][1])
                self.text_box.insert(
                    tkinter.END,
                    "Leg Distance: %s\n" % self.aircraft_info[i][2])
                self.text_box.insert(
                    tkinter.END,
                    "Fuel Required for leg: %s\n" % self.aircraft_info[i][3])
                self.text_box.insert(
                    tkinter.END,
                    "Fuel Purchased: %s\n" % self.aircraft_info[i][4])
                self.text_box.insert(
                    tkinter.END,
                    "Cost of Fuel: %s\n" % self.aircraft_info[i][5])
                self.text_box.insert(tkinter.END, "\n------\n")
            self.text_box.insert(
                tkinter.END,
                "The total cost of the trip was: %s" % self.aircraft_info["Cost"])

        elif self.failed_flight_info is not None:
            self.text_box.delete("1.0", tkinter.END)
            self.text_box.insert(
                tkinter.END, "The selected route is unaccessible with " +
                "the chosen aircraft")
            self.text_box.insert(tkinter.END,
                                 "\nThe leg that is too long is: %s ---> %s" %
                                 (self.failed_flight_info[0].start_airport.name,
                                  self.failed_flight_info[0].end_airport.name))
            self.text_box.insert(
                tkinter.END,
                "\nThe distance of this leg is: %s" % self.failed_flight_info[1])
            self.text_box.insert(
                tkinter.END,
                "\nThe chosen aircraft only has a max flight distance of %s" % self.aircraft.max_fuel)

    def lowest_cost(self):
        if (len(self.aircraft_code) or len(self.airports_list)) < 1:
            self.error = "You must enter some information"
            self.error_label_text.set(self.error)
        else:
            self.aircraft = ac.Aircraft(
                self.aircraft_list, self.aircraft_code)
            triplist = []
            for i in self.airports_list:
                airport = ap.Airport(i, self.airlist.airport_dict)
                triplist.append(airport)

            best_trip = tp.TripPermutations(triplist)
            best_trip.Trip_Permutations()
            best_trip.Route_Distances()
            best_trip.sort_trip_permuatations()
            best_trip.Best_Distance(self.aircraft)
            if best_trip.accessible_routes is not None:
                t = fc.create_sorted_fuel_cost_list(triplist)
                cheapest_route = fc.fuel_calc(
                    self.aircraft, best_trip.accessible_routes, t)
                self.aircraft.fly_route(cheapest_route, t)
                self.aircraft_info = self.aircraft.flight_info
                self.display_info("shortest")
            else:
                self.failed_flight_info = self.aircraft.failed_leg

                self.display_info("shortest")
                self.failed_flight_info = None

    def shortest_trip_cost(self):
        if (len(self.aircraft_code) or len(self.airports_list)) < 1:
            self.error = "You must enter some information"
            self.error_label_text.set(self.error)
        else:
            self.aircraft = ac.Aircraft(self.aircraft_code)
            triplist = []
            for i in self.airports_list:
                airport = ap.Airport(i, self.airlist.airport_dict)
                triplist.append(airport)

            best_trip = tp.TripPermutations(triplist)
            best_trip.Trip_Permutations()
            best_trip.Route_Distances()
            best_trip.sort_trip_permuatations()
            best_trip.Best_Distance(self.aircraft)
            shortest_trip = [(best_trip.shortest_trip,
                              best_trip.shortest_trip.Total_Distance()),
                             best_trip.shortest_trip.distance]

            if best_trip.accessible_routes is not None:
                t = fc.create_sorted_fuel_cost_list(triplist)

                self.aircraft.fly_route(shortest_trip, t)
                self.aircraft_info = self.aircraft.flight_info
                self.display_info("shortest")
            else:
                self.failed_flight_info = self.aircraft.failed_leg
                self.display_info("shortest")
                self.failed_flight_info = None


root = tkinter.Tk()
my_gui = Gui(root)
root.mainloop()
