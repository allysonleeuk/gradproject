# IMPORTS
import pygame
pygame.init()

import sys


# VARIABLES + SETUP
(width, height) = (1470, 956) #currently set to my mac aspect ratio
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/tartan.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))

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
question_font = pygame.font.Font('assets/upheaval.ttf', 40)
input_font = pygame.font.Font('assets/windows.ttf', 45)

# set variables for text input (source: https://youtu.be/Rvcyf4HsWiw?si=ZIizByTLaZT7YBHN)
clock = pygame.time.Clock()
user_text = ''

# temporary variables + stored variables (NOTE: will these be on a different page or draw on the same screen and clear?)
user_name = ''
input_date = ''
input_time = ''

input_parts = [] # save the input in parts so I can send data to the machine learning aspect
final_inputs = []
name_array = []
date_array = []
time_array = []

# ·················•·················• ★ •·················•·················

# add background image
temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 200), (height - 170))
rect_border.center = (width / 2, height / 2)
pygame.draw.rect(temp_screen, (194, 243, 232), rect_border, border_radius = 25)

rect = pygame.Rect(0, 0, (width - 240), (height - 210))
rect.center = (width / 2, height / 2)
pygame.draw.rect(temp_screen, (255, 194, 214), rect, border_radius = 15)

input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
input_rect.center = (width / 2, height / 2)
pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

# add question text
def display_question(question, font, text_colour, y):
    text = font.render(question, True, text_colour) # boolean smooths font

    # center text 
    text_rect = text.get_rect(center=(width/2, y))
    return text, text_rect

question, question_rect = display_question('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), (rect.y + 75))
temp_screen.blit(question, question_rect)

# wrap text function (source: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font)
def wrap_text(text, font, colour, x, y, allowed_width, allowed_height):
    words = text.split()

    # split text into lines
    lines = []
    displayed_lines = []
    while len(words) > 0:

        line_words = []
        while len(words) > 0: # loop through words to form lines
            line_words.append(words.pop(0)) # pop first word
            fw, fh = font.size(' '.join(line_words + words[:1])) # add the first word back and get the size

            if fw > allowed_width:
                break
        
        line = ' '.join(line_words) # add a line with the selected words
        lines.append(line)
        displayed_lines.append(line)
    
    # print lines individually underneath the other
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # tx, ty is the x and y coords for the toft-left of the font surface
        tx = x - fw / 2 # center text
        ty = y + y_offset

        # move the text upwards when height of text box is exceeded
        if y_offset > allowed_height:
            # redraw rect to 'clear' screen
            # NOTE: can I add this into a function for clarity?
            temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
            pygame.display.update()

            pygame.draw.rect(temp_screen, (194, 243, 232), rect_border, border_radius = 25)
            pygame.draw.rect(temp_screen, (255, 194, 214), rect, border_radius = 15)
            pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

            question, question_rect = display_question('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), (rect.y + 75))
            temp_screen.blit(question, question_rect)


            displayed_lines.pop(0) # pop first line
            displayed_y_offset = 0 # reset y_offset to 0 so it draws from the top again
            for displayed_line in displayed_lines:
                fw, fh = font.size(displayed_line)

                tx = x - fw / 2 # center text
                ty = y + displayed_y_offset

                font_surface = font.render(displayed_line, True, colour)
                temp_screen.blit(font_surface, (tx, ty))

                displayed_y_offset += fh
            
            ty -= fh # reset y level

        else:
            font_surface = font.render(line, True, colour)
            temp_screen.blit(font_surface, (tx, ty))

            y_offset += fh # offset next line by font height, next line will be rendered underneath the current line


# add submit button (source: https://www.youtube.com/watch?v=G8MYGDf_9ho)
submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme

class Button(): # button class
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

                final_inputs.append(user_text)
                user_text = '' # reset user_text to an empty string

                # print(final_inputs)
                # print(user_text)

        # draw button to screen
        temp_screen.blit(self.image, (self.rect.x, self.rect.y))

submit_button = Button(height - 200, submit_button_img, 1) # create button instance

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
                
                # append current text to array after every keystroke (most recent  be sent to other screen in intervals)
                input_parts.append(user_text) # NOTE: will this make the array too large?
            
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        
        # text input function
        input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
        input_rect.center = (width / 2, height / 2)
        pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)
        
        if active:
            input_rect_border = pygame.Rect(0, 0, (width - 500), (height - 550))
            input_rect_border.center = (width / 2, height / 2)
            pygame.draw.rect(temp_screen, (194, 243, 232), input_rect_border, 5, border_radius = 15)
        
        padding = 20
        # text_surface = input_font.render(user_text, True, (0, 0, 0))
        # temp_screen.blit(text_surface, (input_rect.x + padding, input_rect.y + padding))
        wrap_text(user_text, 
                  input_font, 
                  (0, 0, 0), 
                  width / 2, 
                  input_rect.y + int(padding), 
                  input_rect.width - int(padding) * 2, 
                  input_rect.height - int(padding) * 2
                  )

        # display button
        submit_button.draw()


        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()
        clock.tick(60)
        