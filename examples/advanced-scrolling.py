#!/usr/bin/env python

import time

import scrollphathd
from mode_config import parse_lines

DISPLAY_BRIGHTNESS = 0.2
REWIND = True
SCROLL_DELAY = 0.03
LINE_PAUSE_MULTIPLIER = 10
LINE_HEIGHT_PADDING = 2

LINES = """In the old #BILGETANK we'll keep you in the know
In the old #BILGETANK we'll fix your techie woes
And we'll make things
And we'll break things
'til we're altogether aching
Then we'll grab a cup of grog down in the old #BILGETANK"""


def _default_lines():
    return parse_lines(LINES, [])


def lines_from_config(get_config):
    raw = get_config("LINES", None)
    if raw is None:
        raw = LINES
    lines = parse_lines(raw, _default_lines())
    return lines if lines else _default_lines()


def _config_version(get_config):
    return get_config.config_version() if hasattr(get_config, "config_version") else 0


def layout_snapshot(get_config):
    return (
        _config_version(get_config),
        tuple(lines_from_config(get_config)),
        get_config("REWIND", REWIND),
        get_config("SCROLL_DELAY", SCROLL_DELAY),
        scrollphathd.DISPLAY_HEIGHT + get_config("LINE_HEIGHT_PADDING", LINE_HEIGHT_PADDING),
        get_config("LINE_PAUSE_MULTIPLIER", LINE_PAUSE_MULTIPLIER),
    )


def config_changed(get_config, snapshot):
    return layout_snapshot(get_config) != snapshot


def build_scroll_buffer(lines, line_height):
    scrollphathd.clear()
    scrollphathd.scroll_to(0, 0)
    offset_left = 0
    lengths = [0] * len(lines)
    for line, text in enumerate(lines):
        lengths[line] = scrollphathd.write_string(text, x=offset_left, y=line_height * line)
        offset_left += lengths[line]
    if lines:
        scrollphathd.set_pixel(offset_left - 1, (len(lines) * line_height) - 1, 0)
    return lengths


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    while stop_event is None or not stop_event.is_set():
        snapshot = layout_snapshot(get_config)
        lines = lines_from_config(get_config)
        rewind = snapshot[2]
        delay = snapshot[3]
        line_height = snapshot[4]
        pause_mult = snapshot[5]

        lengths = build_scroll_buffer(lines, line_height)
        scrollphathd.show()

        pos_x = 0
        pos_y = 0
        aborted = False

        for current_line, line_length in enumerate(lengths):
            if stop_event is not None and stop_event.is_set():
                return
            if config_changed(get_config, snapshot):
                aborted = True
                break

            time.sleep(delay * pause_mult)

            for _y in range(line_length):
                if stop_event is not None and stop_event.is_set():
                    return
                if config_changed(get_config, snapshot):
                    aborted = True
                    break
                scrollphathd.scroll(1, 0)
                pos_x += 1
                time.sleep(delay)
                scrollphathd.show()

            if aborted:
                break

            if current_line == len(lengths) - 1 and rewind:
                for _y in range(pos_y):
                    if stop_event is not None and stop_event.is_set():
                        return
                    if config_changed(get_config, snapshot):
                        aborted = True
                        break
                    scrollphathd.scroll(-int(pos_x / pos_y) if pos_y else 0, -1)
                    scrollphathd.show()
                    time.sleep(delay)
            else:
                for _x in range(line_height):
                    if stop_event is not None and stop_event.is_set():
                        return
                    if config_changed(get_config, snapshot):
                        aborted = True
                        break
                    scrollphathd.scroll(0, 1)
                    pos_y += 1
                    scrollphathd.show()
                    time.sleep(delay)

            if aborted:
                break


if __name__ == "__main__":
    print("Scroll pHAT HD: Advanced Scrolling\nPress Ctrl+C to exit.\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
