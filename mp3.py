import pygame, time
pygame.init()
pygame.mixer.music.load('/home/Torxed/test.mp3')
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.fadeout(5)