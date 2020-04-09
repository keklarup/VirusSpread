# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:25:24 2020

@author: Kyle
"""

import VirusABM
import VirusVisuals
import numpy as np

VirusModel = VirusABM.VirusModel
    
def recordStatus(model, storageArrayList=[]):
    """Taking a ABM and recording the status of the agents in the env.
    """
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        #agent_count = len(cell_content)
        possiblePeople=[elm for elm in cell_content]
        locationIllness=[]
        for agent in possiblePeople:
            locationIllness.append(agent.type)
        try:
            agent_sickness = max(locationIllness)
        except:
            agent_sickness = -1
        agent_counts[x][y] = agent_sickness
    storageArrayList.append(agent_counts)
    return storageArrayList


model = VirusModel(1000, 40, 40,  capacityThresh=0.05, dist=0.0, vac=0, vacEff=.85, sickDuration=35,
                      mortalityRateA=.02, mortalityRateB=.1)
hospitalThreshold = len(model.schedule.agents)*.05
T=120
SAL=[]
for i in range(0, T):
    if i%100 == 0:
        print(i)
    SAL=recordStatus(model, storageArrayList=SAL)
    model.step()

#various ways to visualize:
#VirusVisuals.agentPlot(SAL, cmap=None, save=False, saveFolder=None, 
#              display=True, i=9)

VirusVisuals.agentStatusPlot(SAL, T, cmap=None,
                            hospitalThreshold = hospitalThreshold,
                   save=False, saveFolder=None, 
                    display=True, i=T)

#VirusVisuals.combinedVisuals(SAL, T, cmap=None, i=100, 
#                             hospitalThreshold =hospitalThreshold,
#                    modelName='Model visualization', 
#                    save=False, saveFolder=None, display=True)

print('Finish')