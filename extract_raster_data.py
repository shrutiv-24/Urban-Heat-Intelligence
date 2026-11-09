import os
import numpy as np
import pandas as pd
import rasterio

BASE_DIR = "data/raw"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR, "urban_heat_data.csv"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = {
    "ndvi": "Delhi_NDVI_Map.tif",
    "uhi": "Delhi_UHI_Map.tif",
    "lst_c": "Delhi_LST_Map.tif"
}

arrays = []
reference_shape = None
reference_transform = None
reference_crs = None

# Read raster files
for name, filename in files.items():

    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing raster file: {path}"
        )

    with rasterio.open(path) as src:

        raster = src.read(
            1, masked=True
        ).filled(np.nan).astype(float)

        if reference_shape is None:
            reference_shape = src.shape
            reference_transform = src.transform
            reference_crs = src.crs

        else:
            if (
                src.shape != reference_shape
                or src.transform != reference_transform
                or src.crs != reference_crs
            ):
                raise ValueError(
                    f"Raster grid mismatch: {filename}. "
                    "Align all rasters in QGIS first."
                )

        # Scale NDVI if stored as 8-bit 0-255
        if name == "ndvi":
            valid_values = raster[np.isfinite(raster)]

            if (
                len(valid_values) > 0
                and np.nanmax(valid_values) > 1
            ):
                raster = (raster / 255.0) * 2.0 - 1.0

        arrays.append(raster)

        print("\nRaster:", filename)
        print("Shape:", raster.shape)
        print("Minimum:", np.nanmin(raster))
        print("Maximum:", np.nanmax(raster))

# Extract arrays
ndvi, uhi, lst = arrays

# Select valid pixels
valid = (
    np.isfinite(ndvi)
    & np.isfinite(uhi)
    & np.isfinite(lst)
    & (ndvi >= -1)
    & (ndvi <= 1)
)

rows, cols = np.where(valid)

# Create dataset
data = pd.DataFrame({
    "ndvi": ndvi[valid],
    "uhi": uhi[valid],
    "lst_c": lst[valid],
    "row": rows,
    "col": cols
})

# Remove invalid values
data = data.replace(
    [np.inf, -np.inf], np.nan
).dropna()

data = data.reset_index(drop=True)

# Save dataset
data.to_csv(
    OUTPUT_FILE,
    index=False
)

# Display results
print("\nURBAN HEAT DATA EXTRACTION COMPLETED")

print("Valid pixels:", len(data))
print("Dataset shape:", data.shape)

print("NDVI minimum:", data["ndvi"].min())
print("NDVI maximum:", data["ndvi"].max())

print("UHI minimum:", data["uhi"].min())
print("UHI maximum:", data["uhi"].max())

print("LST minimum:", data["lst_c"].min())
print("LST maximum:", data["lst_c"].max())

print("LST average:", data["lst_c"].mean())

print("\nSaved:", OUTPUT_FILE)