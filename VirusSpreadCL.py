# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:25:24 2020

@author: Kyle
"""

import VirusABM
#import VirusVisuals
import numpy as np
#import os
import argparse

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

def runModel(N, X, Y, capacityThresh, dist, vac, vacEff, sickDuration, mortalityRateA, mortalityRateB, T,
             NstartSick=1,  masked = 0, maskEff = 0.65):
    #print("Setting up model...")
    model = VirusModel(N, X, Y,  
                       capacityThresh=capacityThresh, 
                       dist=dist, 
                       vac=vac, 
                       vacEff=vacEff, 
                       masked = masked, 
                       maskEff = maskEff,
                       sickDuration=sickDuration,
                       mortalityRateA=mortalityRateA, 
                       mortalityRateB=mortalityRateB,
                       numStartSick = NstartSick)
    
    #print("Model running. Every 100th timestep will print out...")
    SAL=[]
    for i in range(0, T):
        #if i%100 == 0:
        #    print(i)
        SAL=recordStatus(model, storageArrayList=SAL)
        model.step()
    agent_status=model.datacollector.get_agent_vars_dataframe()
    
    return SAL, agent_status

def main():
    
    runModel(N, X, Y, capacityThresh, dist, vac, vacEff, 
             masked, maskEff,
             sickDuration, mortalityRateA, mortalityRateB, T)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('envSize', help='Size of environment: format: "X, Y"', default = '20,20')
    parser.add_argument('numAgents', help='Number of Agents: format: "X"', default = '100')
    parser.add_argument('hospCap', help='threshold for fraction of hospitalized agents before mortality goes up', default = '0.05')
    parser.add_argument('moveRed', help='movement reduction fraction', default = '0.0')
    parser.add_argument('vacFract', help='fraction of agents vaccinated', default = '0.0')
    parser.add_argument('vacEff', help='vaccine effectiveness', default = '0.5')
    parser.add_argument('masked', help = "Fraction of population wearing a mask", default = 0.0)
    parser.add_argument('maskEff', help = "fraction mask wearing reduces risk of infection", default = 0.65)
    parser.add_argument('sickDuration', help='number of timesteps agent is sick', default = '35')
    parser.add_argument('hospChance', help='fraction of sick who become hospitalized',default='0.25')
    parser.add_argument('mortalityRateA', help='disease mortality rate for hospitalized agents while hospitalized fraction under hospCap', default = '0.02')
    parser.add_argument('mortalityRateB', help='disease mortality rate for hospitalized agents while hospitalized fraction above hospCap', default = '0.1')
    parser.add_argument('modelTimeSteps', help='number of timesteps to model', default = '100')
    #parser.add_argument('reviewBeforeVisuals', help='Option to pause script and review before generating visuals and/or saving results', default = 'false')
    #parser.add_argument('makeGif', help='Generate GIF of simulation', default = 'false')
    #parser.add_argument('gifFeatures', help='Option to choose what visuals are in GIF', default = 'all')
    #parser.add_argument('gifFPS', help='number of frames per second in gif', default = '10')
    #parser.add_argument('gifSkips', help='Number of timesteps to skip when making GIF', default = '1')
    #parser.add_argument('gifSaveFolder', help='Folder path to save Gif', default = os.getcwd())
    #parser.add_argument('gifSaveName', help='filename to save Gif', default = 'ABM_sim')
    #parser.add_argument('gifTitle', help='title for Git animation', default='ABM Simulation')
    args = parser.parse_args()

    X, Y = [int(elm) for elm in args.envSize.split(',')]
    N = int(args.numAgents)
    capacityThresh = float(args.hospCap)*N
    dist = float(args.moveRed)
    vac = float(args.vacFract)
    vacEff = float(args.vacEff)
    mask = float(args.maskFract)
    maskEff = float(args.maskEff)
    sickDuration = int(args.sickDuration)
    mortalityRateA = float(args.mortalityRateA)
    mortalityRateB = float(args.mortalityRateB)
    T = int(args.modelTimeSteps)
    #visualReview = args.reviewBeforeVisuals
    #makGif = args.makeGif
    #gifFeatures = args.gifFeatures
    #gifFPS = int(args.gifFPS)
    #stepSkip = args.gifSkips
    #gifSaveFolder = args.gifSaveFolder
    #gifSaveName = args.gifSaveName
    #saveName = os.path.join(gifSaveFolder, gifSaveName)
    #gifTitle = args.gifTitle
    
    
    main(args.name)