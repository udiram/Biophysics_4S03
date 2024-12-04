######################### A Brownian Motion simulation developed by Carmen Lee for PHYS 4S03 tutorial #1 python v3.6 ##########################

#######################Variables###################
N = 100 #number of residues
world = 20 # sets up a world that is a 2*world grid
starting_position = [0,10]
########################Importing required modules##########################
import numpy as np
import matplotlib.pyplot as plt

########################Functions##########################################



#######################Set up residues#####################

positionsX = [starting_position[0]] #x, y of the 0th residue, we are initializing the list here with the location of the first points
positionsY = [starting_position[1]] 
for m in range(N-1):
    header = np.random.random()*np.pi*2 #random float between 0 and 1, multiplied by 2*np.pi to give angles up to 360 degrees
    x = positionsX[m]+np.cos(header)
    y = positionsY[m]+np.sin(header)
    positionsX.append(x)
    positionsY.append(y)

##########################Plotting############
fig, ax = plt.subplots(figsize = (6,6)) #setting the figure size
ax.set(xlabel = 'x', ylabel = 'y', xlim = [-world, world], ylim = [-world, world]) ##setting up some labels, axis limits
ax.plot(positionsX, positionsY, '-o', color = 'k')#plotting the position of the residues
ax.plot(positionsX[0], positionsY[0], 'rs')
ax.plot(positionsX[-1], positionsY[-1], 'bs')
plt.show()


#####################################animation###########
'''you can call the pre-written animation section here by uncommenting the lines down below this comment block!
# it has the format where it NEEDS 1. an array that is N x ticks for the horizontal position, 2. the same for the vertical position, 3. the number of time steps, 4. the world size. 
chargesT is an optional input: once you have calculated the charges in part 2 of the assignment, then you can pass a N x ticks array into this function to visualize the charges changing
in the final part of the assignment, you'll be creating a pore in a membrane and you'll need to create variables to set the pore radius (integer) and the membrane thickness (integer). Once you do this, you'll be able to visualise the membrane by passing these to the function'''



from plotting_package import animating_residues
# animating_residues(positionsXarray, positionsYarray, ticks, world, chargesT, radius, thickness)
animating_residues(np.array(positionsX), np.array(positionsY), N, world, chargesT = [np.random.choice([-1,0,1], N) for i in range(N)], radius = 5, thickness = 2)

