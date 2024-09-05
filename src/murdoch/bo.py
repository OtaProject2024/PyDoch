import adafruit_bno055
import board


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self, acc_threshold, mag_threshold):
        self.acceleration_threshold = acc_threshold
        self.magnetic_threshold = mag_threshold

        self.sensor = adafruit_bno055.BNO055_I2C(board.I2C())

    # Get acceleration
    def __acceleration(self):
        return self.sensor.acceleration

    # Get magnetics
    def __magnetic(self):
        return self.sensor.magnetic

    def is_stationary(self):
        acceleration = self.__acceleration()
        magnitude = sum(a ** 2 for a in acceleration) ** 0.5
        return magnitude < self.acceleration_threshold, magnitude

    def is_magnet_contact(self):
        magnetic = self.__magnetic()
        magnitude = sum(m ** 2 for m in magnetic) ** 0.5
        return magnitude > self.magnetic_threshold, magnitude
