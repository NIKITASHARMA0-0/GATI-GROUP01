#getting the animation of the ten satellites over a month

from skyfield.api import EarthSatellite, load, utc
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Satellite Orbit Animation", layout="wide")
st.title("🛰 10 Satellites Orbit Visualization over a Month")

# Starter TLE data (10 satellites)
tle_raw_data = [
  """ISS (ZARYA)
1 25544U 98067A   25233.12345678  .00001234  00000+0  12345-4 0  9991
2 25544  51.6430 160.4574 0003580 140.6673 205.7250 15.50957674 45212""",
  
  """NOAA 19
1 33591U 09005A   25233.23456789  .00000023  00000+0  34567-5 0  9995
2 33591  99.1967 212.3456 0012345 321.6543  38.7654 14.12456789 56789""",
  
  """HUBBLE SPACE TELESCOPE
1 20580U 90037B   25233.34567890  .00000567  00000+0  67890-5 0  9996
2 20580  28.4697 123.4567 0002954  45.6789 314.3210 15.09123456 67890""",
  
  """LANDSAT 8
1 39084U 13008A   25233.45678901  .00000089  00000+0  45678-5 0  9992
2 39084  98.2054 145.6789 0001432 250.9876 109.1234 14.57123456 78901""",
  
  """TERRA
1 25994U 99068A   25233.56789012  .00000123  00000+0  23456-5 0  9997
2 25994  98.2054 200.5678 0001234  80.4567 279.5432 14.57123456 89012""",
  
  """AQUA
1 27424U 02022A   25233.67890123  .00000145  00000+0  34567-5 0  9998
2 27424  98.2054 250.6789 0002345 150.8765 209.6543 14.57123456 90123""",
  
  """NOAA 15
1 25338U 98030A   25233.78901234  .00000101  00000+0  12345-5 0  9993
2 25338  98.5336 265.6789 0010950 145.7140 214.4750 14.27013376 91234""",
  
  """NOAA 18
1 28654U 05018A   25233.89012345  .00000076  00000+0  63584-4 0  9991
2 28654  98.8395 311.1234 0013149 286.4823  73.4904 14.13628417 92345""",
  
  """GPS BIIR-2 (PRN 13)
1 24876U 97035A   25233.90123456 -.00000030  00000+0  00000+0 0  9998
2 24876  55.8345 110.3944 0094273  55.6399 305.3151  2.00562645 93456""",
  
  """COSMOS 2251
1 22675U 93036A   25233.01234567  .00000045  00000+0  56789-5 0  9999
2 22675  82.9260  98.6543 0012345 250.9876 109.1234 13.47023456 94567"""
]

ts = load.timescale()
satellites = {}
for tle in tle_raw_data:
    lines = tle.splitlines()
    name, l1, l2 = lines[0].strip(), lines[1].strip(), lines[2].strip()
    satellites[name] = EarthSatellite(l1, l2, name, ts)

end_time = datetime.now(tz=utc)
start_time = end_time - timedelta(days=30)
step = timedelta(hours=3)

times = []
cur = start_time
while cur <= end_time:
    times.append(ts.utc(cur))
    cur += step

positions = {}
for name, sat in satellites.items():
    pos = [sat.at(t).position.km for t in times]
    xs, ys, zs = zip(*pos)
    positions[name] = (xs, ys, zs)

colors = ["red","blue","green","orange","purple",
          "cyan","magenta","yellow","pink","brown"]

data_init = []
orbit_lines = []
for i, (name, (xs, ys, zs)) in enumerate(positions.items()):
    col = colors[i % len(colors)]
    data_init.append(go.Scatter3d(
        x=[xs[0]], y=[ys[0]], z=[zs[0]],
        mode="markers", marker=dict(size=5, color=col), name=name
    ))
    orbit_lines.append(go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode="lines", line=dict(color=col, width=1),
        name=f"{name} path", opacity=0.3
    ))

u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
earth_x = 6371 * np.cos(u) * np.sin(v)
earth_y = 6371 * np.sin(u) * np.sin(v)
earth_z = 6371 * np.cos(v)
earth = go.Surface(x=earth_x, y=earth_y, z=earth_z,
                   colorscale="Blues", opacity=0.6, showscale=False)

frames = []
for k in range(len(times)):
    frame_data = []
    for i, (name, (xs, ys, zs)) in enumerate(positions.items()):
        col = colors[i % len(colors)]
        frame_data.append(go.Scatter3d(
            x=[xs[k]], y=[ys[k]], z=[zs[k]],
            mode="markers",
            marker=dict(size=6, color=col),
            name=name
        ))
    frames.append(go.Frame(data=frame_data, name=str(k)))

fig = go.Figure(
    data=data_init + orbit_lines + [earth],
    frames=frames,
    layout=go.Layout(
        title="Satellite Orbits Over 30 Days",
        scene=dict(
            xaxis=dict(range=[-12000,12000]),
            yaxis=dict(range=[-12000,12000]),
            zaxis=dict(range=[-12000,12000]),
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        updatemenus=[dict(
            type="buttons",
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, {"frame": {"duration": 100, "redraw": True},
                                  "fromcurrent": True}]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate"}])
            ]
        )]
    )
)

st.plotly_chart(fig, use_container_width=True)
