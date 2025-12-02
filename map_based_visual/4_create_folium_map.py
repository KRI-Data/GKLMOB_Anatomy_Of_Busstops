import pandas as pd
import folium
import branca.colormap as cm

# --- Load your data ---
df = pd.read_csv('busstop_quality_with_coordinates.csv')

df = df.dropna(subset=['final_lat', 'final_lon'])
print(f"✅ Stops left: {len(df)}")

# --- Color scale ---
colormap = cm.LinearColormap(
    colors=['darkred', 'yellow', 'green'],
    vmin=0,
    vmax=8
).to_step(8)

# --- Black & white map ---
m = folium.Map(
    location=[df['final_lat'].mean(), df['final_lon'].mean()],
    zoom_start=12,
    tiles="CartoDB Positron"
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
        weight=1,             # <--- thinner outline
        fill=True,
        fill_color=color,
        fill_opacity=0.5,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# --- Add legend ---
colormap.caption = 'Bus Stop Quality Score (0 = Poor, 10 = Good)'
colormap.add_to(m)

# --- Save ---
m.save('busstop_quality_map_colored.html')
print("✅ Map saved as 'busstop_quality_map_colored.html'")
