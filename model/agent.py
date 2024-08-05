from mesa import Agent
from data import Data
from shapely.geometry import Point

import numpy as np
import random

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

    def generate_trip_times(self):
        # Note: There is assumed there is no correlations between the times of the trips.
        # So all trips can be in the morning or evening. On the large scale, this shouldn't matter too much.
        self.trip_times = []
        for hour, chance in self.model.trips_by_hour_chance.items():
            # Generate a random number between 0 and 1
            if random.random() < chance:
                # If the random number is less than the chance, the trip is taken.
                # Add a random number between 0 and 1 to the hour.
                self.trip_times.append(hour + random.random())

        # Schedule events for the trip times (use self.model.simulator.schedule_event_absolute)
        for trip_time in self.trip_times:
            self.model.simulator.schedule_event_absolute(function=self.perform_journey, time=trip_time)

    def perform_journey(self):
        print(f"Agent {self.unique_id} is performing a journey! Time = {self.model.simulator.time:.3f}")
        # Get a destination


        # Choose a mode of transport


        # Perform the journey


