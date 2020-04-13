# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:25:24 2020

@author: Kyle
"""

import VirusABM
import VirusVisuals
import numpy as np
import os

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

print("Please provide parameters for ABM model. Leave blank for defaults:")
print('Size of environment: format: "X, Y" default: 20,20')
answer = input()
if answer == '':
    X, Y = (20,20)
else:
    X, Y = [int(elm) for elm in answer.split(',')]
print('Number of Agents: format: "X", default: 100')
answer = input()
if answer == '':
    N = 100
else:
    N = int(answer)
print("""Model parameters...""")
print('capacityThreshold (default .05) fraction of hosp. agents before mortality goes up')
answer = input()
if answer == '':
    capacityThresh = 0.05
else:
    capacityThresh = float(answer)*N
print('dist (default 0.0) movement reduction fraction')
answer = input()
if answer == '':
    dist = 0.0
else:
    dist = float(answer)
print('vac (default 0.0) fraction of agents vaccinated')
answer = input()
if answer == '':
    vac = 0.0
else:
    vac = float(answer)
print('vacEff (default 0.85) vaccine effectiveness')
answer = input()
if answer == '':
    vacEff = 0.85
else:
    vacEff = float(answer)
print('sickDuration (default 35) number of time steps an agent will be sick')
answer = input()
if answer == '':
    sickDuration = 35
else:
    sickDuration = int(answer)
print('mortalityRateA (default 0.02) mortality rate below hospital capacity')
answer = input()
if answer == '':
    mortalityRateA = 0.02
else:
    mortalityRateA = float(answer)
print('mortalityRateB (default 0.10) mortality rate after hospital capacity')
answer = input()
if answer == '':
    mortalityRateB = 0.1
else:
    mortalityRateB = float(answer)

print("Setting up model...")
model = VirusModel(N, X, Y,  
                   capacityThresh=capacityThresh, 
                   dist=dist, 
                   vac=vac, 
                   vacEff=vacEff, 
                   sickDuration=sickDuration,
                   mortalityRateA=mortalityRateA, 
                   mortalityRateB=mortalityRateB)
#hospitalThreshold = capacityThresh
print("Number of timesteps for model run (default: 100)")
answer = input()
if answer == '':
    T = 100
else:
    T = int(answer)

print("Model running. Every 100th timestep will print out...")
SAL=[]
for i in range(0, T):
    if i%100 == 0:
        print(i)
    SAL=recordStatus(model, storageArrayList=SAL)
    model.step()
agent_status=model.datacollector.get_agent_vars_dataframe()
print("Model complete! Visualize?")

print("Visualize progression in population? (Y/N)")
answer = input()
if answer.upper() == 'Y':
    VirusVisuals.agentStatusPlot(agent_status, T, cmap=None,
                        hospitalThreshold = capacityThresh,
                   save=False, saveFolder=None, 
                    display=True, i=T)
print("Generate GIF of model run? (Y/N)")
answer = input()
if answer.upper() == 'Y':
    print("Provide parameters for GIF...")
    print("frames per second (default 10):")
    answer = input()
    if answer == '':
        fps = 10;
    else:
        fps = int(answer)
    print('number of steps in model to skip (default 1)')
    answer = input()
    if answer =='':
        stepSkip = 1
    else:
        stepSkip = int(answer)
    print("Save location (default: current working directory)")
    answer = input()
    if answer =='':
        saveFolder = os.getcwd()
    else:
        saveFolder = str(answer)
    print("model name (default: ABM Simulation)")
    answer = input()
    if answer =='':
        modelName = 'ABM Simulation'
    else:
        modelName = str(answer)
    print('GIF file name (default: ABM_sim)')
    answer = input()
    if answer == '':
        GIFname = 'ABM_sim'
    else:
        GIFname = answer
    print('Datestamp file (default True)')
    answer = input()
    if answer =='':
        datestamp = True
    else:
        datestamp = bool(answer)
    print("Generating GIF")
    VirusVisuals.generateGIF(SAL, agent_status, T, 
                             cmap=None, stepSkip=stepSkip, 
                             saveFolder=saveFolder,modelName=modelName, 
                             GIFname=GIFname, datestamp=datestamp, fps = fps)
    print("Generated GIF!")
    
print('Finish')