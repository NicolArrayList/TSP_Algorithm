import copy
import os

from Models.Graph import Graph
from Models.AntColony import AntColony
from Models.MapGenerator import MapGenerator

import numpy as np
import pickle
import matplotlib.pyplot as plt

map_parameters = [
    # [20, 1000, 1000],
    # [35, 1000, 1000],
    # [50, 1000, 1000],
    # [75, 1000, 1000],
    #[100, 1000, 1000],
     [125, 1000, 1000],
    # [150, 1000, 1000],
    # [175, 1000, 1000],
     # [200, 1000, 1000],
    # [225, 1000, 1000],
    # [250, 1000, 1000],
     # [300, 1000, 1000],
    # [350, 1000, 1000],
    # [400, 1000, 1000],
    # [450, 1000, 1000],
     # [500, 1000, 1000],
]

aco_parameters = [
    "ant_count",
    "pheromone_intensity",
    "pheromone_exp_factor",
    "pheromone_dissipation",
    "heuristique_exp_factor"
]

range_configs = {
    "test": {
        aco_parameters[0]: range(8, 10),
        aco_parameters[1]: np.arange(0, 12, 4),
        aco_parameters[2]: np.arange(0, 12, 4),
        aco_parameters[3]: np.arange(0, 1, 0.3),
        aco_parameters[4]: np.arange(1, 13, 4)
    },
    "normal": {
        aco_parameters[0]: range(1, 20, 5),
        aco_parameters[1]: np.arange(0, 5, 1),
        aco_parameters[2]: np.arange(0, 7, 1),
        aco_parameters[3]: np.arange(0, 1.1, 0.1),
        aco_parameters[4]: np.arange(2, 8, 1)
    },
    "big": {
        aco_parameters[0]: range(10, 25, 5),
        aco_parameters[1]: [1, 4],
        aco_parameters[2]: [0, 1, 5, 7],
        aco_parameters[3]: np.arange(0, 1.2, 0.2),
        aco_parameters[4]: [6, 8, 12]
    }
}

aco_parameters = [
    "ant_count",
    "pheromone_intensity",
    "pheromone_exp_factor",
    "pheromone_dissipation",
    "heuristique_exp_factor"
]


def generate_map(args):
    world = MapGenerator(args[0], width=args[1], height=args[2])
    return world


def generate_maps(args_list):
    worlds = list()
    for args in args_list:
        worlds.append(generate_map(args))
    return worlds


def calculate_configuration(
        ant_range,
        p_intensity_range,
        p_e_factor_range,
        p_dissipation_range,
        h_e_factor_range
):
    configs = {
        aco_parameters[0]: [i for i in ant_range],
        aco_parameters[1]: [i for i in p_intensity_range],
        aco_parameters[2]: [i for i in p_e_factor_range],
        aco_parameters[3]: [i for i in p_dissipation_range],
        aco_parameters[4]: [i for i in h_e_factor_range]
    }
    return configs


def get_data_from_configuration(world_graph, configurations, iteration):
    aco = AntColony(
        world_graph,
        ant_amount=configurations[0],
        pheromone_intensity=configurations[1],
        pheromone_factor=configurations[2],
        pheromone_dissipation=configurations[3],
        heuristic_factor=configurations[4]
    )

    result = aco.run_colony(iteration)
    world_graph.reset_pheromones()

    return result[::2]


def run_configs_with_maps(worlds: list[MapGenerator], configs):
    for world in worlds:
        graph = Graph(world.distance_matrix)

        results = iterate_through_parameter(copy.deepcopy(aco_parameters), configs, graph, [])

        write_result(
            {graph.size: results}
        )


def iterate_through_parameter(parameters, configs, graph, current_config):
    results = list()
    if len(parameters) == 1:
        for value in configs[parameters[0]]:
            current_config.append(value)
            results.append((copy.deepcopy(current_config), get_data_from_configuration(graph, current_config, 10)))
            current_config.pop()
        return results
    else:
        for value in configs[parameters[0]]:
            current_config.append(value)
            down_result = iterate_through_parameter(parameters[1:], configs, graph, current_config)
            current_config.pop()
            for result in down_result:
                results.append(result)
        return results


def write_result(results):
    name = "results/stats_" + str(list(results.keys())[0]) + ".pkl"

    file = open(name, "wb")
    pickle.dump(results, file)


def load_data(filename):
    data2 = []
    with open(filename, "rb") as f:
        dict_data = pickle.load(f)

        data = list(dict_data.values())[0]
        for i in data:
            data2.append(i)
    return dict_data


def plotting_data(dict_data: dict):
    left = 0.125  # the left side of the subplots of the figure
    right = 0.9  # the right side of the subplots of the figure
    bottom = 0.1  # the bottom of the subplots of the figure
    top = 0.9  # the top of the subplots of the figure
    wspace = 0  # the amount of width reserved for blank space between subplots
    hspace = 0  # the amount of height reserved for white space between subplots

    point_amount = list(dict_data.keys())[0]
    datas = list(dict_data.values())[0]
    parameters_count = len(aco_parameters) - 1

    fig, axs = plt.subplots(
        len(list(dict_data.items())[0][1][0][1]),
        parameters_count,
        sharex="col",
        sharey="row"
    )
    fig.canvas.manager.set_window_title('Ant Colonies stats for ' + str(point_amount) + ' points')

    fig.text(0, 0.5, 'common ylabel', ha='center', va='center', rotation='vertical')

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.subplots_adjust(
        left=left,
        right=right,
        bottom=bottom,
        top=top,
        wspace=wspace,
        hspace=hspace
    )

    axs[0, 0].set_ylabel("Time in second")
    axs[1, 0].set_ylabel("distance in meters")

    for parameters in range(len(aco_parameters)):
        x = range_configs["test"][aco_parameters[parameters]]
        y_time = []
        y_distance = []

        axs_time = axs[0, parameters - 1]
        axs_distance = axs[1, parameters - 1]

        # axs_time.title.set_text(aco_parameters[parameters])

        for x_value in x:
            total_time = 0
            total_distance = 0
            i = 0
            for data in datas:
                if x_value == data[0][parameters]:
                    total_time += data[1][1]
                    total_distance += data[1][0]
                    i += 1
            total_time /= i
            total_distance /= i
            y_time.append(total_time)
            y_distance.append(total_distance)

        axs_time.plot(x, y_time)
        axs_distance.plot(x, y_distance)
        axs_distance.set_xlabel(aco_parameters[parameters])


def plotting_datas(dict_data: list[dict]):
    left = 0.125  # the left side of the subplots of the figure
    right = 0.9  # the right side of the subplots of the figure
    bottom = 0.1  # the bottom of the subplots of the figure
    top = 0.9  # the top of the subplots of the figure
    wspace = 0  # the amount of width reserved for blank space between subplots
    hspace = 0  # the amount of height reserved for white space between subplots

    parameters_count = len(aco_parameters)

    fig, axs = plt.subplots(
        len(list(dict_data[0].items())[0][1][0][1]),
        parameters_count,
        sharex="col",
        sharey="row"
    )
    fig.canvas.manager.set_window_title('Ant Colonies stats')

    fig.text(0, 0.5, 'common ylabel', ha='center', va='center', rotation='vertical')

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.subplots_adjust(
        left=left,
        right=right,
        bottom=bottom,
        top=top,
        wspace=wspace,
        hspace=hspace
    )

    axs[0, 0].set_ylabel("Time in second")
    axs[1, 0].set_ylabel("distance in meters")

    for current_dict in dict_data:
        datas = list(current_dict.values())[0]
        point_amount = list(current_dict.keys())[0]

        for parameters in range(len(aco_parameters)):
            x = range_configs["big"][aco_parameters[parameters]]
            y_time = []
            y_distance = []

            axs_time = axs[0, parameters]
            axs_distance = axs[1, parameters]

            # axs_time.title.set_text(aco_parameters[parameters])

            for x_value in x:
                total_time = 0
                total_distance = 0
                i = 0
                for data in datas:
                    if x_value == data[0][parameters]:
                        total_time += data[1][1]
                        total_distance += data[1][0]
                        i += 1
                if i == 0:
                    print(x_value)
                total_time /= i
                total_distance /= i
                y_time.append(total_time)
                y_distance.append(total_distance)

            axs_time.plot(x, y_time, label=point_amount)
            axs_distance.plot(x, y_distance, label=point_amount)
            axs_distance.set_xlabel(aco_parameters[parameters])
            axs_time.legend()


def main():

    config_range = range_configs["big"]

    configs = calculate_configuration(
        ant_range=config_range[aco_parameters[0]],
        p_intensity_range=config_range[aco_parameters[1]],
        p_e_factor_range=config_range[aco_parameters[2]],
        p_dissipation_range=config_range[aco_parameters[3]],
        h_e_factor_range=config_range[aco_parameters[4]]
    )
    worlds = generate_maps(map_parameters)
    run_configs_with_maps(worlds, configs)


def load_results():
    dict_list = list()
    for filename in os.scandir("results"):
        if filename.is_file():
            print("Loading : " + str(filename))
            dict_list.append(load_data(filename))

    return dict_list


def load_and_plot_results():
    dict_list = load_results()

    plotting_datas(dict_list)
    plt.show()


def load_and_find_best():
    dict_list = load_results()

    for current_dict in dict_list:
        best = float('inf')
        best_data = None
        datas = list(current_dict.values())[0]
        point_amount = list(current_dict.keys())[0]
        for data in datas:
            current_dist = data[1][0]
            if current_dist < best:
                best = current_dist
                best_data = data
        print("points = " + str(point_amount) + " : " + str(best_data))





    return None


if __name__ == '__main__':
    #main()

    #load_and_plot_results()
    load_and_find_best()

    #results = list()
    #for i in range(10):
    #    world = generate_map(map_parameters[0])
#
    #    graph = Graph(world.distance_matrix)
#
    #    aco = AntColony(
    #        graph,
    #        ant_amount=10,
    #        pheromone_intensity=1,
    #        pheromone_factor=0,
    #        pheromone_dissipation=1,
    #        heuristic_factor=12
    #    )
#
    #    result = aco.run_colony(10)
    #    results.append(result)
    #    print(result[::2])
#
    #sum = 0
    #sum2 = 0
    #for i in range(len(results)):
    #    sum += results[i][0]
    #    sum2 += results[i][2]
    #print("Moyenne pour un configuration heuristique à 12 : " + str([sum/len(results), sum2/len(results)]))