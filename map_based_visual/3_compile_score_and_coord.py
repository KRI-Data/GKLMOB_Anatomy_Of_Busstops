import pandas as pd


""" Script to merge bus stop quality scores with coordinates"""
# --- 1. Load your files ---
# Data A: TXT coordinates
df_A = pd.read_csv('busstop_coordinates.txt')

# Data B: XLSX coordinates
df_B = pd.read_excel('busstop_coordinates_B.xlsx')

# Scores: already processed with binary presence + score
df_scores = pd.read_csv('busstop_quality_scores.csv')

# --- 2. Merge scores with Data A (stop_name, lat, lon) ---
merged_A = df_scores.merge(
    df_A[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']],
    on='stop_id',
    how='left'
)

# --- 3. Merge scores with Data B (lat, lng, name) ---
merged_B = df_scores.merge(
    df_B[['id', 'lat', 'lng', 'name']],
    left_on='stop_id', right_on='id',
    how='left'
)

# --- 4. Combine: prefer Data B where available ---
final = merged_A.copy()

# Use Data B's name if available, else A
final['final_stop_name'] = merged_B['name'].combine_first(final['stop_name'])

# Use Data B's lat/lon if available, else A
final['final_lat'] = merged_B['lat'].combine_first(final['stop_lat'])
final['final_lon'] = merged_B['lng'].combine_first(final['stop_lon'])

# --- 5. Select and reorder columns ---
# Find your infrastructure element columns (elements of bus stop)
infra_cols = [col for col in df_scores.columns if col not in ['stop_id', 'quality_score']]

output_cols = ['stop_id', 'final_stop_name', 'final_lon', 'final_lat', 'quality_score'] + infra_cols

final_out = final[output_cols].rename(columns={'final_stop_name': 'stop_name'})

# --- 6. Save final compiled CSV ---
final_out.to_csv('busstop_quality_with_coordinates.csv', index=False)

print("✅ Combined CSV saved: 'busstop_quality_with_coordinates.csv'")
