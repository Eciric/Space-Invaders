import pygame
import random
# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initial setup
pygame.init()
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


# Objects
class HeadBlock(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

    def update(self):
        # If sprite has moved out of window, get it back
        if self.rect.left > WIDTH:
            self.rect.right = 0

        if self.rect.right < 0:
            self.rect.left = WIDTH

        # Movement
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            self.rect.x -= 5
        elif pressed[pygame.K_d]:
            self.rect.x += 5
        elif pressed[pygame.K_w]:
            self.rect.y -= 5
        elif pressed[pygame.K_s]:
            self.rect.y += 5

class TailBlock(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)


class Fruit(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = random.randint(0, HEIGHT - 20)


# Variables
all_sprites = pygame.sprite.Group()
head = HeadBlock()
fruit = Fruit()
all_sprites.add(head)
all_sprites.add(fruit)
# Game Loop
running = True
while running:
    # Clock ticks
    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # Render
    gameWindow.fill(BLACK)
    all_sprites.draw(gameWindow)
    pygame.display.flip()


pygame.quit()
