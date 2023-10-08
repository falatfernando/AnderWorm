import os
import gzip
import pandas as pd

def convert_pair_gz_to_csv(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pair.gz'):
            with gzip.open(os.path.join(folder_path, file_name), 'rb') as f_in:
                with open(os.path.join(folder_path, file_name[:-8] + '.csv'), 'wb') as f_out:
                    f_out.write(f_in.read())

convert_pair_gz_to_csv(r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\normalized')
print('done')

import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

# Example usage:
file_path = r'C:\Users\ferna\Documents\GitHub\anderworm\Project\ds_shenzou\normalized\GLDS-167_microarray_GSM2412681_1A_532_norm_RMA.csv'
encoding = detect_encoding(file_path)
print(f"The encoding of the file is: {encoding}")