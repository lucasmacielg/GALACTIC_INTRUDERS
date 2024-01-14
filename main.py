import pygame
import random

pygame.init()

FPS = 60

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (63, 72, 204)

FONT = pygame.font.Font(None, 40)

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 10
BASE_WIDTH, BASE_HEIGHT = 400, 80
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Intruders")

class Missiles():
    pass

class Player():  
    COLOR = WHITE
    VEL = 8

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, left=True):
        if left:
            self.x -= self.VEL
        else:
            self.x += self.VEL

    def move_up_down(self, up=True):
        if up:
            self.y -= self.VEL
        if not up:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Base():
    COLOR = BLUE
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

def draw_player(win, player):
    player.draw(win)

def draw_base(win, base):
    base.draw(win)

def movement(keys, player):
    if keys[pygame.K_a] and player.x - player.VEL >= 0:
        player.move(left=True)
    if keys[pygame.K_d] and player.x + player.width + player.VEL <= WIDTH:
        player.move(left=False)
    if keys[pygame.K_w] and player.y - player.VEL >= 0:
        player.move_up_down(up=True)
    if keys[pygame.K_s] and player.y + player.height + player.VEL <= HEIGHT - 80:
        player.move_up_down(up=False)
        

pygame.mixer.music.load("assets/i_wonder.wav")
pygame.mixer.music.set_volume(0.3)

def main():
    pygame.mixer.music.play(-1)
    game_loop = True
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT - 125, PLAYER_WIDTH, PLAYER_HEIGHT)
    base = Base((WIDTH - BASE_WIDTH) // 2, HEIGHT - BASE_HEIGHT, BASE_WIDTH, BASE_HEIGHT)
    lost = False
    restart_text_font = pygame.font.Font(None, 20)
    restart_text = restart_text_font.render("PRESS SPACE TO RESTART", True, WHITE)

    victory = False

    while game_loop:
        clock.tick(FPS)

        game_over = False
        if not lost:
            SCREEN.fill(BLACK)
            draw_base(SCREEN, base)
            draw_player(SCREEN, player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False

            keys = pygame.key.get_pressed()
            movement(keys, player)

            if game_over:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                pygame.display.update()
                lost = True

            if victory:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                win_text = 'YOU WIN!'
                SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
                text = FONT.render(win_text, True, WHITE)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))
                pygame.display.update()
                pygame.time.delay(3000)

            if lost:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
                text = FONT.render("YOU LOST!", True, WHITE)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))
                pygame.display.update()

                space_pressed = False
                while not space_pressed:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_loop = False
                            space_pressed = True
                            pygame.mixer.pause()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                pygame.mixer.pause()
                                pygame.display.update()
                                lost = False
                                space_pressed = True

        pygame.display.update()

if __name__ == '__main__':
    main()
