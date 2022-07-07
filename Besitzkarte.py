import pygame as pg

from Konstanten import *
from Images import *


class Besitzkarte:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.x = 776
        self.y = 1438
        self.breite = 0  # 287 * ZOOMSCALE[game.zoommode]
        self.hoehe = 0  # 349 * ZOOMSCALE[game.zoommode]
        self.imageorig = image.load("Besitzkarten/1.png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        self.stapelorig = image.load("Besitzkarten/Stapel.png")
        self.stapel = pg.transform.scale(self.stapelorig, (self.breite + 10, self.hoehe + 10))
        self.stapelbreite = 300
        self.stapelhoehe = 360

    def zeigekarte(self, nr):
        self.breite = 287 * ZOOMSCALE[self.game.zoommode]
        self.hoehe = 349 * ZOOMSCALE[self.game.zoommode]
        self.imageorig = image.load("Besitzkarten/" + str(nr) + ".png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        self.drawstapel()
        self.draw()

    def drawstapel(self):
        self.stapelbreite = 300 * ZOOMSCALE[self.game.zoommode]
        self.stapelhoehe = 360 * ZOOMSCALE[self.game.zoommode]
        self.stapel = pg.transform.scale(self.stapelorig, (self.stapelbreite, self.stapelhoehe))
        self.screen.blit(self.stapel, ((self.x - 10) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][0], (self.y - 10) * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][1], self.stapelbreite, self.stapelhoehe))

    def draw(self):
        self.screen.blit(self.image, (self.x * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][0], self.y * ZOOMSCALE[self.game.zoommode] + ZOOMPOSDELTA[self.game.zoommode][1], self.breite, self.hoehe))
        pg.display.flip()
