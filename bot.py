# IMPORTS
import pygame
pygame.init()

import sys


# VARIABLES + SETUP
(width, height) = (1470, 956) #currently set to my mac aspect ratio
background_colour = (31, 32, 33)

# set screen size
screen = pygame.display.set_mode((width, height)) # test if it can be resized to fit different screen sizes
# current_screen = pygame.display.get_desktop_sizes()
# print(current_screen)

# ENABLE WHEN CODING ON MAC
# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# test if it can be resized to fit different screen sizes
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# create a 'fake screen' to resize elements (source: https://stackoverflow.com/a/34919705)
temp_screen = screen.copy()

# set window name
pygame.display.set_caption('robots.txt')

#set background colour
temp_screen.fill(background_colour)

# set fonts
title_font = pygame.font.Font('assets/ari.ttf', 85)
body_font = pygame.font.Font('assets/roboto.ttf', 35)

# ·················•·················• ★ •·················•·················

# add title text
def display_title(title, font, text_colour, y):
    text = font.render(title, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

title, title_rect = display_title('I THINK YOU MEANT TO SAY...', body_font, (255, 255, 255), 75)
temp_screen.blit(title, title_rect)

# ·················•·················• ★ •·················•·················

# keep screen on screen forever by creating an infinite loop
# until you close the window

active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)


        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()