#!/usr/bin/env python

import random
import time

import scrollphathd

DISPLAY_BRIGHTNESS = 0.5
INITIAL_TREES = 0.55
TREE_GROW_PROB = 0.01
FIRE_PROB = 0.001
TREE_BRIGHTNESS = 0.3
BURNING_BRIGHTNESS = 0.9
SPACE_BRIGHTNESS = 0.0
LOOP_SLEEP = 0.05

HOOD = ((-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1))


def initialise(width, height, get_config):
    tree = get_config("TREE_BRIGHTNESS", TREE_BRIGHTNESS)
    space = get_config("SPACE_BRIGHTNESS", SPACE_BRIGHTNESS)
    initial = get_config("INITIAL_TREES", INITIAL_TREES)
    return {
        (x, y): (tree if random.random() <= initial else space)
        for x in range(width) for y in range(height)
    }


def show_grid(grid, width, height):
    scrollphathd.clear()
    for x in range(width):
        for y in range(height):
            scrollphathd.set_pixel(x, y, grid[(x, y)])
    scrollphathd.show()


def update_grid(grid, width, height, get_config):
    tree = get_config("TREE_BRIGHTNESS", TREE_BRIGHTNESS)
    burning = get_config("BURNING_BRIGHTNESS", BURNING_BRIGHTNESS)
    space = get_config("SPACE_BRIGHTNESS", SPACE_BRIGHTNESS)
    p = get_config("TREE_GROW_PROB", TREE_GROW_PROB)
    f = get_config("FIRE_PROB", FIRE_PROB)

    new_grid = {}
    for x in range(width):
        for y in range(height):
            if grid[(x, y)] == burning:
                new_grid[(x, y)] = space
            elif grid[(x, y)] == space:
                new_grid[(x, y)] = tree if random.random() <= p else space
            elif grid[(x, y)] == tree:
                neighbor_burning = any(
                    grid.get((x + dx, y + dy), space) == burning
                    for dx, dy in HOOD
                )
                new_grid[(x, y)] = burning if neighbor_burning or random.random() <= f else tree
    return new_grid


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))
    width = scrollphathd.width
    height = scrollphathd.height
    grid = initialise(width, height, get_config)

    while stop_event is None or not stop_event.is_set():
        show_grid(grid, width, height)
        grid = update_grid(grid, width, height, get_config)
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Forest Fire\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
