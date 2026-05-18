#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x7

DISPLAY_BRIGHTNESS = 0.5
ROTATE_DEGREES = 90
INITIAL_DELAY = 0.5
LOOP_SLEEP = 0.05
LINE1 = "Hello World! "
LINE2 = "How are you? "


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.rotate(degrees=get_config("ROTATE_DEGREES", ROTATE_DEGREES))
    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))

    scrollphathd.write_string(get_config("LINE1", LINE1), x=0, y=0, font=font5x7)
    scrollphathd.write_string(get_config("LINE2", LINE2), x=0, y=8, font=font5x7)
    scrollphathd.show()

    time.sleep(get_config("INITIAL_DELAY", INITIAL_DELAY))

    while stop_event is None or not stop_event.is_set():
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Sideways\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
