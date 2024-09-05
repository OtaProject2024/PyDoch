import time

import adafruit_bno055
import board


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self, freq, acc_threshold, mag_threshold):
        self.frequency = freq
        self.acceleration_threshold = acc_threshold
        self.magnetic_threshold = mag_threshold

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
            for i in range(self.frequency):
                acceleration = self.__acceleration()
                s.append(sum(a ** 2 for a in acceleration) ** 0.5)
                time.sleep(0.1)
            magnitude = sum(s) / len(s)
            return magnitude < self.acceleration_threshold, magnitude
        except TypeError:
            return False, 0

    def magnet(self):
        m = []
        try:
            for i in range(self.frequency):
                magnetic = self.__magnetic()
                m.append(sum(b ** 2 for b in magnetic) ** 0.5)
                time.sleep(0.1)
            magnitude = sum(m) / len(m)
            return magnitude > self.magnetic_threshold, magnitude
        except TypeError:
            return False, 0
