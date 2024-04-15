import os
import pandas as pd
from pathlib import Path

def create_ludwig_inputs(samples_df):
    '''
    Create a dataframe with the image paths, labels, and sample name for Ludwig.
    '''
    ludwig_df = pd.DataFrame(columns=['image_path', 'er_status_by_ihc', 'sample'])
    for row in samples_df.itertuples():
        sample_dir = Path(row.filename).stem
        print(sample_dir)
        if os.path.exists(os.path.join("/Users/VanKhai/Desktop/TCGA_BRCA_Histology/" + sample_dir, sample_dir + '_tiles')):
            tiles = os.listdir(os.path.join("/Users/VanKhai/Desktop/TCGA_BRCA_Histology/" + sample_dir, sample_dir + '_tiles')) 
        # tiles = os.listdir("/Users/VanKhai/Desktop/TCGA_BRCA_Histology/TCGA-A1-A0SN-01Z-00-DX1.5E9B85AE-AFB7-41DC-8A1B-BD6DA39B6540/TCGA-A1-A0SN-01Z-00-DX1.5E9B85AE-AFB7-41DC-8A1B-BD6DA39B6540_tiles")
            print (sample_dir)
        # Add each tile to the training data.
            for tile in tiles:
                tile_path = os.path.join(sample_dir, sample_dir + '_tiles', tile)
                ludwig_df.loc[len(ludwig_df)] = {'image_path': tile_path, 'er_status_by_ihc': row.er_status_by_ihc, 'sample': row.sample}      
    return ludwig_df

# Read in samples manifest file.
samples_df = pd.read_csv('/Users/VanKhai/Desktop/TCGA_BRCA_Histology/er_status_samples.txt', sep='\t')
# Write all data to file.
ludwig_all = create_ludwig_inputs(samples_df)
ludwig_all.to_csv('er_status_all_data.csv', index=False)