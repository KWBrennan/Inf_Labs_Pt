import math
from random import choice
import random

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600




class Target:
   
    def __init__(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 10
        x = self.x = random.randint(600, 740)
        y = self.y = random.randint(60, 540)
        r = self.r = random.randint(30, 50)
        vx = self.vx = random.randint(-7, 7)
        vy = self.vy = random.randint(-7, 7)
        color = self.color = RED

    def new_target(self):
        """
        Инициализация еще более новой цели.
        """
        self.live = 10
        x = self.x = random.randint(600, 780)
        y = self.y = random.randint(300, 500)
        r = self.r = random.randint(30, 50)
        vx = self.vx = random.randint(-7, 7)
        vy = self.vy = random.randint(-7, 7)
        color = self.color = YELLOW

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            RED,
            (self.x, self.y),
            self.r
        )

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.vx - self.r < 500:
            self.vx = -self.vx
        elif self.y - self.vy - self.r < 0:
            self.vy = - self.vy
        elif self.x + self.vx + self.r > WIDTH:
            self.vx = -self.vx
        elif self.y - self.vy + self.r > HEIGHT:
            self.vy = -self.vy
               
            
class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # +-FIXME 
        self.vy -= 0.6
        self.vx -= 0.03
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.vx - self.r < 0:
            self.vx = -self.vx + 0.002 * self.vx
        elif self.y - self.vy - self.r < 0:
            self.vy = - self.vy - 0.002 * self.vy
        elif self.x + self.vx + self.r > WIDTH:
            self.vx = -self.vx - 0.002 * self.vx
            

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        return ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) <= (self.r + obj.r) ** 2


            
class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 1
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450
        self.r = 15
        self.gun_l = 10

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = (self.f2_power * math.cos(self.an)) / 2
        new_ball.vy = - (self.f2_power * math.sin(self.an)) / 2
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 0

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if (event.pos[0] - 20) == 0:
            self.an = 0
        else:
            if event:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
                
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY


    def draw(self):
        pygame.draw.polygon(self.screen, self.color,
                            [(self.x - math.sin(self.an) * self.gun_l, self.y + math.cos(self.an) * self.gun_l),
                             (self.x + math.sin(self.an) * self.gun_l, self.y - math.cos(self.an) * self.gun_l), (
                                 self.x + math.sin(self.an) * self.gun_l + math.cos(self.an) * self.f2_power / 1,
                                 self.y - math.cos(self.an) * self.gun_l + math.sin(self.an) * self.f2_power / 1),
                             (
                                 self.x - math.sin(self.an) * self.gun_l + math.cos(self.an) * self.f2_power / 1,
                                 self.y + math.cos(self.an) * self.gun_l + math.sin(self.an) * self.f2_power / 1)])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    target.move()


    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            b.color = WHITE
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
