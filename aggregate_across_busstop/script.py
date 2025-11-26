import os
import pandas as pd
import yaml
import re
from collections import defaultdict

# Load class names
with open('data.yaml', 'r') as f:
    data_yaml = yaml.safe_load(f)
    class_names = data_yaml['names'] if 'names' in data_yaml else {}

# Parse all detection .txt files
results_folder = 'results'
records = []

for filename in os.listdir(results_folder):
    if filename.endswith('.txt'):
        image_name = filename.replace('.txt', '')
        match = re.match(r'stop_(\d+)_h\d+', image_name)
        if not match:
            continue
        stop_id = match.group(1)

        with open(os.path.join(results_folder, filename), 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    cls_id = int(parts[0])
                    label = class_names[cls_id] if cls_id < len(class_names) else f'class_{cls_id}'

                    records.append({
                        'stop_id': stop_id,
                        'label': label
                    })

# Build DataFrame
df = pd.DataFrame(records)

# Pivot table: stop_id × label with counts
agg_df = df.pivot_table(index='stop_id', columns='label', aggfunc='size', fill_value=0)

# Save to CSV
agg_df.to_csv('aggregated_detections_per_stop.csv')

# Show top rows
print(agg_df.head())
