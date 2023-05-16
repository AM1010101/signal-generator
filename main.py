import numpy as np
import streamlit as st

# Define the sampling rate and duration of each sine wave
sr = 40
silence_duration = 1

# Define the frequencies, amplitudes, and offsets of each sine wave
frequencies = [3, 1, 0.3]
amplitudes = [0.5, 3, 0.2]
offsets = [1, 5, 2]
durations = [10, 10, 10] # in seconds

# Create an empty array to store the sine waves
total_samples = int(sr * (sum(durations) + len(durations) * silence_duration))
sine_waves = np.zeros(total_samples)

# Create each sine wave and add it to the array
start = 0
for freq, amp, offset, dur in zip(frequencies, amplitudes, offsets, durations):
    samples = int(sr * dur)
    t = np.linspace(0, dur, samples, endpoint=False)
    sine_wave = amp * np.sin(2 * np.pi * freq * t) + offset
    sine_waves[start:start+samples] += sine_wave
    start += samples
    # Add a silence period
    silence_samples = int(sr * silence_duration)
    sine_waves[start:start+silence_samples] += 0
    start += silence_samples

# Normalize the array
sine_waves /= max(abs(sine_waves))

# Plot the resulting waveform
import matplotlib.pyplot as plt
plt.plot(sine_waves)
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()