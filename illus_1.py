import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# setting variables to be plotted
variable_1 = "energy_density"
variable_2 = "f_readymade"

# getting our grocery data
gro_dat = pd.read_csv("Area-level grocery purchases/year_borough_grocery.csv")
# getting the variables that we want for our analysis
col_dat = gro_dat[["area_id", variable_1, variable_2]]

# map of london
lon_map_df = gpd.read_file("London_Borough_Excluding_MHW.shp")
# map of london with data to be plotted
merged = lon_map_df.set_index("GSS_CODE").join(col_dat.set_index("area_id"))

# setting range for colourbar
vmin1, vmax1 = merged.min(axis=0)[variable_1], merged.max(axis=0)[variable_1]
vmin2, vmax2 = merged.min(axis=0)[variable_2], merged.max(axis=0)[variable_2]

# create figure and axes for Matplotlib
# fig, axs = plt.subplots(1, 2, figsize=(12, 6))
# option for vertical plotting
fig, axs = plt.subplots(2, 1, figsize=(12, 6))

# formatting
merged.plot(column=variable_1, cmap="Reds", linewidth=0.8, ax=axs[0], edgecolor="0.8")
merged.plot(column=variable_2, cmap="Oranges", linewidth=0.8, ax=axs[1], edgecolor="0.8")
axs[0].axis("off")
axs[1].axis("off")
plt.subplots_adjust(left=0, right=0.75, top=0.85, bottom=0.01)

# Create colorbar as a legend
sm_1 = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=vmin1, vmax=vmax1))
sm_2 = plt.cm.ScalarMappable(cmap="Oranges", norm=plt.Normalize(vmin=vmin2, vmax=vmax2))
# add the colorbar to the figure
cbar_1 = plt.colorbar(ax=axs[0], mappable=sm_1, fraction=0.038)
cbar_2 = plt.colorbar(ax=axs[1], mappable=sm_2, fraction=0.038)

plt.show()