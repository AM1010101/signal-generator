import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_waveform(frequencies, amplitudes, offsets, durations, sr=44100, silence_duration=0.1):
    # Calculate the total number of samples for the entire waveform
    total_samples = int(sr * (sum(durations) + len(durations) * silence_duration))
    # Create an empty array to store the waveform
    waveform = np.zeros(total_samples)
    # Create each sine wave and silence period, and add them to the waveform
    start = 0
    for freq, amp, offset, dur in zip(frequencies, amplitudes, offsets, durations):
        samples = int(sr * dur)
        t = np.linspace(0, dur, samples, endpoint=False)
        sine_wave = amp * np.sin(2 * np.pi * freq * t) + offset
        waveform[start:start+samples] += sine_wave
        start += samples
        # Add a silence period
        silence_samples = int(sr * silence_duration)
        waveform[start:start+silence_samples] += 0
        start += silence_samples
    # Normalize the waveform
    waveform /= max(abs(waveform))
    return waveform

def plot_waveform(waveform):
    fig, ax = plt.subplots()
    ax.plot(waveform)
    ax.set_xlabel('Time (samples)')
    ax.set_ylabel('Amplitude')
    st.pyplot(fig)

# Define the default values for the waveform parameters
default_frequencies = [440, 880, 1320]
default_amplitudes = [0.5, 0.3, 0.2]
default_offsets = [0, 0.5, -0.2]
default_durations = [0.5, 0.3, 0.2]

# Create a Streamlit app
st.title('Waveform Generator')
frequencies = st.sidebar.text_input('Frequencies (comma-separated)', ','.join(map(str, default_frequencies)))
amplitudes = st.sidebar.text_input('Amplitudes (comma-separated)', ','.join(map(str, default_amplitudes)))
offsets = st.sidebar.text_input('Offsets (comma-separated)', ','.join(map(str, default_offsets)))
durations = st.sidebar.text_input('Durations (comma-separated)', ','.join(map(str, default_durations)))
sr = st.sidebar.slider('Sampling Rate', 8000, 96000, 44100, 1000)
silence_duration = st.sidebar.slider('Silence Duration', 0.0, 1.0, 0.1, 0.01)
st.experimental_data_editor([frequencies, amplitudes, offsets, durations],num_rows=)

if st.sidebar.button('Generate'):
    frequencies = list(map(float, frequencies.split(',')))
    amplitudes = list(map(float, amplitudes.split(',')))
    offsets = list(map(float, offsets.split(',')))
    durations = list(map(float, durations.split(',')))
    waveform = generate_waveform(frequencies, amplitudes, offsets, durations, sr=sr, silence_duration=silence_duration)
    plot_waveform(waveform)
