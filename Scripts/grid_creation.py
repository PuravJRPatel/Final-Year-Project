import geopandas as gpd
import numpy as np
from shapely.geometry import box

def create_grid(region_shapefile, grid_res = 0.25):
  region = gpd.read_file(region_shapefile)
  minx, miny, maxx, maxy = region.total_bounds

  x_coords = np.arange(minx, maxx, grid_res)
  y_coords = np.arange(miny, maxy, grid_res)

  grid_cells = [box(x, y, x + grid_res, y + grid_res) for x in x_coords for y in y_coords]

  grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs= region.crs)
  grid = gpd.clip(grid, region)

  centroids = grid.copy()
  centroids['geometry'] = grid.geometry.centroid
  centroids['latitude'] = centroids['geometry'].y
  centroids['longitude'] = centroids['geometry'].x

  return grid, centroids

if __name__ == "__main__":
  grid, centroids = create_grid(r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\india_ds.dbf", grid_res=0.25)
  grid.to_file(r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\grid.shp")
  centroids[["geometry"]].to_file(r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Shapefile\India Shape\centroids.shp")
  centroids[["latitude", "longitude"]].to_csv(r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_nodes.csv", index=False)
  print('Grid Completed')