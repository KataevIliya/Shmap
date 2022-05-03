""" Игра-стрелялка"""
' Импорты библиотек и создание основных переменных'
# Импорт самой главной библиотеке в этой программе
import pygame
# Не такие важные библиотеки, но необходимые моей программе
# (вы можете их не использовать)
import time
import random
import os
from os import path

# Создание основных переменных (для начинающих программистов)
v = 0
yrt = True
k = 0
a = 0
# Параметры окна
WIDTH = 480
HEIGHT = 600
# кадры/сек
FPS = 60
# Задаем цвета
B = (76, 105, 113)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Библиотека в которой мы будем хранить изображения
FILE0 = os.path.abspath(os.curdir)
img_dir = FILE0 + '/img'

# Получаем данные
s = int(input("Введите уровень сложности от 1 до 3 (можно и больше)"))
# Здесь мы умножаем уровень сложности на 8 - это будет количество астероидов
# noinspection PyRedeclaration
v = s * 8
# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # Я в своей программе не использовал, инструмент для создания
# и проигрывания звуков и музыки
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Параметры экрана
pygame.display.set_caption("Shmup!")  # Название
clock = pygame.time.Clock()  # Clock - это инструмент, способный держать игровой
# цикл на правильных FPS
# Здесь мы создаём объекты pygame.Surface - поверхности с картинками
# Фон
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
# Пули
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
# От разработчика (чтобы каждую игру менялся корабль)
# Получаем случайное число (1,2,3,4,5,6,7 или 8)
i = random.randrange(1, 9)
# проверяем (это число 1?)
if i == 1:
    # Если да, то загружаем эту картинку
    player_img = pygame.image.load(path.join(img_dir, "playerShip1_green.png")).convert()
elif i == 2:
    player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
elif i == 3:
    player_img = pygame.image.load(path.join(img_dir, "playerShip2_blue.png")).convert()
elif i == 4:
    player_img = pygame.image.load(path.join(img_dir, "playerShip2_orange.png")).convert()
elif i == 5:
    player_img = pygame.image.load(path.join(img_dir, "playerShip2_red.png")).convert()
elif i == 6:
    player_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
elif i == 7:
    player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()
else:
    player_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert()


# создаём спрайт игрока
class Player(pygame.sprite.Sprite):  # Указываем, к какому классу он относится
    # инициализация
    def __init__(self):
        # инициализация как pygame спрайт
        pygame.sprite.Sprite.__init__(self)
        # радиус "действия" спрайта (на каком расстоянии его смогут задевать астероиды)
        self.radius = 20
        # изменяем размеры изображения
        self.image = pygame.transform.scale(player_img, (50, 38))
        # его размеры
        self.rect = self.image.get_rect()
        # на некоторых изображениях присутствует прозрачность, но когда программа их считывает,
        # прозрачные пиксели заменяются чёрными (BLACK) или светло-серымы (B) нам необходимо их убрать
        self.image.set_colorkey(B)
        self.image.set_colorkey(BLACK)
        # координаты
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        # скорость по X
        self.speedx = 0
        # скорость по Y
        self.speedy = 0

    # действия на каждом кадре
    def update(self):
        # обновляем скорость
        self.speedx = 0
        self.speedy = 8
        # включить клавиатуру
        keystate = pygame.key.get_pressed()
        # проверяем игровые клавиши: стрелка влево, вправо, вверх (вниз он должен двигаться всегда)
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        # изменяем его координаты (спрайт двигается)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # не даём игроку выйти за экран
        if self.rect.right > WIDTH + 45:
            self.rect.right = WIDTH + 45
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    # стрельба
    def shoot(self):
        bullet = Bullet(self.rect.centerx - 25, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# спрайт астероида
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        p = random.randrange(1, 9)
        if p == 1:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_big1.png")).convert()
        elif p == 2:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_big2.png")).convert()
        elif p == 3:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_big3.png")).convert()
        elif p == 4:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_big4.png")).convert()
        elif p == 5:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorGrey_big1.png")).convert()
        elif p == 6:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorGrey_big2.png")).convert()
        elif p == 7:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorGrey_big3.png")).convert()
        else:
            meteor_img = pygame.image.load(path.join(img_dir, "meteorGrey_big4.png")).convert()
        y = random.randrange(40, 76)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteor_img, (y, y))
        self.image.set_colorkey(B)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.speedy += k
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    # функция f убивает астероид
    def f(self):
        self.kill()


# спрайт пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Теперь, кроме системного элемента self необходимо дать x и y, т. к.
        # пуля появляется не в одном и том же месте
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (7, 15))
        self.image.set_colorkey(B)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

    '''
    также необходимо в спрайт игрока добавить функцию стрельбы
    def shoot(self):
        bullet = Bullet(self.rect.centerx - 25, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
    '''


# создаём группы
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
# экземпляр класса Player
player = Player()
all_sprites.add(player)
# создаём нужное количество астероидов
for i in range(v):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    # Проверка, не ударил ли моб игрока (последний за отталкивание False)
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    if hits:
        running = False

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    # заменяем
    for hit in hits:
        a += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
print("Ваши очки:", a)
time.sleep(3)
