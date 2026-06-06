from enum import Enum

import pgzrun
import pygame
from pgzero.screen import Screen
from pygame import Rect


class Destination(Enum):
    MIAMI = "Miami"
    NYC = "New York City"


class State(Enum):
    STOPPED = "stop"
    ACCELERATING = "accelerating"
    CRUISING = "cruising"
    DECELERATING = "decelerating"


# set up window
TITLE = "AMTRAK SILVER METEOR"
WIDTH = 900
HEIGHT = 450

# station positions
STATION_NYC_X = 100
STATION_MIAMI_X = 800
TRACK_Y = 320

# scale distance of 1400 miles between NYC and Miami
MILES_PER_PIXEL = 1400 // (STATION_MIAMI_X - STATION_NYC_X)
MPH_SCALE = 30
MAX_SPEED = 4
ACCELERATION = 0.05

screen: Screen
button = Rect(400, 380, 100, 50)
train_x = STATION_NYC_X
target_station = Destination.MIAMI
train_speed = 0
state = State.STOPPED


def draw_train(x, track_y):
    body_top = track_y - 45
    body_bottom = track_y - 10
    body_height = body_bottom - body_top

    # rectangular body
    screen.draw.filled_rect(Rect(x - 35, body_top, 70, body_height), (180, 0, 0))

    # front of train
    front_points = [
        (x + 35, body_top),
        (x + 55, body_top + body_height / 2),
        (x + 35, body_bottom)
    ]
    pygame.draw.polygon(screen.surface, (180, 0, 0), front_points)

    # back of train
    back_points = [
        (x - 35, body_top),
        (x - 55, body_top + body_height / 2),
        (x - 35, body_bottom)
    ]
    pygame.draw.polygon(screen.surface, (180, 0, 0), back_points)

    # windows
    screen.draw.filled_rect(Rect(x - 25, body_top + 5, 12, 12), (200, 230, 255))
    screen.draw.filled_rect(Rect(x - 5, body_top + 5, 12, 12), (200, 230, 255))
    screen.draw.filled_rect(Rect(x + 13, body_top + 5, 12, 12), (200, 230, 255))

    # wheels
    screen.draw.filled_circle((x - 25, track_y - 5), 10, (40, 40, 40))
    screen.draw.filled_circle((x, track_y - 5), 10, (40, 40, 40))
    screen.draw.filled_circle((x + 25, track_y - 5), 10, (40, 40, 40))

    # wheel hubs
    screen.draw.filled_circle((x - 25, track_y - 5), 4, (100, 100, 100))
    screen.draw.filled_circle((x, track_y - 5), 4, (100, 100, 100))
    screen.draw.filled_circle((x + 25, track_y - 5), 4, (100, 100, 100))


# draw stuff
def draw():
    # background(sky)
    screen.fill((135, 206, 235))

    # ground
    screen.draw.filled_rect(Rect(0, TRACK_Y, WIDTH, HEIGHT - TRACK_Y), (210, 180, 140))

    # draw tracks (rails and ties)
    screen.draw.filled_rect(Rect(50, TRACK_Y, 800, 5), (80, 80, 80))  # top rail
    screen.draw.filled_rect(Rect(50, TRACK_Y + 15, 800, 5), (80, 80, 80))  # bottom rail
    for x in range(55, 850, 30):
        screen.draw.filled_rect(Rect(x, TRACK_Y + 5, 5, 10), (131, 67, 33))  # ties

    # draw the action button
    screen.draw.filled_rect(button, (0, 180, 0))
    screen.draw.rect(button, (0, 100, 0))
    screen.draw.text("DEPART", center=button.center, fontsize=32, color="white")

    # nyc station "left"
    screen.draw.filled_rect(Rect(STATION_NYC_X - 60, TRACK_Y - 55, 120, 55), (160, 160, 160))
    screen.draw.text("New York City", center=(STATION_NYC_X, TRACK_Y - 70), fontsize=28, color="Dark Blue")

    # Miami station "right"
    screen.draw.filled_rect(Rect(STATION_MIAMI_X - 60, TRACK_Y - 55, 120, 55), (160, 160, 160))
    screen.draw.text("Miami", center=(STATION_MIAMI_X, TRACK_Y - 70), fontsize=28, color="Dark Blue")
    # info text upper left
    if target_station == Destination.NYC:
        destination = "New York City"
    else:
        destination = "Miami"

    dist_from_nyc = (train_x - STATION_NYC_X) * MILES_PER_PIXEL
    dist_from_miami = (STATION_MIAMI_X - train_x) * MILES_PER_PIXEL

    screen.draw.text(f"Train to {destination}", topleft=(20, 20), fontsize=24, color="Black")
    screen.draw.text(f"Distance from New York City {dist_from_nyc:.0f}", topleft=(20, 50), fontsize=24, color="Black")
    screen.draw.text(f"Distance from Miami {dist_from_miami:.0f}", topleft=(20, 80), fontsize=24, color="Black")
    screen.draw.text(f"Speed: {train_speed * MPH_SCALE:.0f} MPH", topleft=(20, 110), fontsize=24, color="Black")

    # Draw train
    draw_train(train_x, TRACK_Y)


def update():
    global train_x, target_station, train_speed, state

    # calculate stopping distance: d = v ^ 2/(2*a)
    stopping_distance = (train_speed ** 2) / (2 * ACCELERATION)

    if target_station == Destination.MIAMI:
        if state == State.ACCELERATING:
            # calculate the new train speed
            train_speed = train_speed + ACCELERATION
            if train_speed >= MAX_SPEED:
                train_speed = MAX_SPEED
                state = State.CRUISING

        # calculate the new train position
        train_x = train_x + train_speed
        distance_to_target = STATION_MIAMI_X - train_x

        # start decelerating when we need to
        if (distance_to_target <= stopping_distance and
                state in (State.ACCELERATING, State.CRUISING)):
            state = State.DECELERATING

        if state == State.DECELERATING:
            train_speed = train_speed - ACCELERATION
            if train_speed <= 0 or train_x >= STATION_MIAMI_X:
                state = State.STOPPED
                train_speed = 0
                train_x = STATION_MIAMI_X
                target_station = Destination.NYC

    else:  # going to New York City
        target_station = Destination.NYC
        train_speed = 0
        state = State.STOPPED


# respond to mouse clicks
def on_mouse_down(pos):
    global state
    if not button.collidepoint(pos):
        return

    match state:
        case State.STOPPED:
            state = State.ACCELERATING


pgzrun.go()