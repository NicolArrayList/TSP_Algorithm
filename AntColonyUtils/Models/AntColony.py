import copy
import random
import time
from time import perf_counter

from AntColonyUtils.Models import Graph
from AntColonyUtils.Display import Display


class AntColony:
    def __init__(
            self,
            environment: Graph,
            ant_amount: int,
            pheromone_intensity: float,
            pheromone_factor: float,
            pheromone_dissipation: float,
            heuristic_factor: float,
    ):
        self.environment = environment
        self.heuristic = [
            [
                0 if i == j
                else 1 / self.environment.distance_matrix[i][j]
                for j in range(self.environment.size)
            ]
            for i in range(self.environment.size)
        ]

        self.ants_amount = ant_amount
        self.ants = [Ant(self) for _ in range(self.ants_amount)]

        self.Q = pheromone_intensity
        self.a = pheromone_factor
        self.b = heuristic_factor
        self.P = (1 - pheromone_dissipation)

    def update_pheromone(self):
        for i in range(self.environment.size):
            for j in range(self.environment.size):
                self.environment.pheromone[i][j] *= self.P
                for ant in self.ants:
                    self.environment.pheromone[i][j] += ant.emission_map[i][j]

    def run_colony(self, iteration: int, display: Display = None):
        t1_start = perf_counter()

        best_tour_cost = float('inf')
        current_solution = []
        index = None

        if display is not None:
            index = display.register_plot()

        for it in range(iteration):
            [best_tour_cost, current_solution] = self.cycle(best_tour_cost, current_solution)
            self.update_pheromone()

            t1_stop = perf_counter()

            print("\nCurrent solution : \n - current path : ", end=' ')
            for i in range(len(current_solution)):
                print(chr(current_solution[i] + 65), end=' ')
            print("\n - current cost : " + str(best_tour_cost), end=' ')
            print("\n - current time elapsed : " + ("%.6f" % (t1_stop-t1_start)) + "\t\t\t" + str([best_tour_cost]))

            if display is not None:
                display.update_plot(index, self.environment, current_solution,display_pheromone=False)
                time.sleep(0.1)

        return [best_tour_cost, current_solution]

    def cycle(self, best_tour_cost, current_solution):
        for ant in self.ants:
            ant.prepare_tour()

            for i in range(self.environment.size - 1):
                ant.choose_next_point()

            ant.tour_cost += self.environment.distance_matrix[ant.tour[-1]][ant.tour[0]]
            ant.tour.append(ant.tour[0])

            if ant.tour_cost < best_tour_cost:
                best_tour_cost = ant.tour_cost
                current_solution = copy.deepcopy(ant.tour)

            ant.update_pheromone_emission_cycle()
        return [best_tour_cost, current_solution]


class Ant:
    def __init__(self, colony: AntColony, emission_type: int = 0):
        self.colony = colony
        self.environment = colony.environment

        starting_point = random.randint(0, self.environment.size - 1)
        self.tour = [starting_point]
        self.allowed = [1 for i in range(self.environment.size)]
        self.allowed[starting_point] = 0

        self.tour_cost = 0
        self.current_point = starting_point

        self.emission_map = self.environment.copy_as_blank_matrix()

    def prepare_tour(self):
        starting_point = random.randint(0, self.environment.size - 1)
        self.tour = [starting_point]
        self.allowed = [1 for i in range(self.environment.size)]
        self.allowed[starting_point] = 0

        self.tour_cost = 0
        self.current_point = starting_point

        self.emission_map = self.environment.copy_as_blank_matrix()

    def choose_next_point(self):
        tau_sum = 0
        probabilities = [0 for i in range(self.environment.size)]

        for i in range(self.environment.size):
            if self.allowed[i] != 0:
                probabilities[i] = self.environment.pheromone[self.current_point][i] ** self.colony.a * \
                                   self.colony.heuristic[self.current_point][i] ** self.colony.b
                tau_sum += probabilities[i]

        for i in range(self.environment.size):
            if self.allowed[i] != 0:
                if tau_sum == 0.0:
                    probabilities[i] = 1
                    print(probabilities)
                else:
                    probabilities[i] /= tau_sum

        rand = random.random()
        for i in range(self.environment.size):
            rand -= probabilities[i]
            if rand <= 0:
                self.allowed[i] = 0
                self.tour.append(i)
                self.tour_cost += self.environment.distance_matrix[self.current_point][i]
                self.current_point = i
                break

    def update_pheromone_emission_cycle(self):
        for k in range(1, len(self.tour)):
            i = self.tour[k - 1]
            j = self.tour[k]
            self.emission_map[i][j] = self.colony.Q / self.tour_cost
