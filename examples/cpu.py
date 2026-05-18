#!/usr/bin/env python

import sys
import time

try:
    import psutil
except ImportError:
    psutil = None

import scrollphathd

GRAPH_LOW = 0
GRAPH_HIGH = 25
GRAPH_BRIGHTNESS = 0.25
LOOP_SLEEP = 0.2


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    if psutil is None:
        raise ImportError(
            "This script requires the psutil module\nInstall with: sudo pip install psutil"
        )

    cpu_values = [0] * scrollphathd.DISPLAY_WIDTH

    while stop_event is None or not stop_event.is_set():
        cpu_values.pop(0)
        cpu_values.append(psutil.cpu_percent())

        scrollphathd.set_graph(
            cpu_values,
            low=get_config("GRAPH_LOW", GRAPH_LOW),
            high=get_config("GRAPH_HIGH", GRAPH_HIGH),
            brightness=get_config("GRAPH_BRIGHTNESS", GRAPH_BRIGHTNESS),
        )

        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: CPU\nPress Ctrl+C to exit!\n")
    if psutil is None:
        sys.exit("This script requires the psutil module\nInstall with: sudo pip install psutil")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
