import time
from ._gpioutils import Channel


# Controlling DC motor and driver
class DCMotor:
    def __init__(self, ch1=20, ch2=21, freq=50):
        self.ch1 = Channel(ch1)
        self.ch2 = Channel(ch2)
        self.ch1.set_pwm(freq, 0)
        self.ch2.set_pwm(freq, 0)

    # Change to forward mode
    def __forward(self, pw=100):
        self.ch1.set_duty(pw)
        self.ch2.set_duty(0)

    # Change to backward mode
    def __backward(self, pw=100):
        self.ch1.set_duty(0)
        self.ch2.set_duty(pw)

    # Change to stop mode
    def __stop(self):
        self.ch1.set_duty(0)
        self.ch2.set_duty(0)

    # Change to brake mode
    def __brake(self):
        self.ch1.set_duty(100)
        self.ch2.set_duty(100)

    def run(self, wait=15):
        self.__forward()
        time.sleep(wait)

        self.ch1.end()
        self.ch2.end()
