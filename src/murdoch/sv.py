import time

from ._gpioutils import Channel


# Controlling servo motor
class SVMotor:
    def __init__(self, ch=18, freq=50):
        self.ch = Channel(ch)
        self.ch.set_pwm(freq, 0)

        self.angle = 0

    # Convert angle to duty ratio
    def __angle(self, angle):
        d = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        self.ch.set_duty(d)

    def start(self, angle=60):
        self.__angle(self.angle)
        self.angle = angle

    def run(self, state=0):
        if state == 0:
            time.sleep(2)
        elif state == 1:
            self.__angle(self.angle)
            time.sleep(0.5)
            self.__angle(self.angle * -1)
            time.sleep(0.5)
        elif state == 2:
            self.__angle(self.angle)
            time.sleep(3)
        elif state == 3:
            self.__angle(self.angle * -1)
            time.sleep(3)

    def stop(self):
        self.ch.end()
