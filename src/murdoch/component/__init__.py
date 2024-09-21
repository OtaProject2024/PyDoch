import RPi.GPIO as GPIO

# Components
from .bt import Button
from .bo import BNO055Sensor
from .dc import DCMotor
from .sv import SVMotor
from .so import Sound

# RPi.GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
