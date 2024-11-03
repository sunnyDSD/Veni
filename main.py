import pygame
import Settings  # Import the Settings module directly
import os
import sys

# Initialize Pygame display
is_fullscreen = False
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption('Venni Redemption')

# Load the background images for different phases
background_images = Settings.load_images()

# Scroll settings
scroll_positions = []  # Scrolling positions for each parallax layer
scroll_speed = [0.5, 1, 1.5]  # Parallax speed for each layer

# Dynamic scaling factors for buttons, background, and title
scale_factor_x = Settings.SCREEN_WIDTH / 640
scale_factor_y = Settings.SCREEN_HEIGHT / 480

# Load custom font for the title
try:
    title_font = pygame.font.Font(Settings.CUSTOM_FONT_PATH, int(Settings.FONT_SIZE * scale_factor_x))
except FileNotFoundError:
    print(f"Font not found at {Settings.CUSTOM_FONT_PATH}. Falling back to default font.")
    title_font = pygame.font.SysFont('Arial', int(Settings.FONT_SIZE * scale_factor_x))

# Title text rendering
title_text = "Venni Redemption"
title_surface = title_font.render(title_text, True, Settings.RED)
title_rect = title_surface.get_rect(center=(Settings.SCREEN_WIDTH // 2, int(100 * scale_factor_y)))

# Button class remains unchanged
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
                self.image = pygame.transform.scale(
                    self.image,
                    (int(self.image.get_width() * scale_factor_x), int(self.image.get_height() * scale_factor_y)))
                self.hover_image = pygame.transform.scale(
                    self.hover_image,
                    (int(self.hover_image.get_width() * scale_factor_x), int(self.hover_image.get_height() * scale_factor_y)))

        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect)
            if not self.hover_played:
                Settings.BUTTON_HOVER_SOUND.play()
                self.hover_played = True
        else:
            self.hover_played = False
            screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                Settings.BUTTON_CLICK_SOUND.play()
                return True
        return False

# Font for labels (initial size)
try:
    label_font = pygame.font.Font(Settings.CUSTOM_FONT_PATH, 24)
except FileNotFoundError:
    label_font = pygame.font.SysFont('Arial', 24)

# Fullscreen toggle
def toggle_fullscreen():
    global is_fullscreen, screen, scale_factor_x, scale_factor_y
    global title_font, title_surface, title_rect

    if is_fullscreen:
        screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        is_fullscreen = False
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        is_fullscreen = True

    # Update scaling factors based on the new screen size
    current_screen_width, current_screen_height = screen.get_size()
    scale_factor_x = current_screen_width / 640
    scale_factor_y = current_screen_height / 480

    # Resize the title font
    try:
        title_font = pygame.font.Font(Settings.CUSTOM_FONT_PATH, int(Settings.FONT_SIZE * scale_factor_x))
    except FileNotFoundError:
        title_font = pygame.font.SysFont('Arial', int(Settings.FONT_SIZE * scale_factor_x))
    title_surface = title_font.render(title_text, True, Settings.RED)
    title_rect = title_surface.get_rect(center=(current_screen_width // 2, int(80 * scale_factor_y)))

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

    if time_in_phase > Settings.time_phases[current_phase]:
        phase_start_time = current_time

        phases = list(Settings.time_phases.keys())
        current_index = phases.index(current_phase)
        next_phase = phases[(current_index + 1) % len(phases)]

        print(f"Transitioning from {current_phase} to {next_phase}")
        current_phase = next_phase

# Initialize phase control
current_phase = "morning"
phase_start_time = pygame.time.get_ticks()

# Create buttons
start_button = Button(Settings.START_BUTTON_IMAGE, Settings.START_BUTTON_HOVER_IMAGE, (320, 200))
settings_button = Button(Settings.SETTINGS_BUTTON_IMAGE, Settings.SETTINGS_BUTTON_HOVER_IMAGE, (320, 250))
exit_button = Button(Settings.EXIT_BUTTON_IMAGE, Settings.EXIT_BUTTON_HOVER_IMAGE, (320, 300))

# Settings menu
def settings_menu():
    settings_running = True

    # Create the FPS toggle button
    fps_toggle_button = Button(
        Settings.FPS_TOGGLE_BUTTON_IMAGE,
        Settings.FPS_TOGGLE_BUTTON_HOVER_IMAGE,
        (320, 320)  # Adjust position as needed
    )

    # Back button
    back_button = Button(Settings.BACK_BUTTON_ICON, Settings.BACK_BUTTON_HOVER_ICON, (320, 400))

    # Fullscreen toggle button
    toggle_fullscreen_button = Button(Settings.TOGGLE_FULLSCREEN_BUTTON_IMAGE, Settings.TOGGLE_FULLSCREEN_HOVER_IMAGE,
                                      (630, 25), scale=True, scale_size=(50, 50))

    # Label for fullscreen toggle
    label_text_fullscreen = "Toggle Fullscreen"
    try:
        label_font_fullscreen = pygame.font.Font(Settings.CUSTOM_FONT_PATH, 24)
    except FileNotFoundError:
        label_font_fullscreen = pygame.font.SysFont('Arial', 24)
    label_surface_fullscreen = label_font_fullscreen.render(label_text_fullscreen, True, Settings.WHITE)
    label_rect_fullscreen = label_surface_fullscreen.get_rect(center=(475, 70))

    # Function to update FPS label
    def update_fps_label():
        if Settings.show_fps:
            label_text = "FPS: On"
            label_color = Settings.GREEN  # Use green color when FPS is on
        else:
            label_text = "FPS: Off"
            label_color = Settings.RED  # Use red color when FPS is off
        try:
            fps_label_font = pygame.font.Font(Settings.CUSTOM_FONT_PATH, 24)
        except FileNotFoundError:
            fps_label_font = pygame.font.SysFont('Arial', 24)
        fps_label_surface = fps_label_font.render(label_text, True, label_color)
        # Position the label next to the FPS toggle button
        fps_label_rect = fps_label_surface.get_rect(midleft=(fps_toggle_button.rect.right + 10, fps_toggle_button.rect.centery))
        return fps_label_surface, fps_label_rect

    fps_label_surface, fps_label_rect = update_fps_label()

    while settings_running:
        screen.fill(Settings.BLUE)

        # Draw parallax background
        animate_background()

        # Draw fullscreen button and label
        toggle_fullscreen_button.draw(screen)
        screen.blit(label_surface_fullscreen, label_rect_fullscreen)

        # Draw FPS toggle button and label
        fps_toggle_button.draw(screen)
        screen.blit(fps_label_surface, fps_label_rect)

        # Draw back button
        back_button.draw(screen)

        # Custom cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(Settings.CURSOR_IMAGE, (mouse_x, mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if toggle_fullscreen_button.is_clicked(event):
                toggle_fullscreen()
                # Update scaling factors and positions after toggling fullscreen
                current_screen_width, current_screen_height = screen.get_size()
                scale_factor_x = current_screen_width / 640
                scale_factor_y = current_screen_height / 480

                # Update button positions
                fps_toggle_button.rect.center = (int(320 * scale_factor_x), int(320 * scale_factor_y))
                back_button.rect.center = (int(320 * scale_factor_x), int(400 * scale_factor_y))
                toggle_fullscreen_button.rect.center = (int(630 * scale_factor_x), int(10 * scale_factor_y))

                # Update labels
                label_rect_fullscreen = label_surface_fullscreen.get_rect(center=(int(475 * scale_factor_x), int(70 * scale_factor_y)))
                fps_label_surface, fps_label_rect = update_fps_label()
            if fps_toggle_button.is_clicked(event):
                Settings.toggle_fps()
                # Update the FPS label to reflect the new state
                fps_label_surface, fps_label_rect = update_fps_label()
            if back_button.is_clicked(event):
                settings_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_running = False

        pygame.display.flip()
        Settings.clock.tick(Settings.FPS)

# Main menu
def main_menu():
    Settings.play_main_menu_music()

    menu_running = True
    while menu_running:
        screen.fill(Settings.BLUE)
        animate_background()

        screen.blit(title_surface, title_rect)
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        # Remove the fullscreen toggle button and label from the main menu

        # Display FPS if enabled
        if Settings.show_fps:
            fps_font = pygame.font.SysFont('Arial', 18)
            fps_text = fps_font.render(f"FPS: {int(Settings.clock.get_fps())}", True, Settings.WHITE)
            screen.blit(fps_text, (10, 10))

        # Custom cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(Settings.CURSOR_IMAGE, (mouse_x, mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                Settings.stop_main_menu_music()
                menu_running = False
            if settings_button.is_clicked(event):
                settings_menu()
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
            # Remove event handling for the fullscreen toggle button

        pygame.display.flip()
        Settings.clock.tick(Settings.FPS)

# Main game loop
def main_game():
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(Settings.BLACK)
        animate_background()

        # Display FPS if enabled
        if Settings.show_fps:
            fps_font = pygame.font.SysFont('Arial', 18)
            fps_text = fps_font.render(f"FPS: {int(Settings.clock.get_fps())}", True, Settings.WHITE)
            screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        Settings.clock.tick(Settings.FPS)

# Start the game
main_menu()
main_game()
