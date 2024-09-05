import RPi.GPIO as GPIO
import time

class SBMotor:
    def __init__(self):
        self.servo = 18
        self.frequency = 50

    def Metro(self):
        #好みの角度で止まる120刻みのメトロノーム
        angle1 = input('角度を入力してください>>>')
        angle1 = int(angle1)
        pulse_width = ((angle1 / 180) * (2500 - 500) + 500)/100
        angle_1 = pulse_width / 20 * 100 

        angle2 = input('角度を入力してください>>>')
        angle2 = int(angle2)
        pulse_width = ((angle2 / 180) * (2500 - 500) + 500)/100
        angle_2 = pulse_width / 20 * 100  

        count = input('何分行いますか>>>')
        count = int(count)*60

        angle_0 = 2.5 / 20 * 100  #duty: 12.5%

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo, GPIO.OUT)

        pwm = GPIO.PWM(self.servo, self.frequency)

        pwm.start(angle_0)
        time.sleep(1)

        for i in range(count):
            pwm.ChangeDutyCycle(angle_1)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(angle_2)
            time.sleep(0.5)

        pwm.stop()
        GPIO.cleanup()
