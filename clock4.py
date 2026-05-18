import math
import time

import scrollphathd
from scrollphathd.fonts import font5x5

print("""
Scroll pHAT HD: Clean + Fancy Clock

- HH:MM display
- Smooth breathing colon
- Bright seconds bar with moving head
- Small sparkle row for extra life

Press Ctrl+C to exit!
""")

TEXT_BRIGHTNESS = 0.73
BAR_BRIGHTNESS = 0.30
HEAD_BRIGHTNESS = 0.80
SPARKLE_BRIGHTNESS = 0.18

COLON_MIN_BRIGHTNESS = 0.30
COLON_MAX_BRIGHTNESS = 0.55
COLON_BREATH_PERIOD = 2.2

# Uncomment if needed
# scrollphathd.rotate(180)


def colon_brightness(now):
    phase = (now / COLON_BREATH_PERIOD) * (2.0 * math.pi)
    wave = (math.sin(phase) + 1.0) / 2.0
    return COLON_MIN_BRIGHTNESS + wave * (COLON_MAX_BRIGHTNESS - COLON_MIN_BRIGHTNESS)


def draw_breathing_colon(now):
    cb = colon_brightness(now)

    # Remove the original colon drawn by write_string
    scrollphathd.clear_rect(8, 0, 1, 5)

    # Redraw it with smooth breathing brightness
    scrollphathd.set_pixel(8, 1, cb)
    scrollphathd.set_pixel(8, 3, cb)


def draw_seconds_bar(sec_fraction):
    """
    Bottom row:
    - filled bar behind
    - bright 'head' pixel at current second position
    """
    total = sec_fraction * 17.0
    head_x = min(16, int(total))

    for x in range(17):
        pixel = min(max(total - x, 0.0), 1.0)
        if pixel > 0:
            scrollphathd.set_pixel(x, 6, pixel * BAR_BRIGHTNESS)

    head_fraction = total - head_x
    scrollphathd.set_pixel(
        head_x,
        6,
        BAR_BRIGHTNESS + (HEAD_BRIGHTNESS - BAR_BRIGHTNESS) * head_fraction,
    )

    if head_x > 0:
        scrollphathd.set_pixel(head_x - 1, 6, max(0.45, BAR_BRIGHTNESS))


def draw_sparkle(seconds):
    """
    Use row 5 as a subtle separator/animation row.
    A tiny sparkle moves slowly across the display once per minute.
    """
    sparkle_x = min(16, int((seconds / 59.0) * 16))
    scrollphathd.set_pixel(sparkle_x, 5, SPARKLE_BRIGHTNESS)

    if seconds % 10 == 0 and sparkle_x < 16:
        scrollphathd.set_pixel(sparkle_x + 1, 5, SPARKLE_BRIGHTNESS * 0.6)


try:
    while True:
        now = time.time()
        local = time.localtime(now)

        hours = local.tm_hour
        minutes = local.tm_min
        seconds = local.tm_sec

        sec_fraction = (now % 60.0) / 60.0

        scrollphathd.clear()

        # Keep the original layout exactly
        scrollphathd.write_string(
            "{:02d}:{:02d}".format(hours, minutes),
            x=0,
            y=0,
            font=font5x5,
            brightness=TEXT_BRIGHTNESS,
        )

        # Replace blink with smooth breathing
        draw_breathing_colon(now)

        # draw_sparkle(seconds)
        draw_seconds_bar(sec_fraction)

        scrollphathd.show()
        time.sleep(0.05)

except KeyboardInterrupt:
    scrollphathd.clear()
    scrollphathd.show()
