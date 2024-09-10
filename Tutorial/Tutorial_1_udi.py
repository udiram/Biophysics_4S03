import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Step 1: Setting up the simulation
N = 50  # Number of particles
box_size_x = 500  # Horizontal extent of the box
box_size_y = 500  # Vertical extent of the box
a = 10  # Step size
time_steps = 200  # Number of time steps

# Initialize the positions of particles
x = np.random.rand(N) * box_size_x
y = np.random.rand(N) * box_size_y

# Create the figure and axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
ax1.set_xlim(0, box_size_x)
ax1.set_ylim(0, box_size_y)

# Initialize the scatter plot
scat = ax1.scatter(x, y)

# Set up the histogram for elevation (vertical position)
bins = np.linspace(0, box_size_y, 20)
hist_vals, bins, patches = ax2.hist(y, bins=bins, color='blue', alpha=0.7)
ax2.set_xlim(0, box_size_y)
ax2.set_ylim(0, N / 2)  # Adjust as needed


# Function to move the particles
def move(x, y):
    direction = np.random.rand(N) * 2 * np.pi
    new_x = x + a * np.cos(direction)
    new_y = y + a * np.sin(direction)

    # Reflect particles if they hit the box boundary
    new_x = np.where(new_x < 0, box_size_x + new_x, new_x)
    new_x = np.where(new_x > box_size_x, new_x - box_size_x, new_x)
    new_y = np.where(new_y < 0, box_size_y + new_y, new_y)
    new_y = np.where(new_y > box_size_y, new_y - box_size_y, new_y)

    return new_x, new_y


# Update function for animation
def update(frame):
    global x, y
    x, y = move(x, y)

    # Update scatter plot
    scat.set_offsets(np.c_[x, y])

    # Update histogram of the y-coordinates
    ax2.clear()
    ax2.hist(y, bins=bins, color='blue', alpha=0.7)
    ax2.set_xlim(0, box_size_y)
    ax2.set_ylim(0, N / 2)  # Adjust as needed
    ax2.set_ylabel("Count")
    ax2.set_xlabel("Vertical Position (y)")

    ###########################################################################
    # uncomment these lines to add the average vertical position to the plot###
    ###########################################################################

    # # Calculate and display the average vertical position
    # avg_y = np.mean(y)
    # ax2.axvline(avg_y, color='red', linestyle='--', label=f"Avg: {avg_y:.2f}")
    # ax2.legend()

    # Add the text annotation for the average y value
    # ax2.text(0.1, N / 2.5, f"Avg y: {avg_y:.2f}", fontsize=12, color='red')

    return scat,


# Create the animation
ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=50, blit=False)
ani.save('stock_animation.gif', writer='pillow', fps=10)

