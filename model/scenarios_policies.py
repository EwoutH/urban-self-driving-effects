# Custom scenarios
av_vot_factor = 0.5

scenarios_without_vot = {
    "0_current": {
        "av_cost_factor": 1.0,
        "av_density": 1.5,
        "induced_demand": 1.0,
    },
    "1_moderate_progress": {
        "av_cost_factor": 0.5,
        "av_density": 1.0,
        "induced_demand": 1.125,
    },
    "2_extensive_progress": {
        "av_cost_factor": 0.25,
        "av_density": 0.5,
        "induced_demand": 1.25,
    },
    "3_extreme_progress": {
        "av_cost_factor": 0.125,
        "av_density": 0.333333,
        "induced_demand": 1.5,
    },
    "4_private_race_to_the_bottom": {
        "av_cost_factor": 0.125,
        "av_density": 1.5,
        "induced_demand": 1.25,
    },
    "5_shared_race_to_the_bottom": {
        "av_cost_factor": 0.125,
        "av_density": 0.5,
        "induced_demand": 1.25,
    },
    "6_dense_progress": {
        "av_cost_factor": 0.25,
        "av_density": 0.333333,
        "induced_demand": 1.125,
    },
}
# Add av_vot_factor to all scenarios
scenarios = {key: value | {"av_vot_factor": av_vot_factor} for key, value in scenarios_without_vot.items()}

policies = {
    "0_no_policy": {
        "policy_area": "city",
        "policy_speed_reduction": 0,
        "policy_tarif": 0,
        "policy_tarif_time": "day",
    },
    "1_autoluw_peak": {
        "policy_area": "autoluw",
        "policy_speed_reduction": 1,
        "policy_tarif": 5,
        "policy_tarif_time": "peak",
    },
    "2_autoluw_day": {
        "policy_area": "autoluw",
        "policy_speed_reduction": 1,
        "policy_tarif": 5,
        "policy_tarif_time": "day",
    },
    "3_city_peak": {
        "policy_area": "city",
        "policy_speed_reduction": 1,
        "policy_tarif": 5,
        "policy_tarif_time": "peak",
    },
    "4_city_day": {
        "policy_area": "city",
        "policy_speed_reduction": 1,
        "policy_tarif": 5,
        "policy_tarif_time": "day",
    },
    "5_city_speed_reduction": {
        "policy_area": "city",
        "policy_speed_reduction": 1,
        "policy_tarif": 0,
        "policy_tarif_time": "day",
    },
    "6_city_peak_tarif": {
        "policy_area": "city",
        "policy_speed_reduction": 0,
        "policy_tarif": 5,
        "policy_tarif_time": "peak",
    },
    "7_city_day_tarif": {
        "policy_area": "city",
        "policy_speed_reduction": 0,
        "policy_tarif": 5,
        "policy_tarif_time": "day",
    },
    "8_all_out": {
        "policy_area": "city",
        "policy_speed_reduction": 1,
        "policy_tarif": 10,
        "policy_tarif_time": "day",
    },
}

