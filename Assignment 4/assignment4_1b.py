import numpy as np
import matplotlib.pyplot as plt

# Define the world boundary
world = 20


# Initialize a chain of residues in a 2D space
def initialize_chain(N, starting_position):
    """
    Initialize a chain of residues with random positions around the starting point.
    """
    positionsX = [starting_position[0]]
    positionsY = [starting_position[1]]
    for _ in range(N - 1):
        angle = np.random.uniform(0, 2 * np.pi)
        x = positionsX[-1] + np.cos(angle)
        y = positionsY[-1] + np.sin(angle)
        positionsX.append(x)
        positionsY.append(y)
    return positionsX, positionsY


# Function to move a single residue
def move(i, positionsX, positionsY):
    """
    Moves the residue at index i randomly while respecting distance constraints
    and ensuring the residue stays within world boundaries.
    """
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

        # Calculate midpoint between adjacent residues
        x_mid = (x_prev + x_next) / 2
        y_mid = (y_prev + y_next) / 2

        angle = np.random.uniform(0, 2 * np.pi)
        x_new = x_mid + np.cos(angle)
        y_new = y_mid + np.sin(angle)

    # Enforce boundary constraints
    if -world <= x_new <= world and -world <= y_new <= world:
        new_positionsX[i] = x_new
        new_positionsY[i] = y_new

    return new_positionsX, new_positionsY


# Move the entire chain
def move_chain(positionsX, positionsY):
    """
    Moves each residue in the chain once.
    """
    for i in range(len(positionsX)):
        positionsX, positionsY = move(i, positionsX, positionsY)
    return positionsX, positionsY


# Initialize the chain
N = 20  # Number of residues
starting_position = [0, 0]
positionsX, positionsY = initialize_chain(N, starting_position)

# Move the chain
new_positionsX, new_positionsY = move_chain(positionsX, positionsY)

# Plot before and after
plt.figure(figsize=(8, 8))
plt.xlim(-world, world)
plt.ylim(-world, world)
plt.plot(positionsX, positionsY, 'o-', label="Before Move", color="blue")
plt.plot(new_positionsX, new_positionsY, 'o--', label="After Move", color="red")
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Full Chain Movement")
plt.grid(True)
plt.show()
