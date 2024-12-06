import time

from ._gpioutils import Channel


# Controlling DC motor and driver
class DCMotor:
    def __init__(self, ch1=12, ch2=22, ch3=27, pw=100, s_pw=50, dir=0.3, freq=50):
        self.__ch1 = Channel(ch1)
        self.__ch2 = Channel(ch2)
        self.__ch3 = Channel(ch3)

        self.__power = pw
        self.__save_power = s_pw
        self.__direction = dir
        self.__ch1.set_pwm(freq, 100)

    # Change to forward mode
    def __forward(self):
        self.__ch2.set_volt(True)
        self.__ch3.set_volt(False)

    # Change to backward mode
    def __backward(self):
        self.__ch2.set_volt(False)
        self.__ch3.set_volt(True)

    # Change to stop mode
    def __stop(self):
        self.__ch2.set_volt(False)
        self.__ch3.set_volt(False)

    # Change to brake mode
    def __brake(self):
        self.__ch2.set_volt(True)
        self.__ch3.set_volt(True)

    # Change speed
    def __speed(self, pw=100):
        self.__ch1.set_duty(pw)

    def start(self):
        self.__forward()
        self.__speed(self.__power)

    def run(self, state=0):
        if state == 0:
            self.__speed(0)
        elif state == 1:
            self.__speed(self.__power)
        elif state == 2 or state == 3:
            self.__speed(self.__save_power)

        time.sleep(self.__direction)
        self.__backward()
        time.sleep(self.__direction)
        self.__forward()

    def stop(self):
        self.__ch1.end()
        self.__ch2.end()
        self.__ch3.end()
