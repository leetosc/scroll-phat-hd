#!/usr/bin/env python

import random
import time

import scrollphathd

YSIZE = 7
XSIZE = 17
BRIGHT = 0.3
SPEED = 3
MAX_ITERATIONS = 100
STAGNATION_MAX = 10
INITIAL_CELLS = 100
INITIAL_SLEEP = 20


def generatemap(matrix, get_config):
    for y in range(-1, YSIZE + 1):
        for x in range(-1, XSIZE + 1):
            matrix[y, x] = 0

    for _ in range(get_config("INITIAL_CELLS", INITIAL_CELLS)):
        y = random.randint(0, YSIZE - 1)
        x = random.randint(0, XSIZE - 1)
        matrix[y, x] = 1


def printmap(matrix, sleeptime, get_config, stop_event):
    bright = get_config("BRIGHT", BRIGHT)
    alive_counter = 0
    scrollphathd.clear()

    for y in range(0, YSIZE):
        for x in range(0, XSIZE):
            if matrix[y, x]:
                scrollphathd.set_pixel(x, y, bright)
                alive_counter += 1
            else:
                scrollphathd.set_pixel(x, y, 0)

    scrollphathd.show()
    if stop_event is not None and stop_event.is_set():
        return alive_counter
    time.sleep(sleeptime / 10)
    scrollphathd.clear()

    return alive_counter


def lifecycle(matrix):
    soonmatrix = {key: value for key, value in matrix.items()}
    for y in range(YSIZE):
        for x in range(XSIZE):
            neighbors = countneighbors(py=y, px=x, status=matrix[y, x], matrix=matrix)
            if matrix[y, x]:
                soonmatrix[y, x] = 1 if 1 < neighbors < 4 else 0
            else:
                soonmatrix[y, x] = 1 if neighbors == 3 else 0

    matrix.update(soonmatrix)


def countneighbors(py, px, status, matrix):
    neighbors = -1 if status else 0
    for y in range(py - 1, py + 2):
        for x in range(px - 1, px + 2):
            if matrix[y, x]:
                neighbors += 1
    return neighbors


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    while stop_event is None or not stop_event.is_set():
        matrix = {}
        max_iterations = get_config("MAX_ITERATIONS", MAX_ITERATIONS)
        stagnation_max = get_config("STAGNATION_MAX", STAGNATION_MAX)
        alive_count_old = 0
        stagnation_count = 0

        generatemap(matrix, get_config)
        printmap(matrix, get_config("INITIAL_SLEEP", INITIAL_SLEEP), get_config, stop_event)

        while stop_event is None or not stop_event.is_set():
            lifecycle(matrix)
            active_count = printmap(matrix, get_config("SPEED", SPEED), get_config, stop_event)

            if alive_count_old == active_count:
                stagnation_count += 1
            alive_count_old = active_count
            max_iterations -= 1

            if stagnation_count == stagnation_max or max_iterations < 1:
                break


if __name__ == "__main__":
    print("Scroll pHAT HD: GameOfLife\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
