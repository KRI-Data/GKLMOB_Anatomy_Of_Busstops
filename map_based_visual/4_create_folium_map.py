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
    vmax=9
).to_step(9)

# --- Black & white map ---
m = folium.Map(
    location=[df['final_lat'].mean(), df['final_lon'].mean()],
    zoom_start=12,
    tiles="CartoDB Positron"
)

# --- Add CircleMarkers ---
for _, row in df.iterrows():
    score = row['quality_score']
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


# Make legend vertical
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



# --- Save ---
m.save('busstop_quality_map_colored.html')
print("✅ Map saved as 'busstop_quality_map_colored.html'")
