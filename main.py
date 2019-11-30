import pygame
import os
import random

# Constants
WIDTH = 600
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


# Background sprite
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "background.jpg")).convert()
        self.image = pygame.transform.scale(self.image, (600, 800))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


# Player sprite
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_front.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 2
        self.speed = 0

    def update(self):
        # If sprite has moved out of window, get it back
        if self.rect.left > WIDTH:
            self.rect.right = 0

        if self.rect.right < 0:
            self.rect.left = WIDTH

        # Movement
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            if self.speed > -5:
                self.speed -= 1
        elif pressed[pygame.K_d]:
            if self.speed < 5:
                self.speed += 1
        else:
            if self.speed < 0:
                self.speed += 1
            if self.speed > 0:
                self.speed -= 1

        self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "blockerMad.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(-100, -40)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.fallingspeed = random.randint(1, 6)

    def update(self):
        self.rect.y += self.fallingspeed
        if self.rect.top > HEIGHT:
            self.rect.bottom = random.randint(-100, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.fallingspeed = random.randint(1, 6)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "fire.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.bspeed = -5

    def update(self):
        self.rect.y += self.bspeed
        if self.rect.bottom < 0:
            self.kill()


# Initial setup
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.init()
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Green guy in a weird simulation - The Game")
clock = pygame.time.Clock()

points = 0
background = Background()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
got_hit = False

# Game Loop
running = True
while running:
    # Clock ticks
    clock.tick(FPS)
    while len(mobs) < 8:
        mob = Mob()
        mobs.add(mob)
        all_sprites.add(mob)

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()

    # Collision detection
    # Mob - player detection
    collisions = pygame.sprite.spritecollide(player, mobs, False)
    if collisions:
        running = False
        got_hit = True
    # Bullet - mob detection
    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
        points += 100


    # Render
    gameWindow.fill(BLACK)
    gameWindow.blit(background.image, background.rect)
    all_sprites.draw(gameWindow)
    textsurface = myfont.render(str(points), False, (155, 155, 215))
    gameWindow.blit(textsurface, (0, 0))
    pygame.display.flip()


# Player lost, display final message and quit
if got_hit:
    got_enter = False
    while not got_enter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                got_enter = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    got_enter = True
        textsurface2 = myfont.render("Game over!", False, (255, 255, 255))
        gameWindow.blit(textsurface2, ((WIDTH-150)/2, (HEIGHT-55)/2))
        pygame.display.flip()

pygame.quit()
