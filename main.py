# Importing libraries
import pygame
from pygame.locals import *
import sys
import random

# Initialising Pygame and the mixer
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Creating the screen and setting the dimensions
world = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Loading Images and converting them
titleScreen = pygame.image.load('Images/Title Screen.png').convert()
mainScreen = pygame.image.load('Images/UI.png').convert()
Blue = pygame.image.load('Images/Blue.png').convert()
Green = pygame.image.load('Images/Green.png').convert()
Orange = pygame.image.load('Images/Orange.png').convert()
Red = pygame.image.load('Images/Red.png').convert()
Yellow = pygame.image.load('Images/Yellow.png').convert()

# Defining variables for the mouse and clicks and base game state
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed(num_buttons=5)
gameState = 0
resolution = 1
smallFont = pygame.font.SysFont('Arial', 23)
largeFont = pygame.font.SysFont('Arial', 36)


# Creating the main class for entities in the game
class Entity:

    # Initialising the Class and setting each instance's attributes
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed):
        self.HPMax, self.HP = HPMax
        self.MPMax, self.MP = MPMax
        self.Strength = Strength
        self.Magic = Magic
        self.Defence = Defence
        self.Resistance = Resistance
        self.Speed = Speed

    # Attack function [WIP]
    def Attack(self):
        pass


class Player(Entity):
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed):
        super().__init__(HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed)


# Function for creating buttons
def button(start_x, start_y, width, height, function, text):
    start_x = (start_x / 1280) * world.get_width()
    start_y = (start_y / 720) * world.get_height()
    width = (width / 1280) * world.get_width()
    height = (height / 720) * world.get_height()
    if start_x + width > mouse[0] > start_x and start_y + height > mouse[1] > start_y:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.draw.rect(world, (150, 255, 0), (start_x, start_y, width, height))
        if click[0]:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                function()

    else:
        pygame.draw.rect(world, (0, 255, 0), (start_x, start_y, width, height))
    title = smallFont.render(text, True, (0, 0, 255))
    world.blit(title, (start_x, (start_y + (height / 2))))


# Function for changing the resolution of the screen
def change_Resolution():
    global world, mouse, smallFont, largeFont, resolution

    if resolution < 2:
        resolution += 1
    else:
        resolution = 0

    if resolution == 0:
        world = pygame.display.set_mode([640, 480])
        smallFont = pygame.font.SysFont('Arial', 18)
        largeFont = pygame.font.SysFont('Arial', 25)
    elif resolution == 1:
        world = pygame.display.set_mode([1280, 720])
        smallFont = pygame.font.SysFont('Arial', 23)
        largeFont = pygame.font.SysFont('Arial', 36)
    else:
        world = pygame.display.set_mode([1920, 1080])
        smallFont = pygame.font.SysFont('Arial', 28)
        largeFont = pygame.font.SysFont('Arial', 47)


# Function for redrawing the graphics in the game
def redraw_World():
    global titleScreen, mainScreen
    world.fill((0, 0, 0))
    bg = world.get_rect()
    if gameState == 0:
        titleScreenCopy = pygame.transform.scale(titleScreen, (bg[2], bg[3]))
        world.blit(titleScreenCopy, bg)
    elif gameState == 1:
        mainScreenCopy = pygame.transform.scale(mainScreen, (bg[2], bg[3]))
        world.blit(mainScreenCopy, bg)


# Function for generating the layout of the floors in the game
def generate_Floor():
    layout = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            layout[i][j] = random.randint(2, 4)
    return layout


# Function for rendering the map of the current floor on screen
def render_Map(rooms):
    for i in range(len(rooms)):
        pygame.draw.rect(world, [204, 153, 255], [17.5, 62, 40, 40])
        pygame.draw.rect(world, [204, 153, 255], [318.5, 62, 40, 40])
        for j in range(len(rooms[i])):
            if rooms[i][j] == 2:
                pygame.draw.rect(world, [255, 165, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
            elif rooms[i][j] == 3:
                pygame.draw.rect(world, [255, 0, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
            elif rooms[i][j] == 4:
                pygame.draw.rect(world, [0, 0, 255], [60.5 + (j * 43), 17 + (i * 45), 40, 40])


# Opening Screen for the Game
def main_Menu():
    global mouse, click, world
    while True:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        redraw_World()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        button(100.0, 200.0, 100.0, 50.0, main_Game, 'Start')
        button(100.0, 300.0, 100.0, 50.0, load_Game, 'Continue?')
        button(100.0, 400.0, 100.0, 50.0, change_Resolution, 'Toggle Resolution')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()
        clock.tick(60)


# Main game state
def main_Game():
    global gameState, world
    gameState = 1
    floor = generate_Floor()
    print(floor)
    while gameState == 1:

        redraw_World()
        render_Map(floor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()
        clock.tick(60)


# Save Game
def save_Game():
    global gameState
    gameState = 3
    pass


# Load Game
def load_Game():
    global gameState
    gameState = 4
    pass


# Test Function
def test():
    print("Hi")


main_Menu()
