import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 2000  # number of particles
boxSizeX = 20  # width
boxSizeY = 40  # height
R = 0.5  # particle size
timeStep = 2000  # increased length of the simulation
histogram_bin_count = 20  # histogram bins when calculating the concentration profile
g_effect = 0.1  # reduced gravity effect

# Sedimentation length (modified to be inversely proportional to R^3)
ls = 1 / R**3  # Sedimentation length modified

# Initial concentration
volume_box = boxSizeX * boxSizeY * R  # Volume in arbitrary units
c0 = N / volume_box  # Initial concentration in particles per unit volume

# Function to move particles with adjusted gravity effect
def move_with_gravity_adjusted(x, y, g_effect):
    header = np.random.rand() * 2 * np.pi
    newx = x + 1 / np.sqrt(R) * np.cos(header)
    newy = y + 1 / np.sqrt(R) * np.sin(header) - R * g_effect  # Adjust gravity effect to R * g_effect
    # Reflect particles off the walls if they move out of bounds
    newx = max(0, min(newx, boxSizeX))
    newy = max(0, min(newy, boxSizeY))
    return newx, newy

# Simulate Brownian motion with reduced gravity effect and increased time steps using new ls
particles = np.array([[np.random.rand() * boxSizeX, np.random.rand() * boxSizeY] for _ in range(N)])
positionDataY = []

for _ in range(timeStep):
    for i in range(N):
        particles[i][0], particles[i][1] = move_with_gravity_adjusted(particles[i][0], particles[i][1], g_effect)
    positionDataY.extend(particles[:, 1])

# Create histogram for concentration profile
hist, bin_edges = np.histogram(positionDataY, bins=histogram_bin_count, range=(0, boxSizeY), density=True)
bin_midpoints = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Theoretical concentration profile (c(z) = c0 * exp(-z / ls))
z_values = np.linspace(0, boxSizeY, 100)
c_theoretical = c0 * np.exp(-z_values / ls)

# Plotting the results with modified sedimentation length
plt.figure(figsize=(10, 6))

# Plotting simulated concentration profile
plt.plot(bin_midpoints, hist, label="Simulated Concentration Profile", marker='o')

# Plotting theoretical concentration profile
plt.plot(z_values, c_theoretical / max(c_theoretical) * max(hist), label="Theoretical Concentration Profile", linestyle='--')

plt.xlabel('Height (z)')
plt.ylabel('Concentration (c(z))')
plt.title('Simulated vs. Theoretical Concentration')
plt.legend()
plt.grid()
plt.show()
plt.savefig('q2d.png')
