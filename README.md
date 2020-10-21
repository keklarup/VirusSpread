# Agent Based Modeling
## Using ABM to model disease spread within a population
----
### Defining Agent Based Modeling
#### What: 
  * Simulating how autonomous agents act and interact within an environment
#### Why: 
  * Generate insight into what may be driving observed emergent phenomena
  * Generate insight into how small-scale changes can have large-scale effects
  
((insert link to visual))
 
Above simulation of disease spread through a community of 1,200 agents in a simple, 2D environment
----
### Agents
* Simple ‘robots’ following a sequence of rules / actions
* Can carry a set of internal parameters.
### Environment
* The word in which the Agents reside
* In all this work, environment is a simple, 2D grid.

((insert link))

Above: Single agent moving in simple, 2d grid environment. Agent progresses through different disease states (color coded) which impact mobility in environment
----
### Simulation
* Simulation over a sequence of time steps
* Each agent takes turns performing programmed actions
* Each agent in this model preforms the following actions:
   * Move to 1 of 9 neighboring locations
   * If sick and moved to same location as another agent, pass the illness with some probability 
   * If sick for long enough become hospitalized, recover and/or die

((insert link to visual))

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

((insert visual))

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
((insert visual))
Above: ABM simulation that produces realistic Rnot values, hospitalization rates, death rates, etc.
----
### Changing Parameters
#### Simulating how changes to model parameters effect outcomes

#### Parameters to study:
* Movement Reduction
* Mask Wearing
* Vaccination
----


----
Work in progress. VirusSpread.py can be used to run ABM, but still needs polishing for making interaction with visuals better.
