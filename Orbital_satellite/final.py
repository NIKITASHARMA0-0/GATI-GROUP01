#!/usr/bin/env python
# coding: utf-8

# In[100]:


from skyfield.api import load, EarthSatellite
import numpy as np
import plotly.graph_objects as go
import streamlit as st


# In[ ]:


st.set_page_config(page_title="Satellite Orbit Visualizer", layout="wide")

st.title("🌍 Satellite Orbit Visualization")
st.write("This app visualizes satellite orbits around Earth using TLE data.")


# In[101]:


ts = load.timescale()
satellites = load.tle_file("https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=tle")[:10] 


# In[97]:


days = np.arange(1, 31)
hours = [0, 6, 12, 18, 24]
times = [ts.utc(2025, 7, d, h) for d in days for h in hours]

sat_data = {}
for sat in satellites:
    positions = np.array([sat.at(t).position.km for t in times])
    subpoints = [sat.at(t).subpoint() for t in times]
    lats = [sp.latitude.degrees for sp in subpoints]
    lons = [sp.longitude.degrees for sp in subpoints]
    alts = [sp.elevation.km for sp in subpoints]
    sat_data[sat.name] = {
        "positions": positions,
        "lat": lats,
        "lon": lons,
        "alt": alts
    }


# In[99]:


R_EARTH_KM = 6378.137

all_sats = list(sat_data.keys())[:10]

min_len = min(len(np.asarray(sat_data[name]['positions'])) for name in all_sats)

sat_positions = {
    name: np.asarray(sat_data[name]['positions'], dtype=float)[:min_len]
    for name in all_sats
}

def make_earth(radius=R_EARTH_KM, n_lat=60, n_lon=120):
    lat = np.linspace(-np.pi/2, np.pi/2, n_lat)
    lon = np.linspace(-np.pi, np.pi, n_lon)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    xe = radius * np.cos(lat_grid) * np.cos(lon_grid)
    ye = radius * np.cos(lat_grid) * np.sin(lon_grid)
    ze = radius * np.sin(lat_grid)
    return xe, ye, ze

earth_x, earth_y, earth_z = make_earth()
earth_surface = go.Surface(
    x=earth_x, y=earth_y, z=earth_z,
    colorscale="YlGnBu", opacity=0.6, showscale=False,
    hoverinfo="skip", name="Earth"
)

colors = ["red", "orange", "cyan", "yellow", "lime",
          "magenta", "aqua", "violet", "gold", "brown"]

data = [earth_surface]
for i, name in enumerate(all_sats):
    pos = sat_positions[name]
    c = colors[i % len(colors)]

    data.append(go.Scatter3d(
        x=[pos[0, 0]], y=[pos[0, 1]], z=[pos[0, 2]],
        mode="markers",
        marker=dict(size=6, color="black", symbol="diamond"),  
        name=f"{name} Satellite"
    ))

    data.append(go.Scatter3d(
        x=[], y=[], z=[],
        mode="lines", line=dict(width=2, color=c),
        name=f"{name} Trail"
    ))

fig = go.Figure(data=data)

frames = []
trail_len = 40

for i in range(min_len):
    frame_data = []
    for si, name in enumerate(all_sats):
        pos = sat_positions[name]
        start = max(0, i - trail_len)
        # satellite marker
        frame_data.append(go.Scatter3d(
            x=[pos[i, 0]], y=[pos[i, 1]], z=[pos[i, 2]],
            mode="markers",
            marker=dict(size=6, color="black", symbol="diamond")
        ))

        frame_data.append(go.Scatter3d(
            x=pos[start:i+1, 0], y=pos[start:i+1, 1], z=pos[start:i+1, 2],
            mode="lines", line=dict(width=2, color=colors[si % len(colors)])
        ))

    frames.append(go.Frame(
        data=frame_data,
        name=str(i),
        traces=list(range(1, len(data))) 
    ))

fig.frames = frames

play_args = dict(frame=dict(duration=30, redraw=True),
                 transition=dict(duration=0),
                 fromcurrent=True, mode="immediate")
pause_args = dict(frame=dict(duration=0, redraw=False),
                  transition=dict(duration=0),
                  mode="immediate")

fig.update_layout(
    title="Multi-Satellite Orbit Animation",
    scene=dict(
        bgcolor="white",  
        aspectmode="data",
        xaxis=dict(showbackground=True, backgroundcolor="white"),
        yaxis=dict(showbackground=True, backgroundcolor="white"),
        zaxis=dict(showbackground=True, backgroundcolor="white")
    ),
    showlegend=True,
    margin=dict(l=0, r=0, t=40, b=0),
    updatemenus=[dict(
        type="buttons", showactive=False, x=0, y=1.05,
        buttons=[
            dict(label="▶ Play", method="animate", args=[None, play_args]),
            dict(label="⏸ Pause", method="animate", args=[[None], pause_args])
        ]
    )]
)

st.plotly_chart(fig, use_container_width=True)


# In[ ]:




