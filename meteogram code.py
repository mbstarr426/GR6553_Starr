# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:40:16 2025

@author: molle
"""
#Making the meteograms for the month
import pygrib
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

#change this for your data location
base_folder = 'c:/Users/molle/Documents/Comp Methods/GR6553/final project data'

# Lists to hold time series
times = []
temps = []
dewpoints = []
precips = []
wind_speeds = []
rhs = []

# Loop over days
for i in range(1, 31):  # June 1–30, fill in your amount of time
    day_str = str(i).zfill(2)
    folder = os.path.join(base_folder, f'200106{day_str}') #adjust for your folder names
    
    if not os.path.isdir(folder):
        print(f"Folder {folder} not found, skipping...")
        continue

    # Loop over each hour
    for h in range(0, 24): #hours of data
        hour_str = str(h).zfill(2)
        filename = f'wrfprs_d01_2001-06-{day_str}_{hour_str}.grb' #adjust for your file names
        filepath = os.path.join(folder, filename)

        try:
            grbs = pygrib.open(filepath)
            
            # Temperature and Dewpoint (2m)
            temp = grbs.select(name='Temperature', level=2)[0].values
            td = grbs.select(name='Dew point temperature', level=2)[0].values

            # Precipitation (accumulated), convert to inches
            precip = grbs[279].values / 25.4  # mm to inches

            # U/V wind components at 10m
            u = grbs[333].values
            v = grbs[334].values
            wind_speed = np.sqrt(u**2 + v**2)

            # Relative Humidity at 2m
            rh = grbs[274].values

            # Choose central grid point
            i_c, j_c = temp.shape[0] // 2, temp.shape[1] // 2
            dt_obj = datetime(2001, 6, i, h)

            # Append values from central grid point
            times.append(dt_obj)
            temps.append(temp[i_c, j_c])
            dewpoints.append(td[i_c, j_c])
            precips.append(precip[i_c, j_c])
            wind_speeds.append(wind_speed[i_c, j_c])
            rhs.append(rh[i_c, j_c])

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Temp & Dewpoint
axs[0].plot(times, temps, label='Temp (K)', color='red')
axs[0].plot(times, dewpoints, label='Dewpoint (K)', color='green')
axs[0].set_ylabel('Temperature (K)')
axs[0].legend()
axs[0].grid(True)
axs[0].set_title('2m Temperature and Dewpoint')

# RH and Wind Speed
axs[1].plot(times, rhs, label='RH (%)', color='blue')
axs[1].plot(times, wind_speeds, label='10m Wind Speed (m/s)', color='purple')
axs[1].set_ylabel('RH (%) / Wind Speed (m/s)')
axs[1].legend()
axs[1].grid(True)
axs[1].set_title('2m Relative Humidity and 10m Wind Speed')

# Precipitation
axs[2].bar(times, precips, width=0.03, color='dodgerblue')
axs[2].set_ylabel('Precip (in)')
axs[2].grid(True)
axs[2].set_title('Hourly Precipitation')

# Common x-axis
plt.xlabel('Date/Time (UTC)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()