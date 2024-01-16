import pygame
from random import randint

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
EXPLOSION_RADIUS = 8
EXPLOSION_MAX_RADIUS = 30
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Intruders")

class Player():
    COLOR = WHITE
    VEL = 3

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.explosions = []
        self.last_explosion_time = 0

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        for explosion in self.explosions:
            explosion.draw(win)

    def move(self, left=True):
        self.x -= self.VEL if left else 0
        self.x += self.VEL if not left else 0

    def move_up_down(self, up=True):
        self.y -= self.VEL if up else 0
        self.y += self.VEL if not up else 0

    def reset(self):
        self.x, self.y = self.original_x, self.original_y
        self.explosions = []

    def explode(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_explosion_time > 1000:
            new_explosion = Explosion(self.x + self.width // 2, self.y + self.height // 2, EXPLOSION_RADIUS, EXPLOSION_MAX_RADIUS)
            self.explosions.append(new_explosion)
            self.last_explosion_time = current_time

class Base():
    COLOR = BLUE

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

class Explosion():
    def __init__(self, x, y, initial_radius, max_radius):
        self.x, self.y = x, y
        self.initial_radius, self.current_radius, self.max_radius = initial_radius, initial_radius, max_radius
        self.color = RED
        self.duration = 120

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.current_radius))

    def update(self):
        if self.current_radius < self.max_radius:
            self.current_radius += (self.max_radius - self.initial_radius) / self.duration
        elif self.duration > 0:
            self.current_radius -= self.max_radius / self.duration
        self.duration -= 1

    def is_complete(self):
        return self.duration <= 0

class Missile():
    COLOR = (255, 165, 0)
    VEL = 1

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = 10, 10

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, down=True):
        self.y += self.VEL if down else 0

def generate_missile():
    x = randint(0, WIDTH - 10)
    y = 0
    return Missile(x, y, 10, 10)

def draw_missiles(win, missiles):
    for missile in missiles:
        missile.draw(win)
        missile.move()

def draw_player(win, player):
    player.draw(win)

def draw_base(win, base):
    base.draw(win)

def movement(keys, player):
    player.move(left=keys[pygame.K_a])
    player.move(left=not keys[pygame.K_d])
    player.move_up_down(up=keys[pygame.K_w])
    player.move_up_down(up=not keys[pygame.K_s])
    if keys[pygame.K_SPACE]:
        player.explode()

def main():
    pygame.mixer.music.load("assets/i_wonder.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    game_loop = True
    clock = pygame.time.Clock()

    player = Player(WIDTH // 2, HEIGHT - 125, PLAYER_WIDTH, PLAYER_HEIGHT)
    base = Base((WIDTH - BASE_WIDTH) // 2, HEIGHT - BASE_HEIGHT, BASE_WIDTH, BASE_HEIGHT)
    
    missiles = []

    while game_loop:
        clock.tick(FPS)

        SCREEN.fill(BLACK)
        draw_base(SCREEN, base)
        draw_player(SCREEN, player)
        draw_missiles(SCREEN, missiles)
        
        if randint(0, 100) < 5:  
            missiles.append(generate_missile())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        for explosion in player.explosions:
            explosion.update()
            if explosion.is_complete():
                player.explosions.remove(explosion)

        for missile in missiles:
            if missile.y >= HEIGHT:
                missiles.remove(missile)

        keys = pygame.key.get_pressed()
        movement(keys, player)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()