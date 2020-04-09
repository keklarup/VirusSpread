# -*- coding: utf-8 -*-
"""
Agent Based Modeling (ABM) for disease spread using mesa
Created on Thu Apr  9 10:04:11 2020

@author: Kyle
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np

class VirusModel(Model):
    """For modeling disease progression in a community."""
    
    def __init__(self, N, width, height, capacityThresh=0.05, dist=0, vac=0, vacEff=1.0, sickDuration=20, 
                mortalityRateA=.02, mortalityRateB=.1):
        self.num_agents = N
        self.capacityThresh = capacityThresh
        self.sickDuration = sickDuration;
        self.mortalityRateA = mortalityRateA
        self.mortalityRateB = mortalityRateB
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = Person(i, self)
            #a.distance=dist
            if np.random.random()<=vac:
                a.vaccine=vacEff
                a.type=2
            #if np.random.random()<=dist:
                #a.distance=1
            a.distance=dist
            if i%500 == 0:
                a.sick = 1
                a.type = 3
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()
        

class Person(Agent):
    """ Agent in the model,
        with various attributes like sickness and movement"""
    
    Agent.capacityOverload=0
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.sick = 0
        self.inHospital = 0
        self.sicktime = 0
        self.dead = 0
        self.protected = 0
        self.type=0
        ###### types #####
        # -1 - empy square
        # 0 - healthy, can get disease
        # 1 - healthy, immune
        # 2 - healthy, vaccinated
        # 3 - sick, not in hospital
        # 4 - sick, in hospital
        # 5 - dead
        self.sickenedOthers=-1
        self.distance=0
        self.vaccine=0
        
    def move(self):
        """Agent movement function. Don't move if dead"""
        if self.dead==0 and self.distance < np.random.random():
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=True)
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def give_sickness(self):
        """Passing sickness to other agents if in same grid"""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            #other = self.random.choice(cellmates)
            for cellmate in cellmates:
                if cellmate.protected == 0 and cellmate.sick!=1:
                    if np.random.random() >= cellmate.vaccine:
                        cellmate.sick=1;
                        cellmate.type=3
                        cellmate.sickenedOthers=0
                        self.sickenedOthers=self.sickenedOthers+1
    
    def sickness_timeline(self):
        """Tracking progression of disease in an agent.
           Uses a simple counter to decide when to possibly go to hospital
           and when to possibly die"""
        if self.sick == 1:
            self.sicktime=self.sicktime+1
    
    def sickness_endgame(self):
        """Deciding outcome of illness using some pseudorandom calculations"""
        if self.sicktime >= self.model.sickDuration * .7: #at 70% of sickness timeline
            if np.random.random()<=20:
                self.inHospital = 1
                self.type = 4
                self.distance = 1
            else:
                self.inHospital = 0
                self.type = 3
        if self.sicktime == self.model.sickDuration:
            if self.capacityOverload == 0 and self.inHospital == 1:
                survived = np.random.random() > self.model.mortalityRateA
            elif self.capacityOverload == 1 and self.inHospital == 1:
                survived = np.random.random() > self.model.mortalityRateB
            else:
                survived = True
            if survived:
                self.protected = 1
                self.sick = 0
                self.type = 1
                self.distance=0
                self.inHospital = 0
            else:
                self.dead = 1
                self.protected=1
                self.sick = 0
                self.type = 5
                self.inHospital = 0
                

    def step(self):
        """Agent moves"""
        self.move()
        if self.sick == 1:
            self.give_sickness()
            self.sickness_timeline()
            self.sickness_endgame()
        if sum([a.inHospital for a in self.model.schedule.agents]) \
                > self.model.num_agents*self.model.capacityThresh:
            self.capacityOverload = 1
        else:
            self.capacityOverload = 0
