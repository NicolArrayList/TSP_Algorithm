from AntColonyUtils.Models.Graph import Graph
from AntColonyUtils.Models.AntColony import AntColony
from AntColonyUtils.Models.MapGenerator import MapGenerator
from AntColonyUtils.Display.Display import *

from branch_and_bound import *

mg = MapGenerator(5, 100, 100)

apply_BranchAndBound(mg.distance_matrix)
