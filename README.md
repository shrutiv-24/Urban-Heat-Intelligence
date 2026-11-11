# 🌡️ Delhi Urban Heat Intelligence

### Machine Learning-Based Urban Heat Analysis and Prediction

Delhi Urban Heat Intelligence is a data science and machine learning project that analyzes urban heat patterns in Delhi using satellite-derived environmental data, geospatial processing, and predictive modeling.

The project explores the relationship between Land Surface Temperature (LST), Normalized Difference Vegetation Index (NDVI), and Urban Heat Island (UHI) patterns to understand urban heat distribution and generate heat predictions.

---

## 🎯 Project Objectives

- Analyze urban heat patterns across Delhi.
- Process satellite-derived raster datasets.
- Study the relationship between vegetation and surface temperature.
- Identify urban heat intensity patterns.
- Develop machine learning models for urban heat prediction.
- Generate visualizations and analytical reports.

---

## 🛰️ Environmental Indicators

| Indicator | Description |
|---|---|
| LST | Land Surface Temperature (°C), calculated from Landsat thermal band ST_B10 |
| NDVI | Normalized Difference Vegetation Index, calculated from Landsat bands 4 and 5 |
| UHI | Urban Heat Island, calculated as LST minus the mean LST of Delhi |

---

## 🛠️ Technologies Used

- **Programming:** Python
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Visualization:** Matplotlib, Seaborn
- **Geospatial Analysis:** Rasterio, QGIS
- **Model Storage:** Joblib
- **Satellite Data Processing:** Google Earth Engine (Landsat 8 and Landsat 9)
- **Version Control:** Git and GitHub

---

## 📁 Project Structure

```
Urban-Heat-Intelligence/
├── data/
│   ├── raw/                       
│   └── processed/
│       └── urban_heat_data.csv    
├── models/
│   ├── train_model.py            
│   ├── Random_Forest.joblib
│   ├── Linear_Regression.joblib
│   └── model_description.md
├── results/                       
├── earth_engine_script.js         
├── check_rasters.py               
├── extract_raster_data.py        
├── urban_heat_intelligence.py     
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Running

**Requirements:** Python 3.9 or above and Git.

### 1. Clone the Repository

```bash
git clone https://github.com/shrutiv-24/Urban-Heat-Intelligence.git
cd Urban-Heat-Intelligence
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the Raster Data

Run `earth_engine_script.js` in the [Google Earth Engine Code Editor](https://code.earthengine.google.com/) and start the three export tasks in the **Tasks** tab. Download `Delhi_NDVI_Map.tif`, `Delhi_LST_Map.tif` and `Delhi_UHI_Map.tif` from Google Drive and place them in `data/raw/`.

### 4. Run the Project

Run the scripts from the project folder, in this order:

```bash
python check_rasters.py
python extract_raster_data.py
python models/train_model.py
python urban_heat_intelligence.py
```

| Script | What it does |
|---|---|
| `check_rasters.py` | Prints the data type, shape and value range of each raster |
| `extract_raster_data.py` | Converts the rasters into `data/processed/urban_heat_data.csv` |
| `models/train_model.py` | Trains the models and saves them in `models/` |
| `urban_heat_intelligence.py` | Predicts heat, creates heat categories and saves charts in `results/` |

> **Note:** Ensure the required datasets, raster files, and model files are available in their respective directories before execution. Git LFS is used for large CSV files.

---

## 🔬 Methodology

The project follows these major steps:

1. **Satellite Data Collection:** Landsat 8 and Landsat 9 Collection 2 Level-2 imagery for Delhi (April to June 2023, cloud cover below 20%, 14 images) is obtained using Google Earth Engine.
2. **Data Processing:** Cloudy pixels are masked using the QA_PIXEL band, and a median composite is created at 30 m resolution.
3. **Feature Extraction:** NDVI, LST and UHI layers are calculated and exported as float32 GeoTIFF files.
4. **Dataset Preparation:** The rasters are converted into a structured dataset of 1,673,718 valid pixels.
5. **Model Training:** Machine learning models are trained to predict LST from NDVI.
6. **Prediction:** Urban heat predictions are generated and grouped into heat categories.
7. **Visualization:** Graphs and analytical reports are created to understand urban heat patterns.

> **Note:** UHI is not used as a model feature. It equals LST minus a constant, so using it would leak the answer to the model and give a meaningless R² of 1.0.

---

## 🤖 Machine Learning Models

The project uses two regression algorithms, with `ndvi` as the input and `lst_c` (LST in °C) as the target:

### 1. Linear Regression

- Serves as a baseline prediction model.
- Analyzes the relationship between vegetation and heat values.

### 2. Random Forest Regression

- Captures nonlinear relationships in environmental data.
- Uses multiple decision trees (100 trees, minimum 20 samples per leaf) to improve predictive modeling.

Trained models are stored in the `models/` directory. A 300,000-pixel sample is used for training, with an 80% training and 20% test split.

---

## 📊 Results & Visualizations

The project generates the following outputs:

- Urban heat category visualization.
- NDVI and urban heat relationship analysis.
- Land Surface Temperature distribution.
- Urban heat prediction dataset.
- Analytical report.

All generated outputs are stored in the `results/` directory.

### Key Findings

| Measure | Value |
|---|---|
| Mean LST | 41.62 °C |
| LST range | 29.05 to 53.74 °C |
| Hotspot threshold (mean + 1 SD) | 44.41 °C |
| Mean NDVI | 0.32 |
| NDVI and LST correlation | −0.54 |

Areas with more vegetation have lower surface temperatures. The Yamuna corridor and vegetated areas are cooler, while the western and south-western parts of Delhi show the strongest warm areas.

### Heat Categories (predicted LST)

| Category | Range | Pixels | Share |
|---|---|---|---|
| Low | below 40 °C | 289,086 | 17.3% |
| Moderate | 40 to 42 °C | 576,396 | 34.4% |
| High | 42 to 44 °C | 730,075 | 43.6% |
| Extreme | above 44 °C | 78,161 | 4.7% |

---

## 📈 Model Evaluation

Models are evaluated on the test data using:

- Mean Absolute Error (MAE)
- R² Score

| Model | MAE (°C) | R² Score |
|---|---|---|
| Random Forest | 1.733 | 0.324 |
| Linear Regression | 1.759 | 0.297 |

The Random Forest predicts temperature with an average error of about 1.7 °C and explains about 32% of the variation in LST using NDVI alone.

### ⚠️ Limitations

- NDVI is the only feature, so the model explains only part of the temperature variation. Built-up surfaces and building density also affect LST.
- Predictions are smoother than the observed temperatures, so the most extreme values are under-represented.
- The analysis uses one median composite (April to June 2023) and does not show changes between years or seasons.

---

## 🔮 Future Scope

- Add predictors such as a built-up index (NDBI), elevation and land use to improve accuracy.
- Integrate additional satellite datasets and analyze several years of imagery.
- Improve prediction performance through hyperparameter tuning.
- Develop interactive urban heat maps.
- Explore additional machine learning algorithms.
- Build a web-based urban heat monitoring dashboard.
- Extend the analysis to other Indian cities.

---

## 👩‍💻 Author

**Shruti Verma**

GitHub: [@shrutiv-24](https://github.com/shrutiv-24)

Project Repository: [Delhi Urban Heat Intelligence](https://github.com/shrutiv-24/Urban-Heat-Intelligence)