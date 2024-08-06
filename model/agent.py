from mesa import Agent
from data import Data
from shapely.geometry import Point

import numpy as np
import random

data = Data()

class Traveler(Agent):
    def __init__(self, unique_id, model, pc4, mrdh65):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.has_car: bool
        self.has_license: bool
        self.has_bike = True
        self.available_modes = ["car", "bike", "transit"]
        self.mode: str
        self.value_of_time: float  # in euros per hour
        # Assign location
        self.location: Point
        self.pc4: int
        self.mrdh65: int

        # Assign a pc4 area, weighted by population
        self.pc4 = pc4
        self.mrdh65 = mrdh65

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

        print(f"Agent {self.unique_id} has {len(self.trip_times)} trips scheduled from {self.mrdh65} at times {[f"{t:.3f}" for t in self.trip_times]} to destinations {self.destinations}.")

    def perform_journey(self, destination):
        # Choose a mode of transport
        self.mode = self.choose_mode(destination)

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
        return min(percieved_costs, key=percieved_costs.get)

    def get_travel_time_and_costs(self, destination, mode):
        # Get the travel time and costs for a destination and mode
        travel_time: float
        costs: float
        match mode:
            case "car":
                # Get travel time from network, costs from distance conversion (fixed per km)
                return travel_time, costs
            case "bike":
                # Get travel time from Google Maps API, costa are assumed to be zero
                return travel_time, 0
            case "transit":
                # Get travel time from Google Maps API, costs from distance conversion (NS staffel)
                return travel_time, costs

    def calculate_transit_cost(distance, price_per_km, subscription=False):
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
