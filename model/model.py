# local imports
from agent import Traveler
from data import Data

# package imports
from mesa import Model
import numpy as np

data = Data()


class UrbanModel(Model):

    def __init__(self, n_agents=5):
        super().__init__()
        # Create a dictionary of locations pc4 locations and their populations from pop_gdf_nl_pc4 with in_city == True
        gdf = data.pop_gdf_nl_pc4[data.pop_gdf_nl_pc4["in_city"] == True]
        self.pop_dict_pc4_city = {pc4: pop for pc4, pop in zip(gdf.index, gdf["aantal_inwoners"])}
        # Normalize the population weights
        weights = np.array(list(self.pop_dict_pc4_city.values())) / sum(self.pop_dict_pc4_city.values())

        # Sample n_agents locations from the dictionary, weighted by population
        locations = np.random.choice(list(self.pop_dict_pc4_city.keys()), n_agents, p=weights)

        for i in range(n_agents):
            self.agents.add(Traveler(i, self, locations[i], gdf["65x65 Nummer"][locations[i]]))

    def step(self):
        pass
        # For each agent, initialize times they want to create a trip
        # Add those to the discrete event scheduler to

model1 = UrbanModel()
