import pygame as pg
from Konstanten import *


class Marker:
    def __init__(self, nr, farbe, screen, game):
        self.screen = screen
        self.game = game
        self.nr = nr
        self.farbe = farbe
        self.pos = 0
        self.dx = (2426 - 1967) / 15
        self.dy = (895 - 334) / 17
        self.x = 1967
        self.y = int(332 + (nr - 1) * self.dy)

    def setze(self, tankstand):
        self.pos = int(tankstand / 3000)

    def draw(self):
        pg.draw.circle(self.screen, COLOR[BLACK],
                       (int((self.x + self.pos * self.dx) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][0]), int((self.y + Fixdymarker) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][1])),
                       ZOOMSCALE[self.game.zoommode] * 12, 0)
        pg.draw.circle(self.screen, self.farbe,
                       (int((self.x + self.pos * self.dx) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][0]), int((self.y + Fixdymarker) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][1])),
                       ZOOMSCALE[self.game.zoommode] * 10, 0)
