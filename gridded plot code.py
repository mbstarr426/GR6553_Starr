# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:40:51 2025

@author: molle
"""
#MAKE GRIDDED PLOT WITH 2 VARIABLES
import os
import pygrib
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
from datetime import datetime

#change this for your file/folder
base_folder = 'c:/Users/molle/Documents/Comp Methods/GR6553/final project data'

for i in range(1, 31):  # replace with the number of days in your folder
    day_str = str(i).zfill(2)
    folder = os.path.join(base_folder, f'200106{day_str}')

    if not os.path.isdir(folder):
        print(f"Folder {folder} not found, skipping...")
        continue

    for h in range(0, 24):  # Every hour of data you have for the day
        hour_str = str(h).zfill(2)
        filename = f'wrfprs_d01_2001-06-{day_str}_{hour_str}.grb'
        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            print(f"{filename} not found, skipping...")
            continue

        try:
            grbs = pygrib.open(filepath)

            height500 = grbs.select(name='Geopotential height', level=850)[0]
            temp500 = grbs.select(name='Temperature', level=850)[0]
            rh500 = grbs.select(name='Relative humidity', level=850)[0]

            z = height500.values / 10  # meters to decameters
            t = temp500.values - 273.15  # K to °C
            rh = rh500.values
            lats, lons = height500.latlons()

            dt_obj = datetime(2001, 6, i, h)
            timestamp_str = dt_obj.strftime('%Y%m%d_%H%M')

            # Plotting
            fig=plt.figure(figsize=(8, 8))
            proj=ccrs.LambertConformal(central_longitude=-89.5,central_latitude=32.5,standard_parallels=(20.,20.))
            ax=plt.axes(projection=proj)
            ax.set_extent([-92.,-87.,30.,35.5])
            ax.add_feature(cf.LAND, color='wheat')
            ax.add_feature(cf.OCEAN, color='lightblue')
            ax.add_feature(cf.LAKES, color='lightblue')
            ax.add_feature(cf.BORDERS, edgecolor='gray')
            ax.add_feature(cf.COASTLINE, edgecolor='gray')
            ax.add_feature(cf.STATES, edgecolor='gray')

            gl = ax.gridlines(draw_labels=True, linewidth=1, alpha=0.5, linestyle='--', color='white')
            gl.top_labels = False
            gl.right_labels = False

            rh_levels = np.arange(70, 101, 5)
            rh_contour = plt.contourf(lons, lats, rh, levels=rh_levels, cmap='YlGn', transform=ccrs.PlateCarree())
            
            temp_levels = np.arange(-10,120,2)
            temp_contour = plt.contour(lons, lats, t, levels=temp_levels, colors='red', linewidths=3, transform=ccrs.PlateCarree())
            plt.clabel(temp_contour, inline=1, fontsize=8, fmt='%.0f°C', colors='black')

            z_contour = plt.contour(lons, lats, z, levels=np.arange(845, 860), colors='black', linewidths=1.2, transform=ccrs.PlateCarree())
            plt.clabel(z_contour, inline=1, fontsize=9, fmt='%i')

            
            cbar = plt.colorbar(rh_contour, orientation='horizontal', pad=0.05)
            cbar.set_label('Relative Humidity (%)')
           
            plt.title(f'WRF 850 hPa Height, Temp, RH\n{dt_obj.strftime("%Y-%m-%d %H UTC")}')
            plt.tight_layout()

            # Save plot
            output_dir = 'humidity'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f'{output_dir}/wrf_500mb_{timestamp_str}.png', dpi=150)
            plt.show()
            plt.close()

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue
