import math
import time

import scrollphathd
from scrollphathd.fonts import font5x5

TEXT_BRIGHTNESS = 0.73
BAR_BRIGHTNESS = 0.30
HEAD_BRIGHTNESS = 0.80
SPARKLE_BRIGHTNESS = 0.18

COLON_MIN_BRIGHTNESS = 0.30
COLON_MAX_BRIGHTNESS = 0.55
COLON_BREATH_PERIOD = 2.2
LOOP_SLEEP = 0.05

# Uncomment if needed
# scrollphathd.rotate(180)


def colon_brightness(now, get_config):
    period = get_config("COLON_BREATH_PERIOD", COLON_BREATH_PERIOD)
    min_b = get_config("COLON_MIN_BRIGHTNESS", COLON_MIN_BRIGHTNESS)
    max_b = get_config("COLON_MAX_BRIGHTNESS", COLON_MAX_BRIGHTNESS)
    phase = (now / period) * (2.0 * math.pi)
    wave = (math.sin(phase) + 1.0) / 2.0
    return min_b + wave * (max_b - min_b)


def draw_breathing_colon(now, get_config):
    cb = colon_brightness(now, get_config)
    scrollphathd.clear_rect(8, 0, 1, 5)
    scrollphathd.set_pixel(8, 1, cb)
    scrollphathd.set_pixel(8, 3, cb)


def draw_seconds_bar(sec_fraction, get_config):
    bar_brightness = get_config("BAR_BRIGHTNESS", BAR_BRIGHTNESS)
    head_brightness = get_config("HEAD_BRIGHTNESS", HEAD_BRIGHTNESS)

    total = sec_fraction * 17.0
    head_x = min(16, int(total))

    for x in range(17):
        pixel = min(max(total - x, 0.0), 1.0)
        if pixel > 0:
            scrollphathd.set_pixel(x, 6, pixel * bar_brightness)

    head_fraction = min(1.0, (total - head_x) * 2.0)
    scrollphathd.set_pixel(
        head_x,
        6,
        bar_brightness + (head_brightness - bar_brightness) * head_fraction,
    )

    if head_x > 0:
        scrollphathd.set_pixel(head_x - 1, 6, max(0.45, bar_brightness))


def draw_sparkle(seconds, get_config):
    sparkle_brightness = get_config("SPARKLE_BRIGHTNESS", SPARKLE_BRIGHTNESS)
    sparkle_x = min(16, int((seconds / 59.0) * 16))
    scrollphathd.set_pixel(sparkle_x, 5, sparkle_brightness)

    if seconds % 10 == 0 and sparkle_x < 16:
        scrollphathd.set_pixel(sparkle_x + 1, 5, sparkle_brightness * 0.6)


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    while stop_event is None or not stop_event.is_set():
        now = time.time()
        local = time.localtime(now)

        hours = local.tm_hour
        minutes = local.tm_min
        seconds = local.tm_sec
        sec_fraction = (now % 60.0) / 60.0

        scrollphathd.clear()

        scrollphathd.write_string(
            "{:02d}:{:02d}".format(hours, minutes),
            x=0,
            y=0,
            font=font5x5,
            brightness=get_config("TEXT_BRIGHTNESS", TEXT_BRIGHTNESS),
        )

        draw_breathing_colon(now, get_config)
        draw_seconds_bar(sec_fraction, get_config)

        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("""
Scroll pHAT HD: Clean + Fancy Clock

Press Ctrl+C to exit!
""")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
