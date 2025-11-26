import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# Load bus stop quality scores
df_quality = pd.read_csv('busstop_quality_scores.csv')

# Load bus stop coordinates from your text/CSV file
df_coords = pd.read_csv('busstop_coordinates.txt')  

# Rename columns to match expected naming
df_coords = df_coords.rename(columns={'stop_lat': 'latitude', 'stop_lon': 'longitude'})

# Merge both dataframes on stop_id
df = pd.merge(df_quality, df_coords, on='stop_id')
# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.longitude, df.latitude), 
    crs="EPSG:4326"
).to_crs(epsg=3857)

import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

# Create grid for KDE
x = gdf.geometry.x
y = gdf.geometry.y
xy_sample = np.vstack([x, y]).T
weights = df['quality_score_10'].values

# Fit KDE
kde = KernelDensity(bandwidth=300, kernel='gaussian')
kde.fit(xy_sample, sample_weight=weights)

# Generate grid
x_min, x_max = x.min(), x.max()
y_min, y_max = y.min(), y.max()
xx, yy = np.mgrid[x_min:x_max:500j, y_min:y_max:500j]
grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T

# Evaluate KDE
zz = np.exp(kde.score_samples(grid_coords)).reshape(xx.shape)
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(zz.T, extent=(x_min, x_max, y_min, y_max), origin='lower', cmap='YlOrRd', alpha=0.6)
gdf.plot(ax=ax, markersize=1, color='blue', alpha=0.3)
ax.set_title("Kernel Density of Bus Stop Infrastructure")
plt.axis('off')
plt.show()