import numpy as np
import matplotlib.pyplot as plt
#%%
# Constants
A1 = 3.354e-3
B1 = 2.570e-4
C1 = 2.620e-3
D1 = 6.383e-3
Rref = 10e3  # 10k ohms

# Define temperature to resistance in Kelvin
def temperature_kelvin(R):
    lnR = np.log(R / Rref)
    T_inv = A1 + B1 * lnR + C1 * lnR**2 + D1 * lnR**3
    return 1 / T_inv  # Temperature in Kelvin

# Generate resistance range
R_values = np.arange(750, 10001, 10)

# Generate resistance as temperature
Vout = 5 * R_values / (10e3 + R_values)
T_kelvin = temperature_kelvin(R_values)
t_celsius = T_kelvin - 273.15

# empirical data
empirical_data = np.array([1, 14, 23, 31, 47])
voltage_data = np.array([3.800, 3.100, 2.625, 2.220, 1.450])

plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(t_celsius, R_values, color='b')
plt.title('Temperature vs Resistance')
plt.xlabel('Temperature (°C)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(empirical_data, voltage_data, color='r', label='Empirical Data', zorder=5)
plt.title('Temperature vs Voltage')
plt.xlabel('Temperature (°C)')
plt.ylabel('Voltage (V)')
plt.legend()

plt.tight_layout()
plt.show()
#%%
# Specific temperature in Celsius
T_input = float(input("Enter the temperature in Celsius: "))

# Find the closest temperature in the t_celsius array
idx = (np.abs(t_celsius - T_input)).argmin()

# Get the corresponding resistance
R_output = R_values[idx]

# Output the resistance
print(f"The resistance at {T_input}°C is approximately {R_output:.2f} ohms.")

# Calculate voltage output
V_out = 5 * R_output / (10e3 + R_output)
print(f"Voltage output at {T_input}°C is approximately {V_out:.2f}V.")