import numpy as np
import matplotlib.pyplot as plt

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

def move_with_energy(i, positionsX, positionsY, charges, thickness, radius, kT=1):
    """
    Attempts to move a residue with energy considerations for charged residues in the pore.
    """
    N = len(positionsX)
    x_old, y_old = positionsX[i], positionsY[i]
    new_positionsX = positionsX.copy()
    new_positionsY = positionsY.copy()

    angle = np.random.uniform(0, 2 * np.pi)
    x_new = x_old + np.cos(angle)
    y_new = y_old + np.sin(angle)

    if not (-world <= x_new <= world and -world <= y_new <= world):
        return positionsX, positionsY  # Reject move outside the world

    old_location = determine_location(x_old, y_old, thickness, radius)
    new_location = determine_location(x_new, y_new, thickness, radius)

    if charges[i] == -1:  # Negatively charged residue
        if old_location == "pore" and new_location != "pore":
            delta_E = -1  # Leaving the pore
        elif old_location != "pore" and new_location == "pore":
            delta_E = 1  # Entering the pore
        else:
            delta_E = 0  # No energy change
    else:  # Neutral residue
        delta_E = 0

    if delta_E > 0 and np.random.rand() >= np.exp(-delta_E / kT):
        return positionsX, positionsY  # Reject the move based on energy

    new_positionsX[i] = x_new
    new_positionsY[i] = y_new
    return new_positionsX, new_positionsY

def simulate_with_energy(N, ticks, starting_position, thickness, radius, pH, pKa, kT=1):
    """
    Simulates Brownian motion with energy considerations for charged residues in the pore.
    """
    positionsX, positionsY = initialize_chain(N, starting_position)
    positionsX_array = [positionsX]
    positionsY_array = [positionsY]

    probability = 1 / (1 + 10 ** (pKa - pH))
    charges = (np.random.rand(N) < probability).astype(int) * -1  # Charges: -1 or 0

    for _ in range(ticks):
        for i in range(N):
            positionsX, positionsY = move_with_energy(i, positionsX, positionsY, charges, thickness, radius, kT)
        positionsX_array.append(positionsX)
        positionsY_array.append(positionsY)

    residue_index = 0
    trajectory = [positionsY_array[t][residue_index] for t in range(len(positionsY_array))]

    plt.figure(figsize=(10, 6))
    plt.plot(range(ticks + 1), trajectory, label="Y-Position of Tracked Residue")
    plt.axhline(thickness / 2, color='gray', linestyle='--', label="Membrane Top")
    plt.axhline(-thickness / 2, color='gray', linestyle='--', label="Membrane Bottom")
    plt.xlabel("Time Step")
    plt.ylabel("Y-Position")
    plt.title("Tracked Residue Y-Position Over Time (with Energy Considerations)")
    plt.legend()
    plt.grid()
    plt.savefig('3e.png')
    plt.show()

    final_location = determine_location(positionsX[residue_index], positionsY[residue_index], thickness, radius)
    print(f"Final Compartment: {final_location}")

N = 20  # Number of residues
ticks = 1000  # Number of time steps
starting_position = [0, 10]  # Start higher in the box
thickness = 2  # Membrane thickness
radius = 3  # Pore radius
pH = 7  # World pH
pKa = 7  # Residue pKa
kT = 1  # Thermal energy factor

simulate_with_energy(N, ticks, starting_position, thickness, radius, pH, pKa, kT)
