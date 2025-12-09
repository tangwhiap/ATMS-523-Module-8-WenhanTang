#!/usr/bin/env python

"""
    Access the ERA5 netCDF files and
    convert to the pandas data frame.
"""

# The directory of ERA5 netCDF files
OrigDir = "/Users/wenhant2/Datasets/ERA5_2/Orig"

import xarray as xr
import numpy as np

name_dict = {
    "u10": "10m_u_component_of_wind",
    "v10": "10m_v_component_of_wind",
    "d2m": "2m_dewpoint_temperature",
    "t2m": "2m_temperature",
    "msl": "mean_sea_level_pressure",
    "tcc": "total_cloud_cover",
    "tciw": "total_column_cloud_ice_water",
    "tclw": "total_column_cloud_liquid_water",
    "tcrw": "total_column_rain_water",
    "tp": "total_precipitation",
}
    

def plot_prec_hist():
    import matplotlib.pyplot as plt
    import xarray as xr

    ds = xr.open_dataset(OrigDir + "/ERA5_" + name_dict["tp"] + ".nc")
    
    tp = ds["tp"]

    print(np.sum(tp > 0.001) / np.sum(tp >= -1))
    plt.figure(figsize=(10, 5))
    tp.plot.hist(bins=100, color="steelblue", edgecolor="black")

    plt.xlabel("Total precipitation (tp)")
    plt.ylabel("Frequency")
    plt.title("Histogram of ERA5 Total Precipitation (tp)")
    
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


    
def extract_point_var(varName, lon, lat):
    ds = xr.open_dataset(OrigDir + "/ERA5_" + name_dict[varName] + ".nc")
    ts = ds[varName].sel(
        longitude=lon,
        latitude=lat,
        method="nearest",
    )
    ds.close()
    return ts

def extract_point_data(lon, lat):
    ts_list = []
    name_list = []
    for varName in name_dict:
        ts = extract_point_var(varName, lon, lat)
        ts_list.append(ts)
        name_list.append(varName)
    df = xr.concat(ts_list, dim="variable").to_pandas().T
    df.columns = name_list
    df["doy"] = df.index.dayofyear
    return df

def extract_region_var(varName, lon1, lon2, lat1, lat2):
    ds = xr.open_dataset(OrigDir + "/ERA5_" + name_dict[varName] + ".nc")

    region = ds[varName].sel(
        longitude=slice(lon1, lon2),
        latitude=slice(lat2, lat1)  
    )

    ds.close()
    return region

def extract_region_data(lon1, lon2, lat1, lat2):
    
    region_dict = {}

    for varName in name_dict:
        region = extract_region_var(varName, lon1, lon2, lat1, lat2)

        region_dict[varName] = region

    region_ds = xr.Dataset(region_dict)

    df = region_ds.to_dataframe().reset_index()

    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "valid_time": "date"
    })

    df["doy"] = df["date"].dt.dayofyear

    return df

def extract_oneday_var(varName, date, lon1, lon2, lat1, lat2):
    ds = xr.open_dataset(OrigDir + "/ERA5_" + name_dict[varName] + ".nc")
    da_day = ds[varName].sel(valid_time=date)
    da_region = da_day.sel(
        longitude=slice(lon1, lon2),
        latitude=slice(lat2, lat1)
    )
    ds.close()
    return da_region



def extract_oneday_data(date, lon1, lon2, lat1, lat2):
    region_dict = {}

    for varName in name_dict:
        region = extract_oneday_var(varName, date, lon1, lon2, lat1, lat2)

        region_dict[varName] = region
    region_ds = xr.Dataset(region_dict)

    df = region_ds.to_dataframe().reset_index()

    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "valid_time": "date"
    })

    df["doy"] = df["date"].dt.dayofyear
    return df

if __name__ == "__main__":
    """
        The test cases:
    """

    print("Data in one pixel")
    df = extract_point_data(
        lon = -88.2434,
        lat = 40.1164,
    )
    print(df)

    print("Data over a region")
    df = extract_region_data(
        lon1=-105, lon2=-80,
        lat1=35, lat2=49
    )
    print(df)

    print("One-day datq over a region")
    df = extract_oneday_data(
        date="2024-07-15",
        lon1=-105, lon2=-80,
        lat1=35, lat2=49
    )
    print(df)

    print("The total precipitation histogram")
    plot_prec_hist()

