🛰️ Satellite Trajectory Visualizer

This project provides a tool to visualize and analyze satellite trajectories using orbital data (TLEs) and modern visualization libraries. It calculates positions, generates ground tracks, and displays 2D/3D visualizations of satellites moving around Earth.

🚀 Features

Load and parse TLE (Two-Line Element) data.
Calculate satellite position and velocity vectors using Skyfield.
Generate ground tracks (lat/lon projection on Earth’s surface).
Create 3D interactive orbit visualizations with Plotly.
Support for multiple satellites simultaneously.
Export processed trajectory data to CSV/JSON for further analysis.
Interactive Streamlit web app for real-time exploration.

🧩 Approach

The project follows these steps:

TLE Data Acquisition
Download TLEs (Two-Line Element sets) from trusted sources such as Celestrak
 or Space-Track.
Store them locally in JSON/CSV for reproducibility.
Orbit Propagation
Use Skyfield to interpret TLEs.
Compute satellite positions in Earth-Centered Inertial (ECI) coordinates over a defined time window.
Coordinate Transformation
Convert ECI coordinates into latitude, longitude, altitude (LLA) to track movement relative to Earth.
Ground Track Generation
Map LLA values on a 2D Earth map.
Save data as CSV for later plotting and analysis.
Orbit Visualization
Create 3D orbit plots around Earth with Plotly.
Show satellite paths dynamically.
Interactive Web Interface
Implemented via Streamlit.
Allows selection of satellites, time range, and visualization type.

here is the link:https://satellite-trajectory-jsaa35ufnstpkxqjtrb3v5.streamlit.app/
