import pygame
from os.path import join
from random import randint, uniform

#Classes

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Images','spaceship.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(screen_w/2,screen_h/2))

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self,dt):
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 500

        #Player Movement

        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        justonce_keys = pygame.key.get_just_pressed()

        #Shooting Lasers

        if justonce_keys[pygame.K_SPACE] and self.can_shoot:
            Bullets(bullet,self.rect.midtop, (sprites,bullets_group))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,screen_w),randint(0,screen_h)))

class Meteors(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.og_image = surf
        self.image = surf
        self.rect = self.image.get_frect(midtop = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 10000
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(100,200)
        self.rotation_speed = randint(20,50)
        self.rotation = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.og_image,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Bullets(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self,dt):
        self.rect.centery -= 1000*dt
        if self.rect.bottom < 0:
            self.kill()

def collisons():
    global running
    if pygame.sprite.spritecollide(player,meteors_group,True,pygame.sprite.collide_mask):
        running = False
    #pygame.sprite.groupcollide(bullets_group,meteors_group,True,True)
    for shotbullet in bullets_group:
        collision = pygame.sprite.spritecollide(shotbullet,meteors_group,True,pygame.sprite.collide_mask)
        if collision:
            shotbullet.kill()

def display_score():
    current_time=pygame.time.get_ticks()
    score = font.render(str(current_time),True,'white')
    scorect = score.get_frect(midbottom = (75,50))
    screen.blit(score,scorect)
    pygame.draw.rect(screen,'white',scorect.inflate(20,15 ),2,10)

pygame.init()

screen_w = 1000
screen_h = 600
screen = pygame.display.set_mode((screen_w,screen_h))
screen_color = 'Midnight Blue'
clock = pygame.time.Clock()

pygame.display.set_caption("Game One: Space Shooter")
icon = pygame.image.load(join('images','xwing.png')).convert_alpha()
pygame.display.set_icon(icon)
font = pygame.font.Font(None, 50)

#Bullet
bullet = pygame.image.load(join('images','bullet1.png')).convert_alpha()
#Meteor
meteor = pygame.image.load(join('images','meteor.png')).convert_alpha()

#Events
#Meteor
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500 )

#Calling All Sprites
sprites = pygame.sprite.Group()
meteors_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
stars = pygame.image.load(join('Images','star.png')).convert_alpha()
for i in range(100):
    Stars(sprites,stars)
player = Player(sprites)


running = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteorx = randint(0,screen_w)
            meteory = randint(-200,-100)
            Meteors(meteor,(meteorx,meteory), (sprites,meteors_group))
    
    screen.fill(screen_color)
    
#Drawing Things
    sprites.draw(screen)
    
    sprites.update(dt)
    collisons()
    display_score()

    pygame.display.update()

pygame.quit()