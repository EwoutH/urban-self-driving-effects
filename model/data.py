import pickle
import networkx as nx
import pandas as pd
import geopandas as gpd


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
        self.pc4_gdf = pd.read_pickle("../data/population_data_pc4_65coded.pkl")

        # On 65-area level from V-MRDH
        self.mrdh65_gdf = pd.read_pickle("../v_mrdh/areas_mrdh.pkl")

        # Load the road network
        self.road_network = nx.read_graphml("../network/graphs/merged_network.graphml")

        # For both pc4 and mrdh add a column if the centroid is in the target_area
        for target_area, polygon in zip(["in_city", "in_area"], [self.city_polygon_series, self.area_polygon_series]):
            self.pc4_gdf[target_area] = self.pc4_gdf.centroid.within(polygon.geometry[0])
            self.mrdh65_gdf[target_area] = self.mrdh65_gdf.centroid.within(polygon.geometry[0])

        # Create a dictionary of pc4 and mrdh65 centroids: index mapped to Geodataframe centroid
        self.pc4_centroids = {pc4: centroid for pc4, centroid in self.pc4_gdf.centroid.items()}
        self.mrdh_centroids = {mrdh: centroid for mrdh, centroid in self.mrdh65_gdf.centroid.items()}
        print(f"{len(self.mrdh_centroids)} mrhd_centroids: {self.mrdh_centroids}")

# Initialize the data
data = Data()
