import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

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

def assign_charges(pH, pKa, N):
    """
    Assign charges (-1 or 0) to each residue based on the probability.
    """
    probability = 1 / (1 + 10 ** (pKa - pH))  # Henderson-Hasselbalch equation
    charges = np.random.rand(N) < probability  # Randomly assign based on probability
    return charges.astype(int) * -1  # Convert boolean to -1 or 0

def update_charges(positionsX, pH, pKa):
    """
    Update the charges of residues dynamically based on their position.
    """
    N = len(positionsX)
    return assign_charges(pH, pKa, N)

def pick(N, positionsX, positionsY, pH, pKa):
    charges = assign_charges(pH, pKa, N)
    for _ in range(N):  # Randomly pick N residues
        i = np.random.randint(0, len(positionsX))
        positionsX, positionsY = move(i, positionsX, positionsY)
    charges = update_charges(positionsX, pH, pKa)
    return positionsX, positionsY, charges

def animate_chain_with_charges(N, ticks, starting_position, pH, pKa, filename="chain_with_charges.gif"):
    positionsX, positionsY = initialize_chain(N, starting_position)
    charges = assign_charges(pH, pKa, N)
    positionsX_array = [positionsX]
    positionsY_array = [positionsY]
    charges_array = [charges]

    for _ in range(ticks):
        positionsX, positionsY, charges = pick(N, positionsX, positionsY, pH, pKa)
        positionsX_array.append(positionsX)
        positionsY_array.append(positionsY)
        charges_array.append(charges)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-world, world)
    ax.set_ylim(-world, world)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Brownian Motion with Charges")

    scatter = ax.scatter([], [], c=[], cmap="cool", vmin=-1, vmax=0)

    def update(frame):
        scatter.set_offsets(np.c_[positionsX_array[frame], positionsY_array[frame]])
        scatter.set_array(charges_array[frame])
        return scatter,

    writer = PillowWriter(fps=10)
    writer.setup(fig, filename, dpi=100)

    for t in range(len(positionsX_array)):
        update(t)
        writer.grab_frame()

    writer.finish()
    plt.close()
    print(f"Animation saved as {filename}")

N = 20  # Number of residues
ticks = 50  # Number of time steps
starting_position = [0, 10]  # Start higher in the box
pH = 7  # World pH
pKa = 7  # Residue pKa
animate_chain_with_charges(N, ticks, starting_position, pH, pKa, filename="chain_with_charges.gif")
