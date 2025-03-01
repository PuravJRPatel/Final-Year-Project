import os
import xarray as xr
import geopandas as gpd
import numpy as np
from scipy.interpolate import griddata
from scipy.spatial import cKDTree

# Paths
grid_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp"
temperature_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Temperature"
output_file = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_temperature.geojson"

# Load grid shapefile
grid = gpd.read_file(grid_path)

# Compute grid centroids for mapping
grid["centroid"] = grid.geometry.centroid
grid_points = np.array([(p.y, p.x) for p in grid["centroid"]])

# Iterate over all years
for year in range(2000, 2023 + 1):  # Loop from 2000 to 2023
    print(f"Processing Temperature Data for {year}...")

    # Load temperature data
    temp_file = os.path.join(temperature_folder, f"Maxtemp_MaxT_{year}.nc")
    temp_ds = xr.open_dataset(temp_file)

    # Extract latitude, longitude, and temperature
    lat = temp_ds["lat"].values
    lon = temp_ds["lon"].values
    temp = temp_ds["temperature"].values  # Shape: (time, lat, lon)

    # Compute yearly average for each location
    temp_avg = np.nanmean(temp, axis=0)  # Shape: (lat, lon)

    # Create a meshgrid of original points
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    original_points = np.array([lon_grid.flatten(), lat_grid.flatten()]).T
    original_values = temp_avg.flatten()

    # Create the target 0.25°×0.25° grid
    target_lats = np.arange(lat.min(), lat.max() + 0.25, 0.25)
    target_lons = np.arange(lon.min(), lon.max() + 0.25, 0.25)
    target_lon_grid, target_lat_grid = np.meshgrid(target_lons, target_lats)
    target_points = np.array([target_lon_grid.flatten(), target_lat_grid.flatten()]).T

    # Interpolate temperature data to 0.25°×0.25°
    interpolated_temp = griddata(original_points, original_values, target_points, method='linear')

    
    # Map interpolated temperature data to grid centroids
    tree = cKDTree(target_points)
    _, idx = tree.query(grid_points)
    grid[f"temperature_{year}"] = interpolated_temp[idx]

# Drop unnecessary centroid column
grid = grid.drop(columns=["centroid"])

# Save the final mapped temperature data as a single GeoJSON file
grid.to_file(output_file, driver="GeoJSON")

print(f"Temperature Mapping Completed! Data saved to: {output_file}")
