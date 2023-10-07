import streamlit as st
from aux_files.macro_temperature import generate_temperature_plot

# Set the page configuration
st.set_page_config(
    page_title= "AnderWorm",
    page_icon= "🪱"
)

# Title of the app
st.title("AnderWorm 🪱🧬")

# Generate the temperature plot
generate_temperature_plot()
st.image('temperature_plot.png', width=400)

# Display "Hello, World!" on the app
st.write("In development")

# Sidebar title
st.sidebar.title("VARIABLES INPUTS")

# Temperature value and variation
temperature = 23.5
variation = 0.5

# Display the temperature in a box
st.sidebar.info(f"Temperature is {temperature} °C ± {variation} °C")

# Slider for gravity value
gravity_value = st.sidebar.slider("Gravity", 0, 100, 50)
st.sidebar.write(f"Gravity Value: {gravity_value}")

# Slider for radiation value
radiation_value = st.sidebar.slider("Radiation", 0, 100, 50)
st.sidebar.write(f"Radiation Value: {radiation_value}")