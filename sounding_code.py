# -*- coding: utf-8 -*-
"""
Created on Mon May 12 16:18:08 2025

@author: molle
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import pandas_dataframe_to_unit_arrays, units
import numpy as np
from siphon.simplewebservice.wyoming import WyomingUpperAir
from metpy.calc import lcl, parcel_profile, cape_cin
import os

#infromation to change based off your location and times needed
station = 'JAN'
start_date = datetime(2001, 6, 1, 12)
end_date = datetime(2001, 6, 30, 12)

# Output directory- change for desired name
output_dir = 'sounding_plots'
os.makedirs(output_dir, exist_ok=True)

# Loop through each day
current_date = start_date
while current_date <= end_date:
    try:
        # Request and convert data
        df = WyomingUpperAir.request_data(current_date, station)
        data = pandas_dataframe_to_unit_arrays(df)

        p = data['pressure']
        T = data['temperature']
        Td = data['dewpoint']
        u = data['u_wind']
        v = data['v_wind']

        # Surface values
        p_sfc = p[0]
        T_sfc = T[0]
        Td_sfc = Td[0]

        # Compute LCL and parcel profile
        lcl_pressure, lcl_temperature = lcl(p_sfc, T_sfc, Td_sfc)
        parcel_prof = parcel_profile(p, T_sfc, Td_sfc).to('degC')

        # Compute CAPE and CIN
        cape, cin = cape_cin(p, T, Td, parcel_prof)
        print(f"{current_date.strftime('%Y-%m-%d %HZ')}: CAPE = {cape.m:.1f} J/kg, CIN = {cin.m:.1f} J/kg")

        # Create figure and Skew-T
        fig = plt.figure(figsize=(9, 11))
        skew = SkewT(fig, rotation=45)

        # Plot temperature, dewpoint, wind, and parcel trace
        skew.plot(p, T, 'r')
        skew.plot(p, Td, 'g')
        skew.plot(p, parcel_prof, 'k', linewidth=2, label='Parcel Path')
        skew.ax.plot(lcl_temperature.to('degC'), lcl_pressure, 'ko', label='LCL')
        skew.plot_barbs(p[::3], u[::3], v[::3], y_clip_radius=0.03)

        # Axes limits
        skew.ax.set_xlim(-30, 40)
        skew.ax.set_ylim(1020, 100)

        # Thermodynamic reference lines
        skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K, alpha=0.25, color='orangered')
        skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K, alpha=0.25, color='tab:green')
        skew.plot_mixing_lines(linestyle='dotted', color='tab:blue')

        # Titles
        plt.title(f'{station} Sounding', loc='left')
        plt.title(f'Valid Time: {current_date.strftime("%Y-%m-%d %HZ")}', loc='right')

        # Save plot
        filename = f"{station}_{current_date.strftime('%Y%m%d_%HZ')}.png"
        plt.savefig(os.path.join(output_dir, filename), dpi=150)
        plt.close()
        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Failed for {current_date.strftime('%Y-%m-%d')}: {e}")

    current_date += timedelta(days=1)
