# GR6553_Starr
This project contains a comprehensive Python-based analysis and visualization of high-resolution WRF (Weather Research and Forecasting) model output for June 2001, with a focus on central Mississippi.  The data is not uploaded due to its large number of files and research-specific nature. The work is part of a graduate-level meteorology course and includes several key components.

First, a script loops through daily 23Z surface files to produce daily accumulated precipitation maps using Cartopy for spatial visualization. Another script loops through every hour of every day in the month to visualize precipitation evolution more granularly.

Additional scripts generate upper-air soundings from Wyoming’s upper-air archive for Jackson, MS (JAN), plotted using MetPy’s Skew-T functionality. Scripts were originally written by unidata.github.io, but have edits in them to add a few things. There are indicators on places to change data for your selected location and time.

Meteograms were created from model output, displaying time series of 2-meter temperature, dew point, precipitation, 10-meter wind speed, and relative humidity at the central grid point.

Finally, gridded maps of 850 hPa temperature, geopotential height, and relative humidity were plotted for selected days, providing insight into mesoscale environments based on amounts of precipitation to look at convective thunderstorm potential. 

All scripts rely on pygrib, Cartopy, Matplotlib, MetPy, and NumPy, and are organized for batch processing and reproducibility. This project demonstrates skills in geospatial visualization, data processing, and atmospheric interpretation using Python tools commonly employed in operational and research meteorology.
