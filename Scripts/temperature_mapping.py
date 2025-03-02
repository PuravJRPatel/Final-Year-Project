import os
import xarray as xr
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree

grid_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp"
temperature_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Temperature"
output_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Scripts\Average_Temperature"

grid = gpd.read_file(grid_path)

grid["centroid"] = grid.geometry.centroid
grid_points = np.array([(p.y, p.x) for p in grid["centroid"]])

for year in range(2000, 2024):
  print(f'Processing Temperature Data for {year}')
  temperature_file = os.path.join(temperature_folder, f"Maxtemp_MaxT_{year}.nc")
  if not os.path.exists(temperature_file):
        print(f"File not found: {temperature_file}, skipping year {year}")
        continue
  
  temperature_ds = xr.open_dataset(temperature_file)
  avg_temperature = temperature_ds["temperature"].mean(dim="time").compute()
  avg_temperature_file = os.path.join(output_folder, f"Average_temperature_{year}.nc")
  avg_temperature.to_netcdf(avg_temperature_file)
  temperature_ds = xr.open_dataset(avg_temperature_file)
  lat = temperature_ds["lat"].values
  lon = temperature_ds["lon"].values
  temperature = temperature_ds["temperature"].values  
  temperature_points = np.array([(lat[i], lon[j]) for i in range(len(lat)) for j in range(len(lon))])
  temperature_values = temperature.flatten()
  tree = cKDTree(temperature_points)
  _, idx = tree.query(grid_points)
  grid[f"temperature_{year}"] = temperature_values[idx]

grid = grid.drop(columns=["centroid"])

output_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_temperature.geojson"
grid.to_file(output_path, driver="GeoJSON")

print(f"Rainfall Mapping Completed! Data saved to: {output_path}")