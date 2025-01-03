from mesa import Agent

from data import data

import numpy as np
import random
from dataclasses import dataclass

# Import model for type hinting, to avoid circular imports

data = data

@dataclass
class Journey:
    agent: Agent = None
    origin: int = None
    destination: int = None
    mode: str = None
    start_time: float = None
    travel_time: float = None
    end_time: float = None
    distance: float = None
    cost: float = None
    perceived_cost: float = None
    comf_perceived_cost: float = None
    used_network: bool = False  # True for car and av
    available_modes: list = None
    perceived_cost_dict: dict = None
    started: bool = False
    finished: bool = False
    # All variables below are only for car and av
    act_travel_time: float = None
    act_perceived_cost: float = None
    o_node: object = None
    d_node: object = None
    vehicle: object = None

class Traveler(Agent):

    def __init__(self, model, pc4, mrdh65):
        super().__init__(model)
        self.has_car: bool = False
        self.has_license: bool = False
        self.has_bike = True
        self.available_modes = self.model.available_modes
        self.currently_available_modes = None
        # This results in a mean of 1 and standard dev = 0.5 in a lognormal distribution, capped at 4 to prevent wild stochastic swings.
        self.vot_factor = min(np.random.lognormal(mean=-0.1116, sigma=0.4724), 4)
        self.value_of_time = {mode: vot * self.vot_factor for mode, vot in self.model.default_value_of_times.items()}

        self.pc4: int = int(pc4)
        self.mrdh65: int = int(mrdh65)
        self.mrdh65_name: str = data.mrdh65_to_name[mrdh65]

        self.current_location = self.pc4
        self.current_vehicle = None
        self.traveling = False
        self.reschedules = 0
        self.journeys_finished = 0

        self.costs = 0
        self.time_costs = 0

        self.trip_times = []
        self.destinations = []
        self.journeys = []

        self.choose_mode = {
            "rational_vot": self.choice_rational_vot
        }[model.choice_model]

    def generate_trip_times(self):
        """Generate trip times and destinations for the agent

        Assumptions:
        - The agent has a random number of trips, with a chance for each hour of the day.
        - The agent will always return to the origin after each trip, meaning that the number of trips is always even.
        - There's no correlation between the times of the trips. All trips of an agent are independent.
        - No two trips can be in the same whole hour.
        On the large scale, all of those middle out."""

        for hour, chance in self.model.trips_by_hour_chance.items():
            # Generate a random number between 0 and 1
            if random.random() < chance:
                # If the random number is less than the chance, the trip is taken.
                self.trip_times.append(hour)

        # If len(trip_times) is odd, add a 50% chance of adding a trip. This makes the number of trips always even.
        if len(self.trip_times) % 2 == 1:
            if random.random() < 0.5 and len(self.trip_times) < (self.model.end_time - self.model.start_time):
                # Add a random weighted hour that's not already in the list
                trip_chances = {hour: chance for hour, chance in self.model.trips_by_hour_chance.items() if hour not in self.trip_times}
                # Choose a random hour
                hour = random.choices(population=list(trip_chances.keys()), weights=list(trip_chances.values()))[0]
                # Add the hour to the trip times
                self.trip_times.append(hour)
            else:
                # Remove a random trip time, weighted by the chances
                remove_chances = [self.model.trips_by_hour_chance[hour] for hour in self.trip_times]
                hour_to_remove = random.choices(population=self.trip_times, weights=remove_chances)[0]
                self.trip_times.remove(hour_to_remove)

        # Add random fraction of an hour to the trip times, to simulate the trip not starting exactly on the hour
        self.trip_times = [t + random.random() for t in self.trip_times]
        self.trip_times.sort()

        # For each trip time, assign a destination based on the origin-destination chance data for that time period
        mrdh65_destinations = []
        for trip_time in self.trip_times:
            od_chance_dict = self.time_to_od_dict(trip_time)
            pop, weights = zip(*od_chance_dict[self.mrdh65].items())
            mrdh65_destinations.append(random.choices(population=pop, weights=weights, k=1)[0])

        # Pick a random pc4 from the mrdh65 area, using data.mrdh65_to_pc4
        for destination in mrdh65_destinations:
            pc4_destinations = data.mrdh65_to_pc4[destination].copy()
            # If the mrdh65 destination is the same as the origin, remove the pc4 from the list. This allows traveling to the same mrdh65 (but different pc4).
            if destination == self.mrdh65:
                pc4_destinations.remove(self.pc4)
            self.destinations.append(random.choice(pc4_destinations))
        # Replace every second destination with the origin
        for i in range(1, len(self.destinations), 2):
            # TODO: Implement roundtrip chance. Then also check roundtrip consistency.
            # if i == len(self.destinations) - 1 or random.random() < self.model.roundtrip_chance:
            self.destinations[i] = self.pc4

        # Schedule events for the trip times (use self.model.simulator.schedule_event_absolute)
        # Schedule the first trip:
        if len(self.trip_times) > 0:
            first_journey = Journey(agent=self, destination=self.destinations[0])
            self.model.simulator.schedule_event_absolute(self.start_journey, self.trip_times[0], function_kwargs={"journey": first_journey})

        # print(f"Agent {self.unique_id} has {len(self.trip_times)} trips scheduled from {self.pc4} at times {[f"{t:.3f}" for t in self.trip_times]} to destinations {self.destinations}.")

    def start_journey(self, journey: Journey):
        self.journeys.append(journey)
        journey.started = True
        journey.origin = self.current_location
        journey.start_time = self.model.simulator.time
        journey.available_modes = self.currently_available_modes
        self.traveling = True

        if {"car", "av"} & set(journey.available_modes):
            self.choose_network_od_nodes(journey)

        self.choose_mode(journey)

        if journey.mode in ["car", "av"]:
            self.schedule_car_trip(journey)
            if journey.mode == "car":
                self.model.parked_per_area[data.pc4_to_mrdh65[self.current_location]] -= 1
        else:
            self.model.simulator.schedule_event_relative(self.finish_journey, journey.travel_time / 3600, function_kwargs={"journey": journey})

        # print(f"Agent {self.unique_id} at {self.pc4} performs a journey! Time = {self.model.simulator.time:.3f}, destination = {destination}, mode = {self.mode}")

        # Update the current location and available modes
    def finish_journey(self, journey: Journey):
        journey.end_time = self.model.simulator.time

        if journey.destination == self.pc4:
            self.currently_available_modes = self.available_modes
        else:
            match journey.mode:
                case "car":
                    self.currently_available_modes = ["car"]
                case "bike" | "transit" | "av":
                    self.currently_available_modes = [m for m in self.available_modes if m != "car"]
        self.current_location = journey.destination
        self.traveling = False
        self.journeys_finished += 1
        journey.finished = True

        if journey.mode == "car":
            self.model.parked_per_area[data.pc4_to_mrdh65[self.current_location]] += 1
            journey.act_perceived_cost = journey.cost + journey.act_travel_time * self.value_of_time[journey.mode]

        # schedule the next journey
        if self.journeys_finished < len(self.trip_times):
            next_journey = Journey(agent=self, destination=self.destinations[self.journeys_finished])
            start_time = max(self.model.simulator.time, self.trip_times[self.journeys_finished])
            self.model.simulator.schedule_event_absolute(self.start_journey, start_time,
                                                         function_kwargs={"journey": next_journey})

    def choice_rational_vot(self, journey: Journey):
        travel_times, costs, distances = {}, {}, {}
        perceived_costs = {}
        comf_perceived_costs = {}
        for mode in journey.available_modes:
            travel_time, cost, distance = self.get_travel_time_and_costs(journey, mode)
            travel_times[mode], costs[mode], distances[mode] = travel_time, cost, distance
            perceived_costs[mode] = cost + travel_time * self.value_of_time[mode]
            comf_perceived_costs[mode] = perceived_costs[mode] * self.model.comfort_factors[mode]

        chosen_mode = min(comf_perceived_costs, key=comf_perceived_costs.get)
        journey.mode = chosen_mode

        journey.travel_time = travel_times[chosen_mode]
        journey.cost = costs[chosen_mode]
        journey.distance = distances[chosen_mode]
        journey.perceived_cost = perceived_costs[chosen_mode]
        journey.comf_perceived_cost = comf_perceived_costs[chosen_mode]

        journey.perceived_cost_dict = perceived_costs

    def get_travel_time_and_costs(self, journey, mode):
        # Get the travel time and costs for a destination and mode
        match mode:
            case "car" | "av":
                # Get travel time from network, costs from distance conversion (fixed per km)
                o_id, d_id = journey.o_node.id, journey.d_node.id
                travel_time = self.model.uw.ROUTECHOICE.dist[o_id][d_id]
                distance = self.model.car_travel_distance_array[o_id][d_id]
                if mode == "car":
                    costs = distance * self.model.car_price_per_km_variable
                    travel_time = travel_time + 36  # 36 seconds for parking
                if mode == "av":
                    costs = self.model.av_initial_costs + distance * self.model.av_costs_per_km + travel_time * self.model.av_costs_per_sec
                    if (self.model.policy_tarif > 0 and int(journey.start_time) in self.model.policy_tarif_hours
                            and (journey.origin in self.model.policy_pc4s or journey.destination in self.model.policy_pc4s)):
                        costs += self.model.policy_tarif

            case "bike":
                # Get travel time from Google Maps API, costs are assumed to be zero
                travel_time = data.travel_time_pc4["bicycling"][(self.current_location, journey.destination)]
                distance = data.travel_distance_pc4["bicycling"][(self.current_location, journey.destination)]
                costs = 0

            case "transit":
                # Get travel time from Google Maps API, costs from distance conversion (NS staffel)
                travel_time = data.travel_time_pc4["transit"][(self.current_location, journey.destination)]
                distance = data.travel_distance_pc4["transit"][(self.current_location, journey.destination)]
                costs = self.calculate_transit_cost(distance, self.model.transit_price_per_km)

        # print(f"Agent {self.unique_id} at {origin} to {destination} by {mode} has travel time {travel_time:.3f}, costs {costs:.2f} and perceived costs {costs + travel_time * self.value_of_time:.2f}")
        return travel_time, costs, distance

    def choose_network_od_nodes(self, journey: Journey):
        attempts = 0
        max_attempts = 7

        while attempts < max_attempts:
            o_nodes = self.model.uw.node_pc4_dict[journey.origin]
            d_nodes = self.model.uw.node_pc4_dict[journey.destination]

            journey.o_node = self.model.uw.rng.choice(o_nodes)
            journey.d_node = self.model.uw.rng.choice(d_nodes)

            # Check if OD pairs are connected in both directions
            travel_time = self.model.uw.ROUTECHOICE.dist[journey.o_node.id][journey.d_node.id]
            travel_time2 = self.model.uw.ROUTECHOICE.dist[journey.d_node.id][journey.o_node.id]

            if travel_time <= 1e6 and travel_time2 <= 1e6:
                # Successful trip
                self.model.successful_car_trips += 1
                break  # Exit the loop as successful connection is found
            else:
                attempts += 1

        else:
            # If all attempts fail, adjust available modes and count failed trip
            journey.available_modes = [m for m in journey.available_modes if m not in ["car", "av"]]
            if len(journey.available_modes) == 0:
                print(f"Agent {self.unique_id} at {self.pc4} to {journey.destination} has no available modes left.")
                journey.available_modes = ["bike", "transit"]
            self.model.failed_car_trips += 1

    def calculate_transit_cost(self, distance, price_per_km, subscription=False):
        # Calculate the cost of a transit journey based on distance and price per km.
        # Define distance ranges and their corresponding price factors.
        # See https://www.treinonderweg.nl/wat-kost-de-trein.html
        ranges = [(40, 1), (80, .979), (100, .8702), (120, .7),
                  (150, .48), (200, .4), (250, .15), (float('inf'), 0)]

        cost = 0
        prev_limit = 0

        for limit, factor in ranges:
            if distance <= prev_limit:
                break
            km_in_range = min(distance, limit) - prev_limit
            cost += km_in_range * price_per_km * factor
            prev_limit = limit

        return cost

    def time_to_od_dict(self, time):
        if 7 <= time < 9:  # Morning rush hour (ochtendspits, 7-9)
            return data.od_chance_dicts_periods["os"]
        elif 16 <= time < 18:  # Evening rush hour (avondspits, 16-18)
            return data.od_chance_dicts_periods["as"]
        else:
            return data.od_chance_dicts_periods["rd"]

    def schedule_car_trip(self, journey: Journey):
        """"Schedule an event for the car trip with UXsim"""
        if journey.mode == "av" and self.model.av_density != 1.0:
            av_d = self.model.av_density

            # Case where density is smaller than 1
            if av_d < 1.0:
                # Chance that no trip gets scheduled
                if self.random.random() > av_d:
                    return

            # Case where density is larger than 1
            elif av_d > 1.0:
                if self.random.random() < (av_d - 1):
                    # Schedule an additional trip at the same time
                    self.model.uw.addVehicle(orig=journey.o_node, dest=journey.d_node, departure_time=self.model.uw_time)

        # In any case, schedule the regular trip
        journey.vehicle = self.model.uw.addVehicle(orig=journey.o_node, dest=journey.d_node, departure_time=self.model.uw_time)

        journey.used_network = True

        # Trigger the finish_journey function from the vehicle

        old_end_trip = journey.vehicle.end_trip

        def end_trip_with_event():
            old_end_trip()
            self.model.simulator.schedule_event_now(self.finish_journey, function_kwargs={"journey": journey})
            journey.act_travel_time = journey.vehicle.arrival_time - journey.vehicle.departure_time + 36  # 36 seconds for parking
            journey.vehicle = int(journey.vehicle.name)

        journey.vehicle.end_trip = end_trip_with_event
