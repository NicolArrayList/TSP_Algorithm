import math
import random


class MapGenerator:
    """
    This class is in charge of generating a map with a given number of points.
    The points will be used by the heuristic and the distance calculation.
    We are here able to generate the distance matrix between each point which defines among other things, our graph.
    """
    def __init__(self, point_amount, width, height):
        self.point_amount = point_amount
        self.width = width
        self.height = height

        self.points = self.generate_points()
        self.distance_matrix = self.generate_distance_matrix()

    def generate_points(self):
        points = list()
        i = 0
        while i < self.point_amount:
            # We use the random library to generate the points
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            if (x, y) in points:
                i -= 1
            else:
                points.append((x, y))
                i += 1
        return points

    def generate_distance_matrix(self):
        distance_matrix = [[0 for _ in range(self.point_amount)] for _ in range(self.point_amount)]
        for i in range(self.point_amount):
            distance_matrix[i][i] = 0
            for j in range(i + 1, self.point_amount):
                # We calculate here the Euclidean distance between each point
                # Our graph is not oriented. That means the distance is the same between i-j and j-i
                distance_matrix[i][j] = ((self.points[j][0] - self.points[i][0]) ** 2 +
                                         (self.points[j][1] - self.points[i][1]) ** 2) ** 0.5
                distance_matrix[j][i] = distance_matrix[i][j]
        return distance_matrix
