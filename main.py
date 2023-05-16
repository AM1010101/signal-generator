import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

class WavefromGenerator:
    def __init__(self):
        if 'current_waveform' not in st.session_state:
            st.session_state.current_waveform = None
        if 'wave_form_saved' not in st.session_state:
            st.session_state.wave_form_saved = None
        self.render_page()

    
    def render_page(self):
        st.title('Waveform Generator')
        st.write('This `Waveform Generator` allows you to specify a number of waves and then add them together.')

        df = pd.DataFrame()
        wavetype = pd.DataFrame(
            {"command": ["Sine", "Cosine", "Square", "Triangle", "Sawtooth"]}
        )
        df["Frequency"] = [3.0, 2.0, 3.0]
        df["Amplitude"] = [1.0, 1.0, 1.0]
        df["Offset"] = [1.0, 4.0, 3.0]
        df["Duration"] = [1.0, 1.0, 1.0]
        df["Wavetype"] = (
            wavetype["command"].astype("category")
        )

        edited_df = st.experimental_data_editor(df, key="my_df", num_rows='dynamic',width=1000)
        
        # Create two columns for the sliders
        col1, col2, col3 = st.columns(3)
        with col1:
            self.sample_rate = st.slider('Sample Rate', 1, 100, 40, 1)
        with col2:
            silence_duration = st.slider('Gap Duration(sets wave to zero)', 0.0, 2.0, 1.0, 0.05)
        with col3:  
            self.smoothing = st.slider('Smoothing', 0.0, 1.0, 0.0, 0.05)
        
        total_duration = sum(edited_df['Duration'].values) + len(edited_df['Duration'].values) * silence_duration
        st.text(f"Duration: {total_duration} seconds")
        total_samples = int(self.sample_rate * total_duration)
        st.text(f'Total Samples: {total_samples}')
        
        
        if st.button('Generate'):
            frequencies = edited_df['Frequency'].values
            amplitudes = edited_df['Amplitude'].values
            offsets = edited_df['Offset'].values
            durations = edited_df['Duration'].values
            wave_types = edited_df['Wavetype'].values
            st.session_state.current_waveform = self.generate_waveform(frequencies, amplitudes, offsets, durations, sr=self.sample_rate, silence_duration=silence_duration, wavetypes=wave_types)
            st.session_state.wave_form_saved = False
            
        if st.session_state.current_waveform is not None:
            if st.session_state.wave_form_saved == False:
                if st.button('Save'):
                    self.save_waveform(st.session_state.current_waveform, self.sample_rate, 'waveform_data')
                    st.session_state.wave_form_saved = True
            if st.session_state.wave_form_saved == True:
                st.success('Waveform Saved')
            self.plot_waveform(st.session_state.current_waveform, self.sample_rate)


    def generate_waveform(self,frequencies, amplitudes, offsets, durations, sr, silence_duration, wavetypes):
        # Calculate the total number of samples for the entire waveform
        total_samples = int(sr * (sum(durations) + len(durations) * silence_duration))
        # Create an empty array to store the waveform
        waveform = np.zeros(total_samples)
        # Create each sine wave and silence period, and add them to the waveform
        start = 0
        for freq, amp, offset, dur, wt in zip(frequencies, amplitudes, offsets, durations, wavetypes):
            samples = int(sr * dur)
            t = np.linspace(0, dur, samples, endpoint=False)
            # check the wavetype and generate appropriate waveform
            if wt == 'Sine':
                wave = amp * np.sin(2 * np.pi * freq * t) + offset
            elif wt == 'Cosine':
                wave = amp * np.cos(2 * np.pi * freq * t) + offset
            elif wt == 'Square':
                wave = amp * np.sign(np.sin(2 * np.pi * freq * t)) + offset
            elif wt == 'Triangle':
                wave = amp * np.arcsin(np.sin(2 * np.pi * freq * t)) + offset
            elif wt == 'Sawtooth':
                wave = amp * np.arctan(np.tan(2 * np.pi * freq * t)) + offset
            else:
                wave = amp * np.sin(2 * np.pi * freq * t) + offset
            waveform[start:start+samples] += wave
            start += samples
            # Add a silence period
            silence_samples = int(sr * silence_duration)
            waveform[start:start+silence_samples] += 0
            start += silence_samples
        # Smooth the waveform
        if self.smoothing > 0:
            waveform = np.convolve(waveform, np.ones(int(sr * self.smoothing)) / (sr * self.smoothing), mode='same')
        # Normalize the waveform
        # waveform /= max(abs(waveform))

        return waveform

    def plot_waveform(self, waveform, sample_rate):
        fig, ax = plt.subplots()
        time_values = np.arange(len(waveform)) / sample_rate
        ax.plot(time_values, waveform)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Generated Waveform')
        # Remove top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Set y-axis tick labels to show time in seconds
        ax.set_yticks(np.arange(0, max(waveform), step=max(waveform)/5))
        # set the aspect ratio to fit the window
        # set the height to width ratio to 1:2
        fig.set_figheight(7)
        fig.set_figwidth(20)
        fig.set_dpi(500)
        plt.show()

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
        print(type(waveform))

        
if __name__ == "__main__":
    waveform_generator = WavefromGenerator()
    