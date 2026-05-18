#!/usr/bin/env python

import math
import time

import scrollphathd

DISPLAY_BRIGHTNESS = 0.8
TIME_DIVISOR = 18.0
TIME_AMPLITUDE = 1500.0
STEP_DIVISOR = 10.0
DIST_DIVISOR = 1.5
RADIUS_DIVISOR = 8.0
MAX_BRIGHTNESS = 0.7
LOOP_SLEEP = 0.001


def swirl(x, y, step, get_config):
    x -= (scrollphathd.DISPLAY_WIDTH / 2.0)
    y -= (scrollphathd.DISPLAY_HEIGHT / 2.0)

    dist = math.sqrt(pow(x, 2) + pow(y, 2))
    angle = (step / get_config("STEP_DIVISOR", STEP_DIVISOR)) + dist / get_config("DIST_DIVISOR", DIST_DIVISOR)

    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    r = abs(xs + ys)
    max_b = get_config("MAX_BRIGHTNESS", MAX_BRIGHTNESS)
    return max(0.0, max_b - min(1.0, r / get_config("RADIUS_DIVISOR", RADIUS_DIVISOR)))


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))

    while stop_event is None or not stop_event.is_set():
        timestep = math.sin(time.time() / get_config("TIME_DIVISOR", TIME_DIVISOR)) * get_config("TIME_AMPLITUDE", TIME_AMPLITUDE)

        for x in range(0, scrollphathd.DISPLAY_WIDTH):
            for y in range(0, scrollphathd.DISPLAY_HEIGHT):
                v = swirl(x, y, timestep, get_config)
                scrollphathd.pixel(x, y, v)

        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))
        scrollphathd.show()


if __name__ == "__main__":
    print("Scroll pHAT HD: Swirl\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
