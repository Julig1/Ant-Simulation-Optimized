# ant_simulation.pyx

import math
import numpy as np
cimport numpy as np

# Define the sense function as a cython function to improve speed
def sense(float angle_offset, np.ndarray pheromone_grid, float x, float y, float sense_distance, float angle):
    cdef int sx, sy
    cdef float sense_angle = angle + angle_offset
    sx = int(x + math.cos(sense_angle) * sense_distance)
    sy = int(y + math.sin(sense_angle) * sense_distance)

    if 0 <= sx < pheromone_grid.shape[0] and 0 <= sy < pheromone_grid.shape[1]:
        return pheromone_grid[sx, sy]
    return 0

# Define the update pheromone function (to speed up pheromone spreading)
def update_pheromone(np.ndarray pheromone_grid, int ix, int iy, float pheromone_strength):
    pheromone_grid[ix, iy] = min(255, pheromone_grid[ix, iy] + pheromone_strength)
