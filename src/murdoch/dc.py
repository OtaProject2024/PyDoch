import time
from ._gpioutils import Channel


# Controlling DC motor and driver
class DCMotor:
    def __init__(self, ch1=12, ch2=22, ch3=27, freq=50):
        self.ch1 = Channel(ch1)
        self.ch2 = Channel(ch2)
        self.ch3 = Channel(ch3)
        self.ch1.set_pwm(freq, 100)

    # Change to forward mode
    def __forward(self):
        self.ch2.set_volt(True)
        self.ch3.set_volt(False)

    # Change to backward mode
    def __backward(self):
        self.ch2.set_volt(False)
        self.ch3.set_volt(True)

    # Change to stop mode
    def __stop(self):
        self.ch2.set_volt(False)
        self.ch3.set_volt(False)

    # Change to brake mode
    def __brake(self):
        self.ch2.set_volt(True)
        self.ch3.set_volt(True)

    def __speed(self, pw=100):
        self.ch1.set_duty(pw)

    def run(self, wait=15):
        self.__forward()
        self.__speed(25)
        print("speed 25")
        time.sleep(wait)
        self.__speed(50)
        print("speed 50")
        time.sleep(wait)
        self.__speed(75)
        print("speed 75")
        time.sleep(wait)
        self.__speed(100)
        print("speed 100")
        time.sleep(wait)

        self.ch1.end()
        self.ch2.end()
        self.ch3.end()
