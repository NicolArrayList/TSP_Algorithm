from AntColonyUtils.Models.Graph import Graph
from AntColonyUtils.Models.AntColony import AntColony
from AntColonyUtils.Models.MapGenerator import MapGenerator
from AntColonyUtils.Display.Display import *

from branch_and_bound import *

mat = [[0, 3, 1, 6, 1],
       [3, 0, 5, 2, 1],
       [1, 5, 0, 2, 3],
       [6, 2, 2, 0, 7],
       [1, 1, 3, 7, 0]]

mg = MapGenerator(5, 100, 100)

environment = Graph(mat)

ACO = AntColony(
       environment,
       ant_amount=20,
       pheromone_intensity=1,
       pheromone_factor=3,
       pheromone_dissipation=0.2,
       heuristic_factor=0.01)

result = ACO.run_colony(1, display=None)

apply_BranchAndBound(mat)

print("\nANT COLONY RESULT")
print("Best solution : \n - Best path : ", end=' ')
for i in range(len(result[1])):
    print(chr(result[1][i] + 65), end=' ')
print("\n - Best cost : " + str(result[0]))