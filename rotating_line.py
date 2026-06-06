"""
A pgzero program that displays a line fixed at the center of the screen,
rotating at 12 degrees per second, with the current angle shown at the top.
"""

import pgzrun
from pgzero.screen import Screen
import math

WIDTH = 400
HEIGHT = 400
TITLE = "Rotating Line"

angle = 0  # degrees
screen: Screen


def update(dt):
    global angle
    angle += 12 * dt  # 12 degrees per second


def draw():
    screen.clear()
    cx, cy = WIDTH // 2, HEIGHT // 2
    rad = math.radians(angle)
    length = 150
    ex = cx + length * math.cos(rad)
    ey = cy + length * math.sin(rad)
    screen.draw.line((cx, cy), (ex, ey), 'black')
    screen.draw.filled_circle((cx, cy), 10, 'white')
    screen.draw.filled_circle((ex, ey), 5, 'white')
    screen.draw.text(f"{angle % 360:.0f}°",
                     center=(WIDTH // 2, 20), fontsize=30, color='white')


pgzrun.go()
