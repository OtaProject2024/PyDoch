import threading
import time
import RPi.GPIO as GPIO

class Led:
    def __init__(self, pin=18, wait=3):
        self.pin = pin
        self.wait = wait

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def run(self):
        print(f'pin:{self.pin} start')
        for i in range(5):
            GPIO.output(self.pin, True)
            time.sleep(self.wait)
            GPIO.output(self.pin, False)
            time.sleep(2)

        GPIO.cleanup(self.pin)
        print(f'pin:{self.pin} finish')



def start(pin, wait):
    a = Led(pin, wait)
    a.run()

if __name__ == '__main__':
    t1 = threading.Thread(target=start, args=(17, 2))
    t2 = threading.Thread(target=start, args=(18, 4))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
