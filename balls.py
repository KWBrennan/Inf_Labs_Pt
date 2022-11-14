import pygame
from pygame.draw import circle
from random import randint
from math import cos, sin, radians

pygame.init()

# Экран
FPS = 60
display_size = (900, 600)
screen = pygame.display.set_mode(display_size)


# Размер шаров
max_figure_size = 50
min_figure_size = 30

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
VIOLET = (127, 0, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GOLDEN = (212, 175, 55)
COLORS = [RED, BLUE, VIOLET, GREEN, MAGENTA, CYAN]


# Функции
def new_ball():
    """
    Создаёт новый шарик со случайным радиусом в случайном месте
    Returns:
        params - возвращает параметры созданного шара:
            color - цвет шара
            [x_b, y_b] - начальные иксовая и игрековая координаты центра шара
            r_b - радиус шара
            alpha - угол, задающий направление движения
        """

    x_b = randint(max_figure_size, display_size[0] - max_figure_size)
    y_b = randint(max_figure_size, display_size[1] - max_figure_size)
    r_b = randint(min_figure_size, max_figure_size)
    alpha = randint(0, 359)
    color = COLORS[randint(0, 5)]
    params = [color, [x_b, y_b], r_b, alpha]
    return params


def get_starting_objects(object_count=3):
    starting_objects = []
    for _ in range(object_count):
        ball = new_ball()
        starting_objects.append(ball)
    return starting_objects


def objects_draw():
    for thing in objects_on_screen:
        circle(screen, *thing[:-1])


def balls_list():
    return objects_on_screen


def is_hit(x_o, y_o, r_o):
    x_cl, y_cl = pygame.mouse.get_pos()
    return (x_o - x_cl) ** 2 + (y_o - y_cl) ** 2 <= r_o ** 2

def get_phi(min_phi=0, max_phi=359):
    phi = randint(min_phi, max_phi)
    return phi


def is_close_to_wall(something):
    """
    Проверяет, сталкивается ли объект 'something' со стеной (краем экрана)
    и изменяет направление его движения согласно закону отражения
    Args:
        something: объект, который проверяем на столкновение со стеной
    Функция ничего не возвращает
     """

    if something[1][0] + cos(radians(something[3])) - something[2] < 0:
        something[3] = 180 - something[3]
    elif something[1][0] + cos(radians(something[3])) + something[2] > display_size[0]:
        something[3] = 180 - something[3]
    elif something[1][1] + sin(radians(something[3])) + something[2] > display_size[1]:
        something[3] = -something[3]
    elif something[1][1] + sin(radians(something[3])) - something[2] < 0:
        something[3] = -something[3]


def moving_objects():
    """
    Перемещает объекты в направлении, заложенном в параметрах объекта.
    Функция ничего не принимает и не возвращает
    """

    for j in range(len(objects_on_screen)):
        is_close_to_wall(objects_on_screen[j])
        x_move = 100 / FPS * cos(radians(objects_on_screen[j][3]))  
        y_move = 100 / FPS * sin(radians(objects_on_screen[j][3]))  
        objects_on_screen[j][1][0] += x_move
        objects_on_screen[j][1][1] += y_move
       

pygame.display.update()
clock = pygame.time.Clock()
finished = False
escape = False


hit_counter = 0
snitch_counter = 0
ball_counter = 0
miss_counter = 0


objects_on_screen = get_starting_objects()

while (not finished) and (not escape):
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                escape = True
        elif event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for obj in reversed(objects_on_screen):  
                x, y, r = obj[1][0], obj[1][1], obj[2]
                if is_hit(x, y, r):
                    hit_counter += 1
                    ball_counter += 1
                    new_object = new_ball()
                    objects_on_screen[objects_on_screen.index(obj)] = new_object
                    break
            else:
                miss_counter += 1
                miss_fill = FPS // 20
    moving_objects()
    objects_draw()
    pygame.display.update()
    screen.fill(WHITE)

if finished:
    pygame.quit()
elif escape:
    escape = False
    font = pygame.font.Font(None, 36)
    total = font.render("Total:", True, BLACK)
    points = font.render(f'You got {hit_counter} points', True, BLACK)
    miss = font.render(f'You missed {miss_counter} times', False, BLACK)
    if (ball_counter + miss_counter) != 0:
        accuracy_number = round((ball_counter) / (ball_counter + miss_counter) * 100, 2)
    else:
        accuracy_number = 0
    accuracy = font.render(f'Your accuracy was '
                           f'{accuracy_number}%',
                           True, BLACK)
    texts = (total, points, miss, accuracy)
    for i in range(len(texts)):
        screen.blit(texts[i], (display_size[0] // 2, display_size[1] // 2 + 40 * i))
        pygame.display.update()
    while (not finished) and (not escape):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                finished = True
pygame.quit()