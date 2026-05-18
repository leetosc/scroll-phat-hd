#!/usr/bin/env python

import argparse
import random
import time

import scrollphathd

DISPLAY_BRIGHTNESS = 1
ROTATE_DEGREES = 0
PRECIP_AMOUNT = 0.7
PRECIP_BRIGHTNESS = 0.15
PRECIP_DELAY = 0.0
PRECIP_FADE = 0.05
PRECIP_INTENSITY = 1
PRECIP_LIGHTNING = 0.01
PRECIP_SAFE = 0.3

width = 0
height = 0


def generate_lightning(intensity):
    if random.random() < intensity:
        x = random.randint(0, width - 1)

        for y in range(0, height):
            if y > 1 and y < height - 1:
                branch = random.random()
                if branch < .3:
                    x -= 1
                    if x <= 0:
                        x = 0
                elif branch > .6:
                    x += 1
                    if x >= width - 1:
                        x = width - 1

            wide = [int(x - (width / 2)), int(x + (width / 2))]
            med = [int(x - (width / 4)), int(x + (width / 4))]
            small = [x - 1, x + 1]

            for val in [wide, med, small]:
                if val[0] < 0:
                    val[0] = 0
                if val[1] > width - 1:
                    val[1] = width - 1

            for flash in [[wide, .1], [med, .2], [small, .4]]:
                scrollphathd.fill(
                    flash[1],
                    x=flash[0][0],
                    y=y,
                    width=flash[0][1] - flash[0][0] + 1,
                    height=1
                )

            scrollphathd.set_pixel(x, y, brightness=1)
            scrollphathd.show()
        scrollphathd.clear()


def new_drop(pixels, values):
    cols = []
    for x in range(0, width):
        good_col = True
        for y in range(0, int(height * values['safe'])):
            if pixels[x][y] == values['brightness']:
                good_col = False
        if good_col is True:
            cols.append(x)

    if len(cols) > 0:
        random.shuffle(cols)
        cols_left = values['intensity']
        while len(cols) > 0 and cols_left > 0:
            if random.random() <= values['amount']:
                pixels[cols.pop()][0] = values['brightness'] + values['fade']
            cols_left -= 1


def fade_pixels(pixel_array, fade):
    for x in range(0, width):
        for y in range(0, height):
            if pixel_array[x][y] > 0:
                pixel_array[x][y] -= fade
                pixel_array[x][y] = round(pixel_array[x][y], 2)
            if pixel_array[x][y] < 0:
                pixel_array[x][y] = 0
    return pixel_array


def update_pixels(pixels, values):
    for x in range(0, width):
        for y in range(0, height - 1):
            if pixels[x][y] == values['brightness']:
                pixels[x][y + 1] = values['brightness'] + values['fade']

    fade_pixels(pixels, values['fade'])

    for a in range(0, len(pixels)):
        for b in range(0, len(pixels[a])):
            scrollphathd.set_pixel(a, b, pixels[a][b])

    scrollphathd.show()


def build_values(get_config):
    return {
        'amount': get_config('PRECIP_AMOUNT', PRECIP_AMOUNT),
        'brightness': get_config('PRECIP_BRIGHTNESS', PRECIP_BRIGHTNESS),
        'delay': get_config('PRECIP_DELAY', PRECIP_DELAY),
        'fade': get_config('PRECIP_FADE', PRECIP_FADE),
        'intensity': int(get_config('PRECIP_INTENSITY', PRECIP_INTENSITY)),
        'lightning': get_config('PRECIP_LIGHTNING', PRECIP_LIGHTNING),
        'safe': get_config('PRECIP_SAFE', PRECIP_SAFE),
    }


def run_display(stop_event=None, get_config=None):
    global width, height

    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    scrollphathd.set_clear_on_exit()

    width = scrollphathd.get_shape()[0]
    height = scrollphathd.get_shape()[1]
    pixels = [[0 for _ in range(height)] for _ in range(width)]
    layout_cache = {}

    while stop_event is None or not stop_event.is_set():
        rotate = int(get_config('ROTATE_DEGREES', ROTATE_DEGREES))
        if layout_cache.get('rotate') != rotate:
            scrollphathd.rotate(rotate)
            width = scrollphathd.get_shape()[0]
            height = scrollphathd.get_shape()[1]
            pixels = [[0 for _ in range(height)] for _ in range(width)]
            layout_cache['rotate'] = rotate

        values = build_values(get_config)
        if values['lightning'] > 0:
            generate_lightning(values['lightning'])
        new_drop(pixels, values)
        update_pixels(pixels, values)
        time.sleep(values['delay'])


def setup_parser():
    parser = argparse.ArgumentParser(
        description='Generate precipitation; CTRL+C to exit',
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument("-a", "--amount", type=float)
    parser.add_argument("-b", "--brightness", type=float)
    parser.add_argument("-d", "--delay", type=float)
    parser.add_argument("-f", "--fade", type=float)
    parser.add_argument("-i", "--intensity", type=int)
    parser.add_argument("-l", "--lightning", type=float)
    parser.add_argument("-r", "--rotate", default=0, choices=[0, 90, 180, 270], type=int)
    parser.add_argument("-s", "--safe", type=float)
    return parser


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()
    arguments = vars(args)

    overrides = {
        'PRECIP_AMOUNT': arguments.get('amount'),
        'PRECIP_BRIGHTNESS': arguments.get('brightness'),
        'PRECIP_DELAY': arguments.get('delay'),
        'PRECIP_FADE': arguments.get('fade'),
        'PRECIP_INTENSITY': arguments.get('intensity'),
        'PRECIP_LIGHTNING': arguments.get('lightning'),
        'PRECIP_SAFE': arguments.get('safe'),
        'ROTATE_DEGREES': arguments.get('rotate'),
    }

    def cli_get_config(key, default=None):
        val = overrides.get(key)
        if val is not None:
            return val
        return globals().get(key, default)

    try:
        run_display(get_config=cli_get_config)
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
