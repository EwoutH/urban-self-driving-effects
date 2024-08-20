from mesa import Agent
from data import Data
from shapely.geometry import Point

import numpy as np
import random

data = Data()

class Traveler(Agent):
    # Add counter
    _successful_trips = 0
    _not_successful_trips = 0
    def __init__(self, unique_id, model, pc4, mrdh65):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.has_car: bool
        self.has_license: bool
        self.has_bike = True
        self.available_modes = ["car", "bike", "transit"]
        self.mode: str
        # https://www.kimnet.nl/binaries/kimnet/documenten/publicaties/2023/12/04/nieuwe-waarderingskengetallen-voor-reistijd-betrouwbaarheid-en-comfort/Significance_Value+of+Travel+Time+in+the+Netherlands+2022_final+technical+report.pdf
        self.value_of_time: float = 10.76 / 3600  # in euros per second
        # Assign location
        self.location: Point

        # Assign a pc4 area, weighted by population
        self.pc4: int = int(pc4)
        self.mrdh65: int = int(mrdh65)
        self.mrdh65_name: str = data.mrdh65_to_name[mrdh65]

        self.trip_times = []
        self.destinations = []

        # Match the model.choice_model string to a function. Use Python 3.10 pattern matching.
        # lookup self.choose_mode from dictionary
        self.choose_mode = {
            "random": self.choice_model_random,
            "rational_vot": self.choice_rational_vot
        }[model.choice_model]

    def generate_trip_times(self):
        # Note: There is assumed there is no correlations between the times of the trips.
        # So all trips can be in the morning or evening. On the large scale, this shouldn't matter too much.
        for hour, chance in self.model.trips_by_hour_chance.items():
            # Generate a random number between 0 and 1
            if random.random() < chance:
                # If the random number is less than the chance, the trip is taken.
                # Add a random number between 0 and 1 to the hour.
                self.trip_times.append(hour + random.random())

        # For each trip time, assign a destination based on the origin-destination chance data
        self.destinations = random.choices(population=list(data.od_chance_dicts["Totaal"][self.mrdh65].keys()),
                                           weights=list(data.od_chance_dicts["Totaal"][self.mrdh65].values()),
                                           k=len(self.trip_times))

        # Schedule events for the trip times (use self.model.simulator.schedule_event_absolute)
        for trip_time, destination in zip(self.trip_times, self.destinations):
            self.model.simulator.schedule_event_absolute(function=self.perform_journey, time=trip_time, function_kwargs={"destination": destination})

        # print(f"Agent {self.unique_id} has {len(self.trip_times)} trips scheduled from {self.mrdh65} at times {[f"{t:.3f}" for t in self.trip_times]} to destinations {self.destinations}.")

    def perform_journey(self, destination):
        # Choose a mode of transport
        self.mode = self.choose_mode(destination)
        self.model.trips_by_mode[self.mode] += 1

        if self.mode == "car":
            self.schedule_car_trip(*self.od_car)

        print(f"Agent {self.unique_id} at {self.mrdh65} performs a journey! Time = {self.model.simulator.time:.3f}, destination = {destination}, mode = {self.mode}")

        # Perform the journey

    def choice_model_random(self, destination):
        return random.choice(self.available_modes)

    def choice_rational_vot(self, destination):
        # 100% rational value-of-time model
        # percieved_costs = costs + travel_time * value_of_time
        # Choose the mode with the lowest percieved costs
        percieved_costs = {}
        for mode in self.available_modes:
            travel_time, costs = self.get_travel_time_and_costs(destination, mode)
            percieved_costs[mode] = costs + travel_time * self.value_of_time
        # print(f"Agent {self.unique_id} at {self.mrdh65} to {destination} has percieved costs {percieved_costs}")
        return min(percieved_costs, key=percieved_costs.get)

    def get_travel_time_and_costs(self, destination, mode):
        # Get the travel time and costs for a destination and mode
        match mode:
            case "car":
                # Get travel time from network, costs from distance conversion (fixed per km)
                self.od_car = None
                try:
                    o = self.model.uw.rng.choice(self.model.uw.node_area_dict[self.mrdh65])
                    d = self.model.uw.rng.choice(self.model.uw.node_area_dict[destination])
                    travel_time = self.model.car_travel_time_dict[o.name][d.name]
                    costs = self.model.car_travel_distance_dict[o.name][d.name] * self.model.car_price_per_km_variable
                    self.od_car = (o, d)
                    self.model.successful_car_trips += 1
                except:
                    travel_time = np.inf
                    self.model.failed_car_trips += 1
                    costs = np.inf
            case "bike":
                # Get travel time from Google Maps API, costa are assumed to be zero
                travel_time = data.travel_time_mrdh["bicycling"][(self.mrdh65, destination)]
                costs = 0
            case "transit":
                # Get travel time from Google Maps API, costs from distance conversion (NS staffel)
                travel_time = data.travel_time_mrdh["transit"][(self.mrdh65, destination)]
                distance = data.travel_distance_mrdh["transit"][(self.mrdh65, destination)]
                costs = self.calculate_transit_cost(distance, self.model.transit_price_per_km)
        # print(f"Agent {self.unique_id} at {self.mrdh65} to {destination} by {mode} has travel time {travel_time:.3f}, costs {costs:.2f} and percieved costs {costs + travel_time * self.value_of_time:.2f}")
        return travel_time, costs

    def calculate_transit_cost(self, distance, price_per_km, subscription=False):
        # Calculate the cost of a transit journey based on distance and price per km.
        # Define distance ranges and their corresponding price factors.
        # See https://www.treinonderweg.nl/wat-kost-de-trein.html
        ranges = [(40, 1), (80, .979), (100, .8702), (120, .7),
                  (150, .48), (200, .4), (250, .15), (float('inf'), 0)]

        cost = 0
        prev_limit = 0

        for limit, factor in ranges:
            if distance <= prev_limit:
                break
            km_in_range = min(distance, limit) - prev_limit
            cost += km_in_range * price_per_km * factor
            prev_limit = limit

        return cost

    def schedule_car_trip(self, origin_node, destination_node):
        """"Schedule an event for the car trip with UXsim"""
        self.model.uw.addVehicle(orig=origin_node, dest=destination_node, departure_time=self.model.uw_time)
