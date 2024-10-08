import os
import random
import multiprocessing as mp
from itertools import product
from model import run_model
from scenarios_policies import scenarios, policies

# Define output folder and suffix
folder = "sce_pol/"
suffix_base = "sce_pol"

if __name__ == "__main__":
    # Generate all combinations of scenarios and policies
    combinations = list(product(scenarios.keys(), policies.keys()))
    random.shuffle(combinations)

    # Filter out combinations that have already been run
    combinations_to_run = []
    for scenario_key, policy_key in combinations:
        suffix = f"{scenario_key}_{policy_key}_{suffix_base}"
        journeys_file = f"../results/{folder}journeys_df_{suffix}.feather"
        uxsim_file = f"../results/{folder}uxsim_df_{suffix}.pkl"
        parked_file = f"../results/{folder}parked_dict_{suffix}.pkl"

        if not all(os.path.exists(f) for f in [journeys_file, uxsim_file, parked_file]):
            combinations_to_run.append((scenario_key, policy_key))

    # Set up multiprocessing
    num_cores = 4
    print(f"Running {len(combinations_to_run)} of {len(combinations)} experiments on {num_cores} cores.")

    # Prepare arguments for run_model
    run_args = []
    for scenario_key, policy_key in combinations_to_run:
        params = scenarios[scenario_key].copy()
        params.update(policies[policy_key])
        suffix = f"{scenario_key}_{policy_key}_{suffix_base}"
        run_args.append((True, suffix, folder, params))

    # Run experiments in parallel
    with mp.Pool(processes=num_cores, maxtasksperchild=1) as pool:
        pool.starmap(run_model, run_args)

    print("All experiments completed.")
