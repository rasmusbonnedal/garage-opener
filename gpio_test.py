#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep  # Import sleep Module for timing

GPIO.setmode(GPIO.BCM)  # Configures how we are describing our pin numbering
GPIO.setwarnings(False)  # Disable Warnings

pin = 22
GPIO.setup(pin, GPIO.OUT)

sleep(5)
GPIO.output(pin, True)
sleep(1)
GPIO.output(pin, False)
