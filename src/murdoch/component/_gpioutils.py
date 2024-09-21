import RPi.GPIO as GPIO


# Controlling GPIO channel
class Channel:
    # Activate channel
    def __init__(self, ch=12, io=False, pull=False):
        self.channel = ch
        self.pwm = None

        if io:
            if pull:
                GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.channel, GPIO.IN)
        else:
            if pull:
                GPIO.setup(self.channel, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.channel, GPIO.OUT)

    # Return string
    def __str__(self):
        return f"channel: {self.channel}"

    # Enable pwm
    def set_pwm(self, freq=50, duty=50):
        self.pwm = GPIO.PWM(self.channel, freq)
        self.pwm.start(duty)

    # Change duty ratio
    def set_duty(self, duty=50):
        self.pwm.ChangeDutyCycle(duty)

    # Change voltage
    def set_volt(self, hl=True):
        if hl:
            GPIO.output(self.channel, GPIO.HIGH)
        else:
            GPIO.output(self.channel, GPIO.LOW)

    # Wait for change
    def wait(self):
        while True:
            if GPIO.input(self.channel) == 0:
                break

    # Deactivate channel
    def end(self):
        if self.pwm is not None:
            self.pwm.stop()
        GPIO.cleanup(self.channel)
