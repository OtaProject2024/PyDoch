import RPi.GPIO as GPIO
import time

class DcMotor:
    def __init__(self, in1=20, in2=21):
        self.in1 = in1
        self.in2 = in2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

    def run(self):
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        print("初期条件")
        print_mode((GPIO.input(20), GPIO.input(21)))
        time.sleep(1)
        print("######################")

        try:
            for i in range(5):
                print("正転モード")
                GPIO.output(20, GPIO.HIGH)
                GPIO.output(21, GPIO.LOW)
                print_mode((GPIO.input(20), GPIO.input(21)))
                time.sleep(3)
                print("ストップモード")
                GPIO.output(20, GPIO.LOW)
                GPIO.output(21, GPIO.LOW)
                print_mode((GPIO.input(20), GPIO.input(21)))
                time.sleep(1)
                print("逆転モード")
                GPIO.output(20, GPIO.LOW)
                GPIO.output(21, GPIO.HIGH)
                print_mode((GPIO.input(20), GPIO.input(21)))
                time.sleep(3)
                print("ブレーキモード")
                GPIO.output(20, GPIO.HIGH)
                GPIO.output(21, GPIO.HIGH)
                print_mode((GPIO.input(20), GPIO.input(21)))
                time.sleep(2)
        except KeyboardInterrupt:
            pass

        GPIO.cleanup()
