# imports
import pygame
pygame.init()

import sys


# variables
(width, height) = (1600, 1000) #currently set to mac aspect ratio
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/tartan.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))


# set screen size
screen = pygame.display.set_mode((width, height))
# current_screen = pygame.display.get_desktop_sizes()
# print(current_screen)

# set window name
pygame.display.set_caption('robots.txt')

#set background colour
screen.fill(background_colour)

# set font
question_font = pygame.font.Font('assets/upheaval.ttf', 40)

# ·················•·················• ★ •·················•·················

# add background image
screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 200), (height - 150))
rect_border.center = (width / 2, height / 2)
pygame.draw.rect(screen, (194, 243, 232), rect_border, border_radius = 25)

rect = pygame.Rect(0, 0, (width - 240), (height - 190))
rect.center = (width / 2, height / 2)
pygame.draw.rect(screen, (255, 194, 214), rect, border_radius = 20)


input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
input_rect.center = (width / 2, height / 2)
pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius = 15)

# add question text
def display_question(question, font, text_colour, y):
    text = font.render(question, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

question, question_rect = display_question('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), height / 5)
screen.blit(question, question_rect)


# ·················•·················• ★ •·················•·················

#display changes to the window
pygame.display.flip()

# keep screen on screen forever by creating an infinite loop
# until you close the window
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

# how to set window to fullscreen (only do this once it's finished)
# how to change the screen size to whatever the monitor size is