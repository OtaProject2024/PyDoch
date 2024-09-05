import adafruit_bno055
import board
import time


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self):
        self.sensor = adafruit_bno055.BNO055(board.I2C())
        self.sensor.mode = adafruit_bno055.MODE_ACCEL_MAG

    # Get acceleration
    def __acceleration(self):
        return self.sensor.acceleration

    # Get magnetics
    def __magnetic(self):
        return self.sensor.magnetic

    def is_stationary(self):
        acceleration = self.__acceleration()
        magnitude = sum(a ** 2 for a in acceleration) ** 0.5
        print(magnitude)

    def is_magnet_contact(self):
        magnetic = self.__magnetic()
        magnitude = sum(m ** 2 for m in magnetic) ** 0.5
        print(magnitude)

if __name__ == '__main__':
    sensor = BNO055Sensor()
    while True:
        sensor.is_stationary()
        sensor.is_magnet_contact()
        time.sleep(1)
