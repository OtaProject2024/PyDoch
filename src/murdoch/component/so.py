import os
import time
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame.mixer as mixer


# Controlling sound
class Sound:
    def __init__(self, file="a.wav", val=1.0):
        mixer.init()
        self.__sound = mixer.Sound(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "assets",
                "sounds",
                file
            )
        )
        self.__sound.set_volume(val)
        self.__played = False

    def run(self, state=False):
        if state:
            if not self.__played:
                self.__sound.play()
                time.sleep(self.__sound.get_length())
            self.__played = True
        else:
            self.__played = False
