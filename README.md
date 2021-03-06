# Agent Based Modeling
## Using ABM to model disease spread within a population
----
### Defining Agent Based Modeling
#### What: 
  * Simulating how autonomous agents act and interact within an environment
#### Why: 
  * Generate insight into what may be driving observed emergent phenomena
  * Generate insight into how small-scale changes can have large-scale effects
  
![1200](https://github.com/keklarup/VirusSpread/blob/master/Visuals/1200Agents-optimized.gif)
 
Above simulation of disease spread through a community of 1,200 agents in a simple, 2D environment
----
### Agents
* Simple ‘robots’ following a sequence of rules / actions
* Can carry a set of internal parameters.
### Environment
* The word in which the Agents reside
* In all this work, environment is a simple, 2D grid.

![single agent](https://github.com/keklarup/VirusSpread/blob/master/Visuals/SingleAgent_200914.gif)

Above: Single agent moving in simple, 2d grid environment. Agent progresses through different disease states (color coded) which impact mobility in environment
----
### Simulation
* Simulation over a sequence of time steps
* Each agent takes turns performing programmed actions
* Each agent in this model preforms the following actions:
   * Move to 1 of 9 neighboring locations
   * If sick and moved to same location as another agent, pass the illness with some probability 
   * If sick for long enough become hospitalized, recover and/or die
![example timesteps](https://github.com/keklarup/VirusSpread/blob/master/Visuals/TimestepsExample.png)

Above: 4 timesteps of a small ABM with 5 agents on a 5x5 grid, showing the infection of a second agent.

----
### Infinite choice in parameters:
#### What actions can affect disease spread in a population?

Possible parameters:
* Number of people in population
* Frequency of interactions/encounters
* How long people are infectious
* Virulence of the disease
* Reinfection rate
* Hospitalization rate
* …

Possible Agent disease states:
* Healthy and unexposed
* Healthy and vaccinated
* Healthy and recovered
* Sick and mobile
* Sick and immobile (hospitalized)
* Dead
----
### Setting up a simulation
* With so many knobs to turn, first challenge is creating a <b>realistic simulation</b>.
* Good rule of thumb: find model parameters which replicate current measurables before trying to develop insight into how to change measurables 

![10](https://github.com/keklarup/VirusSpread/blob/master/Visuals/10Agents-optimized.gif) 

![100](https://github.com/keklarup/VirusSpread/blob/master/Visuals/100Agents-optimized.gif)

![500](https://github.com/keklarup/VirusSpread/blob/master/Visuals/500Agents-optimized.gif)

Above: all parameters held constant except for number of agents, which greatly impacts outcome

----
### Constraining parameters with reality:

Possible parameters:
* Number of people in population
* Frequency of interactions/encounters
* How long people are infectious
* Virulence of the disease
* Reinfection rate
* Hospitalization rate
* …

<b>Simplify by using basic reproductive number as metric to create original simulation that mimics real world value.</b>
* Population Density: 16%
* Sickness duration: 35
* Chance to infect on encounter: 100%
* Change of hospitalization: 20%
* Immunity after infection
#### Results in: Rnot around 3.2
(Measured by average number of Agents infected by patient 0 after running simulation 300 times)
----
![R3.2](https://github.com/keklarup/VirusSpread/blob/master/Visuals/movementRed0.0_stats-optimize.gif)

Above: ABM simulation that produces realistic Rnot values, hospitalization rates, death rates, etc.
----
### Changing Parameters
#### Simulating how changes to model parameters effect outcomes

#### Parameters to study:
* Movement Reduction
* Mask Wearing
* Vaccination
----
### Movement Reduction (Lockdowns)

#### 0% Movement Reduction
![Movement0](https://github.com/keklarup/VirusSpread/blob/master/Visuals/movementRed0.0-optimize.gif)

#### 50% Movement Reduction
Each agent has a 50% chance to skip the move routine each time step.
![Movement5](https://github.com/keklarup/VirusSpread/blob/master/Visuals/movementRed0.5-optimize.gif)
----
### Effects of lockdowns
* 30% Movement Reduction
  * Ro = 2.83 +/- 0.12
  * 89% get sick, 2% die
* 60% Movement Reduction
  * Ro = 2.0 +/- 0.12
  * 28% get sick, 1% die
* 90% Movement Reduction
  * Ro = 0.94 +/- 0.11
  * 2% get sick, 0% die
  
(R values calculated by running ABM simulation 100 times and taking mean. Error calculated by bootstrapping 100 datasets from original and finding standard deviation)

![lockdowns](https://github.com/keklarup/VirusSpread/blob/master/Visuals/lockdowns.png)
----
### Nonlinear effects of Lockdowns
* Minor effects in changes well away from the inflection point
  * Minor movement reductions ineffective
  * Difference between complete lockdown and 80% movement reduction negligible
* Large Variance at inflection point

![nonlinearLockdowns](https://github.com/keklarup/VirusSpread/blob/master/Visuals/exampleLockdownR3.2.png)

Data generated by running ABM simulation 20 times for each variable setting, then using the average and std deviation of the outcomes to generate figure and error bars
----
### Mask Wearing
#### (reduces chance of infection per interaction)
 
#### 0% population mask wearing
![masks0](https://github.com/keklarup/VirusSpread/blob/master/Visuals/masks0.0-optimized.gif)

### 50% population mask wearing
Each mask wearing agent reduces the chance of passing on the infection per encounter
![masks5](https://github.com/keklarup/VirusSpread/blob/master/Visuals/masks0.5-optimized.gif)

----
### Effects of Masks
Mask wearing reduces the odds of getting sick by 65% 1,2,3
  * 1 https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)31142-9/fulltext
  * 2 https://www.webmd.com/lung/news/20200710/face-masks-reduce-covid-risk-by-65-percent
  * 3 https://www.ucsf.edu/news/2020/06/417906/still-confused-about-masks-heres-science-behind-how-face-masks-prevent
* 30% population wearing mask
  * Ro = 2.51 +/- 0.16
  * 74% get sick, 2% die
* 60% population wearing mask
  * Ro = 1.73 +/- 0.17
  * 49% get sick, 1% die
* 90% population wearing mask
  * Ro = 1.03 +/- 0.10
  * 2% get sick, 0% die

![masks](https://github.com/keklarup/VirusSpread/blob/master/Visuals/masks.png)

----
### Nonlinear effects of mask wearing
* Inflection point around 50-60% use rate
  * Rare mask wearing ineffective
* Large Variance at inflection point

![nonlinearMasks](https://github.com/keklarup/VirusSpread/blob/master/Visuals/exampleMasksR3.2.png)

Data generated by running ABM simulation 20 times for each variable setting, then using the average and std deviation of the outcomes to generate figure and error bars

----
### Vaccine
#### (Makes portion of population immune)

#### 0% population has vaccine

![vac0](https://github.com/keklarup/VirusSpread/blob/master/Visuals/vaccine0.0-optimized.gif)

#### 50% population has vaccine
Vaccinated agents have some chance to be immune to the disease

![vac5](https://github.com/keklarup/VirusSpread/blob/master/Visuals/vaccine0.5-optimized.gif)
----
### Effects of a vaccine
Minimum vaccine effectiveness: 50%
* 30% population vaccinated
  * Ro = 2.77 +/- 0.16
  * 77% get sick, 2% dead
* 60% population vaccinated
  * Ro = 2.54 +/- 0.14
  * 47% get sick, 1% dead
* 90% population vaccinated
  * Ro = 1.85 +/- 0.13 
  * 26% get sick, 0% die
  
![vaccines](https://github.com/keklarup/VirusSpread/blob/master/Visuals/vaccines.png)
----
### Linear effects of a vaccine
* Linear reduction in fraction of population infected
* Simple reduction of susceptible population

![linearVacs](https://github.com/keklarup/VirusSpread/blob/master/Visuals/exampleVaccinationR3.2.png)

Data generated by running ABM simulation 20 times for each variable setting, then using the average and std deviation of the outcomes to generate figure and error bars
----
### Comparing masks/vaccine and movement reduction
Gain insight into best mix of control options for best outcome

![maskMovement](https://github.com/keklarup/VirusSpread/blob/master/Visuals/heatmap_moveMask.png)

![maskVac](https://github.com/keklarup/VirusSpread/blob/master/Visuals/heatmap_vacMask.png)

----
### Modeling software
* NetLogo
* SpaDES or RnetLogo (R)
* Mesa (Python)

![netLogo](https://github.com/keklarup/VirusSpread/blob/master/Visuals/NetLogoExamples.png)



----
Work in progress. VirusSpread.py can be used to run ABM, but still needs polishing for making interaction with visuals better.
