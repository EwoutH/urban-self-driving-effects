from mesa import Agent
from data import Data
from shapely.geometry import Point

import numpy as np

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
        # Generate 3 random trip times between the model start and end time.
        self.trip_times = [self.model.start_time + (self.model.end_time - self.model.start_time) * np.random.random() for _ in range(3)]
        self.trip_times.sort()

        # Schedule events for the trip times (use self.model.simulator.schedule_event_absolute)
        for trip_time in self.trip_times:
            self.model.simulator.schedule_event_absolute(function=self.perform_journey, time=trip_time)

    def perform_journey(self):
        print(f"Agent {self.unique_id} is performing a journey! Model time = {self.model._time}, simulator time = {self.model.simulator.time}")
        # Get a destination


        # Choose a mode of transport


        # Perform the journey


