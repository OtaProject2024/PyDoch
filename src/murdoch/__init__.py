import RPi.GPIO as GPIO

# Component modules
from .bt import Button
from .dc import DCMotor
from .sv import SVMotor

# RPi.GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
