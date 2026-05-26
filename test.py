# IMPORTS
import pygame
pygame.init()

import sys
import socket
import time


# VARIABLES + SETUP
# (width, height) = (1470, 956) # currently set to my mac aspect ratio
(width, height) = (735, 823) # for split screen
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/frutigeraero.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))

# set screen size
screen = pygame.display.set_mode((width, height))


# create a 'fake screen' to resize elements (source: https://stackoverflow.com/a/34919705)
temp_screen = screen.copy()

# set window name
pygame.display.set_caption('robots.txt')

#set background colour
temp_screen.fill(background_colour)

# set fonts
name_font = pygame.font.Font('assets/upheaval.ttf', 52) # NOTE: CHANGED
disclaimer_font = pygame.font.Font('assets/upheaval.ttf', 22) # NOTE: CHANGED
question_font = pygame.font.Font('assets/upheaval.ttf', 40)
name_input_font = pygame.font.Font('assets/windows.ttf', 50) # NOTE: CHANGED
input_font = pygame.font.Font('assets/windows.ttf', 45)
# input_font = pygame.font.Font('assets/windows.ttf', 80) # for testing

# set variables for text input (source: https://youtu.be/Rvcyf4HsWiw?si=ZIizByTLaZT7YBHN)
clock = pygame.time.Clock()
user_text = ''
user_name = ''

# temporary variables + stored variables
input_date = '' # NOTE: ADD THIS, AND SEND TO ARDUINO
input_time = '' # NOTE: ADD THIS, AND SEND TO ARDUINO

final_inputs = [] # NOTE: DO I NEED TO STORE THIS??? I'M SENDING IT IMMEDIATELY
name_array = [] # NOTE: DO I NEED TO STORE THIS??? I'M SENDING IT IMMEDIATELY
# date_array = [] # NOTE: DO I NEED TO STORE THIS??? I'M SENDING IT IMMEDIATELY
# time_array = [] # NOTE: DO I NEED TO STORE THIS??? I'M SENDING IT IMMEDIATELY

# booleans
main_screen_active = False

name_active = False
main_active = False

# ·················•·················• FUNCTIONS ETC. •·················•·················

# make rects transparent (source: https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame)
def draw_rect_alpha(surface, color, rect, radius):
    transparent_screen = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(transparent_screen, color, transparent_screen.get_rect(), border_radius = radius)
    surface.blit(transparent_screen, rect)

# display text to screen and centre
def display_text(question, font, text_colour, y):
    text = font.render(question, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

# add submit button (source: https://www.youtube.com/watch?v=G8MYGDf_9ho)
class Change_Button(): # button class
    def __init__(self, y, image, scale):
        img_width = image.get_width()
        img_height = image.get_height()

        self.image = pygame.transform.scale(image, (int(img_width * scale), int(img_height * scale)))
        self.rect = self.image.get_rect(center=(width/2, y))

    def draw(self): # draw button on screen

        # get mouse position and check mouseover + click
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: # 0 indicates a left click
                global user_name
                
                name_array.append(user_name)
                user_name = ''

                global main_screen_active
                main_screen_active = True

        # draw button to screen
        temp_screen.blit(self.image, (self.rect.x, self.rect.y))

class Submit_Button(): # button class
    def __init__(self, y, image, scale):
        img_width = image.get_width()
        img_height = image.get_height()

        self.image = pygame.transform.scale(image, (int(img_width * scale), int(img_height * scale)))
        self.rect = self.image.get_rect(center=(width/2, y))

    def draw(self): # draw button on screen

        # get mouse position and check mouseover + click
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: # 0 indicates a left click
                global user_text # change to global variable so I can reset it
                global input_parts

                final_inputs.append(user_text)
                user_text = '' # reset user_text to an empty string
                input_parts = [] # reset input_parts to an empty string

                # print(final_inputs)
                # print(user_text)

                global main_screen_active
                main_screen_active = False

        # draw button to screen
        temp_screen.blit(self.image, (self.rect.x, self.rect.y))


# ·················•·················• NAME SCREEN •·················•·················

# add background image
temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 60), (height - 320))
rect_border.center = (width / 2, height / 2)
# pygame.draw.rect(temp_screen, (30, 180, 221), rect_border, border_radius = 25)
draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

rect = pygame.Rect(0, 0, (width - 90), (height - 350))
rect.center = (width / 2, height / 2)
# pygame.draw.rect(temp_screen, (51, 215, 239), rect, border_radius = 15)
draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

name_input_rect = pygame.Rect(0, 0, (width - 280), (height - 700))
name_input_rect.center = (width / 2, height / 2)
pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

# add name and disclaimer text text
name, name_rect = display_text('Enter Your Name', name_font, (0, 0, 0), (rect.y + 75))
temp_screen.blit(name, name_rect)

disclaimer, disclaimer_rect = display_text('*Leave name empty to remain anonymous', disclaimer_font, (0, 0, 0), (rect.y + 115))
temp_screen.blit(disclaimer, disclaimer_rect)

# add submit button
submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme

change_button = Change_Button(height - 275, submit_button_img, 0.8) # create button instance

def name_screen():
    # add background image
    temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
    pygame.display.update()

    # add rect backgrounds
    rect_border = pygame.Rect(0, 0, (width - 60), (height - 320))
    rect_border.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (30, 180, 221), rect_border, border_radius = 25)
    draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

    rect = pygame.Rect(0, 0, (width - 90), (height - 350))
    rect.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (51, 215, 239), rect, border_radius = 15)
    draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

    name_input_rect = pygame.Rect(0, 0, (width - 280), (height - 700))
    name_input_rect.center = (width / 2, height / 2)
    pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

    # add name and disclaimer text text
    name, name_rect = display_text('Enter Your Name', name_font, (0, 0, 0), (rect.y + 75))
    temp_screen.blit(name, name_rect)

    disclaimer, disclaimer_rect = display_text('*Leave name empty to remain anonymous', disclaimer_font, (0, 0, 0), (rect.y + 115))
    temp_screen.blit(disclaimer, disclaimer_rect)

    # add submit button
    submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme

    change_button = Change_Button(height - 275, submit_button_img, 0.8) # create button instance
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            s.close() # close socket connections

        
        if main_screen_active == False: # NAME SCREEN
            name_screen()

            # text input rect
            name_input_rect = pygame.Rect(0, 0, (width - 800), (height - 750))
            name_input_rect.center = (width / 2, height / 2)
            pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

            # only let the user type when text box is selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_input_rect.collidepoint(event.pos):
                    name_active = True
                else:
                    name_active = False
                
            # typing function
            if event.type == pygame.KEYDOWN:
                if name_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1] # remove last character
                    else:
                        user_name += event.unicode
            
            # create a border on the input rect when active
            if name_active == True:
                name_input_rect_border = pygame.Rect(0, 0, (width - 800), (height - 750))
                name_input_rect_border.center = (width / 2, height / 2)
                pygame.draw.rect(temp_screen, (30, 180, 221), name_input_rect_border, 5, border_radius = 15)
            
            # display button
            change_button.draw()

        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()
        clock.tick(60)