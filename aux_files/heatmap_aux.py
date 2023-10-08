import pandas as pd
import numpy as np
import gzip
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(folder_path):
    # Initialize an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            # Read each CSV file into a temporary DataFrame
            temp_df = pd.read_csv(file_path)

            # Add a 'file_name' column with the current filename
            temp_df['file_name'] = filename

            # Append the temporary DataFrame to the combined DataFrame
            combined_df = combined_df.append(temp_df, ignore_index=True)

    return combined_df

def merge_data(df_norm_data, df_transcription, df_samples):
    df_transcription['source'] = df_transcription['Derived Array Data File'].str.split('_norm').str[0]
    df_norm_data1 = df_norm_data[['PM', 'file_name', 'SEQ_ID']]
    df_norm_data1['source'] = df_norm_data1['file_name'].str.split('.pair').str[0]
    left_df = df_norm_data1
    right_df = df_transcription
    result_df = pd.merge(left_df, right_df, on='source', how='left')
    final_df = result_df[['PM', 'SEQ_ID', 'Sample Name']]

    left_df1 = final_df
    result_df1 = pd.merge(left_df1, df_samples, on='Sample Name', how='left')
    return result_df1

def transform_seq_id(seq_id):
    if pd.notna(seq_id):
        match = re.match(r'^\w+_(\w+)_(\d+)_(\w+)_(\d+)$', seq_id)
        if match:
            gene_name = match.group(1).upper()
            gene_number = match.group(2)
            formatted_seq_id = f"{gene_name}-{gene_number} {match.group(3)} {match.group(4)}"
            return formatted_seq_id
    return seq_id

def clean_data(df):
    df['SEQ_ID'] = df['SEQ_ID'].apply(transform_seq_id)
    df = df.rename(columns={
        'PM': 'PM',
        'SEQ_ID': 'SEQ ID',
        'Sample Name': 'Sample',
        'Characteristics: Organism': 'Organism',
        'Characteristics: Strain': 'Strain',
        'Factor Value: Genotype': 'Genotype',
        'Factor Value: Altered Gravity': 'Altered Gravity',
        'Parameter Value: Absorbed Radiation Dose': 'Absorbed Radiation Dose',
        'Parameter Value: Sample Preservation Method': 'Preservation Method'
    })
    df['SEQ'] = df['SEQ ID'].str.split('-').str[0]
    mask = (df['SEQ'].str.len() <= 10) & (df['SEQ'] != "nan")
    df_seq_normalized = df[mask]
    return df_seq_normalized

def create_heatmap(df, protein_id):
    df_heatmap = df[['PM', 'SEQ ID', 'SEQ', 'Sample']]
    df_heatmap['PM'] = df_heatmap['PM'].astype(float)
    df_heatmap.reset_index(drop=True, inplace=True)
    aap_df = df_heatmap[df_heatmap['SEQ'].isin(protein_id)]
    df = aap_df
    df['SEQ'] = df['SEQ'].str.replace(r'\d+', '', regex=True)
    df['SEQ'] = df['SEQ'].replace('', pd.NA)
    pivot_table = df.pivot_table(index='SEQ ID', columns='Sample', values='PM', aggfunc='mean')
    return pivot_table

def plot_heatmap(df):
    sample_names = df.columns.tolist()[1:]
    genes = df.index.tolist()
    data = df.iloc[:, 1:].values.astype(float)

    sns.set_context("paper", font_scale=1)
    sns_plot = sns.heatmap(data, xticklabels=sample_names, yticklabels=genes)
    sns_plot.figure.savefig("heatmap.pdf")
    plt.show()

if __name__ == "__main__":
    folder_path = r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\normalized'
    df_norm_data = load_data(folder_path)

    transcription_file = r"C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\metadata\a_gse90786_transcription_profiling_DNA_microarray.txt"
    df_transcription = pd.read_csv(transcription_file, delimiter='\t')

    samples_file = r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\samples\OSD-167-samples.csv'
    df_samples = pd.read_csv(samples_file)

    merged_data = merge_data(df_norm_data, df_transcription, df_samples)
    cleaned_data = clean_data(merged_data)
    heatmap_data = create_heatmap(cleaned_data)
    plot_heatmap(heatmap_data)