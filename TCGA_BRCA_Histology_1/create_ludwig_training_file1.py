import os
import pandas as pd
from pathlib import Path

def create_ludwig_inputs(samples_df, output_feature):
    ludwig_df = pd.DataFrame(columns=['image_path', output_feature, 'sample'])
    for row in samples_df.itertuples():
        sample_dir = Path(row.filename).stem
        if os.path.exists(os.path.join("/Users/VanKhai/Desktop/TCGA_BRCA_Histology/" + sample_dir, sample_dir + '_tiles')):
            tiles = os.listdir(os.path.join("/Users/VanKhai/Desktop/TCGA_BRCA_Histology/" + sample_dir, sample_dir + '_tiles'))
            for tile in tiles:
                tile_path = os.path.join(sample_dir, sample_dir + '_tiles', tile)
                output_value = getattr(row, output_feature) if hasattr(row, output_feature) else None
                ludwig_df.loc[len(ludwig_df)] = {'image_path': tile_path, output_feature: output_value, 'sample': row.sample}
    return ludwig_df

# Read in samples manifest files
er_samples_df = pd.read_csv('/Users/VanKhai/Desktop/TCGA_BRCA_Histology/er_status_samples.txt', sep='\t', usecols=['filename', 'er_status_by_ihc', 'sample'])
pr_samples_df = pd.read_csv('/Users/VanKhai/Desktop/TCGA_BRCA_Histology/pr_status_samples.txt', sep='\t', usecols=['filename', 'pr_status_by_ihc', 'sample']) 
her2_samples_df = pd.read_csv('/Users/VanKhai/Desktop/TCGA_BRCA_Histology/her2_status_samples.txt', sep='\t', usecols=['filename', 'HER2_status', 'sample'])
tn_samples_df = pd.read_csv('/Users/VanKhai/Desktop/TCGA_BRCA_Histology/tn_status_samples.txt', sep='\t', usecols=['filename', 'Triple_negative_status', 'sample'])

# Create dataframes for each task
er_ludwig_df = create_ludwig_inputs(er_samples_df, 'er_status_by_ihc')
pr_ludwig_df = create_ludwig_inputs(pr_samples_df, 'pr_status_by_ihc')  
her2_ludwig_df = create_ludwig_inputs(her2_samples_df, 'HER2_status')
tn_ludwig_df = create_ludwig_inputs(tn_samples_df, 'Triple_negative_status')

# Write each dataframe to a separate file
er_ludwig_df.to_csv('er_task_data.csv', index=False)
pr_ludwig_df.to_csv('pr_task_data.csv', index=False)
her2_ludwig_df.to_csv('her2_task_data.csv', index=False)
tn_ludwig_df.to_csv('tn_task_data.csv', index=False)