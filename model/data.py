import pickle
import pandas as pd
import geopandas as gpd

populated_in_city = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 28, 29, 31, 34, 41, 43, 44, 45}
# Geospatial variable names: description_gdf_area_resolution.pkl

class Data:
    def __init__(self):
        # Load travel time and distance data from Google Maps API
        self.travel_time_mrdh = {}
        self.travel_distance_mrdh  = {}

        for mode in ["transit", "bicycling"]:
            with open(f"../data/travel_time_distance_google_{mode}.pkl", "rb") as f:
                self.travel_time_mrdh[mode], self.travel_distance_mrdh[mode] = pickle.load(f)
                # Convert distance from meters to kilometers
                self.travel_distance_mrdh[mode] = {key: value / 1000 for key, value in self.travel_distance_mrdh[mode].items()}

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
        self.pop_gdf_nl_pc4.set_index("postcode", inplace=True)

        # On 65-area level from V-MRDH
        self.gdf_mrdh_65 = pd.read_pickle("../data/areas_mrdh_weighted_centroids.pkl")

        # Create a dict mapping the gdf_mrdh_65 keys to the ["65x65 Naam"] column
        self.mrdh65_to_name = {n65: name for n65, name in zip(self.gdf_mrdh_65.index, self.gdf_mrdh_65["65x65 Naam"])}

        # Create a dict mapping mrdh65 to pc4. pc4: pop_gdf_nl_pc4["postcode"], mrdh65: pop_gdf_nl_pc4["65x65 Nummer"]
        self.pc4_to_mrdh65 = dict(zip(self.pop_gdf_nl_pc4.index, self.pop_gdf_nl_pc4["65x65 Nummer"]))

        # For both pc4 and mrdh add a column if the centroid is in the target_area
        for target_area, polygon in zip(["in_city", "in_area"], [self.city_polygon_series, self.area_polygon_series]):
            self.pop_gdf_nl_pc4[target_area] = self.pop_gdf_nl_pc4.centroid.within(polygon.geometry[0])
            self.gdf_mrdh_65[target_area] = self.gdf_mrdh_65.centroid.within(polygon.geometry[0])

        # Create a dictionary of pc4 and mrdh65 centroids: index mapped to Geodataframe centroid
        self.centroids_dict_nl_pc4 = {pc4: centroid for pc4, centroid in self.pop_gdf_nl_pc4.centroid.items()}
        self.centroids_dict_mrdh_65 = {n65: centroid for n65, centroid in self.gdf_mrdh_65.centroid.items()}
        self.weighted_centroids_dict_mrdh_65 = {pc4: centroid for pc4, centroid in self.gdf_mrdh_65["weighted_centroid"].items()}

        self.licenses_cars_pc4 = pd.read_pickle("../data/rijbewijzen_personenautos.pkl")

         # Load chance on trip per hour data:
        self.trips_by_hour_chances = pd.read_pickle("../data/trips_by_hour_chances.pickle")
        self.trip_counts_distribution = pd.read_pickle("../data/trip_counts_distribution.pickle")

        # Origin-Destination volumes
        with open("../data/od_chance_dicts.pickle", "rb") as f:
            # totaal, auto, fiets, ov
            self.od_chance_dicts = pickle.load(f)
            # Set all keys higher than 50 to chance 0. We limit trips to roughly the south-holland area.
            for mode in self.od_chance_dicts:
                for origin in self.od_chance_dicts[mode]:
                    for destination in self.od_chance_dicts[mode][origin]:
                        # Remove these if larger API runs are performed.
                        # if destination >= 50:  # MRDH area
                        #     self.od_chance_dicts[mode][origin][destination] = 0
                        # if destination >= 21:  # Inner Rotterdam area.
                        #     self.od_chance_dicts[mode][origin][destination] = 0
                        if destination not in populated_in_city:
                            self.od_chance_dicts[mode][origin][destination] = 0
                        if origin == destination:  # No trips to the same location
                            self.od_chance_dicts[mode][origin][destination] = 0
                    # Normalize the chances back to 1. This skewes the data to more inner city trips, but with a correct total number of trips.
                    total = sum(self.od_chance_dicts[mode][origin].values())
                    if total > 0:
                        self.od_chance_dicts[mode][origin] = {key: value / total for key, value in self.od_chance_dicts[mode][origin].items()}


# Initialize the data
data = Data()
