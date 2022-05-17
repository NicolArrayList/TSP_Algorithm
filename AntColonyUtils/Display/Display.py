import matplotlib.pyplot as plt


class Display:

    def __init__(self, display_pheromone: False):
        self.titles = list()
        self.environment = list()
        self.points = list()
        self.paths = list()

        self.display_pheromone = display_pheromone

        plt.ion()

        self.fig = None

        self.axs = list()
        self.paths_arrows = list()
        self.pheromones_arrows = list()

    def register_plot(self, environment):
        self.environment.append(environment)
        self.paths.append([])
        self.titles.append("WAITING FOR DATA")
        self.paths_arrows.append([])
        self.pheromones_arrows.append([])

        return len(self.environment) - 1

    def start_subplots(self):
        self.fig, self.axs = plt.subplots(len(self.paths), sharex="col")
        for index in range(len(self.axs)):
            self.axs[index].set_title("WAITING FOR DATA")

            points = self.environment[index].points
            x = []
            y = []
            for point in points:
                x.append(point[0])
                y.append(point[1])
            self.axs[index].plot(x, y, 'co')

            arrows = list()

            if self.display_pheromone:
                for i in range(len(self.environment[index].pheromone)):
                    for _ in range(i, len(self.environment[index].pheromone)):
                        arrows.append(self.axs[index].arrow(
                            0, 0, 0, 0,
                            color='#111',
                            alpha=0,
                            width=0
                        ))
                self.pheromones_arrows[index] = arrows

            arrows = list()

            for _ in range(len(self.environment[index].points) + 1):
                arrows.append(self.axs[index].arrow(
                    0, 0, 0, 0,
                    color='#111',
                    alpha=0,
                    width=0
                ))

            self.paths_arrows[index] = arrows

        self.fig.set_figwidth(5)
        self.fig.set_figheight(6)

        plt.subplots_adjust()
        plt.tight_layout()

        self.fig.canvas.flush_events()
        self.fig.canvas.manager.set_window_title('Ant Colonies')

    def update_plots(self):
        for i in range(len(self.axs)):
            self.update_plot(i, self.environment[i], self.paths[i], self.titles[i])

    def update_plot(self, index, environment, path, title):
        points = environment.points
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])

        ax = self.axs[index]
        ax.set_title(title, size=8)

        if self.display_pheromone:
            k = 0
            for i in range(len(environment.pheromone)):
                for j in range(i, len(environment.pheromone)):

                    if i != j:
                        if environment.pheromone[i][j] * 10 > 1:
                            a = 1
                        else:
                            a = environment.pheromone[i][j] * 10

                        self.pheromones_arrows[index][k].remove()

                        self.pheromones_arrows[index][k] = ax.arrow(
                            x[i], y[i], x[j] - x[i], y[j] - y[i],
                            color='#111',
                            length_includes_head=True,
                            alpha=a,
                            width=0.2
                        )
                    k += 1

        for k in range(1, len(path)):
            i = path[k - 1]
            j = path[k]
            self.paths_arrows[index][k].remove()
            self.paths_arrows[index][k] = \
                ax.arrow(
                    x[i], y[i],
                    x[j] - x[i], y[j] - y[i],
                    color='r', length_includes_head=True, width=0.1,
                    head_length=None
                )
            self.fig.draw_artist(self.paths_arrows[index][k])
        self.fig.canvas.flush_events()

    def update_plot_values(self, index, environment, path, title):
        self.environment[index] = environment
        self.paths[index] = path
        self.titles[index] = title

    def show_subplots_end(self):
        self.fig.show()
        plt.show(block=True)


"""
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
"""
