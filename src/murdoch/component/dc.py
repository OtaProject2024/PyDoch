import time

from ._gpioutils import Channel


# Controlling DC motor and driver
class DCMotor:
    def __init__(self, ch1=12, ch2=22, ch3=27, pw=100, s_pw=50, ward=0.3, freq=50):
        self.ch1 = Channel(ch1)
        self.ch2 = Channel(ch2)
        self.ch3 = Channel(ch3)

        self.power = pw
        self.save_power = s_pw
        self.ward = ward
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

    # Change speed
    def __speed(self, pw=100):
        self.ch1.set_duty(pw)

    def start(self):
        self.__forward()
        self.__speed(self.power)

    def run(self, state=0):
        if state == 0:
            self.__speed(0)
        elif state == 1:
            self.__speed(self.power)
        elif state == 2 or state == 3:
            self.__speed(self.save_power)

        time.sleep(self.ward)
        self.__backward()
        time.sleep(self.ward)
        self.__forward()

    def stop(self):
        self.ch1.end()
        self.ch2.end()
        self.ch3.end()
