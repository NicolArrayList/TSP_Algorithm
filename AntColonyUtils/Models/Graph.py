from AntColonyUtils.Models.MapGenerator import MapGenerator


class Graph:
    """
    The Graph class uses a map generation to initialize a graph useful for the management of the ant colony.
    It carries all the information that make up the environment of the ant colony.
    """
    def __init__(self, distance_matrix: list[list[float]], points=None):
        self.points = points
        self.distance_matrix = distance_matrix
        self.size = len(self.distance_matrix)
        self.pheromone = list(list())
        self.reset_pheromones()

    def reset_pheromones(self):
        self.pheromone = [[1 / self.size for _ in range(self.size)] for _ in range(self.size)]

    def copy_as_blank_matrix(self):
        return [[0 for _ in range(self.size)] for _ in range(self.size)]
