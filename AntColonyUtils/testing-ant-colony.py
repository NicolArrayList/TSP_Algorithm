from Models.Graph import Graph
from Models.AntColony import AntColony
from Models.MapGenerator import MapGenerator
from Display.Display import *
import matplotlib.pyplot as plt


def test():
    mg = MapGenerator(50, 100, 100)

    environment = Graph(mg.distance_matrix, mg.points)

    display = Display(display_pheromone=True)

    result = list()

    ACO1 = AntColony(
        environment,
        ant_amount=10,
        pheromone_intensity=1,
        pheromone_factor=2,
        pheromone_dissipation=0.2,
        heuristic_factor=3,
        display=display)
    result1 = ACO1.run_colony(25)
    result.append(result1[1])
    print(result1)

    ACO2 = AntColony(
        environment,
        ant_amount=7,
        pheromone_intensity=0.5,
        pheromone_factor=3,
        pheromone_dissipation=0.3,
        heuristic_factor=5,
        display=display)
    result2 = ACO2.run_colony(5)
    result.append(result2[1])
    print(result2)


    """
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


if __name__ == "__main__":
    test()

    plt.ioff()
    plt.show(block=True)
