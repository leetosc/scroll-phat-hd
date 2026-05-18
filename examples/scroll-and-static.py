#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font3x5

DISPLAY_BRIGHTNESS = 0.5
TEXT = " Hello World! "
TEXT_BRIGHTNESS = 1.0
LOOP_SLEEP = 0.05


def draw_static_elements(buf):
    if int(time.time() * 2) % 2 == 0:
        for x in range(scrollphathd.DISPLAY_WIDTH):
            if x % 2 == 0:
                buf[x][0] = 1.0
                buf[x][scrollphathd.DISPLAY_HEIGHT - 1] = 1.0

        for y in range(scrollphathd.DISPLAY_HEIGHT):
            if y % 2 == 0:
                buf[0][y] = 1.0
                buf[scrollphathd.DISPLAY_WIDTH - 1][y] = 1.0

    return buf


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))
    scrollphathd.write_string(
        get_config("TEXT", TEXT),
        x=0,
        y=1,
        font=font3x5,
        brightness=get_config("TEXT_BRIGHTNESS", TEXT_BRIGHTNESS),
    )

    while stop_event is None or not stop_event.is_set():
        scrollphathd.show(before_display=draw_static_elements)
        scrollphathd.scroll()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Scroll and Static\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
