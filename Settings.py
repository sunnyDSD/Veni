import pygame
import os
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Define colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (51, 153, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# P1: Frame rate settings (default to 60fps)
FPS = 60

# Load button images
START_BUTTON_IMAGE = pygame.image.load('Images/Button Itch Pack/Start/Start1.png')
START_BUTTON_HOVER_IMAGE = pygame.image.load('Images/Button Itch Pack/Start/Start5.png')

SETTINGS_BUTTON_IMAGE = pygame.image.load('Images/Button Itch Pack/Settings/Settings1.png')
SETTINGS_BUTTON_HOVER_IMAGE = pygame.image.load('Images/Button Itch Pack/Settings/Settings5.png')

EXIT_BUTTON_IMAGE = pygame.image.load('Images/Button Itch Pack/Quit/Quit1.png')
EXIT_BUTTON_HOVER_IMAGE = pygame.image.load('Images/Button Itch Pack/Quit/Quit5.png')

BACK_BUTTON_ICON = pygame.image.load('Images/Button Itch Pack/Back/Back1.png')
BACK_BUTTON_HOVER_ICON = pygame.image.load('Images/Button Itch Pack/Back/Back5.png')

# Fullscreen toggle button images (replace with correct image paths)
TOGGLE_FULLSCREEN_BUTTON_IMAGE = pygame.image.load('Images/IconsWenrexa/01.png')
TOGGLE_FULLSCREEN_HOVER_IMAGE = pygame.image.load('Images/IconsWenrexa/01.png')

# Cursor image (ensure these paths are correct)
CURSOR_IMAGE = pygame.image.load('Images/100 Mouse Cursors - Pack (8x8)/cursor-8x8-white/10.png')

# Custom font path (replace with the correct font file path)
CUSTOM_FONT_PATH = 'Images/boxel_v0.1 (1)/Boxel_v0.1/Boxel_v0.1_beta.ttf'
FONT_SIZE = 50  # Set a base font size  

# Load additional images for the main menu decoration
MENU_DECORATION_IMAGE_1 = pygame.image.load('Images/UI buttons/Pxiel Art U3I borders.png')
MENU_DECORATION_IMAGE_2 = pygame.image.load('Images/UI buttons/Dungeon Ruins Tileset2 Day.png')

# Load sounds for button interactions
BUTTON_HOVER_SOUND = pygame.mixer.Sound('audio/UI Soundpack/UI Soundpack/MP3/Abstract1.mp3')
BUTTON_CLICK_SOUND = pygame.mixer.Sound('audio/UI Soundpack/UI Soundpack/MP3/African1.mp3')

# Load background music (main menu)
MAIN_MENU_MUSIC = 'audio/UI Soundpack/Recording 2024-09-17 024141 (online-audio-converter.com).wav'

# P2: Function to start playing background music
def play_main_menu_music():
    try:
        pygame.mixer.music.load(MAIN_MENU_MUSIC)
        pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop the music infinitely
        print("Main menu music playing.")
    except pygame.error as e:
        print(f"Error playing music: {e}")

# P3: Function to stop playing background music
def stop_main_menu_music():
    pygame.mixer.music.stop()
    print("Main menu music stopped.")

# Clock setup
clock = pygame.time.Clock()

# Time settings for transitioning between phases (in milliseconds)
time_phases = {
    "morning": 60000,  # 60 seconds for the morning phase
    "daytime": 60000,  # 60 seconds for daytime
    "evening": 60000,  # 60 seconds for evening
    "night": 60000,    # 60 seconds for night
    "late_night": 60000, # 60 seconds for late night
    "sunrise": 60000   # 60 seconds for sunrise
}

# P4: Function to load images for the parallax scrolling background
def load_images():
    background_images = {
        "morning": load_layered_images_from_folder('Images/Clouds/Clouds 1'),
        "daytime": load_layered_images_from_folder('Images/Clouds/Clouds 2'),
        "evening": load_layered_images_from_folder('Images/Clouds/Clouds 3'),
        "night": load_layered_images_from_folder('Images/Clouds/Clouds 4'),
        "late_night": load_layered_images_from_folder('Images/Clouds/Clouds 5'),
        "sunrise": load_layered_images_from_folder('Images/Clouds/Clouds 6')
    }
    return background_images

# P5: Helper function to load layered images from a folder
def load_layered_images_from_folder(folder_path):
    layers = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            img = pygame.image.load(img_path).convert_alpha()
            layers.append(img)
    return layers
