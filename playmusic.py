
import pygame

import pygame

class MusicPlayer:
    def __init__(self, music_file):
    
        pygame.init()
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(music_file)

    def play(self):
        self.sound.play()
        pygame.time.delay(int(self.sound.get_length() * 1000))

    def stop(self):
        pygame.mixer.stop()

    def quit(self):
        pygame.quit()


