import geopandas as gpd

rainfall_file = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_rainfall.geojson"
temperature_file = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_temperature.geojson"
output_file = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_data.geojson"

rainfall_gdf = gpd.read_file(rainfall_file)
temperature_gdf = gpd.read_file(temperature_file)


merged_gdf = rainfall_gdf.merge(temperature_gdf.drop(columns=["geometry"]), on="FID")

merged_gdf.to_file(output_file, driver="GeoJSON")

print(f"Merged data saved to {output_file}")
