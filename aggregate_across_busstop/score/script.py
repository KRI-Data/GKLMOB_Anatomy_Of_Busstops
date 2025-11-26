import pandas as pd
import matplotlib.pyplot as plt

# Load aggregated detection results
df = pd.read_csv('aggregated_detections_per_stop.csv')

# Define infrastructure elements that count toward bus stop quality
quality_elements = ['bench', 'road_marking_sign', 'street_light', 'shelter', 'board_sign', 'stop_sign', 'trash_bin']

# Ensure all expected columns exist (fill with 0 if not)
for col in quality_elements:
    if col not in df.columns:
        df[col] = 0

# Convert count data to presence-only (1 if ≥1, else 0)
df_binary = df.copy()
df_binary[quality_elements] = df_binary[quality_elements].gt(0).astype(int)

# Compute quality score: number of unique elements present
df_binary['quality_score_raw'] = df_binary[quality_elements].sum(axis=1)

# Normalize score to a 0–10 scale
df_binary['quality_score_10'] = (df_binary['quality_score_raw'] / len(quality_elements)) * 10

# Save to CSV
df_binary.to_csv('busstop_quality_scores.csv', index=False)

# Compute stats
mean_score = df_binary['quality_score_10'].mean()
median_score = df_binary['quality_score_10'].median()

# Plot histogram
plt.figure(figsize=(10, 5))
n, bins, patches = plt.hist(df_binary['quality_score_10'], bins=10, color='darkblue', edgecolor='black', rwidth=0.95)

# Plot mean and median lines
plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
plt.axvline(median_score, color='skyblue', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')

# Title and labels
plt.title('🇲🇾 Distribution of Malaysia Bus Stop Quality Scores (0–10)')
plt.xlabel('Quality Score')
plt.ylabel('Number of Bus Stops')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('quality_distribution_histogram.png', dpi=300)
plt.show()

# Print average
print(f"🇲🇾 Average Bus Stop Quality Score: {mean_score:.2f}/10")
