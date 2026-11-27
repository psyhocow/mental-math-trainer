import pygame

pygame.mixer.init()

def play_sound(type):
    if type == 'right': 
        pygame.mixer.music.load('right.mp3')
        pygame.mixer.music.play(loops=0)
    elif type == 'wrong': 
        pygame.mixer.music.load('wrong.mp3')
        pygame.mixer.music.play(loops=0)