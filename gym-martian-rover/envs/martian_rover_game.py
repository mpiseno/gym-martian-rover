import sys
import random
import euclid3
import pygame
from pygame.locals import *

pygame.init()

RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
FPS = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
font = pygame.font.SysFont("Verdana", 60)

goal_met = font.render("Goal met", True, RED)

GRAVITY = 1
class Goal(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        size = (100, 100)
        self.width = size[0]
        self.height = size[1]
        if not x: x = SCREEN_WIDTH-self.width//2
        if not y: y = SCREEN_HEIGHT-self.height//2


        self.position = euclid3.Vector2(x, y);
        self.color = RED

    def display(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position.x - self.width // 2, self.position.y - self.height // 2, self.width, self.height)
        )

    def didContact(self, xCoord, yCoord):
        xIntersect = (self.position.x - self.width // 2) < xCoord < (self.position.x + self.width // 2)
        yIntersect = (self.position.y - self.height // 2) < yCoord < (self.position.y + self.height // 2)
        return xIntersect and yIntersect

class Rover(pygame.sprite.Sprite):
    def __init__(self, size=(50, 20), x=None, y=None, color=BLACK):
        super().__init__()
        if not x: x = random.randint(size[0]//2, SCREEN_WIDTH - size[0]//2)
        if not y: y = random.randint(size[1]//2, SCREEN_HEIGHT - size[1]//2)
        self.position = euclid3.Vector2(x, y)
        self.velocity = euclid3.Vector2(15, 0)
        self.width, self.height = size
        self.color = color

        #self.surf = pygame.Surface(self.size)
        #self.surf.fill(self.color)
        #self.rover = self.surf.get_rect(center=(self.x, self.y))

    def update(self, dt):
        # Handle key presses
        pressed_keys = pygame.key.get_pressed()
        if self.position.x > self.width // 2 and pressed_keys[K_LEFT]:
            self.position.x = max(0, self.position.x - 5)
        elif self.position.x < SCREEN_WIDTH - self.width // 2 and pressed_keys[K_RIGHT]:
            self.position.x = min(SCREEN_WIDTH, self.position.x + 5)
        
        # Handle gravity
        print(self.position)
        self.position += self.velocity * dt
        #self.rover.position = self.position

    def display(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position.x - self.width // 2, self.position.y - self.height // 2, self.width, self.height)
        )
        #surface.blit(self.surf, self.rover)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Martian Rover")

goal = Goal(y=100)
rover = Rover(y=100)
game_over = False
while not game_over:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # if pygame.sprite.spritecollideany(rover, goal):
    if goal.didContact(rover.position.x - rover.width // 2, rover.position.y - rover.height // 2):
        screen.blit(goal_met, (100, 100))
        pygame.display.update()
        # pygame.time.sleep(2)
        pygame.quit()
        sys.exit()

    clock_ms = clock.tick(FPS)
    dt = clock_ms / 1000.0
    rover.update(dt)
    screen.fill(WHITE)
    rover.display(screen)
    goal.display(screen)
    pygame.display.update()