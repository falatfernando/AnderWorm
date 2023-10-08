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