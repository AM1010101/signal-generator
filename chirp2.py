import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the chirp signal
duration = 1.0  # Duration of the signal in seconds
sampling_rate = 44100  # Sampling rate in Hz (samples per second)
start_frequency = 100  # Start frequency in Hz
end_frequency = 1000  # End frequency in Hz

# Create a time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Calculate the duration for each chirp segment (up and down)
half_duration = duration / 2

# Calculate the instantaneous frequency for the up and down segments
up_instantaneous_frequency = np.linspace(start_frequency, end_frequency, int(sampling_rate * half_duration))
down_instantaneous_frequency = np.linspace(end_frequency, start_frequency, int(sampling_rate * half_duration))

# Calculate the cumulative frequency for the up and down segments
up_cumulative_frequency = np.cumsum(up_instantaneous_frequency) / sampling_rate
down_cumulative_frequency = np.cumsum(down_instantaneous_frequency) / sampling_rate

# Generate the chirp signals for the up and down segments
up_chirp_signal = np.sin(2 * np.pi * up_cumulative_frequency * t[:len(up_cumulative_frequency)])
down_chirp_signal = np.sin(2 * np.pi * down_cumulative_frequency * t[len(up_cumulative_frequency):])

# Concatenate the two chirp segments to create the complete chirp signal
chirp_signal = np.concatenate((up_chirp_signal, down_chirp_signal))

# Plot the chirp signal
plt.plot(t, chirp_signal)
plt.title("Chirp Signal (Up and Down)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
