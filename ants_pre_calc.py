import pygame
import random
import sys
import math
import numpy as np

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Simulation")

# Settings
NUM_ANTS = 5000
ANT_RADIUS = 1
SPEED = 1.5
TURN_ANGLE = math.radians(15)
PHEROMONE_DECAY = 0.988
PHEROMONE_STRENGTH = 100
SENSE_DISTANCE = 5
SENSE_ANGLE = math.radians(30)
MAX_FRAMES = 2000  # Total number of frames to calculate

# Colors
WHITE = (255, 255, 255)
FOOD_COLOR = (0, 200, 0)

# Pheromone layers
pheromone_search = np.zeros((WIDTH, HEIGHT))
pheromone_return = np.zeros((WIDTH, HEIGHT))

# Food setup
food = []
for _ in range(10):
    fx = random.randint(50, WIDTH - 50)
    fy = random.randint(50, HEIGHT - 50)
    for _ in range(30):
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        food.append(pygame.Rect(fx + dx, fy + dy, 3, 3))

# Anthill
ANTHILL = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)

# Ants
ants = []
for _ in range(NUM_ANTS):
    angle = random.uniform(0, 2 * math.pi)
    ants.append({
        "x": WIDTH / 2,
        "y": HEIGHT / 2,
        "angle": angle,
        "state": "searching",
        "has_food": False
    })

# Frame buffer to store all frames
frames = []

# Font setup for displaying frame counter
font = pygame.font.SysFont('Arial', 24)

# Simulate and store frames
clock = pygame.time.Clock()
frame_count = 0
running = True
while running and frame_count < MAX_FRAMES:
    clock.tick(60)

    # Handle quit event (this is only needed if we interrupt the calculation)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pheromone decay
    pheromone_search *= PHEROMONE_DECAY
    pheromone_return *= PHEROMONE_DECAY

    # Ant logic
    for ant in ants:
        def sense(angle_offset, grid):
            angle = ant["angle"] + angle_offset
            sx = int(ant["x"] + math.cos(angle) * SENSE_DISTANCE)
            sy = int(ant["y"] + math.sin(angle) * SENSE_DISTANCE)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                return grid[sx, sy]
            return 0

        follow_grid = pheromone_return if ant["state"] == "searching" else pheromone_search
        center = sense(0, follow_grid)
        left = sense(-SENSE_ANGLE, follow_grid)
        right = sense(SENSE_ANGLE, follow_grid)

        if left > center and left > right:
            ant["angle"] -= TURN_ANGLE
        elif right > center and right > left:
            ant["angle"] += TURN_ANGLE
        else:
            ant["angle"] += random.uniform(-TURN_ANGLE, TURN_ANGLE)

        ant["x"] += math.cos(ant["angle"]) * SPEED
        ant["y"] += math.sin(ant["angle"]) * SPEED

        # Wall bounce
        if ant["x"] <= 0 or ant["x"] >= WIDTH - 1:
            ant["angle"] = math.pi - ant["angle"]
            ant["x"] = max(0, min(WIDTH - 1, ant["x"]))
        if ant["y"] <= 0 or ant["y"] >= HEIGHT - 1:
            ant["angle"] = -ant["angle"]
            ant["y"] = max(0, min(HEIGHT - 1, ant["y"]))

        ix, iy = int(ant["x"]), int(ant["y"])

        if ant["state"] == "searching":
            pheromone_search[ix, iy] = min(255, pheromone_search[ix, iy] + PHEROMONE_STRENGTH)
        else:
            pheromone_return[ix, iy] = min(255, pheromone_return[ix, iy] + PHEROMONE_STRENGTH)

        if ant["state"] == "searching":
            for f in food:
                if f.collidepoint(ant["x"], ant["y"]):
                    ant["state"] = "returning"
                    ant["has_food"] = True
                    food.remove(f)
                    break
        elif ant["state"] == "returning":
            if ANTHILL.collidepoint(ant["x"], ant["y"]):
                ant["state"] = "searching"
                ant["has_food"] = False

    # Save the frame to buffer
    frame_data = {
        "ants": [(int(ant["x"]), int(ant["y"])) for ant in ants],
        "food": [f.copy() for f in food],
        "pheromone_rgb": np.dstack((
            pheromone_return.clip(0, 255),
            np.zeros((WIDTH, HEIGHT)),
            pheromone_search.clip(0, 255)
        )).astype(np.uint8)
    }
    frames.append(frame_data)
    frame_count += 1

    # Display frame counter on the simulation window
    screen.fill(WHITE)
    frame_counter_text = font.render(f"Computing frame: {frame_count}/{MAX_FRAMES}", True, (0, 0, 0))
    screen.blit(frame_counter_text, (10, 10))

    pygame.display.flip()

# After simulation completes, playback frames
for frame in frames:
    screen.fill(WHITE)

    # Pheromone rendering
    pheromone_surface = pygame.surfarray.make_surface(frame["pheromone_rgb"])
    screen.blit(pygame.transform.smoothscale(pheromone_surface, (WIDTH, HEIGHT)), (0, 0))

    # Draw food
    for f in frame["food"]:
        pygame.draw.rect(screen, FOOD_COLOR, f)

    # Draw anthill
    pygame.draw.rect(screen, (150, 75, 0), ANTHILL)

    # Draw ants
    for x, y in frame["ants"]:
        pygame.draw.circle(screen, WHITE, (x, y), ANT_RADIUS)

    pygame.display.flip()
    pygame.time.delay(16)  # ~60 FPS for playback

pygame.quit()
sys.exit()
