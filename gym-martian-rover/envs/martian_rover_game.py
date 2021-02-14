import sys
import random
import pygame
from pygame.locals import *

vec = pygame.math.Vector2
pygame.init()

RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
ORANGE = pygame.Color(175, 99, 0)
FPS = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
ROVER_ACC = 1
FRICTION = -0.05
GRAVITY = vec(0.0, 0.5)

font = pygame.font.SysFont("Verdana", 60)
goal_met = font.render("Goal met", True, RED)

class Goal(pygame.sprite.Sprite):
    def __init__(self, size=(100, 100), x=300, y=SCREEN_HEIGHT // 2):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = vec(x, y)
        self.color = RED

    def didContact(self, xCoord, yCoord):
        xIntersect = (self.position.x - self.width // 2) < xCoord < (self.position.x + self.width // 2)
        yIntersect = (self.position.y - self.height // 2) < yCoord < (self.position.y + self.height // 2)
        return xIntersect and yIntersect


class Rover(pygame.sprite.Sprite):
    def __init__(self, size=(50, 20), color=WHITE):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width, self.height = size
        #self.rect.center = (self.width / 2, self.height / 2)
        self.pos = vec(7 * SCREEN_WIDTH // 8, SCREEN_HEIGHT // 4)
        self.vel = vec(0, 0)
        self.acc = GRAVITY
        self.width, self.height = size
        self.color = color

    def update(self, action=None):
        # 0 is left and 1 is right
        # Handle key presses
        self.acc = vec(GRAVITY.x, GRAVITY.y)
        if action is None:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.acc.x -= ROVER_ACC
            elif pressed_keys[K_RIGHT]:
                self.acc.x += ROVER_ACC
        else:
            if action == 0:
                self.acc.x -= ROVER_ACC
            else:
                self.acc.x += ROVER_ACC

        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos


class LandScape(pygame.sprite.Sprite):
    def __init__(self, w=600, h=200):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200


class RoverGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Martian Rover")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(BLACK)

        self.all_sprites = pygame.sprite.Group()
        self.landscape_sprites = pygame.sprite.Group()
        self.goal_sprites = pygame.sprite.Group()

        self.rover = Rover()
        self.all_sprites.add(self.rover)

        self.goal = Goal(size=(5, 50))
        self.all_sprites.add(self.goal)
        self.goal_sprites.add(self.goal)

        self.landscape = LandScape()
        self.all_sprites.add(self.landscape)
        self.landscape_sprites.add(self.landscape)

        self.running = True
        self.success = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self, human=False, action=None):
        self.all_sprites.update(action=action)
        hits = pygame.sprite.spritecollide(self.rover, self.landscape_sprites, False)
        if hits:
            self.rover.pos.y = hits[0].rect.top + 1
            self.rover.vel.y = 0

        hits = pygame.sprite.spritecollide(self.rover, self.goal_sprites, False)
        if hits and abs(self.rover.vel.x) < 0.5:
            self.running = False
            self.success = True

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        return None

    def reset(self):
        pass


# g = Game()
# g.run()
