import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import mplcursors

def generate_distinct_colors(N):
  cmap = plt.get_cmap('tab20')
  colors = [cmap(i) for i in np.linspace(0, 1, N)]
  return colors

df = pd.read_csv('./passes_lat_lon.csv')

pass_groups = df["Location"]
unique_groups = pass_groups.unique()

df_climbed = df.loc[df["Climbed"] == "Y"]

df_2000ers = df.loc[df["Height (m)"] >= 2000]
total_2000ers = len(df_2000ers)
#print(df_2000ers["Name of pass"])
df_2000ers_climbed = df_2000ers.loc[df_2000ers["Climbed"] == "Y"]
total_2000ers_climbed = len(df_2000ers_climbed)

distinct_colors = generate_distinct_colors(len(unique_groups))
pass_group_dict = dict(zip(unique_groups, distinct_colors))
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(20,15))


for group, group_df in df.groupby('Location'):
  ax.scatter(group_df["Longitude"], group_df["Latitude"], color=pass_group_dict[group], s=0.002*group_df['Height (m)'].apply(lambda x: x**1.5), label=group, edgecolor='black', transform=ccrs.PlateCarree())

ax.scatter(df_climbed["Longitude"], df_climbed["Latitude"], facecolors="None", s=0.0015*df_climbed['Height (m)'].apply(lambda x: x**1.5), edgecolors="gold", linewidths=2, transform=ccrs.PlateCarree())

scatter = ax.scatter(df["Longitude"], df["Latitude"], color="k", s=0.1*df['Height (m)'], alpha=0, transform=ccrs.PlateCarree())

df['combined_name'] = df['Name of pass'] + "\nAltitude: " + df['Height (m)'].astype(str) + "m\nLat: " + df["Latitude"].astype(str) + " N\nLon: " + df["Longitude"].astype(str) + " E"
pass_info = df['combined_name'].to_list()

mplcursors.cursor(scatter, hover=True).connect("add", lambda sel: sel.annotation.set_text(pass_info[sel.index]))

ax.add_feature(cfeature.BORDERS)
ax.coastlines()
ax.legend(loc='lower right')
ax.annotate("Climbed " + str(total_2000ers_climbed) + " 2000ers\nof " + str(total_2000ers) + " in the Alps", 
    xy=(1.2*df["Longitude"].min(), 0.9*df["Latitude"].max()),horizontalalignment='center',fontsize=16)
plt.show()
