######################### A Brownian Motion simulation developed by Carmen Lee for PHYS 4S03 tutorial #1 python v3.6 ##########################

########################## Variables ################
N = 200  # Reduced number of particles
boxSizeX = 20  # Width
boxSizeY = 40  # Height
R = 0.5  # Particle size
timeStep = 200  # Reduced length of the simulation
histogrambin = 20  # Histogram bins when calculating the concentration profile

################# Modules ###########################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

#################### Initialize #####################
# Initial positions for both normal and centrifuge simulations
particles_normal = np.random.rand(N, 2) * [boxSizeX, boxSizeY]
particles_centrifuge = np.copy(particles_normal)

###################### Functions ###############################
def move_particles(particles, g_effect):
    headers = np.random.rand(N) * 2 * np.pi
    particles[:, 0] += 1 / np.sqrt(R) * np.cos(headers)
    particles[:, 1] += 1 / np.sqrt(R) * np.sin(headers) - g_effect

    # Ensure particles stay within bounds
    particles[:, 0] = np.clip(particles[:, 0], 0, boxSizeX)
    particles[:, 1] = np.clip(particles[:, 1], 0, boxSizeY)

####################### Progressing the simulation ###########################

positionDataX_normal = []  # Saves the group x data for each time step (normal gravity)
positionDataY_normal = []  # Saves the group y data for each time step (normal gravity)
positionDataX_centrifuge = []  # Saves the group x data for each time step (centrifuge)
positionDataY_centrifuge = []  # Saves the group y data for each time step (centrifuge)

for t in tqdm(range(timeStep)):
    # Update positions for normal gravity particles
    move_particles(particles_normal, g_effect=1)
    positionDataX_normal.append(particles_normal[:, 0].copy())
    positionDataY_normal.append(particles_normal[:, 1].copy())

    # Update positions for centrifuge particles
    move_particles(particles_centrifuge, g_effect=1000)
    positionDataX_centrifuge.append(particles_centrifuge[:, 0].copy())
    positionDataY_centrifuge.append(particles_centrifuge[:, 1].copy())

################## Animating the simulation #################

fig, (ax1, ax2) = plt.subplots(ncols=2)
fig.subplots_adjust(wspace=0.3)

ax1.set(xlim=(0, boxSizeX), ylim=(0, boxSizeY), title='Brownian Motion: Normal vs Centrifuge')
ax2.set(xlim=(0, N / 10), ylim=(0, boxSizeY), xlabel='Concentration', ylabel='Elevation', title='Concentration Profile')

plotter_normal, = ax1.plot([], [], 'bo', markersize=R, label='Normal Gravity')
plotter_centrifuge, = ax1.plot([], [], 'ro', markersize=R, alpha=0.5, label='Centrifuge (1000x Gravity)')
ax1.legend()

plotterConc_normal, = ax2.plot([], [], 'k-', label='Normal Gravity')
plotterConc_centrifuge, = ax2.plot([], [], 'r-', label='Centrifuge (1000x Gravity)')
ax2.legend()

def animate(i):
    # Update particle positions for normal and centrifuge
    plotter_normal.set_data(positionDataX_normal[i], positionDataY_normal[i])
    plotter_centrifuge.set_data(positionDataX_centrifuge[i], positionDataY_centrifuge[i])

    # Update concentration profiles
    hist_normal = np.histogram(positionDataY_normal[i], bins=histogrambin, range=(0, boxSizeY))
    plotterConc_normal.set_data(hist_normal[0], hist_normal[1][:-1] + 0.5 * boxSizeY / histogrambin)

    hist_centrifuge = np.histogram(positionDataY_centrifuge[i], bins=histogrambin, range=(0, boxSizeY))
    plotterConc_centrifuge.set_data(hist_centrifuge[0], hist_centrifuge[1][:-1] + 0.5 * boxSizeY / histogrambin)

    return plotter_normal, plotter_centrifuge, plotterConc_normal, plotterConc_centrifuge

ani = animation.FuncAnimation(fig, animate, frames=timeStep, blit=True)

# Save the animation
ani.save('Brownian_vs_Centrifuge_optimized.gif', writer='pillow', fps=10)

plt.show()
