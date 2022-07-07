import pygame as pg
from Images import *


class Button:
    def __init__(self, typ, scalex, scaley, x, y, pressable, eventtyp):
        self.typ = typ
        self.x = x
        self.y = y
        self.eventtyp = eventtyp
        self.scalex = scalex
        self.scaley = scaley
        self.pressable = pressable
        self.originalImage = buttonImages[self.typ]
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        # self.originalImage = pg.transform.scale(self.originalImage, (self.originalwidth * self.scalex, self.originalheight * self.scaley))
        self.image = pg.transform.scale(self.originalImage, (self.originalwidth * self.scalex, self.originalheight * self.scaley))
        self.button_width = self.image.get_width()
        self.button_height = self.image.get_height()
        self.my_event = 0
        self.x_min = self.x
        self.y_min = self.y
        self.x_max = self.x_min + self.button_width
        self.y_max = self.y_min + self.button_height

    def checkselection(self):
        if self.pressable:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if (mouse_x > self.x_min) and (mouse_y > self.y_min) and (mouse_x < self.x_max) and (mouse_y < self.y_max):
                pg.event.post(pg.event.Event(self.eventtyp, message='Button pressed'))

    def draw(self, screen):
        self.image = pg.transform.scale(self.originalImage, (self.originalwidth * self.scalex, self.originalheight * self.scaley))
        screen.blit(self.image, (self.x, self.y))

    def setalpha(self, wert):
        self.originalImage.set_alpha(wert)

    def switchcheckstate(self, state):
        if state == False:
            self.originalImage = image.load("Bedienfeld/unchecked-d.png")
        else:
            self.originalImage = image.load("Bedienfeld/checked-d.png")
        self.originalImage = pg.transform.scale(self.originalImage, (self.originalwidth * self.scalex, self.originalheight * self.scaley))

