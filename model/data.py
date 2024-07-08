# Dataclass

from dataclasses import dataclass
import pickle

@dataclass
class Data:
    travel_time_pc4: dict
    travel_distance_pc4: dict

    def __init__(self):
        # Load travel time and distance data from Google Maps API
        for mode in ["transit", "bicycling"]:
            with open(f"../travel_api/travel_time_distance_google_{mode}.pkl", "rb") as f:
                self.travel_time_pc4[mode], self.travel_distance_pc4[mode] = pickle.load(f)
