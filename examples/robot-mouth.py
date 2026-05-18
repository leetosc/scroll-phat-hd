#!/usr/bin/env python

import os
import time
from sys import exit

try:
    from PIL import Image
except ImportError:
    Image = None

import scrollphathd

IMAGE_BRIGHTNESS = 0.5
LOOP_SLEEP = 0.03
IMAGE_FILE = "mouth.bmp"


def get_pixel(img, x, y):
    p = img.getpixel((x, y))

    if img.getpalette() is not None:
        r, g, b = img.getpalette()[p:p + 3]
        p = max(r, g, b)

    return p / 255.0


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    if Image is None:
        raise ImportError(
            "This script requires the pillow module\nInstall with: sudo pip install pillow"
        )

    image_file = get_config("IMAGE_FILE", IMAGE_FILE)
    if not os.path.isabs(image_file):
        image_file = os.path.join(os.path.dirname(__file__), image_file)

    img = Image.open(image_file)
    image_brightness = get_config("IMAGE_BRIGHTNESS", IMAGE_BRIGHTNESS)

    for x in range(0, scrollphathd.DISPLAY_WIDTH):
        for y in range(0, scrollphathd.DISPLAY_HEIGHT):
            brightness = get_pixel(img, x, y)
            scrollphathd.pixel(x, 6 - y, brightness * image_brightness)

    while stop_event is None or not stop_event.is_set():
        scrollphathd.show()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))
        scrollphathd.scroll(-1)


if __name__ == "__main__":
    print("Scroll pHAT HD: Robot Mouth\nPress Ctrl+C to exit!\n")
    if Image is None:
        exit("This script requires the pillow module\nInstall with: sudo pip install pillow")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
