import RPi.GPIO as GPIO


# Controlling GPIO channel
class Channel:
    # Activate channel
    def __init__(self, ch=12, io=False, pull=False):
        self.__channel = ch
        self.__pwm = None

        if io:
            if pull:
                GPIO.setup(self.__channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.__channel, GPIO.IN)
        else:
            if pull:
                GPIO.setup(self.__channel, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.__channel, GPIO.OUT)

    # Return string
    def __str__(self):
        return f"channel: {self.__channel}"

    # Enable pwm
    def set_pwm(self, freq=50, duty=50):
        self.__pwm = GPIO.PWM(self.__channel, freq)
        self.__pwm.start(duty)

    # Change duty ratio
    def set_duty(self, duty=50):
        self.__pwm.ChangeDutyCycle(duty)

    # Change voltage
    def set_volt(self, hl=True):
        if hl:
            GPIO.output(self.__channel, GPIO.HIGH)
        else:
            GPIO.output(self.__channel, GPIO.LOW)

    # Input monitoring
    def input(self):
        if GPIO.input(self.__channel) == 0:
            return True
        elif GPIO.input(self.__channel) == 1:
            return False

    # Deactivate channel
    def end(self):
        if self.__pwm is not None:
            self.__pwm.stop()
        GPIO.cleanup(self.__channel)
