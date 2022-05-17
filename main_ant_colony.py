import threading
import time

from AntColonyUtils.Models.Graph import Graph
from AntColonyUtils.Models.AntColony import AntColony
from AntColonyUtils.Models.MapGenerator import MapGenerator

from AntColonyUtils.Display.Display import *

global display, world, t_ACO, sync, thread_start, update_display, processing


def prepare_environment(points_amount, width, height):
    global world

    world = MapGenerator(points_amount, width=width, height=height)


def main():
    global display, t_ACO, sync, thread_start, update_display, processing
    update_display = False
    processing = True
    thread_start = False
    sync = list()

    display = Display(display_pheromone=False)
    t_display = threading.Thread(target=display_controller_thread, args=[1])
    t_display.start()

    t_ACO = list()

    prepare_environment(150, 1000, 1000)

    iteration = 25

    args = [
        [25, 0, 0, 1, 5, iteration],
        [25, 1, 2, 0.2, 5, iteration],
        [25, 1, 5, 0.2, 4, iteration]
    ]

    for i in range(len(args)):
        args[i].append(i)

    sync = [False] * len(args)

    for i in range(len(args)):
        t_ACO.append(threading.Thread(target=launch_colony_thread, args=args[i]))

    for i in range(len(args)):
        t_ACO[i].start()

    while not thread_start:
        print("waiting...")
        if all(sync):
            display.start_subplots()
            time.sleep(1)
            thread_start = True
            print(f"Starting process at : {time.time()}\n")

    while processing:
        if update_display:
            display.update_plots()
            update_display = False

        if not any(sync):
            processing = False

    display.show_subplots_end()
    print("Process Ended Successfully")


def display_controller_thread(interval_in_seconds):
    global update_display, processing

    while processing:
        update_display = True
        time.sleep(interval_in_seconds)


def launch_colony_thread(
        ant_amount,
        pheromone_intensity,
        pheromone_factor,
        pheromone_dissipation,
        heuristic_factor,
        iteration,
        thread_number
):
    global display, world, sync, thread_start

    environment = Graph(distance_matrix=world.distance_matrix, points=world.points)

    ACO = AntColony(
        environment,
        ant_amount=ant_amount,
        pheromone_intensity=pheromone_intensity,
        pheromone_factor=pheromone_factor,
        pheromone_dissipation=pheromone_dissipation,
        heuristic_factor=heuristic_factor,
        display=display
    )

    # Thread is ready to go
    sync[thread_number] = True
    print(f"Thread {thread_number} ready : {sync}\n")

    while not thread_start:
        time.sleep(0.1)

    result = ACO.run_colony(iteration, pause_delay=0.5)
    print(result)

    sync[thread_number] = False


if __name__ == '__main__':
    main()
