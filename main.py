# imports
import pygame
pygame.init()


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
question_font = pygame.font.Font('assets/upheaval.ttf', 50)

# ·················•·················• ★ •·················•·················

# add background image
screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add question text
def display_question(text, font, text_colour, x, y):
    question = font.render(text, True, text_colour) # boolean smooths font
    screen.blit(question, (x, y))

display_question('WHAT do you dislike about the modern-day internet?', question_font, (0, 0, 0), 0, 0)



# ·················•·················• ★ •·················•·················

#display changes to the window
pygame.display.flip()

# keep screen on screen forever by creating an infinite loop
# until you close the window
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

# how to set window to fullscreen (only do this once it's finished)
# how to change the screen size to whatever the monitor size is