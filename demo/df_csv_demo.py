import pandas as pd
import numpy as np
import xarray as xr
import csv

'''
to install x_array
$ conda install -c conda-forge xarray dask netCDF4 bottleneck
'''

data = np.arange(27).reshape(3,3,3)

''' convert to xarray DataArray'''
xrData = xr.DataArray(data, name="pressure")
xrData.to_netcdf("demo.nc")

''' read from .nc file to dataframe '''
data = xr.open_dataset("demo.nc")
df = xrData.to_dataframe(name="pressure")
print(df["pressure"][0][1][1])
