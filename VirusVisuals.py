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

class visuals():

    def agentPlot(self, storageArrayList, cmap=None, save=False, saveFolder=None, 
                  display=False, i=0, fig=None, axs=None):
        """Generate a plot of the environment grid.
           Expects ABM to have already been run and status of every grid point
           (which will encode status of every agent) to be saved in an array.
           Each time step is also in array, and which time step to visualize
           is set by i.
           cmap needs to be defined to provide color coding for agent status."""
        if cmap ==None:
            cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                          [elm/250 for elm in [72, 169, 171]], 'orange','red', 'black'])
        storedArray=storageArrayList[i]
        
        if axs == None:
            fig, (ax1) = plt.subplots(1, figsize=[8,8])
        else:
            ax1=axs[0]
        #plt.figure(figsize=[8,8])
        ax1.pcolormesh(storedArray, cmap=cmap, vmin=-1,vmax=5)
        # #plt.colorbar()
        ax1.axis('off')
        plt.tight_layout()
        if save==True:
            plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(i)))
        if display == True:
            plt.show()
        #plt.close()
        #return fig

    def agentStatusPlot(self, agent_status, steps, cmap=None, hospitalThreshold = None,
                        save=False, saveFolder=None, 
                        display=False,
                        fig = None,
                        axs=None):
        """Generates various high level visuals of the progression of the
        disease through the population. Expects """

        agent_status = agent_status[['type']]; #hotfix for updated code elsewhere
        if cmap ==None:
            cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                          [elm/250 for elm in [72, 169, 171]], 'orange','red', 'black'])
        i = agent_status.index[-1][0]+1
        #i=steps
        healthy=np.count_nonzero(agent_status.unstack().to_numpy() == 0,axis=1)[:i]
        recovered=np.count_nonzero(agent_status.unstack().to_numpy() == 1,axis=1)[:i]
        vaccinated=np.count_nonzero(agent_status.unstack().to_numpy() == 2,axis=1)[:i]
        walkingSick=np.count_nonzero(agent_status.unstack().to_numpy() == 3,axis=1)[:i]
        hospital=np.count_nonzero(agent_status.unstack().to_numpy() == 4,axis=1)[:i]
        dead=np.count_nonzero(agent_status.unstack().to_numpy() == 5,axis=1)[:i]
        
        if axs == None:
            fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=[12,8])
        else:
            ax1=axs[0]; ax2=axs[1]; ax3=axs[2]
        ax1.bar(range(len(healthy)), dead, width=1.0, color='black', label='dead')
        ax1.bar(range(len(healthy)), hospital, width=1.0, 
                bottom=dead, 
                color='red', label='hospitalized')
        ax1.bar(range(len(healthy)), walkingSick, width=1.0, 
                bottom=dead+hospital, 
                color='orange', label='walking sick')
        ax1.bar(range(len(healthy)), vaccinated, width=1.0, 
                bottom=dead+hospital+walkingSick, 
                color=[elm/250 for elm in [72, 169, 171]], label='vaccinated')
        ax1.bar(range(len(healthy)), healthy, width=1.0,
                bottom=dead+hospital+walkingSick+vaccinated, 
                color='lightblue', label='healthy')
        ax1.bar(range(len(healthy)), recovered, width=1.0,
                bottom=dead+hospital+walkingSick+vaccinated+healthy, 
                color='green', label='recovered')
        ax1.set_ylabel('Population', size=12);
        ax1.set_title('Effect of Virus on Population Over Time',size=20)
        ax2.plot(walkingSick, color='orange', label='walking sick')
        ax2.plot(hospital, color='red', label='hospitalized')
        if hospitalThreshold:
            print(hospitalThreshold)
            ax2.axhline(y=hospitalThreshold, 
                    linestyle='--',color='gray', label='capacity')
        ax2.set_ylabel('Number of sick');
        ax2.set_title('Number of Sick Over Time', size=20)
        ax3.plot(dead, color='black', label='dead');
        ax3.set_xlabel('Time Steps',size=18)
        ax3.set_ylabel('Number of deaad');
        ax3.set_title('Number of Dead Over Time', size=20)

        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        ax1.axvline(x=steps, color='black',alpha=.25,linewidth=7)
        ax2.axvline(x=steps, color='black',alpha=.25,linewidth=7)
        ax3.axvline(x=steps, color='black',alpha=.25,linewidth=7)
        
        #plt.xlim([0,steps])
        plt.xlim([0,i])
        #plt.tight_layout();
        if save==True:
            plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(steps)))
        if display==True:
            plt.show()
        #plt.close()
        #return fig

    def combinedVisuals(self, SAL, agent_status, cmap=None, i=0, 
                            hospitalThreshold = None,
                            modelName='Model visualization', 
                            save=False, saveFolder=None, display=False):
        """Combines a few different visuals into a single large image."""


        fig = plt.figure(figsize=[16,8])
        gs = fig.add_gridspec(3, 5)
        ax4 = fig.add_subplot(gs[0:3, 0:3])
        ax3 = fig.add_subplot(gs[2, 3:])
        ax1 = fig.add_subplot(gs[0, 3:], sharex=ax3)
        ax2 = fig.add_subplot(gs[1, 3:], sharex=ax3)
        self.agentPlot(SAL, i=i, fig=fig, axs=[ax4])
        self.agentStatusPlot(agent_status, i, fig=fig, axs=(ax1, ax2, ax3), cmap=cmap, hospitalThreshold=hospitalThreshold)

        plt.suptitle('%s\nTime Step %s'%(modelName, i), size=24)
        fig.tight_layout(rect=[0, 0.03, 1, 0.9])
        if save==True:
            plt.savefig(os.path.join(os.getcwd(), saveFolder, 'step_%s.png'%(i)))
        if display == True:
            plt.show()
        #plt.close()
        #return fig

    def generateGIF(self, SAL, agent_status, NumSteps, visualFunction='all', cmap=None, stepSkip=1, 
                    saveFolder=os.getcwd(),modelName='ABM Simulation', 
                    GIFname='ABM_sim', datestamp=True, fps = 10,
                    hospitalThreshold = None):
        if not cmap:
            cmap = colors.ListedColormap(['white','lightblue','lightgreen', 
                                          [elm/250 for elm in [72, 169, 171]], 'orange','red', 'black'])
        print("Starting to generate frames for GIF...")
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as f:
            for i in range(0, NumSteps):
                if i%stepSkip == 0: #saving only every stepSkip frame for the GIF
                    if visualFunction == 'all' and i != 0:
                        self.combinedVisuals(SAL, agent_status, i = i,
                                             cmap=None,
                                            hospitalThreshold = None,#hospitalThreshold,
                                            modelName=modelName.strip()+' ',
                                            save=True, saveFolder=f, display=False)
                    elif visualFunction == 'animation':
                        self.agentPlot(SAL, cmap=cmap, save=True, saveFolder=f, display=False, i = i)
                    elif visualFunction == 'graphs':
                        self.agentStatusPlot(agent_status, i, cmap=cmap, 
                                           hospitalThreshold=hospitalThreshold, 
                                           save=True, saveFolder=f, display=False)
                plt.close()
            print("frames generated. Making GIF...")
            images = []
            fileNums = [int(elm.split('_')[1].split('.png')[0]) for elm in os.listdir(f) if '.png' in elm]
            fileNums = sorted(fileNums)
            for num in fileNums:
                file_name = 'step_%s.png'%(num)
                file_path = os.path.join(f, file_name)
                images.append(imageio.imread(file_path))
            imageio.mimsave(os.path.join(saveFolder,'%s.gif'%(GIFname)),images,fps=fps)
            print("GIF complete!")