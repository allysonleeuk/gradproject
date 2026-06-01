# IMPORTS
import pygame
pygame.init()

import sys
import socket
import time
from datetime import datetime

import serial


# VARIABLES + SETUP
# (width, height) = (1470, 956) # currently set to my mac aspect ratio
(width, height) = (734, 830) # for split screen
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/frutigeraero.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))

# set screen size
screen = pygame.display.set_mode((width, height))

# create a 'fake screen' to resize elements (source: https://stackoverflow.com/a/34919705)
temp_screen = screen.copy()

# set window name
pygame.display.set_caption('human-side')

#set background colour
temp_screen.fill(background_colour)

# set fonts
name_font = pygame.font.Font('assets/upheaval.ttf', 52)
disclaimer_font = pygame.font.Font('assets/upheaval.ttf', 22)
question_font = pygame.font.Font('assets/upheaval.ttf', 30)
name_input_font = pygame.font.Font('assets/windows.ttf', 48)
input_font = pygame.font.Font('assets/windows.ttf', 35)

# set variables for text input (source: https://youtu.be/Rvcyf4HsWiw?si=ZIizByTLaZT7YBHN)
clock = pygame.time.Clock()
user_text = ''
user_name = ''
input_datetime = ''

# booleans
main_screen_active = False

name_active = False
main_active = False

# socket setup
host = "127.0.0.1"
port = 65432 # any number higher than 1023

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

last_sent_time = 0 # timer

# arduino setup
BAUD = 9600
ARDUINOPORT = '/dev/cu.usbmodem1020BA0AAC782' # serial port of arduino
ser = serial.Serial(ARDUINOPORT, BAUD)


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

        self.image = pygame.transform.smoothscale(image, (int(img_width * scale), int(img_height * scale)))
        self.rect = self.image.get_rect(center=(width/2, y))

    def draw(self): # draw button on screen

        # get mouse position and check mouseover + click
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: # 0 indicates a left click
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
                global user_name
                global input_datetime
                
                now = datetime.now().replace(microsecond=0)
                input_datetime = str(now)
                
                ser.write(f"{user_text}|{user_name}|{input_datetime}\n".encode())
                
                # print(user_text)
                # print(user_name)
                # print(input_datetime)
                
                user_text = '' # reset user_text to an empty string
                user_name = ''
                input_datetime = ''

                global main_screen_active
                main_screen_active = False

        # draw button to screen
        temp_screen.blit(self.image, (self.rect.x, self.rect.y))

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

        # tx, ty is the x and y coords for the top-left of the font surface
        tx = x - fw / 2 # centre text
        ty = y + y_offset

        # move the text upwards when height of text box is exceeded
        if y_offset > allowed_height:
            # redraw whole screen to 'clear' screen
            temp_screen.blit(bg_image, (0, 0))
            pygame.display.update()

            draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)
            draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)
            pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)
            
            # simulates that input box is active (main_active) -> once the screen clears it stops and I'm not sure how to amend that
            input_rect_border = pygame.Rect(0, 0, (width - 150), (height - 300))
            input_rect_border.center = (width / 2, height / 2)
            pygame.draw.rect(temp_screen, (30, 180, 221), input_rect_border, 5, border_radius = 15)

            question1, question1_rect = display_text('What do you dislike about', question_font, (0, 0, 0), (rect.y + 40))
            question2, question2_rect = display_text('the modern-day internet?', question_font, (0, 0, 0), (rect.y + 65))
            temp_screen.blit(question1, question1_rect)
            temp_screen.blit(question2, question2_rect)

            displayed_lines.pop(0) # pop first line
            displayed_y_offset = 0 # reset y_offset to 0 so it draws from the top again
            for displayed_line in displayed_lines:
                fw, fh = font.size(displayed_line)

                tx = x - fw / 2 # centre text
                ty = y + displayed_y_offset

                font_surface = font.render(displayed_line, True, colour)
                temp_screen.blit(font_surface, (tx, ty))

                displayed_y_offset += fh
            
            ty -= fh # reset y level

        else:
            font_surface = font.render(line, True, colour)
            temp_screen.blit(font_surface, (tx, ty))

            y_offset += fh # offset next line by font height, next line will be rendered underneath the current line


# ·················•·················• NAME SCREEN •·················•·················

# add background image
temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 60), (height - 60))
rect_border.center = (width / 2, height / 2)
draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

rect = pygame.Rect(0, 0, (width - 90), (height - 90))
rect.center = (width / 2, height / 2)
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
submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha()

change_button = Change_Button(height - 275, submit_button_img, 0.3) # create button instance

def name_screen():
    # add background image
    temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
    pygame.display.update()

    # add rect backgrounds
    rect_border = pygame.Rect(0, 0, (width - 60), (height - 60))
    rect_border.center = (width / 2, height / 2)
    draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

    rect = pygame.Rect(0, 0, (width - 90), (height - 90))
    rect.center = (width / 2, height / 2)
    draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

    name_input_rect = pygame.Rect(0, 0, (width - 280), (height - 700))
    name_input_rect.center = (width / 2, height / 2)
    pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

    # add name and disclaimer text text
    name, name_rect = display_text('Enter Your Name', name_font, (0, 0, 0), (rect.y + 200))
    temp_screen.blit(name, name_rect)

    disclaimer, disclaimer_rect = display_text('*Leave name empty to remain anonymous', disclaimer_font, (0, 0, 0), (rect.y + 240))
    temp_screen.blit(disclaimer, disclaimer_rect)

    # add submit button
    submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha()

    change_button = Change_Button(height - 275, submit_button_img, 0.3) # create button instance


# ·················•·················• MAIN SCREEN •·················•·················
def main_screen():
    # add background image
    temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
    pygame.display.update()

    rect_border = pygame.Rect(0, 0, (width - 60), (height - 60))
    rect_border.center = (width / 2, height / 2)
    draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

    rect = pygame.Rect(0, 0, (width - 90), (height - 90))
    rect.center = (width / 2, height / 2)
    draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

    # add question text
    question1, question1_rect = display_text('What do you dislike about', question_font, (0, 0, 0), (rect.y + 40))
    question2, question2_rect = display_text('the modern-day internet?', question_font, (0, 0, 0), (rect.y + 65))
    temp_screen.blit(question1, question1_rect)
    temp_screen.blit(question2, question2_rect)

    # add submit button
    submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha()
    
    global submit_button
    submit_button = Submit_Button(height - 100, submit_button_img, 0.3) # create button instance

# ·················•·················• ★ •·················•·················

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            s.close() # close socket connections

        
        if main_screen_active == False: # NAME SCREEN
            name_screen()

            # text input rect
            name_input_rect = pygame.Rect(0, 0, (width - 280), (height - 700))
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
                name_input_rect_border = pygame.Rect(0, 0, (width - 280), (height - 700))
                name_input_rect_border.center = (width / 2, height / 2)
                pygame.draw.rect(temp_screen, (30, 180, 221), name_input_rect_border, 5, border_radius = 15)
            
            padding = 20
            wrap_text(user_name, 
                    name_input_font, 
                    (0, 0, 0), 
                    width / 2, 
                    name_input_rect.y + 38,
                    name_input_rect.width - int(padding) * 2, 
                    name_input_rect.height - int(padding) * 2
                    )
            
            # display button
            change_button.draw()
            
        if main_screen_active == True: # MAIN SCREEN
            main_screen()

            # text input rect
            input_rect = pygame.Rect(0, 0, (width - 150), (height - 300))
            input_rect.center = (width / 2, height / 2)
            pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

            # only let the user type when text box is selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    main_active = True
                else:
                    main_active = False
                
            # typing function
            if event.type == pygame.KEYDOWN:
                if main_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1] # remove last character
                    else:
                        user_text += event.unicode
            
            # create a border on the input rect when active
            if main_active == True:
                input_rect_border = pygame.Rect(0, 0, (width - 150), (height - 300))
                input_rect_border.center = (width / 2, height / 2)
                pygame.draw.rect(temp_screen, (30, 180, 221), input_rect_border, 5, border_radius = 15)

            padding = 20
            wrap_text(user_text, 
                    input_font, 
                    (0, 0, 0), 
                    width / 2, 
                    input_rect.y + int(padding), 
                    input_rect.width - (int(padding) * 3), 
                    input_rect.height - (int(padding) * 3)
                    )
            
            # display button
            submit_button.draw()
            
        # open socket connection to transfer current user input to bot.py
        # send every 5 seconds
        current_time = time.time()
        
        if current_time - last_sent_time >= 5:
            s.send(user_text.encode())
            last_sent_time = current_time


        if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()
        clock.tick(60)
        