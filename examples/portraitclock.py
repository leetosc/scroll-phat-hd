#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x5

DISPLAY_BRIGHTNESS = 0.3
ROTATE_DEGREES = 270
LOOP_SLEEP = 0.1


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))
    scrollphathd.rotate(get_config("ROTATE_DEGREES", ROTATE_DEGREES))

    while stop_event is None or not stop_event.is_set():
        scrollphathd.clear()

        scrollphathd.write_string(time.strftime("%H"), x=0, y=0, font=font5x5)
        scrollphathd.write_string(time.strftime("%M"), x=0, y=6, font=font5x5)
        scrollphathd.write_string(time.strftime("%S"), x=0, y=12, font=font5x5)

        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Portrait Clock\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
