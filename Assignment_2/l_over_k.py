import numpy as np
import matplotlib.pyplot as plt

# Define the function for the fraction of occupied receptors f as a function of L/K
def fraction_occupied(L_over_K):
    return (L_over_K) / (1 + L_over_K)

# Create an array for L/K values between 0 and 5
L_over_K_values = np.linspace(0, 5, 100)

# Calculate the corresponding f values
f_values = fraction_occupied(L_over_K_values)

# Plot f as a function of L/K
plt.figure(figsize=(8, 6))
plt.plot(L_over_K_values, f_values, label=r'$f = \frac{\frac{[L]}{K}}{1 + \frac{[L]}{K}}$', color='red')
plt.title('Fraction of Occupied Receptors as a Function of [L]/K')
plt.xlabel(r'$\frac{[L]}{K}$')
plt.ylabel('Fraction of Occupied Receptors (f)')
plt.grid(True)
plt.legend()
plt.show()
