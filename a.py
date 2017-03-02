import sys
import pygame
pygame.init()

mov_name = "video.mpg"
pygame.mouse.set_visible(False)
pygame.mixer.quit()
screen = pygame.display.set_mode((320, 240))
video = pygame.movie.Movie(mov_name)
screen = pygame.display.set_mode(video.get_size())
video.play()

while video.get_busy():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

