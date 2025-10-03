from skyfield.api import EarthSatellite, load, utc
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

ts = load.timescale()

with open(r'C:\Users\yeeshika\gatiWeek1\ActiveTLE.txt', 'r') as ActiveTLE:
    allLines = ActiveTLE.readlines()
    
    satName = open(r'C:\Users\yeeshika\gatiWeek1\satName.txt', 'w')
    rows = []
    times = []
    end_time = datetime.now(tz = utc)     ###
    start_time = end_time - timedelta(days=30)
    delta = timedelta(minutes=15)

    while start_time <= end_time :  #list of time

        times.append(ts.utc(start_time))
        start_time += delta

    print(len(times))

    for i in range(0, len(allLines), 3): ###
        name = allLines[i].strip()
        line1 = allLines[i+1].strip()
        line2 = allLines[i+2].strip()
        
        satName.write(f"{name}\n")

        sat_info = EarthSatellite(line1, line2, name, ts)

        for time in times :
            geo = sat_info.at(time)
            pos = geo.position.km
            rows.append({
                "satellite": name,
                "x": pos[0],
                "y": pos[1],
                "z": pos[2]
            })

    df = pd.DataFrame(rows)
    df.to_parquet(r"C:\Users\yeeshika\gatiWeek1\posOfSat.parquet", engine="pyarrow", index=False)
    
        
    