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

# set screen padding
padding = 75

# set arrays
user_inputs = [] # array that will receive user inputs
bot_inputs = ["i love", "i love bots", "i love bots so", "i love bots so much"] # array that will receive bot inputs from the text prediction model

# ·················•·················• ★ •·················•·················

# add title text
def display_title(title, font, text_colour, y):
    text = font.render(title, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

title, title_rect = display_title('I THINK YOU MEANT TO SAY...', title_font, (255, 255, 255), padding)
temp_screen.blit(title, title_rect)

# display text function
# NOTE: for now only intaking bot inputs -- have to figure out how to use this with an updating array and how to combine with the user input array
def display_text(array, font, colour, x, y, allowed_width, allowed_height):
    text_gap = 50
    for text in array:
        y = y + text_gap
        words = text.split()

        # split text into lines
        lines = []
        while len(words) > 0:

            line_words = []
            while len(words) > 0: # loop through words to form lines
                line_words.append(words.pop(0)) # pop first word
                fw, fh = font.size(' '.join(line_words + words[:1])) # add the first word back and get the size

                if fw > allowed_width:
                    break
            
            line = ' '.join(line_words) # add a line with the selected words
            line = '> ' + line
            lines.append(line)
        
        # print lines individually underneath the other
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # tx, ty is the x and y coords for the top-left of the font surface
            tx = x
            ty = y + y_offset

            # # NOTE: how do you 'move the text upwards' and bring it back when you go back up to the previous line?
            # if y_offset + fh > allowed_height:
            #     displayed_lines.pop(0) # pop first line
            #     ty -= fh

            #     font_surface = font.render(line, True, colour)
            #     temp_screen.blit(font_surface, (tx, ty))
            # else:
            font_surface = font.render(line, True, colour)
            temp_screen.blit(font_surface, (tx, ty))

            y_offset += fh # offset next line by font height, next line will be rendered underneath the current line

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


        display_text(bot_inputs, 
                  body_font, 
                  (0, 0, 0), 
                  padding, 
                  200, 
                  width - int(padding) * 2, 
                  height - int(padding) * 2
                  ) 
        
        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()