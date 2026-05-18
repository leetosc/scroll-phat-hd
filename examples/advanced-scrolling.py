#!/usr/bin/env python

import time

import scrollphathd

DISPLAY_BRIGHTNESS = 0.2
REWIND = True
SCROLL_DELAY = 0.03
LINE_PAUSE_MULTIPLIER = 10
LINE_HEIGHT_PADDING = 2

LINES = [
    "In the old #BILGETANK we'll keep you in the know",
    "In the old #BILGETANK we'll fix your techie woes",
    "And we'll make things",
    "And we'll break things",
    "'til we're altogether aching",
    "Then we'll grab a cup of grog down in the old #BILGETANK",
]


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))
    rewind = get_config("REWIND", REWIND)
    delay = get_config("SCROLL_DELAY", SCROLL_DELAY)
    line_height = scrollphathd.DISPLAY_HEIGHT + get_config("LINE_HEIGHT_PADDING", LINE_HEIGHT_PADDING)

    offset_left = 0
    lengths = [0] * len(LINES)

    for line, text in enumerate(LINES):
        lengths[line] = scrollphathd.write_string(text, x=offset_left, y=line_height * line)
        offset_left += lengths[line]

    scrollphathd.set_pixel(offset_left - 1, (len(LINES) * line_height) - 1, 0)

    while stop_event is None or not stop_event.is_set():
        scrollphathd.scroll_to(0, 0)
        scrollphathd.show()

        pos_x = 0
        pos_y = 0

        for current_line, line_length in enumerate(lengths):
            if stop_event is not None and stop_event.is_set():
                return
            time.sleep(delay * get_config("LINE_PAUSE_MULTIPLIER", LINE_PAUSE_MULTIPLIER))

            for _y in range(line_length):
                if stop_event is not None and stop_event.is_set():
                    return
                scrollphathd.scroll(1, 0)
                pos_x += 1
                time.sleep(delay)
                scrollphathd.show()

            if current_line == len(LINES) - 1 and rewind:
                for _y in range(pos_y):
                    if stop_event is not None and stop_event.is_set():
                        return
                    scrollphathd.scroll(-int(pos_x / pos_y) if pos_y else 0, -1)
                    scrollphathd.show()
                    time.sleep(delay)
            else:
                for _x in range(line_height):
                    if stop_event is not None and stop_event.is_set():
                        return
                    scrollphathd.scroll(0, 1)
                    pos_y += 1
                    scrollphathd.show()
                    time.sleep(delay)


if __name__ == "__main__":
    print("Scroll pHAT HD: Advanced Scrolling\nPress Ctrl+C to exit.\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
