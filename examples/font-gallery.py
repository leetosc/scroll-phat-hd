#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import fontd3, fontgauntlet, fontorgan, fonthachicro

DISPLAY_BRIGHTNESS = 0.5
INITIAL_DELAY = 0.5
SCROLL_DELAY = 0.02
END_DELAY = 0.5
FONT_PAUSE = 0.5


def scroll_message(font, message, get_config, stop_event):
    scrollphathd.set_font(font)
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

    scrollphathd.set_brightness(get_config("DISPLAY_BRIGHTNESS", DISPLAY_BRIGHTNESS))

    fonts = (
        (fontd3, "THIS IS FONT D3"),
        (fontgauntlet, "THIS IS FONT GAUNTLET"),
        (fontorgan, "THIS IS FONT ORGAN"),
        (fonthachicro, "This is font Hachicro"),
    )

    while stop_event is None or not stop_event.is_set():
        for font, text in fonts:
            if stop_event is not None and stop_event.is_set():
                return
            scroll_message(font, text, get_config, stop_event)
            time.sleep(get_config("FONT_PAUSE", FONT_PAUSE))


if __name__ == "__main__":
    print("Scroll pHAT HD: Font Gallery\nPress Ctrl+C to exit.\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
