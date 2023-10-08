import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from aux_files.macro_temperature import generate_temperature_plot
from aux_files.heatmap_aux import load_data, merge_data, clean_data, create_heatmap
from PIL import Image
import base64

################################################### Set the page configuration ###############################################
st.set_page_config(
    page_title= "AnderWorm",
    page_icon= "🪱",
    layout= "wide"
)

page_bg_img = '''
 <style>
 [data-testid="stAppViewContainer"] {
background-color: #000000;
opacity: 0.9;
background-color: #000000;
opacity: 1;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #000000 40px ), repeating-linear-gradient( #0f0f1155, #0f0f11 );}
 </style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Temperature value and variation
temperature = 23.5
variation = 0.5

############################################# SIDEBAR #########################################################################

# Data selection
with open('aux_files/list.txt', "r") as file:
    options = file.read().splitlines()

st.sidebar.header("Data Analysis 🔎")
protein_id = st.sidebar.multiselect("Select Protein IDs", options, [], key="protein_id", help="Search and select multiple Protein IDs")

st.sidebar.markdown("<hr> </hr>", unsafe_allow_html=True)

st.sidebar.header("Data Prediction 📊")

# Display the temperature in a box
st.sidebar.info(f"Temperature is {temperature} °C ± {variation} °C")

# Slider for gravity value
# Values and labels for the slider
values = [1e-6, 1e-3, 1]
labels = ["10^-6", "10^-3", "1"]

# Create a slider for gravity value with custom labels
selected_index = st.sidebar.selectbox("Select Gravity (G)", range(len(values)), format_func=lambda x: labels[x])

# Slider for radiation value
radiations = [0.0, 1.92, 2.27]
radiation_value = st.sidebar.slider("Radiation (miligray)", min(radiations), max(radiations), 1.92)

############################################### MAIN ################################################################

# Create a heatmap based on the selected protein_id
if st.sidebar.button("Generate Heatmap"):
    with st.spinner('Loading you analysis...'):
        # Parameters
        folder_path = '/ds_shenzou/normalized'
        transcription_file = "/ds_shenzou/metadata/a_gse90786_transcription_profiling_DNA_microarray.txt"
        df_transcription = pd.read_csv(transcription_file, delimiter='\t')
        samples_file = '/ds_shenzou/samples/OSD-167-samples.csv'
        df_samples = pd.read_csv(samples_file)
        df_norm_data = load_data(folder_path)
        merged_data = merge_data(df_norm_data, df_transcription, df_samples)
        cleaned_data = clean_data(merged_data)
        heatmap_data = create_heatmap(cleaned_data, protein_id)
        
        st.markdown("<h1 style = 'color:white; text-align:center'>Data Analysis 🔎 </h1>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            # Display the heatmap
            st.success(f"Heatmap for proteins: {protein_id} expression")

            # Create the heatmap plot using Seaborn
            sample_names = heatmap_data.columns.tolist()[1:]
            genes = heatmap_data.index.tolist()
            data = heatmap_data.iloc[:, 1:].values.astype(float)
            
            sns.set_context("paper", font_scale=1)
            sns_plot = sns.heatmap(data, xticklabels=sample_names, yticklabels=genes)
            
            # Display the plot
            st.pyplot(plt)
        with col4:
            st.warning('Mean UNF values x Temperature for C. elegans')
            # Generate the temperature plot
            generate_temperature_plot()
            st.image('temperature_plot.png', use_column_width=True)

else:
    # Title of the app
    st.markdown("<h1 style = 'color: white; text-align: center'> AnderWorm 🪱🧬 </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style = 'color: white; text-align: center'> Anderworm is a NASA Space APPS (2023) project </h4>"
                , unsafe_allow_html=True)
    st.warning('Use the sidebar menu to choose between different input parameters, study the data and predict Caenorhabditis elegans genomic behaviours!')
    st.markdown(''' <p style = 'color: white; text-align: justify'> This app was inspired by the study conducted by Gao, Y.; Xu, D.; Zhao, L.; Zhang, M.; Sun, Y. on the effects of microgravity on DNA damage response in Caenorhabditis elegans during the Shenzhou-8 spaceflight, published in the International Journal of Radiation Biology in 2015 (DOI: 10.3109/09553002.2015.1043754). The data used in this app is sourced from official NASA websites. </p>
    ''', unsafe_allow_html= True)
    st.write('Developed by Fernando Falat, Henrique Galeski and Juan Penas.')
    st.markdown('<br>' '</br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.image('https://assets.spaceappschallenge.org/media/images/SpaceAppsLogo_Default_2ColorWhi.width-440.jpegquality-60.png', width= 300)
    with col2:
        st.image('https://i.imgur.com/Xqif8jIl.png',width=300)