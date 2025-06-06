import pygame
import random
import sys
import math
import numpy as np

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600  # Reduced for performance
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Simulation")

# Settings
NUM_ANTS = 500
ANT_RADIUS = 1
SPEED = 1.5
TURN_ANGLE = math.radians(15)
PHEROMONE_DECAY = 0.988
PHEROMONE_STRENGTH = 100
SENSE_DISTANCE = 5
SENSE_ANGLE = math.radians(30)

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FOOD_COLOR = (0, 200, 0)
WHITE = (255, 255, 255)

# Pheromone layers (float intensity values)
pheromone_search = np.zeros((WIDTH, HEIGHT))
pheromone_return = np.zeros((WIDTH, HEIGHT))

# Food setup: clumps
food = []
for _ in range(10):  # 10 clumps
    fx = random.randint(50, WIDTH - 50)
    fy = random.randint(50, HEIGHT - 50)
    for _ in range(30):  # 30 pieces per clump
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        food.append(pygame.Rect(fx + dx, fy + dy, 3, 3))

# Anthill in center
ANTHILL = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)

# Ants
ants = []
for _ in range(NUM_ANTS):
    angle = random.uniform(0, 2 * math.pi)
    ants.append({
        "x": WIDTH / 2,
        "y": HEIGHT / 2,
        "angle": angle,
        "state": "searching",  # or "returning"
        "has_food": False
    })

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Pheromone decay
    pheromone_search *= PHEROMONE_DECAY
    pheromone_return *= PHEROMONE_DECAY

    # Ant logic
    for ant in ants:
        x, y = int(ant["x"]), int(ant["y"])

        # Sense pheromone (front, left, right)
        def sense(angle_offset, pheromone_grid):
            angle = ant["angle"] + angle_offset
            sx = int(ant["x"] + math.cos(angle) * SENSE_DISTANCE)
            sy = int(ant["y"] + math.sin(angle) * SENSE_DISTANCE)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                return pheromone_grid[sx, sy]
            return 0

        # Pick which pheromone to follow
        follow_grid = pheromone_return if ant["state"] == "searching" else pheromone_search

        # Steering decision
        center = sense(0, follow_grid)
        left = sense(-SENSE_ANGLE, follow_grid)
        right = sense(SENSE_ANGLE, follow_grid)
        if left > center and left > right:
            ant["angle"] -= TURN_ANGLE
        elif right > center and right > left:
            ant["angle"] += TURN_ANGLE
        else:
            ant["angle"] += random.uniform(-TURN_ANGLE, TURN_ANGLE)

        # Move ant
        ant["x"] += math.cos(ant["angle"]) * SPEED
        ant["y"] += math.sin(ant["angle"]) * SPEED

        # Clamp position
        # Bounce off walls
        if ant["x"] <= 0 or ant["x"] >= WIDTH - 1:
            ant["angle"] = math.pi - ant["angle"]
            ant["x"] = max(0, min(WIDTH - 1, ant["x"]))
        if ant["y"] <= 0 or ant["y"] >= HEIGHT - 1:
            ant["angle"] = -ant["angle"]
            ant["y"] = max(0, min(HEIGHT - 1, ant["y"]))


        ix, iy = int(ant["x"]), int(ant["y"])

        # Leave pheromone
        if ant["state"] == "searching":
            pheromone_search[ix, iy] = min(255, pheromone_search[ix, iy] + PHEROMONE_STRENGTH)
        else:
            pheromone_return[ix, iy] = min(255, pheromone_return[ix, iy] + PHEROMONE_STRENGTH)

        # Check for food
        if ant["state"] == "searching":
            for f in food:
                if f.collidepoint(ant["x"], ant["y"]):
                    ant["state"] = "returning"
                    ant["has_food"] = True
                    food.remove(f)
                    break

        # Check for home
        elif ant["state"] == "returning":
            if ANTHILL.collidepoint(ant["x"], ant["y"]):
                ant["state"] = "searching"
                ant["has_food"] = False

    # Draw
    # ✅ Clear screen with white background FIRST
    screen.fill((255, 255, 255))  # RGB for white

    # Transpose the pheromone array correctly (to shape H x W x 3)
    pheromone_rgb = np.dstack((
        pheromone_return.clip(0, 255),               # Red channel
        np.zeros((WIDTH, HEIGHT)),                  # Green channel
        pheromone_search.clip(0, 255)               # Blue channel
    )).astype(np.uint8)         # Transpose to (HEIGHT, WIDTH, 3)

    pheromone_surface = pygame.surfarray.make_surface(pheromone_rgb)
    screen.blit(pygame.transform.smoothscale(pheromone_surface, (WIDTH, HEIGHT)), (0, 0))

    # Draw food
    for f in food:
        pygame.draw.rect(screen, FOOD_COLOR, f)

    # Draw anthill
    pygame.draw.rect(screen, (150, 75, 0), ANTHILL)

    # Draw ants
    for ant in ants:
        pygame.draw.circle(screen, (255, 255, 255), (int(ant["x"]), int(ant["y"])), ANT_RADIUS)

    pygame.display.flip()

pygame.quit()
sys.exit()