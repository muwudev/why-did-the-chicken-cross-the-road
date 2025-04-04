import pygame
import os

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)

# Gameplay
GRAVITY = 1
JUMP_STRENGTH = 18
OBSTACLE_SPEED = 5
SPAWN_RATE = 1500  # ms between obstacles

# Paths
def asset_path(path):
    return os.path.join(os.path.dirname(__file__), 'assets', path)

DEATH_MESSAGES = [
    "SPLAT! You got kebab'd.",
    "CLUCK! That's gonna leave a mark.",
    "FEATHER FLYING FINISH!",
    "EGG-STREMELY bad landing.",
    "Poultry in motion... no longer."
]

DEATH_CAUSES = [
    "Slipped on onion.",
    "Tripped over own feet.",
    "Distracted by worm.",
    "Butcher got too close.",
    "Lost a feather duel."
]

BUTCHER_QUOTES = [
    "GET BACK HERE KEVIN!",
    "SUNDAY ROAST COMING UP!",
    "I NEED MORE CHICKEN WINGS!",
    "YOU'D TASTE GREAT FRIED!",
    "RUNNING WON'T SAVE YOU!"
]