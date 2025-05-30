
# Ant Colony Simulation with Pygame and Cython

This repository simulates ant behavior using **Pygame** for visualization. It explores different approaches to improve performance, from live real-time calculations to precomputed frames, and further optimizes the simulation using **Cython** to accelerate key sections. This is ideal for large-scale ant colony simulations where performance and smooth animation are critical.

---

## Features

- **Live Simulation (Default)**: The ants move in real-time, searching for food and leaving pheromone trails to guide others.
- **Precomputed Frames**: Precompute the frames ahead of time to improve performance and display the results as an animation.
- **Cython Optimization**: Accelerate computationally intensive sections using Cython for faster pheromone and movement calculations, especially for large ant colonies.

---

## Requirements

- Python 3.x
- Pygame
- Cython (for the optimized version)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ant-colony-simulation.git
   cd ant-colony-simulation
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, if you're using Cython for optimization:

   ```bash
   pip install cython
   ```

---

## Usage

### 1. Live Simulation (Default)

To run the simulation in real-time, simply execute the following:

```bash
python ant_simulation_live.py
```

This will run the simulation live, with ants moving, leaving pheromone trails, and searching for food in real-time.

### 2. Precompute Frames

For performance optimization, precompute all frames and display them as an animation. This approach is ideal for systems with limited processing power:

```bash
python ant_simulation_precalc.py
```

This will generate the frames first and then play them as a pre-recorded animation.

### 3. Cython Optimized Simulation

For large-scale simulations, using Cython optimizations can significantly improve performance. Ensure you have Cython installed, then run:

```bash
python ant_simulation_cython.py
```

This will execute the simulation with Cython-based optimizations, speeding up key calculations like pheromone updates and ant movement.

---

## How It Works

### Ant Behavior

- **Searching for Food**: Ants start at the anthill and move randomly, searching for food. They leave a pheromone trail to guide other ants towards food.
- **Returning to Anthill**: Once food is found, ants return to the anthill, leaving a different pheromone trail for others to follow.
- **Pheromone Decay**: Over time, the pheromone trails decay, creating a dynamic and ever-changing environment.

### Optimization Techniques

1. **Live Calculation**: Ant movement, pheromone updates, and collision checks are done live.
2. **Precomputed Frames**: Simulation steps are pre-calculated and stored as frames for faster playback.
3. **Cython**: Key sections of the code are accelerated using Cython, speeding up the simulation significantly, especially in the pheromone calculation and movement logic.

---

## Contributing

Feel free to contribute by submitting issues or pull requests. Whether it's improving performance, fixing bugs, or adding new features, all contributions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
