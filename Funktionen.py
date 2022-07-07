import pygame as pg
from Konstanten import *
from Images import *
from Sounds import *
from time import *
import sys


def playsound(sound, klick):
    sound.play()
    sleep(sound.get_length())
    if klick:
        warteaufklick()


def warteaufklick(screen):
    mousepressed = False
    done = False
    screen.blit(buttonKlick, (1546, 980))
    pg.display.update()
    while not done:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mousepressed = True
            if event.type == pg.MOUSEBUTTONUP and mousepressed:
                done = True


def spielzuende(spieler):
    # Die Abfrage muss nach jedem Beenden eines Spielzugs über alle Spieler laufen,
    # denn auch die anderen Spieler können durch eine Dividendenausschüttung die
    # Obergrenze erreicht haben
    for i in range(len(spieler)):
        if spieler[i].istbankrott():
            playsound(verloren[i], False)
            return True
        if spieler[i].hatzehnmillionen():
            playsound(gewonnen[i], False)
            return True
    return False


def drawmoney(screen, wert, size, posx, posy):
    grossimages = []
    kleinimages = []
    for i in range(10):
        grossimages.append(Zahlimages[i])
        kleinimages.append(Zahlimages[i])
        grossimages[i] = pg.transform.scale(Zahlimages[i], (0.35 * Zahlimages[i].get_width(), 0.5 * Zahlimages[i].get_height()))
        kleinimages[i] = pg.transform.scale(Zahlimages[i], (0.20 * Zahlimages[i].get_width(), 0.30 * Zahlimages[i].get_height()))
    dollarimage = pg.transform.scale(Dollar, (0.5 * Dollar.get_width(), 0.5 * Dollar.get_height()))
    dollarkleinimage = pg.transform.scale(Dollar, (0.3 * Dollar.get_width(), 0.3 * Dollar.get_height()))
    dx = 7
    dy = 67
    dp = 15
    dz = 35
    dd = 20
    ps = 5
    if size == SMALL:
        dx = 5
        dy = 40
        dp = 10
        dz = 22
        dd = 15
        ps = 3

    moneystring = str(int(wert))
    anzpunkte = 0
    i = 0
    for i in range(len(moneystring)):
        if i == 3 or i == 6:
            pg.draw.circle(screen, COLOR[BLACK], (posx - dx - anzpunkte * dp - (i - 1) * dz, posy + dy), ps, 0)
            pg.draw.circle(screen, (150, 0, 0), (posx - dx - anzpunkte * dp - (i - 1) * dz, posy + dy), ps - 2, 0)
            anzpunkte += 1
        ziffer = int(moneystring[len(moneystring) - 1 - i])
        if size == LARGE:
            screen.blit(grossimages[ziffer], (posx - anzpunkte * dp - i * dz, posy))
        else:
            screen.blit(kleinimages[ziffer], (posx - anzpunkte * dp - i * dz, posy))
    if size == LARGE:
        screen.blit(dollarimage, (posx - dd - anzpunkte * dp - (i + 1) * dz, posy))
    else:
        screen.blit(dollarkleinimage, (posx - dd - anzpunkte * dp - (i + 1) * dz, posy))
        font = pg.font.SysFont("Helvetica", 20)
        gmlabel = font.render("Gesamt-", True, COLOR[BLACK])
        screen.blit(gmlabel, (posx + 30, posy))
        gmlabel = font.render("vermögen", True, COLOR[BLACK])
        screen.blit(gmlabel, (posx + 30, posy + 20))
