# Solving the TSP problem with Ant Colony and Branch and Bounds

Intro

This solution is working under python 3.9, you'll need matplotlib to see the main_ant_colony.py work. 
We strongly advise you to use PyCharm.

! ANT COLONY IS STILL A WORK IN PROGRESS !

1) Run the main.py file to solve the problem with the branch and bound and the ant colony methods.
To change the size of the graph to solve, change the vertex_number value in main.py.

2) Run main_ant_colony.py to see 3 ant colonies working with different parameters live. Each colony work with it's own thread :

![alt text](https://github.com/NicolArrayList/TSP_Algorithm/blob/main/other/ScreenShots/Capture%20d’écran%202022-05-16%20233555.png)

By updating values in the main_ant_colony.py, you can change the size and the number of points in the environment.
You can also change colonies parameters. Everything is at the beginning of the file.

![alt text](https://github.com/NicolArrayList/TSP_Algorithm/blob/main/other/ScreenShots/Capture%20d’écran%202022-05-16%20234324.png)

Colonies paramters :

- Q : pheromone constant 

- a : pheromone exponent, defines the importance of pheromones in the ant's decision

- b : heuristic exponent, defines the importance of heuristic (nearest neighbor) in the ant's decision

- P : pheromone disipation (0 : no dissipation, 1 : total dissipation)

- n : number of ants

- iteration : number of iteration for each ant before stopping the colony

NOTE : pheromone_display is a work in progress don't use it with too many points !

See the PDF presentation for more details !

Thank you

Pheromone display :

![alt text](https://github.com/NicolArrayList/TSP_Algorithm/blob/main/other/ScreenShots/Capture%20d’écran%202022-05-16%20235613.png)

