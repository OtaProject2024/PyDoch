import time

import adafruit_bno055
import board


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self):
        self.sensor = adafruit_bno055.BNO055_I2C(board.I2C())

    # Get acceleration
    def __acceleration(self):
        return self.sensor.acceleration

    # Get magnetics
    def __magnetic(self):
        return self.sensor.magnetic

    def is_stationary(self):
        acceleration = self.__acceleration()
        print(acceleration)
        try:
            magnitude = sum(a ** 2 for a in acceleration) ** 0.5
            print(f"acceleration: {magnitude}")
        except TypeError:
            print("acceleration: TypeError")

    def is_magnet_contact(self):
        magnetic = self.__magnetic()
        print(magnetic)
        try:
            magnitude = sum(m ** 2 for m in magnetic) ** 0.5
            print(f"magnetic: {magnitude}")
        except TypeError:
            print("magnetic: TypeError")


if __name__ == '__main__':
    sensor = BNO055Sensor()
    while True:
        sensor.is_stationary()
        sensor.is_magnet_contact()
        time.sleep(1)
