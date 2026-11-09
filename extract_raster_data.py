import os
import numpy as np
import pandas as pd
import rasterio

BASE_DIR = "data/raw"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "urban_heat_data.csv")

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
                    "Re-export all rasters with the same region, scale and crs."
                )

    arrays.append(raster)

    print("\nRaster:", filename)
    print("Shape:", raster.shape)
    print("Minimum:", np.nanmin(raster))
    print("Maximum:", np.nanmax(raster))

ndvi, uhi, lst = arrays

valid = (
    np.isfinite(ndvi)
    & np.isfinite(uhi)
    & np.isfinite(lst)
    & (ndvi >= -1)
    & (ndvi <= 1)
    & (lst > 0)
    & (lst < 70)
)

rows, cols = np.where(valid)

data = pd.DataFrame({
    "ndvi": ndvi[valid],
    "uhi": uhi[valid],
    "lst_c": lst[valid],
    "row": rows,
    "col": cols
})

data = data.replace(
    [np.inf, -np.inf], np.nan
).dropna()

data = data.reset_index(drop=True)

data.to_csv(
    OUTPUT_FILE,
    index=False
)

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