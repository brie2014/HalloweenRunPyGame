import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Witch/MayaRun00.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.4)
        player_walk_2 = pygame.image.load('graphics/Witch/MayaRun01.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.4)
        player_walk_3 = pygame.image.load('graphics/Witch/MayaRun02.png').convert_alpha()
        player_walk_3 = pygame.transform.rotozoom(player_walk_3, 0, 0.4)
        player_walk_4 = pygame.image.load('graphics/Witch/MayaRun03.png').convert_alpha()
        player_walk_4 = pygame.transform.rotozoom(player_walk_4, 0, 0.4)
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Witch/Jump.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(self.player_jump, 0, 0.4)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2, GROUND_HEIGHT))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    # Function to handle input for the player (jumping)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_HEIGHT:
            self.gravity = -20
            self.jump_sound.play()

    # Function to adjust the player gravity
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT

    # Function to animate the player
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # Function to call the other methods and update the player
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        if name == 'bat':
            bat_frame_1 = pygame.image.load('graphics/Bat/bat-1.png').convert_alpha()
            bat_frame_1 = pygame.transform.flip(bat_frame_1, True, False)
            bat_frame_2 = pygame.image.load('graphics/Bat/bat-2.png').convert_alpha()
            bat_frame_2 = pygame.transform.flip(bat_frame_2, True, False)
            bat_frame_3 = pygame.image.load('graphics/Bat/bat-3.png').convert_alpha()
            bat_frame_3 = pygame.transform.flip(bat_frame_3, True, False)
            bat_frame_4 = pygame.image.load('graphics/Bat/bat-4.png').convert_alpha()
            bat_frame_4 = pygame.transform.flip(bat_frame_4, True, False)
            bat_frame_5 = pygame.image.load('graphics/Bat/bat-5.png').convert_alpha()
            bat_frame_5 = pygame.transform.flip(bat_frame_5, True, False)
            self.frames = [bat_frame_1, bat_frame_2, bat_frame_3, bat_frame_4, bat_frame_5]
            y_pos = 250
        elif name == 'pumpkin':
            pumpkin_frame_1 = pygame.image.load('graphics/Pumpkin/jack1.png').convert_alpha()
            pumpkin_frame_2 = pygame.image.load('graphics/Pumpkin/jack2.png').convert_alpha()

            self.frames = [pumpkin_frame_1, pumpkin_frame_2]
            y_pos = GROUND_HEIGHT
        else:
            skull_frame_1 = pygame.image.load('graphics/Skull/frame-1.png').convert_alpha()
            skull_frame_2 = pygame.image.load('graphics/Skull/frame-2.png').convert_alpha()
            self.frames = [skull_frame_1, skull_frame_2]
            y_pos = GROUND_HEIGHT
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    # Function to animate the obstacle
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # Function to destroy the obstacle once it moves off screen
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    # Function to call the other methods and update the obstacle
    def update(self):
        self.animation_state()
        time_elapsed = pygame.time.get_ticks() - start_time
        # Progressively move faster and faster
        self.rect.x -= 6 + time_elapsed/2000
        self.destroy()


# Function to display the score and high score on the screen. Returns the elapsed time for the game
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'Score: {current_time}', False, text_color)
    score_rect = score_surf.get_rect(midright=(SCREEN_WIDTH-50, 50))
    screen.blit(score_surf, score_rect)

    high_score_surf = test_font.render(f'High Score: {high_score}', False, text_color)
    high_score_rect = score_surf.get_rect(midleft=(50, 50))
    screen.blit(high_score_surf, high_score_rect)
    return current_time


# Function to check for a collision. Returns True if the player has collided with an obstacle
def collision_check():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return True
    else:
        return False


# Game Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 350
text_color = 'White'

# Initialize the frame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the game title
pygame.display.set_caption('Halloween Run')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
high_score = 0

# Timers
clock = pygame.time.Clock()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Background Image & Music
sky_surf = pygame.image.load('graphics/SpookyBackground.png').convert()
bg_music = pygame.mixer.Sound('audio/spooky.wav')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

# Player and Obstacle Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Intro Screen Graphics
player_stand = pygame.image.load('graphics/Witch/Stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 0.7)
player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

game_name = test_font.render('Halloween Run', False, text_color)
game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH/2, 80))

game_message = test_font.render('Press space to run', False, text_color)
game_message_rect = game_message.get_rect(center=(SCREEN_WIDTH/2, 340))

while True:
    # Event Loop--handles game events
    for event in pygame.event.get():
        # Closing the window ends the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Pressing space bar starts the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_active:
            game_active = True
            start_time = pygame.time.get_ticks()
        # If the game is started, add obstacles
        if game_active:
            if event.type == obstacle_timer and game_active:
                obstacle_group.add(Obstacle(choice(['bat', 'pumpkin', 'skull', 'skull'])))

    # What we show if the game is being played
    if game_active:
        # BACKGROUND AND SCORE
        screen.blit(sky_surf, (0, 0))
        score = display_score()

        # PLAYER
        player.draw(screen)
        player.update()

        # OBSTACLES
        obstacle_group.draw(screen)
        obstacle_group.update()

        # COLLISIONS
        game_active = not collision_check()
        if score > high_score:
            high_score = score

    # What we show before and after the game is being played
    else:
        # BACKGROUND AND GAME NAME
        player_gravity = 0
        screen.blit(sky_surf, (0, 0))
        screen.blit(game_name, game_name_rect)

        # PLAYER
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your Score: {score}', False, text_color)
        score_message_rect = score_message.get_rect(center=(SCREEN_WIDTH / 2, 330))

        high_score_message = test_font.render(f'High Score: {high_score}', False, text_color)
        high_score_message_rect = score_message.get_rect(center=(SCREEN_WIDTH / 2, 370))

        # SCORE/MESSAGE
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(high_score_message, high_score_message_rect)

    # UPDATE EVERYTHING
    pygame.display.update()

    # This game should only run up to 60 times per second (60 FPS)
    clock.tick(60)
