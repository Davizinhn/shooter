# Example file showing a basic pygame "game loop"
import pygame
import random
from playsound import playsound

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
telas = 'menu'

pygame.mixer.music.load('assets/song.wav')

# Set the volume
pygame.mixer.music.set_volume(0.5)
musicvolume = pygame.mixer.music.get_volume()

# Play the music file in an infinite loop
pygame.mixer.music.play(loops=-1)
pygame.display.set_caption('Generic Space Shooter')
# Here we load the image we want to
# use
Icon = pygame.image.load('assets/icon.png')
 
# We use set_icon to set new icon
pygame.display.set_icon(Icon)

playerX = 500
playerY = 590
canMoveL = True
canMoveR = True
canShoot = False
moveSpeed = 10
playerRect = pygame.Rect(playerX,playerY,128,128)
quando = 0
score = 0

class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((16, 32))
            self.image.fill("white")
            self.rect = self.image.get_rect()
            self.rect.x = x+55
            self.rect.y = y

        def update(self):
            if self.rect.y > -200:
                self.rect.y -= 10

bullet_group = pygame.sprite.Group()

class Square(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((70, 16))
            self.image.fill("white")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            if self.rect.y < 720:
                self.rect.y += 4


    # group for squares
square_group = pygame.sprite.Group()

    # game loop
while running:
        musicvolume = pygame.mixer.music.get_volume()
        screen.fill("black")
        if telas == 'game':
            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                    if musicvolume > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)

            # move the player
            if playerX < 0:
                canMoveL=False
            else:
                canMoveL=True

            if playerX+128 > 1280:
                canMoveR=False
            else:
                canMoveR=True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and canMoveL:
                playerX -= moveSpeed
                playerRect.move(playerX, playerY)
            if keys[pygame.K_RIGHT] and canMoveR:
                playerX += moveSpeed
                playerRect.move(playerX, playerY)
            if keys[pygame.K_SPACE] and canShoot:
                canShoot=False
                ch = pygame.mixer.find_channel() # find open channel, returns None if all channels used
                snd = pygame.mixer.Sound('assets/laserShoot.wav')
                snd.set_volume(0.3)
                if (ch): ch.play(snd)
                bullet = Bullet(playerX, playerY)
                bullet_group.add(bullet)
                print('espaço')

            # spawn squares randomly
            if random.randint(0, 85) == 0:
                square_x = random.randint(70, 1190)
                square_y = -50
                square = Square(square_x, square_y)
                square_group.add(square)

            if not canShoot:
                max = 15
                quando+=1
                if quando >= max:
                    quando=0
                    canShoot=True

            # check for collisions
            for square in square_group:
                if square.rect.y > 720:
                    ch = pygame.mixer.find_channel() # find open channel, returns None if all channels used
                    snd = pygame.mixer.Sound('assets/hitHurt.wav')
                    snd.set_volume(0.3)
                    if (ch): ch.play(snd)
                    playerX=500
                    playerY=590
                    canShoot=False
                    canMoveR=True
                    canMoveL=True
                    score=0
                    square_group.empty()
                    bullet_group.empty()
                    telas='menu'
                if not playerRect.colliderect(square.rect):
                    for bullet in bullet_group:
                        squares_hit = pygame.sprite.spritecollide(bullet, square_group, True)
                        if squares_hit:
                            ch = pygame.mixer.find_channel() # find open channel, returns None if all channels used
                            snd = pygame.mixer.Sound('assets/explosion.wav')
                            snd.set_volume(0.3)
                            if (ch): ch.play(snd)
                            score += 1

            # update and draw everything
            playerRect.update(playerX, playerY, playerRect.width, playerRect.height)
            bullet_group.update()
            bullet_group.draw(screen)
            square_group.update()
            square_group.draw(screen)
            pygame.draw.rect(screen, "white", playerRect)

            font = pygame.font.Font("assets/Pixellari.ttf", 95)
            text_surface = font.render(str(score), True, "white")
            # Crie um objeto de superfície de texto

            # Obtenha as dimensões da tela
            screen_width = 1280
            screen_height = 720
            text_width, text_height = text_surface.get_size()
            x = (screen_width - text_width) / 2
            y = 0+15
            screen.blit(text_surface, (x, y))
        if telas=='menu':
            image = pygame.image.load("assets/menu.png")
            screen.blit(image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and not event.key == pygame.K_m:
                    ch = pygame.mixer.find_channel() # find open channel, returns None if all channels used
                    snd = pygame.mixer.Sound('assets/blipSelect.wav')
                    snd.set_volume(0.45)
                    if (ch): ch.play(snd)
                    telas='game'
                elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                    if musicvolume > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)
        pygame.display.flip()
        clock.tick(60)

pygame.mixer.quit()   
pygame.quit()
