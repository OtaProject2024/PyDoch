import time
from ._gpioutils import Channel


# Controlling servo motor
class SVMotor:
    def __init__(self, ch=18, freq=50):
        self.ch = Channel(ch)
        self.ch.set_pwm(freq, 0)

    # Convert angle to duty ratio
    def __angle(self, angle):
        d = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        self.ch.set_duty(d)

    def run(self, angle=30):
        for i in range(5):
            self.__angle(angle)
            time.sleep(1.0)
            self.__angle(angle * -1)
            time.sleep(1.0)

        self.ch.end()
