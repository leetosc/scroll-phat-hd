#!/usr/bin/env python

import time

import scrollphathd
from mode_config import sync_scrolling_text

TEXT = " Hello World!"
TEXT_BRIGHTNESS = 0.5
LOOP_SLEEP = 0.1


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    cache = {}
    while stop_event is None or not stop_event.is_set():
        sync_scrolling_text(
            get_config, cache, "TEXT", TEXT, "TEXT_BRIGHTNESS", TEXT_BRIGHTNESS
        )
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Hello World\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
