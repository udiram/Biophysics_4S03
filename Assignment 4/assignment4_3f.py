import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# World boundary
world = 20

# Initialize a chain of residues in a 2D polymer structure
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

# Determine residue location
def determine_location(x, y, thickness, radius):
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

# Assign charges dynamically based on location and pH
def assign_charges_dynamic(positionsX, positionsY, pKa, thickness, radius):
    charges = []
    for x, y in zip(positionsX, positionsY):
        location = determine_location(x, y, thickness, radius)
        if location == "endosome":
            pH = 5  # Endosome pH
        elif location == "cytosol":
            pH = 7  # Cytosol pH
        else:
            charges.append(0)  # No charge in the membrane or pore
            continue
        probability = 1 / (1 + 10 ** (pKa - pH))
        charge = -1 if np.random.rand() < probability else 0
        charges.append(charge)
    return charges

# Move a single residue in a polymer
def move_with_energy_dynamic(i, positionsX, positionsY, charges, thickness, radius, kT=1):
    N = len(positionsX)
    x_old, y_old = positionsX[i], positionsY[i]
    new_positionsX = positionsX.copy()
    new_positionsY = positionsY.copy()

    # Propose a new position
    angle = np.random.uniform(0, 2 * np.pi)
    x_new = x_old + np.cos(angle)
    y_new = y_old + np.sin(angle)

    # Maintain polymer structure
    if i > 0:
        x_prev, y_prev = new_positionsX[i - 1], new_positionsY[i - 1]
        if np.sqrt((x_new - x_prev) ** 2 + (y_new - y_prev) ** 2) > 1.5:
            return positionsX, positionsY
    if i < N - 1:
        x_next, y_next = new_positionsX[i + 1], new_positionsY[i + 1]
        if np.sqrt((x_new - x_next) ** 2 + (y_new - y_next) ** 2) > 1.5:
            return positionsX, positionsY

    # Boundary constraints
    if not (-world <= x_new <= world and -world <= y_new <= world):
        return positionsX, positionsY

    # Accept the move
    new_positionsX[i] = x_new
    new_positionsY[i] = y_new
    return new_positionsX, new_positionsY

# Simulate and plot center of mass y-position
def simulate_and_plot_y_position(N, ticks, starting_position, thickness, radius, pKa, filename="translocation_y_position.gif", kT=1):
    positionsX, positionsY = initialize_chain(N, starting_position)
    charges = assign_charges_dynamic(positionsX, positionsY, pKa, thickness, radius)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-world, world)
    ax.set_ylim(-world, world)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Polymer Translocation with Proton Gradient")

    # Draw membrane and pore
    membrane_top = thickness / 2
    membrane_bottom = -thickness / 2
    ax.fill_betweenx([membrane_bottom, membrane_top], -world, -radius, color="gray", alpha=0.5)
    ax.fill_betweenx([membrane_bottom, membrane_top], radius, world, color="gray", alpha=0.5)

    scatter, = ax.plot(positionsX, positionsY, '-o', color="blue", label="Polymer")
    counter_text = ax.text(-world + 1, world - 1, f"Residues in Cytosol: 0", fontsize=12, color="red")

    # Track center of mass (y-coordinate)
    y_positions_center_of_mass = []

    def update(frame):
        nonlocal positionsX, positionsY, charges

        # Move all residues and assign charges dynamically
        for i in range(N):
            positionsX, positionsY = move_with_energy_dynamic(i, positionsX, positionsY, charges, thickness, radius, kT)
        charges = assign_charges_dynamic(positionsX, positionsY, pKa, thickness, radius)

        # Calculate and track center of mass y-coordinate
        y_center_of_mass = np.mean(positionsY)
        y_positions_center_of_mass.append(y_center_of_mass)

        # Update polymer positions
        scatter.set_data(positionsX, positionsY)
        counter_text.set_text(f"Center of Mass Y: {y_center_of_mass:.2f}")

        return scatter, counter_text

    # Save animation
    writer = PillowWriter(fps=30)
    writer.setup(fig, filename, dpi=100)

    for t in range(ticks):
        update(t)
        writer.grab_frame()

    writer.finish()
    plt.close()
    print(f"Animation saved as {filename}")

    # Plot center of mass y-coordinate over time
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(y_positions_center_of_mass)), y_positions_center_of_mass, label="Center of Mass (Y)")
    plt.axhline(membrane_top, color="gray", linestyle="--", label="Membrane Top")
    plt.axhline(membrane_bottom, color="gray", linestyle="--", label="Membrane Bottom")
    plt.xlabel("Time Step")
    plt.ylabel("Y Position (Center of Mass)")
    plt.title("Center of Mass Y-Position Over Time")
    plt.legend()
    plt.grid()
    plt.savefig('3f.png')
    plt.show()

# Parameters
N = 20  # Number of residues
ticks = 1000  # Number of time steps
starting_position = [0, 10]  # Start higher in the box
thickness = 2  # Membrane thickness
radius = 3  # Pore radius
pKa = 6  # Residue pKa

# Run simulation and plot y-position of center of mass
simulate_and_plot_y_position(N, ticks, starting_position, thickness, radius, pKa, filename="translocation_y_position.gif")
