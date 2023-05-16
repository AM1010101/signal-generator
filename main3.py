import streamlit as st
import pandas as pd

# Define a function that takes a dataframe as input and does something with it
def process_dataframe(df):
    # Do something with the dataframe, e.g. print it
    st.write(df)

# Define the Streamlit app
def app():
    # Create an empty dataframe with the desired columns
    df = pd.DataFrame(columns=['frequency', 'amplitude', 'offset', 'duration'])

    # Add a button to allow the user to add new rows to the dataframe
    if st.button('Add new row'):
        # Get the values for the new row from the user
        frequency = st.number_input('Frequency', min_value=0.0, max_value=1000.0, step=0.1)
        amplitude = st.number_input('Amplitude', min_value=0.0, max_value=1000.0, step=0.1)
        offset = st.number_input('Offset', min_value=0.0, max_value=1000.0, step=0.1)
        duration = st.number_input('Duration', min_value=0.0, max_value=1000.0, step=0.1)

        # Add the new row to the dataframe
        new_row = {'frequency': frequency, 'amplitude': amplitude, 'offset': offset, 'duration': duration}
        df = df.append(new_row, ignore_index=True)

    # Add a button to submit the dataframe to the processing function
    if st.button('Process dataframe'):
        process_dataframe(df)

# Run the Streamlit app
if __name__ == '__main__':
    app()
