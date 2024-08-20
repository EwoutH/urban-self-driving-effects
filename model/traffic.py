# ### Traffic simulation with OSMnx and UXsim
# - [OSMnx](https://www.github.com/gboeing/osmnx)
# - [UXsim](https://www.github.com/toruseo/uxsim)

from data import Data

from collections import defaultdict

import osmnx as ox
import uxsim

data1 = Data()

# print(f"UXsim version: {uxsim.__version__}")

def get_uxsim_world(save_mode=False, show_mode=False):
    city_name = "Rotterdam"
    surrounding_area_name = "South Holland"

    road_network = ox.load_graphml("../network/graphs/merged_network.graphml")

    # Print number of nodes and edges
    print(f"Number of nodes: {len(road_network.nodes)}\nNumber of edges: {len(road_network.edges)}")

    # ### UXsim model

    # Initialize the simulation environment (World)

    # Set simulation parameters
    simulation_name = "trafficsim"
    simulation_duration = (23-6)*3600  # in seconds (e.g., 3600 = 1 hour)
    platoon_size = 5  # vehicles per platoon
    reaction_time = 1  # in seconds
    duo_update_time = 150  # in seconds, for dynamic user equilibrium (DUO) route choice update
    duo_update_weight = 0.5  # weight for DUO update
    duo_noise = 0.01  # noise for DUO route choice to prevent identical choices
    eular_dt = 60  # in seconds, for Eulerian traffic state computation
    eular_dx = 50  # in meters, for Eulerian traffic state computation
    random_seed = 42  # for reproducibility

    # Create the World object with the specified parameters
    world = uxsim.World(name=simulation_name,
                        deltan=platoon_size,
                        reaction_time=reaction_time,
                        duo_update_time=duo_update_time,
                        duo_update_weight=duo_update_weight,
                        duo_noise=duo_noise,
                        eular_dt=eular_dt,
                        eular_dx=eular_dx,
                        random_seed=random_seed,
                        print_mode=1,  # Enable printing simulation progress
                        save_mode=save_mode,  # Enable saving simulation results
                        show_mode=show_mode,  # Enable showing results via matplotlib (for faster performance)
                        route_choice_principle="homogeneous_DUO",
                        show_progress=1,  # Show simulation progress
                        show_progress_deltat=300,  # Interval for showing progress, in seconds
                        tmax=simulation_duration)  # Total simulation duration


    # Helper function to determine max density based on road type and number of lanes
    def calculate_max_density(road_type, network_name):
        default_density = 0.15  # Default maximum density in vehicles per meter per lane
        if network_name == surrounding_area_name:
            return 5  # We don't care about the density in the surrounding area
        if road_type in ['motorway', 'trunk']:
            return 0.07  # Lower density due to higher speeds and longer headways
        elif road_type in ['primary', 'secondary']:
            return 0.10
        elif road_type in ['residential', 'tertiary']:
            return 0.20  # Higher density due to lower speeds
        else:
            return default_density  # Default for unspecified or other road types


    # Create Nodes in UXsim from OSMnx graph nodes
    for node_id, data in road_network.nodes(data=True):
        try:
            mrdh65 = data1.pc4_to_mrdh65[int(data['postcode'])]
        except KeyError:
            mrdh65 = 0
        world.addNode(name=str(node_id), x=data['x'], y=data['y'], attribute=mrdh65)

    world.node_area_dict = defaultdict(list)
    for node in world.NODES:
        world.node_area_dict[node.attribute].append(node)
    world.area_list = list(world.node_area_dict.keys())

    # Create Links in UXsim from OSMnx graph edges
    for u, v, data in road_network.edges(data=True):
        start_node_name = str(u)
        end_node_name = str(v)
        osmid = data['osmid']
        length = data['length']  # Assuming 'length' attribute exists
        # Assuming 'speed' attribute exists, convert speed from km/h to m/s
        speed_limit = data.get('speed', 30) * 1000 / 3600  # Default speed: 30 km/h
        # Calculate max density based on road type and lanes
        road_type = data.get('highway', '')
        network_name = data.get('network', '')
        max_density = calculate_max_density(road_type, network_name)
        priority = 1  # Example value
        # Get the lanes
        lanes = data.get('lanes', 1)
        # If lanes is a list, take the minimum value, and convert to int
        lanes = min(lanes) if isinstance(lanes, list) else lanes
        lanes = int(lanes)

        world.addLink(name=f"{u}_{v}_{osmid}", start_node=start_node_name, end_node=end_node_name, length=length,
                      free_flow_speed=speed_limit, jam_density=max_density, merge_priority=priority, number_of_lanes=lanes)

    # Assuming 'world' is your UXsim world and it has been populated with nodes and links as per previous steps
    nodes = {node.name: node for node in world.NODES}  # List of node names

    return world
