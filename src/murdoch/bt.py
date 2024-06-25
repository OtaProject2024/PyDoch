from ._gpioutils import Channel


# Controlling button
class Button:
    def __init__(self, ch=15):
        self.ch = Channel(ch, io=True, pull=True)
        self.state = False

    def run(self):
        self.ch.wait()
        self.state = not self.state
        return self.state

    def stop(self):
        self.ch.end()
