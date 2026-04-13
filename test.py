# IMPORTS
import pygame
pygame.init()

import sys


# VARIABLES + SETUP
(width, height) = (1470, 956) #currently set to my mac aspect ratio
background_colour = (255,255,255)

# load in image and resize it to fit screen
bg_image = pygame.image.load('assets/frutigeraero.jpg')
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
name_font = pygame.font.Font('assets/upheaval.ttf', 60)
disclaimer_font = pygame.font.Font('assets/upheaval.ttf', 30)
question_font = pygame.font.Font('assets/upheaval.ttf', 40)
input_font = pygame.font.Font('assets/windows.ttf', 45)
# input_font = pygame.font.Font('assets/windows.ttf', 80) # for testing

# set variables for text input (source: https://youtu.be/Rvcyf4HsWiw?si=ZIizByTLaZT7YBHN)
clock = pygame.time.Clock()
user_text = ''
user_name = ''

# temporary variables + stored variables (NOTE: will these be on a different page or draw on the same screen and clear?)
input_date = ''
input_time = ''

input_parts = [] # save the input in parts so I can send data to the machine learning aspect
final_inputs = []
name_array = []
date_array = []
time_array = []

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
            temp_screen.blit(bg_image, (0, 0))
            pygame.display.update()

            draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)
            draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)
            pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

            question, question_rect = display_text('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), (rect.y + 75))
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


# ·················•·················• NAME SCREEN •·················•·················

# add background image
temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
pygame.display.update()

# add rect backgrounds
rect_border = pygame.Rect(0, 0, (width - 200), (height - 170))
rect_border.center = (width / 2, height / 2)
# pygame.draw.rect(temp_screen, (30, 180, 221), rect_border, border_radius = 25)
draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

rect = pygame.Rect(0, 0, (width - 240), (height - 210))
rect.center = (width / 2, height / 2)
# pygame.draw.rect(temp_screen, (51, 215, 239), rect, border_radius = 15)
draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

name_input_rect = pygame.Rect(0, 0, (width - 800), (height - 750))
name_input_rect.center = (width / 2, height / 2)
pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

# add name and disclaimer text text
name, name_rect = display_text('Enter Your Name', name_font, (0, 0, 0), (rect.y + 120))
temp_screen.blit(name, name_rect)

# add question text
disclaimer, disclaimer_rect = display_text('*Leave name empty to remain anonymous', disclaimer_font, (0, 0, 0), (rect.y + 180))
temp_screen.blit(disclaimer, disclaimer_rect)

# add submit button
submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme

change_button = Change_Button(height - 250, submit_button_img, 1) # create button instance

def name_screen():
    # add background image
    temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
    pygame.display.update()

    # add rect backgrounds
    rect_border = pygame.Rect(0, 0, (width - 200), (height - 170))
    rect_border.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (30, 180, 221), rect_border, border_radius = 25)
    draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

    rect = pygame.Rect(0, 0, (width - 240), (height - 210))
    rect.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (51, 215, 239), rect, border_radius = 15)
    draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

    name_input_rect = pygame.Rect(0, 0, (width - 800), (height - 750))
    name_input_rect.center = (width / 2, height / 2)
    pygame.draw.rect(temp_screen, (255, 255, 255), name_input_rect, border_radius = 15)

    # add name and disclaimer text text
    name, name_rect = display_text('Enter Your Name', name_font, (0, 0, 0), (rect.y + 120))
    temp_screen.blit(name, name_rect)

    # add question text
    disclaimer, disclaimer_rect = display_text('*Leave name empty to remain anonymous', disclaimer_font, (0, 0, 0), (rect.y + 180))
    temp_screen.blit(disclaimer, disclaimer_rect)

    # add submit button
    submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme

    change_button = Change_Button(height - 250, submit_button_img, 1) # create button instance


# ·················•·················• MAIN SCREEN •·················•·················
def main_screen():
    # add background image
    temp_screen.blit(bg_image, (0, 0)) # pygame.blit() = thin wrapper that allows you to draw images to the screen
    pygame.display.update()

    rect_border = pygame.Rect(0, 0, (width - 200), (height - 170))
    rect_border.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (30, 180, 221), rect_border, border_radius = 25)
    draw_rect_alpha(temp_screen, (30, 180, 221, 150), rect_border, 25)

    rect = pygame.Rect(0, 0, (width - 240), (height - 210))
    rect.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (51, 215, 239), rect, border_radius = 15)
    draw_rect_alpha(temp_screen, (51, 215, 239, 150), rect, 15)

    # input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
    # input_rect.center = (width / 2, height / 2)
    # pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

    # add question text
    question, question_rect = display_text('What do you dislike about the modern-day internet?', question_font, (0, 0, 0), (rect.y + 75))
    temp_screen.blit(question, question_rect)

    # add submit button
    submit_button_img = pygame.image.load('assets/submit_button.png').convert_alpha() # placeholder for now until I solidify the design theme
    
    global submit_button
    submit_button = Submit_Button(height - 200, submit_button_img, 1) # create button instance

# ·················•·················• ★ •·················•·················

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
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
            
            padding = 20
            wrap_text(user_name, 
                    name_font, 
                    (0, 0, 0), 
                    width / 2, 
                    name_input_rect.y + (name_input_rect.height / 2), # NOTE: fix this
                    name_input_rect.width - int(padding) * 2, 
                    name_input_rect.height - int(padding) * 2
                    )
            
            # display button
            change_button.draw()
            
        if main_screen_active == True: # MAIN SCREEN
            main_screen()

            # text input rect
            input_rect = pygame.Rect(0, 0, (width - 500), (height - 550))
            input_rect.center = (width / 2, height / 2)
            pygame.draw.rect(temp_screen, (255, 255, 255), input_rect, border_radius = 15)

            # only let the user type when text box is selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    main_active = True
                else:
                    main_active = False

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
                        user_text = user_text[:-1] # remove last character
                    else:
                        user_text += event.unicode
                    
                    # append current text to array after every keystroke (most recent  be sent to other screen in intervals)
                    input_parts.append(user_text) # NOTE: will this make the array too large?
            
            # create a border on the input rect when active
            if main_active == True:
                input_rect_border = pygame.Rect(0, 0, (width - 500), (height - 550))
                input_rect_border.center = (width / 2, height / 2)
                pygame.draw.rect(temp_screen, (30, 180, 221), input_rect_border, 5, border_radius = 15)

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


        if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        # draw fake screen to screen, have it transform when window size changes
        screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), (0, 0))
        
        # display changes to the window
        pygame.display.flip()
        clock.tick(60)
        