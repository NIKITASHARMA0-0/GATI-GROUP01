LIVE LINK
"https://genaisatellite.streamlit.app/"

# Satellite Orbit Visualization

This project visualizes the **3D orbital paths of 10 satellites** around Earth over the past 30 days.  
It uses **Skyfield** for satellite orbit calculations, **Plotly** for interactive 3D visualization,  
and **Streamlit** for the web interface.

---

## 🚀 Features
- Loads TLE (Two-Line Element) satellite orbital data
- Computes satellite positions (X, Y, Z in km) for the past 30 days
- Plots satellite trajectories in 3D with **Plotly**
- Animates real-time orbit motion
- Interactive controls (play/pause)
- Visual Earth sphere as reference

---

## 📦 Requirements

Make sure you have Python 3.8+ installed. Install dependencies with:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
streamlit
skyfield
plotly
numpy
```

---

## ▶️ Running the App

Run the Streamlit app with:

```bash
streamlit run genai.py
```

This will start a local web server. Open the provided URL in your browser to see the visualization.

---

## 📂 Project Structure
```
.
├── genai.py                # Main application code
├── README.md               # Project documentation
├── requirements.txt        # Dependencies
```

---

## 🌍 Visualization

- Satellites are shown as colored dots moving along their orbital paths.
- Each orbit is displayed with a unique color line.
- Earth is rendered as a 3D sphere (radius = 6371 km).

---

## 🛰️ Satellites Included
- ISS (ZARYA)
- NOAA 19
- HUBBLE SPACE TELESCOPE
- LANDSAT 8
- TERRA
- AQUA
- NOAA 15
- NOAA 18
- GPS BIIR-2 (PRN 13)
- COSMOS 2251

---

## 🙌 Acknowledgements
- [Celestrak](https://celestrak.org/) for providing TLE data
- [Skyfield](https://rhodesmill.org/skyfield/) for orbital mechanics
- [Plotly](https://plotly.com/) for visualization
- [Streamlit](https://streamlit.io/) for app deployment
