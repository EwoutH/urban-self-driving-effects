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

    def __init__(self, n_agents=5, step_time=1/12, start_time=6, end_time=22, simulator=None):
        super().__init__()
        # Set up simulator time
        self.simulator = simulator
        self.simulator.time = float(start_time)

        # Set up time variables
        self.step_time = step_time
        self.start_time = start_time
        self.end_time = end_time
        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
        self.pop_dict_pc4_city = {pc4: pop for pc4, pop in zip(gdf.index, gdf["aantal_inwoners"])}
        # Normalize the population weights
        weights = np.array(list(self.pop_dict_pc4_city.values())) / sum(self.pop_dict_pc4_city.values())

        # Sample n_agents locations from the dictionary, weighted by population
        locations = np.random.choice(list(self.pop_dict_pc4_city.keys()), n_agents, p=weights)

        for i in range(n_agents):
            self.agents.add(Traveler(i, self, locations[i], gdf["65x65 Nummer"][locations[i]]))

        # Request agents to 
        self.agents.do("generate_trip_times")
        print(f"Events scheduled for agents: {self.simulator.event_list}")
        # Schedule a model step
        self.simulator.schedule_event_now(self.step)

    def step(self):
        # Print the current time
        print(f"Model step (time: {self.simulator.time})")
        # A step is considerd once the step_time. Default is 1/12 hour (5 minutes).

        # For each agent, initialize times they want to create a trip
        # Add those to the discrete event scheduler to

        # Schedule next even
        self.simulator.schedule_event_relative(function=self.step, time_delta=self.step_time)


simulator1 = DEVSimulator()
model1 = UrbanModel(n_agents=5, simulator=simulator1)
simulator1.model = model1
print(f"Running the model from {model1.start_time} to {model1.end_time}")

simulator1.run_until(model1.end_time)
print(f"Model finished at {model1.simulator.time}")
