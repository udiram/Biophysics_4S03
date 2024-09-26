######################### A Brownian Motion simulation developed by Carmen Lee for PHYS 4S03 tutorial #1 python v3.6 ##########################


##########################Variables################
N = 2000 #number of particles
boxSizeX = 20 # width
boxSizeY = 40 # height
R = 0.5 #particle size
timeStep = 100 #length of the simulation
histogrambin = 20 #histogram bins when calculating the concentration profile


#################Modules###########################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

####################Initialize#####################
particles = []

for n in range(N):
    x = np.random.rand()*boxSizeX
    y = np.random.rand()*boxSizeY
    particles.append([x, y])

######################Functions###############################
def move(x, y):
    header = np.random.rand()*2*np.pi
    newx = x + 1/np.sqrt(R)*np.cos(header)
    newy = y + 1/np.sqrt(R)*np.sin(header)
    while newx < 0 or newx >= boxSizeX or newy < 0 or newy >= boxSizeY: #keeps particles inside the box by resetting the header direction to keep it within the box
        header = np.random.rand()*2*np.pi
        newx = x + 1/np.sqrt(R)*np.cos(header)
        newy = y + 1/np.sqrt(R)*np.sin(header)
    #reset header for the next time step
    return([newx, newy])

#######################progressing the simulation###########################

positionDataX = [] #saves the group x data for each time step
positionDataY = [] #saves the group y data for each time step
for t in range(timeStep):
    x = []
    y = []
    for turtle in range(N):
        particles[turtle] = move(particles[turtle][0], particles[turtle][1])
        x.append(particles[turtle][0])
        y.append(particles[turtle][1])
    positionDataX.append(x)
    positionDataY.append(y)

##################Animating the simulation #################

fig, (ax1, ax2) = plt.subplots(ncols=2)
fig.subplots_adjust(wspace = 0.3)

ax1.set(xlim = (0, boxSizeX), ylim=(0, boxSizeY), title = 'Brownian motion')
ax2.set(xlim =  (0, N/10), ylim =(0, boxSizeY), xlabel = 'Concentration', ylabel = 'Elevation', title = 'Concentration profile')

plotter, = ax1.plot([], [], 'bo', markersize = R)
plotterConc, = ax2.plot([], [], 'k-')

def animate(i):
    plotter.set(xdata =positionDataX[i], ydata =positionDataY[i])
    hist = np.histogram(positionDataY[i], histogrambin) # creates a histogram of all data
    plotterConc.set(xdata =hist[0] , ydata = hist[1][0:-1]+0.5*boxSizeY/histogrambin) #the histogram function labels the outside of the bins that it counts from. Here, I've shifted the y data by half of the bin width to even out the profile
    

ani = animation.FuncAnimation(fig, animate, frames=timeStep)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60)
ani.save('Browniantest.mp4', writer=writer) # this should save the video in the working directory
plt.show()


