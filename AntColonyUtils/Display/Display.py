import operator
import matplotlib.pyplot as plt


class Display:

    def __init__(self):
        self.points = list()
        self.paths = list()
        plt.ion()

        self.fig = plt.figure()

        self.c_subplot = 111
        self.axs = list()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def register_plot(self):
        ax = self.fig.add_subplot(self.c_subplot)
        self.axs.append(ax)

        return len(self.points) - 1

    def update_plot(self, index, environment, path, display_pheromone: bool = False):
        points = environment.points

        ax = self.axs[index]

        x = []
        y = []

        ax.clear()
        for point in points:
            x.append(point[0])
            y.append(point[1])
        ax.plot(x, y, 'co')

        if display_pheromone:
            for i in range(len(environment.pheromone)):
                for j in range(i, len(environment.pheromone)):
                    if i != j:
                        if environment.pheromone[i][j]*10 > 1:
                            a = 1
                        else:
                            a = environment.pheromone[i][j]*10

                        ax.arrow(
                            x[i], y[i], x[j] - x[i], y[j] - y[i],
                            color='grey',
                            length_includes_head=True,
                            alpha=a,
                            width=0.2
                        )

        for _ in range(1, len(path)):
            i = path[_ - 1]
            j = path[_]
            ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True, width=0.1, head_length=None)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def run_subplot(points, paths):
    plots_amount = len(paths)
    a = plots_amount // 2
    b = plots_amount % 2

    fig, axs = plt.subplots(2, 2, sharex='col')

    index = 0
    for row in axs:
        for ax in row:
            subplot(ax, points, paths[index])
            ax.set_title("Plot " + str(index))
            index += 1

    plt.show()


def subplot(axs, points, path):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])

    axs.plot(x, y, 'co')

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        # noinspection PyUnresolvedReferences
        axs.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)


def plot(points, path: list):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    # noinspection PyUnusedLocal
    plt.plot(x, y, 'co')

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        # noinspection PyUnresolvedReferences
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)
    # noinspection PyTypeChecker
    plt.xlim(0, max(x) * 1.1)
    # noinspection PyTypeChecker
    plt.ylim(0, max(y) * 1.1)
    plt.show()
