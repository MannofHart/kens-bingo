#!/usr/bin/python

# This is a port of a bingo program I wrote many years ago using C#
# it has been used in many bars in the Benidorm area, and now I am
# attempting to port it over to python for linux use
#
# Ken Williams GW3TMH ken@kensmail.uk

# Import a library of functions called 'pygame'
import pygame
from pygame.locals import *
import random
from pygame.mixer import music

# Initialize the game engine
pygame.mixer.pre_init(22000, -16, 2, 2048)
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# Default screen size
display_width = 840
display_height = 480

# Used to define which screen is displayed
mode = 0
# Counter that increments with each call
calls = 0

should_stop = True
game_started = False
auto_play_countdown = 5

# Place for randomly generated numbers
number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
          10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
          30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
          40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
          50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
          60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
          70, 71, 72, 73, 74, 75]

# Used by calls checker screen
checks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
          10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
          30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
          40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
          50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
          60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
          70, 71, 72, 73, 74, 75]

bingo_array = ['B', 'I', 'N', 'G', 'O']

# Ditty displayed under number
ditty = ['C=Check R=Reset Spacebar=Start P=Pause Game ESC=Close Game']
filepath = 'phrases.txt'
with open(filepath) as fp:
   line = fp.readline().strip()
   while line:
       ditty.append(line)
       line = fp.readline().strip()

sounds = []
for x in range(1, 76):
    try:
        sound = pygame.mixer.Sound('assets/%d.wav' % x)
        sounds.append(sound)
    except Exception as err:
        print(err)
        raise

# Reset game definition is here
def reset_game():
    global calls
    global number
    global auto_play_countdown
    global should_stop
    global game_started

    # set arrays to zero's
    for i in range(0, 76):
        checks[i] = 0
        number[i] = 0

    calls = 0
    auto_play_countdown = 5
    should_stop = True
    game_started = False

    while True:
        x = random.randint(1, 75)
        for i in range(1, 76):
            if (number[i] == x):
                break
            if (number[i] == 0):
                number[i] = x
                if (i == 75):
                    return
                break


# Set the height and width of the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # default screensize to fullscreen

pygame.display.set_caption("Ken's Bingo")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

pygame.time.set_timer(pygame.USEREVENT, 1000)

# Reset game
reset_game()

def stop_loop():
    global should_stop

    should_stop = True

# Loop as long as done == False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #use ESC key to close program
                pygame.quit()
          
        if event.type == pygame.USEREVENT and 'key' not in event.dict:
            if should_stop or mode == 2:
                continue

            auto_play_countdown -= 1
            if auto_play_countdown < 0:
                auto_play_countdown = 5

                if mode == 1:
                    mode = 0
                    pygame.event.post(pygame.event.Event(USEREVENT, key=pygame.K_SPACE))
                else:
                    mode = 1
                    pygame.event.post(pygame.event.Event(USEREVENT, key=pygame.K_c))

        if event.type == VIDEORESIZE:
            # The main code that resizes the window:
            # (recreate the window with the new size)
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            pygame.display.flip()
        elif event.type == KEYDOWN and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True
                pygame.event.post(pygame.event.Event(USEREVENT, key=pygame.K_c))
                mode = 1

            # start and stop
            should_stop = not should_stop
        elif event.type == USEREVENT and 'key' in event.dict and event.dict['key'] == pygame.K_SPACE:
            # Get next number
            mode = 0
            if (calls < 75):
                calls = calls + 1
                checks[number[calls]] = number[calls]
                sound = sounds[number[calls] - 1]
                sound.play()

        elif event.type == KEYDOWN and event.key == pygame.K_p:
            # Get previous number
            should_stop = not should_stop
        elif event.type == USEREVENT and 'key' in event.dict and event.dict['key'] == pygame.K_c:
            mode = 1
        elif event.type == KEYDOWN and event.key == pygame.K_c:
            if mode == 1:
                continue
            else:
                should_stop = True
                mode = 1
        elif event.type == KEYDOWN and event.key == pygame.K_n:
            # Reset game abort
            if (mode == 2):
                mode = 0
        elif event.type == KEYDOWN and event.key == pygame.K_r:
            # Reset game ?
            mode = 2
        elif event.type == KEYDOWN and event.key == pygame.K_y:
            # Reset game confirm
            if (mode == 2):
                mode = 0
                reset_game()

    # All drawing code happens after the for loop and but
    # inside the main while not done loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Get the surface of the current active display
    surface = pygame.display.get_surface()

    # Create an array of surface.width and surface.height
    display_width, display_height = size = surface.get_width(), surface.get_height()

    # Draw a rectangle on the top 90 percent of screen
    pygame.draw.rect(screen, BLUE, [0, 0, display_width, (display_height / 10 * 9)], 0)

    if (mode == 0):
        # Display called number very big
        text = ""
        text_center = (0,0)
        text_size = 0

        if calls == 0 and not game_started:
            text = "Ready to play?"
            text_center = ((display_width / 2), (display_height / 10 * 4))
            text_size = int(display_height / 10 * 2)
        elif calls != 0:
            number_letter = 'N/A'

            if number[calls] in range(1, 16):
                number_letter = 'B'
            elif number[calls] in range(16, 31):
                number_letter = 'I'
            elif number[calls] in range(31, 46):
                number_letter = 'N'
            elif number[calls] in range(46, 61):
                number_letter = 'G'
            elif number[calls] in range(61, 75):
                number_letter = '0'
            # Get the text
            text = "%s %d" % (number_letter, (number[calls]))
            text_center = ((display_width / 2), (display_height / 10 * 4))
            text_size = int(display_height / 10 * 7.5)

        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Arial', text_size, True, False)
        # Get the rectangle size
        TextSurface = font.render(text, True, BLACK)
        TextRect = TextSurface.get_rect()
        # Display result
        TextRect.center = text_center
        # Put the image of the text on the screen
        screen.blit(TextSurface, TextRect)

    if (mode == 1):
        # Check screen
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Arial', int(display_height / 12), True, False)
        # Get the text
        i = 0
        for r in range(1, 6):
            # Get the rectangle size
            TextSurface = font.render(bingo_array[r-1], True, BLACK)
            TextRect = TextSurface.get_rect()
            # Display result
            TextRect.center = ((display_width / 18 * 0) + display_width / 33,
                               (display_height / 50 * 6) + (r * display_height / 14) - display_height / 14)
            # Put the image of the text on the screen
            screen.blit(TextSurface, TextRect)

            for c in range(1, 16):
                i = i + 1
                # Default
                text = "-"
                if (checks[i] != 0):
                    text = "%d" % (checks[i])
                # Get the rectangle size
                TextSurface = font.render(text, True, BLACK)
                TextRect = TextSurface.get_rect()
                # Display result
                TextRect.center = ((display_width / 18 * c) + display_width / 33,
                                   (display_height / 50 * 6) + (r * display_height / 14) - display_height / 14)
                # Put the image of the text on the screen
                screen.blit(TextSurface, TextRect)

    if (mode == 2):
        # Ask if you are sure you want to do a reset
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Arial', int(display_height / 8), True, False)
        # Get the text
        text = "Reset game? y or n"
        # Get the rectangle size
        TextSurface = font.render(text, True, RED)
        TextRect = TextSurface.get_rect()
        # Display result
        TextRect.center = ((display_width / 2), (display_height / 3))
        # Put the image of the text on the screen
        screen.blit(TextSurface, TextRect)

    if should_stop and game_started:
        # Ask if you are sure you want to do a reset
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Arial', int(32), True, False)
        # Get the text
        text = "Paused"
        # Get the rectangle size
        TextSurface = font.render(text, True, RED)
        TextRect = TextSurface.get_rect()
        # Display result
        TextRect.center = (TextSurface.get_width(), TextSurface.get_height() + 5)
        # Put the image of the text on the screen
        screen.blit(TextSurface, TextRect)

    # Display number ditty
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Arial', int(display_height / 20), True, False)
    # Get the text
    text = ditty[number[calls]]
    # Get the rectangle size
    TextSurface = font.render(text, True, BLACK)
    TextRect = TextSurface.get_rect()
    # Display result
    TextRect.center = ((display_width / 2), (display_height / 10 * 8))
    # Put the image of the text on the screen
    screen.blit(TextSurface, TextRect)

    # Display number of calls
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Arial', int(display_height / 20), True, False)
    # Get the text
    text = "Number Of Calls %d Last Number Called %d" % (calls, number[calls])
    # Get the rectangle size
    TextSurface = font.render(text, True, BLACK)
    TextRect = TextSurface.get_rect()
    # Display result
    TextRect.center = ((display_width / 2), (display_height / 10 * 9.5))
    # Put the image of the text on the screen
    screen.blit(TextSurface, TextRect)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
