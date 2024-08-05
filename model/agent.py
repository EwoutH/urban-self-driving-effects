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
        # Assign location
        self.location: Point
        self.pc4: int
        self.mrdh65: int

        # Assign a pc4 area, weighted by population
        self.pc4 = pc4
        self.mrdh65 = mrdh65

        self.trip_times = []
        self.destinations = []

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
        print(f"Agent {self.unique_id} at {self.mrdh65} is performing a journey! Time = {self.model.simulator.time:.3f}, destinations = {destination}")

        # Choose a mode of transport

        # Perform the journey

