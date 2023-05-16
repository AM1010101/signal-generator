import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

class WavefromGenerator:
    def __init__(self):
        st.session_state.current_waveform = None
        self.render_page()

    
    def render_page(self):
        df = pd.DataFrame()
        wavetype = pd.DataFrame(
            {"command": ["Sine", "Square", "Triangle", "Sawtooth"]}
        )
        df["Frequency"] = [3.0, 2.0, 3.0]
        df["Amplitude"] = [1, 1, 1]
        df["Offset"] = [1, 4, 3]
        df["Duration"] = [1, 1, 1]
        df["Wavetype"] = (
            wavetype["command"].astype("category")
        )

        edited_df = st.experimental_data_editor(df, key="my_df", num_rows='dynamic')

        self.sample_rate = st.slider('Sample Rate', 1, 100, 40, 1)
        silence_duration = st.slider('Zero Gap', 0.0, 2.0, 1.0, 0.1)

        if st.button('Generate'):
            frequencies = edited_df['Frequency'].values
            amplitudes = edited_df['Amplitude'].values
            offsets = edited_df['Offset'].values
            durations = edited_df['Duration'].values
            st.session_state.current_waveform = self.generate_waveform(frequencies, amplitudes, offsets, durations, sr=self.sample_rate, silence_duration=silence_duration)
            st.button('Save', on_click=self.save_waveform(st.session_state.current_waveform, self.sample_rate, 'test'))
        
        if st.session_state.current_waveform is not None:
            self.plot_waveform(st.session_state.current_waveform)

        
        
        
    

    def generate_waveform(self,frequencies, amplitudes, offsets, durations, sr, silence_duration):
        # Calculate the total number of samples for the entire waveform
        total_samples = int(sr * (sum(durations) + len(durations) * silence_duration))
        # Create an empty array to store the waveform
        waveform = np.zeros(total_samples)
        # Create each sine wave and silence period, and add them to the waveform
        start = 0
        for freq, amp, offset, dur in zip(frequencies, amplitudes, offsets, durations):
            samples = int(sr * dur)
            t = np.linspace(0, dur, samples, endpoint=False)
            # check the wavetype and generate appropriate waveform
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

    def plot_waveform(self,waveform):
        fig, ax = plt.subplots()
        ax.plot(waveform)
        ax.set_xlabel('Time (samples)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Generated Waveform')
        # Remove top and right borders
        ax.spines['top'].set_visible(False)

        return st.pyplot(fig)

    def save_waveform(self, waveform, sample_rate, filename):
        '''Save the waveform to a file'''
        # Calculate time interval between samples
        time_interval = 1 / sample_rate
        # Generate timestamps based on the time interval
        timestamps = [i * time_interval for i in range(len(waveform))]
        # Create a CSV file and write the data to it
        with open(f'{filename}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Amplitude'])
            for i in range(len(waveform)):
                writer.writerow([timestamps[i], waveform[i]])

        

if __name__ == "__main__":
    waveform_generator = WavefromGenerator()
    