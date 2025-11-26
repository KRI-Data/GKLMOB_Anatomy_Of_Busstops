import pandas as pd
import folium
import branca.colormap as cm

# --- Load your data ---
df = pd.read_csv('busstop_quality_with_coordinates.csv')

# Drop stops with missing coordinates
df = df.dropna(subset=['final_lat', 'final_lon'])

print(f"✅ Stops left: {len(df)}")

# --- Create a color scale ---
# Red = low, Yellow = medium, Dark Green = high
colormap = cm.LinearColormap(
    colors=['red', 'yellow', 'green'],
    vmin=0,
    vmax=10
).to_step(10)  # optional: discrete steps

# --- Create Folium map ---
m = folium.Map(
    location=[df['final_lat'].mean(), df['final_lon'].mean()],
    zoom_start=12
)

# --- Add CircleMarkers ---
for _, row in df.iterrows():
    score = row['quality_score_10']
    color = colormap(score)
    
    popup_text = (
        f"<b>Stop ID:</b> {row['stop_id']}<br>"
        f"<b>Stop Name:</b> {row['stop_name']}<br>"
        f"<b>Quality Score:</b> {score:.2f}"
    )
    
    folium.CircleMarker(
        location=[row['final_lat'], row['final_lon']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# --- Add the legend ---
colormap.caption = 'Bus Stop Quality Score (0 = Poor, 10 = Good)'
colormap.add_to(m)

# --- Save map ---
m.save('busstop_quality_map_colored.html')

print("✅ Map saved as 'busstop_quality_map_colored.html'")
