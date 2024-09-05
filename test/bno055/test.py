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

    def stationary(self):
        s = []
        try:
            for i in range(5):
                acceleration = self.__acceleration()
                s.append(sum(a ** 2 for a in acceleration) ** 0.5)
                time.sleep(0.1)
            magnitude = sum(s) / len(s)
            print(f"acceleration: {magnitude}")
        except TypeError:
            print("acceleration: TypeError")

    def magnet(self):
        m = []
        try:
            for i in range(5):
                magnetic = self.__magnetic()
                m.append(sum(m ** 2 for m in magnetic) ** 0.5)
                time.sleep(0.1)
            magnitude = sum(m) / len(m)
            print(f"magnetic: {magnitude}")
        except TypeError:
            print("magnetic: TypeError")


if __name__ == '__main__':
    sensor = BNO055Sensor()
    while True:
        sensor.stationary()
        sensor.magnet()
        time.sleep(1)
