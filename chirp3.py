import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the chirp signal
duration = 2.0  # Duration of the signal in seconds
sampling_rate = 1000  # Sampling rate in Hz (samples per second)
start_frequency = 1  # Start frequency in Hz
end_frequency = 10  # End frequency in Hz

# Create a time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Define a custom function for the instantaneous frequency
def custom_instantaneous_frequency(t):
    '''returns a sinewave where the period is duration and the phase offset is 90 degrees'''
    return np.sin(2*np.pi*t/duration + np.pi/2*sampling_rate)*40

# Calculate the instantaneous frequency using the custom function
instantaneous_frequency = np.array([custom_instantaneous_frequency(ti) for ti in t])

# Calculate the cumulative frequency by integrating the instantaneous frequency
cumulative_frequency = np.cumsum(instantaneous_frequency) / sampling_rate

# Generate the chirp signal
chirp_signal = np.sin(2 * np.pi * cumulative_frequency * t)

# Plot the chirp signal
plt.plot(t, chirp_signal)
plt.plot(t, cumulative_frequency)
plt.title("Chirp Signal with Ascending and Descending Frequency Sweep")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
