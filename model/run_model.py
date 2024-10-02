# Imports
import os
import gc
import multiprocessing as mp
from itertools import product
from model import run_model

folder = "exp2/"
suffix = "exp_ff"


if __name__ == "__main__":
    # Define parameter ranges
    av_cost_factors = [1.0, 0.5, 0.25]
    av_vot_factors = [1.0, 0.5, 0.25]
    av_densities = [1.5, 1.0, 0.5, 0.333333]
    induced_demands = [1.0, 1.25, 1.5]

    # Generate all combinations of parameters
    param_combinations = list(product(av_cost_factors, av_vot_factors, av_densities, induced_demands))

    # Create a new dict for combinations to run
    combinations_to_run = {}

    # Remove the combinations that are already run
    for comb in param_combinations:
        av_cost_factor, av_vot_factor, av_density, induced_demand = comb
        suffix = f"av_cost_{av_cost_factor}_av_vot_{av_vot_factor}_av_density_{av_density}_induced_{induced_demand}"
        param_dict = {
            "av_cost_factor": av_cost_factor,
            "av_vot_factor": av_vot_factor,
            "av_density": av_density,
            "induced_demand": induced_demand,
        }

        # Check if the output files already exist
        journeys_file = f"../results/{folder}journeys_df_{suffix}.feather"
        uxsim_file = f"../results/{folder}uxsim_df_{suffix}.pkl"
        parked_file = f"../results/{folder}parked_dict_{suffix}.pkl"

        if os.path.exists(uxsim_file) and os.path.exists(journeys_file) and os.path.exists(parked_file):
            print(f"Skipping experiment with {suffix}.")
        else:
            # Add combinations that need to be run
            combinations_to_run[suffix] = param_dict

    # Set up multiprocessing
    num_cores = 4
    print(f"Running {len(combinations_to_run)} of {len(param_combinations)} experiments on {num_cores} cores.")

    # Run experiments in parallel
    with mp.Pool(processes=num_cores, maxtasksperchild=1) as pool:
        run_args = [(False, suffix, folder, params) for suffix, params in combinations_to_run.items()]
        pool.starmap(run_model, run_args)

    print("All experiments completed.")
