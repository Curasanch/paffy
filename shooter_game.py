#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer 

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
# mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.Font('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font('Arial', 36)
font3 = font.Font('Arial', 50)

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = "bullet.png" # пуля
img_asteroid = "ast.png" # астероид

score = 0 # сбито кораблей
goal = 10 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 3 # проиграли, если пропустили столько
life = 3 # счетчик жизней

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# класс спрайта-пули
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed 
        # исчезает, если дойти до края экрана
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(90, win_width - 90) 
            self.rect.y = 0

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()


asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 50, 50, randint(5, 10))
    asteroids.add(asteroid)



# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна

def setColor():
    text_color = (0,0,0)
    if life == 3:
        text_color = (0,255,0)
    elif life == 2:
        text_color = (0,255,255)
    elif life == 1:
        text_color = (255,0,0)
    return text_color

rel_time = False # флаг, отвечающий за перезарядку
num_fire = 0 # переменная для подсчёта выстрелов

while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # проверим, сколько выстрелов сделано и не происходит ли перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False: # если игрок сделал 5 выстрелов
                    last_time = timer() # засекаем время
                    rel_time = True

               



    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_color = setColor()
        text_life = font3.render(str(life), 1, text_color)
        window.blit(text_life, (win_width - 50, 10))

        # производим движения спрайтов
        ship.update()
        monsters.update() 
        bullets.update()
        asteroids.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window) 
        bullets.draw(window)
        asteroids.draw(window)

        # перезарядка
        if rel_time == True:
            now_time = timer() # считываем время

            if now_time - last_time < 3: # пока не пропало 3 секунды выводим информацию о перезарядке
                reload = font2.render('Wait, reload...', 1 ,(150,0,0))
                window.blit(reload, (260, 460))
            else: 
                num_fire = 0 # обнуляем счётчик пуль
                rel_time = False # сбрасываем флаг перезарядки


        # проверка столкновения пули и монстров( и монстр, и пули при касании исчезает)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повтортся столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # возможный проигрыш: пропустили слишком много или гурой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, True) or lost>= max_lost or sprite.spritecollide(ship, asteroids, True):
            life -= 1

        if lost >= max_lost or life == 0:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами
            window.blit(lose, (200, 200))

        # проверка выиграша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
 
            display.update()
        else:
            finish = False
            score = 0
            lost = 0
            life = 3

            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for ast in asteroids:
                ast.kill()
            
            time.delay(3000) # временная задержка

            for i in range(1, 6):
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

            for i in range(2):
                asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 50, 50, randint(5, 10))
                asteroids.add(asteroid)

    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)

