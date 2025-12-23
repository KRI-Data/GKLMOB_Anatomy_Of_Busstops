import os
import pandas as pd
import yaml
import re
from collections import defaultdict

""" Script to count detected bus stop objects in each detection result file"""

# Load class names
with open('data.yaml', 'r') as f:
    data_yaml = yaml.safe_load(f)
    class_names = data_yaml['names'] if 'names' in data_yaml else {}

# Parse all detection .txt files
results_folder = 'result_labels.yolov8'
records = []


for filename in os.listdir(results_folder):
    if filename.endswith('.txt'):
        # Remove the .txt extension
        base = filename[:-4]

        # Extract only the stop_<id>_h<number> part
        match = re.match(r'(stop_\d+_h\d+)', base)
        if not match:
            print("hello1")
            continue
        clean_name = match.group(1)

        # Extract stop_id
        stop_id_match = re.match(r'stop_(\d+)_h\d+', clean_name)
        if not stop_id_match:
            continue
        stop_id = stop_id_match.group(1)

        objects_found = False  # flag to check if file has any objects

        # Read the label file
        with open(os.path.join(results_folder, filename), 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    objects_found = True  # found at least one object
                    cls_id = int(parts[0])
                    label = class_names[cls_id] if cls_id < len(class_names) else f'class_{cls_id}'

                    records.append({
                        'stop_id': stop_id,
                        'label': label
                    })
                


        # If no objects were found, append a placeholder
        if not objects_found:
            records.append({
                'stop_id': stop_id,
                'label': 'no_objects'  # temporary label for empty stops
            })



# Build DataFrame
df = pd.DataFrame(records)

# Pivot table: stop_id × label with counts
agg_df = df.pivot_table(index='stop_id', columns='label', aggfunc='size', fill_value=0)

# Save to CSV
agg_df.to_csv('aggregated_detections_per_stop.csv')

# Show top rows
print(agg_df.head())
