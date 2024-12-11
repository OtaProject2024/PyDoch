import time

from ._gpioutils import Channel


# Controlling servo motor
class SVMotor:
    def __init__(self, ch=18, freq=50, ang=60):
        self.__ch = Channel(ch)
        self.__ch.set_pwm(freq, 0)

        self.__angle = ang

    # Convert angle to duty ratio
    def __convert_angle(self, angle):
        d = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        self.__ch.set_duty(d)

    def start(self):
        self.__convert_angle(self.__angle)

    def run(self, state=0):
        match state:
            case 0:
                time.sleep(2)
            case 1:
                self.__convert_angle(self.__angle)
                time.sleep(0.5)
                self.__convert_angle(self.__angle * -1)
                time.sleep(0.5)
            case 2:
                self.__convert_angle(self.__angle)
                time.sleep(3)
            case 3:
                self.__convert_angle(self.__angle * -1)
                time.sleep(3)

    def stop(self):
        self.__ch.end()
