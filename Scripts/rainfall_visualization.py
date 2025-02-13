import geopandas as gpd
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np

# Paths
rainfall_data_path = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Data\Processed\grid_with_rainfall.geojson"
frames_folder = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Results\frames"
video_output = r"C:\Users\purav\OneDrive\Desktop\Fi Year Project\Final-Year-Project\Results\rainfall_transition.mp4"

# Ensure frames folder exists
os.makedirs(frames_folder, exist_ok=True)

# Load Grid with Rainfall Data
grid = gpd.read_file(rainfall_data_path)

# Get first year for reference dimensions
first_year = 2000
first_column = f"rainfall_{first_year}"

# Generate frames for each year
for year in range(2000, 2024):
    column_name = f"rainfall_{year}"
    
    if column_name not in grid.columns:
        print(f"Skipping {year}, rainfall data not found.")
        continue

    # Create a new figure for each frame
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot Rainfall Map
    grid.plot(column=column_name, cmap="Blues_r", edgecolor="lightgray", linewidth=0.1, legend=True, ax=ax)

    # Enhance Colorbar & Titles
    sm = plt.cm.ScalarMappable(cmap="Blues_r", norm=plt.Normalize(vmin=grid[column_name].min(), vmax=grid[column_name].max()))
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Rainfall (mm)", fontsize=12)

    # Clean Up the Plot
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)  # Hide axis border
    ax.set_title(f"Rainfall Mapping - {year}", fontsize=16, fontweight="bold")

    # Save frame
    frame_path = os.path.join(frames_folder, f"rainfall_{year}.png")
    plt.savefig(frame_path, dpi=300, bbox_inches="tight")
    plt.close(fig)  # Close figure to prevent overlapping
    print(f"Saved frame for {year}")

# Create Video from Frames
frame_files = sorted([os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if f.endswith(".png")])
if not frame_files:
    print("No frames found. Video cannot be created.")
    exit()

# Read first frame for video properties
first_frame = cv2.imread(frame_files[0])
height, width, _ = first_frame.shape
fps = 5  # Increased FPS for smoother transition

# Initialize Video Writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(video_output, fourcc, fps, (width, height))

# Function to Crossfade Between Frames
def crossfade(img1, img2, steps=10):
    """ Creates a smooth transition between two frames. """
    for alpha in np.linspace(0, 1, steps):
        blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        video.write(blended)

# Write frames to video with smooth transitions
prev_frame = None
for frame_file in frame_files:
    frame = cv2.imread(frame_file)
    
    # Ensure frame size is consistent
    frame = cv2.resize(frame, (width, height))

    if prev_frame is not None:
        crossfade(prev_frame, frame, steps=10)  # Smooth fade transition

    video.write(frame)
    prev_frame = frame

video.release()
print(f"Rainfall transition video saved at: {video_output}")
