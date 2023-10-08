import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from aux_files.macro_temperature import generate_temperature_plot
from aux_files.heatmap_aux import load_data, merge_data, clean_data, create_heatmap

# Set the page configuration
st.set_page_config(
    page_title= "AnderWorm",
    page_icon= "🪱"
)

# Title of the app
st.title("AnderWorm 🪱🧬")

# Parameters
folder_path = r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\normalized'
transcription_file = r"C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\metadata\a_gse90786_transcription_profiling_DNA_microarray.txt"
df_transcription = pd.read_csv(transcription_file, delimiter='\t')
samples_file = r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\samples\OSD-167-samples.csv'
df_samples = pd.read_csv(samples_file)
df_norm_data = load_data(folder_path)
merged_data = merge_data(df_norm_data, df_transcription, df_samples)
cleaned_data = clean_data(merged_data)

# Generate the temperature plot
#generate_temperature_plot()
#st.image('temperature_plot.png', width=400)

# Sidebar title
st.sidebar.title("VARIABLES INPUTS")

# Temperature value and variation
temperature = 23.5
variation = 0.5

# Data selection
st.sidebar.header("Filter Data")
protein_id = st.sidebar.multiselect("Select Protein IDs", cleaned_data['SEQ'].unique(), [], key="protein_ids", help="Search and select multiple Protein IDs")

# Display the temperature in a box
st.sidebar.info(f"Temperature is {temperature} °C ± {variation} °C")

# Slider for gravity value
gravity_value = st.sidebar.slider("Gravity", 0, 100, 50)
st.sidebar.write(f"Gravity Value: {gravity_value}")

# Slider for radiation value
radiation_value = st.sidebar.slider("Radiation", 0, 100, 50)
st.sidebar.write(f"Radiation Value: {radiation_value}")

# Create a heatmap based on the selected protein_id
if st.sidebar.button("Generate Heatmap"):
    heatmap_data = create_heatmap(cleaned_data, protein_id)
    
    # Display the heatmap
    st.subheader(f"Heatmap for Protein ID: {protein_id}")

    # Create the heatmap plot using Seaborn
    sample_names = heatmap_data.columns.tolist()[1:]
    genes = heatmap_data.index.tolist()
    data = heatmap_data.iloc[:, 1:].values.astype(float)
    
    sns.set_context("paper", font_scale=1)
    sns_plot = sns.heatmap(data, xticklabels=sample_names, yticklabels=genes)
    
    # Display the plot
    st.pyplot(plt)