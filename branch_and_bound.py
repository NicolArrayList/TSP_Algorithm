import math
import time

max_size = float('inf')


# Function to get the final solution path
def get_final_path(current_path):
    final_path[:N + 1] = current_path[:]
    final_path[N] = current_path[0]


# Function to get the edge of a vertex i with the minimum cost
def minimum_edge(mat, i):
    min = max_size
    for j in range(N):
        if mat[i][j] < min and i != j:
            min = mat[i][j]

    return min


# Function to get the edge of a vertex i with the second minimum cost
# that will be used in lower bounds calculations
def second_minimum_edge(mat, i):
    min, second_min = max_size, max_size
    for j in range(N):
        if i == j:
            continue
        if mat[i][j] <= min:
            second_min = min
            min = mat[i][j]
        elif mat[i][j] <= second_min and mat[i][j] != min:
            second_min = mat[i][j]

    return second_min


# This a recursive function that allows to build the search tree and explore the right
# nodes according to their calculated lower bounds
def exploration(mat, current_bound, current_weight, exploration_level, current_path, visited):
    global final_result

    # First, we check if we're at the last level of the tree, which means all nodes
    # were covered
    if exploration_level == N:

        # We check if there is a way to go from the last vertex found back to the first to make a cycle
        # if not, the path explored can't be a solution
        if mat[current_path[exploration_level - 1]][current_path[0]] != 0:
            # current_result is the total weight of our current solution
            current_result = current_weight + mat[current_path[exploration_level - 1]][current_path[0]]

            # If the total coast of the current result is lower of the current final result, it becomes the
            # new final result (the best solution until now)
            if current_result < final_result:
                get_final_path(current_path)
                final_result = current_result

        return

    # For the other levels of exploration, we go through all vertices to build the search tree
    for i in range(N):

        # First, we care about not going from a vertex to the same vertex, which can't be possible in a cycle, and we
        # also check if we didn't already visit the next vertex (check if it's not already in our partial solution path)
        if mat[current_path[exploration_level - 1]][i] != 0 and visited[i] == False:
            temp_bound = current_bound
            current_weight += mat[current_path[exploration_level - 1]][i]

            # Update current bound depending on which level of exploration we are
            if exploration_level == 1:
                current_bound -= ((minimum_edge(mat, current_path[exploration_level - 1]) + minimum_edge(mat, i)) / 2)
            else:
                current_bound -= (
                        (second_minimum_edge(mat, current_path[exploration_level - 1]) + minimum_edge(mat, i)) / 2)

            # lower_bound is the current lower bound for the node of the tree we have arrived on
            lower_bound = current_bound + current_weight

            # If the lower bound is lower than the final result, then we need to continue the exploration
            if lower_bound < final_result:
                current_path[exploration_level] = i
                visited[i] = True

                # Recursive call to do the search for the next level
                exploration(mat, current_bound, current_weight, exploration_level + 1, current_path, visited)

            # If the lower bound isn't lower than the final result, we have to put back all the values of current weight
            # and current bound for the exploration of the next node, if there is one
            current_weight -= mat[current_path[exploration_level - 1]][i]
            current_bound = temp_bound

            # We also reset the visited array
            visited = [False] * len(visited)
            for j in range(exploration_level):
                if current_path[j] != -1:
                    visited[current_path[j]] = True


# This is the main function that will solve the traveler salesman problem (TSP) and will build the solution path
def TSP(mat):
    current_bound = 0
    current_path = [-1] * (N + 1)
    visited = [False] * N

    for i in range(N):
        current_bound += (minimum_edge(mat, i) + second_minimum_edge(mat, i))

    current_bound = math.ceil(current_bound / 2)

    visited[0] = True
    current_path[0] = 0

    exploration(mat, current_bound, 0, 1, current_path, visited)


# Number of vertices
N = 5

# final_path is where we store the solution path
final_path = [None] * (N + 1)

# array to keep the visited node for each path
visited = [False] * N

# Minimum cost of the solution cycle
final_result = max_size


def apply_BranchAndBound():
    # Adjacency matrix from the graph example in the report
    mat = [[0, 3, 1, 6, 1],
           [3, 0, 5, 2, 1],
           [1, 5, 0, 2, 3],
           [6, 2, 2, 0, 7],
           [1, 1, 3, 7, 0]]

    tic = time.perf_counter()
    TSP(mat)
    toc = time.perf_counter()

    print("Minimum cost :", final_result)
    print("Solution path : ", end=' ')
    for i in range(N + 1):
        print(chr(final_path[i] + 65), end=' ')

    print(f"\nBranch and Bound is done in {toc - tic:0.7f} seconds")
