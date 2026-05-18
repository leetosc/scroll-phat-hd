#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x5

DISPLAY_BAR = False
BRIGHTNESS = 0.3
LOOP_SLEEP = 0.1
SECONDS_SCALE = 15.0


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    while stop_event is None or not stop_event.is_set():
        scrollphathd.clear()

        float_sec = (time.time() % 60) / 59.0
        seconds_progress = float_sec * get_config("SECONDS_SCALE", SECONDS_SCALE)
        brightness = get_config("BRIGHTNESS", BRIGHTNESS)

        if get_config("DISPLAY_BAR", DISPLAY_BAR):
            for y in range(15):
                current_pixel = min(seconds_progress, 1)
                scrollphathd.set_pixel(y + 1, 6, current_pixel * brightness)
                seconds_progress -= 1
                if seconds_progress <= 0:
                    break
        else:
            scrollphathd.set_pixel(int(seconds_progress), 6, brightness)

        scrollphathd.write_string(
            time.strftime("%H:%M"),
            x=0,
            y=0,
            font=font5x5,
            brightness=brightness,
        )

        if int(time.time()) % 2 == 0:
            scrollphathd.clear_rect(8, 0, 1, 5)

        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Clock\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
