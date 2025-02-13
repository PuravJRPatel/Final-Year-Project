import os
import xarray as xr
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree

# Paths
grid_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp"
rainfall_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Rainfall"

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
    rainfall_ds = xr.open_dataset(rainfall_file)

    # Extract lat/lon & rainfall
    lat = rainfall_ds["LATITUDE"].values
    lon = rainfall_ds["LONGITUDE"].values
    rainfall = rainfall_ds["RAINFALL"].values  # Adjust variable name if needed

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
