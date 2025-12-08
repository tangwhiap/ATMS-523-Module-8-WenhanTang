#!/usr/bin/env python

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
    
OrigDir = "/data/keeling/a/wenhant2/datasets/ERA2/Orig"

def extract_point_var(varName, lon, lat):
    ds = xr.open_dataset(OrigDir + "/ERA5_" + name_dict[varName] + ".nc")
    ts = ds[varName].sel(
        longitude=lon,
        latitude=lat,
        method="nearest",
    )
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

if __name__ == "__main__":
    df = extract_point_data(
        lon = -88.2434,
        lat = 40.1164,
    )
    print(df)

    df = extract_region_data(
        lon1=-105, lon2=-80,
        lat1=35, lat2=49
    )
    print(df)
