import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.plot_data = []

    @staticmethod
    def draw_data_set(data_set):
        first = True
        units = data_set.get_entries_by_units()
        loc = len(units)
        for unit in units:
            if first:
                first = False
                fig, x = plt.subplots()
                ax1 = x
                ax1.set_xlabel(data_set.x_data.units)
                line_style = 'solid'
            else:
                x = ax1.twinx()
                line_style = 'dashed'
            for_legend = []
            for entry in units[unit]:
                line, = x.plot(data_set.x_data, data_set[entry], label=data_set[entry].name, linestyle=line_style)
                x.set_ylabel(data_set[entry].units)
                for_legend += [line]
            plt.legend(handles=for_legend, loc=loc)
            loc -= 1
            lim = x.get_ylim()
            x.set_ylim(lim[0], lim[1] * 1.2)
        plt.title(data_set.get_title())
        plt.show()
