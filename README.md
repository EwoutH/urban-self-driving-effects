This repository contains the code and data for a thesis project examining the systemic effects of autonomous vehicles on urban mobility patterns, with a case study focusing on Rotterdam.

Full paper: [`paper/paper.md`](paper/paper.md)

## Abstract

**Background:** The introduction of autonomous vehicles (AVs) represents a potential paradigm shift in urban transportation, but their system-level impacts remain uncertain. While AVs promise benefits like reduced parking demand and improved safety, questions persist about their effects on congestion, mode choice, and overall urban mobility patterns.

**Objective:** This research investigates how the introduction of self-driving cars will affect urban transportation systems, focusing on which undesired effects might emerge and what policies could effectively mitigate them while preserving benefits.

**Methods:** An agent-based model combined with mesoscopic traffic simulation was developed to simulate AV adoption in Rotterdam. The model integrates empirical data on travel patterns, road networks, and mode choice behavior. A full-factorial analysis explored 144 scenarios examining four key uncertainties: AV costs, perceived value of time, space efficiency, and induced demand. Additionally, 72 policy combinations were tested to evaluate intervention effectiveness.

**Results:** AV adoption is primarily driven by cost, with significant uptake occurring only when costs fall below 50% of current levels. Space efficiency emerges as the critical factor determining system outcomes: inefficient AVs (density factors ≥1.0) lead to severe congestion, while efficient AVs (density factors ≤0.5) can maintain or improve traffic flow even at high adoption rates. Notably, cyclists and transit users are more likely to switch to AVs than car users, potentially undermining sustainable transport goals. Traditional policy interventions show limited effectiveness, with no single approach consistently improving system performance across different scenarios.

**Implications:** Traditional policy interventions show limited effectiveness across different scenarios, suggesting that cities need to develop proactive, adaptive policy frameworks to manage AV adoption, focusing on space efficiency requirements, shared use and integration with existing sustainable mobility options rather than simple restrictions or pricing mechanisms.

## Repository structure
### Core components
- [`model/`](model/) - Core simulation code
  - [`model.py`](model/model.py) - Main model implementation ([documentation](paper/paper.md#3-model-description))
  - [`agent.py`](model/agent.py) - Agent behavior and decision making ([documentation](paper/paper.md#32-key-submodels))
  - [`data.py`](model/data.py) - Data loading and preprocessing ([documentation](paper/paper.md#6-input-data))
  - [`traffic.py`](model/traffic.py) - Traffic simulation integration using [UXsim](https://arxiv.org/abs/2309.17114)
  - [`run_model.py`](model/run_model.py) - Experiment execution scripts ([experimental setup](paper/paper.md#4-experimental-design))
  - [`scenarios_policies.py`](model/scenarios_policies.py) - Scenarios and policies used ([appendix D](paper/paper.md#appendix-d-experimental-setup)

### Data
- `data/` - Input data files ([full documentation](paper/paper.md#6-input-data))
  - Population data (`population_data_pc4_*.pkl`) - from [CBS](https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode)
  - Travel time matrices (`travel_time_distance_google_*.pkl`) - from [Google Maps API](https://developers.google.com/maps/documentation/distance-matrix)
  - Trip generation probabilities (`trips_by_hour_chances.pickle`) - from [ODiN 2023](https://www.cbs.nl/nl-nl/longread/rapportages/2024/onderweg-in-nederland--odin---2023-onderzoeksbeschrijving)
  - Origin-destination matrices (`od_chance_dicts_periods.pickle`) - from [V-MRDH model](https://www.mrdh.nl/verkeersmodel)
  - Network data (`polygons.pkl`) - derived from [OpenStreetMap](https://www.openstreetmap.org/)
  - Vehicle ownership data (`rijbewijzen_personenautos.pkl`) - from [CBS mobility data](https://www.cbs.nl/nl-nl/maatwerk/2023/35/auto-s-kilometers-en-rijbewijzen-per-pc4)

### Network data
- [`network/graphs/`](network/graphs/) - Road network files
  - `merged_network.graphml` - Combined Rotterdam road network ([documentation](paper/paper.md#63-road-network-data))
- [`network/create_network.ipynb`](network/create_network.ipynb) - Network processing notebook

### Results and analysis
- `results/` - Simulation outputs 
  - Various subfolders for different experiments ([results analysis](paper/paper.md#5-results))
- [`img/`](img/) - Generated plots and visualizations
  - [`default/`](img/default/) - Base scenario results
  - [`exp4/`](img/exp4/) - Scenario analysis results
  - [`sce_pol/`](img/sce_pol/) - Policy analysis results

### Supporting code
- [`prototyping/`](prototyping/) - Development notebooks
  - [`ODiN_analysis.ipynb`](prototyping/ODiN_analysis.ipynb) - Trip pattern analysis
  - [`pc4.ipynb`](prototyping/pc4.ipynb) - Population and car ownership analysis
- [`travel_api/`](travel_api/) - Travel time data collection
  - [`travel_time_distance_google.ipynb`](travel_api/travel_time_distance_google.ipynb) - Travel time collection and processing
- [`v_mrdh/`](v_mrdh/) - Origin-destination data processing
  - [`v_mrdh_od_demand.ipynb`](v_mrdh/v_mrdh_od_demand.ipynb) - OD matrix processing

### Analysis notebooks
- [`model/analysis_single_run.ipynb`](model/analysis_single_run.ipynb) - Single simulation run analysis
- [`model/analysis_ff.ipynb`](model/analysis_ff.ipynb) - Scenario and policy analysis

### Github actions
- [`.github/workflows/`](.github/workflows/) - CI configuration
  - Python environment setup
  - Model test run

See the full [model documentation](paper/paper.md#3-model-description) and [experimental setup](paper/paper.md#4-experimental-design) for detailed information about the implementation and experiments.

## Data Requirements
### Required Data Files
The model requires several data files to run. Key files include:

1. Network Data:
   - `network/graphs/merged_network.graphml`
2. Population and Geographic Data:
   - `data/population_data_pc4_65coded.pkl`
   - `data/areas_mrdh_weighted_centroids.pkl`
   - `data/polygons.pkl`
3. Travel Time Data:
   - `data/travel_time_distance_google_transit.pkl`
   - `data/travel_time_distance_google_bicycling.pkl`
   - PC4-level versions of above
4. Trip Pattern Data:
   - `data/trips_by_hour_chances.pickle`
   - `data/od_chance_dicts_periods.pickle`
   - `data/rijbewijzen_personenautos.pkl`

### Data Sources
- Population data: CBS (Dutch Central Bureau of Statistics)
- Road network: OpenStreetMap
- Travel times: Google Maps Distance Matrix API
- Trip patterns: ODiN 2023 (Dutch National Travel Survey)
- O-D matrices: V-MRDH transport model
