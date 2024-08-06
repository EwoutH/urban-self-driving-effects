# local imports
from agent import Traveler
from data import Data

# package imports
from mesa import Model
from mesa.experimental.devs.simulator import DEVSimulator
import numpy as np
from datetime import datetime

data = Data()


class UrbanModel(Model):

    def __init__(self, n_agents=100, step_time=1/12, start_time=6, end_time=23, choice_model="random", simulator=None):
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

        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
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

        # Request agents to do stuff
        self.agents.do("generate_trip_times")
        print(f"Events scheduled for agents: {len(self.simulator.event_list)} (on average {len(self.simulator.event_list) / n_agents:.2f} per agent)")
        # Schedule a model step
        self.simulator.schedule_event_now(self.step)

    def step(self):
        # Print the current time
        print(f"Model step (time: {self.simulator.time:.3f})")
        # A step is considerd once the step_time. Default is 1/12 hour (5 minutes).

        # For each agent, initialize times they want to create a trip
        # Add those to the discrete event scheduler to

        # Schedule next even
        self.simulator.schedule_event_relative(function=self.step, time_delta=self.step_time)


simulator1 = DEVSimulator()
model1 = UrbanModel(simulator=simulator1)
simulator1.model = model1
print(f"Running the model from {model1.start_time} to {model1.end_time}")

simulator1.run_until(model1.end_time)
print(f"Model finished at {model1.simulator.time}")
