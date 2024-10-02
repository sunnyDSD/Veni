import pygame
from Settings import *  # Import everything from Settings.py
import os

# Initialize Pygame display
is_fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Venni Redemption')

# Load the background images for different phases
background_images = load_images()

# Scroll settings
scroll_positions = []  # Scrolling positions for each parallax layer
scroll_speed = [0.5, 1, 1.5]  # Parallax speed for each layer

# Dynamic scaling factors for buttons, background, and title
scale_factor_x = SCREEN_WIDTH / 640
scale_factor_y = SCREEN_HEIGHT / 480

# Load custom font for the title
try:
    title_font = pygame.font.Font(CUSTOM_FONT_PATH, int(FONT_SIZE * scale_factor_x))
except FileNotFoundError:
    print(f"Font not found at {CUSTOM_FONT_PATH}. Falling back to default font.")
    title_font = pygame.font.SysFont('Arial', int(FONT_SIZE * scale_factor_x))

# Title text rendering
title_text = "Venni Redemption"
title_surface = title_font.render(title_text, True, RED)
title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, int(100 * scale_factor_y)))

# Button class for handling buttons
class Button:
    def __init__(self, image, hover_image, pos, scale=True, scale_size=None):
        self.image = image
        self.hover_image = hover_image
        self.pos = pos
        self.hover_played = False  # Track hover sound play status

        if scale:
            if scale_size:
                self.image = pygame.transform.scale(self.image, scale_size)
                self.hover_image = pygame.transform.scale(self.hover_image, scale_size)
            else:
                self.image = pygame.transform.scale(self.image,
                    (int(self.image.get_width() * scale_factor_x), int(self.image.get_height() * scale_factor_y)))
                self.hover_image = pygame.transform.scale(self.hover_image,
                    (int(self.hover_image.get_width() * scale_factor_x), int(self.hover_image.get_height() * scale_factor_y)))

        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect)
            if not self.hover_played:
                BUTTON_HOVER_SOUND.play()
                self.hover_played = True
        else:
            self.hover_played = False
            screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                return True
        return False

# Font for fullscreen label (initial size)
try:
    label_font = pygame.font.Font(CUSTOM_FONT_PATH, 24)
except FileNotFoundError:
    label_font = pygame.font.SysFont('Arial', 24)

# Label surface and rect for fullscreen text
label_text = "Toggle Fullscreen"
label_surface = label_font.render(label_text, True, WHITE)
label_rect = label_surface.get_rect(center=(475, 70))  # Positioning below the fullscreen button

# Fullscreen toggle
def toggle_fullscreen():
    global is_fullscreen, screen, scale_factor_x, scale_factor_y, start_button, settings_button, exit_button, toggle_fullscreen_button, title_font, title_surface, title_rect, label_font, label_surface, label_rect

    if is_fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        is_fullscreen = False
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        is_fullscreen = True

    # Update scaling factors based on the new screen size
    current_screen_width, current_screen_height = screen.get_size()
    scale_factor_x = current_screen_width / 640
    scale_factor_y = current_screen_height / 480

    # Resize the buttons
    start_button = Button(START_BUTTON_IMAGE, START_BUTTON_HOVER_IMAGE, (int(320 * scale_factor_x), int(180 * scale_factor_y)))
    settings_button = Button(SETTINGS_BUTTON_IMAGE, SETTINGS_BUTTON_HOVER_IMAGE, (int(320 * scale_factor_x), int(250 * scale_factor_y)))
    exit_button = Button(EXIT_BUTTON_IMAGE, EXIT_BUTTON_HOVER_IMAGE, (int(320 * scale_factor_x), int(320 * scale_factor_y)))
    toggle_fullscreen_button = Button(TOGGLE_FULLSCREEN_BUTTON_IMAGE, TOGGLE_FULLSCREEN_HOVER_IMAGE, (int(630 * scale_factor_x), int(10 * scale_factor_y)), scale=True, scale_size=(50, 50))

    # Resize the title font
    title_font = pygame.font.Font(CUSTOM_FONT_PATH, int(FONT_SIZE * scale_factor_x))
    title_surface = title_font.render(title_text, True, RED)
    title_rect = title_surface.get_rect(center=(current_screen_width // 2, int(80 * scale_factor_y)))

    # **Resize the fullscreen label** based on new screen dimensions
    label_font = pygame.font.Font(CUSTOM_FONT_PATH, int(12 * scale_factor_x))  # Scale font size with screen width
    label_surface = label_font.render(label_text, True, WHITE)
    label_rect = label_surface.get_rect(center=(int(545 * scale_factor_x), int(25 * scale_factor_y)))  # Adjust label position as well

# Resize background layer if needed
def resize_layer(layer, target_width, target_height):
    layer_width, layer_height = layer.get_size()
    if layer_width < target_width or layer_height < target_height:
        layer = pygame.transform.scale(layer, (target_width, target_height))
    return layer

# Initialize scroll positions based on the number of layers
def initialize_scroll_positions(num_layers):
    global scroll_positions
    scroll_positions = [0] * num_layers

# Draw parallax background
def draw_parallax_background():
    global scroll_positions

    current_layers = background_images.get(current_phase, [])

    if len(scroll_positions) != len(current_layers):
        initialize_scroll_positions(len(current_layers))

    for i, layer in enumerate(current_layers):
        layer = resize_layer(layer, screen.get_width(), screen.get_height())
        layer_speed = scroll_speed[i % len(scroll_speed)]
        scroll_positions[i] -= layer_speed

        if scroll_positions[i] <= -screen.get_width():
            scroll_positions[i] = 0

        screen.blit(layer, (scroll_positions[i], 0))
        screen.blit(layer, (scroll_positions[i] + screen.get_width(), 0))

# Animate the background phase transition
def animate_background():
    global current_phase, phase_start_time

    current_time = pygame.time.get_ticks()
    time_in_phase = current_time - phase_start_time

    draw_parallax_background()

    if time_in_phase > time_phases[current_phase]:
        phase_start_time = current_time

        phases = list(time_phases.keys())
        current_index = phases.index(current_phase)
        next_phase = phases[(current_index + 1) % len(phases)]

        print(f"Transitioning from {current_phase} to {next_phase}")
        current_phase = next_phase

# Initialize phase control
current_phase = "morning"
phase_start_time = pygame.time.get_ticks()

# Create buttons
start_button = Button(START_BUTTON_IMAGE, START_BUTTON_HOVER_IMAGE, (320, 200))
settings_button = Button(SETTINGS_BUTTON_IMAGE, SETTINGS_BUTTON_HOVER_IMAGE, (320, 250))
exit_button = Button(EXIT_BUTTON_IMAGE, EXIT_BUTTON_HOVER_IMAGE, (320, 300))
toggle_fullscreen_button = Button(TOGGLE_FULLSCREEN_BUTTON_IMAGE, TOGGLE_FULLSCREEN_HOVER_IMAGE, (620, 25), scale=True, scale_size=(50, 50))

# Settings menu
def settings_menu():
    settings_running = True
    while settings_running:
        screen.fill(BLUE)

        # Draw parallax background
        animate_background()

        # Draw fullscreen button
        toggle_fullscreen_button.draw(screen)

        # Fullscreen label text
        screen.blit(label_surface, label_rect)  # Draw resized label

        fps_toggle_button = Button(BACK_BUTTON_ICON, BACK_BUTTON_HOVER_ICON, (320, 320))
        fps_toggle_button.draw(screen)

        back_button = Button(BACK_BUTTON_ICON, BACK_BUTTON_HOVER_ICON, (320, 400))
        back_button.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(CURSOR_IMAGE, (mouse_x, mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if toggle_fullscreen_button.is_clicked(event):
                toggle_fullscreen()
            if fps_toggle_button.is_clicked(event):
                toggle_fps()
            if back_button.is_clicked(event):
                settings_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_running = False

        pygame.display.flip()
        clock.tick(FPS)

# Main menu
def main_menu():
    play_main_menu_music()

    menu_running = True
    while menu_running:
        screen.fill(BLUE)
        animate_background()

        screen.blit(title_surface, title_rect)
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(CURSOR_IMAGE, (mouse_x, mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                stop_main_menu_music()
                menu_running = False
            if settings_button.is_clicked(event):
                settings_menu()
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# Main game loop
def main_game():
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        animate_background()

        pygame.display.flip()
        clock.tick(FPS)

# Start the game
main_menu()
main_game()
