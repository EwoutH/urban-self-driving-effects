# local imports
from agent import Traveler
from data import data
from traffic import get_uxsim_world

# package imports
from mesa import Model
from mesa.experimental.devs.simulator import DEVSimulator
import numpy as np
import pandas as pd
from dataclasses import asdict
import pickle


data = data
real_population = 991575  # sum(self.pop_dict_pc4_city.values())


class UrbanModel(Model):
    def __init__(self, step_time=1/12, start_time=6, end_time=22, choice_model="rational_vot", enable_av=False, av_cost_factor=1, av_vot_factor=1, ext_vehicle_load=1, uxsim_platoon_size=25, simulator=None):
        super().__init__()
        n_agents = int(real_population / uxsim_platoon_size)
        print(f"### Initializing UrbanModel with {n_agents} agents, step time {step_time:.3f} hours, start time {start_time}, end time {end_time}, choice model {choice_model}, AV enabled {enable_av}, AV cost factor {av_cost_factor}, AV VOT factor {av_vot_factor}.")
        # Set up simulator time
        self.n_agents = n_agents
        self.simulator = simulator
        self.simulator.time = float(start_time)
        self.uxsim_platoon_size = uxsim_platoon_size

        # Set up time variables
        self.step_time = step_time
        self.start_time = start_time
        self.end_time = end_time

        # External vehicle load
        self.ext_vehicle_load = ext_vehicle_load

        # Set up the choice model
        self.choice_model = choice_model
        self.available_modes = ["car", "bike", "transit"]
        if enable_av:
            self.available_modes.append("av")

        # Set up the cost factors
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
        self.default_value_of_times = {mode: vot / 3600 for mode, vot in self.default_value_of_times.items()}  # Euros per second

        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
        gdf = gdf[gdf["aantal_inwoners"] > 100]  # Filter out insignificant areas (from 129 to 124)

        # select only the rows where the 65x65 Nummer is in the mrhd65 index
        gdf = gdf[gdf["65x65 Nummer"].isin(data.gdf_mrdh_65.index)]  # Rotterdam area.

        # Create a dictionary of pc4 locations and their populations
        self.pop_dict_pc4_city = {pc4: pop for pc4, pop in zip(gdf.index, gdf["aantal_inwoners"])}

        # SAVE THE pop_dict_pc4_city and gdf to a pickle file
        with open("../data/TEMP_pop_dict_pc4_city.pkl", "wb") as f:
            pickle.dump(self.pop_dict_pc4_city, f)
        gdf.to_pickle("../data/TEMP_gdf.pkl")

        # Normalize the population weights
        weights = np.array(list(self.pop_dict_pc4_city.values())) / sum(self.pop_dict_pc4_city.values())

        # Sample n_agents locations from the dictionary, weighted by population
        locations = np.random.choice(list(self.pop_dict_pc4_city.keys()), n_agents, p=weights)

        for i in range(n_agents):
            Traveler(self, pc4=locations[i], mrdh65=gdf["65x65 Nummer"][locations[i]])

        print(f"Default value of times: {self.default_value_of_times} (€/hour). Average vot factor: {self.agents.agg('vot_factor', np.mean):.4f}.")

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
        self.mrdh65s = list(set([a.mrdh65 for a in self.agents]))
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
        self.uw = get_uxsim_world(save_mode=False, show_mode=True, uxsim_platoon_size=self.uxsim_platoon_size)

        # External vehicle load
        # Get a list of origin and destination areas for the external trips
        def add_external_vehicle_load():
            print(f"Adding external vehicles to the simulation.")
            ext_vehicles = 0
            self.mrdh65s_ext = data.od_ext_into_city.index.to_list()

            # Convert to NumPy, int16
            self.od_ext_into_city = data.od_ext_into_city * self.ext_vehicle_load / self.uxsim_platoon_size
            self.od_ext_out_city = data.od_ext_out_city * self.ext_vehicle_load / self.uxsim_platoon_size

            for hour in range(self.start_time, self.end_time):

                # Calculate the start and end times for this hour
                sim_hour = hour - self.start_time
                start_time = sim_hour * 3600
                end_time = (sim_hour + 1) * 3600

                # Get the trip multiplier for this hour
                hour_multiplier = self.trips_by_hour_chance[hour]

                for ext_area in self.mrdh65s_ext:
                    for int_area in self.mrdh65s:
                        volume_in = round(self.od_ext_into_city[int_area][ext_area] * hour_multiplier)
                        volume_out = round(self.od_ext_out_city[ext_area][int_area] * hour_multiplier)

                        # print(f"Hour {hour}, ext {ext_area}, int {int_area}: in {volume_in}, out {volume_out}")

                        ext_nodes = self.uw.node_mrdh65_dict[ext_area]
                        int_nodes = self.uw.node_mrdh65_dict[int_area]

                        def add_vehicle_load(volume, orig_nodes, dest_nodes):
                            times = np.random.uniform(start_time, end_time, volume)
                            os, ds = self.random.choices(orig_nodes, k=volume), self.random.choices(dest_nodes, k=volume)
                            for time, o, d in zip(times, os, ds):
                                self.uw.addVehicle(orig=o, dest=d, departure_time=time)

                        if volume_in > 0:
                            add_vehicle_load(volume_in, ext_nodes, int_nodes)
                        if volume_out > 0:
                            add_vehicle_load(volume_out, int_nodes, ext_nodes)

                        ext_vehicles += volume_in + volume_out

            print(f"Added {ext_vehicles} external vehicles to the simulation.")

        if self.ext_vehicle_load:
            add_external_vehicle_load()

        # KPIs
        self.trips_by_mode = {mode: 0 for mode in self.available_modes}
        # Create nested dict
        self.trips_by_hour_by_mode = {(hour, mode): 0 for hour in range(start_time, end_time) for mode in self.available_modes}
        self.uxsim_data = {}

        self.parked_per_area = {area: 0 for area in self.mrdh65s}
        groups = self.agents.select(lambda a: a.has_car).groupby(by="mrdh65", result_type="list")
        parked = {area: len(group) for area, group in groups}
        self.parked_per_area.update(parked)
        self.parked_dict = {self.simulator.time: self.parked_per_area.copy()}
        print(f"Parked per area: {self.parked_per_area}")

        self.successful_car_trips, self.failed_car_trips = 0, 0

        # Request agents to do stuff
        self.agents.do("generate_trip_times")
        print(f"Events scheduled for agents: {len(self.simulator.event_list)} (on average {len(self.simulator.event_list) / n_agents:.3f} per agent)")
        print(f"Trips planned by agents: {(total_trip_times := sum(map(len, self.agents.get('trip_times'))))} (on average {total_trip_times / n_agents:.3f} per agent)")

        self.uw.finalize_scenario()

        self.car_travel_distance_array = np.array(self.uw.ROUTECHOICE.get_all_distances()) / 1000
        # Create a boolean mask for where the values are 'inf'
        inf_mask = np.isinf(self.car_travel_distance_array)
        # Transpose the matrix and replace the 'inf' values using the inverse values
        self.car_travel_distance_array[inf_mask] = self.car_travel_distance_array.T[inf_mask]

        # Schedule a model step
        self.simulator.schedule_event_now(self.step)

    @property
    def uw_time(self):
        return (self.simulator.time - self.start_time) * 3600

    def step(self):
        # Print the current time
        print(f"Model step (sim time: {self.simulator.time:.3f}, uw time: {self.uw_time:.1f}).", end=" ")
        # A step is considerd once the step_time. Default is 1/12 hour (5 minutes).
        # Schedule the travel_time execution 1 timestep ahead. This way all agents have had a chance to add their trips.
        self.simulator.schedule_event_relative(function=self.exec_simulation, time_delta=self.step_time)

        # Schedule next event
        self.simulator.schedule_event_relative(function=self.step, time_delta=self.step_time)

        self.parked_dict[self.simulator.time] = self.parked_per_area.copy()

    def exec_simulation(self):
        # Execute the simulation for a given duration
        self.uw.exec_simulation(duration_t=self.step_time * 3600)

        # show simulation
        # self.uw.analyzer.network(self.uw.TIME, detailed=0, network_font_size=0, figsize=(6, 6), left_handed=0, node_size=0.2)

# Create a simulator and model
simulator1 = DEVSimulator()
model1 = UrbanModel(simulator=simulator1)
simulator1.model = model1

print(f"### Running the model from {model1.start_time} to {model1.end_time}")
simulator1.run_until(model1.end_time)
print(f"### Model finished at {model1.simulator.time}")

### Journey data
# Create a flat list with all journeys from all agents. Each agent has a journeys list.
all_journeys = [journey for agent in model1.agents for journey in agent.journeys]

# In all_journeys, replace the agent with the agent unique_id, the o_node, d_node and vehicle with their names in each Journey class.
for journey in all_journeys:
    journey.agent = journey.agent.unique_id
    try:
        journey.o_node = journey.o_node.name
        journey.d_node = journey.d_node.name
    except AttributeError:
        pass  # In this case the o_node and d_node are already None
    if journey.vehicle:
        journey.vehicle = journey.vehicle.name

journeys_df = pd.DataFrame([asdict(journey) for journey in all_journeys])
journeys_df.to_pickle("results/journeys_df.pkl")

mode_counts = journeys_df['mode'].value_counts(normalize=True).to_dict()
print(f"Mode choice distribution: {({mode: f"{count:.2%}" for mode, count in mode_counts.items()})}")

mode_counts_weighted = journeys_df.groupby('mode')['distance'].sum() / journeys_df['distance'].sum()
print(f"Distance weighted mode choice distribution: {({mode: f"{count:.2%}" for mode, count in mode_counts_weighted.items()})}")


### UXsim data
area_names, areas = zip(*model1.uw.node_mrdh65_dict.items())
# link_cumulative_to_pandas
model1.uxsim_data = model1.uw.analyzer.area_to_pandas(areas, area_names, time_bin=900, set_index=True)
model1.uxsim_data.drop(columns="n_links", inplace=True)

# Save uxsim_data as pickle
with open("results/uxsim_df.pkl", "wb") as f:
    pickle.dump(model1.uxsim_data, f)

print(f"{model1.successful_car_trips} of {model1.successful_car_trips + model1.failed_car_trips} car trips were successful.")

# Save uxsim_data to a file
with open("results/parked_dict.pkl", "wb") as f:
    pickle.dump(model1.parked_dict, f)

# W.analyzer.print_simple_stats()
model1.uw.analyzer.basic_analysis()
print(f"\nSimple stats: {model1.uw.analyzer.print_simple_stats()}")
