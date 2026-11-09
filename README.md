🌡️ Delhi Urban Heat Intelligence

Machine Learning-Based Urban Heat Analysis and Prediction

Delhi Urban Heat Intelligence is a data science and machine learning project that analyzes urban heat patterns in Delhi using satellite-derived environmental data, geospatial processing, and predictive modeling.

The project explores the relationship between Land Surface Temperature (LST), Normalized Difference Vegetation Index (NDVI), and Urban Heat Island (UHI) patterns to understand urban heat distribution and generate heat predictions.

---

🎯 Project Objectives

- Analyze urban heat patterns across Delhi.
- Process satellite-derived raster datasets.
- Study the relationship between vegetation and surface temperature.
- Identify urban heat intensity patterns.
- Develop machine learning models for urban heat prediction.
- Generate visualizations and analytical reports.

🛰️ Environmental Indicators

Indicator| Description
LST| Land Surface Temperature
NDVI| Normalized Difference Vegetation Index
UHI| Urban Heat Island

🛠️ Technologies Used

- Programming: Python
- Data Analysis: Pandas, NumPy
- Machine Learning: Scikit-learn
- Visualization: Matplotlib, Seaborn
- Geospatial Analysis: Raster data processing
- Model Storage: Joblib
- Satellite Data Processing: Google Earth Engine
- Version Control: Git and GitHub


⚙️ Installation & Running

Requirements: Python 3.9 or above and Git.

1. Clone the Repository

git clone https://github.com/shrutiv-24/Urban-Heat-Intelligence.git
cd Urban-Heat-Intelligence

2. Install Dependencies

pip install -r requirements.txt

3. Run the Project

python urban_heat_intelligence.py

4. Train the Models

python models/train_model.py

Note: Ensure the required datasets, raster files, and model files are available in their respective directories before execution. Git LFS is used for large CSV files.

🔬 Methodology

The project follows these major steps:

1. Satellite Data Collection: Obtain environmental raster data using Google Earth Engine.
2. Data Processing: Inspect and process satellite-derived raster datasets.
3. Feature Extraction: Extract relevant environmental indicators such as LST, NDVI, and UHI.
4. Dataset Preparation: Organize extracted values into a structured dataset.
5. Model Training: Train machine learning models using the prepared dataset.
6. Prediction: Generate urban heat predictions.
7. Visualization: Create graphs and analytical reports to understand urban heat patterns.

🤖 Machine Learning Models

The project uses two regression algorithms:

1. Linear Regression

- Serves as a baseline prediction model.
- Analyzes relationships between environmental variables and heat values.

2. Random Forest Regression

- Captures nonlinear relationships in environmental data.
- Uses multiple decision trees to improve predictive modeling.

Trained models are stored in the "models/" directory.

📊 Results & Visualizations

The project generates the following outputs:

- Urban heat category visualization.
- NDVI and urban heat relationship analysis.
- Land Surface Temperature distribution.
- Urban heat prediction dataset.
- Analytical report.

All generated outputs are stored in the "results/" directory.

📈 Model Evaluation

Model performance can be evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

Actual evaluation metrics will be added after model validation.

🔮 Future Scope

- Integrate additional satellite datasets.
- Improve prediction performance through hyperparameter tuning.
- Develop interactive urban heat maps.
- Explore additional machine learning algorithms.
- Build a web-based urban heat monitoring dashboard.
- Extend the analysis to other Indian cities.

👩‍💻 Author

Shruti Verma

GitHub: "@shrutiv-24" (https://github.com/shrutiv-24)

Project Repository: "Delhi Urban Heat Intelligence" (https://github.com/shrutiv-24/Urban-Heat-Intelligence)

---
