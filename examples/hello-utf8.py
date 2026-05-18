#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import scrollphathd
from scrollphathd.fonts import font5x7

try:
    from six import unichr
except ImportError:
    unichr = chr

DISPLAY_BRIGHTNESS = 0.5
TEXT_BRIGHTNESS = 0.5
LOOP_SLEEP = 0.05


def _utf8_scroll_text(get_config):
    text = [unichr(x) for x in range(256)]
    return u"{}        ".format(u"".join(text))


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    cache = {}
    while stop_event is None or not stop_event.is_set():
        brightness = get_config("TEXT_BRIGHTNESS", TEXT_BRIGHTNESS)
        key = (brightness,)
        if cache.get("scroll") != key:
            scrollphathd.clear()
            scrollphathd.write_string(
                _utf8_scroll_text(get_config),
                x=0,
                y=0,
                font=font5x7,
                brightness=brightness,
            )
            cache["scroll"] = key

        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Hello utf-8\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
