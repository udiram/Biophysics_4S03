import numpy as np
import matplotlib.pyplot as plt

# Define the function for the modified fraction of occupied receptors f' as a function of (L/K)^(1/4)
def modified_fraction_occupied(L_over_K_fourth):
    return (L_over_K_fourth**4) / (1 + L_over_K_fourth**4)

# Create an array for (L/K)^(1/4) values between 0 and 5
L_over_K_fourth_values = np.linspace(0, 5, 100)

# Calculate the corresponding f' values
f_prime_values = modified_fraction_occupied(L_over_K_fourth_values)

# Plot f' as a function of (L/K)^(1/4)
plt.figure(figsize=(8, 6))
plt.plot(L_over_K_fourth_values, f_prime_values, label=r"$f' = \frac{\left(\frac{[L]}{K}\right)^4}{1 + \left(\frac{[L]}{K}\right)^4}$", color='blue')
plt.title(r"Fraction of Occupied Receptors $f'$ as a Function of $\left(\frac{[L]}{K}\right)^{1/4}$")
plt.xlabel(r"$\left(\frac{[L]}{K}\right)^{1/4}$")
plt.ylabel("Fraction of Occupied Receptors (f')")
plt.grid(True)
plt.legend()
plt.savefig('f_prime.png')
plt.show()
