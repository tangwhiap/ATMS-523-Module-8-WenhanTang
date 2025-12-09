# 🌧️ Seasonal Machine Learning for Precipitation Prediction over the U.S. Midwest
*A final project for ATMS 523*

## ✨ Author

**Wenhan Tang** (UIN: 678054985)

University of Illinois at Urbana–Champaign  

---

## 📌 Overview

This project applies random forest method to predict **daily precipitation occurrence** over the U.S. Midwest using **ERA5 reanalysis data**. A set of surface meteorological variables—including wind, temperature, humidity, pressure, and cloud properties—is extracted at each grid cell and used as predictors.

To account for seasonal variability in precipitation regimes, **separate Random Forest classifiers** are trained for **winter, spring, summer, and autumn**. The models are evaluated using accuracy, precision, and recall, and spatial performance maps are generated for each season. Feature importance analyses (including Random Forest importances and SHAP values) further highlight key predictors.

A one-day case study illustrates model predictions versus true precipitation fields.

---

## 📂 Project Structure

    ATMS523_Final_Project/
    │
    ├── data_proc.py                                # Data extraction: point, region, one-day samples
    ├── ATMS523_final_project_WenhanTang.ipynb      # Seasonal RF model training and evaluation
    ├── LICENSE                                     # The MIT license
    └── README.md                                   # Project documentation

---

## 🧠 Methods

### ✔ Data Source

- ERA5 hourly reanalysis  
- Variables: `u10`, `v10`, `d2m`, `t2m`, `msl`, `tcc`, `tciw`, `tclw`, `tcrw`, and `tp`  
- Precipitation occurrence defined as:  

    tp ≥ 0.1 mm  → Precipitation (1)  
    tp < 0.1 mm  → No precipitation (0)

### ✔ Machine Learning

- Random Forest classifier (scikit-learn)  
- Four separate seasonal models  
- Train/test split: 70/30  
- Metrics: Accuracy, Precision, Recall  
- Interpretation tools:
  - Random Forest feature importances  
  - SHAP summary plots  

---

## 🌎 Results

### 🔹 Seasonal model performance

Spatial maps show accuracy, precision, and recall for each season across the Midwest.

### 🔹 Feature importance

RF importance and SHAP analysis reveal the dominant predictors of precipitation occurrence, with cloud and humidity-related variables contributing strongly.

### 🔹 One-day case study

Prediction example for **2024-07-14**, comparing:  
- Predicted precipitation map  
- True ERA5 precipitation map  

---

## ▶️ How to Run

### 1. Install dependencies

    conda install numpy pandas xarray cartopy shap seaborn scikit-learn

### 2. Prepare ERA5 data

Prepare the following ERA5 NetCDF files into a directory:

    `ERA5_10m_u_component_of_wind.nc`
    `ERA5_10m_v_component_of_wind.nc`
    `ERA5_2m_dewpoint_temperature.nc`
    `ERA5_2m_temperature.nc`
    `ERA5_mean_sea_level_pressure.nc`
    `ERA5_total_cloud_cover.nc`
    `ERA5_total_column_cloud_ice_water.nc`
    `ERA5_total_column_cloud_liquid_water.nc`
    `ERA5_total_column_rain_water.nc`
    `ERA5_total_precipitation.nc`


### 3. Test the ERA5 data by running
    Set the variable `OrigDir=` the directory of ERA5 files
    Excute `./data_proc.py`
    If no errors are raised, the test is passed

### 4. Run notebook the notebook

    `ATMS523_final_project_WenhanTang.ipynb`

---

## 📜 Citation / Acknowledgment

ERA5 Daily Reanalysis (DOI: 10.24381/cds.4991cf48) will be used, covering one full year (e.g., 2023, or more years if necessary) over the continental U.S. at 0.25° spatial resolution.

I would like to thank Haotian Ma (University of Wisconsin) for helping me resolve technical issues and for valuable discussions about the results.
