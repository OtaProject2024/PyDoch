import time

from ._gpioutils import Channel


# Controlling button
class Button:
    def __init__(self, ch=24, dly=1.0):
        self.__ch = Channel(ch, io=True, pull=True)

        self.__delay = dly
        self.__state = False

    def run(self):
        time.sleep(self.__delay)
        self.__ch.wait()
        self.__state = not self.__state
        return self.__state

    def stop(self):
        self.__ch.end()
