import pygame as pg
from Konstanten import *
from Funktionen import *
from Images import *


class Spielende:
    def __init__(self, screen, game, spieler):
        self.screen = screen
        self.game = game
        self.spieler = spieler
        self.image = endeImage
        self.blende = blendeImage

    def drawergebnisse(self):
        posx = 800
        posy = 320
        reihe = []
        for i in range(self.game.anzahlspieler):
            reihe.append((i, self.spieler[i].gesamtvermoegen()))
        reihe.sort(key=lambda x: x[1], reverse=True)

        for i in range(self.game.anzahlspieler):
            figur = imgSpielfigur[reihe[i][0] + 4]
            figur = pg.transform.scale(figur, (0.4 * figur.get_width(), 0.4 * figur.get_height()))
            self.screen.blit(figur, (posx, posy + i * 115))
            drawmoney(self.screen, self.spieler[reihe[i][0]].gesamtvermoegen(), LARGE, posx + 400, posy + 10 + i * 115)

    def draw(self, alpha):
        self.screen.blit(self.image, (0, 0))
        self.drawergebnisse()
        self.blende.set_alpha(alpha)
        self.screen.blit(self.blende, (0, 0))
        pg.display.flip()

    def ausblenden(self):
        for alpha in range(5, 255, 10):
            self.draw(alpha)

    def einblenden(self):
        for alpha in range(255, 5, -10):
            self.draw(alpha)

    def show(self):
        self.einblenden()
        warteaufklick(self.screen)
        self.ausblenden()
