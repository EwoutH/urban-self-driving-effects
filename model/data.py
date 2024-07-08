import pickle
import networkx as nx
from pandas import read_pickle


class Data:
    def __init__(self):
        # Load travel time and distance data from Google Maps API
        self.travel_time_pc4 = {}
        self.travel_distance_pc4 = {}

        for mode in ["transit", "bicycling"]:
            with open(f"../travel_api/travel_time_distance_google_{mode}.pkl", "rb") as f:
                self.travel_time_pc4[mode], self.travel_distance_pc4[mode] = pickle.load(f)

        # Load Shapely polygons
        with open("../data/polygons.pkl", "rb") as f:
            self.city_polygon, self.area_polygon = pickle.load(f)

        # Load the population data geodate
        self.pc4_pop = read_pickle("../data/population_data_pc4.pkl")
        self.mrdh_pop = read_pickle("../data/mrdh_pop.pickle")

        # Load the road network
        self.road_network = nx.read_graphml("../network/graphs/merged_network.graphml")

# Initialize the data
# data = Data()
