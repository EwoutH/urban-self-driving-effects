#%% md
# ## Transit Travel time & distance
# Using the Google maps API
#%%
import googlemaps
import geopandas as gpd
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from pygments.styles.dracula import background
#%%
# Load data
mrdh = pd.read_pickle("../v_mrdh/areas_mrdh.pkl")
print("Source CRS:", mrdh.crs)
mrdh.head()
#%%
# Load NS stations
ns_stations = pd.read_pickle("../travel_api/urban_stations.pkl")
print("Source CRS:", ns_stations.crs)
ns_stations.head()
#%%
# Load the polygons from pickle
with open("../data/polygons.pkl", "rb") as f:
    city_polygon, area_polygon, autoluw_polygon = pickle.load(f)
#%%
fig, ax = plt.subplots(figsize=(16, 12))
# Filter data to only include postcodes in the Randstad
mrdh.plot(column="GEBIEDEN", figsize=(16, 12), ax=ax)
# Add the centroids
mrdh.centroid.plot(ax=ax, color="red")
# Add the name labels above the centroids
for x, y, label in zip(mrdh.centroid.x, mrdh.centroid.y-750, mrdh["65x65 Naam"]):
    ax.text(x, y, label, color="black", fontsize=5, ha="center")
    
# Add the NS stations
ns_stations.plot(ax=ax, color="green")
# Add the name labels above the NS stations
for x, y, label in zip(ns_stations.geometry.x, ns_stations.geometry.y, ns_stations["name"]):
    ax.text(x, y, label, color="white", fontsize=5, ha="center")

# Add the city polygon (CRS 3857)
city_polygon_series = gpd.GeoSeries(city_polygon, crs="epsg:4326")
# Convert to epsg:28992
city_polygon_series = city_polygon_series.to_crs(epsg=28992)
city_polygon_series.plot(ax=ax, color="black", alpha=0.5)
# Add a title
plt.title("Areas in MRDH, their centroids and NS stations")
# Save the plot
plt.savefig("img/areas_mrdh_ns_stations.png", dpi=300, bbox_inches="tight")
#%% md
# ### Add the 65x65 areas to the population data
#%%
# Load areas_65.pkl
areas_65 = pd.read_pickle("../v_mrdh/areas_65.pkl")
#%%
# Load the population data
population = pd.read_pickle("../data/population_data_pc4.pkl")
# Remove 0 inhabitants
population = population[population['aantal_inwoners'] > 0]
#%%
# Perform the spatial join with the 'touches' predicate
pop_mrdh = gpd.sjoin(population, areas_65, how='inner', predicate='intersects')

# Calculate the intersection areas
pop_mrdh['intersection_area'] = pop_mrdh.apply(
    lambda row: row.geometry.intersection(areas_65.loc[row['65x65 Nummer']].geometry).area, axis=1
)

# Sort the result by intersection area in descending order and drop duplicates, keeping the largest
pop_mrdh = pop_mrdh.sort_values(by='intersection_area', ascending=False)
# Drop duplicates, keeping one row per postcode
pop_mrdh = pop_mrdh.drop_duplicates(subset='postcode', keep='first')
#%%
# Stupid fix for an extra polygon in the multipolygon geometry in postcode 3053 and 2641
from shapely.geometry import MultiPolygon

pop_mrdh.loc[pop_mrdh["postcode"] == 3053, 'geometry'] = pop_mrdh.loc[pop_mrdh["postcode"] == 3053, 'geometry'].apply(lambda geom: MultiPolygon(list(geom.geoms)[:-1]) if isinstance(geom, MultiPolygon) else geom)
pop_mrdh.loc[pop_mrdh["postcode"] == 2641, 'geometry'] = pop_mrdh.loc[pop_mrdh["postcode"] == 2641, 'geometry'].apply(lambda geom: MultiPolygon(list(geom.geoms)[:-1]) if isinstance(geom, MultiPolygon) else geom)
#%%
# Remove areas with 0 INWONERS_A
pop_mrdh = pop_mrdh[pop_mrdh['INWONERS_A'] > 0]
mrdh = mrdh[mrdh['INWONERS_A'] > 0]

# Remove areas from mrdh with no population
# mrdh = mrdh[mrdh.index.isin(pop_mrdh['65x65 Nummer'])]
#%%
# Save 
pop_mrdh.to_pickle("../data/population_data_pc4_65coded.pkl")
#%% md
# ### Calculate weighted centroids
#%%
# Drop any columns with a 65x65 Nummer that not in the mrdh index
pop_mrdh_sel = pop_mrdh[pop_mrdh['65x65 Nummer'].isin(mrdh.index)]
#%%
from shapely.geometry import Point

# Step 1: Group by 65x65 Nummer
grouped = pop_mrdh_sel.groupby('65x65 Nummer')

# Step 2: Calculate weighted centroids
def weighted_centroid(group):
    total_population = group['aantal_inwoners'].sum()
    wx = (group.geometry.centroid.x * group['aantal_inwoners']).sum() / total_population
    wy = (group.geometry.centroid.y * group['aantal_inwoners']).sum() / total_population
    return pd.Series({'geometry': Point(wx, wy), 'total_population': total_population})

# Apply the function to selected columns
weighted_centroids = grouped[['geometry', 'aantal_inwoners']].apply(weighted_centroid).reset_index()

# Step 3: Create a new geodataframe with the results. Set the 65x65 Nummer as the index
result_gdf = gpd.GeoDataFrame(weighted_centroids, geometry='geometry')
result_gdf.set_index('65x65 Nummer', inplace=True)

# Step 4: Add the weighted centroids to the mrdh geodataframe
mrdh = mrdh.copy()  # Create a copy to avoid SettingWithCopyWarning
mrdh.loc[:, 'weighted_centroid'] = result_gdf['geometry']

# Save the result
mrdh.to_pickle("../data/areas_mrdh_weighted_centroids.pkl")
#%%
# Plot the population over the map
fig, ax = plt.subplots(figsize=(16, 12))
pop_mrdh_sel.plot(figsize=(16, 12), ax=ax, alpha=0.5, column="65x65 Nummer", cmap="tab20b", edgecolor="black")
mrdh.plot(column=mrdh.index.values, figsize=(16, 12), ax=ax, cmap='tab20b', alpha=0.5, edgecolor='red')
# Add the centroids
mrdh.centroid.plot(ax=ax, color="red")
# Add the weighted centroids
mrdh.weighted_centroid.plot(ax=ax, color="blue")
# Add the NS stations, as a triangle
ns_stations.plot(ax=ax, color="green", marker="^", markersize=25)
# Add a legend
ax.legend(["Geographic centroids", "Weighted centroids", "NS stations"])
# Save the plot
plt.savefig("img/population_areas_mrdh2.png", dpi=300, bbox_inches="tight")
#%%
# Save the population data
pop_mrdh_sel.to_pickle("../data/population_data_pc4_mrdh.pkl")
#%%
city_polygon
#%%
# Select only the 65x65 areas with centroids in the polygon (city_polygon_series
city65 = mrdh[mrdh.centroid.within(city_polygon_series.geometry[0])]
pc65 = pop_mrdh_sel[pop_mrdh_sel['65x65 Nummer'].isin(city65.index)]

# Select the NS stations within the polygon
ns_stations_city = ns_stations[ns_stations.geometry.within(city_polygon_series.geometry[0])]
#%% md
# 
#%%
# Generate a increasing list of unique color values, from 0 to n based on the unique 65x65 Nummers
color_number_dict = {n: i for i, n in enumerate(city65.index)}
pc65["Color"] = pc65["65x65 Nummer"].map(color_number_dict)
city65["Color"] = city65.index.map(color_number_dict)
#%%
# Combine colors from tab20 and Set1
from matplotlib.colors import ListedColormap
colors = plt.cm.tab20.colors + plt.cm.Set1.colors
custom_cmap = ListedColormap(colors)

# Plot
fig, ax = plt.subplots(figsize=(16, 12))
# city65.plot(column="Color", ax=ax, cmap=custom_cmap, alpha=0.5, edgecolor='red')
pc65.plot(column="Color", ax=ax, alpha=0.5, cmap=custom_cmap, edgecolor="black")

# Add the MRDH 65 names above each weighted centroid
for x, y, label in zip(city65.weighted_centroid.x, city65.weighted_centroid.y, city65["65x65 Naam"]):
    ax.text(x, y+200, f"{label}", color="black", fontsize=8, ha="center", va="bottom", backgroundcolor=(1, 1, 1, 0.5))
# Add the pc4 numbers to each 
for x, y, label in zip(pc65.geometry.centroid.x, pc65.geometry.centroid.y, pc65["postcode"]):
    ax.text(x, y, f"{label}", color="black", fontsize=5, ha="center")

# Add the centroids
# city65.centroid.plot(ax=ax, color="blue")
# Add the weighted centroids
city65.weighted_centroid.plot(ax=ax, color="red")
# Add the NS stations, as a triangle
# ns_stations_city.plot(ax=ax, color="red", marker="^", markersize=25)

# Remove the grid
ax.set_axis_off()
    
# Add a legend
ax.legend(["Population-weighted centroids"])

# Save the plot
plt.savefig("img/rotterdam_mrdh65_pc4_areas.svg",bbox_inches="tight")
#%%
# Set postcode as the index for pc65
pc65.set_index("postcode", inplace=True)

# To dict and save
pc4_to_n65_dict = pc65["65x65 Nummer"].to_dict()
with open("../data/pc4_to_n65_dict.pkl", "wb") as f:
    pickle.dump(pc4_to_n65_dict, f)
#%% md
# ### Google maps API
#%%
# time: 2024-09-17 08:00:00 (a Thursday)
time = datetime(2024, 9, 19, 8, 0, 0)
print(time)
#%%
# Select stedelijkheid 5 or higher
data_sel = pc65.copy()
# Sort by MRDH area, index
data_sel.sort_values(by=["65x65 Nummer", "postcode"], inplace=True)
# Calculate centroids
data_sel["centroid"] = data_sel["geometry"].centroid

# Convert to EPSG:4326
print("Source CRS:", data_sel.crs)
data_sel = data_sel.to_crs(epsg=4326)
data_sel["centroid"] = data_sel["centroid"].to_crs(epsg=4326)
print("New CRS:", data_sel.crs)
data_sel.head(3)
#%%
# Get API key from /secrets/gmaps_api_key.txt
with open("../secrets/gmap_api_key.txt") as f:
    api_key = f.readline()
#%%
# # Single query
# time_1 = datetime(2024, 7, 2, 8, 30, 0)
# origin_1 = ["Rotterdam Alexander, 3068 AV Rotterdam"]
# destinations_1 = ["Delft Campus, 2623 CS Delft"]
# mode_1 = "transit"
# run_1 = False
# 
# if run_1:
#     gmaps = googlemaps.Client(key=api_key)
#     result = gmaps.distance_matrix(
#         origins=origin_1,
#         destinations=destinations_1,
#         mode=mode_1,
#         departure_time=time_1,
#     )
#     result
#%%
### Warning: This can be a very expensive cell to run. 5 USD per 1000 elements. The full 125x125 matrix is 78.125 USD, so for both modes it is 156.25 USD. 
def run_google_maps(mode, redownload=False):
    if redownload:
        gmaps = googlemaps.Client(key=api_key)
        
        # Extract centroids and convert them to a suitable format for the Google Maps API
        centroids = data_sel["centroid"].to_list()
        # Select only the first 3 centroids for testing
        centroids = centroids[:4]
        # Note the order of the coordinates: (latitude (y), longitude (x))
        locations = [(centroid.y, centroid.x) for centroid in centroids]
        print(f"{len(locations)} locations: {locations}")
    
        # Initialize dictionaries to hold the travel info
        travel_time_pc4 = {}
        travel_distance_pc4 = {}
    
        # Function to split destinations into chunks of max_chunk_size
        def chunk_destinations(destinations, max_chunk_size=25):
            chunk = [destinations[i:i + max_chunk_size] for i in range(0, len(destinations), max_chunk_size)]
            return chunk

        for i, origin in enumerate(locations):
            destinations = locations
            destination_chunks = chunk_destinations(destinations)

            for chunk in destination_chunks:
                result = gmaps.distance_matrix(
                    origins=[origin],
                    destinations=chunk,
                    mode=mode,
                    departure_time=time,
                )

                # Extract distances and populate the corresponding row in the distance matrix
                for j, destination in enumerate(chunk):
                    if origin != destination:
                        element = result["rows"][0]["elements"][j]
                        destination_index = destinations.index(destination)
                        key = (i, destination_index)
                        
                        if element["status"] == "OK":
                            distance_meters = element["distance"]["value"]
                            duration_seconds = element["duration"]["value"]
                            
                            # Update the travel info dictionaries
                            travel_distance_pc4[key] = distance_meters
                            travel_time_pc4[key] = duration_seconds
                        else:
                            print(f"Error for {key}: {element['status']}")
                        
                        if i == 0 and destination_index == 1:
                            print(f"Example for {key}: {element}")
            # Break after the second origin
            if i == 1:
                break

        # Correct dict keys. The keys are now (index, index) instead of (n65, n65)
        key_to_n65 = {i: n65 for i, n65 in enumerate(data_sel.index)}
        travel_time_pc4 = {(key_to_n65[key[0]], key_to_n65[key[1]]): value for key, value in travel_time_pc4.items()}
        travel_distance_pc4 = {(key_to_n65[key[0]], key_to_n65[key[1]]): value for key, value in travel_distance_pc4.items()}

        # Save as pickle
        with open(f"../data/travel_time_distance_google_{mode}_pc4.pkl", "wb") as f:
            pickle.dump((travel_time_pc4, travel_distance_pc4), f)
        print(f"Saved travel_time_distance_google_{mode}_pc4.pkl")

    else:
        print(f"Skipping Google Maps API, loading: travel_time_distance_google_{mode}_pc4.pkl")
        with open(f"../data/travel_time_distance_google_{mode}_pc4.pkl", "rb") as f:
            travel_time_pc4, travel_distance_pc4 = pickle.load(f)

    return travel_time_pc4, travel_distance_pc4

# Run the Google Maps API
travel_time_dict = {}
travel_distance_dict = {}

redownload = False
for mode in ["transit", "bicycling"]:
    travel_time, travel_distance = run_google_maps(mode=mode, redownload=redownload)
    travel_time_dict[mode] = travel_time
    travel_distance_dict[mode] = travel_distance
#%%
key_list = list(travel_time_dict["transit"].keys())
# The keys are tuples. Get the unique values for the first element
unique_keys = set([key[0] for key in key_list])
print(f"Unique keys: {unique_keys}")
#%%
# Create a combined name: 65x65 Naam (pc4)
data_sel["combined_name"] = data_sel["65x65 Naam"] + " (" + data_sel.index.astype(str) + ")"
print(data_sel[["65x65 Naam", "combined_name"]].head(3))
n65_to_name = data_sel["combined_name"].to_dict()

# replace the (index, index) keys with the (name, name) keys
for mode in travel_time_dict.keys():
    travel_time_dict[mode] = {(n65_to_name[key[0]], n65_to_name[key[1]]): value for key, value in travel_time_dict[mode].items()}
    travel_distance_dict[mode] = {(n65_to_name[key[0]], n65_to_name[key[1]]): value for key, value in travel_distance_dict[mode].items()}
#%%
# Create dataframe from the first mode in the dictionary
first_mode = next(iter(travel_time_dict))
travel_time_df = pd.DataFrame.from_dict(travel_time_dict[first_mode], orient='index', columns=[first_mode])

# Add columns for other modes
for mode, times in travel_time_dict.items():
    if mode != first_mode:
        travel_time_df[mode] = times.values()

# Split index into Origin and Destination
travel_time_df.index = pd.MultiIndex.from_tuples(travel_time_df.index, names=['Origin', 'Destination'])
travel_time_df["trans-bike-diff"] = travel_time_df["transit"] - travel_time_df["bicycling"]
travel_time_df.head(3)
#%%
# Create two subplots
fig, axs = plt.subplots(1, 3, figsize=(60, 15))

# Get the max value
max_value = travel_time_df[["transit", "bicycling"]].max().max()

# Directly use travel_time_df
for i, mode in enumerate(travel_time_dict.keys()):
    # Heatmap with seaborn. Use the max value as the max value for the color scale
    sns.heatmap((travel_time_df[mode]/60).unstack(), annot=False, fmt=".0f", cmap="Reds", ax=axs[i], square=True, vmax=max_value/60)
    axs[i].set_title(f"Travel time by {mode} (minutes)")

# Add a plot with the difference between the two modes. Set 0 as the middle value.
sns.heatmap((travel_time_df["trans-bike-diff"]/60).unstack(), annot=False, fmt=".0f", cmap="PRGn", ax=axs[2], center=0, square=True)
axs[2].set_title("Difference transit - bicycling (minutes)\nPositive values means cycling is faster")

# Add title
plt.suptitle("Travel time between MRDH areas in Rotterdam urban area by mode")
# Save the plot
plt.savefig("img/travel_time_heatmap.png", dpi=300, bbox_inches="tight")
#%%
# Create a histogram and boxplot side-by-side
fig, axes = plt.subplots(1, 2, figsize=(20, 8), gridspec_kw={'width_ratios': [5, 1]})

# Plot the histograms.
sns.histplot(travel_time_df[['bicycling', 'transit']]/60, kde=True, ax=axes[0], bins=range(0, 180, 2))
axes[0].set_xlim(0, 120)
axes[0].set_xticks(range(0, 121, 10))
axes[0].set_xlabel("Travel time (minutes)")

# Plot the boxplots
sns.boxplot(travel_time_df[['bicycling', 'transit']]/60, ax=axes[1], showmeans=True)
axes[1].set_ylabel("Travel time (minutes)")

# Add title
plt.suptitle("Travel time distribution between all 125 postal code areas pairs by bike and transit", y=0.92)
# Save the plot
plt.savefig("../img/travel_time_google_maps_api_hist_boxplot.svg", bbox_inches="tight")
#%%
# Convert the data to epsg:28992
data = data_sel.to_crs(epsg=28992)
#%%
mode_m = "bicycling"
origin_m = "Rotterdam Centrum (3013)"
# Plot a map with the travel time from Rotterdam Centrum to all other areas. Green means short travel time, red means long travel time
fig, ax = plt.subplots(figsize=(16, 12))
data.plot(column="GEBIEDEN", figsize=(16, 12), ax=ax)
# Add the name labels above the centroids
for x, y, label in zip(data.centroid.x, data.centroid.y-250, data["combined_name"]):
    # Replace the " (" with a newline
    label = label.replace(" (", "\n(")
    ax.text(x, y, label, color="black", fontsize=5, ha="center")
# Add the travel time from Rotterdam Centrum
for idx, row in data.iterrows():
    destination = row["combined_name"]
    if destination == origin_m:
        continue
    travel_time = travel_time_dict[mode_m][(origin_m, destination)]
    if travel_time is not None:
        color = sns.color_palette("coolwarm", as_cmap=True)(travel_time / travel_time_df[mode].max())
        data[data["combined_name"] == destination].plot(color=color, ax=ax)
# Set title
plt.title(f"Travel time from {origin_m} by {mode_m}")
# Add the centroids
data.centroid.plot(ax=ax, color="red")
# Save the plot
# plt.savefig(f"img/travel_time_{origin_m.lower().replace(' ', '_')}_{mode_m}.png", dpi=300, bbox_inches="tight")
#%%
from geopy.distance import geodesic
#%%
# Calculate the distance between all centroids
distances = {}
for i, origin in data_sel.iterrows():
    for j, destination in data_sel.iterrows():
        if i != j:
            key = (origin["combined_name"], destination["combined_name"])
            distances[key] = geodesic((origin["centroid"].y, origin["centroid"].x), (destination["centroid"].y, destination["centroid"].x)).kilometers
#%%
# Add the distances to the travel_time_df
travel_time_df["distance"] = [distances[key] for key in travel_time_df.index]
travel_time_df.head()
#%%
# Create two subplots
fig, axs = plt.subplots(1, 2, figsize=(20, 8))

for i, mode in enumerate(travel_time_dict.keys()):
    # Scatter plot with seaborn
    sns.scatterplot(data=travel_time_df, x="distance", y=mode/60, ax=axs[i])
    axs[i].set_title(mode.capitalize())
    axs[i].set_xlabel("Distance (km)")
    axs[i].set_ylabel("Travel time (seconds)")
    # X and y axis start at 0
    axs[i].set_xlim(0, None)
    axs[i].set_ylim(0, None)

# Add title
plt.suptitle("Scatter plot of travel time vs geodesic (bird's flight) distance") 
# Save the plot
plt.savefig("img/travel_time_distance_scatter.png", dpi=300, bbox_inches="tight")
#%% md
# ### Areas and resolutions
# This project has 4 relevant areas:
# - The Netherlands
# - The Metropoolregio Rotterdam Den Haag (MRDH)
# - The "area" polygon, which is currently Rotterdam with some margin, custom defined.
# - The "city" polygon, which is the currently city of Rotterdam, custom defined.
# 
# The resolutions are as follows:
# - pc4: Postcode 4, the first 4 digits of the postcode
# - v65: The 65x65 areas, as used in the V-MRDH traffic model
#%%
# Calculate r-square
import numpy as np
from sklearn.linear_model import LinearRegression

# Create a linear regression model
model = LinearRegression()

# Fit the model
model.fit(travel_time_df["distance"].values.reshape(-1, 1
), travel_time_df["transit"].values)

# Get the R^2 value
r_squared = model.score(travel_time_df["distance"].values.reshape(-1, 1), travel_time_df["transit"].values)
print(f"R^2 value: {r_squared}")

# bike
model.fit(travel_time_df["distance"].values.reshape(-1, 1
), travel_time_df["bicycling"].values)

# Get the R^2 value
r_squared = model.score(travel_time_df["distance"].values.reshape(-1, 1), travel_time_df["bicycling"].values)
print(f"R^2 value: {r_squared}")
#%%
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Plot the outlines of the different relevant areas
fig, ax = plt.subplots(figsize=(16, 12))

# Plot the outlines of the areas
nl_outline = population.union_all()
gpd.GeoSeries(nl_outline).plot(ax=ax, color="blue", alpha=0.5, edgecolor="blue")

mrdh_outline = mrdh.union_all()
gpd.GeoSeries(mrdh_outline).plot(ax=ax, color="green", alpha=0.5, edgecolor="green")

area_polygon_series = gpd.GeoSeries(area_polygon, crs="epsg:4326").to_crs(epsg=28992)
area_polygon_series.plot(ax=ax, color="yellow", alpha=0.5, edgecolor="yellow")

city_polygon_series.plot(ax=ax, color="red", alpha=0.5, edgecolor="red")

# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color='blue', lw=4, label='The Netherlands'),
    Line2D([0], [0], color='green', lw=4, label='MRDH'),
    Line2D([0], [0], color='yellow', lw=4, label='Area'),
    Line2D([0], [0], color='red', lw=4, label='City')
]

# Add a legend to the plot and save it
ax.legend(handles=legend_elements, loc='upper left')
plt.title("Outlines of the different relevant areas")
plt.savefig("img/area_outlines.png", dpi=300, bbox_inches="tight")
#%%
