from AntColonyUtils.Models.Graph import Graph
from AntColonyUtils.Models.AntColony import AntColony
from AntColonyUtils.Models.MapGenerator import MapGenerator
from AntColonyUtils.Display.Display import *

from branch_and_bound import *

# Matrix from the branch and bound example in the report
mat = [[0, 3, 1, 6, 1],
       [3, 0, 5, 2, 1],
       [1, 5, 0, 2, 3],
       [6, 2, 2, 0, 7],
       [1, 1, 3, 7, 0]]

vertex_number = 10

mg = MapGenerator(vertex_number, 100, 100)

environment = Graph(mg.distance_matrix)

ACO = AntColony(
       environment,
       ant_amount=20,
       pheromone_intensity=1,
       pheromone_factor=3,
       pheromone_dissipation=0.2,
       heuristic_factor=0.01)

result = ACO.run_colony(3, display=None)

apply_BranchAndBound(mg.distance_matrix)

print("\n-----------------")
print("ANT COLONY RESULT")
print("-----------------")
print(" - Best path : ", end=' ')
for i in range(len(result[1])):
    print(chr(result[1][i] + 65), end=' ')
print("\n - Best cost : " + str(result[0]))
print(" - Best time elapsed : " + ("%.8f" % (result[2])))
