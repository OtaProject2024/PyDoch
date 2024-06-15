import RPi.GPIO as GPIO


# Controlling GPIO channel
class Channel:
    # Activate channel
    def __init__(self, ch=12, io=False):
        self.channel = ch
        self.pwm = None

        if io:
            GPIO.setup(self.channel, GPIO.IN)
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

    # Deactivate channel
    def end(self):
        if self.pwm is not None:
            self.pwm.stop()
        GPIO.cleanup(self.channel)
