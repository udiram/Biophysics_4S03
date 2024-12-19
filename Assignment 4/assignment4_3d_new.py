import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
world = 20

def initialize_chain(N, starting_position):
    positionsX = [starting_position[0]]
    positionsY = [starting_position[1]]
    for _ in range(N - 1):
        angle = np.random.uniform(0, 2 * np.pi)
        x = positionsX[-1] + np.cos(angle)
        y = positionsY[-1] + np.sin(angle)
        positionsX.append(x)
        positionsY.append(y)
    return positionsX, positionsY

# Move a single residue
def move(i, positionsX, positionsY):
    N = len(positionsX)
    new_positionsX = positionsX.copy()
    new_positionsY = positionsY.copy()

    if i == 0:  # First residue
        angle = np.random.uniform(0, 2 * np.pi)
        x_new = positionsX[i] + np.cos(angle)
        y_new = positionsY[i] + np.sin(angle)
    elif i == N - 1:  # Last residue
        angle = np.random.uniform(0, 2 * np.pi)
        x_new = positionsX[i] + np.cos(angle)
        y_new = positionsY[i] + np.sin(angle)
    else:  # Intermediate residues
        x_prev, y_prev = positionsX[i - 1], positionsY[i - 1]
        x_next, y_next = positionsX[i + 1], positionsY[i + 1]
        x_mid = (x_prev + x_next) / 2
        y_mid = (y_prev + y_next) / 2
        angle = np.random.uniform(0, 2 * np.pi)
        x_new = x_mid + np.cos(angle)
        y_new = y_mid + np.sin(angle)

    if -world <= x_new <= world and -world <= y_new <= world:
        new_positionsX[i] = x_new
        new_positionsY[i] = y_new

    return new_positionsX, new_positionsY

def determine_location(x, y, thickness, radius):
    """
    Determines whether a point (x, y) is in the endosome, cytosol, membrane, or pore.
    """
    membrane_top = thickness / 2
    membrane_bottom = -thickness / 2

    if membrane_bottom < y < membrane_top:
        if -radius <= x <= radius:
            return "pore"
        else:
            return "membrane"
    elif y >= membrane_top:
        return "endosome"
    else:
        return "cytosol"

# Track compartment changes
def track_compartment_changes(positionsX, positionsY, ticks, thickness, radius):
    """
    Tracks the trajectory of a residue and counts compartment changes.
    """
    residue_index = 0
    y_positions = [positionsY[t][residue_index] for t in range(ticks)]
    x_positions = [positionsX[t][residue_index] for t in range(ticks)]

    compartments = [
        determine_location(x_positions[t], y_positions[t], thickness, radius)
        for t in range(ticks)
    ]

    compartment_changes = sum(
        1 for t in range(1, len(compartments)) if compartments[t] != compartments[t - 1]
    )

    return compartment_changes, y_positions, compartments

def simulate_and_track(N, ticks, starting_position, thickness, radius):
    """
    Simulates Brownian motion and tracks residue movement through compartments.
    """
    positionsX, positionsY = initialize_chain(N, starting_position)
    positionsX_array = [positionsX]
    positionsY_array = [positionsY]

    # Simulate motion
    for _ in tqdm(range(ticks)):
        for i in range(N):
            positionsX, positionsY = move(i, positionsX, positionsY)
        positionsX_array.append(positionsX)
        positionsY_array.append(positionsY)

    compartment_changes, trajectory, compartments = track_compartment_changes(
        positionsX_array, positionsY_array, ticks, thickness, radius
    )

    plt.figure(figsize=(10, 6))
    plt.plot(range(ticks), trajectory, label="Y-Position of Tracked Residue")
    plt.axhline(thickness / 2, color='gray', linestyle='--', label="Membrane Top")
    plt.axhline(-thickness / 2, color='gray', linestyle='--', label="Membrane Bottom")
    plt.xlabel("Time Step")
    plt.ylabel("Y-Position")
    plt.title("Tracked Residue Y-Position Over Time")
    plt.legend()
    plt.grid()
    plt.savefig('3d.png')
    plt.show()

    print(f"Number of Compartment Changes: {compartment_changes}")
    print(f"Final Compartment: {compartments[-1]}")

# Parameters
N = 20  # Number of residues
ticks = 1_000  # Number of time steps
starting_position = [0, 10]  # Start higher in the box
thickness = 2  # Membrane thickness
radius = 3  # Pore radius

simulate_and_track(N, ticks, starting_position, thickness, radius)
