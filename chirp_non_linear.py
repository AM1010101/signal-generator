import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the chirp signal
duration = 2.0  # Duration of the signal in seconds
sampling_rate = 1000  # Sampling rate in Hz (samples per second)
start_frequency = 1  # Start frequency in Hz
end_frequency = 3  # End frequency in Hz

# Create a time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Define a custom function for the instantaneous frequency
def custom_instantaneous_frequency(t):
    return start_frequency + (end_frequency - start_frequency) * t**2

# Calculate the instantaneous frequency using the custom function
instantaneous_frequency = custom_instantaneous_frequency(t)

# Calculate the cumulative frequency by integrating the instantaneous frequency
cumulative_frequency = np.cumsum(instantaneous_frequency) / sampling_rate

# Generate the chirp signal
chirp_signal = np.sin(2 * np.pi * cumulative_frequency * t)

# Plot the chirp signal
plt.plot(t, chirp_signal)
plt.title("Chirp Signal with Nonlinear Frequency Sweep")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()