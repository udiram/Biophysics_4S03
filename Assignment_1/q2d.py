import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 2000  # number of particles
boxSizeX = 20  # width
boxSizeY = 40  # height
R = 0.5  # particle size
timeStep = 500  # length of the simulation
histogram_bin_count = 20  # histogram bins when calculating the concentration profile
g_effect = 1  # gravity effect

# Parameters for sedimentation length calculation
kT = 1.38e-23 * 300  # Boltzmann constant * Temperature (Joule)
R_meters = 0.5e-6  # Particle radius in meters (0.5 micrometers)
d = 1.05e3  # Density of particle (kg/m^3)
df = 1e3  # Fluid density (kg/m^3)
g = 9.81  # Acceleration due to gravity (m/s^2)

# Initial concentration
volume_box = boxSizeX * boxSizeY * R  # Volume in arbitrary units
c0 = N / volume_box  # Initial concentration in particles per unit volume

# Sedimentation length (ls)
ls = kT / ((4 / 3) * np.pi * R_meters**3 * (d - df) * g)

# Initialize particles
particles = np.array([[np.random.rand() * boxSizeX, np.random.rand() * boxSizeY] for _ in range(N)])

# Function to move particles with gravity effect
def move_with_gravity(x, y, g_effect):
    header = np.random.rand() * 2 * np.pi
    newx = x + 1 / np.sqrt(R) * np.cos(header)
    newy = y + 1 / np.sqrt(R) * np.sin(header) - g_effect
    while newx < 0 or newx >= boxSizeX or newy < 0 or newy >= boxSizeY:
        header = np.random.rand() * 2 * np.pi
        newx = x + 1 / np.sqrt(R) * np.cos(header)
        newy = y + 1 / np.sqrt(R) * np.sin(header) - g_effect
    return newx, newy

# Simulate Brownian motion with gravity effect
positionDataY = []

for _ in range(timeStep):
    for i in range(N):
        particles[i][0], particles[i][1] = move_with_gravity(particles[i][0], particles[i][1], g_effect)
    positionDataY.extend(particles[:, 1])

# Create histogram for concentration profile
hist, bin_edges = np.histogram(positionDataY, bins=histogram_bin_count, range=(0, boxSizeY), density=True)
bin_midpoints = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Theoretical concentration profile (c(z) = c0 * exp(-z / ls))
z_values = np.linspace(0, boxSizeY, 100)
c_theoretical = c0 * np.exp(-z_values / ls)

# Plotting the results
plt.figure(figsize=(10, 6))

# Plotting simulated concentration profile
plt.plot(bin_midpoints, hist, label="Simulated Concentration Profile", marker='o')

# Plotting theoretical concentration profile
plt.plot(z_values, c_theoretical / max(c_theoretical) * max(hist), label="Theoretical Concentration Profile", linestyle='--')

plt.xlabel('Height (z)')
plt.ylabel('Concentration')
plt.title('Comparison of Simulated and Theoretical Concentration Profiles')
plt.legend()
plt.grid()
plt.show()

# Display calculated sedimentation length and initial concentration
print(f"Sedimentation length (ls): {ls}")
print(f"Initial concentration (c0): {c0}")