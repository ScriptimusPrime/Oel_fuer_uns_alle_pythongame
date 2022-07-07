import pygame as pg
from Konstanten import *
from Images import *
from Button import *
from Game import *
from Funktionen import *
import random


class Console:
    def __init__(self, screen, game, spieler):
        self.screen = screen
        self.game = game
        self.spieler = spieler
        self.x = 1516
        self.y = 0
        self.width = 406
        self.height = 1080

        self.x_money = self.x + 310
        self.y_money = 160
        self.x_gesamtmoney = self.x + 260
        self.y_gesamtmoney = 250
        self.AktienReedimage = pg.transform.scale(Aktienimages[TANKSCHIFF], (0.73 * Aktienimages[TANKSCHIFF].get_width(), 0.73 * Aktienimages[TANKSCHIFF].get_height()))
        self.AktienRaffimage = pg.transform.scale(Aktienimages[RAFFINERIE], (0.73 * Aktienimages[RAFFINERIE].get_width(), 0.73 * Aktienimages[RAFFINERIE].get_height()))

        self.landbutton = []

        self.buttonplus1 = Button(BUTTON_PLUS, 0.7, 0.7, self.x + 50, 462, True, BUTTON_PLUS1_PRESSED)
        self.buttonminus1 = Button(BUTTON_MINUS, 0.7, 0.7, self.x + 110, 462, True, BUTTON_MINUS1_PRESSED)
        self.buttonplus2 = Button(BUTTON_PLUS, 0.7, 0.7, self.x + 250, 462, True, BUTTON_PLUS2_PRESSED)
        self.buttonminus2 = Button(BUTTON_MINUS, 0.7, 0.7, self.x + 310, 462, True, BUTTON_MINUS2_PRESSED)
        self.wuerfelmatte = Button(WUERFELMATTE, 1, 1, self.x + 30, 770, True, BUTTON_WUERFELMATTE_PRESSED)
        self.zugbeenden = Button(BUTTON_ZUGBEENDEN, 1, 1, self.x + 30, 980, True, BUTTON_ZUGBEENDEN_PRESSED)
        self.tankerstarten = Button(BUTTON_TANKERSTARTEN, 1, 1, self.x + 30, 680, True, BUTTON_TANKERSTARTEN_PRESSED)
        self.probebohrung = Button(BUTTON_PROBEBOHRUNG, 1, 1, self.x + 30, 590, True, BUTTON_PROBEBOHRUNG_PRESSED)
        self.quellekaufen = Button(BUTTON_QUELLEKAUFEN, 1, 1, self.x + 30, 590, True, BUTTON_QUELLEKAUFEN_PRESSED)
        self.buttonclose = Button(BUTTON_CLOSE, 1, 1, 1865, 5, True, BUTTON_CLOSE_PRESSED)
        self.wuerfelimage = wuerfelimages[0]
        self.wuerfelimage = pg.transform.scale(self.wuerfelimage, (int(0.7 * self.wuerfelimage.get_width()), int(0.7 * self.wuerfelimage.get_height())))
        self.wuerfelx = self.x + 150
        self.wuerfely = 825
        # Buttons für Landauswahl zum Verschiffen
        for i in range(5):
            self.landbutton.append(Button(i + 10, 1, 1, int(Landbutton_pos[i][0] * ZOOMSCALE[ZOOMFULL] + ZOOMPOSDELTA[ZOOMFULL][0]), int(Landbutton_pos[i][1] * ZOOMSCALE[ZOOMFULL] + ZOOMPOSDELTA[ZOOMFULL][1]), True, i + 13))

    def changewuerfel(self, nr):
        if 1 <= nr <= 6:  # Abfrage zur Sicherheit, weil für Tests auch größere Zahlen eingestellt sein können
            self.wuerfelimage = wuerfelimages[nr - 1]
            self.wuerfelimage = pg.transform.scale(self.wuerfelimage, (int(0.7 * self.wuerfelimage.get_width()), int(0.7 * self.wuerfelimage.get_height())))
            self.wuerfelx = self.x + 150 + random.randrange(-2, 3) * 30
            self.wuerfely = 825 + random.randrange(-2, 3) * 13
            self.draw()
            pg.display.flip()

    def drawwuerfel(self):
        self.screen.blit(self.wuerfelimage, (self.wuerfelx, self.wuerfely, self.wuerfelimage.get_width(), self.wuerfelimage.get_height()))

    def drawplayer(self):
        self.screen.blit(imgSpielfigur[self.game.aktspieler + 4], (self.x + 140, self.y + 15))

    def drawaktien(self):
        self.screen.blit(self.AktienRaffimage, (self.x + 10, 340, self.AktienRaffimage.get_width(), self.AktienRaffimage.get_height()))
        self.screen.blit(self.AktienReedimage, (self.x + 210, 340, self.AktienReedimage.get_width(), self.AktienReedimage.get_height()))
        font = pg.font.SysFont("Verdana", 46)
        raff_label = font.render(str(int(self.spieler[self.game.aktspieler].tankschiffaktien)) + "x", True, COLOR[BLACK])
        reed_label = font.render(str(int(self.spieler[self.game.aktspieler].raffinerieaktien)) + "x", True, COLOR[BLACK])
        self.screen.blit(reed_label, (int(self.x + 90 - reed_label.get_width() / 2), 300))
        self.screen.blit(raff_label, (int(self.x + 300 - raff_label.get_width() / 2), 300))

    def drawaktivekarten(self):
        if self.game.suezkanalgesperrt:
            self.screen.blit(aktivekarten[SUEZKANALGESPERRT], (self.x + 10, 530, aktivekarten[SUEZKANALGESPERRT].get_width(), aktivekarten[SUEZKANALGESPERRT].get_height()))
        if self.spieler[self.game.aktspieler].foerderstop:
            self.screen.blit(aktivekarten[FOERDERSTOPQUELLEN], (self.x + 140, 530, aktivekarten[FOERDERSTOPQUELLEN].get_width(), aktivekarten[FOERDERSTOPQUELLEN].get_height()))
        if self.spieler[self.game.aktspieler].doppeltefoerderung:
            self.screen.blit(aktivekarten[DOPPELTEFOERDERUNG], (self.x + 270, 530, aktivekarten[DOPPELTEFOERDERUNG].get_width(), aktivekarten[DOPPELTEFOERDERUNG].get_height()))

    def draw(self):
        pg.draw.rect(self.screen, COLOR[BLACK], (self.x - 2, self.y, 2, self.height), 0)
        pg.draw.rect(self.screen, COLOR[GREY], (self.x, self.y, self.width, self.height), 0)

        self.buttonclose.draw(self.screen)
        self.drawplayer()
        drawmoney(self.screen, self.spieler[self.game.aktspieler].geld, LARGE, self.x_money, self.y_money)
        drawmoney(self.screen, self.spieler[self.game.aktspieler].gesamtvermoegen(), SMALL, self.x_gesamtmoney, self.y_gesamtmoney)
        self.drawaktien()
        self.drawaktivekarten()
        if self.spieler[self.game.aktspieler].darfquellekaufen:
            self.quellekaufen.draw(self.screen)
        if self.spieler[self.game.aktspieler].darfprobebohrung:
            self.probebohrung.draw(self.screen)
        if self.spieler[self.game.aktspieler].onboerse:
            self.buttonplus1.draw(self.screen)
            self.buttonminus1.draw(self.screen)
            self.buttonplus2.draw(self.screen)
            self.buttonminus2.draw(self.screen)
            if self.spieler[self.game.aktspieler].onboersemodus == HALBERPREIS:
                self.screen.blit(saleimage, (1670, 400))
        if self.spieler[self.game.aktspieler].kannbeenden:
            self.zugbeenden.draw(self.screen)
        self.tankerstarten.draw(self.screen)
        self.wuerfelmatte.draw(self.screen)
        self.drawwuerfel()
        # Länderbuttons zeigen
        if self.spieler[self.game.aktspieler].landauswahl:
            for button in self.landbutton:
                button.draw(self.screen)

    def checkselection(self):
        if self.spieler[self.game.aktspieler].landauswahl:
            for button in self.landbutton:
                button.checkselection()
        if self.spieler[self.game.aktspieler].darfprobebohrung:
            self.probebohrung.checkselection()
        if self.spieler[self.game.aktspieler].darfquellekaufen:
            self.quellekaufen.checkselection()
        if self.spieler[self.game.aktspieler].onboerse:
            self.buttonplus1.checkselection()
            self.buttonminus1.checkselection()
            self.buttonplus2.checkselection()
            self.buttonminus2.checkselection()
        self.wuerfelmatte.checkselection()
        if self.spieler[self.game.aktspieler].kannbeenden:
            self.zugbeenden.checkselection()
        self.tankerstarten.checkselection()
        self.buttonclose.checkselection()
