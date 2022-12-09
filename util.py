import csv

import numpy as np
import time
import pandas as pd
from tqdm import tqdm
import math


class Util(object):

    @staticmethod
    def x_to_ind(x):
        return math.ceil(x / 0.03) + 100

    @staticmethod
    def x_to_flt_ind(x):
        return (x / 0.03) + 100

    @staticmethod
    def find_points(c):
        x_max = Util.x_to_ind(max(c['X [R]']))
        x_min = Util.x_to_ind(min(c['X [R]']))
        y_max = Util.x_to_ind(max(c['Y [R]']))
        y_min = Util.x_to_ind(min(c['Y [R]']))
        z_max = Util.x_to_ind(max(c['Z [R]']))
        z_min = Util.x_to_ind(min(c['Z [R]']))
        return range(x_min, x_max), range(y_min, y_max), range(z_min, z_max)

    @staticmethod
    def combine_3d(results):
        init = np.zeros(results[0].shape)
        init.fill(-1)
        for i in tqdm(range(results[0].shape[0])):
            for j in range(results[0].shape[1]):
                for k in range(results[0].shape[2]):
                    for result in results:
                        if result[i][j][k] != -1:
                            init[i][j][k] = result[i][j][k]
                            break

        return init

    @staticmethod
    def combine_2d(results):
        init = np.zeros(results[0].shape)
        for i in tqdm(range(results[0].shape[0])):
            for j in range(results[0].shape[1]):
                for result in results:
                    if result[i][j] != 0:
                        init[i][j] = result[i][j]
                        break
        return init

    @staticmethod
    def presort(df, df_pos):
        temp = np.zeros((201, 201, 201))
        temp.fill(-1)
        pt_label = [f'P{n}' for n in range(1, 9)]
        for n in tqdm(df_pos.index):
            idxs = [int(df_pos.loc[n][s])-1 for s in pt_label]
            cube = df.loc[idxs]
            xs, ys, zs = Util.find_points(cube)
            for i in xs:
                if 0 <= i <= 200:
                    for j in ys:
                        if 0 <= j <= 200:
                            for k in zs:
                                if 0 <= k <= 200:
                                    temp[i][j][k] = n
        return temp

    @staticmethod
    def dat2df(path):

        with open(path) as file:
            header = False
            n, headers = 0, []
            lines = []
            csv_file = csv.reader(file, delimiter=' ')

            for row in csv_file:
                if row[0] == '':
                    row.pop(0)
                lines.append(row)

            i = 0
            while 'DT=(SINGLE' not in lines[i]:
                if 'VARIABLES' in lines[i]:
                    header = True
                    headers.append(lines[i][2])
                elif 'ZONE' in lines[i]:
                    header = False
                elif header is True:
                    headers.append(lines[i][0])
                elif 'ZONETYPE=FEBrick' in lines[i]:
                    n = int(lines[i][0].split('=')[1].split(',')[0])
                i += 1

            df_point = pd.DataFrame(lines[i+1:i+n+1], columns=headers)
            df_pos = pd.DataFrame(lines[i+n+1:], columns=[f'P{i}' for i in range(1,9)])

            return df_point, df_pos




























