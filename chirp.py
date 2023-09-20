import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the chirp signal
duration = 2.0  # Duration of the signal in seconds
sampling_rate = 1000  # Sampling rate in Hz (samples per second)
start_frequency = 1  # Start frequency in Hz
end_frequency = 10  # End frequency in Hz

# Create a time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Calculate the instantaneous frequency as a linear sweep
instantaneous_frequency = np.linspace(start_frequency, end_frequency, (len(t)//2))
return_inst_freq = np.linspace( 0,end_frequency-1, (len(t)//2))

instantaneous_frequency = np.concatenate((instantaneous_frequency, return_inst_freq))

print(instantaneous_frequency)

# Calculate the cumulative frequency by integrating the instantaneous frequency
cumulative_frequency = np.cumsum(instantaneous_frequency) / sampling_rate
print(cumulative_frequency) 


# Generate the chirp signal
chirp_signal = np.sin(2 * np.pi * cumulative_frequency * t)

# Plot the chirp signal
plt.plot(t, chirp_signal)
plt.title("Chirp Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
