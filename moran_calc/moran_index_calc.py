import pandas as pd
import numpy as np
from libpysal.weights import KNN
from esda.moran import Moran

# 1) Load CSV
df = pd.read_csv("busstop_quality_with_coordinates.csv")

# 2) Convert bad coordinates to NaN and drop them
df['final_lon'] = pd.to_numeric(df['final_lon'], errors='coerce')
df['final_lat'] = pd.to_numeric(df['final_lat'], errors='coerce')
df_clean = df[np.isfinite(df['final_lon']) & np.isfinite(df['final_lat'])]

# 3) Build coordinates array
coords = df_clean[['final_lon', 'final_lat']].to_numpy()

# 4) Build spatial weights (kNN)
w = KNN.from_array(coords, k=8)
w.transform = "r"  # row-standardize

# 5) Extract the variable
y = df_clean['quality_score_10'].values

# 6) Compute Moran's I
moran = Moran(y, w, permutations=999)

# 7) Print results
print("Moran's I:", moran.I)
print("Expected I under randomness:", moran.EI)
print("p-value (permutations):", moran.p_sim)
print("z-score (permutations):", moran.z_sim)
