import os
import sys
import math
import random
import pygame

WIDTH = 623
HEIGHT = 150

# Создание окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Jumping Dino")

class Scale: # Счет

     def __init__(self): # Инициализация
          self.p = 0
          self.font = pygame.font.SysFont('Times New Roman', 20, bold=True)
          self.color = (0, 0, 0)
          self.show()
        
     def update(self, point): # Обновление очков
          self.p = point
          
     def show(self): # Показ счета
          self.lbl = self.font.render(f'{self.p}', 1, self.color)
          lbl_width = self.lbl.get_rect().width
          screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

     def point(self, obj1, obj2): # Сравнение координаты
          distance = abs(obj1.x - obj2.x)
          if (distance < 2):
               return 0
          return 1
    
class Collision: # Коллизия объектов
    
    def beetween(self, obj1, obj2): # Столкновение объектов
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 35
    
class Rock: # Камень
    
    def __init__(self, x): # Инициализация
        self.width = 45
        self.height = 50
        self.x = x
        self.y = 83
        self.set_texture()
        self.show()

    def update(self, dx): # Анимация камня
        self.x += dx

    def show(self): # Показ камня
        screen.blit(self.texture, (self.x, self.y))
        
    def set_texture(self): # Добавление изображения камня
        path = os.path.join('assets/images/rock.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Dino: # Динозаврик
    
    def __init__(self): # Инициализация
        self.width = 44
        self.height = 47
        self.x = 20
        self.y = 80
        self.texture_num = 0 # Начальное положение динозаврика
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 10 # Высота прыжка
        self.falling = False
        self.fall_stop = self.y # Длина прыжка
        self.set_texture()
        self.show()
        
    def update(self, loops): # Анимация динозаврика
        # Динозаврик прыгает
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()      
        # Динозаврик идет
        if loops % 10 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()
    
    def show(self): # Показ динозаврика
        screen.blit(self.texture, (self.x, self.y))
    
    def set_texture(self): # Добавление изображения динозаврика
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        
    # Функции для правильной анимации динозаврика в прыжке
    def jump(self):
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True
        
class BG: # Фон

    def __init__(self, x): # Инициализация
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx): # Обновление координат, анимация фона
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self): # Показ
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self): # Добавление изображения фона
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Game: # Игра
    
    def __init__(self): # Инициализация
        self.bg = [BG(x = 0), BG(x = WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.collision = Collision()
        self.scale = Scale()
        self.speed = 3
        self.playing = False
        self.set_labels()

    def set_labels(self): # Текст после конца игры
        big_font = pygame.font.SysFont('Times New Roman', 30, bold=True)
        small_font = pygame.font.SysFont('Times New Roman', 15)
        self.big_lbl = big_font.render(f'G A M E  O V E R', 1, (192, 0, 0))
        self.small_lbl = small_font.render(f'press -f- to restart', 1, (0, 213, 0))
        
    def start(self): # Начало игры
        self.playing = True
        
    def over(self): # Конец игры
        screen.blit(self.big_lbl, (WIDTH // 2 - self.big_lbl.get_width() // 2, HEIGHT // 6))
        screen.blit(self.small_lbl, (WIDTH // 2 - self.small_lbl.get_width() // 2, HEIGHT // 2.5))
        self.playing = False
        
    def restart(self): # Рестарт игры
        self.__init__()

    # Добавление камней  
    def tospawn(self, loops):
        return loops % 100 == 0
    
    def spawn_rock(self):
        # Список с камнями
        if len(self.obstacles) > 0:
            prev_rock = self.obstacles[-1]
            x = random.randint(prev_rock.x + self.dino.width + 84, WIDTH + prev_rock.x + self.dino.width + 84)
        # Пустой список
        else:
            x = random.randint(WIDTH + 100, 1000)
        # Новый камень
        rock = Rock(x)
        self.obstacles.append(rock)

def main():
     # Объекты 
     game = Game()
     dino = game.dino
     # Параметры
     clock = pygame.time.Clock()
     loops = 0
     over = False
     point = 0
     # Основной цикл
     while True:
          if game.playing:
               loops += 1
               # Фон
               for bg in game.bg: 
                    bg.update(-game.speed)
                    bg.show()

               # Динозаврик
               dino.update(loops)
               dino.show()

               # Камень
               if game.tospawn(loops):
                    game.spawn_rock()
               for rock in game.obstacles:
                    rock.update(-game.speed)
                    rock.show()
                    # Коллизия
                    if game.collision.beetween(dino, rock):
                         game.over()
                         over = True
                     # Счет
                    if game.scale.point(dino, rock) == 0:
                         point += 1
                         game.scale.update(point)
               game.scale.show()
          # События
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
               # Прыжок - пробел
               if event.type == pygame.KEYDOWN:
                    if over == False:
                         if event.key == pygame.K_SPACE:
                              if dino.onground:
                                   dino.jump()
                              if not game.playing:
                                   game.start()
                    # Рестарт игры - f
                    if event.key == pygame.K_f:
                         game.restart()
                         dino = game.dino
                         loops = 0
                         over = False
                         point = 0
                        
          clock.tick(100) # Ограничение скорости передвижения фона
          pygame.display.update()

main()
