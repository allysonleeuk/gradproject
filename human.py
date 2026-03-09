# IMPORTS
import pygame
pygame.init()

import sys


# VARIABLES
(width, height) = (1470, 956) #currently set to my mac aspect ratio
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/tartan.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))


# SETUP

# set screen size
screen = pygame.display.set_mode((width, height)) # test if it can be resized to fit different screen sizes
# screen = pygame.display.set_mode((width, height), pygame.RESIZABLE) # test if it can be resized to fit different screen sizes
# current_screen = pygame.display.get_desktop_sizes()
# print(current_screen)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# create a 'fake screen' to resize elements (source: https://stackoverflow.com/a/34919705)
fake_screen = screen.copy()

# set window name
pygame.display.set_caption('robots.txt')

# set variables for text input (source: https://youtu.be/Rvcyf4HsWiw?si=ZIizByTLaZT7YBHN)
clock = pygame.time.Clock()
user_text = ''

#set background colour
fake_screen.fill(background_colour)

# set fonts
question_font = pygame.font.Font('assets/upheaval.ttf', 40)
input_font = pygame.font.Font('assets/windows.ttf', 35)

# ·················•·················• ★ •·················•·················

# add background image
fake_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 200), (height - 170))
rect_border.center = (width / 2, height / 2)
pygame.draw.rect(fake_screen, (194, 243, 232), rect_border, border_radius = 25)

rect = pygame.Rect(0, 0, (width - 240), (height - 210))
rect.center = (width / 2, height / 2)
pygame.draw.rect(fake_screen, (255, 194, 214), rect, border_radius = 15)

input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
input_rect.center = (width / 2, height / 2)
pygame.draw.rect(fake_screen, (255, 255, 255), input_rect, border_radius = 15)

# add question text
def display_question(question, font, text_colour, y):
    text = font.render(question, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

question, question_rect = display_question('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), (rect.y + 75))
fake_screen.blit(question, question_rect)


# ·················•·················• ★ •·················•·················

# keep screen on screen forever by creating an infinite loop
# until you close the window

active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # only let the user type when text box is selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
            
        # typing function
        if event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1] # remove last character
                else:
                    user_text += event.unicode
            
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            
        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
        
        # text input function
        input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
        input_rect.center = (width / 2, height / 2)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius = 15)
        
        if active:
            input_rect_border = pygame.Rect(0, 0, (width - 500), (height - 550))
            input_rect_border.center = (width / 2, height / 2)
            pygame.draw.rect(screen, (194, 243, 232), input_rect_border, 5, border_radius = 15)
        
        text_surface = input_font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 20, input_rect.y + 20))
        
        # display changes to the window
        pygame.display.flip()
        clock.tick(60)


# how to change the screen size to whatever the monitor size is