import time

from ._gpioutils import Channel


# Controlling button
class Button:
    def __init__(self, ch=24, dly=1.0, st=False):
        self.__ch = Channel(ch, io=True, pull=True)

        self.__delay = dly
        self.__state = st
        self.__input = False

    def run(self):
        if self.__input:
            time.sleep(self.__delay)
            self.__input = False
        if self.__ch.input():
            self.__state = not self.__state
            self.__input = True
        return self.__state

    def stop(self):
        self.__ch.end()
