import time

from ._gpioutils import Channel


# Controlling button
class Button:
    def __init__(self, ch=24, dly=1.0):
        self.ch = Channel(ch, io=True, pull=True)

        self.delay = dly
        self.state = False

    def run(self):
        time.sleep(self.delay)
        self.ch.wait()
        self.state = not self.state
        return self.state

    def stop(self):
        self.ch.end()
