#plotting package for 4S03 assignment 3

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import Rectangle



def animating_residues(positionsX, positionsY, ticks, world, chargesT= None , radius = None , thickness =None):
    fig, ax1 = plt.subplots(figsize = (6,6))

    ax1.set(xlabel = 'x', ylabel = 'y', xlim = [-world, world], ylim = [-world, world]) ##setting up some labels, axis limits
    if thickness != None:
        ax1.axhspan(0, world, facecolor='lightblue', alpha=0.5)
        ax1.axhspan(-world, 0, facecolor = 'lavender', alpha = 0.5)
        r = Rectangle((-world,0), world-radius, thickness, fc='black',ec="black")
        r2 = Rectangle((radius,0), world-radius, thickness, fc='black',ec="black")
        ax1.add_patch(r)
        ax1.add_patch(r2)
    
    if chargesT.all() == None:
        plotter, = ax1.plot([],[],'-o', color ='k')
        ends, = ax1.plot([],[], 'ro')
        begins, =ax1.plot([],[], 'bo')
    else:
        plotter, = ax1.plot([],[], 'k')
        uncharged, = ax1.plot([], [], 'o', color = 'k')
        charged, = ax1.plot([],[], 'o', color = 'g')
        ends, = ax1.plot([],[], 'r')
        begins, =ax1.plot([],[], 'b')
    
    def animate(i):
        if chargesT.all() != None:
            index_charge = np.where(chargesT[:,i]==-1)
            print(index_charge[0][0] == 0)
            index_uncharge = np.where(chargesT[:,i]==0)
            charged.set(xdata =positionsX[index_charge,i], ydata =positionsY[index_charge,i])
            uncharged.set(xdata = positionsX[index_uncharge,i], ydata =positionsY[index_uncharge,i])
            if index_charge[0][0] == 0:
                
                begins.set(xdata = positionsX[0, i], ydata=positionsY[0, i],  marker = 's')
            else:
                begins.set(xdata = positionsX[0, i], ydata=positionsY[0, i],  marker = 'o')
            if index_charge[0][-1] == len(chargesT[:,i])-1:
                ends.set(xdata = positionsX[-1, i], ydata=positionsY[-1, i],  marker = 's')
            else:
                ends.set(xdata = positionsX[-1, i], ydata=positionsY[-1
                                                                           , i],  marker = 'o')
        else:
            ends.set(xdata= positionsX[-1,i], ydata = positionsY[-1,i])
            begins.set(xdata= positionsX[0,i], ydata = positionsY[0,i])
        plotter.set(xdata = positionsX[:,i], ydata =positionsY[:,i])
        


    ani = animation.FuncAnimation(fig, animate, frames=ticks, interval = 60)
    plt.show()
