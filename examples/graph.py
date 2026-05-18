#!/usr/bin/env python

import random
import time

import scrollphathd

MIN_VALUE = 0
MAX_VALUE = 50
GRAPH_BRIGHTNESS = 0.3
LOOP_SLEEP = 0.05


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    values = [0] * scrollphathd.DISPLAY_WIDTH

    while stop_event is None or not stop_event.is_set():
        min_val = get_config("MIN_VALUE", MIN_VALUE)
        max_val = get_config("MAX_VALUE", MAX_VALUE)
        values.insert(0, random.randrange(min_val, max_val))
        values = values[:scrollphathd.DISPLAY_WIDTH]

        scrollphathd.set_graph(
            values,
            low=min_val,
            high=max_val,
            brightness=get_config("GRAPH_BRIGHTNESS", GRAPH_BRIGHTNESS),
        )

        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Graph\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
