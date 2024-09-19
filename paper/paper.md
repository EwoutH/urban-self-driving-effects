_Very WIP version of a possible paper_

# Introduction

The introduction of the automobile fundamentally transformed human transportation and urban development in the 20th century. While providing unprecedented mobility and economic opportunities, the widespread adoption of cars has also led to significant challenges in urban environments. These include traffic congestion, parking scarcity, air and noise pollution, and safety concerns for pedestrians and cyclists. As we progress into the 21st century, a new technological revolution is on the horizon: self-driving cars.

Self-driving cars, also known as autonomous vehicles (AVs), represent a potential paradigm shift in urban transportation. Unlike the gradual evolution of traditional automobiles, AVs promise to radically alter not just how we drive, but also patterns of vehicle ownership and use. The transition from private ownership to a Mobility-as-a-Service (MaaS) model, where self-driving "robotaxis" become the dominant form of motorized road transport, could reshape our cities in profound ways.

Proponents of AVs highlight numerous potential benefits. For individual travelers, the ability to engage in other activities while in transit could significantly alter the perceived cost of travel time. From an urban planning perspective, the promise of solving pervasive parking problems is particularly appealing, as AVs could simply move on to their next passenger instead of occupying valuable urban space. Furthermore, optimized routing and platooning capabilities could increase road network efficiency and potentially improve safety.

However, the introduction of AVs also raises important questions and potential concerns. While each individual AV might offer improvements over traditional cars in terms of efficiency and environmental impact, the aggregate effect on urban systems remains uncertain. Historical precedent suggests that improvements in transportation technology often lead to induced demand, resulting in more total distance traveled. This raises a critical question: Will the increased efficiency of self-driving cars outweigh the induced demand they generate?

The complexity of this question stems from the multifaceted nature of urban transportation systems. Changes in one aspect, such as the introduction of AVs, can have cascading effects on traffic patterns, land use, public transit usage, and even residential and commercial development. Moreover, the rate and pattern of AV adoption are likely to vary across different urban contexts and demographic groups, further complicating predictions of system-wide impacts.

This thesis aims to address these uncertainties by developing an agent-based model (ABM) to simulate the introduction and adoption of self-driving cars in urban environments. By modeling individual decision-making processes and their collective outcomes, we seek to understand the emergent properties of a transportation system in transition. Our primary research question is:

*Which undesired urban problems will the introduction of self-driving cars cause, considering the modal shift and induced demand, and what policies can effectively mitigate undesired impacts?*

To answer this overarching question, we will explore several key sub-questions:

1. How can a traffic and mode choice model represent the system that shows the tradeoffs and potentially undesired effects of self-driving cars?
2. How will self-driving cars be adopted under different future uncertainties?
3. Which potential undesired system effects are amplified and which are reduced by the introduction of self-driving cars?
4. Which potential policies are most effective in minimizing which undesired system effects while maintaining benefits under different uncertainties?

By addressing these questions, this research aims to provide valuable insights for urban planners, policymakers, and transportation engineers as they prepare for the advent of self-driving cars. Understanding the potential system-wide effects of AVs is crucial for developing proactive strategies to maximize their benefits while mitigating unintended negative consequences in our urban environments.

# Method

## Model Description

The model description follows the ODD (Overview, Design concepts, Details) protocol (Grimm et al., 2006, 2020). This protocol provides a standardized format for describing agent-based models, ensuring clarity and reproducibility.

### 1. Purpose

The purpose of this model is to simulate the introduction and adoption of self-driving cars (autonomous vehicles, AVs) in urban environments, specifically focusing on the Rotterdam area in the Netherlands. The model aims to explore the system-level effects of AVs on urban transportation, including changes in mode choice, traffic patterns, and potential unintended consequences. By simulating individual agent behaviors and their collective outcomes, the model seeks to answer the following key questions:

1. How does the introduction of self-driving cars affect mode choice and travel patterns in urban areas?
2. What are the potential undesired effects of self-driving cars on urban transportation systems?
3. How do different policies influence the adoption and impact of self-driving cars?

The model is designed to provide insights for urban planners, policymakers, and transportation engineers to support decision-making in preparation for the widespread adoption of autonomous vehicles.

### 2. Entities, State Variables, and Scales

#### 2.1 Entities

The model consists of the following main entities:

1. **Travelers (Agents)**: Represent individual residents of the urban area who make travel decisions.
2. **Urban Model**: Represents the overall simulation environment, including the transportation network and global variables.
3. **UXsim World**: Represents the traffic simulation environment, including road network and vehicle movements.

#### 2.2 State Variables

##### 2.2.1 Traveler (Agent) State Variables

- `unique_id`: Unique identifier for each agent
- `pc4`: 4-digit postal code of the agent's location
- `mrdh65`: MRDH (Metropoolregio Rotterdam Den Haag) region number
- `mrdh65_name`: Name of the MRDH region
- `has_car`: Boolean indicating whether the agent owns a car
- `has_license`: Boolean indicating whether the agent has a driver's license
- `has_bike`: Boolean indicating whether the agent has a bicycle (default is True)
- `available_modes`: List of available transportation modes
- `currently_available_modes`: List of currently available transportation modes
- `vot_factor`: Value of time factor (lognormally distributed)
- `value_of_time`: Dictionary of value of time for different modes
- `current_location`: Current location (postal code) of the agent
- `current_vehicle`: Current vehicle being used by the agent
- `traveling`: Boolean indicating whether the agent is currently traveling
- `reschedules`: Number of times the agent has rescheduled trips
- `journeys_finished`: Number of completed journeys
- `costs`: Total costs incurred by the agent
- `time_costs`: Total time costs incurred by the agent
- `trip_times`: List of scheduled trip times
- `destinations`: List of trip destinations
- `journeys`: List of Journey objects representing completed and ongoing trips

##### 2.2.2 Urban Model State Variables

- `step_time`: Time step of the simulation (in hours)
- `start_time`: Start time of the simulation (in hours)
- `end_time`: End time of the simulation (in hours)
- `choice_model`: Type of mode choice model used
- `available_modes`: List of available transportation modes
- `transit_price_per_km`: Price per kilometer for public transit
- `car_price_per_km_variable`: Variable cost per kilometer for cars
- `car_price_per_km_total`: Total cost per kilometer for cars
- `av_initial_costs`: Initial costs for using an autonomous vehicle
- `av_costs_per_km`: Cost per kilometer for autonomous vehicles
- `av_costs_per_sec`: Cost per second for autonomous vehicles
- `av_vot_factor`: Value of time factor for autonomous vehicles
- `default_value_of_times`: Default values of time for different modes
- `pop_dict_pc4_city`: Dictionary of population by postal code
- `areas`: List of unique MRDH regions in the simulation
- `pc4s`: List of unique postal codes in the simulation
- `trips_by_hour_chance`: Dictionary of trip probabilities by hour
- `trips_by_mode`: Dictionary tracking the number of trips by mode
- `trips_by_hour_by_mode`: Nested dictionary tracking trips by hour and mode
- `uxsim_data`: Dictionary storing UXsim simulation data
- `parked_per_area`: Dictionary tracking parked vehicles by area
- `parked_dict`: Dictionary tracking parked vehicles over time
- `successful_car_trips`: Counter for successful car trips
- `failed_car_trips`: Counter for failed car trips

##### 2.2.3 UXsim World State Variables

- `name`: Name of the simulation
- `deltan`: Platoon size (number of vehicles per platoon)
- `reaction_time`: Reaction time of vehicles
- `duo_update_time`: Time interval for dynamic user equilibrium updates
- `duo_update_weight`: Weight for dynamic user equilibrium updates
- `duo_noise`: Noise factor for route choice
- `eular_dt`: Time step for Eulerian traffic state computation
- `eular_dx`: Spatial step for Eulerian traffic state computation
- `random_seed`: Seed for random number generation
- `tmax`: Total simulation duration
- `node_pc4_dict`: Dictionary mapping postal codes to network nodes
- `node_mrdh65_dict`: Dictionary mapping MRDH regions to network nodes

#### 2.3 Scales

- **Spatial scale**: The model covers the Rotterdam urban area, represented by 125 4-digit postal code (PC4) regions within 21 MRDH (Metropoolregio Rotterdam Den Haag) areas.
- **Temporal scale**: The simulation runs from 6:00 to 22:00 (16 hours) with a default step time of 5 minutes (1/12 hour).
- **Population scale**: The model simulates approximately 100,000 agents, representing about 1/10 of the actual population (991,575) of the area.

### 3. Process Overview and Scheduling

The model follows a discrete event simulation approach, with the following main processes:

1. **Initialization**: 
   - Set up the simulation environment
   - Create agents and assign them to locations
   - Initialize the road network and traffic simulation (UXsim)

2. **Generate trip times**: 
   - Each agent generates a set of trip times based on hourly probabilities
   - Destinations are assigned for each trip

3. **Start journey**:
   - Determine available modes for the journey
   - Choose origin and destination nodes (for car and AV trips)
   - Select travel mode using the specified choice model
   - Schedule the trip in the traffic simulation (for car and AV trips)

4. **Execute simulation step**:
   - Update the traffic simulation (UXsim)
   - Collect data on traffic conditions and parking

5. **Finish journey**:
   - Update agent's location and available modes
   - Schedule the next journey if available

6. **Data collection and analysis**:
   - Collect data on mode choices, travel times, and system-level metrics
   - Analyze and visualize results

The simulation uses a combination of time-step and event-based scheduling. The Urban Model steps forward in discrete time intervals (default 5 minutes), while individual agent actions and vehicle movements are scheduled as events.

### 4. Design Concepts

#### 4.1 Basic Principles

The model is based on several key principles and theories from transportation modeling and urban systems:

1. **Mode choice theory**: The model implements a rational choice framework for mode selection, based on the concept of utility maximization (Ben-Akiva and Lerman, 1985). Agents choose their travel mode by comparing the perceived costs (including both monetary and time costs) of available options.

2. **Traffic flow theory**: The UXsim component of the model is based on kinematic wave theory and car-following models, specifically using a mesoscopic version of Newell's simplified car-following model (Newell, 2002).

3. **Induced demand**: The model incorporates the concept of induced demand, which suggests that improvements in transportation systems can lead to increased travel (Downs, 1962; Cervero, 2003).

4. **Value of Time (VOT)**: The model uses the concept of Value of Time from transportation economics to represent how agents trade off time and money in their travel decisions (Small, 2012).

5. **Dynamic User Equilibrium (DUE)**: The traffic simulation component uses a DUE approach to model route choice, reflecting the idea that travelers adjust their routes based on experienced travel times (Wardrop, 1952).

#### 4.2 Emergence

The model is designed to reveal emergent phenomena at the system level, including:

- Modal shift patterns as a result of individual mode choices
- Traffic congestion patterns emerging from individual trip decisions and route choices
- Parking demand distribution across the urban area
- Potential unintended consequences of AV adoption, such as increased total vehicle kilometers traveled

#### 4.3 Adaptation

Agents in the model adapt their behavior in several ways:

- Mode choice: Agents select their travel mode based on the perceived costs and available options for each trip.
- Route choice: For car and AV trips, routes are dynamically updated based on traffic conditions (implemented in the UXsim component).
- Trip chaining: Agents adapt their available modes based on their previous trips, reflecting constraints such as needing to return home with the same mode they left with.

#### 4.4 Objectives

Agents in the model aim to minimize their perceived travel costs, which include both monetary costs and time costs weighted by their individual Value of Time. This objective is expressed in the `choice_rational_vot` method of the `Traveler` class.

#### 4.5 Learning

The current model does not implement explicit learning mechanisms for individual agents. However, the Dynamic User Equilibrium approach in the traffic simulation component represents a form of collective learning, where the system as a whole adapts to changing conditions.

#### 4.6 Prediction

Agents make implicit predictions about travel times and costs when choosing their mode of transport. These predictions are based on current information about the transportation network and their personal experiences (represented by their Value of Time and other parameters).

#### 4.7 Sensing

Agents are assumed to have perfect information about:
- Their own attributes (e.g., car ownership, driver's license)
- Available transportation modes
- Travel times and costs for different modes

The model does not currently implement limitations on sensing or information availability, which could be an area for future refinement.

#### 4.8 Interaction

Agents interact indirectly through their impact on the transportation system:
- Car and AV trips contribute to traffic congestion, affecting travel times for other agents
- Vehicle parking affects the availability of parking spaces in different areas

Direct agent-to-agent interactions are not currently modeled.

#### 4.9 Stochasticity

The model incorporates stochasticity in several ways:

- Trip generation: The number and timing of trips for each agent are determined probabilistically based on hourly trip probabilities.
- Value of Time: Each agent's Value of Time factor is drawn from a lognormal distribution.
- Initial conditions: Agent attributes like car ownership and possession of a driver's license are assigned probabilistically based on data for each postal code area.
- Traffic simulation: The UXsim component includes stochastic elements in route choice and traffic flow.

#### 4.10 Collectives

The model does not explicitly represent collectives or agent groups. However, agents are implicitly grouped by their postal code and MRDH region, which influences their trip patterns and available transportation options.

#### 4.11 Observation

The model collects and outputs various data for analysis:

- Mode choice distribution
- Trips by mode and time of day
- Traffic conditions (from UXsim)
- Parking demand by area
- Journey details for each completed trip

This data is saved in various formats (Python pickle files, CSV) for further analysis and visualization.

### 5. Initialization

The model is initialized with the following steps:

1. Set up the simulation environment with specified parameters (e.g., number of agents, start and end times, time step).
2. Load geographical and population data for the Rotterdam area.
3. Create agents and assign them to postal code areas based on population distribution.
4. Assign car ownership and driver's licenses to agents based on data for each postal code.
5. Generate trip schedules for each agent.
6. Initialize the UXsim traffic simulation component with the road network data.

The initial state can vary between simulation runs due to the stochastic elements in agent creation and trip generation.

### 6. Input Data

The model uses several external data sources:

1. Population data by postal code (PC4) and MRDH region
2. Car ownership and driver's license data by postal code
3. Road network data from OpenStreetMap
4. Travel time and distance data for public transit and cycling (from Google Maps API)
5. Trip generation probabilities by hour (derived from ODiN 2023 data)
6. Origin-destination matrices for the Rotterdam area

These data are preprocessed and stored in various formats (CSV, pickle files, GraphML) for use in the simulation.

### 7. Submodels

#### 7.1 Trip Generation

Trips are generated for each agent using the following process:

1. For each hour in the simulation period, generate a trip with probability given by `trips_by_hour_chance`.
2. Ensure an even number of trips by potentially adding or removing a trip.
3. Assign destinations based on origin-destination probability matrices.
4. Schedule the trips as events in the simulation.

#### 7.2 Mode Choice

The mode choice model is implemented in the `choice_rational_vot` method of the `Traveler` class. It calculates the perceived cost for each available mode:

```python
perceived_cost = monetary_cost + travel_time * value_of_time[mode]
```

The mode with the lowest perceived cost is chosen.

#### 7.3 Traffic Simulation

Traffic is simulated using the UXsim library, which implements a mesoscopic traffic model based on Newell's car-following model. Key components include:

- Dynamic User Equilibrium (DUE) for route choice
- Platoon-based vehicle representation
- Link-based traffic flow calculations

#### 7.4 Parking

Parking is modeled by tracking the number of parked vehicles in each MRDH region. When a car trip starts, a parking space is freed in the origin area. When a car trip ends, a parking space is occupied in the destination area.

#### 7.5 Cost Calculation

Travel costs are calculated differently for each mode:

- Car: Distance-based cost using `car_price_per_km_variable`
- AV: Initial cost plus distance and time-based costs
- Bike: Assumed to be zero
- Transit: Distance-based cost with a non-linear pricing scheme

#### 7.6 Value of Time

Each agent's Value of Time is calculated as:

```python
vot_factor = min(np.random.lognormal(mean=-0.1116, sigma=0.4724), 4)
value_of_time = {mode: default_vot[mode] * vot_factor for mode in modes}
```

This creates heterogeneity in how agents value their time, influencing their mode choices.
