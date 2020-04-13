# -*- coding: utf-8 -*-
"""
ABM virus visuals
Created on Thu Apr  9 10:16:47 2020

@author: Kyle
"""
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import os
import tempfile
from datetime import datetime
import imageio

def agentPlot(storageArrayList, cmap=None, save=False, saveFolder=None, 
              display=False, i=0):
    """Generate a plot of the environment grid.
       Expects ABM to have already been run and status of every grid point
       (which will encode status of every agent) to be saved in an array.
       Each time step is also in array, and which time step to visualize
       is set by i.
       cmap needs to be defined to provide color coding for agent status."""
    if cmap ==None:
        cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                      'blue', 'orange','red', 'black'])
    storedArray=storageArrayList[i]
    plt.figure(figsize=[8,8])
    plt.pcolormesh(storedArray, cmap=cmap, vmin=-1,vmax=5)
    #plt.colorbar()
    plt.axis('off')
    plt.tight_layout()
    if save==True:
        plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(i)))
    if display == True:
        plt.show()
    #plt.close()
    return plt
    
def agentStatusPlot(agent_status, steps, cmap=None, hospitalThreshold = None,
                    save=False, saveFolder=None, 
                    display=False, i=0):
    """Generates various high level visuals of the progression of the
    disease through the population. Expects """
    
    if cmap ==None:
        cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                      'blue', 'orange','red', 'black'])
    i=steps
    healthy=np.count_nonzero(agent_status.unstack().to_numpy() == 0,axis=1)[:i]
    recovered=np.count_nonzero(agent_status.unstack().to_numpy() == 1,axis=1)[:i]
    vaccinated=np.count_nonzero(agent_status.unstack().to_numpy() == 2,axis=1)[:i]
    walkingSick=np.count_nonzero(agent_status.unstack().to_numpy() == 3,axis=1)[:i]
    hospital=np.count_nonzero(agent_status.unstack().to_numpy() == 4,axis=1)[:i]
    dead=np.count_nonzero(agent_status.unstack().to_numpy() == 5,axis=1)[:i]

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=[12,8])
    ax1.bar(range(len(healthy)), dead, width=1.0, color='black', label='dead')
    ax1.bar(range(len(healthy)), hospital, width=1.0, 
            bottom=dead, 
            color='red', label='hospitalized')
    ax1.bar(range(len(healthy)), walkingSick, width=1.0, 
            bottom=dead+hospital, 
            color='orange', label='walking sick')
    ax1.bar(range(len(healthy)), vaccinated, width=1.0, 
            bottom=dead+hospital+walkingSick, 
            color='blue', label='vaccinated')
    ax1.bar(range(len(healthy)), healthy, width=1.0,
            bottom=dead+hospital+walkingSick+vaccinated, 
            color='lightblue', label='healthy')
    ax1.bar(range(len(healthy)), recovered, width=1.0,
            bottom=dead+hospital+walkingSick+vaccinated+healthy, 
            color='green', label='recovered')
    ax1.legend(bbox_to_anchor=[1.,1], fontsize=12);
    ax1.set_ylabel('Population', size=18);
    ax1.set_title('Effect of Virus on Population Over Time',size=20)
    ax2.plot(walkingSick, color='orange', label='walking sick')
    ax2.plot(hospital, color='red', label='hospitalized')
    if hospitalThreshold:
        ax2.axhline(y=hospitalThreshold, 
                linestyle='--',color='gray', label='capacity')
    ax2.set_ylabel('Number of sick');
    ax2.set_title('Number of Sick Over Time', size=20)
    ax2.legend(bbox_to_anchor=[1.,1], fontsize=12);
    ax3.plot(dead, color='black', label='dead');
    ax3.set_xlabel('Time Steps',size=18)
    ax3.set_ylabel('Number of deaad');
    ax3.set_title('Number of Dead Over Time', size=20)
    ax3.legend(bbox_to_anchor=[1.,1], fontsize=12);
    plt.xlim([0,steps])
    plt.tight_layout();
    if save==True:
        plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(i)))
    if display==True:
        plt.show()
    #plt.close()
    return fig

def combinedVisuals(SAL, agent_status, cmap=None, i=0, 
                    hospitalThreshold = None,
                    modelName='Model visualization', 
                    save=False, saveFolder=None, display=False):
    """Combines a few different visuals into a single large image."""
    if not cmap:
        cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                      'blue', 'orange','red', 'black'])
    storedArray=SAL[i]
    healthy=np.count_nonzero(agent_status.unstack().to_numpy() == 0,axis=1)[:i]
    recovered=np.count_nonzero(agent_status.unstack().to_numpy() == 1,axis=1)[:i]
    vaccinated=np.count_nonzero(agent_status.unstack().to_numpy() == 2,axis=1)[:i]
    walkingSick=np.count_nonzero(agent_status.unstack().to_numpy() == 3,axis=1)[:i]
    hospital=np.count_nonzero(agent_status.unstack().to_numpy() == 4,axis=1)[:i]
    dead=np.count_nonzero(agent_status.unstack().to_numpy() == 5,axis=1)[:i]

    fig = plt.figure(figsize=[16,8])
    gs = fig.add_gridspec(3, 5)
    ax4 = fig.add_subplot(gs[0:3, 0:3])
    ax3 = fig.add_subplot(gs[2, 3:])
    ax1 = fig.add_subplot(gs[0, 3:], sharex=ax3)
    ax2 = fig.add_subplot(gs[1, 3:], sharex=ax3)
    ax4.pcolormesh(storedArray, cmap=cmap, vmin=-1,vmax=5)
    ax4.axis('off')
    ax4.set_title('Simulation', size=18)
    ax1.bar(range(len(healthy)), dead, width=1.0, color='black', label='dead')
    ax1.bar(range(len(healthy)), hospital, width=1.0, bottom=dead, color='red',
            label='hospitalized')
    ax1.bar(range(len(healthy)), walkingSick, width=1.0, bottom=dead+hospital, 
            color='orange', label='walking sick')
    ax1.bar(range(len(healthy)), vaccinated, width=1.0, 
            bottom=dead+hospital+walkingSick, color='blue', label='vaccinated')
    ax1.bar(range(len(healthy)), healthy, width=1.0, 
            bottom=dead+hospital+walkingSick+vaccinated, 
            color='lightblue', label='healthy')
    ax1.bar(range(len(healthy)), recovered, width=1.0, 
            bottom=dead+hospital+walkingSick+vaccinated+healthy, 
            color='green', label='recovered')
    ax1.legend(bbox_to_anchor=[1.,1], fontsize=12);
    ax1.set_ylabel('Population', size=18);
    ax1.set_title('Population Status Over Time',size=20)
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2.plot(walkingSick, color='orange', label='walking sick')
    ax2.plot(hospital, color='red', label='hospitalized')
    if hospitalThreshold:
        ax2.axhline(y=hospitalThreshold, linestyle='--',
                color='gray', label='capacity')
    ax2.set_ylabel('Number of sick',size=18);
    ax2.set_title('Number of Sick Over Time', size=20)
    ax2.legend(bbox_to_anchor=[1.,1], fontsize=12);
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3.plot(dead, color='black', label='dead');
    ax3.set_xlabel('Time Steps',size=18)
    ax3.set_ylabel('Number of deaad',size=18);
    ax3.set_title('Number of Dead Over Time', size=20)
    ax3.legend(bbox_to_anchor=[1.,1], fontsize=12);
    plt.suptitle('%s\nTime Step %s'%(modelName, i), size=24)
    fig.tight_layout(rect=[0, 0.03, 1, 0.9])
    if save==True:
        plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(i)))
    if display == True:
        plt.show()
    plt.close()

def generateGIF(SAL, agent_status, NumSteps, cmap=None, stepSkip=2, 
                saveFolder=os.getcwd(),modelName='ABM Simulation', 
                GIFname='ABM_sim', datestamp=True, fps = 10,
                hospitalThreshold = None):
    if not cmap:
        cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                      'blue', 'orange','red', 'black'])
    print("Starting to generate frames for GIF...")
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as f:
        for i in range(1, len(SAL)):
            if i%stepSkip == 0: #saving only every stepSkip frame for the GIF
                combinedVisuals(SAL, agent_status, cmap,i=i, 
                                hospitalThreshold = hospitalThreshold,
                                modelName=modelName.strip()+' ',
                                save=True, saveFolder=f, display=False)
        print("frames generated. Making GIF...")
        if datestamp:
            date = datetime.today().date().strftime('%y%m%d')
        images = []
        fileNums = [int(elm.split('_')[1].split('.png')[0]) for elm in os.listdir(f) if '.png' in elm]
        fileNums = sorted(fileNums)
        for num in fileNums:
            file_name = 'step_%s.png'%(num)
            file_path = os.path.join(f, file_name)
            images.append(imageio.imread(file_path))
        imageio.mimsave(os.path.join(saveFolder,'%s_%s.gif'%(GIFname, date)),images,fps=fps)
        print("GIF complete!")