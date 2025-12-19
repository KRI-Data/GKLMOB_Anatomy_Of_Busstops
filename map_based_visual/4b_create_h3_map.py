import pandas as pd
import folium
import h3
import branca.colormap as cm
import os

""" Script to create an H3 hexagon map of bus stop quality scores """

# --- 1. Load bus stop data ---
df = pd.read_csv("busstop_quality_with_coordinates.csv")
df = df.dropna(subset=["final_lat", "final_lon"])

# --- 2. H3 resolution ---
h3_res = 7

# --- 3. Map each bus stop to an H3 cell ---
df['hex_id'] = df.apply(lambda row: h3.latlng_to_cell(row['final_lat'], row['final_lon'], h3_res), axis=1)


# --- 4. Aggregate data per hex cell ---
hex_scores = df.groupby('hex_id')['quality_score'].mean().reset_index().rename(columns={'quality_score': 'avg_quality'})

# --- 5. Prepare color scale ---
colormap = cm.LinearColormap(
    colors=['darkred', 'yellow', 'green'],
    vmin=0,
    vmax=9
).to_step(9)
colormap.caption = 'Bus Stop Quality Score (0 = Poor, 9 = Good)'

# --- 6. Build Folium map (black and white) ---
m = folium.Map(
    location=[df['final_lat'].mean(), df['final_lon'].mean()],
    zoom_start=12,
    tiles='CartoDB Positron',
    control_scale=True
)

# --- 7. Add hexagons to map ---
for _, row in hex_scores.iterrows():
    boundary = h3.cell_to_boundary(row['hex_id'])
    # boundary is list of (lat, lng) pairs
    folium.Polygon(
        locations=[(lat, lng) for lat, lng in boundary],
        color='black',
        weight=0.4,
        fill=True,
        fill_color=colormap(row['avg_quality']),
        fill_opacity=0.7,
        popup=f"Avg Quality: {row['avg_quality']:.2f}"
    ).add_to(m)




# --- 8. Add vertical legend that matches the map colors ---

legend_html = """
<div style="
    position: fixed;
    top: 50px;
    right: 50px;
    height: 350px;
    display: flex;
    flex-direction: column;
    z-index: 9999;
    font-size: 12px;
">
  <!-- Title -->
  <div style="
      margin-bottom: 5px;
      font-weight: bold;
      text-align: left;
  ">
    Bus Stop Quality Score (0 = Poor, 9 = Good)
  </div>
  
  <!-- Discrete color boxes + numbers aligned bottom right -->
  <div style="
      display: flex;
      align-items: flex-end;  /* push gradient + numbers to bottom */
      justify-content: flex-end; /* right align */
      height: 100%;
  ">
    <!-- Discrete color boxes -->
    <div style="
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 20px;
        border: 1px solid black;
        border-radius: 5px;
        overflow: hidden;
    ">
        <div style="flex:1; background:#008000ff;"></div>    <!-- 9 -->
        <div style="flex:1; background:#3fa000ff;"></div>    <!-- 8 -->
        <div style="flex:1; background:#7fc000ff;"></div>    <!-- 7 -->
        <div style="flex:1; background:#bfe000ff;"></div>    <!-- 6 -->
        <div style="flex:1; background:#ffff00ff;"></div>    <!-- 5 -->
        <div style="flex:1; background:#e2bf00ff;"></div>    <!-- 4 -->
        <div style="flex:1; background:#c57f00ff;"></div>    <!-- 3 -->
        <div style="flex:1; background:#a83f00ff;"></div>    <!-- 2 -->
        <div style="flex:1; background:#8b0000ff;"></div>    <!-- 1 -->
        <div style="flex:1; background:#8b0000ff;"></div>    <!-- 0 -->

    </div>
    
    <!-- Numbers on the side -->
    <div style="
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-left: 5px;
        height: 100%;
        font-weight: bold;
        color: black;
    ">
      <div>9</div>
      <div>8</div>
      <div>7</div>
      <div>6</div>
      <div>5</div>
      <div>4</div>
      <div>3</div>
      <div>2</div>
      <div>1</div>
      <div>0</div>
    </div>
  </div>
</div>
"""


# Inject into Folium map
m.get_root().html.add_child(folium.Element(legend_html))

# --- Save to file ---
output_dir = "h3_map_html"
os.makedirs(output_dir, exist_ok=True)

m.save(os.path.join(output_dir, "index.html"))

print("✅ Map saved as 'h3_map_html/index.html'")
