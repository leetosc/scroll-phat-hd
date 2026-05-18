#!/usr/bin/env python

import time

try:
    import numpy
except ImportError:
    numpy = None

import scrollphathd
from mode_config import parse_int_list

DISPLAY_BRIGHTNESS = 0.1
MAX_STEPS = 100
SPEED = 10
STEP_SLEEP = 0.01

FIRST_ROW = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    if numpy is None:
        raise ImportError(
            "This script requires the numpy module\nInstall with: sudo pip install numpy"
        )

    scrollphathd.clear()

    rules = numpy.array([22, 30, 54, 60, 75, 90, 110, 150])
    rule = rules[0]
    loop_count = 0
    matrix = numpy.zeros((7, 17), dtype=numpy.int)
    matrix[0] = parse_int_list(get_config("FIRST_ROW", FIRST_ROW), FIRST_ROW)
    row = 0

    while stop_event is None or not stop_event.is_set():
        max_steps = get_config("MAX_STEPS", MAX_STEPS)

        for y in range(0, 7):
            for x in range(0, 17):
                scrollphathd.pixel(x, y, matrix[y, x])

        scrollphathd.show()
        loop_count += 1

        if loop_count > max_steps:
            loop_count = 0
            row = 0
            matrix = numpy.zeros((7, 17), dtype=numpy.int)
            matrix[0] = parse_int_list(get_config("FIRST_ROW", FIRST_ROW), FIRST_ROW)
            rules = numpy.roll(rules, -1, axis=0)
            rule = rules[0]

        input_row = matrix[row]
        output_row = numpy.zeros((17), dtype=numpy.int)

        for x in range(0, 17):
            a = input_row[x - 1] if x > 0 else input_row[16]
            b = input_row[x]
            c = input_row[x + 1] if x < 16 else input_row[0]
            o = 1 << ((a << 2) + (b << 1) + c)
            output_row[x] = 1 if o & rule else 0

        if row < 6:
            row = row + 1
        else:
            matrix = numpy.roll(matrix, -1, axis=0)

        matrix[row] = output_row
        speed = get_config("SPEED", SPEED)
        time.sleep(get_config("STEP_SLEEP", STEP_SLEEP) * speed)


if __name__ == "__main__":
    print("Scroll pHAT HD: Cellular Automata\nPress Ctrl+C to exit!\n")
    if numpy is None:
        import sys
        sys.exit("This script requires the numpy module\nInstall with: sudo pip install numpy")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
