<div align="center">
<h1>When do autonomous vehicles solve or exacerbate different urban mobility problems?</h1>
<h3>A simulation study exploring modal shifts and system-level impacts in dense urban environments</h3>
</div>

# Abstract
**Background:** The introduction of autonomous vehicles (AVs) could fundamentally transform urban transportation, but their system-level effects on cities remain poorly understood. Previous research has focused primarily on individual adoption decisions or specific impacts like congestion, without capturing the complex interactions between adoption patterns, modal shifts, and transportation system performance.

**Goal:** This study investigates how autonomous vehicles might affect urban mobility problems, considering both modal shifts and induced demand, and examines which policies could effectively mitigate potential negative impacts while preserving benefits.

**Methods:** An agent-based model combined with mesoscopic traffic simulation was developed to simulate travel behavior in Rotterdam, Netherlands. The model explores 144 scenarios varying AV costs, perceived time value, space efficiency, and induced demand. Eight representative scenarios were then tested against nine policy combinations.

**Results:** AV adoption patterns depend more strongly on space efficiency than cost or comfort advantages. A critical threshold around a density factor of 0.5 emerged - below this threshold, high AV adoption can maintain system performance, while above it, increased adoption degrades network performance. AVs compete more directly with sustainable transport modes than with private cars. Traditional policy interventions showed limited effectiveness across different scenarios.

**Conclusions:** Autonomous vehicles may represent neither an inherent solution nor an inevitable problem for urban mobility. Their impact appears likely to depend on the interaction between their operating characteristics, adoption patterns, and policy frameworks. Results suggest that cities should focus on ensuring space-efficient AV operations rather than just regulating costs or access.

Keywords: autonomous vehicles, urban mobility, agent-based modeling, traffic simulation, mode choice, transportation policy, modal shift, induced demand

# 1. Introduction
Autonomous vehicles could fundamentally alter urban transportation systems, yet predicting their system-level impacts remains a major modeling challenge. Unlike incremental improvements to existing modes, AVs simultaneously affect mode choice, network capacity, and travel demand through interconnected feedback loops. A growing body of simulation research has explored these impacts, but as a recent synthesis of 170 AV simulation studies reveals, critical gaps persist: most studies include only AV modes without modeling competition with conventional vehicles or public transit, few systematically explore parameter uncertainty, and policy recommendations remain fragmented and sometimes contradictory (Hardaway & Cai, 2026). The dominant finding across this literature – that AVs are likely to increase vehicle kilometers traveled unless actively managed – masks substantial variation in outcomes depending on modeling assumptions, particularly regarding operational efficiency and induced demand.

## 1.1 Challenges in modeling system-level AV impacts
Three interrelated technical challenges have limited previous attempts to capture AV impacts at the system level, spanning both behavioral representation and network modeling.

The first concerns modal competition. Most AV simulation studies focus on AV-only or AV-with-car scenarios (Hardaway & Cai, 2026), yet empirical evidence from ride-hailing services suggests that new mobility technologies may primarily attract users away from public transit rather than reducing private car use (Graehler et al., 2019). Hörl et al. (2021) demonstrated this dynamic through an agent-based simulation of a cost-covering autonomous taxi service in Zurich: despite clear benefits to individual users, the service produced largely negative system impacts, with driven distance increasing by up to 100% due to modal shifts from sustainable modes. Whether AVs would similarly draw from cycling, a dominant mode in many European cities, has received limited attention, partly because few studies have been conducted in contexts with high cycling mode shares. Modeling this competition requires a framework that endogenously represents mode choice across all major urban transport options, including non-motorized modes, while capturing how individual decisions aggregate into system-level effects.

The second challenge involves the representation of operational efficiency in traffic simulation. AV studies typically assume either that AVs operate as standard vehicles or that they achieve idealized efficiency through platooning or sharing, without systematically exploring intermediate cases or identifying critical performance thresholds. Yet the space each AV consumes per passenger transported, determined by vehicle size, occupancy, following distances, and empty repositioning, fundamentally shapes network-level outcomes. Liu et al. (2022) showed that shared AV fleet efficiency significantly influences vehicle miles traveled and parking demand, Yan et al. (2020) demonstrated that fleet performance varies substantially with trip density and operational constraints, and Tang et al. (2024) found that AVs generated an average of 8.8 km of additional zero-occupant travel per trip in a Hangzhou simulation. Dai et al. (2024) estimated total VKT increases of 10–25% across three Chinese cities under full AV adoption. These findings suggest that operational efficiency may matter more than commonly assumed, but the literature lacks a systematic framework for understanding how different efficiency levels produce qualitatively different system dynamics rather than merely shifting outcomes along a continuum.

The third challenge is capturing the feedback between adoption patterns and network performance within a single modeling framework. Agent-based models can represent heterogeneous decision-making but traditionally struggle with network-scale traffic dynamics, while traffic simulation models excel at network analysis but typically use simplified behavioral assumptions. Recent work has advanced integration of these approaches — Narayanan et al. (2022) combined dynamic user equilibrium with operational models for shared AV services, Fakhrmoosavi et al. (2022) proposed a stochastic framework for assessing network-level impacts of connected vehicles, and Wang et al. (2024) developed multimodal traffic assignment models considering heterogeneous demand. However, these studies have generally relied on static assignment methods or predetermined adoption scenarios rather than capturing how adoption patterns and network conditions co-evolve temporally. Li et al. (2025) developed an activity-based and agent-based co-simulation framework for the Rotterdam–The Hague metropolitan region that integrates ActivitySim with MATSim, demonstrating the potential for detailed behavioral modeling at regional scale, though their initial application focused on establishing the baseline framework rather than exploring technology scenarios.

## 1.2 Research gaps
These challenges interact in ways that existing approaches do not adequately capture. Hardaway & Cai (2026) found that whether a simulation includes induced demand fundamentally determines its policy conclusions: studies that model feedback loops consistently find AVs increase congestion and recommend restrictive policies, while those that omit such dynamics tend to predict efficiency gains. Similarly, studies simulating only peak hours tend to miss demand accumulation effects that emerge over a full day. Yet no study has systematically explored how the interaction between operational efficiency, cost, perceived travel time value, and induced demand creates different adoption trajectories and system outcomes, or tested whether commonly recommended policies like congestion pricing (the most frequently suggested intervention across the literature) remain effective across these different futures.

This gap is both substantive and methodological. On the substantive side, it remains unclear whether AV operating characteristics create gradual performance changes or sharp threshold effects, and how modal competition with sustainable modes varies across different adoption trajectories. On the methodological side, addressing these questions requires an integrated framework that combines behaviorally-rich individual decision-making with dynamic network simulation at sufficient scale for city-wide analysis, while remaining computationally tractable enough to explore a large scenario space.

## 1.3 Research contribution
This paper addresses these gaps through an integrated simulation framework combining agent-based modeling with mesoscopic traffic simulation, applied to Rotterdam, Netherlands. Building on Fakhrmoosavi et al.'s (2022) approach to handling parameter uncertainty, we systematically explore 144 scenarios through full-factorial variation of AV cost, perceived time value, space efficiency, and induced demand. Our framework extends Narayanan et al.'s (2022) integration of transport modeling approaches while adding explicit representation of operational efficiency thresholds identified as important by Yan et al. (2020) and Liu et al. (2022).

The study makes both methodological and substantive contributions. Methodologically, the framework integrates individual mode choice decisions with mesoscopic traffic simulation through a discrete event system, enabling analysis of temporal feedback between adoption and network performance at urban scale. Substantively, the framework is applied to address four research objectives:

1. Identify critical thresholds in AV operating characteristics, particularly space efficiency, that create qualitatively different system behaviors, by treating density as a continuous, outcome-based variable agnostic to specific technological implementations.
2. Quantify how different AV characteristics influence competition with all major urban transport modes, including cycling, within a city where sustainable modes hold dominant market shares – addressing the gap identified across most AV simulation studies, which omit non-motorized modes entirely.
3. Evaluate the robustness of commonly recommended policy interventions – congestion pricing, speed reductions, spatial restrictions – across multiple possible futures rather than optimizing for a single scenario.
4. Assess whether the interaction between AV characteristics and policy creates scenario-dependent effectiveness, where interventions beneficial in one future prove counterproductive in another.

Rotterdam provides a particularly informative case study for these questions. Its combination of high cycling mode share, extensive public transit, and significant car usage creates a multimodal context where AV competition with sustainable modes can be directly observed, a dynamic that studies in car-dependent cities, which dominate the current literature (Hardaway & Cai, 2026), cannot capture. Additionally, the city's size (approximately one million inhabitants) makes it large enough to exhibit complex mobility patterns while remaining computationally manageable for systematic scenario analysis.

## 1.4 Paper organization
The remainder of this paper is organized as follows. Section 2 describes the modeling framework, study area, data sources, validation, and experimental design. Section 3 presents results examining adoption patterns, network effects, and intervention effectiveness. Section 4 discusses implications for transportation system modeling and planning, while Section 5 concludes with key insights and future research directions.

# 2. Methods
This study employs an integrated simulation framework combining agent-based modeling (ABM) for individual travel decisions with mesoscopic traffic simulation for network dynamics, applied to the Rotterdam metropolitan area. The framework enables analysis of feedback loops between AV adoption patterns and transportation system performance at urban scale, while remaining computationally tractable for systematic exploration of 144 scenarios and 72 scenario-policy combinations. The model was developed following the Modeling & Simulation lifecycle (Law, 2014) and structured according to the ODD protocol (Grimm et al., 2020).

## 2.1 Modeling framework
The modeling approach consists of three interconnected layers. The first layer contains dynamic processes: the daily movements of travelers choosing transport modes and navigating through traffic, with continuous feedback between individual decisions and network conditions. The second layer includes experimental variables representing key uncertainties about AVs (cost, perceived time value, space efficiency, and induced demand) and potential policy interventions. These variables remain constant during each simulation but are systematically varied between simulations to explore different futures. The third layer provides validated baseline data — population distribution, road networks, and travel patterns — which remains constant across all scenarios to ensure meaningful comparisons.

The model builds upon the traditional four-step transportation demand model (McNally, 2007) but implements it within an agent-based, discrete-event framework using Mesa 3 (Ter Hoeven et al., 2025). The first two steps — trip generation and trip distribution — are derived from empirical data to ground the model in validated travel patterns. Trip generation rates come from the Dutch National Travel Survey (ODiN 2023), while trip distribution uses origin-destination matrices from the V-MRDH transport model. The latter two steps — mode choice and route assignment — are modeled dynamically through agent behavior and traffic simulation, enabling investigation of how travelers might respond to new mobility options.

![Conceptual-model-v2-no-exp.svg](img/Conceptual-model-v2-no-exp.svg)
_Fig. 2.1: Conceptual model displaying submodels, variables, and their interactions. Population data and trip patterns determine where and when agents travel; the road network provides infrastructure for traffic simulation. When agents choose car or AV modes, their trips feed into the mesoscopic simulation, which calculates congestion and travel times that feed back into subsequent mode choices. Non-motorized and transit travel times remain fixed._

The process creates two feedback loops: a direct loop where traffic conditions influence immediate mode choices through updated travel times, and an indirect loop where accumulated trips affect network performance over time. This generates emergent phenomena including congestion-based stabilization (negative feedback as congestion discourages further motorized travel), mode choice reinforcement through trip chaining (agents who choose car for an outbound trip must use it for the return), and tipping point behavior where interactions between heterogeneous value of time, density-dependent congestion, and mode-specific comfort factors create sharp transitions between system states.

## 2.2 Study area and data
Rotterdam, Netherlands was selected as representative of medium-sized European cities with diverse transport options and current mobility challenges. The study area encompasses approximately one million residents across 125 four-digit postal code (PC4) areas nested within 21 traffic analysis zones from the V-MRDH transport model. Rotterdam's combination of high cycling mode share, extensive public transit, and significant car usage creates a multimodal context where AV competition with sustainable modes can be directly observed. Its size makes it large enough to exhibit complex mobility patterns while remaining computationally manageable for systematic scenario analysis.

![rotterdam_mrdh65_pc4_areas.svg](img/rotterdam_mrdh65_pc4_areas.svg)
_Fig. 2.2: Study area divided into 21 MRDH regions and 125 postal code areas._

### Spatial and temporal structure
The 125 PC4 areas create 15,500 possible origin-destination pairs, ensuring highly heterogeneous travel options. The road network, derived from OpenStreetMap (September 2024), comprises 1,575 nodes and 3,328 edges. The inner-city network includes all roads from tertiary level upward, while a simplified surrounding network includes major roads only, balancing detail with computational efficiency. Planned infrastructure improvements (A16 motorway, Blankenburg tunnel) were included to represent near-future conditions.

![merged_network.svg](img/merged_network.svg)
_Fig. 2.3: Road network used in the traffic simulation, showing hierarchical road types._

Simulations run from 05:00 to 24:00 with 5-minute system time steps. The model uses discrete event simulation to activate agents with high temporal precision: individual agents initiate trips at any point in continuous time based on ODiN-derived hourly probabilities distributed uniformly within each hour. The traffic simulation operates at nested frequencies — vehicle platoons are updated every 10 seconds for position and speed, route choices are recomputed every 150 seconds through Dynamic User Equilibrium, and network metrics are collected at 15-minute intervals. The excluded overnight period accounts for less than 1% of daily trips.

### Data sources
Multiple empirical data sources were integrated to enable realistic simulation. Population distribution and vehicle ownership data from CBS (2023) were used at the PC4 level, with car ownership varying between 19% and 65% across areas (mean 31.5%). Each agent in the simulation represents a platoon of 10 actual travelers for computational efficiency, yielding approximately 100,000 agents for the 991,575 residents.

Origin-destination matrices from the V-MRDH 3.0 transport model (October 2023) provide spatial trip distribution for three time periods: morning peak (7:00–9:00), evening peak (16:00–18:00), and off-peak. These matrices were processed into probability distributions for trip destinations given each origin, aggregated across all transport modes, so that mode choice could be modeled endogenously as an agent decision. External traffic entering and leaving the study area was modeled separately using mode-specific matrices from V-MRDH, scaled by a calibrated load factor of 0.8 to account for imperfections in both the extracted road network and the traffic simulation. This factor was determined through calibration against observed traffic patterns and held constant across all experiments.

Travel times and costs for non-car modes were collected using the Google Maps Distance Matrix API for all 15,500 origin-destination pairs, captured on a typical Thursday morning (September 17, 2024, 08:00). For cars, travel times are calculated dynamically by the traffic simulation. Travel costs were derived from mode-specific sources: variable car costs of €0.268/km (Nibud, 2024), distance-based public transit pricing following the NS tariff structure (€0.169/km base rate with declining rates beyond 40 km), zero marginal cost for bicycles, and AV pricing based on a regression analysis of Waymo's September 2024 rates in Los Angeles (€3.79 base fare + €1.41/km + €0.40/min).

Value of time (VoT) parameters were derived from KiM (2023): €10.42/hour for cars, €10.39/hour for bicycles, and €7.12/hour for public transit. AV values are scaled from the car VoT using an adjustable factor explored in scenarios. Individual heterogeneity was introduced through agent-specific VoT multipliers drawn from a lognormal distribution (μ = −0.1116, σ = 0.4724, capped at 4.0), producing a population mean of 1.0 and standard deviation of 0.5. An agent's final VoT for each mode is the product of the mode's base value and their personal multiplier, creating realistic variation in mode preferences even among agents facing identical travel options.

## 2.3 Agent behavior model
Agents represent individual travelers with heterogeneous characteristics: home location (PC4 area), car ownership, driver's license possession, and personal VoT multiplier. Each agent generates trips based on empirically-derived hourly probabilities from ODiN 2023, with destinations drawn from V-MRDH origin-destination probability matrices that vary by time period. Trips are structured as two-leg chains (outbound and return), with mode availability constrained by previous choices — if an agent departs by car, the return trip must also be by car, as the vehicle must return home.

### Mode choice specification
Agents choose between available modes (conventional car, AV, bicycle, public transit) by minimizing comfort-adjusted perceived cost. The perceived cost $C_{p,m}$ for a trip using mode $m$ is:

$$C_{p,m} = (C_{m,m} + T_m \cdot V_m) \cdot \alpha_m$$

where $C_{m,m}$ is the monetary cost, $T_m$ is the travel time, $V_m$ is the agent's individual value of time for mode $m$, and $\alpha_m$ is a mode-specific comfort factor. The agent selects the mode with the lowest $C_{p,m}$. Comfort factors were set to $\alpha_{\text{car}} = 0.5$, $\alpha_{\text{bike}} = 1.33$, $\alpha_{\text{transit}} = 1.0$, and $\alpha_{\text{AV}} = 1.0$. These values reflect that car travel is generally perceived as more comfortable than alternatives (effective halving of perceived cost), while cycling carries a comfort penalty relative to motorized modes, consistent with revealed preference patterns in Dutch travel behavior. Transit and AVs are treated as neutral baselines.

This deterministic utility-minimization approach was chosen over random utility models (e.g., multinomial logit) for three reasons. First, the lack of stated preference data for AVs in the Rotterdam context made calibrating error terms and scale parameters speculative. Second, the research focus on system-level threshold behavior benefits from a framework where transitions between system states are not smoothed by random error — the deterministic formulation identifies tipping points more sharply, making it more conservative for threshold detection. Third, population-level stochasticity is already introduced through the heterogeneous VoT multipliers drawn from the lognormal distribution: agents with different VoT values make different mode choices for identical trips, producing realistic variation in aggregate mode shares without requiring an explicit error component. The combination of deterministic individual choice with heterogeneous preferences thus serves a similar function to random utility at the population level while providing cleaner identification of threshold behavior at the system level.

A limitation of this approach is that it does not capture habitual behavior, psychological factors, or complex preferences beyond the single comfort factor per mode. This likely produces sharper modal transitions than would occur in practice. However, for the research objective of identifying whether qualitatively different system states exist and under what conditions transitions occur, this sharpness is methodologically advantageous — it reveals thresholds that might be obscured by behavioral noise in more complex choice models.

### Mode availability and trip chaining
All agents are assumed to have bicycle access. Car availability depends on ownership and driver's license possession, assigned probabilistically at initialization based on PC4-level CBS data. When an agent uses a car for an outbound trip, only car is available for the return leg; when using bike, transit, or AV, car is excluded from the return trip options (as the car remains at home). This creates path dependency where initial mode choices constrain subsequent options, amplifying the impact of factors influencing initial choices.

## 2.4 Traffic simulation
The traffic simulation uses UXsim (Seo, 2025), a mesoscopic simulator implementing Newell's simplified car-following model, which represents traffic flow as a kinematic wave. This approach was selected as a middle ground: microscopic simulation would be computationally prohibitive at city scale for 144+ scenarios, while macroscopic models would miss intersection delays and route choice dynamics that affect system performance.

### Vehicle dynamics
When agents choose car or AV, they are added to the traffic simulation as vehicles grouped into platoons of 10. Each platoon's position on a link evolves as:

$$X(t + \Delta t, n) = \min\{X(t, n) + u\Delta t, \; X(t + \Delta t - \tau \Delta n, n - \Delta n) - \delta\Delta n\}$$

where $X(t,n)$ is the position of platoon $n$ at time $t$, $u$ is the link's free-flow speed, and $\delta$ is the jam spacing. Vehicles travel at free-flow speed when unconstrained and maintain safe following distances in congestion. Road characteristics are differentiated by type: motorways use jam densities of 0.14 vehicles/m/lane, scaling up to 0.20 for residential and tertiary roads.

Traffic at intersections is resolved by the incremental node model (Tampère et al., 2011), which processes vehicles sequentially based on merge priorities. Due to the absence of explicit intersection data in OpenStreetMap, default equal priorities were assigned to all incoming lanes — a simplification that may underestimate local bottleneck effects but is adequate for system-level analysis.

### Route choice
Route choice employs a Dynamic User Equilibrium (DUO) model. The attractiveness $B^{z,i}_o$ of link $o$ for vehicles with destination $z$ at time step $i$ is updated as:

$$B^{z,i}_o = (1 - \lambda)B^{z,i-\Delta i_B}_o + \lambda b^{z,i}_o$$

where $\lambda = 0.5$ is a weight parameter, $b^{z,i}_o$ indicates whether link $o$ is on the current shortest path to $z$, and routes are recomputed every 150 seconds (with noise parameter 0.01 to prevent identical route choices). This formulation allows vehicles to gradually adapt routes based on evolving conditions rather than responding instantaneously.

### AV density implementation
AV space efficiency is parameterized through a density factor representing the road space consumed per person transported, relative to conventional vehicles. Rather than modifying vehicle physics, density is implemented probabilistically at trip generation: for a density factor $d < 1.0$, each AV trip is added to the traffic simulation with probability $d$ (the remaining trips still occur but without network impact, representing higher occupancy or smaller vehicles that consume proportionally less capacity). For $d > 1.0$, each trip generates an additional vehicle with probability $d - 1$ (representing empty repositioning trips or increased safety margins). In all cases, the agent completes their journey — the mechanism affects only the network load per AV trip.

This implementation treats density as an outcome-based metric agnostic to specific technological implementations. A density factor of 0.5 could represent doubled average occupancy, halved following distances through platooning, smaller urban-optimized vehicles, or combinations thereof. By abstracting from implementation specifics, results remain relevant regardless of which efficiency mechanisms ultimately emerge.

### Feedback between components
The agent-based and traffic simulation components are synchronized at 5-minute intervals. When agents choose car or AV, their trips are injected into UXsim, which simulates traffic flow and updates network travel times. These updated times are then available to subsequent agents making mode choices, creating the feedback loop between individual decisions and system performance. For bicycle and transit, travel times remain fixed based on Google Maps data, as these modes are assumed to be largely unaffected by road traffic congestion.

Car trips include an additional 36 seconds of travel time representing parking search and walking time. Upon trip completion, vehicle arrival triggers a callback event that schedules the agent's journey completion in the discrete event system, ensuring precise temporal coordination between the two simulation components.

## 2.5 Model validation
The model was validated against ODiN 2023 data for the Rotterdam area and assessed for plausible network behavior. The objective was not absolute predictive accuracy but sufficient validity to meaningfully examine relative changes across scenarios.

### Mode share validation
In the inner city (Noord, Kralingen, Rotterdam Centrum, Feyenoord, Delfshaven), the model produces mode shares of 11.3% car, 82.3% bicycle, and 6.5% transit, compared to empirical values of 13.4%, 69.9%, and 16.7%. For the broader study area, the model shows 25.4% car, 65.1% bicycle, and 9.5% transit versus empirical values of 37.7%, 49.0%, and 13.3%.

The model systematically overestimates bicycle usage and underestimates car and transit use. This deviation is consistent with the model's omission of car-favoring factors not captured in the cost-time framework: weather conditions, cargo requirements, multi-stop trip chains, and habitual preferences. The comfort factor for cars ($\alpha = 0.5$) partially compensates for these factors but does not fully capture their effect.

For interpreting AV adoption results, this bias has directional implications. The overrepresentation of cyclists means the model contains a larger pool of agents who could potentially switch to AVs from cycling, which may overstate the magnitude of cycling-to-AV shifts. Conversely, the underrepresentation of car users means fewer agents are available for car-to-AV transitions, potentially understating this shift. However, the *relative ordering* — that cyclists switch earlier and faster than car users — is robust to this bias, as it emerges from the structural cost advantages AVs hold over cycling (weather independence, productive travel time, comfort) versus the smaller differential with car travel (similar comfort, offset by AV pricing). The finding that AVs compete more with sustainable modes than cars is therefore likely conservative for the car competition dimension but may overstate the absolute magnitude of cycling displacement.

### Travel pattern and network validation
Temporal patterns show strong alignment with empirical data: the model reproduces the sharp morning peak (8:00–9:00) and broader evening peak (16:00–18:00) observed in ODiN data. Trip distance distributions follow expected log-normal patterns, with bicycles dominating shorter trips (1–5 km) and motorized modes more prevalent at longer distances.

![mode_distribution_default.svg](img/default/mode_distribution_default.svg)
_Fig. 2.4: Mode distribution throughout the day in the default scenario (no AVs)._

![journeys_data_default.svg](img/default/journeys_data_default.svg)
_Fig. 2.5: Distributions of travel time, distance, monetary cost, and perceived cost by mode in the default scenario._

The traffic simulation demonstrates plausible behavior at known congestion points. The Algera bridge bottleneck in Krimpen aan den IJssel and the Terbregseplein interchange show appropriate congestion patterns. Network speeds average 25 km/h in the default scenario, decreasing to 10–15 km/h in congested inner-city areas during peak hours. The model captures expected asymmetry between morning and evening peaks: despite similar trip generation rates, the evening peak produces more severe congestion due to more dispersed destination patterns, locked-in mode choices and accumulated delay effects, the latter an emergent property.

![uxsim_heatmaps_default.png](img/default/uxsim_heatmaps_default.png)
_Fig. 2.6: Network performance metrics by geographic area during the day in the default scenario._

### Validation limitations
Several limitations inform result interpretation. Detailed validation of intersection-level dynamics was not possible due to computational constraints and data availability (commercial traffic data providers declined access requests). AV-related behavioral assumptions cannot be directly verified due to the technology's emerging nature. Non-car travel times are based on a single Thursday morning measurement, not capturing time-of-day variation in transit service frequency. Despite these limitations, the model's reproduction of key modal, temporal, and spatial patterns provides sufficient validity for examining relative changes across scenarios, while specific numerical predictions should be interpreted with appropriate caution.

## 2.6 Experimental design
Two complementary experiments were conducted: a scenario analysis exploring AV adoption under uncertainty, and a policy analysis testing interventions across representative futures.

![Conceptual-model-v2.svg](img/Conceptual-model-v2.svg)
_Fig. 2.7: Conceptual model including scenario uncertainties and policy levers._

### Scenario analysis
A full-factorial design was employed to systematically explore interactions between four key uncertainties, selected through literature review and stakeholder consultation as the factors most likely to produce distinct system-level dynamics:

1. **AV cost factor** (4 levels: 1.0, 0.5, 0.25, 0.125): Cost relative to current Waymo pricing. Logarithmic spacing reflects that cost differences matter more at lower price points where they may trigger adoption thresholds.
2. **AV value of time factor** (3 levels: 1.0, 0.5, 0.25): Perceived value of time in AVs relative to conventional cars. Lower values represent scenarios where productive use of travel time reduces its perceived cost.
3. **AV density factor** (4 levels: 1.5, 1.0, 0.5, 0.333): Space efficiency relative to conventional vehicles. Values above 1.0 indicate less efficient operation (safety margins, empty repositioning); below 1.0 represents improved efficiency (higher occupancy, platooning, smaller vehicles).
4. **Induced demand** (3 levels: 1.0, 1.25, 1.5): Multiplicative increase in trip generation rates, capturing both AV-induced demand and external growth factors. Range based on historical precedent from major transportation improvements.

This design created 144 unique scenarios (4 × 3 × 4 × 3), each simulated for a full day (05:00–24:00). The factorial approach was chosen over Monte Carlo or Latin Hypercube sampling for its interpretability: each scenario represents a clear parameter combination enabling direct comparison, and the logarithmic spacing of cost levels captures non-linear adoption responses.

### Policy analysis
Eight representative scenarios were selected to span the range of futures identified in the scenario analysis, from current conditions to extreme AV progress, including several "race to bottom" scenarios with cheap but variably efficient AVs (Table 2.1). All policy scenarios used a VoT factor of 0.5 to focus on cost and density interactions.

| Scenario | Cost factor | Density | Induced demand |
|----------|-------------|---------|----------------|
| Current situation | 1.0 | 1.5 | 1.0 |
| Moderate progress | 0.5 | 1.0 | 1.125 |
| Extensive progress | 0.25 | 0.5 | 1.25 |
| Extreme progress | 0.125 | 0.333 | 1.5 |
| Private race to bottom | 0.125 | 1.5 | 1.25 |
| Mixed race to bottom | 0.125 | 1.0 | 1.25 |
| Shared race to bottom | 0.125 | 0.5 | 1.25 |
| Dense progress | 0.25 | 0.333 | 1.125 |

_Table 2.1: Scenarios selected for policy analysis._

Nine policy combinations were tested, varying intervention type (speed reduction, congestion pricing, or both), spatial scope (Rotterdam's central "autoluw" low-traffic zone covering ~13% of the population, or city-wide), and temporal scope (peak hours 7:00–9:00 and 16:00–18:00, or daytime 6:00–19:00). Speed reductions of 20 km/h represent policies consistent with those being implemented in cities like Amsterdam (50→30 km/h). Pricing levels (€5 and €10 per AV trip) fall within ranges of existing congestion pricing schemes.

| Policy | Area | Speed reduction | Tariff (€) | Timing |
|--------|------|-----------------|------------|---------|
| No policy | - | None | 0 | - |
| Autoluw peak | Autoluw | −20 km/h | 5 | Peak |
| Autoluw day | Autoluw | −20 km/h | 5 | Day |
| City peak | City | −20 km/h | 5 | Peak |
| City day | City | −20 km/h | 5 | Day |
| City speed only | City | −20 km/h | 0 | - |
| City peak tariff | City | None | 5 | Peak |
| City day tariff | City | None | 5 | Day |
| All out | City | −20 km/h | 10 | Day |

_Table 2.2: Policy combinations tested._

This created 72 scenario-policy combinations (8 × 9). Each was evaluated using multiple metrics: mode shares, network speeds, delay ratios, total vehicle kilometers traveled, average travel times, and perceived costs, enabling analysis of both intended and unintended policy effects. Speed reductions were implemented by reducing the free-flow speed on all links within the policy area by 20 km/h (minimum 20 km/h), while congestion pricing was applied as a flat surcharge on AV trips with origin or destination within the policy area during the specified hours.

# 3. Results
This section presents findings from two complementary experiments: a full-factorial scenario analysis (144 scenarios) and a focused policy analysis (72 scenario-policy combinations). Section 3.1 examines AV adoption patterns and modal competition across the scenario space. Section 3.2 analyzes the resulting system-level effects on network performance, vehicle kilometers traveled, and travel times. Section 3.3 evaluates policy intervention effectiveness across representative scenarios. Section 3.4 synthesizes the key findings.

Results are displayed in dimensionally-stacked heatmaps where each tile represents one scenario. The axes are arranged as follows: inner x-axis shows AV value of time factor (1.0 to 0.25), outer x-axis shows AV cost factor (1.0 to 0.125), inner y-axis shows induced demand factor (1.0 to 1.5), and outer y-axis shows AV density factor (1.5 to 0.333). Green generally indicates outcomes preferred by stakeholders, red indicates undesired outcomes, and yellow marks the reference scenario without AVs. Where the preferred direction is ambiguous, a brown-to-blue scale is used with white as the reference.

## 3.1 AV adoption and modal competition
Figure 3.1 shows AV mode share and the mode shares of conventional cars, bicycles, and public transit across all 144 scenarios.

| ![heatmap_mode_share_av.png](img/exp4/heatmap_mode_share_av.png) | ![heatmap_mode_share_car.png](img/exp4/heatmap_mode_share_car.png) |
|-----|-----|
| ![heatmap_mode_share_bike.png](img/exp4/heatmap_mode_share_bike.png) | ![heatmap_mode_share_transit.png](img/exp4/heatmap_mode_share_transit.png) |

_Figure 3.1: Mode share of AVs, cars, bicycles, and public transit across 144 scenarios. Reference values without AVs: 29.8% car, 58.4% bicycle, 11.8% transit._

### Cost as the primary adoption driver
AV adoption is primarily driven by cost reductions rather than comfort or time perception improvements. At current pricing (cost factor 1.0), adoption remains marginal at 0.7–2.5% of trips regardless of other parameters. Halving costs increases adoption by roughly 5× to 4–12%, while a further halving to a cost factor of 0.25 produces another substantial increase, reaching up to 35% depending on density and value of time. At one-eighth of current costs (factor 0.125), adoption ranges widely from 7% to 84%, with density and value of time determining where within this range each scenario falls.

The value of time factor plays a secondary but important role, particularly in determining whether car users switch to AVs. At a cost factor of 0.125, reducing the VoT factor from 1.0 to 0.25 roughly doubles AV adoption in many scenarios, but only when density is also favorable. With inefficient AVs (density ≥ 1.0), low VoT alone cannot push adoption above approximately 24%. Finally, it's notable that the first halving of value-of-time has a larger effect than the second one, and high-AV adoption can be reached with one halvation in value of time.

### The density threshold in modal competition
The most striking pattern in Figure 3.1 is not in AV adoption itself but in how AVs compete with other modes, which differs qualitatively above and below a density factor of approximately 0.5.

With efficient AVs (density ≤ 0.5), adoption draws heavily from cycling and transit. Bicycle mode share, 58.4% in the reference scenario, drops below 10% in the most favorable AV scenarios (cost 0.125, density 0.333, VoT 0.25). Transit share follows a similar trajectory, falling from 11.8% to under 1%. Meanwhile, car share also declines substantially in these scenarios – reaching below 10% – as both cars and sustainable modes lose riders to AVs. The net effect is an AV-dominated system where the primary losers are cyclists and transit users.

With inefficient AVs (density ≥ 1.0), a fundamentally different dynamic emerges. As AVs become cheaper, cycling and transit shares erode more gradually, but car share declines steeply – falling to 1–3% in extreme cases at density 1.5 with cost factor 0.125. This occurs because inefficient AVs generate severe congestion (detailed in Section 3.2), which penalizes all road-based modes. Since car travel times increase while bicycle and transit times remain fixed in the model, congestion shifts travelers away from cars toward non-road modes. Transit share actually *increases* above the reference value in several of these scenarios, reaching 15–16% – a consequence of congestion making car travel less attractive relative to transit.

### Asymmetric competition with sustainable modes
Across both density regimes, a consistent asymmetry is visible: the modal shift from cycling and transit to AVs begins at higher cost levels and proceeds faster than the shift from cars. At a cost factor of 0.5 with density 0.333, cycling share has already fallen by approximately 10 percentage points while car share remains near the reference value. This asymmetry arises from the structural cost advantages AVs hold over cycling – weather independence, productive travel time, comfort – versus the smaller perceived differential with car travel, where similar comfort is offset by AV pricing.

This pattern has an important implication: there exists a range of AV cost levels (roughly 0.5–0.25) where AVs are cheap enough to attract cyclists and transit users but not yet cheap enough to displace significant car use. In this transitional range, AVs add vehicles to the network without removing many, because the riders they attract were previously not contributing to road traffic.

Induced demand shows minimal influence on mode shares compared to cost and density effects. While higher demand slightly reduces AV adoption in near-term scenarios (where the network is already congested), density becomes the dominant factor as costs decrease. The interaction between induced demand and system performance is explored further in Section 3.2.

## 3.2 System-level effects
The adoption patterns described above produce markedly different system-level outcomes depending on AV density. This section examines network performance, vehicle kilometers traveled, and travel times across the 144 scenarios.

### Network speed and congestion
Figure 3.2 shows average network speed and average delay (ratio of actual to free-flow travel time) across scenarios. The reference scenario without AVs produces an average network speed of 25.1 km/h and an average delay of 70.6% above free-flow times.

| ![heatmap_mean_network_speed.png](img/exp4/heatmap_mean_network_speed.png) | ![traffic_heatmap_average_delay_weighted.png](img/exp4/traffic_heatmap_average_delay_weighted.png) |
|-----|-----|

_Figure 3.2: Average network speed (km/h) and average delay relative to free-flow travel time across 144 scenarios. Reference: 25.1 km/h, 70.6% delay._

Even without AV adoption, induced demand alone substantially degrades performance: at 1.25× demand, average speeds drop to approximately 18 km/h; at 1.5× demand, to approximately 15 km/h. Cheaper AVs compound this degradation in all scenarios where density exceeds 0.5, as additional vehicles enter an already strained network.

The density threshold identified in Section 3.1 produces a sharp bifurcation in network outcomes. With density factors of 1.0 and 1.5, cheaper AVs systematically reduce network speeds. At cost factor 0.125 with density 1.0, speeds fall to 11–12 km/h; with density 1.5, they reach 7–12 km/h – representing near-gridlock conditions where vehicles move at roughly one-third of current average speeds. Delays in these scenarios exceed 300–450% of free-flow times, meaning trips take four to five times longer than uncongested travel would allow.

Below the threshold, the pattern reverses. At density 0.5, network speeds remain near reference levels (18–31 km/h) even with substantial AV adoption, suggesting that AVs at this efficiency contribute roughly as much capacity as they consume. At density 0.333, speeds increase substantially above the reference, reaching 33–38 km/h in the most favorable scenarios – a 30–50% improvement over current conditions. This occurs because highly efficient AVs effectively increase network capacity: each AV trip displaces approximately three conventional vehicle-equivalents worth of road space while serving the same number of travelers.

The interaction between density and other parameters is notably asymmetric. Above the threshold, neither cost reductions nor VoT improvements can compensate for inefficient space use – no scenario with density ≥ 1.0 achieves reference-level network speeds regardless of other parameter values. Below the threshold, however, cheaper and more comfortable AVs generally improve network performance by attracting riders away from less space-efficient conventional cars.

### Vehicle kilometers traveled
Figure 3.3 shows total network vehicle distance, measured in thousands of vehicle-kilometers, where each AV trip contributes distance weighted by its density factor. The reference scenario produces 644 thousand vkm.

<div align="center">
    <img src="img/exp4/heatmap_total_network_distance.png" width="60%">
</div>

_Figure 3.3: Total network vehicle distance (thousands of vkm) across 144 scenarios. Reference: 644 thousand vkm._

VKT exhibits a counterintuitive relationship with system performance. In scenarios with inefficient AVs (density ≥ 1.0) and low costs, total VKT *decreases* – sometimes dramatically, falling below 300 thousand vkm in the most congested scenarios. This is not because fewer trips are attempted but because gridlocked vehicles physically cannot cover distance: slow-moving traffic produces less VKT per unit time regardless of demand. This paradoxical outcome means that the worst-performing scenarios in terms of mobility also show the lowest VKT, while the metric might normally be interpreted as indicating reduced environmental impact.

Conversely, efficient AVs (density ≤ 0.5) enable substantially higher VKT. With density 0.333 and cost factor 0.25, VKT reaches 1,100–1,300 thousand vkm – roughly double the reference – and scales nearly linearly with induced demand at this efficiency level. The freed network capacity accommodates all additional travel demand, resulting in more vehicles traveling faster over longer distances. With density 0.5, VKT increases are more moderate but still substantial, reaching 900–1,500 thousand vkm depending on cost and induced demand.

This creates a fundamental tension: the scenarios that most successfully improve mobility also generate the most vehicle travel. Even assuming full electrification, the associated increases in tire particulate emissions, road infrastructure wear, noise, and collision exposure scale with VKT rather than with emissions. The source of density improvement matters here – if efficiency gains come primarily from higher vehicle occupancy, per-capita VKT would decrease, but if they come from technical optimizations (smaller vehicles, reduced following distances), total VKT increases proportionally with the freed capacity.

### Travel times
Figure 3.4 shows mean travel time across all completed trips (all modes) in each scenario. The reference value is 940 seconds (approximately 15.7 minutes).

<div align="center">
    <img src="img/exp4/heatmap_mean_travel_time.png" width="60%">
</div>

_Figure 3.4: Mean travel time in seconds across all completed trips. Reference: 940 seconds._

Average travel times mirror the network speed patterns but reveal an additional interaction with value of time. With density ≥ 1.0, travel times increase in nearly every scenario, reaching 1,100–1,350 seconds (18–22 minutes) with cheap, inefficient AVs – an increase of 17–43% over the reference. No combination of cost reduction or VoT improvement can offset this degradation when AVs operate inefficiently.

With density 0.333, travel times decrease substantially, reaching 489–556 seconds (8–9 minutes) in the most favorable scenarios – a reduction of roughly 40–48% compared to the reference. However, this improvement only materializes when VoT is sufficiently low (factor ≤ 0.5) to trigger substantial modal shift from cars to AVs. At VoT factor 1.0 with density 0.333, travel times still improve but more modestly (814–1,116 seconds), because insufficient car-to-AV switching means conventional vehicles continue to consume road space while AVs add to traffic. This demonstrates that even highly efficient AVs can only improve system performance if they attract enough riders away from conventional cars – density enables improvement, but behavioral shift is required to realize it.

With density 0.5, the picture is mixed: travel times improve modestly when induced demand is low (1.0) and costs are sufficiently reduced, but degrade when induced demand reaches 1.25 or higher. This positions density 0.5 as a knife-edge where the system can tip in either direction depending on demand conditions.

In scenarios with density ≥ 1.0 at cost factor 0.125, some travel time values (particularly with low VoT) should be interpreted with caution: severe congestion prevented a portion of trips from completing within the simulation duration (05:00–24:00), meaning the reported averages reflect only completed trips and may understate actual experienced travel times in those scenarios.

## 5.3 Policy intervention effectiveness across scenarios
Traditional policy interventions show limited effectiveness and often counterproductive outcomes, with no single strategy proving robust across different AV deployment scenarios. Figure 5.4 presents mode shares under nine policy combinations ranging from localized interventions (autoluw area restrictions) to comprehensive city-wide measures (combined speed reductions and congestion pricing). All pricing-based policies reduce AV adoption compared to no intervention, while speed reductions alone (policy 5) show virtually no effect on mode shares or any other metric.

| ![heatmap_mode_share_car.png](img/sce_pol/heatmap_mode_share_car.png) | ![heatmap_mode_share_av.png](img/sce_pol/heatmap_mode_share_av.png) |
|-----|-----|
| ![heatmap_mode_share_bike.png](img/sce_pol/heatmap_mode_share_bike.png) | ![heatmap_mode_share_transit.png](img/sce_pol/heatmap_mode_share_transit.png) |
_Figure 5.4: Mode shares across eight scenarios and nine policy interventions_

The most aggressive intervention—city-wide €10 congestion pricing with 20 km/h speed reductions applied throughout the day (policy 8)—reduces AV share most consistently, bringing adoption below 10% even in high-adoption scenarios. However, this policy fails to shift travelers toward sustainable modes; instead, it primarily dampens modal shifts that would have occurred, occasionally even increasing car usage. The city-wide day tariff (policy 7) achieves similar AV adoption reductions without speed limits, demonstrating that pricing alone drives behavioral change more effectively than speed restrictions.

Localized interventions (policies 1-2) targeting Rotterdam's autoluw area—affecting only 13% of the population—show negligible impact on system-wide metrics. Even city-wide peak-hour interventions (policies 3, 6) prove insufficient, suggesting that temporal and spatial limitations fundamentally constrain policy effectiveness in networked transportation systems.

| ![heatmap_mean_network_speed.png](img/sce_pol/heatmap_mean_network_speed.png) | ![heatmap_total_network_distance.png](img/sce_pol/heatmap_total_network_distance.png) |
|-----|-----|
_Figure 5.5: Network speed and total vehicle distance across scenarios and policies_

Network performance metrics reveal why traditional policies struggle. Figure 5.5 shows that policies effective at reducing AV adoption in congested scenarios (with inefficient AVs) often harm performance in scenarios with efficient AVs. The city-day (4) and all-out (8) policies can increase car speeds in scenarios with density factors of 1.0-1.5 by suppressing inefficient AV adoption, but the same policies reduce speeds when applied to scenarios with efficient AVs (density ≤0.5), as they discourage use of the more space-efficient vehicles. This scenario-dependence means optimizing policy for one future may be counterproductive in another.

Perhaps most tellingly, policies that successfully reduce AV adoption rarely improve—and sometimes worsen—travel times or perceived costs. No policy consistently benefits all metrics across scenarios. The speed reduction component of combined policies actually registers as reducing "delay" in the technical sense (ratio of actual to free-flow time) because it lowers free-flow speeds, but this represents a measurement artifact rather than genuine improvement. The fundamental challenge is that static, mode-specific interventions cannot adapt to the complex, scenario-dependent dynamics of AV integration into existing transportation systems.

# 6. Discussion
## 6.1 The density imperative: implications for AV deployment
The primacy of space efficiency over cost or comfort in determining system outcomes fundamentally challenges conventional assumptions about AV development priorities. While previous research has emphasized safety, liability, and user acceptance as primary concerns (Fagnant & Kockelman, 2015), our results suggest that space efficiency may be equally critical for urban environments. The emergence of a sharp threshold around density factor 0.5—below which high adoption maintains system performance, above which it triggers degradation—has profound implications for both technology development and urban planning.

This threshold behavior extends but substantially refines earlier findings. Fagnant and Kockelman (2015) estimated that cooperative adaptive cruise control could increase lane capacity by 1-80% depending on market penetration, focusing primarily on positive potential. Our results demonstrate the inverse: inefficient AVs can dramatically reduce effective capacity, creating gridlock even in moderately-sized cities. The split we observe is more pronounced than previous research suggested, with scenarios above and below the threshold exhibiting fundamentally different system dynamics rather than gradual performance degradation.

Critically, our model treated density as an outcome-based metric agnostic to implementation. A density factor of 0.5 could emerge from smaller vehicle sizes, reduced following distances through platooning, higher occupancy through ride-sharing, more efficient routing, or combinations thereof. This approach reveals that regardless of which technological or operational solutions emerge, cities need clear performance standards focused on space consumption per passenger rather than treating all AVs as equivalent. The finding that even dramatic cost reductions to one-eighth current levels cannot drive beneficial adoption without adequate space efficiency underscores that affordability alone is insufficient—efficiency determines system viability.

The non-linear adoption patterns we observe, particularly the rapid acceleration once cost and efficiency thresholds align, align with Rogers' (1962) diffusion of innovation theory but add important nuance. Our results suggest technology adoption curves may be strongly conditional on performance thresholds—without adequate space efficiency, even aggressive price reductions cannot trigger the rapid adoption phase typical of successful innovations. This implies that AV developers focusing solely on cost reduction may be pursuing a strategy that cannot succeed in urban environments without parallel efficiency improvements.

The modal competition patterns revealed in our simulations challenge optimistic assumptions about AV impacts on sustainable transport. Our finding that cyclists and transit users switch to AVs more readily than car users extends research on ride-hailing services (Graehler et al., 2019) but shows larger magnitude effects. This occurs because our model captures how AVs might reduce perceived time costs through enabling productive use of travel time, creating particularly strong competition with modes that currently require user attention (cycling) or have inherent waiting times (transit). For cities like Rotterdam with high cycling mode shares, this represents a more severe threat to sustainability goals than typically acknowledged.

The relationship between space efficiency and vehicle kilometers traveled adds critical nuance to debates about induced demand. Metz (2018) argued that AV impacts would depend largely on ownership models, but our results suggest the critical factor is operational space efficiency regardless of ownership structure. With inefficient AVs, the system becomes so congested that VKT actually decreases—a perverse outcome where poor performance constrains total travel. With efficient AVs, VKT can increase substantially, scaling nearly linearly with induced demand once capacity constraints are relieved. This creates a challenging dynamic: the scenarios that successfully improve mobility also generate significantly more vehicle travel, with implications for tire wear, road maintenance, noise, and energy consumption that persist even with full electrification. The source of efficiency improvements matters—if density gains come from higher occupancy, per-capita VKT may decrease, but if they come from technical optimizations, total VKT will likely increase substantially.

## 6.2 The policy adaptation challenge
The scenario-dependent effectiveness of interventions reveals fundamental limitations in static transportation policy frameworks for managing technology-driven transitions. Our finding that policies optimized for one scenario often prove counterproductive in others represents a novel challenge distinct from traditional transportation policy contexts. While previous research has explored optimal policy design for specific AV scenarios, the wide variation in policy effectiveness across our scenario space suggests that the real challenge lies not in optimizing individual interventions but in developing frameworks that remain effective across multiple possible futures.

The failure of localized interventions like the autoluw area policies aligns with network theory predictions about limitations of spatially-constrained traffic interventions. However, the limited effectiveness of even comprehensive city-wide interventions in many scenarios reveals deeper challenges. Traditional transportation demand management assumes relatively stable relationships between policy levers and behavioral responses. Our results suggest these relationships may be fundamentally unstable during technology transitions, with the same intervention producing opposite effects depending on AV operating characteristics.

Speed reductions demonstrate this instability particularly clearly. In isolation, they show virtually no benefit on any metric—a finding that challenges current policy trends toward blanket urban speed limit reductions. While such policies may serve legitimate safety or livability goals not captured in our model, their ineffectiveness at managing AV-related congestion suggests they should not be relied upon as primary AV management tools. Even when combined with congestion pricing, speed reductions contribute little beyond the pricing effect alone, as demonstrated by comparing policies 7 and 8.

The more fundamental challenge is that policies successfully reducing AV adoption in congested scenarios with inefficient AVs often harm performance in scenarios with efficient AVs. This creates a temporal paradox for policymakers: interventions must be designed and implemented before knowing which future will materialize, yet effectiveness depends critically on future conditions. Traditional approaches of observing problems and responding reactively will likely prove inadequate given the potential for rapid adoption once cost and efficiency thresholds align.

This suggests the need for adaptive policy frameworks that automatically adjust based on observed system performance rather than implementing static interventions. Such frameworks might include dynamic pricing that responds to both congestion levels and AV fleet efficiency metrics, access rules that automatically adjust based on measured space consumption per passenger, or performance standards that become more stringent as adoption increases. However, implementing such approaches requires not just technical solutions but new institutional capabilities for real-time monitoring and automatic policy adjustment—capabilities that most cities currently lack.

The vulnerability of sustainable transport modes to AV competition revealed in our results suggests that protecting these modes requires more than traditional infrastructure provision. Our finding that AVs attract cyclists and transit users more readily than car drivers implies that defensive policies focusing only on restricting AVs may be insufficient. Instead, cities may need proactive integration strategies that leverage AVs to complement rather than compete with sustainable modes—for example, designing AV services specifically for first/last mile connections rather than allowing them to serve as direct alternatives to transit or cycling for entire trips.

The policy analysis also reveals important gaps in current intervention strategies. None of the tested policies effectively address the VKT increases associated with efficient AVs, suggesting need for approaches directly targeting absolute mobility levels rather than just managing congestion. This might include occupancy-based road pricing that differentiates between single-occupancy and shared AVs, or VKT-normalized impact fees that account for vehicle weight and usage patterns. Such policies would need to balance mobility benefits against externalities like tire wear and infrastructure degradation that persist regardless of electrification.

## 6.3 Methodological contributions and limitations
The integrated agent-based and mesoscopic simulation approach successfully captured critical feedback loops between individual decisions and system performance, while revealing important areas requiring further development. The hybrid methodology proved effective at representing both heterogeneous individual behavior and emergent network-level dynamics at the scale required for urban analysis—a challenge that neither pure agent-based models nor traditional traffic assignment approaches adequately address. The discrete event framework enabled precise temporal modeling while maintaining computational tractability for exploring 144 scenarios, demonstrating that detailed behavioral modeling and systematic scenario analysis need not be mutually exclusive.

However, several methodological limitations inform result interpretation. The rational choice mode selection framework, while useful for exploring system-level dynamics, likely oversimplifies the complexity of actual travel decisions. Real adoption patterns involve habit, psychological factors, social influences, and complex preferences that our utility-maximization approach cannot fully capture. The deliberate choice to use this simplified framework was driven by lack of stated preference data for AVs and focus on system-level effects rather than individual prediction, but it means our adoption curves should be interpreted as illustrative of threshold behavior rather than precise forecasts.

The traffic simulation component, while adequate for examining system-level congestion effects, simplified intersection dynamics through default merge priorities due to data limitations. This may underestimate local bottleneck effects, particularly in dense urban areas where intersection capacity often constrains network performance. The use of fixed travel times for non-car modes, necessitated by API cost constraints, means the model cannot capture potential benefits AVs might provide to other modes through reduced traffic interference, nor can it represent how extreme congestion might eventually affect cycling safety or transit reliability.

The validation results demonstrated that the model reproduces key characteristics of current travel patterns while showing systematic deviations, particularly overestimating bicycle usage and underestimating car use. These differences likely stem from the model's omission of weather effects, cargo requirements, multi-stop trips, and other car-favoring factors beyond pure time-cost optimization. However, the relative ordering of mode preferences and temporal patterns align with observed behavior, suggesting sufficient validity for examining modal shift dynamics even if absolute mode shares differ from current empirical data.

Most fundamentally, the model examines short-term effects within fixed urban form, unable to capture potential long-term land use changes that might result from altered transportation costs and travel times. Previous transportation innovations have consistently reshaped urban development patterns over decades—improved mobility enabling residential dispersion, which in turn increases travel demand. Our findings about reduced perceived travel costs with efficient AVs suggest potential for significant induced development effects, but these remain outside the model's scope. This limitation is particularly important for interpreting the VKT results: current urban form constrains how much additional vehicle travel can be generated, but in the long term, land use adaptation might enable substantially greater increases.

The treatment of induced demand as an exogenous scenario variable rather than an endogenous response represents both a limitation and a deliberate modeling choice. This approach enabled systematic exploration of different demand trajectories without requiring speculative assumptions about elasticities, but it means the model cannot represent how induced demand might vary by trip purpose, time of day, or demographic group. Future research incorporating activity-based travel demand models could better capture these dynamics, though at significant computational cost.

# 7. Conclusions

This research demonstrates that autonomous vehicle impacts on urban mobility depend fundamentally on space efficiency rather than cost or comfort, with implications for both technology development and policy design. Through integrated agent-based and mesoscopic traffic simulation of 144 scenarios in Rotterdam, three critical findings emerge that challenge conventional assumptions about AV deployment.

Space efficiency emerges as the primary determinant of whether AVs improve or degrade urban transportation systems. A critical threshold around density factor 0.5—representing the space required per person transported relative to conventional vehicles—divides two fundamentally different futures. Below this threshold, high AV adoption can maintain or even improve network performance despite induced demand. Above it, increased adoption inevitably degrades system performance regardless of cost reductions or comfort improvements. This finding fundamentally challenges development priorities that emphasize cost reduction and user experience over operational efficiency. Even reducing costs to one-eighth of current levels cannot enable beneficial urban adoption without adequate space efficiency. Cities and developers should therefore prioritize metrics of space consumption per passenger over traditional performance indicators, establishing clear operational standards focused on outcomes rather than prescribing specific technological implementations. Whether efficiency improvements come from vehicle size optimization, platooning, ride-sharing, or routing optimization matters less than achieving the threshold itself.

Moreover, AVs compete more directly with sustainable modes than with private cars, with cyclists and transit users switching to AVs earlier and faster than car drivers as costs decrease. This asymmetry stems from how AVs might reduce perceived time costs through enabling productive use of travel time, creating particularly strong competition with modes requiring user attention or involving waiting. The pattern intensifies with efficient AVs (density ≤0.5) where adoption reaches high levels: cycling and transit shares plummet while car usage remains stable or increases. This threatens urban sustainability goals more severely than typically recognized, suggesting that AV deployment without careful integration strategies could undermine decades of investment in sustainable transportation infrastructure. The finding is particularly concerning for cities like Rotterdam with high cycling mode shares. Defensive policies restricting AVs alone appear insufficient—cities need proactive strategies ensuring AVs complement rather than compete with sustainable modes, potentially by designing services specifically for first/last mile connections rather than allowing direct competition for entire trips.

Additionally, traditional static policy interventions show limited effectiveness and often counterproductive outcomes across different scenarios. Localized restrictions prove too limited in scope to affect networked systems meaningfully. Even comprehensive city-wide interventions combining speed reductions and congestion pricing show highly scenario-dependent effectiveness—policies that reduce congestion in scenarios with inefficient AVs often harm performance in scenarios with efficient AVs by discouraging use of space-efficient vehicles. Speed reductions alone demonstrate virtually no benefit on any metric. No single intervention strategy proves robust across the range of plausible futures explored. This scenario-dependence reveals fundamental limitations in current transportation policy frameworks that assume relatively stable relationships between interventions and responses. Cities need adaptive frameworks that automatically adjust based on observed performance rather than implementing static rules—dynamic pricing responding to both congestion and fleet efficiency, access policies adjusting based on measured space consumption, performance standards that tighten with adoption. However, such approaches require new institutional capabilities for real-time monitoring and automatic adjustment that most cities currently lack.

These findings advance transportation systems modeling by demonstrating critical threshold behavior in technology adoption that creates discrete rather than continuous response patterns, identifying space efficiency as a primary determinant of system-level impacts distinct from cost or comfort factors, and revealing fundamental limitations of static policy frameworks for managing transitions with high uncertainty. The integrated simulation approach proves effective at capturing feedback loops between individual decisions and network performance at urban scale, though results also highlight needs for better behavioral representation and longer-term land use dynamics.

For technology developers, space efficiency must become a primary design objective alongside safety and user experience. For cities, this implies establishing clear performance standards focused on space consumption per passenger rather than treating all AVs equivalently, monitoring not just adoption rates but operational efficiency metrics, and preparing adaptive policy frameworks before adoption accelerates. For transport authorities, the finding that AVs threaten sustainable modes more than cars suggests that integration strategies should focus on protecting cycling and transit through service design rather than relying solely on restrictions. The substantial VKT increases possible with efficient AVs indicate that cities must address absolute mobility levels through occupancy-based pricing or VKT-normalized impact fees rather than managing congestion alone.

Three critical gaps require investigation in future research. First, activity-based travel demand modeling could better capture how AVs might reshape daily activity patterns and long-term location choices, particularly important given findings about reduced perceived travel costs. Second, detailed studies of operational strategies for achieving density thresholds below 0.5—whether through vehicle design, fleet management, ride-sharing incentives, or routing optimization—would inform practical implementation. Third, research into adaptive policy frameworks that respond automatically to observed conditions could address the scenario-dependence challenge revealed in intervention effectiveness. Understanding the determinants of space efficiency and developing institutional capabilities for policy adaptation emerge as particularly urgent priorities.

The significant variations between potential futures revealed by this research—from improved mobility to system gridlock—emphasize that early trajectory decisions may have lasting implications. AV impacts appear neither inherently beneficial nor inevitably problematic, but rather highly conditional on the interaction between operating characteristics, adoption patterns, and policy frameworks. Governments, regulators, and industry stakeholders should prioritize understanding this complex system and developing steering mechanisms toward futures where AVs support urban sustainability, connectivity, and livability rather than allowing market forces alone to determine outcomes. The network effects and behavioral patterns identified suggest that waiting to observe problems before responding will likely prove inadequate given the potential for rapid change once critical thresholds align.

# References
Ben-Akiva, M. E., & Lerman, S. R. (1985). Discrete choice analysis: theory and application to travel demand (Vol. 9). MIT press.

Centraal Bureau voor de Statistiek. (2023a). Auto's, kilometers en rijbewijzen per pc4 [Cars, kilometers and driver's licenses per postcode]. https://www.cbs.nl/nl-nl/maatwerk/2023/35/auto-s-kilometers-en-rijbewijzen-per-pc4

Centraal Bureau voor de Statistiek. (2023b). Gegevens per postcode [Data by postcode]. https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode

Centraal Bureau voor de Statistiek. (2023c). Statistische gegevens per vierkant en postcode 2022-2021-2020-2019 [Statistical data by grid and postcode 2019-2022]. https://www.cbs.nl/nl-nl/longread/diversen/2023/statistische-gegevens-per-vierkant-en-postcode-2022-2021-2020-2019/bijlagen

Centraal Bureau voor de Statistiek. (2023d). Voertuigen naar brandstofsoort en postcode 2023 [Vehicles by fuel type and postcode 2023]. https://www.cbs.nl/nl-nl/maatwerk/2023/24/voertuigen-naar-brandstofsoort-en-postcode-2023

Centraal Bureau voor de Statistiek. (2024). Onderweg in Nederland (ODiN) 2023: Onderzoeksbeschrijving [Traveling in the Netherlands 2023: Research description]. https://www.cbs.nl/nl-nl/longread/rapportages/2024/onderweg-in-nederland--odin---2023-onderzoeksbeschrijving

Cervero, R. (2002). Induced travel demand: Research design, empirical evidence, and normative policies. Journal of Planning Literature, 17(1), 3-20.

Downs, A. (1962). The law of peak-hour expressway congestion. Traffic Quarterly, 16(3).

Duarte, F., & Ratti, C. (2018). The impact of autonomous vehicles on cities: A review. Transport Reviews, 38(3), 409-428. https://doi.org/10.1080/10630732.2018.1493883

Fagnant, D. J., & Kockelman, K. (2015). Preparing a nation for autonomous vehicles: Opportunities, barriers and policy recommendations. Transportation Research Part A: Policy and Practice, 77, 167-181. https://doi.org/10.1016/j.tra.2015.04.003

Fakhrmoosavi, F., Kamjoo, E., Kavianipour, M., Zockaie, A., Talebpour, A., & Mittal, A. (2022). A stochastic framework using Bayesian optimization algorithm to assess the network-level societal impacts of connected and autonomous vehicles. Transportation Research Part C: Emerging Technologies, 139, 103663. https://doi.org/10.1016/j.trc.2022.103663

Gemeente Rotterdam. (2024). Verkeerscirculatieplan [Traffic circulation plan]. https://www.rotterdam.nl/verkeerscirculatieplan

Google Developers. (2024). Distance Matrix API. https://developers.google.com/maps/documentation/distance-matrix/overview

Graehler Jr, M., Mucci, R. A., & Erhardt, G. D. (2019). *Understanding the recent transit ridership decline in major US cities: Service cuts or emerging modes?* Paper presented at the Transportation Research Board 98th Annual Meeting, Washington, DC, United States, January 13-17. Transportation Research Board. https://trid.trb.org/View/1572517

Kennisinstituut voor Mobiliteitsbeleid. (2023). Nieuwe waarderingskengetallen voor reistijd, betrouwbaarheid en comfort [New valuation indicators for travel time, reliability and comfort]. https://www.kimnet.nl/publicaties/publicaties/2023/12/04/nieuwe-waarderingskengetallen-voor-reistijd-betrouwbaarheid-en-comfort

Law, A. M. (2014). Simulation modeling and analysis (5th ed.). McGraw-Hill.

Lee, D. B., Jr., & Klein, L. A. (1999). Induced traffic and induced demand. Transportation Research Record, 1659, 9-17. https://doi.org/10.3141/1659-09

Liu, Z., Li, R., & Dai, J. (2022). Effects and feasibility of shared mobility with shared autonomous vehicles: An investigation based on data-driven modeling approach. Transportation Research Part A: Policy and Practice, 156, 206-226. https://doi.org/10.1016/j.tra.2022.01.001

McNally, M. G. (2007). The four step model. https://escholarship.org/uc/item/6091s9tg

Metropolitaan Verkeer- en Vervoermodel MRDH. (2024). MRDH Verkeersmodel (V-MRDH). https://www.mrdh.nl/verkeersmodel

Metz, D. (2018). Developing policy for urban autonomous vehicles: Impact on congestion. Urban Science, 2(2), 33. https://doi.org/10.3390/urbansci2020033

Narayanan, S., Chaniotakis, E., & Antoniou, C. (2022). Modelling reservation-based shared autonomous vehicle services: A dynamic user equilibrium approach. Transportation Research Part C: Emerging Technologies, 140, 103651. https://doi.org/10.1016/j.trc.2022.103651

Nederlands Instituut voor Budgetvoorlichting. (2024). Autokosten [Car costs]. https://www.nibud.nl/onderwerpen/uitgaven/autokosten/

Nederlandse Spoorwegen. (2024). NS API Portal. https://apiportal.ns.nl/

Newell, G. (2002). A simplified car-following theory: a lower order model. Transportation Research Part B Methodological, 36(3), 195–205. https://doi.org/10.1016/s0191-2615(00)00044-8

OpenStreetMap Foundation. (2024). About OpenStreetMap. https://www.openstreetmap.org/about

Ter Hoeven, E., Kwakkel, J., Hess, V., Pike, T., Wang, B., Rht, N., & Kazil, J. (2025). Mesa 3: Agent-based modeling with Python in 2025. The Journal of Open Source Software, 10(107), 7668. https://doi.org/10.21105/joss.07668

Seo, T. (2025). UXsim: lightweight mesoscopic traffic flow simulator in pure Python. The Journal of Open Source Software, 10(106), 7617. https://doi.org/10.21105/joss.07617

Small, K. A. (2012). Valuation of travel time. Economics of transportation, 1(1-2), 2-14.

Talebian, A., & Mishra, S. (2018). Predicting the adoption of connected autonomous vehicles: A new approach based on the theory of diffusion of innovations. Transportation Research Part A: Policy and Practice, 116, 92-104. https://doi.org/10.1016/j.tra.2018.06.007

Talebian, A., & Mishra, S. (2018). Predicting the adoption of connected autonomous vehicles: A new approach based on the theory of diffusion of innovations. Transportation Research Part C: Emerging Technologies, 95, 363-380. https://doi.org/10.1016/j.trc.2018.06.005

Trein Onderweg. (2024). Wat kost de trein [Train costs]. https://www.treinonderweg.nl/wat-kost-de-trein.html

Wang, T., Jian, S., Zhou, C., Jia, B., & Long, J. (2024). Multimodal traffic assignment considering heterogeneous demand and modular operation of shared autonomous vehicles. Transportation Research Part C: Emerging Technologies, 169, 104881. https://doi.org/10.1016/j.trc.2024.104881

Wardrop, J. G. (1952). Road paper. some theoretical aspects of road traffic research. Proceedings of the institution of civil engineers, 1(3), 325-362.

Yan, H., Kockelman, K. M., & Gurumurthy, K. M. (2020). Shared autonomous vehicle fleet performance: Impacts of trip densities and parking limitations. Transportation Research Part D: Transport and Environment, 89, 102577. https://doi.org/10.1016/j.trd.2020.102577

# Appendices
## Appendix A: Model description

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
4. **Journeys**: Represent individual trips made by travelers.

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
- `enable_av`: Boolean indicating if AVs are enabled in the simulation
- `av_cost_factor`: Cost factor for AVs
- `av_vot_factor`: Value of time factor for AVs
- `ext_vehicle_load`: External vehicle load factor
- `uxsim_platoon_size`: Platoon size for UXsim traffic simulation
- `car_comfort`: Comfort factor for cars
- `bike_comfort`: Comfort factor for bicycles
- `av_density`: Density factor for AVs
- `induced_demand`: Factor for induced demand
- `policy_tarif`: Tariff for policy implementation
- `policy_tarif_time`: Time period for policy tariff
- `policy_speed_reduction`: Speed reduction factor for policy
- `policy_area`: Area where policy is applied
- `available_modes`: List of available transportation modes
- `transit_price_per_km`: Price per kilometer for public transit
- `car_price_per_km_variable`: Variable cost per kilometer for cars
- `car_price_per_km_total`: Total cost per kilometer for cars
- `av_initial_costs`: Initial costs for using an autonomous vehicle
- `av_costs_per_km`: Cost per kilometer for autonomous vehicles
- `av_costs_per_sec`: Cost per second for autonomous vehicles
- `default_value_of_times`: Default values of time for different modes
- `comfort_factors`: Comfort factors for different modes
- `pop_dict_pc4_city`: Dictionary of population by postal code
- `mrdh65s`: List of unique MRDH regions in the simulation
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

##### 2.2.4 Journey State Variables

- `agent`: Reference to the agent making the journey
- `origin`: Origin of the journey (postal code)
- `destination`: Destination of the journey (postal code)
- `mode`: Chosen mode of transport
- `start_time`: Start time of the journey
- `travel_time`: Estimated travel time
- `end_time`: End time of the journey
- `distance`: Journey distance
- `cost`: Monetary cost of the journey
- `perceived_cost`: Perceived cost (including time value)
- `comf_perceived_cost`: Comfort-adjusted perceived cost
- `used_network`: Boolean indicating if the journey used the road network
- `available_modes`: List of available modes for this journey
- `perceived_cost_dict`: Dictionary of perceived costs for all available modes
- `started`: Boolean indicating if the journey has started
- `finished`: Boolean indicating if the journey has finished
- `act_travel_time`: Actual travel time (for car/AV journeys)
- `act_perceived_cost`: Actual perceived cost (for car/AV journeys)
- `o_node`: Origin node in the road network
- `d_node`: Destination node in the road network
- `vehicle`: Vehicle object for car/AV journeys

#### 2.3 Scales

- **Spatial scale**: The model covers the Rotterdam urban area, represented by 125 4-digit postal code (PC4) regions within 21 MRDH (Metropoolregio Rotterdam Den Haag) areas.
- **Temporal scale**: The simulation typically runs from 5:00 to 24:00 (19 hours) with a default step time of 5 minutes (1/12 hour).
- **Population scale**: The model simulates approximately 100,000 agents, with each agent representing a platoon of vehicles (default size 10), approximating the actual population of 991,575 in the area.

### 3. Process Overview and Scheduling

The model follows a discrete event simulation approach, with the following main processes:

1. **Initialization**: 
   - Set up the simulation environment and parameters
   - Create agents and assign them to locations based on population data
   - Initialize the road network and traffic simulation (UXsim)
   - Assign car ownership and driver's licenses based on postal code data

2. **Generate trip times and destinations**: 
   - Each agent generates a set of trip times based on hourly probabilities
   - Destinations are assigned for each trip based on origin-destination matrices

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

6. **Add external vehicle load**:
   - Add vehicles representing external traffic at specified intervals

7. **Data collection and analysis**:
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
- Origin-destination pairs: Trip destinations are chosen probabilistically based on origin-destination matrices.

#### 4.10 Collectives

The model does not explicitly represent collectives or agent groups. However, agents are implicitly grouped by their postal code and MRDH region, which influences their trip patterns and available transportation options.

#### 4.11 Observation

The model collects and outputs various data for analysis:

- Mode choice distribution (overall and distance-weighted)
- Trips by mode and time of day
- Traffic conditions (from UXsim), including speed, density, and flow
- Parking demand by area over time
- Journey details for each completed trip, including origin, destination, mode, travel time, and costs
- System-level metrics such as total vehicle kilometers traveled, average speeds, and congestion levels

This data is saved in various formats (Python pickle files, Feather files) for further analysis and visualization.

### 5. Initialization

The model is initialized with the following steps:

1. Set up the simulation environment with specified parameters (e.g., number of agents, start and end times, time step, policy variables).
2. Load geographical and population data for the Rotterdam area from various sources (CBS, MRDH, OpenStreetMap).
3. Create agents and assign them to postal code areas based on population distribution.
4. Assign car ownership and driver's licenses to agents based on data for each postal code.
5. Generate trip schedules for each agent based on time-of-day probabilities.
6. Initialize the UXsim traffic simulation component with the road network data.
7. Set up initial parking distribution based on car ownership in each area.
8. Initialize data collection structures for various metrics.

The initial state can vary between simulation runs due to the stochastic elements in agent creation, attribute assignment, and trip generation.

### 6. Input data
The model uses several external data sources as input for agent and system behavior:

#### 6.1 Population data by 4-digit postal code (PC4) from CBS

Population data from the CBS is used to distribute agents across the urban area ([CBS-postcode]). The Dutch 4-digit postal code areas are used, which roughly represent a neighbourhood each. This gives heterogeneity in the system and enables adequate travel counts and traffic pressure on the network. In the 125 PC4 areas, there are in total 991,575 residents. The population in each area gets scaled down with the platoon size (10 by default), resulting in approximately 100,000 agents in the simulation.

![pop_density_pc4.svg](img%2Fdata%2Fpop_density_pc4.svg)
_Fig A.1: Population count for each PC4 area (number) and population density (color)_

#### 6.2 Car ownership and driver's license data by postal code (CBS)

Car ownership is also sourced from the CBS per PC4 area. For each area, a certain percentage of agents gets assigned a car as additional available mode. On average that's 35.4% and varies between ~19% and ~65% per area. This enables heterogeneity among agents and enables realistic mode choices.
![car_per_inhabitant_pc4.svg](img%2Fdata%2Fcar_per_inhabitant_pc4.svg)
_Fig A.2: Car ownership per inhabitant for each PC4 area_

The full analysis for both the population and car ownership data is available in the [`prototyping/pc4.ipynb`](../prototyping/pc4.ipynb) notebook.

#### 6.3 Road network data from OpenStreetMap

The road network data was extracted from OpenStreetMap (OSM) using the [OSMnx] library (version 2.0.0b2) on September 30, 2024. The network consists of two distinct components: a detailed inner-city network covering the city area and a broader surrounding network covering supporting area. This dual-network approach allows for higher resolution within the primary study area while still allowing traffic to flow in and out of the city.

The inner-city network includes all roads from tertiary level and above (motorways, trunks, primary, secondary, and tertiary roads, including their respective link roads), which are all arterial roads to allow traffic to flow accurately. The surrounding network includes only major roads (secondary level and above) to reduce computational complexity, since precise traffic flow is less critical in these areas (and are not included in the measurements). Roads under construction, particularly the new A16 motorway and Blankenburg tunnel, were included to ensure the network represents the near-future situation.

The downloaded networks contained:
- City network: 44,464 nodes and 56,236 edges
- Supporting network: 48,674 nodes and 57,024 edges
- Combined raw network: 93,138 nodes and 113,260 edges

Since the computational complexity scales quadratically with the number of edges, the raw networks were simplified to reduce the number of nodes and edges. This was done by eliminating nodes with degree 2, which are not intersections, and consolidating intersections within a certain distance threshold.

These networks were processed through the following steps:
1. Projection to a unified coordinate reference system (EPSG:28992, Amersfoort / RD New)
2. Network attribute assignment, including:
   - Speed limits (derived from OSM maxspeed tags)
   - Number of lanes (from OSM lane tags)
   - Road type classification
   - Network identification (city or surrounding area)
3. Intersection consolidation using variable tolerances:
   - 10-meter tolerance for the city network
   - 50-meter tolerance for the surrounding network
4. Network simplification while preserving essential attributes (length, travel time, lanes)

The final processed network contains 1,575 nodes and 3,328 edges, which was both suitable for the research problem and feasible to simulate. Each edge in the network contains the following key attributes:
- Length (meters)
- Speed limit (km/h)
- Number of lanes
- Road type (motorway, trunk, primary, secondary, tertiary)
- Network identification (city or surrounding)
- Travel time (seconds, calculated from length and speed limit)

![merged_network.svg](img%2Fmerged_network.svg)
_Fig A.3: The processed road network showing hierarchical road types (line width) and network components (color). The main network (red) includes tertiary and larger roads within Rotterdam, while the supporting network (blue) includes secondary and larger roads in the surrounding area._

During simulation, the network is used by the UXsim traffic model to:
- Calculate shortest paths between origins and destinations
- Simulate traffic flow and congestion
- Track vehicle movements and area-based metrics
- Apply speed reductions in policy scenarios

The simplified network structure proved particularly efficient for the mesoscopic simulation approach, allowing for city-scale simulations while maintaining adequate detail for analyzing both local and system-wide effects of autonomous vehicles and policy interventions.

The full analysis is available in the [`network/create_network.ipynb`](../network/create_network.ipynb) notebook.

#### 6.4 Travel time and distance data for public transit and cycling (from Google Maps API)
Travel times and distances for non-car modes (public transit and cycling) were collected using the Google Maps Distance Matrix API. Data was gathered for all possible origin-destination pairs between the 125 postal code areas in the Rotterdam urban area, resulting in 15,500 unique combinations for both cycling and public transit. This fell withing the free tier of the API, which allows for up to 40.000 elements travel time requests per month, costing \$156.25 for the complete matrix in both modes, within the \$200 free monthly credit Google provides.
 
The data collection was performed for Thursday, September 17, 2024, at 08:00, representing typical weekday conditions. While for bycicle the travel time is relatively stable, for public transit it can vary due to the frequency of the services and more data collections would be needed to capture proper early morning, late evening and weekend travel times. The travel times on a Thursday morning are when the highest frequency of trips are made, and provide generally the fastest travel times, representing the optimal conditions for public transit.

The API provided both travel time (in seconds) and distance (in meters) for each origin-destination pair. For transit, this includes walking to/from stops, waiting times, and any transfers. For cycling, it assumes use of the standard cycling infrastructure and average cycling speeds.

Centroid-to-centroid measurements between postal code areas where made, initially only between the 21 MRDH regions (420 pairs), which lead to visible noise in even the high-level KPIs. It also didn't allow within-region travel, which is a significant part of the trips. Also, some of the centroids were really unfortunately placed (right between stations for example), which with the low number of points resulted in unexpected behavior. Therefore, the resolution was increased to 4-digit postal code level, and OD lookup tables for all 15.500 pairs between the geographical centroids of the 125 PC4 areas was created. This directly lead to practically eliminating the noise in the KPIs, and allowed for trips to other PC4 areas within the same MRDH region.

To validate and gain insights into the collected data, an exploratory analysis was performed, including histograms, box plots, and scatter plots of travel times and distances for both modes. Notably:

Fig A.4 shows the distribution of cycling travel times are more skewed towards shorter durations, with a median and mean below 40 minutes, while transit travel times were more evenly distributed, with a median and mean above 50 minutes.

![travel_time_google_maps_api_hist_boxplot.svg](img%2Fdata%2Ftravel_time_google_maps_api_hist_boxplot.svg)
_Fig A.4: Distribution of travel times between the 15.500 centroid-pairs for cycling and public transit._

Fig A.5 shows a scatter plot of travel times versus bird's-eye distances for both modes. It shows cycling having a clear maximum speed and relatively linear relationship between time and distance, while public transit has a lesser correlation, with a lot of variation in travel times for similar distances, and now clear minimum or maximum speeds.

![travel_time_distance_scatter.png](img%2Fdata%2Ftravel_time_distance_scatter.png)
_Fig A.5: Scatter plot of travel times versus distances between the 15.500 centroid-pairs for cycling and public transit._

The full analysis is available in the [`travel_api/travel_time_distance_google.ipynb`](../travel_api/travel_time_distance_google.ipynb) notebook.

#### 6.5 Trip generation probabilities by hour (derived from ODiN 2023 data)

Trip generation probabilities were derived from the Dutch National Travel Survey (ODiN) 2023 dataset to create temporal patterns of travel demand. The ODiN survey provides detailed information about travel behavior in the Netherlands, including the timing of trip starts throughout the day. Since it is a survey, the data is not perfect, and more care was taken to ensure the data was cleaned properly and representative for this research.

While ODiN offers a wealth of data, the focus was on the timing of trips, which was used to create hourly trip generation probabilities for the simulation model. The data was aggregated to count the number of trips starting in each hour of the day, resulting in a distribution of travel demand over time.

![trips_by_weekday_and_hour_heatmap.svg](img%2Fdata%2Ftrips_by_weekday_and_hour_heatmap.svg)
_Fig A.6: Heatmap showing the number of trips by hour and day of the week. The color intensity indicates the number of trips, with lighter colors representing more trips._

The heatmap in Figure A.6 shows several distinct temporal patterns:
- A sharp morning peak (8:00-9:00) and more spread out evening peak (16:00-18:00) peak hours on weekdays
- Lower (especially on Sunday) but more spread out travel demand during weekends
- Very low travel activity between midnight and 5:00
- Relatively consistent patterns Monday through Thursday (except with a small lunch peak on Wednesday, probably due to school schedules)
- Slightly different pattern on Fridays, with a less pronounced evening peak, more spread out through the afternoon
- Weekend travel starting later in the day and more evenly distributed

For use in the simulation model, the trip generation probabilities were calculated by:
1. Counting the number of unique travelers per day of the week
2. Counting trips starting in each hour
3. Dividing the hourly trip counts by the number of unique travelers to get the probability that an individual starts a trip in that hour
4. Averaging the probabilities for Monday through Thursday to get representative weekday patterns (done in the Model itself, any day or combination of days can be selected there).

Since there are relatively large steps between some hours, 15-minute intervals were also explored to see if more smoother steps could be achieved.

![trips_by_weekday_and_quarter_hour_heatmap.png](img%2Fdata%2Ftrips_by_weekday_and_quarter_hour_heatmap.png)
_Fig A.7: Heatmap showing the number of trips by quarter-hour and day of the week._

However, as can be seen in the quarter-hour heatmap, there are very distinct pattern in which the whole, and in a lesser extent half, hours are over-represented. This is likely caused by people rounding their travel times to the nearest hour in the survey, and the data was therefore kept in hourly bins.

As a default value the travel distribution is averaged over Monday to Thursday, as weekdays are when the largest congestion and travel demand is expected, and thus most interesting for this research. The number of trip for each hour of each day was normalized over the number of the number of people taking trips that day, to create a lookup table giving the probability of a person starting trip starting in a specific hour of a specific day.

![chance_of_starting_trip_by_hour.svg](img%2Fdata%2Fchance_of_starting_trip_by_hour.svg)
_Fig A.8: Average probability of an individual starting a trip by hour during weekdays (Monday-Thursday)._

Using these lookup tables, the start time, end time (and thus duration) and day of the week could be varied in the model, while always initiating a representative number of trips. Many initial tests were only performed on a few hours (like 7:00-11:00), while the full 05:00-24:00 in which significant travel demand is present was used for all experiments.

The full analysis is available in the [`prototyping/ODiN_analysis.ipynb`](../prototyping/ODiN_analysis.ipynb) notebook.

#### 6.6 Origin-destination matrices for the Rotterdam area (V-MRDH model)
Origin-destination (OD) matrices were obtained from the V-MRDH 3.0 transport model (October 2023 version), which provides detailed travel demand data for the Rotterdam-The Hague metropolitan area. The V-MRDH model divides The Netherlands into 65 traffic analysis zones with varying sizes - smaller zones in dense urban areas and larger zones in peripheral regions. This model was selected because it:
- Provides validated OD patterns based on extensive traffic counts and travel surveys
- Captures different time periods (morning peak 7-9h, evening peak 16-18h, and off-peak)
- Contains separate matrices for different transport modes (car, bicycle, public transport)
- Covers both internal traffic within Rotterdam and external traffic to/from surrounding areas

![mrdh_areas_65.svg](img%2Fmrdh_areas_65.svg)
_Fig A.9: The 65 traffic analysis zones defined in the V-MRDH model, with decreasing resolution farther from the MRDH area. Numbers indicate zone identifiers._

The OD matrices were processed in several steps:

1. Data extraction and normalization:
   - Raw matrices were extracted for each mode and time period
   - Values were normalized to create probability distributions for each origin zone
   - Total travel demand was preserved while converting absolute numbers to relative flows

2. Area selection and filtering:
   - 21 zones covering the Rotterdam city area were selected as internal zones
   - 13 surrounding zones were designated as external zones for modeling boundary traffic
   - Remaining peripheral zones were excluded from the simulation
   
3. Creation of lookup tables:
   - Probability matrices were created for trip distribution in different time periods
   - Separate tables were made for internal-internal and internal-external flows
   - Data was stored in efficient dictionary format for quick runtime lookup

![od_demand.png](img%2Fdata%2Fod_demand.png)
_Fig A.10: Travel demand visualization by mode (total, car, bicycle, public transport) between zones in the Rotterdam area. Line thickness indicates trip volume._

The matrices revealed several interesting patterns, used for both model validation and input:

First, the modal split varies significantly by area. In the inner Rotterdam area (Noord, Kralingen, Rotterdam Centrum, Feyenoord, Delfshaven), the model split was 13.4% car, 69.9% bicycle and 16.7% public transport.
In the (full study area) of broader Rotterdam, the split was 37.7% car, 49.0% bicycle and 13.3% public transport. These modal splits were used to validate and kalibrate the model.

Secondly, distinct time-of-day patterns were present, as shown in the figure below.

![inbound_outbound_traffic.png](img%2Fdata%2Finbound_outbound_traffic.png)
_Fig A.12: Analysis of inbound/outbound traffic patterns. Top: total traffic volume. Middle: absolute difference between inbound and outbound flows. Bottom: relative asymmetry ratio._

Certain regions showed strong inbound or outbound flows during morning and evening peak hours. For example, the city center (Rotterdam Centrum) had a high volume of inbound traffic in the morning and outbound traffic in the evening, reflecting commuting patterns. The industrial harbor area (Botlek, Europoort, Maasvlakte and Vondelingenplaat) had a similar pattern, with especially the ratio of inbound to outbound traffic being high. Evening peak displays opposite outbound patterns, while off-peak hours have more balanced bi-directional flows.

From this data, OD chance dictionaries were created for each of the three time periods (morning peak, evening peak, off-peak). For each origin, the probability of traveling to each destination was stored, allowing for efficient lookup during trip generation. The total summed values for all modalities were used, leaving the mode choice to the agent behavior model.

Where withing the study area all internal trips were analyzed, for trips between the study area and the supporting area only the car trips were modelled. From the OD matrices, a fixed amount of cars was added to the simulation from each external zone to the internal zones and visa versa. The total daily external traffic, together with the internal demand, is shown in the figure below.

![od_demand_int_ext.png](img%2Fdata%2Fod_demand_int_ext.png)
_Fig A.13: Comparison of internal demand (green) and external car traffic (red) patterns._

Notable is large external traffic from the directly neighboring zones, especially from the east and south.

Finally, the processed OD data serves three main purposes in the model:

1. Trip distribution: When agents generate trips, destinations are selected probabilistically based on the normalized OD matrices for the appropriate time period.
2. External traffic: Car traffic entering and leaving the study area is simulated based on the external zone matrices, scaled by time-of-day factors.
3. Validation: The modal split and spatial distribution patterns provide reference values for validating model behavior.

One limitation is that the matrices represent current travel patterns, which may not fully reflect behavior in future scenarios with autonomous vehicles. However, they provide a validated baseline for trip distribution patterns, while mode choice is handled separately by the agent behavior model. This is in line with the short to medium term scope of this research.

The full analysis is available in the [`v_mrdh/v_mrdh_od_demand.ipynb`](../v_mrdh/v_mrdh_od_demand.ipynb) notebook.

#### 6.8 Value of Time data
The model uses Value of Time (VoT) data from the Dutch Institute for Transport Policy Analysis (KiM)'s 2023 study on travel time valuation ([KiM-valuation]). Default values per mode were set at:
- Car: €10.42 per hour 
- Bicycle: €10.39 per hour
- Public Transit: €7.12 per hour
- Autonomous Vehicle: Scaled from car VoT using the av_vot_factor parameter. Experimental values of 1.0, 0.5, and 0.25 were used, resulting in the following VoT values:
  - AV VoT factor 1.0: €10.42 per hour
  - AV VoT factor 0.5: €5.21 per hour
  - AV VoT factor 0.25: €2.61 per hour

To capture heterogeneity in how individuals value their time, each agent's personal value of time is drawn from a lognormal distribution with parameters μ = -0.1116 and σ = 0.4724, capped at 4 times the default value. These parameters were chosen to produce a distribution with:
- Mean of 1.0 (preserving the base VoT values on average)
- Standard deviation of 0.5 (representing reasonable variation between individuals)
- Maximum of 4.0 (preventing extreme outliers)

The resulting distribution is shown in Figure A.x:

![vot_distribution.svg](img%2Fdata%2Fvot_distribution.svg)
_Fig A.14: Distribution of agents' Value of Time factors._

An agent's final VoT for each mode is calculated by multiplying the mode's default value by their personal VoT factor. For example, an agent with a VoT factor of 1.5 would value car travel at €15.63 per hour (1.5 × €10.42). This heterogeneous valuation leads to varied mode choices among agents even when faced with identical travel options.

Note that the VoT factor is consistent for all modes, meaning that an agent who values their time highly for car travel will also value their time highly for other modes.

For autonomous vehicles, an additional `av_vot_factor` parameter scales the car VoT before applying the agent's personal factor. This represents potential differences in how time is valued in AVs compared to conventional cars, for example due to the ability to engage in other activities while traveling. The av_vot_factor is one of the key uncertainties explored in the scenario analysis.

All VoT values are converted from euros per hour to euros per second in the model for computational efficiency, since travel times are tracked in seconds. The values represent 2022 price levels and include VAT, following standard Dutch transportation analysis practice.

This implementation of heterogeneous Values of Time helps capture realistic variation in travel preferences and mode choices among agents. It also prevents hard tipping points in mode choice, where small changes in travel times or costs could lead to large shifts in behavior.

### 6.9 Data storage, preprocessing, and integration
The model integrates multiple data sources through a centralized `Data` class in `data.py`, which is initialized once at model startup and made available throughout the simulation. This section describes how different data sources are processed and utilized within the model.

The following key data structures are loaded and processed during model initialization:

1. **Travel time and distance data**
   - Stored in pickle files: `travel_time_distance_google_{mode}.pkl` and `travel_time_distance_google_{mode}_pc4.pkl`
   - Available for modes: "transit" and "bicycling"
   - Contains matrices of travel times and distances between origins and destinations
   - Distances are converted from meters to kilometers during loading
   - Used by agents to determine travel times and costs for non-car modes
2. **Geographic information**
   - Loaded from `polygons.pkl`
   - Contains three key polygons: city_polygon, area_polygon, autoluw_polygon
   - Converted to GeoSeries with EPSG:28992 projection
   - Used for spatial queries and policy implementation zones
3. **Population and area data**
   - Population data: `population_data_pc4_65coded.pkl`
   - Areas data: `areas_mrdh_weighted_centroids.pkl`
   - Various mapping dictionaries maintained for cross-referencing:
     - `mrdh65_to_name`: Maps region numbers to names
     - `pc4_to_mrdh65`: Maps postal codes to MRDH regions
     - `mrdh65_to_pc4`: Maps MRDH regions to lists of postal codes
4. **Car ownership and licenses**
   - Stored in `rijbewijzen_personenautos.pkl`
   - Contains car ownership and driver's license rates by postal code
   - Used to assign cars and licenses to agents based on their location
5. **Trip generation data**
   - Trip probabilities: `trips_by_hour_chances.pickle`
   - Trip count distribution: `trip_counts_distribution.pickle`
   - Used to generate realistic temporal patterns of trip starts
6. **Origin-destination matrices**
   - Stored in `od_chance_dicts_periods.pickle`
   - Contains matrices for different time periods (morning peak, evening peak, off-peak)
   - Used to determine trip destinations based on origins

Several data transformations are performed during initialization, the most notable:

1. **Geographic filtering**
   - Centroids are calculated for both postal codes and MRDH65 regions
   - Areas are classified as "in_city", "in_area", or "autoluw" based on polygon containment
   - Limited to populated areas within the city (21 specific MRDH65 regions)
2. **Origin-destination processing**
   - OD matrices are normalized to create probability distributions
   - Destinations outside the study area are assigned zero probability
   - Same-location trips are handled specially based on area size
   - Probabilities are renormalized after filtering
3. **Travel time data**
   - Conversions from raw units to model units (meters to kilometers, etc.)
   - Creation of lookup dictionaries for efficient runtime access
   - Validation of data completeness for all required origin-destination pairs

A trade-off was made here between pre-processing data for efficiency and maintaining flexibility for future extensions. While much data was pre-processed to reduce runtime overhead, some of the more destructive processing (like selecting and aggregating) was done on data initialization, to allow for easy modification and extension of the model, without needed to alter data files themselves.

### 7. Submodels
Aside from the two main submodels for mode-choice and traffic simulation discussed in section [3.2](#32-key-submodels), the model has several smaller submodels that handle specific aspects of the simulation.

#### 7.1 Trip Generation
Trips are generated for each agent using the following process:

1. For each hour in the simulation period, generate a trip with probability given by `trips_by_hour_chance`.
2. Ensure an even number of trips by potentially adding or removing a trip.
3. Assign destinations based on origin-destination probability matrices, differentiating between peak and off-peak hours.
4. Schedule the trips as events in the simulation.

#### 7.2 Mode Choice
The mode choice model is implemented in the `choice_rational_vot` method of the `Traveler` class. It calculates the perceived cost for each available mode:

```python
perceived_cost = monetary_cost + travel_time * value_of_time[mode]
comf_perceived_cost = perceived_cost * comfort_factor[mode]
```

The mode with the lowest comfort-adjusted perceived cost is chosen.

#### 7.3 Traffic Simulation
The traffic simulation uses [UXsim](https://arxiv.org/abs/2309.17114), a mesoscopic traffic simulator that implements a version of [Newell's simplified car-following model](https://doi.org/10.1016/S0191-2615(00)00044-8). This model represents traffic flow as a kinematic wave, a state between microscopic (individual vehicle) and macroscopic (flow-based) modeling, providing computational efficiency while maintaining key traffic dynamics and the ability to measure traffic and congestion on a link or area level.

The driving behavior of a platoon consisting of $\Delta n$ vehicles in a link is expressed as:

$X(t + \Delta t, n) = \min\{X(t, n) + u\Delta t, X(t + \Delta t - \tau \Delta n, n - \Delta n) - \delta\Delta n\}$

where $X(t, n)$ denotes the position of platoon $n$ at time $t$, $\Delta t$ denotes the simulation time step width, $u$ denotes free-flow speed of the link, and $\delta$ denotes jam spacing of the link. This equation represents vehicles traveling at free-flow speed when unconstrained, while maintaining safe following distances when in congestion.

Traffic behavior at intersections is handled by the [incremental node model](https://doi.org/10.1016/j.trb.2011.03.001), which resolves conflicts between competing flows by processing vehicles sequentially based on predefined merge priorities. This approach maintains consistency with the kinematic wave model while efficiently managing complex intersection dynamics. The OpenStreetMap data didn't contain explicit intersection information, merge priorities were left at their default values, giving each incoming lane equal priority.

For route choice, UXsim employs a [Dynamic User Optimum](https://doi.org/10.1016/S0191-2615(00)00005-9) (DUO) model with stochasticity and delay. The attractiveness $B^{z,i}_o$ of link $o$ for vehicles with destination $z$ at time step $i$ is updated as:

$B^{z,i}_o = (1 - \lambda)B^{z,i-\Delta i_B}_o + \lambda b^{z,i}_o$

where $\lambda$ is a weight parameter and $b^{z,i}_o$ indicates whether link $o$ is on the shortest path to destination $z$. This formulation allows vehicles to gradually adapt their routes based on evolving traffic conditions, rather than instantly responding to changes in travel times.

Road characteristics are captured through differentiated jam density parameters based on road hierarchy, with motorways having lower jam densities (0.14 vehicles/meter/lane) than local streets (0.20 vehicles/meter/lane). This reflects the different spacing requirements at different operational speeds and road types. Each link's behavior is governed by a triangular fundamental diagram that relates traffic flow to density, characterized by the free-flow speed, jam density, and resulting capacity.

The model uses a hybrid simulation approach: Mesa's discrete event simulation manages agent decisions and scheduling, while UXsim handles continuous traffic flow dynamics. Synchronization between the two systems occurs at 5-minute intervals, where agents make mode choices based on current network conditions, new vehicle trips are added to UXsim, traffic flow is simulated, and the updated network conditions inform future agent decisions. Network performance data is collected at 15-minute intervals using UXsim's area-based analysis capabilities, allowing for evaluation of both localized congestion effects and network-wide performance metrics.

#### 7.4 Parking
Parking is modeled by tracking the number of parked vehicles in each MRDH region:

- When a car trip starts, a parking space is freed in the origin area.
- When a car trip ends, a parking space is occupied in the destination area.

The `parked_per_area` dictionary is updated in real-time, and the `parked_dict` stores the parking situation over time for later analysis.

#### 7.5 Cost Calculation
Travel costs are calculated differently for each mode:

- Car: Distance-based cost using a fixed price per kilometer
  - `distance * car_price_per_km_variable`
- AV: Initial cost plus distance and time-based costs
  - `av_initial_costs + distance * av_costs_per_km + travel_time * av_costs_per_sec`
- Bike: Assumed to be zero
- Transit: Distance-based cost with a non-linear pricing scheme, simulating real-world transit pricing:
  ```python
  ranges = [(40, 1), (80, .979), (100, .8702), (120, .7),
            (150, .48), (200, .4), (250, .15), (float('inf'), 0)]
  ```
  - In practice, the vast majority of trips are under 40 kilometers, and thus priced at the full rate, but this allows to extend the model further. 

#### 7.6 Value of Time
Each agent's Value of Time is calculated as:

```python
vot_factor = min(np.random.lognormal(mean=-0.1116, sigma=0.4724), 4)
value_of_time = {mode: default_vot[mode] * vot_factor for mode in modes}
```

This creates heterogeneity in how agents value their time, influencing their mode choices. It prevents sharp tipping points in mode choice and allows for more realistic variation in travel preferences. For more details and sources, see the Value of Time data section.

#### 7.7 External Vehicle Load
External vehicle traffic is modeled based on origin-destination matrices:

- Vehicles are added at the start of each hour based on time-of-day probabilities.
- The number of vehicles is scaled by `ext_vehicle_load` factor.
- Origins and destinations are chosen from predefined external and internal areas.

#### 7.8 Scenario & Policy Implementation
The model includes several scenario uncertainties and policy levers that can be adjusted:

##### Scenario uncertainties
1. AV cost factor: Scales the fixed, time based and distance based cost of using autonomous vehicles.
2. AV Value of Time factor: Scales how users perceive time spent in AVs.
3. AV Density factor: Scales the number of AVs that get generated, as a proxy for the space (per person) an AV takes up on the road.
4. Induced demand factor: Scales the overall trip generation rates.

##### Policy levers
1. Congestion pricing:
   - `policy_tarif`: Sets the pricing level.
   - `policy_tarif_time`: Determines when the pricing is active (e.g., peak hours, all day).
   - `policy_area`: Defines the geographical area where the pricing is applied.
2. Speed reduction:
   - `policy_speed_reduction`: Probability of reducing speed on a given road.
   - `policy_area`: Defines the area where speed reductions are applied.

These scenario uncertainties and policies levers can be combined and varied into different scenarios and policies to explore their impacts on the transportation system. The scenarios and policies explored in this research are discussed in [Appendix D](#appendix-d-experimental-setup).

#### 7.9 Journey Management
The `Journey` class encapsulates all information about a single trip:

- It tracks the origin, destination, mode, costs, and timings of each trip.
- For car and AV trips, it interfaces with the UXsim traffic simulation to schedule vehicle movements.
- It handles the logic for trip chaining, ensuring that agents return to their original location and maintaining mode consistency (e.g., if an agent leaves with a car, they must return with a car).

#### 7.10 Data Collection and Analysis
The model collects data at multiple levels:

- Agent level: Individual trip details, mode choices, and costs.
- Network level: Traffic conditions from UXsim (speed, density, flow) for each network link.
- System level: Aggregated metrics like mode shares, total vehicle kilometers traveled, and parking occupancy.

Data is collected at regular intervals and stored for post-simulation analysis. The `process_results` function in the `UrbanModel` class handles the aggregation and storage of this data.


## Appendix B: Assumptions
This appendix lists the most important assumptions made in the model design and implementation.

### Agent behavior
1. Rational decision-making: Agents make mode choices based on minimizing comfort-adjusted perceived costs, including monetary costs and time costs weighted by their value of time, and a comfort factor.
2. Perfect information: Agents have complete knowledge of travel times and costs for all available modes.
3. Heterogeneous value of time: Each agent's value of time is drawn from a lognormal distribution, representing varying sensitivities to travel time, and differs by mode ([KiM 2023](https://www.kimnet.nl/publicaties/publicaties/2023/12/04/nieuwe-waarderingskengetallen-voor-reistijd-betrouwbaarheid-en-comfort)).
4. Trip generation: The number and timing of trips for each agent are determined probabilistically based on hourly trip probabilities derived from [ODiN 2023](https://www.cbs.nl/nl-nl/longread/rapportages/2024/onderweg-in-nederland--odin---2023-onderzoeksbeschrijving).
5. Trip chaining: Agents always return to their origin location after each outbound trip, creating simple two-leg trip chains.
   - ODiN 2022 data showed 43.8% of trips start at home, 43.8% end at home (total 87.6%), and only 12.4% are neither.
6. Mode availability: An agent's available modes depend on car ownership, possession of a driver's license, and the previous leg of their trip chain.
   - Notably, if a car is used for the first leg of a trip, it must be used for the return leg as well.
7. Bicycle ownership: All agents are assumed to have access to a bicycle.
8. No en-route mode switching: Once a mode is chosen for a trip, it cannot be changed during the journey.
9. No trip cancellation: Agents do not cancel trips due to high costs or unavailable modes.
10. No carpooling or ride-sharing: Each car or AV trip represents a single agent.

### Traffic model
1. Mesoscopic simulation: Traffic is modeled at a medium level of detail, balancing computational efficiency with realistic traffic dynamics.
2. Platoon-based representation: Vehicles are grouped into platoons (of 10 by default) for computational efficiency, with each agent representing multiple actual vehicles.
3. Dynamic User Equilibrium: Drivers choose routes based on experienced travel times, updating their choices periodically.
4. Simplified intersection behavior: Detailed intersection dynamics (e.g., traffic signals, turn lanes) are not explicitly modeled.
5. Constant road capacity: Road capacities do not change due to weather, incidents, or other temporary factors.
6. Homogeneous vehicle types: All vehicles are assumed to have the same physical characteristics and performance.
7. External traffic: Traffic entering and leaving the study area is modeled based on fixed origin-destination matrices and time-of-day factors.

### Data
1. Population distribution: Agent locations are based on actual population data at the 4-digit postal code level, as reported by the CBS for 2020 ([CBS-postcode]).
   - In total 991.575 people live in the simulation area.
2. Car ownership and driver's licenses: Distribution of car ownership and driver's licenses is based on 4-digit postal code level data ([CBS-mobility]).
   - On average, 31.5% of agents in the simulation area own a car, and thus have car as a mode option. This varies per postal code area.
3. Road network: The road network is derived from OpenStreetMap data, on September 30, 2024, using [OSMnx] 2.0.0b2. It includes ternary roads and larger roads, with speed limits, lane counts and lengths.
   - The road network contains 1575 nodes and 3328 edges.
4. Travel times and distances: Non-car mode travel times and distances are based on Google Maps Distance Matrix API data ([Google-Maps-API]), on Thursday 2024-09-17 at 08:00 (a normal workday without major construction).
   - Note that cycling and public transit times are relatively stable throughout the day, while car travel times can vary significantly.
5. Trip generation rates: Hourly trip probabilities are derived from the Dutch National Travel Survey ([ODiN 2023]).
6. Origin-destination patterns: Origin-destination lookup is based on matrices from the [V-MRDH] transport model.
   - Only the total values for all modes are used, not the per-mode values, since mode-choice is integrated in the model.
7. Value of Time: Default values of time for different modes are based on Dutch transportation studies ([KiM-valuation]). AV is assumed to be the same as car (and varied in experiments with the AV VOT factor).
   - The default value of times are €10.42 for car, €10.39 for bike, and €7.12 for transit. 
8. Default AV costs are based on own research, as no public data was available. A survey was put out on Reddit, on which a linear regression model was estimated ([Waymo-pricing]).
   - The default AV costs are €3.79 plus €1.41 per kilometer and €0.40 per minute.

### Other
1. Static land use: The model assumes no changes in land use or population distribution during the simulation period.
2. No seasonal variations: The model does not account for seasonal changes in travel behavior or weather conditions.
3. No special events: The impact of large events (e.g., sports matches, festivals) on travel patterns is not considered.
4. Constant fuel/energy prices: The model assumes static prices for fuel and energy throughout the simulation.
5. No technological improvements: The model assumes constant vehicle efficiency and performance over time.
   - AV density and costs can be adjusted to represent technological improvements.
6. Simplified AV behavior: Autonomous vehicles are assumed to operate similarly to human-driven vehicles, with adjustments only to cost structure and value of time.
7. No adaptation of public transit: The public transit system is assumed to remain constant, not adapting to changes in demand or competing modes.

## Appendix C: Limitations
### Agent behavior
The Agent mode-choice model is the most limited part of the model, mainly because of data-availability and computational constraints. Ideally an activity-based model would be used, but this would require carefully designed surveys with large sample sizes, which weren't available.

Some specific limitations include:
1. Limited behavioral complexity: The model does not capture complex decision-making processes, psychological factors, or habitual behaviors that may influence mode choice.
   - Implementing more complex behavioral models needs carefully designed stated-preference (SP) studies, which also collects socio-economical data. Only revealed-preference studies were available, but different to fit to scenarios and modalities that currently do not exist.
2. Lack of sociodemographic factors: Beyond value of time, the model does not consider how factors like age, income, or household composition affect travel behavior.
   - Data for these factors is available, but would only make sense to use with proper stated-preference studies (or other calibrated models).
3. Simplified trip chaining: The model only implements simple two-leg trip chains, not capturing more complex trip patterns (e.g., home-work-shop-home).
   - More complex trip chaining would also require additional data on activity patterns.
4. No long-term adaptation: Agents do not learn or adapt their behavior over time based on experiences.
   - Implementing learning behaviors would require longer simulation periods, for which compute budgets where out of scope for this study.
5. Limited mode options: The model considers only four modes (car, bike, transit, AV), not including options like walking, e-bikes, or shared mobility services.
   - Adding more modes would require additional data and increase the complexity of the mode choice model.
6. Limited social considerations: The model does not account for social influence on mode choice or household-level decision making.
   - Social factors like peer effects and household car sharing could significantly impact AV adoption patterns.
7. No explicit parking behavior: While parking occupancy is tracked, parking availability and search time are not incorporated into mode choice decisions.
   - This could underestimate the full costs of car-based travel, especially in dense urban areas.

One interesting thing to note is that for most metrics, like congestion, it doesn't matter how the agents make their decisions, as long as they are consistent. The model is about the system-level effects of the decisions, rather than the individual decisions themselves. Of course the feedback loops and stabilizing mechanisms would be different for different decision-making models, leading to different system-level outcomes.

Highly recommended for future research is to conduct a stated-preference study, which can be used to calibrate the model to real-world data. Learning mechanisms and an activity-based model would also be beneficial to capture more realistic agent behavior.

### Traffic Model
The traffic model mainly lacks in details on crossings and intersections, which are not specifically modeled. The remainder of the model is relatively detailed, but still has some limitations:

1. Limited network detail: The mesoscopic approach does not capture detailed vehicle interactions or traffic signal operations.
   - A more detailed microscopic simulation would be computationally intensive for a city-scale model.
2. Simplified parking model: Parking is modeled at an aggregate level, not considering specific parking locations or search time. Parking costs were also not included.
   - Detailed parking modeling would require extensive data on parking supply, which wasn't accurately available.
3. No consideration of freight traffic: The model focuses on passenger transport, not explicitly modeling freight movements.
   - Freight transport is a relatively small part of urban traffic, but could be included in future versions.
4. Limited representation of public transit: Transit is modeled simplistically, not capturing details of transit routes, schedules, or capacity constraints.
   - Detailed transit modeling would require integration with a separate transit simulation model.
   - Peak hour capacity constraints and crowding effects are not considered.
5. No modeling of active modes infrastructure: The model does not consider the impact of bicycle lanes or pedestrian infrastructure on mode choice and traffic flow.
   - Bicycle and public transport don't face many delays due to congestion, so the impact of infrastructure is limited.
   - It was found that bicycle travel times are remarkable consistent with distance for bicycle trips (see [travel_time_distance_google.ipynb](..%2Ftravel_api%2Ftravel_time_distance_google.ipynb)), so an explicit model was not deemed necessary as long as the lookup tables have enough detail.
6. Simplified intersection dynamics: The model uses default merge priorities and does not include traffic signal timing or turn lane specifications.
   - While adequate for system-level analysis, this may affect the accuracy of local congestion patterns.
7. Homogeneous vehicle characteristics: All vehicles within a mode are assumed to have identical performance characteristics.
   - In reality, different vehicle types (e.g., electric vs. conventional) could affect traffic flow and mode choice.

### Data
Data availability is always a limitation in ABM models, and this model is no exception. Especially validation data for congestion, mode choice and AV pricing was hard to come by. Some specific limitations include:

1. Temporal specificity of travel time data: Google Maps API data used for non-car modes represents conditions at a specific time, not capturing variations throughout the day.
   - Collecting time-varying data for all origin-destination pairs would be prohibitively expensive (current lookups were 156.25 USD, within a 200 USD free tier).
2. Aggregation of origin-destination data: Trip distribution is based on larger traffic analysis zones used by [V-MRDH], not capturing fine-grained variations in travel patterns.
   - More detailed O-D data was not available. A problem is that the more fine-grained the data, the more sparse it becomes, decreasing the signal-to-noise ratio.
3. Simplified representation of transit costs: The transit cost model uses a simplified distance-based approach, not capturing the complexity of real-world fare systems.
   - Implementing detailed fare structures for all transit operators would require extensive data collection, which was out of scope.
4. Limited validation data: The model lacks comprehensive data for validating results, especially for future scenarios involving autonomous vehicles.
   - Detailed validation data for emerging transportation technologies is inherently limited. Behavior was examined to see if it was plausible, but no real-world data was available to compare to.
5. Static infrastructure data: The road network and transit services are based on a single snapshot, not capturing planned changes or maintenance effects.
   - While major planned infrastructure (like the new A16) was included, smaller changes could affect local travel patterns.
6. Limited calibration data: While mode shares could be validated against ODiN data, detailed validation of traffic patterns was constrained by data availability.
   - Attempts to obtain commercial traffic data for validation were unsuccessful.

### Other
The main other limitation is the lack of long-term dynamics and feedback loops. The model is a static scenario analysis, not capturing how the system might evolve over time. This was a conscious choice in the model scope, since this study was primarily about how the urban transportation system might respond to AV adoption and policy interventions, and how people might make different day-to-day decisions based on these changes.

Some specific limitations include:
1. Static scenario analysis: The model simulates a single day, not capturing longer-term evolving dynamics of AV adoption and system adaptation.
   - Long-term dynamic simulations would require additional assumptions about technology adoption and system changes, increasing uncertainty.
2. Limited policy options: While the model includes some policy levers (congestion pricing, speed reductions), it does not cover the full range of potential policy interventions.
   - Implementing a wider range of policies was consciously avoided, since this study was primarily about the system-level effects of AVs.
3. No feedback between transportation and land use: The model does not capture how changes in the transportation system might influence land use patterns over time.
   - Land use requires long-term simulations and detailed urban planning models, which were out of scope.
4. Limited environmental impact assessment: The model does not directly calculate emissions or other environmental impacts of transportation choices.
   - Adding detailed environmental impact modeling would require additional data on vehicle characteristics and emissions factors. However, the distance traveled by car and AV is available, which is a good proxy for emissions.
5. No consideration of equity impacts: The model does not explicitly address how changes in the transportation system affect different socioeconomic groups.
   - Equity analysis would require more detailed sociodemographic data and additional post-processing of model outputs.
6. Simplified AV implementation: The model treats AVs essentially as cheaper, more comfortable cars, not capturing potential transformative impacts on urban form or travel behavior.
   - The exact impacts of AVs are still uncertain, and more complex representations would require speculative assumptions.
   - Density is used as a proxy for the space an AV takes up on the road and the average number of people in a car. This is a simplification, but a good first-order approximation.
7. Limited geographic scope: The model focuses on the Rotterdam area, potentially missing broader regional or national-level impacts.
   - Expanding the geographic scope would require significantly more data and computational resources. Other regions could be relatively easily added, population and network data is available for the whole of the Netherlands. OD-matrix data would need to be added if going beyond the MRDH area.
8. Weather and seasonal effects: The model does not account for how weather conditions or seasonal patterns affect mode choice and traffic flow.
   - This could be particularly relevant for cycling behavior and AV operations.
9. Time-of-day variations: While trip generation varies by hour, mode characteristics (like transit frequencies) are static throughout the day.
   - This simplification could affect the accuracy of off-peak travel patterns, especially for transit in weekends, evenings, and nights.

## Appendix D: Experimental setup

This appendix describes the experimental setup used in this study. Two main experiments were conducted: a scenario analysis exploring uncertainties in autonomous vehicle (AV) adoption and a policy analysis testing various interventions across different scenarios.

### 1. Scenario Analysis

The scenario analysis employed a full-factorial design to explore four key uncertainties related to the adoption and impact of autonomous vehicles. These uncertainties were represented by the following variables:

1. AV Cost Factor (`av_cost_factor`): Represents the relative cost of using AVs compared to the current cost AVs (as operated by Waymo in Los Angeles in September 2024 ([Waymo-pricing]), see [Appendix B](#appendix-b-assumptions) for more details).
2. AV Value of Time Factor (`av_vot_factor`): Reflects how users perceive time spent in AVs compared to conventional vehicles.
3. AV Density (`av_density`): Represents the space efficiency of AVs on the road compared to conventional vehicles.
4. Induced Demand (`induced_demand`): Reflects the potential increase in overall travel demand (either due to the introduction of AVs or other mobility or macroeconomic factors).

Note that AV density represents the average space a single person transported with an AV takes up on the road (a lower value means more people can be transported with the same road space). How that density is achieved is not relevant for the simulation outcomes, but it can be for interpretation. AV density can be improved by either increasing the average number of people in a car (picking up more people on the way, driving less empty between trips) or taking up less road space (smaller vehicle sizes, faster reaction times, platooning).
The table below shows the values used for each variable in the full-factorial design:

| Variable | Values |
|----------|--------|
| `av_cost_factor` | 1.0, 0.5, 0.25, 0.125 |
| `av_vot_factor` | 1.0, 0.5, 0.25 |
| `av_density` | 1.5, 1.0, 0.5, 0.333333 |
| `induced_demand` | 1.0, 1.25, 1.5 |

This design resulted in a total of 4 × 3 × 4 × 3 = 144 unique combinations, each representing a possible future scenario for AV adoption and its impacts.

The scenario analysis was executed using the [`run_model.py`](../model/run_model.py) script, which implemented the full-factorial design and managed the parallel execution of simulations for each combination of variables.

Other relevant model settings for the scenario analysis included:

- Time step: 5 minutes (1/12 hour)
- Simulation period: 5:00 to 24:00 (19 hours)
- Choice model: Rational value of time
- AVs enabled: Yes
- External vehicle load: 0.8
- UXsim platoon size: 10
- Car comfort factor: 0.5
- Bike comfort factor: 1.33

### 2. Policy Analysis

The policy analysis was designed to test the effectiveness of various policy interventions across different AV adoption scenarios. This analysis used a set of predefined scenarios and policies, as specified in the [`scenarios_policies.py`](../model/scenarios_policies.py) file.

#### 2.1 Scenarios

Eight scenarios were defined, representing different possible futures for AV adoption and its impacts. Table A.2 summarizes these scenarios:

| Scenario Key | Description | `av_cost_factor` | `av_density` | `induced_demand` |
|--------------|-------------|------------------|--------------|------------------|
| 0_current | Current situation | 1.0 | 1.5 | 1.0 |
| 1_moderate_progress | Moderate AV progress | 0.5 | 1.0 | 1.125 |
| 2_extensive_progress | Extensive AV progress | 0.25 | 0.5 | 1.25 |
| 3_extreme_progress | Extreme AV progress | 0.125 | 0.333333 | 1.5 |
| 4_private_race_to_the_bottom | Cheap, inefficient AVs | 0.125 | 1.5 | 1.25 |
| 5_mixed_race_to_the_bottom | Cheap AVs, mixed efficiency | 0.125 | 1.0 | 1.25 |
| 6_shared_race_to_the_bottom | Cheap, efficient AVs | 0.125 | 0.5 | 1.25 |
| 7_dense_progress | Efficient AVs, moderate demand | 0.25 | 0.333333 | 1.125 |

All scenarios used an `av_vot_factor` of 0.5.

#### 2.2 Policies

Nine different policy combinations were tested, varying in their approach to speed reduction, congestion pricing, and geographical scope. Table A.3 summarizes these policies:

| Policy Key | Area | Speed Reduction | Tariff | Tariff Time |
|------------|------|-----------------|--------|-------------|
| 0_no_policy | City | 0 | 0 | Day |
| 1_autoluw_peak | Autoluw | 1 | 5 | Peak |
| 2_autoluw_day | Autoluw | 1 | 5 | Day |
| 3_city_peak | City | 1 | 5 | Peak |
| 4_city_day | City | 1 | 5 | Day |
| 5_city_speed_reduction | City | 1 | 0 | Day |
| 6_city_peak_tarif | City | 0 | 5 | Peak |
| 7_city_day_tarif | City | 0 | 5 | Day |
| 8_all_out | City | 1 | 10 | Day |

Where:
- "Autoluw" refers to a specific low-traffic area within the city ([Rotterdam-verkeerscirculatieplan]), and city indicates the entire city area (all roads in the main network).
- Speed Reduction: The fraction of roads in that area that get a 20 km/h maximum speed reduction (0 meaning 0% of roads, 1 meaning 100% of roads)
- Tariff: Congestion charge in euros per trip, if either the origin or destination is in the area
- Tariff Time: "Peak" = applied during peak hours (7:00-9:00 and 16:00-18:00), "Day" = applied throughout the day (6:00-19:00)

![merged_network_autoluw.svg](img%2Fmerged_network_autoluw.svg)
_Fig D.1: The network with the autoluw area highlighted in green._

The following PC4 areas are within the autoluw area (and thus potentially affected by the policies):

- Rotterdam Centrum (1): [3011, 3016, 3015, 3012, 3014, 3013]
- Delfshaven (2): [3022, 3021, 3023]
- Noord (3): [3039, 3041, 3037, 3032, 3038, 3036, 3035, 3033]
- Kralingen (4): [3031]

AV pricing, if enabled for the autoluw area, will affect about 13% of the agents in the simulation. 130.835 of 991.575 inhabitants live in the autoluw area, of which:
- Rotterdam Centrum (1): 38.705
- Delfshaven (2): 31.410
- Noord (3): 52.420
- Kralingen (4): 8.300

The city area covers the all 125 PC4 areas in the research area and thus all agents.

#### 2.3 Experimental Design

The policy analysis involved running simulations for all combinations of the 8 scenarios and 9 policies, resulting in 72 unique experiments. This was implemented in the [`run_model_2.py`](../model/run_model_2.py) script, which managed the execution of simulations for each scenario-policy combination.

For each combination, the script:
1. Combined the scenario and policy parameters
2. Generated a unique suffix for the output files
3. Checked if the simulation had already been run (to avoid duplication)
4. Executed the simulation if needed

The simulations were run in parallel across multiple cores to improve computational efficiency.

### 3. Data Collection and Analysis

For both the scenario and policy analyses, each simulation run collected the following data:

1. Journey details: Origin, destination, mode, travel time, costs, etc.
2. Traffic conditions: Speed, density, and flow for each network link
3. Parking occupancy over time

This data was saved in various formats (Feather files for journey data, Python pickle files for UXsim and parking data) for subsequent analysis.

The collected data allowed for the evaluation of various metrics, including:
- Mode share distributions
- Network performance (average speeds, congestion levels)
- Parking demand patterns
- Total vehicle kilometers traveled
- Distribution of travel times and costs

These metrics were used to assess the impacts of different AV adoption scenarios and the effectiveness of various policy interventions.

## Appendix E: Additional results
This section contains some additional results that were not included in the main report, but might be interesting for specific audiences.

### 1. Default behavior
![uxsim_data_default_default.png](img%2Fdefault%2Fuxsim_data_default_default.png)
![parked_data_default.png](img%2Fdefault%2Fparked_data_default.png)

### 2. Scenario analysis
#### 2.1. Full mode and mode distance shares

| ![heatmap_mode_share_car.png](..%2Fimg%2Fexp4%2Fheatmap_mode_share_car.png) | ![heatmap_mode_share_bike.png](..%2Fimg%2Fexp4%2Fheatmap_mode_share_bike.png) | ![heatmap_mode_share_transit.png](..%2Fimg%2Fexp4%2Fheatmap_mode_share_transit.png) | ![heatmap_mode_share_av.png](..%2Fimg%2Fexp4%2Fheatmap_mode_share_av.png) |
|-----|-----|-----|-----|
| ![heatmap_mode_distance_share_car.png](..%2Fimg%2Fexp4%2Fheatmap_mode_distance_share_car.png) | ![heatmap_mode_distance_share_bike.png](..%2Fimg%2Fexp4%2Fheatmap_mode_distance_share_bike.png) | ![heatmap_mode_distance_share_transit.png](..%2Fimg%2Fexp4%2Fheatmap_mode_distance_share_transit.png) | ![heatmap_mode_distance_share_av.png](..%2Fimg%2Fexp4%2Fheatmap_mode_distance_share_av.png) |

### 3. Default behavior
#### 3.1. Parking occupancy
![parked_heatmaps_default.png](img%2Fdefault%2Fparked_heatmaps_default.png)


[CBS-mobility]: https://www.cbs.nl/nl-nl/maatwerk/2023/35/auto-s-kilometers-en-rijbewijzen-per-pc4 "CBS data on cars, kilometers driven, and driver's licenses per postcode"
[CBS-postcode]: https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode "CBS geographical data by postcode"
[CBS-statistics]: https://www.cbs.nl/nl-nl/longread/diversen/2023/statistische-gegevens-per-vierkant-en-postcode-2022-2021-2020-2019/bijlagen "CBS statistical data by grid and postcode (2019-2022)"
[CBS-vehicles]: https://www.cbs.nl/nl-nl/maatwerk/2023/24/voertuigen-naar-brandstofsoort-en-postcode-2023 "CBS data on vehicles by fuel type and postcode (2023)"
[Google-Maps-API]: https://developers.google.com/maps/documentation/distance-matrix/overview "Google Maps Distance Matrix API documentation"
[KiM-valuation]: https://www.kimnet.nl/publicaties/publicaties/2023/12/04/nieuwe-waarderingskengetallen-voor-reistijd-betrouwbaarheid-en-comfort "KiM publication on travel time valuation"
[MPN]: https://www.mpndata.nl/ "Netherlands Mobility Panel (MPN) data"
[Mapshaper]: https://mapshaper.org/ "Tool for converting VMRDH areas"
[Mesa]: https://github.com/projectmesa/mesa "Mesa agent-based modeling framework"
[NS-API]: https://apiportal.ns.nl/ "NS (Dutch Railways) API portal"
[Nibud-car-costs]: https://www.nibud.nl/onderwerpen/uitgaven/autokosten/ "Nibud information on car costs"
[ODiN 2022]: https://ssh.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/SS/BXIK2X "Onderweg in Nederland (ODiN) 2022 dataset"
[ODiN 2023]: https://www.cbs.nl/nl-nl/longread/rapportages/2024/onderweg-in-nederland--odin---2023-onderzoeksbeschrijving "Onderweg in Nederland (ODiN) 2023 dataset"
[OSMnx]: https://www.github.com/gboeing/osmnx "OSMnx library for working with OpenStreetMap data"
[OpenStreetMap]: https://www.openstreetmap.org/about "OpenStreetMap data source"
[Train-costs]: https://www.treinonderweg.nl/wat-kost-de-trein.html "Information on train costs in the Netherlands"
[UXsim-original]: https://www.github.com/toruseo/uxsim "Original UXsim repository"
[UXsim]: https://github.com/EwoutH/UXsim/ "UXsim traffic simulation library"
[V-MRDH]: https://www.mrdh.nl/verkeersmodel "MRDH Verkeersmodel (V-MRDH)"
[Waymo-pricing]: https://github.com/EwoutH/Waymo-pricing "Repository for Waymo pricing data"
[Rotterdam-verkeerscirculatieplan]: https://www.rotterdam.nl/verkeerscirculatieplan "Rotterdam's traffic circulation plan"