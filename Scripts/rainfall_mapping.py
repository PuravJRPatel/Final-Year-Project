import os
import xarray as xr
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree

# Paths
grid_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp"
rainfall_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Rainfall"
output_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Scripts"

# Load Grid
grid = gpd.read_file(grid_path)

# Compute grid centroids for mapping
grid["centroid"] = grid.geometry.centroid
grid_points = np.array([(p.y, p.x) for p in grid["centroid"]])

# Iterate over all years
for year in range(2000, 2024):
    print(f"Processing Rainfall Data for {year}...")

    # Load rainfall data
    rainfall_file = os.path.join(rainfall_folder, f"RF25_ind{year}_rfp25.nc")
    
    if not os.path.exists(rainfall_file):
        print(f"File not found: {rainfall_file}, skipping year {year}")
        continue  # Skip this year if file is missing

    rainfall_ds = xr.open_dataset(rainfall_file)

    # Compute average rainfall over time
    avg_rainfall = rainfall_ds["RAINFALL"].mean(dim="TIME").compute()  # Ensure computation is done
    avg_rainfall = avg_rainfall.fillna(0)  # Handle NaN values

    # Save the average rainfall to a new NetCDF file
    avg_rainfall_file = os.path.join(output_folder, f"Average_Rainfall_{year}.nc")
    avg_rainfall.to_netcdf(avg_rainfall_file)

    # Reload the saved average rainfall file
    rainfall_ds = xr.open_dataset(avg_rainfall_file)

    # Extract lat/lon & rainfall
    lat = rainfall_ds["LATITUDE"].values
    lon = rainfall_ds["LONGITUDE"].values
    rainfall = rainfall_ds["RAINFALL"].values  # Ensure this is the correct variable name

    # Create coordinate pairs & flatten rainfall data
    rainfall_points = np.array([(lat[i], lon[j]) for i in range(len(lat)) for j in range(len(lon))])
    rainfall_values = rainfall.flatten()

    # Build KDTree & map rainfall data to grid centroids
    tree = cKDTree(rainfall_points)
    _, idx = tree.query(grid_points)
    grid[f"rainfall_{year}"] = rainfall_values[idx]

# Drop unnecessary columns
grid = grid.drop(columns=["centroid"])

# Save only the mapped rainfall grid
output_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_rainfall.geojson"
grid.to_file(output_path, driver="GeoJSON")

print(f"Rainfall Mapping Completed! Data saved to: {output_path}")
