import time


# Controlling BNO055Sensor
class BNO055Sensor:
    def __init__(self, freq, ivl, mag_threshold, acc_threshold):
        import adafruit_bno055
        self.adafruit_bno055 = adafruit_bno055
        import board
        self.board = board

        self.__sensor = self.adafruit_bno055.BNO055_I2C(self.board.I2C())
        self.__frequency = freq
        self.__interval = ivl

        self.__contact = False
        self.__magnetic = 0
        self.__magnetic_threshold = mag_threshold
        self.__stationary = False
        self.__acceleration = 0
        self.__acceleration_threshold = acc_threshold

    # Get magnetics
    def magnetic(self):
        return self.__sensor.magnetic

    # Get magnetic magnitude
    def __magnetic_magnitude(self):
        m = []
        try:
            for i in range(self.__frequency):
                magnetic = self.magnetic()
                m.append(sum(b ** 2 for b in magnetic) ** 0.5)
                time.sleep(self.__interval)
            self.__magnetic = sum(m) / len(m)
            self.__contact = self.__magnetic < self.__magnetic_threshold
        except TypeError:
            self.__magnetic = 0
            self.__contact = False

    # Get acceleration
    def get_acceleration(self):
        return self.__sensor.acceleration

    # Get acceleration magnitude
    def __acceleration_magnitude(self):
        s = []
        try:
            for i in range(self.__frequency):
                acceleration = self.get_acceleration()
                s.append(sum(a ** 2 for a in acceleration) ** 0.5)
                time.sleep(self.__interval)
            self.__acceleration = sum(s) / len(s)
            self.__stationary = self.__acceleration < self.__acceleration_threshold
        except TypeError:
            self.__acceleration = 0
            self.__stationary = False

    def run(self):
        self.__magnetic_magnitude()
        self.__acceleration_magnitude()
        return self.__contact, self.__stationary, self.__magnetic, self.__acceleration
