import os
import time

import pygame.mixer as mixer


# Controlling sound
class Sound:
    def __init__(self, file="a.wav", val=1.0):
        mixer.init()
        self.sound = mixer.Sound(os.path.join("..", "assets", "sounds", file))
        self.sound.set_volume(val)

        self.played = False

    def run(self, state=False):
        if state:
            if not self.played:
                self.sound.play()
                time.sleep(self.sound.get_length())
            self.played = True
        else:
            self.played = False
