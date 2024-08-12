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

    def run(self):
        self.__angle(self.angle)
        time.sleep(0.5)
        self.__angle(self.angle * -1)
        time.sleep(0.5)

    def stop(self):
        self.ch.end()

    def Right(self): #Turn to the right. (When it touches a wall or something)
        self.__angle(self.angle)
        time.sleep(4)
    
    def left(self): #Turn to the left. (When it touches a wall or something)
        self.__angle(self.angle * -1)
        time.sleep(4)

#runメソッドで引数を受け取るのはどうしようか悩み中です
#とりあえず下二つのRightとleftだけ追加
#加速度センサで壁当たったのが感知できそうならこの二つはそのまま使えるのかな