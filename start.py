from pygame import *
from random import *

# Инициализация Pygame
init()

# Создание игрового экрана и установка частоты обновления кадров
screen = display.set_mode((1280, 720))
fps = time.Clock()

# Определение размеров и количества клеток
cell_x = 20
cell_y = 14
cell_size = 50

# Загрузка изображений
bg = image.load("bg.png")
floor = transform.scale(image.load("rpgTile024.png"), (cell_size, cell_size))
wall = transform.scale(image.load("rpgTile133.png"), (cell_size, cell_size))
door = transform.scale(image.load("rpgTile154.png"), (cell_size, cell_size))
dark = transform.scale(image.load("rpgTile000.png"), (cell_size, cell_size))


class Cell():
    def __init__(self, x, y):
        # Клетка состоит из изображения пола и координат на экране
        self.img = [floor]
        self.pos = [10 + x * cell_size, 10 + y * cell_size]


def set_random_wall(level, amount):
    # Установка случайных стен на уровне
    if amount > cell_x * cell_y:
        amount = cell_x * cell_y
    for i in range(amount):
        x = randint(0, cell_x - 1)
        y = randint(0, cell_y - 1)
        # Повторяем генерацию, если клетка уже содержит стену
        while wall in level[x][y].img:
            x = randint(0, cell_x - 1)
            y = randint(0, cell_y - 1)
        level[x][y].img.append(wall)
    # Убедиться, что стартовая клетка не содержит стены
    if wall in level[0][0].img:
        level[0][0].img.remove(wall)


def set_path(level):
    # Создание пути от начала до конца уровня
    x, y = 0, 0
    while x < cell_x - 2:
        path = []
        if y > 1:
            path.append("up")
        if y < 12:
            path.append("down")
        path = choice(path)

        if path == "down":
            amount = randint(2, cell_y - 1 - y)
            for i in range(amount):
                y += 1
                if wall in level[x][y].img:
                    level[x][y].img.remove(wall)
        else:
            amount = randint(2, y)
            for i in range(amount):
                y -= 1
                if wall in level[x][y].img:
                    level[x][y].img.remove(wall)
        amount = 2
        for i in range(amount):
            x += 1
            if wall in level[x][y].img:
                level[x][y].img.remove(wall)
    while y < cell_y - 1:
        y += 1
        if wall in level[x][y].img:
            level[x][y].img.remove(wall)
    x += 1
    if wall in level[x][y].img:
        level[x][y].img.remove(wall)
    level[x][y].img.append(door)


class Hero():
    def __init__(self, n):
        # Инициализация героя: положение, размер, скорость, изображения
        self.pos = [10, 10]
        self.size = [50, 50]
        self.speed = 2
        self.img = [
            [
                image.load("hero/3_Actor1_" + str(int(n) + 36) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 35) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 36) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 37) + ".png"),
            ],
            [
                image.load("hero/3_Actor1_" + str(int(n) + 12) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 11) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 12) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 13) + ".png"),
            ],
            [
                image.load("hero/3_Actor1_" + str(int(n) + 0) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) - 1) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 0) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 1) + ".png"),
            ],
            [
                image.load("hero/3_Actor1_" + str(int(n) + 24) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 23) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 24) + ".png"),
                image.load("hero/3_Actor1_" + str(int(n) + 25) + ".png"),
            ],
        ]
        for i in range(len(self.img)):
            for j in range(len(self.img[i])):
                self.img[i][j] = transform.scale(self.img[i][j], (cell_size, cell_size))
        self.dire = K_s
        self.finish = False
        self.cadr = 0

    def move(self):
        # Движение героя
        speed = [[0, -self.speed], [-self.speed, 0], [0, self.speed], [self.speed, 0]]
        keys = key.get_pressed()
        n = 0
        for i in range(len(dire)):
            if keys[dire[i]]:
                self.pos[0] += speed[i][0]
                self.pos[1] += speed[i][1]
                self.dire = dire[i]
                self.cadr += 1
                if self.cadr >= 4 * 3:
                    self.cadr = 0
                if self.out_of_range():
                    self.pos[0] -= speed[i][0]
                    self.pos[1] -= speed[i][1]
                    self.cadr = 0
                if self.collide():
                    self.pos[0] -= speed[i][0]
                    self.pos[1] -= speed[i][1]
                    self.cadr = 0
                break
            n += 1
        if n == 4:
            self.cadr = 0

    def out_of_range(self):
        # Проверка выхода за пределы игрового поля
        return (self.pos[0] < 10 or self.pos[1] < 10 or self.pos[0] + self.size[0] > 1010 or
                self.pos[1] + self.size[1] > 710)

    def collide(self):
        # Проверка столкновений с препятствиями и дверью
        corner = [
            [self.pos[0] + 6, self.pos[1] + 6],
            [self.pos[0] - 6 + self.size[0] - 1, self.pos[1] + 6],
            [self.pos[0] + 6, self.pos[1] + self.size[1] - 1],
            [self.pos[0] - 6 + self.size[0] - 1, self.pos[1] + self.size[1] - 1]
        ]
        for i in range(len(corner)):
            x = (corner[i][0] - 10) // cell_size
            y = (corner[i][1] - 10) // cell_size
            if wall in level[x][y].img:
                return True
            if door in level[x][y].img:
                self.finish = True
        return False


def set_dark(level):
    # Установка затемнения на клетки, которые не находятся рядом с героем
    hx = (hero.pos[0] + hero.size[0] // 2 - 10) // cell_size
    hy = (hero.pos[1] + hero.size[1] // 2 - 10) // cell_size

    range_x = [hx]
    if hx > 0:
        range_x.append(hx - 1)
    if hx < cell_x - 1:
        range_x.append(hx + 1)

    range_y = [hy]
    if hy > 0:
        range_y.append(hy - 1)
    if hy < cell_y - 1:
        range_y.append(hy + 1)

    for x in range(cell_x):
        for y in range(cell_y):
            q = False
            for hx in range_x:
                for hy in range_y:
                    if hx == x and hy == y:
                        if dark in level[x][y].img:
                            level[x][y].img.remove(dark)
                        q = True
            if not q:
                if not (dark in level[x][y].img):
                    level[x][y].img.append(dark)


def show_info():
    # Отображение информации об уровне
    mes = "Уровень: %s" % (n_lvl)
    f = font.SysFont("Arial", 30)
    mes_size = f.size(mes)
    img = f.render(mes, True, (255, 202, 134))
    screen.blit(img, (1020 + (260 - mes_size[0]) // 2, 10))


def show_all():
    # Отображение всех игровых элементов на экране
    screen.blit(bg, (0, 0))
    show_info()
    set_dark(level)
    for x in range(cell_x):
        for y in range(cell_y):
            for i in range(len(level[x][y].img)):
                screen.blit(level[x][y].img[i], level[x][y].pos)
    n = dire.index(hero.dire)
    screen.blit(hero.img[n][hero.cadr // 3], hero.pos)


def set_level():
    # Установка нового уровня
    global level, hero, n_lvl
    level = []
    for x in range(cell_x):
        level.append([])
        for y in range(cell_y):
            level[x].append(Cell(x, y))

    set_random_wall(level, 180)
    set_path(level)
    n_lvl += 1
    hero = Hero("50")


# Определение направления движения
dire = [K_w, K_a, K_s, K_d]

# Начальный уровень
n_lvl = 0

# Флаг начала игры
game_started = False


def show_start_screen():
    # Отображение стартового экрана
    screen.blit(bg, (0, 0))
    f = font.SysFont("Arial", 100)
    play_text = f.render("Играть", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(640, 360))
    screen.blit(play_text, play_rect)
    return play_rect


# Установка первого уровня
set_level()

# Основной игровой цикл
while True:
    for action in event.get():
        if action.type == QUIT:
            quit()
            exit()
        if action.type == MOUSEBUTTONDOWN and not game_started:
            if play_rect.collidepoint(action.pos):
                game_started = True

    if game_started:
        hero.move()
        show_all()
    else:
        play_rect = show_start_screen()

    display.update()
    fps.tick(60)

    if game_started and hero.finish:
        set_level()
