import pygame
import json
from pygame.math import Vector2
from math import cos, sin, pi
import datetime
import math


# Аналогичный метод из библеотеки math выдаёт плохия значения
def radians(deg):
    return deg * pi / 180


def lineLen(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


class Entity:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.rotateAng = 0
        self.size = 1

    def getRotateRad(self):
        return radians(self.rotateAng)


class Wall:
    def __init__(self, p1=Vector2(0, 0), p2=Vector2(0, 0)):
        self.p1 = p1
        self.p2 = p2

    def collision(self, p1, p2):
        # Раскрываем точки на координаты
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = self.p1
        x4, y4 = self.p2

        # Математическая магия (Поиск пересечения двух прямых)
        if y2 - y1 != 0:
            q = (x2 - x1) / (y1 - y2)
            sn = (x3 - x4) + (y3 - y4) * q
            if not sn:
                return False
            fn = (x3 - x1) + (y3 - y1) * q
            n = fn / sn
        else:
            if not (y3 - y4):
                return False
            n = (y3 - y1) / (y3 - y4)
        x = x3 + (x4 - x3) * n
        y = y3 + (y4 - y3) * n

        res = Vector2(x, y)

        # Переворачиваем координаты, чтобы шли по часовой стрелке, нужно для следующих формул
        if x3 > x4:
            x3, x4 = x4, x3
        if y3 > y4:
            y3, y4 = y4, y3

        # Проверяем на принадлежность точки стене
        if not (x3 <= res.x <= x4 and y3 <= res.y <= y4):
            return False

        # Проверяем что точка лежит по правильную сторону луча
        if not ((res.x > x1) == (x2 > x1) and (res.y > y1) == (y2 > y1)):
            return False
        return res

    def draw2d(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.p1, self.p2)


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = Vector2(0, 0)
        self.speedS = 10

    def draw2d(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, 5)
        pygame.draw.line(screen, (100, 100, 100), self.position,
                         self.position + Vector2(cos(self.getRotateRad()) - sin(self.getRotateRad()),
                                                 sin(self.getRotateRad()) + cos(self.getRotateRad())) * 10,
                         width=3)

    def speedTick(self, time, walls):

        minVec = None

        #################### Колизия со стенами ##########################
        for j in walls:
            res = j.collision(self.position, self.position + self.speed * self.speedS)
            if res:
                if minVec is None:
                    minVec = res
                else:
                    if lineLen(self.position, res) < lineLen(self.position, minVec):
                        minVec = res
        if minVec is not None:
            if lineLen(self.position, minVec) < self.size:
                self.speed = Vector2(0, 0)
        #################################################################

        self.position += self.speed * self.speedS * (time / 1000)


class Pseudo3dRender:

    def __init__(self, screen, configPath="config.json", debug=False):
        self.config = json.load(open(configPath))
        self.debug = debug
        self.playerObj = Player()
        self.screen = screen
        self.walls = []

        self.start = None
        self.now = None
        pygame.font.init()
        self.font1 = pygame.font.SysFont('calibri', 30)

    def keyHander(self):
        keys = pygame.key.get_pressed()
        self.playerObj.speed = Vector2(0, 0)
        if keys[pygame.K_a]:
            self.playerObj.speed -= Vector2(
                cos(radians(self.playerObj.rotateAng + 90)) - sin(radians(self.playerObj.rotateAng + 90)),
                sin(radians(self.playerObj.rotateAng + 90)) + cos(radians(self.playerObj.rotateAng + 90)))
        if keys[pygame.K_d]:
            self.playerObj.speed += Vector2(
                cos(radians(self.playerObj.rotateAng + 90)) - sin(radians(self.playerObj.rotateAng + 90)),
                sin(radians(self.playerObj.rotateAng + 90)) + cos(radians(self.playerObj.rotateAng + 90)))
        if keys[pygame.K_w]:
            self.playerObj.speed += Vector2(cos(self.playerObj.getRotateRad()) - sin(self.playerObj.getRotateRad()),
                                            sin(self.playerObj.getRotateRad()) + cos(self.playerObj.getRotateRad()))
        if keys[pygame.K_s]:
            self.playerObj.speed += -Vector2(cos(self.playerObj.getRotateRad()) - sin(self.playerObj.getRotateRad()),
                                             sin(self.playerObj.getRotateRad()) + cos(self.playerObj.getRotateRad()))
        if keys[pygame.K_LEFT]:
            self.playerObj.rotateAng -= 1000 / config["FPS"] * 0.1
        if keys[pygame.K_RIGHT]:
            self.playerObj.rotateAng += 1000 / config["FPS"] * 0.1

    def tick(self):
        self.now = datetime.datetime.now()
        # Заливаем чёрным
        self.screen.fill((0, 0, 0))

        # Рисуем пол
        pygame.draw.rect(self.screen, (124, 124, 124), (0, height / 2, width, height / 2))

        # Просчитываем перемещение игрока
        self.playerObj.speedTick(1000 / config["FPS"], self.walls)

        # Отрисовка миникарты для дебага
        if self.debug:
            self.Minimap2d()
        self.draw()
        delta = self.now - self.start
        string1 = self.font1.render(str(delta), True, pygame.Color(120, 120, 120))
        self.screen.blit(string1, (width // 2 - 100 + 2, 0))

    def draw(self):
        # 1 луч равен 1-10 горизонтальных пикселей в зависимости от коэфицента
        # Больше значение - хуже качество, но больше быстродействие
        schacalCoef = 3
        for i in range(config["RESOLUTION"][0] // schacalCoef):
            iterat = i * schacalCoef
            ang = radians(
                (iterat * config["FOV"] / config["RESOLUTION"][0]) + self.playerObj.rotateAng - config["FOV"] / 2)

            # Поворачиваем вектор луча
            V2 = Vector2(cos(ang) - sin(ang), sin(ang) + cos(ang))

            minVec = None

            # Проверка пересечения стен лучём и нахождение ближайшей точки пересечения
            for j in self.walls:
                res = j.collision(self.playerObj.position, self.playerObj.position + V2)
                if res:
                    if minVec is None:
                        minVec = res
                    else:
                        if lineLen(self.playerObj.position, res) < lineLen(self.playerObj.position, minVec):
                            minVec = res
            if minVec is not None:
                # Начало вертикальной полоски
                nCeiling = (height / 2) - height / (lineLen(self.playerObj.position, minVec) / 5)

                # Конец вертикальной полоски
                nFloor = height - nCeiling

                # Затемнение дальних
                depthColor = min(max(255 - lineLen(self.playerObj.position, minVec) * 3.5, 0), 255)

                pygame.draw.line(screen, (depthColor, depthColor, depthColor), Vector2(iterat, nCeiling),
                                 Vector2(iterat, nFloor),
                                 width=schacalCoef)

    def loadMap(self, mapId):
        map = json.load(open(self.config["maps"][mapId]))
        self.walls = []
        for i in map["Walls"]:
            self.walls.append(Wall(Vector2(i[0]), Vector2(i[1])))
        self.playerObj.position = Vector2(map["Zones"]["StartPos"])
        self.start = datetime.datetime.now()

    def Minimap2d(self):
        [i.draw2d(screen) for i in self.walls]
        self.playerObj.draw2d(screen)


class LeaderBoard:
    def __init__(self, path="records.json"):
        self.path = path

    def getRecord(self):
        print(json.load(open(self.path, mode="r")))
        return json.load(open(self.path, mode="r"))

    def addRecord(self, map, name, time):
        outJson = self.getRecord()
        record = outJson.get(map, [])
        record.append({"name": name, "time": time})
        outJson[map] = record
        print(outJson)
        json.dump(outJson, open(self.path, mode="w"))


class StartWindow:
    def __init__(self):
        pass


config = json.load(open("config.json"))
leaderBoard = LeaderBoard()

size = width, height = config["RESOLUTION"]
screen = pygame.display.set_mode(size)

GameRender = Pseudo3dRender(screen, debug=False)
GameRender.loadMap(0)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    GameRender.keyHander()
    GameRender.tick()
    clock.tick(config["FPS"])
    pygame.display.flip()
