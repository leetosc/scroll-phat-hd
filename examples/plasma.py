#!/usr/bin/env python

import math
import time

import scrollphathd

BRIGHTNESS_BASE = 0.3
BRIGHTNESS_AMP = 0.3
FRAME_STEP = 2
SINE_DIVISOR = 50.0
WAVE_SCALE = 2.0
WAVE_OFFSET = 6.0
PHASE_DIVISOR = 4.0
LOOP_SLEEP = 0.01


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    i = 0
    while stop_event is None or not stop_event.is_set():
        i += get_config("FRAME_STEP", FRAME_STEP)
        s = math.sin(i / get_config("SINE_DIVISOR", SINE_DIVISOR)) * get_config("WAVE_SCALE", WAVE_SCALE) + get_config("WAVE_OFFSET", WAVE_OFFSET)
        base = get_config("BRIGHTNESS_BASE", BRIGHTNESS_BASE)
        amp = get_config("BRIGHTNESS_AMP", BRIGHTNESS_AMP)
        phase_div = get_config("PHASE_DIVISOR", PHASE_DIVISOR)

        for x in range(0, 17):
            for y in range(0, 7):
                v = base + (amp * math.sin((x * s) + i / phase_div) * math.cos((y * s) + i / phase_div))
                scrollphathd.pixel(x, y, max(0.0, min(1.0, v)))

        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))
        scrollphathd.show()


if __name__ == "__main__":
    print("Scroll pHAT HD: Plasma\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
