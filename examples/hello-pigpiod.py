#!/usr/bin/env python

import time

import scrollphathd
from mode_config import sync_scrolling_text

TEXT = " Hello World!"
TEXT_BRIGHTNESS = 0.5
LOOP_SLEEP = 0.1


class I2C_PIGPIO(object):
    def __init__(self, pigpio_module):
        self.pi = pigpio_module.pi()
        self.i2c_handle = self.pi.i2c_open(1, 0x74)

    def write_byte_data(self, address, register, value):
        self.pi.i2c_write_byte_data(self.i2c_handle, register, value)

    def read_byte_data(self, address, register):
        return self.pi.i2c_read_byte_data(self.i2c_handle, register)

    def write_i2c_block_data(self, address, register, values):
        self.pi.i2c_write_i2c_block_data(self.i2c_handle, register, values)


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    try:
        import pigpio
    except ImportError:
        raise ImportError("This script requires pigpiod and the pigpio module")

    scrollphathd.setup(i2c_dev=I2C_PIGPIO(pigpio))
    cache = {}
    while stop_event is None or not stop_event.is_set():
        sync_scrolling_text(
            get_config, cache, "TEXT", TEXT, "TEXT_BRIGHTNESS", TEXT_BRIGHTNESS
        )
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(get_config("LOOP_SLEEP", LOOP_SLEEP))


if __name__ == "__main__":
    print("Scroll pHAT HD: Hello World (pigpio)\nPress Ctrl+C to exit!\n")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
