from Models.Graph import Graph
from Models.AntColony import AntColony
from Models.MapGenerator import MapGenerator
from Display.Display import *
import matplotlib.pyplot as plt

matrix = [
    [0, 2, 5],
    [2, 0, 4],
    [1, 8, 0]
]


def test():

    mg = MapGenerator(12, 100, 100)

    environment = Graph(mg)

    #display = Display()

    result = list()

    ACO1 = AntColony(
        environment,
        ant_amount=20,
        pheromone_intensity=1,
        pheromone_factor=1,
        pheromone_dissipation=0.2,
        heuristic_factor=3)
    result1 = ACO1.run_colony(75, display=None)
    result.append(result1[1])
    print(result1)

    plt.ioff()
    plt.show(block=True)

    """ACO2 = AntColony(
        environment,
        ant_amount=7,
        pheromone_intensity=0.5,
        pheromone_factor=3,
        pheromone_dissipation=0.3,
        heuristic_factor=5)
    result2 = ACO2.run_colony(5)
    result.append(result2[1])
    print(result2)

    ACO3 = AntColony(
        environment,
        ant_amount=7,
        pheromone_intensity=0.5,
        pheromone_factor=3,
        pheromone_dissipation=0.6,
        heuristic_factor=5)
    result3 = ACO3.run_colony(5)
    result.append(result3[1])
    print(result3)

    ACO4 = AntColony(
        environment,
        ant_amount=7,
        pheromone_intensity=0.5,
        pheromone_factor=3,
        pheromone_dissipation=0.9,
        heuristic_factor=5)
    result4 = ACO4.run_colony(5)
    result.append(result4[1])
    print(result4)

    run_subplot(mg.points, result)
    """


test()
