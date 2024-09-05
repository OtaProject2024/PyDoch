import time
import RPi.GPIO as GPIO


class SBMotor:
    def __init__(self, pin=18, freq=50):
        self.pin = pin
        self.frequency = freq
        self.__begin()

    def __begin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)

    def __end(self):
        self.pwm.stop()
        GPIO.cleanup(self.pin)

    def __servo_angle(self, angle):
        duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1.0)

    def run(self, angle):
        self.pwm.start(0)
        time.sleep(1.0)
        for i in range(5):
            self.__servo_angle(angle)
            self.__servo_angle(angle * -1)

        self.__end()


if __name__ == '__main__':
    a = SBMotor()
    a.run(90)
