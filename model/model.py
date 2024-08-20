# local imports
from agent import Traveler
from data import Data
from traffic import get_uxsim_world

# package imports
from mesa import Model
from mesa.experimental.devs.simulator import DEVSimulator
import numpy as np
import networkx as nx
from collections import defaultdict


data = Data()


class UrbanModel(Model):

    def __init__(self, n_agents=100, step_time=1/12, start_time=6, end_time=23, choice_model="rational_vot", simulator=None):
        super().__init__()
        # Set up simulator time
        self.simulator = simulator
        self.simulator.time = float(start_time)

        # Set up time variables
        self.step_time = step_time
        self.start_time = start_time
        self.end_time = end_time

        # Set up the choice model
        self.choice_model = choice_model
        self.available_modes = ["car", "bike", "transit"]
        self.transit_price_per_km = 0.169  # https://www.treinonderweg.nl/wat-kost-de-trein.html
        self.car_price_per_km_variable = 0.268
        # kleine middenklasse, https://www.nibud.nl/onderwerpen/uitgaven/autokosten/
        self.car_price_per_km_total = 0.604

        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
        # select only the rows where the 65x65 Nummer is in the mrhd65 index
        gdf = gdf[gdf["65x65 Nummer"].isin(range(0, 20))]  # Rotterdam area. Replace with data.gdf_mrdh_65.index to expand to all MRDH area

        # Create a dictionary of pc4 locations and their populations
        self.pop_dict_pc4_city = {pc4: pop for pc4, pop in zip(gdf.index, gdf["aantal_inwoners"])}
        # Normalize the population weights
        weights = np.array(list(self.pop_dict_pc4_city.values())) / sum(self.pop_dict_pc4_city.values())

        # Sample n_agents locations from the dictionary, weighted by population
        locations = np.random.choice(list(self.pop_dict_pc4_city.keys()), n_agents, p=weights)

        for i in range(n_agents):
            self.agents.add(Traveler(i, self, locations[i], gdf["65x65 Nummer"][locations[i]]))

        # For a weekday, take the average of days 0-3 (Monday-Thursday)
        self.trips_by_hour_chance = data.trips_by_hour_chance = data.trips_by_hour_chances.iloc[:, 0:4].mean(axis=1).drop("Total")
        # Drop the hours that are not in the range of the model and save as a dictionary
        self.trips_by_hour_chance = self.trips_by_hour_chance.loc[start_time:(end_time-1)].to_dict()
        print(f"Trips by hour chances: {self.trips_by_hour_chance}")

        # self.trip_counts_distribution = data.trip_counts_distribution.to_dict()
        # print(f"Trip counts distribution: {self.trip_counts_distribution}")

        # UXsim world (from traffic.py)
        self.uw = get_uxsim_world()
        self.G = nx.DiGraph()  # Initialize the graph once
        self._initialize_graph()  # Set up the graph structure

        self.car_travel_time_dict = {}
        self.car_travel_distance_dict = self.get_car_travel_distance()

        # KPIs
        self.trips_by_mode = {mode: 0 for mode in self.available_modes}

        self.successful_car_trips, self.failed_car_trips = 0, 0

        # Request agents to do stuff
        self.agents.do("generate_trip_times")
        print(f"Events scheduled for agents: {len(self.simulator.event_list)} (on average {len(self.simulator.event_list) / n_agents:.2f} per agent)")
        # Schedule a model step
        self.simulator.schedule_event_now(self.step)

    @property
    def uw_time(self):
        return (self.simulator.time - self.start_time) * 3600

    def step(self):
        # Print the current time
        print(f"Model step (sim time: {self.simulator.time:.3f}, uw time: {self.uw_time:.3f})")
        # A step is considerd once the step_time. Default is 1/12 hour (5 minutes).

        # For each agent, initialize times they want to create a trip
        # Add those to the discrete event scheduler to

        # Schedule next even
        self.simulator.schedule_event_relative(function=self.step, time_delta=self.step_time)
        # Run the traffic simulation for the duration of the step_time
        self.uw.exec_simulation(duration_t=self.step_time * 3600)
        # Update travel times
        self.update_car_travel_times()

    def _initialize_graph(self):
        for l in self.uw.LINKS:
            self.G.add_edge(l.start_node.name, l.end_node.name)

    def update_car_travel_times(self):
        for l in self.uw.LINKS:
            self.G[l.start_node.name][l.end_node.name]['weight'] = l.instant_travel_time(self.uw.TIME)

        self.car_travel_time_dict = dict(nx.all_pairs_dijkstra_path_length(self.G, weight='weight'))

    def get_car_travel_distance(self):
        G2 = nx.DiGraph()  # Create a new directed graph

        for l in self.uw.LINKS:
            G2.add_edge(l.start_node.name, l.end_node.name, weight=l.length)

        car_dist_dict = dict(nx.all_pairs_dijkstra_path_length(G2, weight='weight'))
        # Devide by 1000 to convert from meters to kilometers
        return {o: {d: dist / 1000 for d, dist in dist_dict.items()} for o, dist_dict in car_dist_dict.items()}

# Create a simulator and model
simulator1 = DEVSimulator()
model1 = UrbanModel(simulator=simulator1)
simulator1.model = model1

print(f"### Running the model from {model1.start_time} to {model1.end_time}")
simulator1.run_until(model1.end_time)
print(f"### Model finished at {model1.simulator.time}")

# Print some results
total_trips = sum(model1.trips_by_mode.values())
mode_shares = {mode: trips / total_trips for mode, trips in model1.trips_by_mode.items()}
print(f"Trips by mode: {model1.trips_by_mode}\n"
      f"Mode shares: {[f'{mode}: {share:.2%}' for mode, share in mode_shares.items()]}")

print(f"{model1.successful_car_trips} of {model1.successful_car_trips + model1.failed_car_trips} car trips were successful.")

