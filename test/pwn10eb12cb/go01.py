import time
import RPi.GPIO as GPIO


class DCMotor:
    def __init__(self, pin1=20, pin2=21):
        self.pin1 = pin1
        self.pin2 = pin2
        self.__begin()

    def __begin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

    def __end(self):
        GPIO.cleanup((self.pin1, self.pin2))

    def __forward(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)

    def __backward(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)

    def __stop(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)

    def __brake(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.HIGH)

    def run(self, wait=15):
        self.__forward()
        time.sleep(wait)

        self.__end()


if __name__ == '__main__':
    a = DCMotor()
    a.run(30)
