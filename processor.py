import pandas as pd
import numpy as np
from util import Util
import multiprocessing as mp
from tqdm import tqdm
import math
import os


class Processor:

    def __init__(self, dat, stored, core_num):

        self.mapping = np.zeros((201, 201, 201))

        is_file = os.path.isfile(stored)
        if is_file:
            self.df = pd.read_csv('./data/points.csv')
            self.df_pos = pd.read_csv('./data/all_pos.csv')
            self.load_in_matrix(stored)
        else:
            # self.df, self.df_pos = Util.dat2df(dat)
            # self.df.to_csv('./data/points.csv', index=False)
            # self.df_pos.to_csv('./data/all_pos.csv', index=False)
            self.df = pd.read_csv('./data/points.csv')
            self.df_pos = pd.read_csv('./data/all_pos.csv')
            self.init_in_matrix(core_num)
            self.save_in_matrix(stored)


    def init_in_matrix(self, core_num):
        if core_num == 1:
            self.mapping = Util.presort(self.df, self.df_pos)
        else:
            pos_split = np.array_split(self.df_pos, core_num)
            args = []
            for pos in pos_split:
                args.append((self.df, pos))

            pool = mp.Pool(core_num)
            results = pool.starmap(Util.presort, args)
            for result in results:
                print(result.shape)
            pool.close()
            pool.join()

            self.mapping = Util.combine_3d(results)

    def save_in_matrix(self, file):
        np.save(file, self.mapping)

    def load_in_matrix(self, file):
        self.mapping = np.load(file)

    def get_df(self, plane, level, var, core_num):

        if core_num == 1:
            temp = self.insert(0, 201, plane=plane, level=level, var=var)
        else:
            ranges = np.linspace(0, 201, core_num+1, dtype=np.int32)
            args = []
            for i in range(core_num):
                args.append((ranges[i], ranges[i+1], plane, level, var))

            pool = mp.Pool(core_num)
            results = pool.starmap(self.insert, args)
            pool.close()
            pool.join()
            temp = Util.combine_2d(results)

        df = pd.DataFrame(temp, index=[round((i - 100) * 0.03, 2) for i in range(201)],
                          columns=[round((i - 100) * 0.03, 2) for i in range(201)], dtype=np.float32)
        return df

    def __idw(self, idx, pt, var):

        pt_label = [f'P{n}' for n in range(1, 9)]

        if idx == -1:
            return 0
        else:
            idxs = [int(self.df_pos.loc[idx][s]) for s in pt_label]
            cube = self.df.loc[idxs]
            dividend = 0
            divisor = 0
            for p in cube.index:
                d = math.dist(pt, (Util.x_to_flt_ind(cube.loc[p]['X [R]']),
                                   Util.x_to_flt_ind(cube.loc[p]['Y [R]']),
                                   Util.x_to_flt_ind(cube.loc[p]['Z [R]'])))
                dividend += cube.loc[p][var] / d
                divisor += 1 / d

            return dividend / divisor

    def insert(self, start, end, plane, level, var):
        temp = np.zeros((201, 201))
        if plane == 0:
            for i in tqdm(range(start, end)):
                for j in range(201):
                    temp[i][j] = self.__idw(self.mapping[level][i][j], (level, i, j), var)
        elif plane == 1:
            for i in tqdm(range(start, end)):
                for j in range(201):
                    temp[i][j] = self.__idw(self.mapping[i][level][j], (i, level, j), var)
        elif plane == 2:
            for i in tqdm(range(start, end)):
                for j in range(201):
                    temp[i][j] = self.__idw(self.mapping[i][j][level], (i, j, level), var)

        return temp

    def get_variables(self):
        return self.df.columns
        
    def __repr__(self):
        return f"the current data has a shape of {self.mapping.shape}"




