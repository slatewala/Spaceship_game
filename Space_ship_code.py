import pygame
import sys
import random


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load('spaceship_charged.png')

        self.image = self.uncharged
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.shield_surface = pygame.image.load('shield.png')
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_health()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10 + index * 40, 10))

    def damage(self, damage_amount):
        self.health -= damage_amount

    def charge(self):
        self.image = self.charged

    def discharge(self):
        self.image = self.uncharged


class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed

        if self.rect.centery <= -100:
            self.kill()


def main_game():
    global laser_active
    # group draw
    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteor_group.draw(screen)

    # group update
    laser_group.update()
    spaceship_group.update()
    meteor_group.update()

    # collisions
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.damage(1)

    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteor_group, True)

    # laser timer
    if pygame.time.get_ticks() - laser_timer >= 1000:
        laser_active = True
        spaceship_group.sprite.charge()

    return 1


def end_game():
    text_surface = game_font.render('Game Over', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(640, 340))
    screen.blit(text_surface, text_rect)

    score_surface = game_font.render(f'Score : {score}', True, (255, 255, 255))
    score_rect = text_surface.get_rect(center=(640, 380))
    screen.blit(score_surface, score_rect)


pygame.init()  # initiate pygame
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))  # create display
pygame.display.set_caption('Spaceship shooter')  # captions
clock = pygame.time.Clock()  # clock object
pygame.mouse.set_visible(False)
game_font = pygame.font.Font('LazenbyCompSmooth.ttf', 40)
score = 0
laser_timer = 0
laser_active = False

# spaceship
spaceship = Spaceship('spaceship.png', 640, 500)
spaceship_group = pygame.sprite.GroupSingle(spaceship)
spaceship_group.add(spaceship)

# meteor
meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 150)

# laser
laser_group = pygame.sprite.Group()

while True:  # game loop
    for event in pygame.event.get():  # check events / player input
        if event.type == pygame.QUIT:  # close game
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            new_laser = Laser('Laser.png', event.pos, 15)
            laser_group.add(new_laser)
            laser_active = False
            laser_timer = pygame.time.get_ticks()
            spaceship_group.sprite.discharge()

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
            spaceship_group.sprite.health = 5
            meteor_group.empty()
            score = 0

        if event.type == METEOR_EVENT:
            meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
            random_x_pos = random.randint(0, 1280)
            random_y_pos = random.randint(-500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(4, 10)
            meteor = Meteor(meteor_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
            meteor_group.add(meteor)

    # screen fill
    screen.fill((42, 45, 51))
    if spaceship_group.sprite.health > 0:
        score += main_game()
    else:
        end_game()

    pygame.display.update()  # draw frame
    clock.tick(120)  # control the framerate
