import sys
import random
import euclid3
import pygame
from pygame.locals import *


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
FPS = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

GRAVITY = 1

class Rover(pygame.sprite.Sprite):
    def __init__(self, size=(50, 20), x=None, y=None, color=BLACK):
        super().__init__()
        self.x = x
        self.y = y
        if not self.x: self.x = random.randint(size[0]//2, SCREEN_WIDTH - size[0]//2)
        if not self.y: self.y = random.randint(size[1]//2, SCREEN_HEIGHT - size[1]//2)
        self.position = euclid3.Vector2(self.x, self.y)
        self.velocity = euclid3.Vector2(1, 0)
        self.size = size
        self.color = color

        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.rover = self.surf.get_rect(center=(self.x, self.y))

    def update(self, dt):
        # Handle key presses
        pressed_keys = pygame.key.get_pressed()
        if self.rover.left > 0:
            if pressed_keys[K_LEFT]:
                self.rover.move_ip(-5, 0)
        if self.rover.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rover.move_ip(5, 0)
        
        # Handle gravity
        self.position += self.velocity * dt

    def display(self, surface):
        surface.blit(self.surf, self.rover)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Martian Rover")

rover = Rover()
game_over = False
while not game_over:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    clock_ms = clock.tick(FPS)
    dt = clock_ms / 1000.0
    rover.update(dt)
    screen.fill(WHITE)
    rover.display(screen)

    pygame.display.update()