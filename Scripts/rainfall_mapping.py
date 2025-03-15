import os
import xarray as xr
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree

# Paths
grid_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp"
rainfall_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Rainfall"
output_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Scripts\Average_Rainfall"

# Load Grid
grid = gpd.read_file(grid_path)

# Compute grid centroids for mapping
grid["centroid"] = grid.geometry.centroid
grid_points = np.array([(p.y, p.x) for p in grid["centroid"]])


for year in range(2000, 2024):
    print(f"Processing Rainfall Data for {year}...")

    # Load rainfall data
    rainfall_file = os.path.join(rainfall_folder, f"RF25_ind{year}_rfp25.nc")
    
    if not os.path.exists(rainfall_file):
        print(f"File not found: {rainfall_file}, skipping year {year}")
        continue  # Skip this year if file is missing

    rainfall_ds = xr.open_dataset(rainfall_file)


    avg_rainfall = rainfall_ds["RAINFALL"].mean(dim="TIME").compute()  
    avg_rainfall = avg_rainfall.fillna(0)  


    avg_rainfall_file = os.path.join(output_folder, f"Average_Rainfall_{year}.nc")
    avg_rainfall.to_netcdf(avg_rainfall_file)


    rainfall_ds = xr.open_dataset(avg_rainfall_file)


    lat = rainfall_ds["LATITUDE"].values
    lon = rainfall_ds["LONGITUDE"].values
    rainfall = rainfall_ds["RAINFALL"].values  


    rainfall_points = np.array([(lat[i], lon[j]) for i in range(len(lat)) for j in range(len(lon))])
    rainfall_values = rainfall.flatten()

    tree = cKDTree(rainfall_points)
    _, idx = tree.query(grid_points)
    grid[f"rainfall_{year}"] = rainfall_values[idx]


grid = grid.drop(columns=["centroid"])

output_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_rainfall.geojson"
grid.to_file(output_path, driver="GeoJSON")

print(f"Rainfall Mapping Completed! Data saved to: {output_path}")
