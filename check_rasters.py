import rasterio
import os
import numpy as np

RASTER_DIR = "data/raw"

for filename in os.listdir(RASTER_DIR):
    if filename.endswith(".tif"):
        path = os.path.join(RASTER_DIR, filename)

        with rasterio.open(path) as src:
            print("\nRaster:", filename)
            print("Data type:", src.dtypes)
            print("Shape:", src.shape)
            print("NoData:", src.nodata)
            print("Scale:", src.scales)
            print("Offset:", src.offsets)
            print("Tags:", src.tags())

            data = src.read(1, masked=True)

            print("Minimum:", data.min())
            print("Maximum:", data.max())
            print("Mean:", data.mean())