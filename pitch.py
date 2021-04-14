#!/usr/bin/env python
#
# Copyright (c) 2021 by Joelle Maslak, All Rights Reserved
# See LICENSE
#

# Inspired by:
# https://github.com/aubio/aubio/issues/78

import aubio
import numpy
import os
import pyaudio
import shutil
import sys
from colors import color
from datetime import datetime

MIDRANGE_LOW = 160
MIDRANGE_HIGH = 180
SAMPLES = 1024


def main():
    stream = get_audio_stream()

    pDetection = aubio.pitch("default", 2048*2, SAMPLES, 44100)
    pDetection.set_unit("Hz")
    pDetection.set_silence(-50)

    print("READY")
    while True:

        data = stream.read(SAMPLES)
        samples = numpy.frombuffer(data, dtype=aubio.float_type)
        pitch = pDetection(samples)[0]

        # Compute the energy (volume) of the
        # current frame.
        volume = numpy.sum(samples**2)/len(samples)

        # Floor for volume
        if volume > 0.0005:

            # Celing for pitch
            if pitch > 70.0 and pitch < 500.0:
                print_sample(volume, pitch)


def print_sample(volume, pitch):
    """Prints a sample"""

    # Get the current date, chop off last 3 digits of microseconds to
    # get milliseconds
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    pstr = "{:5.0f}".format(pitch)
    outstr = dt + " " + pstr + "hz  "  # 33 chars wide
    outstrwidth = len(outstr)

    # Colorize
    if pitch < MIDRANGE_LOW:
        outstr = color(outstr, fg="black", bg="red")
    elif pitch <= MIDRANGE_HIGH:
        outstr = color(outstr, fg="black", bg="yellow")
    else:
        outstr = color(outstr, fg="green", bg="black")
    outstr = outstr + color("", fg="gray", bg="black")

    width = get_width()
    if width > (outstrwidth + 5):
        bar_space = width - (outstrwidth + 1)
        min_bar = 110
        max_bar = 260

        outbar = []
        for i in range(bar_space):
            outbar.append(" ")

        pos = find_position(pitch, min_bar, max_bar, bar_space)
        outbar[pos] = "*"

        pos = find_position(MIDRANGE_LOW, min_bar, max_bar, bar_space)
        outbar[pos] = color(outbar[pos], bg=52) + color("", bg="black")

        pos = find_position(MIDRANGE_HIGH, min_bar, max_bar, bar_space)
        outbar[pos] = color(outbar[pos], bg=22) + color("", bg="black")

        outstr = outstr + "".join(outbar)

    print(outstr)


def find_position(value, min_bar, max_bar, size):
    range_bar = max_bar - min_bar
    pos = int(((value - min_bar) / range_bar) * size) - 1
    if pos >= size:
        pos = size - 1
    if pos < 0:
        pos = 0

    return pos


def get_audio_stream():
    """Initialize the audio stream"""

    # We want to ignore stderr.
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

    audio = pyaudio.PyAudio()
    # XXX We probably should check for errors.

    # Restore stderr
    os.dup2(old_stderr, 2)
    os.close(old_stderr)

    stream = audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
    )

    return stream


def get_width():
    """Gets the screen width"""
    if sys.stdout.isatty():
        return shutil.get_terminal_size((80, 25)).columns
    else:
        return 80


if __name__ == '__main__':
    main()
