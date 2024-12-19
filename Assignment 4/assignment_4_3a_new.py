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

def draw_membrane(ax, thickness, radius):
    """
    Draw the membrane with a pore.
    """
    membrane_top = thickness / 2
    membrane_bottom = -thickness / 2

    # Draw the membrane as rectangles, leaving a pore in the center
    ax.add_patch(plt.Rectangle((-world, membrane_top), world - radius, thickness, color='gray', alpha=0.5))
    ax.add_patch(plt.Rectangle((radius, membrane_top), world - radius, thickness, color='gray', alpha=0.5))

def animate_chain_with_membrane(N, ticks, starting_position, thickness, radius, filename="chain_with_membrane.gif"):
    positionsX, positionsY = initialize_chain(N, starting_position)
    positionsX_array = [positionsX]
    positionsY_array = [positionsY]

    for _ in range(ticks):
        for i in range(N):
            positionsX, positionsY = move(i, positionsX, positionsY)
        positionsX_array.append(positionsX)
        positionsY_array.append(positionsY)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-world, world)
    ax.set_ylim(-world, world)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Brownian Motion with Membrane and Pore")

    draw_membrane(ax, thickness, radius)

    scatter = ax.scatter([], [], c="blue")

    def update(frame):
        scatter.set_offsets(np.c_[positionsX_array[frame], positionsY_array[frame]])
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
thickness = 2  # Membrane thickness
radius = 3  # Pore radius
animate_chain_with_membrane(N, ticks, starting_position, thickness, radius, filename="chain_with_membrane.gif")
