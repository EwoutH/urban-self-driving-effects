from mesa import Agent
from data import Data
from shapely.geometry import Point

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

    def plan_journey(self):
        pass
        # Get a destination


        # Choose a mode of transport


        # Perform the journey


