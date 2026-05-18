#!/usr/bin/env python

import time

import scrollphathd

MESSAGE = "Hello World! How are you today?"
INITIAL_DELAY = 0.5
SCROLL_DELAY = 0.02
END_DELAY = 0.5


def scroll_message(message, get_config, stop_event):
    scrollphathd.clear()
    length = scrollphathd.write_string(message)
    scrollphathd.show()
    time.sleep(get_config("INITIAL_DELAY", INITIAL_DELAY))

    length -= scrollphathd.width

    while length > 0:
        if stop_event is not None and stop_event.is_set():
            return
        scrollphathd.scroll(1)
        scrollphathd.show()
        length -= 1
        time.sleep(get_config("SCROLL_DELAY", SCROLL_DELAY))

    time.sleep(get_config("END_DELAY", END_DELAY))


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    while stop_event is None or not stop_event.is_set():
        scroll_message(get_config("MESSAGE", MESSAGE), get_config, stop_event)


if __name__ == "__main__":
    print("Scroll pHAT HD: Simple Scrolling\nPress Ctrl+C to exit.\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
