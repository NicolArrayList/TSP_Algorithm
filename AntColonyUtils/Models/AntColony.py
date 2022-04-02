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
        """
        The AntColony class is responsible for the management of the ant colony.
        It sends the ants in the environment and updates the pheromones.

        :param environment: Graph pass to describe environment
        :param ant_amount: Number of ants wandering
        :param pheromone_intensity: Intensity of pheromone deposit
        :param pheromone_factor: pheromone factor exponent
        :param pheromone_dissipation: dissipation value for pheromone (1 is total dissipation and 0 is no dissipation)
        :param heuristic_factor: heuristic factor exponent
        """
        self.environment = environment

        # heuristic is based on the distance between point
        # Basically heuristic[i][j] is the inverted distance between i and j
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
        """
        This method update the pheromone value of the environment based on ant deposits.
        It also decreases pheromone by a factor of P which is (1 - "dissipation")
        :return: None
        """
        for i in range(self.environment.size):
            for j in range(self.environment.size):
                self.environment.pheromone[i][j] *= self.P
                for ant in self.ants:
                    self.environment.pheromone[i][j] += ant.emission_map[i][j]

    def run_colony(self, iteration: int, display: Display = None):
        """

        :param iteration: Number of iteration done before ending the graph exploration
        :param display: if you want a pyplot display or not
        :return: [the best cost tour, the path to do it, elapsed time find it]
        """
        t1_start = perf_counter()

        # No best tour so we set it to infinity
        best_tour_cost = float('inf')
        # No current solution
        current_solution = []
        # No current best time
        best_time = 0

        # Index is used to find the plot in various subplot
        index = None

        print("-----------------")
        print("ANT COLONY METHOD")
        print("-----------------")
        if display is not None:
            index = display.register_plot()

        # Iterations start here
        for it in range(iteration):
            # For each iteration we send our ants to find the best path
            [best_tour_cost, current_solution, best_time] = self.cycle(best_tour_cost, current_solution, best_time)

            # After all ants completed their work, we can update pheromones
            # This can be done during the exploration. However, it's simpler this way
            self.update_pheromone()

            # Console revue
            print("\nCurrent solution : \n - current path : ", end=' ')
            for i in range(len(current_solution)):
                print(chr(current_solution[i] + 65), end=' ')
            print("\n - current cost : " + str(best_tour_cost) + "\n")

            # Display
            if display is not None:
                display.update_plot(index, self.environment, current_solution, display_pheromone=True)
                time.sleep(0.5)

        # We return the best we got
        return [best_tour_cost, current_solution, best_time-t1_start]

    def cycle(self, best_tour_cost, current_solution, best_time=None):
        """
        cycle method send ants to find the best path.
        Ants choose their path with a probability based on the heuristic and the pheromone values.
        :param best_tour_cost:
        :param current_solution:
        :param best_time:
        :return:
        """
        # For each ant we prepare it and send it
        for ant in self.ants:
            # Reset ant values
            ant.prepare_tour()

            # Our goal is to go through every destination
            # So we choose to move the ant as many times as there are stops (-1 because we start somewhere!)
            for i in range(self.environment.size - 1):
                ant.choose_next_point()

            # Once the tour is done we can come back to the starting point
            ant.tour_cost += self.environment.distance_matrix[ant.tour[-1]][ant.tour[0]]
            ant.tour.append(ant.tour[0])

            # If this tour is the best we rewrite the passed values
            if ant.tour_cost < best_tour_cost:
                best_tour_cost = ant.tour_cost
                current_solution = copy.deepcopy(ant.tour)
                best_time = perf_counter()

            # Update the pheromone map deposits of the ant
            ant.update_pheromone_emission_cycle()
        return [best_tour_cost, current_solution, best_time]


class Ant:
    def __init__(self, colony: AntColony, emission_type: int = 0):
        """
        The ant is our little explorer. It can go from a point to another. It obviously has a colony.
        Ant calculate the amount of pheromone deposits they leave behind them in a pheromone emission map.
        :param colony: the colony attached to the ant
        :param emission_type: this value is experimental for various ways of leaving the pheromone
        """
        self.colony = colony
        self.environment = colony.environment

        # We start somewhere
        starting_point = random.randint(0, self.environment.size - 1)
        self.tour = [starting_point]
        self.allowed = [1 for i in range(self.environment.size)]
        self.allowed[starting_point] = 0

        self.tour_cost = 0
        self.current_point = starting_point

        self.emission_map = self.environment.copy_as_blank_matrix()

    # Reset ant's values
    def prepare_tour(self):
        starting_point = random.randint(0, self.environment.size - 1)
        self.tour = [starting_point]
        self.allowed = [1 for i in range(self.environment.size)]
        self.allowed[starting_point] = 0

        self.tour_cost = 0
        self.current_point = starting_point

        self.emission_map = self.environment.copy_as_blank_matrix()

    def choose_next_point(self):
        """
        Change the position of the ant. An ant can't go back to a past position in the graph.
        The decision is made based on heuristic and pheromone maps.
        (cf. AntColony mathematics section in the report)
        :return: None
        """
        tau_sum = 0
        probabilities = [0 for i in range(self.environment.size)]

        # If the heuristic value or the pheromone value is a high value then the probability for this destination
        # is a high probability.
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

        # Randomly choose a destination
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
        """
        For each road traveled, the ant update its pheromone emission map based on the distance it has done.
        :return: None
        """
        for k in range(1, len(self.tour)):
            i = self.tour[k - 1]
            j = self.tour[k]
            self.emission_map[i][j] = self.colony.Q / self.tour_cost
