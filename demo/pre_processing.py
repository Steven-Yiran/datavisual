import pandas as pd
import numpy as np
import xarray as xr #require numpy and pandas
import multiprocessing
import concurrent.futures
import csv
from tqdm import tqdm


data_pressure = "./data/pressure.csv"
data_pos = "./data/allpos.csv"

df_pressure = pd.read_csv(data_pressure)
df_pos = pd.read_csv(data_pos)


def to_index(x):
    return int(x/0.015)+200


def data_reader(df, start, end):
    field_name = "p [nPa]"
    data = np.zeros((401, 401, 401))
    for i in tqdm(range(start, end)):
        x_ind = to_index(df.loc[i]["X [R]"])
        y_ind = to_index(df.loc[i]["Y [R]"])
        z_ind = to_index(df.loc[i]["Z [R]"])
        if 0 <= x_ind <= 400 and 0 <= y_ind <= 400 and 0 <= z_ind <= 400:
            data[x_ind][y_ind][z_ind] = df.loc[i][field_name]
    # save data as xarray DataArray
    xr.DataArray(data, name=field_name).to_netcdf("./data/file.nc")


def multi(df, num):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        boundaries = np.linspace(0,df.shape[0],num+1, dtype=np.int32)
        results = [executor.submit(data_reader(df,boundaries[i], boundaries[i+1])) for i in range(num)]


if __name__ == "__main__":
    """ multi thread """
    multi(df_pressure,4)
    print(np.linspace(0,df_pressure.shape[0],4,dtype=np.int32))

'''
to install x_array
$ conda install -c conda-forge xarray dask netCDF4 bottleneck

data = np.arange(27).reshape(3,3,3)

#convert to xarray DataArray
xrData = xr.DataArray(data, name="pressure")
xrData.to_netcdf("demo.nc")

#read from .nc file to dataframe
data = xr.open_dataset("demo.nc")
df = xrData.to_dataframe(name="pressure")
print(df["pressure"][0][1][1])
'''
