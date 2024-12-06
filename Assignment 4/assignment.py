import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Constants and parameters
N = 10  # Number of residues
ticks = 1000  # Number of time steps
world = 10  # Size of the 2D world
pH_cytosol = 7
pH_endosome = 5
pKa = 7
membrane_thickness = 2
pore_radius = 3
kT = 1.0  # Boltzmann constant times temperature

# Initialize positions and charges
positionsX = np.random.uniform(-world, world, N)
positionsY = np.random.uniform(-world, world, N)
charges = np.zeros(N)
positionsXarray = np.zeros((N, ticks))
positionsYarray = np.zeros((N, ticks))
chargesarray = np.zeros((N, ticks))


# Helper functions
def charge_probability(pH, pKa):
    Ka = 10 ** -pKa
    H = 10 ** -pH
    return Ka / (Ka + H)


def assign_charges(charges, pH, pKa):
    prob = charge_probability(pH, pKa)
    for i in range(len(charges)):
        charges[i] = -1 if np.random.rand() < prob else 0
    return charges


def location(x, y, membrane_thickness, pore_radius):
    if abs(y) < membrane_thickness / 2:
        if abs(x) < pore_radius:
            return "pore"
        else:
            return "membrane"
    elif y >= membrane_thickness / 2:
        return "cytosol"
    else:
        return "endosome"


def move(i, positionsX, positionsY, world, membrane_thickness, pore_radius):
    xi, yi = positionsX[i], positionsY[i]
    theta = np.random.uniform(0, 2 * np.pi)
    new_x = xi + np.cos(theta)
    new_y = yi + np.sin(theta)

    # Check boundaries
    if abs(new_x) > world or abs(new_y) > world:
        return positionsX, positionsY  # Reject move

    # Check location constraints
    loc = location(new_x, new_y, membrane_thickness, pore_radius)
    if loc == "membrane":
        return positionsX, positionsY  # Reject move

    if loc == "pore" and charges[i] == -1:
        delta_E = 1  # Energy cost
        if np.random.rand() > np.exp(-delta_E / kT):
            return positionsX, positionsY  # Reject move

    # Accept move
    positionsX[i], positionsY[i] = new_x, new_y
    return positionsX, positionsY


def update_charges(charges, positionsX, positionsY, pKa, pH_cytosol, pH_endosome, membrane_thickness, pore_radius):
    for i in range(len(charges)):
        current_loc = location(positionsX[i], positionsY[i], membrane_thickness, pore_radius)
        current_pH = pH_cytosol if current_loc == "cytosol" else pH_endosome
        charges[i] = -1 if np.random.rand() < charge_probability(current_pH, pKa) else 0
    return charges


# Main simulation loop
for t in range(ticks):
    for _ in range(N):  # Move residues
        i = np.random.randint(0, N)
        positionsX, positionsY = move(i, positionsX, positionsY, world, membrane_thickness, pore_radius)

    # Update charges
    charges = update_charges(charges, positionsX, positionsY, pKa, pH_cytosol, pH_endosome, membrane_thickness,
                             pore_radius)

    # Store data for visualization
    positionsXarray[:, t] = positionsX
    positionsYarray[:, t] = positionsY
    chargesarray[:, t] = charges


# Visualization and saving animation
def animate(frame):
    plt.clf()
    for i in range(N):
        color = 'green' if chargesarray[i, frame] == -1 else 'black'
        shape = 's' if i == 0 or i == N - 1 else 'o'
        plt.scatter(positionsXarray[i, frame], positionsYarray[i, frame], c=color, marker=shape)
    plt.xlim(-world, world)
    plt.ylim(-world, world)
    plt.title(f"Time step: {frame}")


fig = plt.figure()
animation = FuncAnimation(fig, animate, frames=ticks, interval=50)

# Save the animation as a GIF
output_file = "ProteinTranslocation.gif"
animation.save(output_file, writer=PillowWriter(fps=20))
print(f"Animation saved as {output_file}")