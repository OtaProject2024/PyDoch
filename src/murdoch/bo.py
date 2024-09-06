import time

import adafruit_bno055
import board


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self, freq, ivl, mag_threshold, acc_threshold):
        self.sensor = adafruit_bno055.BNO055_I2C(board.I2C())
        self.frequency = freq
        self.interval = ivl

        self.contact = False
        self.magnetic_magnitude = 0
        self.magnetic_threshold = mag_threshold
        self.stationary = False
        self.acceleration_magnitude = 0
        self.acceleration_threshold = acc_threshold

    # Get magnetics
    def __magnetic(self):
        return self.sensor.magnetic

    # Get magnetic magnitude
    def __magnetic_magnitude(self):
        m = []
        try:
            for i in range(self.frequency):
                magnetic = self.__magnetic()
                m.append(sum(b ** 2 for b in magnetic) ** 0.5)
                time.sleep(self.interval)
            self.magnetic_magnitude = sum(m) / len(m)
            self.contact = self.magnetic_magnitude < self.magnetic_threshold
        except TypeError:
            self.magnetic_magnitude = 0
            self.contact = False

    # Get acceleration
    def __acceleration(self):
        return self.sensor.acceleration

    # Get acceleration magnitude
    def __acceleration_magnitude(self):
        s = []
        try:
            for i in range(self.frequency):
                acceleration = self.__acceleration()
                s.append(sum(a ** 2 for a in acceleration) ** 0.5)
                time.sleep(self.interval)
            self.acceleration_magnitude = sum(s) / len(s)
            self.stationary = self.acceleration_magnitude < self.acceleration_threshold
        except TypeError:
            self.acceleration_magnitude = 0
            self.stationary = False

    def run(self):
        self.__magnetic_magnitude()
        self.__acceleration_magnitude()
        return self.contact, self.stationary, self.magnetic_magnitude, self.acceleration_magnitude
