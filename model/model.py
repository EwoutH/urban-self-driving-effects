# local imports
from agent import Traveler
from data import Data
from traffic import get_uxsim_world

# package imports
from mesa import Model
from mesa.experimental.devs.simulator import DEVSimulator
import numpy as np
import networkx as nx


data = Data()
real_population = 991575  # sum(self.pop_dict_pc4_city.values())
simulated_population = int(real_population / 10)  # UXsim platoon size


class UrbanModel(Model):
    def __init__(self, n_agents=simulated_population, step_time=1/12, data_time=900, start_time=7, end_time=9, choice_model="rational_vot", enable_av=True, av_cost_factor=0.2, av_vot_factor=0.2, simulator=None):
        super().__init__()
        print(f"### Initializing UrbanModel with {n_agents} agents, step time {step_time:.3f} hours, start time {start_time}, end time {end_time}, choice model {choice_model}, AV enabled {enable_av}, AV cost factor {av_cost_factor}, AV VOT factor {av_vot_factor}.")
        # Set up simulator time
        self.simulator = simulator
        self.simulator.time = float(start_time)

        # Set up time variables
        self.step_time = step_time
        self.data_time = data_time
        self.start_time = start_time
        self.end_time = end_time

        # Set up the choice model
        self.choice_model = choice_model
        self.available_modes = ["car", "bike", "transit"]
        if enable_av:
            self.available_modes.append("av")
        self.transit_price_per_km = 0.169  # https://www.treinonderweg.nl/wat-kost-de-trein.html
        self.car_price_per_km_variable = 0.268
        # kleine middenklasse, https://www.nibud.nl/onderwerpen/uitgaven/autokosten/
        self.car_price_per_km_total = 0.604
        self.av_initial_costs = 3.79 * av_cost_factor
        self.av_costs_per_km = 1.41 * av_cost_factor  # TODO: Update from Waymo regression https://waymo-pricing.streamlit.app/
        self.av_costs_per_sec = 0.40 / 60 * av_cost_factor
        self.av_vot_factor = av_vot_factor
        # https://www.kimnet.nl/binaries/kimnet/documenten/publicaties/2023/12/04/nieuwe-waarderingskengetallen-voor-reistijd-betrouwbaarheid-en-comfort/Significance_Value+of+Travel+Time+in+the+Netherlands+2022_final+technical+report.pdf
        self.default_value_of_times = {
            "car": 10.42,
            "bike": 10.39,
            "transit": 7.12,
        }
        self.default_value_of_times["av"] = self.default_value_of_times["car"] * self.av_vot_factor
        print(f"Default value of times: {self.default_value_of_times} (€/hour)")
        self.default_value_of_times = {mode: vot / 3600 for mode, vot in self.default_value_of_times.items()}  # Euros per second

        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
        gdf = gdf[gdf["aantal_inwoners"] > 100]  # Filter out insignificant areas (from 129 to 124)

        # select only the rows where the 65x65 Nummer is in the mrhd65 index
        gdf = gdf[gdf["65x65 Nummer"].isin(data.gdf_mrdh_65.index)]  # Rotterdam area.

        # Create a dictionary of pc4 locations and their populations
        self.pop_dict_pc4_city = {pc4: pop for pc4, pop in zip(gdf.index, gdf["aantal_inwoners"])}
        # Normalize the population weights
        weights = np.array(list(self.pop_dict_pc4_city.values())) / sum(self.pop_dict_pc4_city.values())

        # Sample n_agents locations from the dictionary, weighted by population
        locations = np.random.choice(list(self.pop_dict_pc4_city.keys()), n_agents, p=weights)

        for i in range(n_agents):
            Traveler(i, self, pc4=locations[i], mrdh65=gdf["65x65 Nummer"][locations[i]])

        for pc4 in self.pop_dict_pc4_city.keys():
            # Dataframe is indexed by pc4, so we can directly access the number of licenses and cars
            license_chance, car_chance = data.licenses_cars_pc4.loc[int(pc4)]
            trav = self.agents.select(lambda a: a.pc4 == pc4)

            # Give license_chance of the agents a license
            trav_license = trav.shuffle(inplace=True).select(at_most=license_chance).set('has_license', True)
            # Of those with a license, give n_car agents a car
            n_car = round(len(trav) * car_chance)
            trav_license.shuffle(inplace=True).select(at_most=n_car).set('has_car', True)

        # Get all the unique mrdh65 values
        self.areas = list(set([a.mrdh65 for a in self.agents]))
        self.pc4s = list(set([a.pc4 for a in self.agents]))

        # For agents that don't have a car, remove the car from the available modes
        self.agents.select(lambda a: not a.has_car).do(lambda a: setattr(a, 'available_modes', [m for m in a.available_modes if m != "car"]))
        # TODO: Implement some car sharing / lending from friends/family thing here.
        # Update currently available modes after having assigned cars
        self.agents.do(lambda a: setattr(a, 'currently_available_modes', a.available_modes))

        # For a weekday, take the average of days 0-3 (Monday-Thursday)
        self.trips_by_hour_chance = data.trips_by_hour_chance = data.trips_by_hour_chances.iloc[:, 0:4].mean(axis=1).drop("Total")
        # Drop the hours that are not in the range of the model and save as a dictionary
        self.trips_by_hour_chance = self.trips_by_hour_chance.loc[start_time:(end_time-1)].to_dict()
        print(f"Trip chance sum: {sum(self.trips_by_hour_chance.values()):.3f}, chance by hour: {self.trips_by_hour_chance}")

        # self.trip_counts_distribution = data.trip_counts_distribution.to_dict()
        # print(f"Trip counts distribution: {self.trip_counts_distribution}")

        # UXsim world (from traffic.py)
        self.uw = get_uxsim_world(save_mode=False, show_mode=True)

        self.car_travel_distance_dict = self.get_car_travel_distance()

        # KPIs
        self.trips_by_mode = {mode: 0 for mode in self.available_modes}
        # Create nested dict
        self.trips_by_hour_by_mode = {(hour, mode): 0 for hour in range(start_time, end_time) for mode in self.available_modes}
        self.uxsim_data = {}
        self.parked_per_area = {area: 0 for area in self.areas}
        groups = self.agents.select(lambda a: a.has_car).groupby(by="mrdh65", result_type="list")
        parked = {area: len(group) for area, group in groups}
        self.parked_per_area.update(parked)
        print(f"Parked per area: {self.parked_per_area}")

        self.successful_car_trips, self.failed_car_trips = 0, 0

        # Request agents to do stuff
        self.agents.do("generate_trip_times")
        print(f"Events scheduled for agents: {len(self.simulator.event_list)} (on average {len(self.simulator.event_list) / n_agents:.3f} per agent)")

        self.uw.finalize_scenario()
        # Schedule a model step
        self.simulator.schedule_event_now(self.step)
        self.simulator.schedule_event_relative(function=self.collect_uxsim_data, time_delta=(self.data_time+0.25) / 3600)  # Add 0.25 seconds to avoid collecting before uxsim being finished

    @property
    def uw_time(self):
        return (self.simulator.time - self.start_time) * 3600

    def step(self):
        # Print the current time
        print(f"Model step (sim time: {self.simulator.time:.3f}, uw time: {self.uw_time:.1f}).", end=" ")
        # A step is considerd once the step_time. Default is 1/12 hour (5 minutes).
        # Schedule the travel_time execution 1 timestep ahead. This way all agents have had a chance to add their trips.
        self.simulator.schedule_event_relative(function=self.exec_simulation_travel_times, time_delta=self.step_time)

        # Schedule next event
        self.simulator.schedule_event_relative(function=self.step, time_delta=self.step_time)

    def exec_simulation_travel_times(self):
        # Execute the simulation for a given duration
        self.uw.exec_simulation(duration_t=self.step_time * 3600)

        # show simulation
        # self.uw.analyzer.network(self.uw.TIME, detailed=0, network_font_size=0, figsize=(6, 6), left_handed=0, node_size=0.2)

    def collect_uxsim_data(self):
        area_names, areas = zip(*self.uw.node_area_dict.items())
        self.uxsim_data[round(self.uw_time)] = self.uw.analyzer.area_to_pandas(areas, area_names, t_seconds=round(self.data_time))

        print(f"Collected data at {round(self.uw_time)} seconds.")
        self.simulator.schedule_event_relative(function=self.collect_uxsim_data, time_delta=self.data_time / 3600)

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

# Print the mode shares by hour
for hour in range(model1.start_time, model1.end_time):
    total_trips_hour = sum(model1.trips_by_hour_by_mode[(hour, mode)] for mode in model1.available_modes)
    mode_shares_hour = {mode: model1.trips_by_hour_by_mode[(hour, mode)] / total_trips_hour for mode in model1.available_modes}
    print(f"Hour {hour}: Mode shares: {[f'{mode}: {share:.2%}' for mode, share in mode_shares_hour.items()]}")

print(f"{model1.successful_car_trips} of {model1.successful_car_trips + model1.failed_car_trips} car trips were successful.")

# Save uxsim_data to a file
import pickle
with open("uxsim_data.pkl", "wb") as f:
    pickle.dump(model1.uxsim_data, f)

# W.analyzer.print_simple_stats()
model1.uw.analyzer.basic_analysis()
print(f"\nSimple stats: {model1.uw.analyzer.print_simple_stats()}")


