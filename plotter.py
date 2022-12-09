import matplotlib.pyplot as plt
import seaborn as sns
from util import Util
from matplotlib.widgets import TextBox, RadioButtons, Button
from processor import Processor


class Plotter:

    def __init__(self, dat, stored, core_num=4):
        self.processor = Processor(dat, stored, core_num)
        self.core_num = core_num

    def plot(self, plane, lev, var, axes, show_cbar=True):
        df = self.processor.get_df(plane, Util.x_to_ind(lev), var, self.core_num)
        label_dict = {0: "X [R]", 1: "Y [R]", 2: "Z [R]"}
        label_list = ["X [R]", "Y [R]", "Z [R]"]
        var_label = list(self.processor.get_variables())
        var_label.remove("X [R]")
        var_label.remove("Y [R]")
        var_label.remove("Z [R]")

        label_list.remove(label_dict[plane])
        palette = sns.color_palette("Spectral_r", as_cmap=True)

        ax = sns.heatmap(df, cbar_kws={"label": var},
                         xticklabels=40, yticklabels=40, ax=axes, cmap=palette, cbar=show_cbar)
        ax.set_xlabel(label_list[0])
        ax.invert_yaxis()
        ax.set_ylabel(label_list[1])
        return ax

    def interactive_plot(self, para_1=(0, 0, 0), para_2=(0, 0, 0), para_3=(0, 0, 0), para_4=(0, 0, 0)):
        """para = (plane, level, variable)"""
        plane_1 = para_1[0]
        level_1 = para_1[1]
        plane_2 = para_2[0]
        level_2 = para_2[1]
        plane_3 = para_3[0]
        level_3 = para_3[1]
        plane_4 = para_4[0]
        level_4 = para_4[1]

        var_label = list(self.processor.get_variables())
        var_label.remove("X [R]")
        var_label.remove("Y [R]")
        var_label.remove("Z [R]")

        variable_1 = var_label[para_1[2]]
        variable_2 = var_label[para_2[2]]
        variable_3 = var_label[para_3[2]]
        variable_4 = var_label[para_4[2]]

        fig = plt.figure(figsize=(16, 12))
        ax_1 = fig.add_axes((3 / 20, 1.8 / 3, 3 / 10, 1 / 3))
        graph_1 = self.plot(plane_1, level_1, variable_1, ax_1)
        ax_2 = fig.add_axes((3 / 20, 0.5 / 3, 3 / 10, 1 / 3))
        graph_2 = self.plot(plane_2, level_2, variable_2, ax_2)
        ax_3 = fig.add_axes((13 / 20, 1.8 / 3, 3 / 10, 1 / 3))
        graph_3 = self.plot(plane_3, level_3, variable_3, ax_3)
        ax_4 = fig.add_axes((13 / 20, 0.5 / 3, 3 / 10, 1 / 3))
        graph_4 = self.plot(plane_4, level_4, variable_4, ax_4)
        ax_color = 'lightgoldenrodyellow'

        # TextBox
        ax_box_1 = plt.axes([1.5/100, 1.8 / 3, 0.9 / 10, 1/25])
        textbox_1 = TextBox(ax_box_1, '', initial=level_1)

        ax_box_2 = plt.axes([1.5 / 100, 0.5 / 3, 0.9 / 10, 1 / 25])
        textbox_2 = TextBox(ax_box_2, '', initial=level_2)

        ax_box_3 = plt.axes([51.5 / 100, 1.8 / 3, 0.9 / 10, 1 / 25])
        textbox_3 = TextBox(ax_box_3, '', initial=level_3)

        ax_box_4 = plt.axes([51.5 / 100, 0.5 / 3, 0.9 / 10, 1 / 25])
        textbox_4 = TextBox(ax_box_4, '', initial=level_4)

        # RadioButton
        spec_label = ['Y-Z', 'X-Z', 'X-Y']

        ax_spec_radio_1 = plt.axes([1.5 / 100, 2 / 3, 0.9 / 10, 2 / 25], facecolor=ax_color)
        spec_radio_1 = RadioButtons(
            ax=ax_spec_radio_1,
            labels=spec_label,
            active=plane_1
        )

        ax_spec_radio_2 = plt.axes([1.5 / 100, 0.7 / 3, 0.9 / 10, 2 / 25], facecolor=ax_color)
        spec_radio_2 = RadioButtons(
            ax=ax_spec_radio_2,
            labels=spec_label,
            active=plane_2
        )

        ax_spec_radio_3 = plt.axes([51.5 / 100, 2 / 3, 0.9 / 10, 2 / 25], facecolor=ax_color)
        spec_radio_3 = RadioButtons(
            ax=ax_spec_radio_3,
            labels=spec_label,
            active=plane_3
        )

        ax_spec_radio_4 = plt.axes([51.5 / 100, 0.7 / 3, 0.9 / 10, 2 / 25], facecolor=ax_color)
        spec_radio_4 = RadioButtons(
            ax=ax_spec_radio_4,
            labels=spec_label,
            active=plane_4
        )

        # VariableButton
        ax_var_radio_1 = plt.axes([1.5 / 100, 2.3 / 3, 0.9 / 10, 4 / 25], facecolor=ax_color)
        var_radio_1 = RadioButtons(
            ax=ax_var_radio_1,
            labels=var_label,
            active=para_1[2],
        )

        ax_var_radio_2 = plt.axes([1.5 / 100, 1 / 3, 0.9 / 10, 4 / 25], facecolor=ax_color)
        var_radio_2 = RadioButtons(
            ax=ax_var_radio_2,
            labels=var_label,
            active=para_2[2],
        )

        ax_var_radio_3 = plt.axes([51.5 / 100, 2.3 / 3, 0.9 / 10, 4 / 25], facecolor=ax_color)
        var_radio_3 = RadioButtons(
            ax=ax_var_radio_3,
            labels=var_label,
            active=para_3[2],
        )

        ax_var_radio_4 = plt.axes([51.5 / 100, 1 / 3, 0.9 / 10, 4 / 25], facecolor=ax_color)
        var_radio_4 = RadioButtons(
            ax=ax_var_radio_4,
            labels=var_label,
            active=para_4[2],
        )

        # Button
        ax_button = plt.axes([0.4, 0.03, 0.2, 0.07])
        button = Button(ax_button, 'Process')

        def update_all(value):
            plot_update_1()
            plot_update_2()
            plot_update_3()
            plot_update_4()

        def plot_update_1():
            nonlocal graph_1, level_1, plane_1, variable_1
            graph_1 = self.plot(plane_1, level_1, variable_1, ax_1, False)
            plt.show()

        def plot_update_2():
            nonlocal graph_2, level_2, plane_2, variable_2
            graph_2 = self.plot(plane_2, level_2, variable_2, ax_2, False)
            plt.show()

        def plot_update_3():
            nonlocal graph_3, level_3, plane_3, variable_3
            graph_3 = self.plot(plane_3, level_3, variable_3, ax_3, False)
            plt.show()

        def plot_update_4():
            nonlocal graph_4, level_4, plane_4, variable_4
            graph_4 = self.plot(plane_4, level_4, variable_4, ax_4, False)
            plt.show()

        button.on_clicked(update_all)

        def plane_update_1(value):
            nonlocal plane_1
            index = spec_radio_1.value_selected
            if index == 'Y-Z':
                plane_1 = 0
            elif index == 'X-Z':
                plane_1 = 1
            else:
                plane_1 = 2

        spec_radio_1.on_clicked(plane_update_1)

        def plane_update_2(value):
            nonlocal plane_2
            index = spec_radio_2.value_selected
            if index == 'Y-Z':
                plane_2 = 0
            elif index == 'X-Z':
                plane_2 = 1
            else:
                plane_2 = 2

        spec_radio_2.on_clicked(plane_update_2)

        def plane_update_3(value):
            nonlocal plane_3
            index = spec_radio_3.value_selected
            if index == 'Y-Z':
                plane_3 = 0
            elif index == 'X-Z':
                plane_3 = 1
            else:
                plane_3 = 2

        spec_radio_3.on_clicked(plane_update_3)

        def plane_update_4(value):
            nonlocal plane_4
            index = spec_radio_4.value_selected
            if index == 'Y-Z':
                plane_4 = 0
            elif index == 'X-Z':
                plane_4 = 1
            else:
                plane_4 = 2

        spec_radio_4.on_clicked(plane_update_4)

        def var_update_1(value):
            nonlocal variable_1
            variable_1 = var_radio_1.value_selected

        var_radio_1.on_clicked(var_update_1)

        def var_update_2(value):
            nonlocal variable_2
            variable_2 = var_radio_2.value_selected

        var_radio_2.on_clicked(var_update_2)

        def var_update_3(value):
            nonlocal variable_3
            variable_3 = var_radio_3.value_selected

        var_radio_3.on_clicked(var_update_3)

        def var_update_4(value):
            nonlocal variable_4
            variable_4 = var_radio_4.value_selected

        var_radio_4.on_clicked(var_update_4)

        def text_update_1(value):
            if -3 <= float(value) <= 3:
                nonlocal level_1
                level_1 = float(value)

        textbox_1.on_text_change(text_update_1)

        def text_update_2(value):
            if -3 <= float(value) <= 3:
                nonlocal level_2
                level_2 = float(value)

        textbox_2.on_text_change(text_update_2)

        def text_update_3(value):
            if -3 <= float(value) <= 3:
                nonlocal level_3
                level_3 = float(value)

        textbox_3.on_text_change(text_update_3)

        def text_update_4(value):
            if -3 <= float(value) <= 3:
                nonlocal level_4
                level_4 = float(value)

        textbox_4.on_text_change(text_update_4)

        plt.show()







