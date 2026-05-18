#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x7

from mode_config import config_tuple, sync_rotation

DISPLAY_BRIGHTNESS = 0.5
ROTATE_DEGREES = 90
INITIAL_DELAY = 0.5
LOOP_SLEEP = 0.05
LINE1 = "Hello World! "
LINE2 = "How are you? "


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    cache = {}
    delay_done = False

    while stop_event is None or not stop_event.is_set():
        sync_rotation(get_config, cache, "ROTATE_DEGREES", ROTATE_DEGREES)

        layout = config_tuple(
            get_config,
            [("LINE1", LINE1), ("LINE2", LINE2)],
        )
        if cache.get("layout") != layout:
            scrollphathd.clear()
            scrollphathd.write_string(layout[0], x=0, y=0, font=font5x7)
            scrollphathd.write_string(layout[1], x=0, y=8, font=font5x7)
            scrollphathd.show()
            cache["layout"] = layout
            delay_done = False

        if not delay_done:
            time.sleep(get_config("INITIAL_DELAY", INITIAL_DELAY))
            delay_done = True

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
