import pandas as pd

from plotter import Plotter


def main():
    stored = "./data/stored.npy"
    dat = './data/alldata-simple.dat'

    plotter = Plotter(dat, stored, core_num=4)
    plotter.interactive_plot(para_1=(0, 0, 6),
                             para_2=(1, 0, 6),
                             para_3=(2, 0, 6),
                             para_4=(1, 0, 0))


if __name__ == '__main__':
    main()
