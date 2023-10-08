import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import norm

# OSD 40 - Thermal Conditions
current_directory = os.getcwd()
relative_path = 'datasets/temperature_osd40' 
folder_path = os.path.join(current_directory, relative_path)

data_frames = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file has a .txt extension
    if filename.endswith('.txt'):
        # Create the absolute file path for each text file
        file_path = os.path.join(folder_path, filename)
        
        # Read the text file into a temporary DataFrame
        temp_df = pd.read_csv(file_path, delimiter='\t')  # Use the appropriate delimiter if needed
        temp_df['Sample_Name'] = filename
        # Append the temporary DataFrame to the list of DataFrames
        data_frames.append(temp_df)

# Concatenate all DataFrames into a single DataFrame
df_temperature = pd.concat(data_frames, ignore_index=True)

# Temperature studies
df_40_samples = pd.read_csv("datasets/temperature_osd40/OSD-40-samples.csv")
df_40_assays = pd.read_csv("datasets/temperature_osd40/OSD-40-assays.csv")

# Perfoming merge with tables to extract temperature for each gene expression
df_40 = df_temperature.merge(df_40_assays, left_on= 'Sample_Name', right_on= 'Derived Array Data File',how = 'left')
df_40 = df_40.merge(df_40_samples, on= 'Sample Name', how = 'left')

df_40['Temperature C'] = df_40['Comment: Sample_source_name'].str.extract(r'(\d+)').astype(int)

df_40_normalized = df_40[['UNF_VALUE', 'Temperature C']]

df_40_normalized10 = df_40_normalized[df_40_normalized['Temperature C']==10]
df_40_normalized15 = df_40_normalized[df_40_normalized['Temperature C']==15]
df_40_normalized20 = df_40_normalized[df_40_normalized['Temperature C']==20]
df_40_normalized25 = df_40_normalized[df_40_normalized['Temperature C']==25]

def generate_temperature_plot():
    # Create an empty list to store the filtered dataframes
    filtered_dfs = []

    # Define temperature values
    temperatures = [10, 15, 20, 25]

    # Create a list to store the mean UNF_VALUE for each temperature
    mean_unf_values = []

    # Iterate through each temperature group
    for temp in temperatures:
        # Get the corresponding dataframe
        df_temp = globals()[f'df_40_normalized{temp}']

        # Calculate the mean and standard deviation
        mu, std = norm.fit(df_temp['UNF_VALUE'])

        # Define a threshold for filtering unnormalized values (e.g., within 3 standard deviations)
        threshold = 3 * std

        # Filter out values that are not within the threshold
        filtered_df = df_temp[(df_temp['UNF_VALUE'] >= mu - threshold) & (df_temp['UNF_VALUE'] <= mu + threshold)]

        # Append the filtered dataframe to the list
        filtered_dfs.append(filtered_df)

        # Calculate and store the mean UNF_VALUE
        mean_unf_values.append(filtered_df['UNF_VALUE'].mean())

    # Create a plot showing only the four temperatures on the x-axis and mean UNF_VALUE on the y-axis
    plt.figure(figsize=(8, 6))
    plt.plot(temperatures, mean_unf_values, marker='o', linestyle='-', color='blue')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Mean UNF_VALUE')
    plt.title('Mean UNF_VALUE for Different Temperatures')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(temperatures)  # Set the x-axis ticks to only the specified temperatures

    # Save the plot to a file
    #plt.savefig('temperature_plot.png')
