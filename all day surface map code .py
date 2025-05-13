# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:39:11 2025

@author: molle
"""
#THIS LOOPS THROUGH ALL THE DAYS AND HOURS
import pygrib as grb
import matplotlib.pyplot as plt
import numpy as np
import cartopy
import cartopy.feature as cf 
import cartopy.crs as ccrs
import os

output_dir = 'allprecipmaps'
os.makedirs(output_dir, exist_ok=True)

#chagne this 
base_folder = 'c:/Users/molle/Documents/Comp Methods/GR6553/final project data'
 
for i in range(1,31):  # includes all june, change this
    days = str(i).zfill(2)  # ensures two-digit format
    folder = os.path.join(base_folder, f'200106{days}')  #change this  
    if not os.path.isdir(folder):
        print(f"Folder {folder} not found, skipping...")
        continue

    for h in range(0, 24):  # 00 to 23, change this
        hour_str = str(h).zfill(2)
        filename = f'wrfprs_d01_2001-06-{days}_{hour_str}.grb' #change this
        filepath = os.path.join(folder, filename)

        try:
            gribfile = grb.open(filepath)
            precipitation = gribfile[279]  # Adjust if index is incorrect
            lats, lons = precipitation.latlons()
            precip = precipitation.values / 25.4  # mm to inches

            fig = plt.figure(figsize=(8, 8))
            proj = ccrs.LambertConformal(central_longitude=-89.5,central_latitude=32.5,standard_parallels=(20., 20.))
            ax = plt.axes(projection=proj)
            ax.set_extent([-92., -87., 30., 35.5])
            ax.set_facecolor('white')

            ax.add_feature(cf.LAND, facecolor='wheat')
            ax.add_feature(cf.OCEAN, facecolor='lightblue')
            ax.add_feature(cf.BORDERS, edgecolor='brown')
            ax.add_feature(cf.COASTLINE, edgecolor='brown')
            ax.add_feature(cf.STATES, edgecolor='brown')
            ax.add_feature(cf.LAKES, color='lightblue', alpha=0.5)

            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--', color='black')
            gl.left_labels = False

            levels = [0.25, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
            rain = plt.contourf(lons, lats, precip, levels=levels, cmap='gist_ncar', transform=ccrs.PlateCarree())
            cbar = plt.colorbar(rain, orientation='horizontal')
            cbar.set_label('Accumulated precipitation (in)')

            plt.title(f"Accumulated Precipitation (in) - 2001-06-{days} {hour_str}Z", fontsize=14)
            plt.savefig(f"{output_dir}/precip_200106{days}_{hour_str}Z.png", dpi=150)
            plt.close()
            gribfile.close()
            print(f"Saved plot for 2001-06-{days} {hour_str}Z")

        except Exception as e:
            print(f"Failed to open or plot {filename} : {e}")
