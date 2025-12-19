import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

""" Script to calculate bus stop quality scores based on detected elements"""

# Load aggregated detection results
df = pd.read_csv('aggregated_detections_per_stop.csv')

# Define infrastructure elements that count toward bus stop quality
quality_elements = ['bas_road_marking', 'bench', 'board_sign','rumble_strips', 'shelter', 'stop_sign', 'street_light', 'trash_bin', 'zebra_crossing']

# Ensure all expected columns exist (fill with 0 if not)
for col in quality_elements:
    if col not in df.columns:
        df[col] = 0


# Convert count data to presence-only (1 if ≥1, else 0)
df_binary = df.copy()
df_binary[quality_elements] = df_binary[quality_elements].gt(0).astype(int)

# Compute quality score: number of unique elements present
df_binary['quality_score'] = df_binary[quality_elements].sum(axis=1)



# Critical elements that identify a bus stop
critical = ['bas_road_marking', 'board_sign', 'shelter', 'stop_sign']
# Override score: if NONE of the 4 critical elements exist → score = 0
df_binary.loc[df_binary[critical].sum(axis=1) == 0, 'quality_score'] = 0


# Save to CSV
df_binary.to_csv('busstop_quality_scores.csv', index=False)

# Compute stats
mean_score = df_binary['quality_score'].mean()
median_score = df_binary['quality_score'].median()

# Print how many there are of each score (optional)
# print(df_binary['quality_score'].value_counts().sort_index())

# Plot histogram
plt.figure(figsize=(10, 5))
# n, bins, patches = plt.hist(df_binary['quality_score'], bins=range(0, 10), color='darkblue', edgecolor='black', rwidth=0.95)

plt.hist(df_binary['quality_score'], bins=np.arange(-0.5, 10.5, 1), color='darkblue', edgecolor='black', rwidth=0.95)
plt.xticks(range(0, 10))


# Plot mean and median lines
plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
plt.axvline(median_score, color='skyblue', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')

# Title and labels
plt.title('🇲🇾 Distribution of Malaysia Bus Stop Quality Scores (0–9)')
plt.xlabel('Quality Score')
plt.ylabel('Number of Bus Stops')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('quality_distribution_histogram.png', dpi=300)
plt.show()

# Print average
print(f"🇲🇾 Average Bus Stop Quality Score: {mean_score:.2f}/10")

