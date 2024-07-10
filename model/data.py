import pickle
import networkx as nx
import pandas as pd
import geopandas as gpd

# Geospatial variable names: description_gdf_area_resolution.pkl

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

        self.city_polygon_series = gpd.GeoSeries(self.city_polygon, crs="epsg:4326")
        self.city_polygon_series = self.city_polygon_series.to_crs(epsg=28992)

        self.area_polygon_series = gpd.GeoSeries(self.area_polygon, crs="epsg:4326")
        self.area_polygon_series = self.area_polygon_series.to_crs(epsg=28992)

        # Load the population data geodataframes
        # On PC4 level (postal code areas)
        self.pop_gdf_nl_pc4 = pd.read_pickle("../data/population_data_pc4_65coded.pkl")

        # On 65-area level from V-MRDH
        self.gdf_mrdh_65 = pd.read_pickle("../data/areas_mrdh_weighted_centroids.pkl")

        # Load the road network
        self.road_network = nx.read_graphml("../network/graphs/merged_network.graphml")

        # For both pc4 and mrdh add a column if the centroid is in the target_area
        for target_area, polygon in zip(["in_city", "in_area"], [self.city_polygon_series, self.area_polygon_series]):
            self.pop_gdf_nl_pc4[target_area] = self.pop_gdf_nl_pc4.centroid.within(polygon.geometry[0])
            self.gdf_mrdh_65[target_area] = self.gdf_mrdh_65.centroid.within(polygon.geometry[0])

        # Create a dictionary of pc4 and mrdh65 centroids: index mapped to Geodataframe centroid
        self.centroids_dict_nl_pc4 = {pc4: centroid for pc4, centroid in self.pop_gdf_nl_pc4.centroid.items()}
        self.centroids_dict_mrdh_65 = {n65: centroid for n65, centroid in self.gdf_mrdh_65.centroid.items()}
        self.weighted_centroids_dict_mrdh_65 = {pc4: centroid for pc4, centroid in self.gdf_mrdh_65["weighted_centroid"].items()}

# Initialize the data
data = Data()
