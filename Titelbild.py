# from Images import *
# from Sounds import *
from Button import *
from Funktionen import *

from Konstanten import *


class Titelbild:
    def __init__(self, screen):
        self.screen = screen
        self.bild = imgTitelbild
        self.blende = blendeImage
        self.bildrect = self.bild.get_rect()
        self.mousepressed = False
        self.fertig = False
        self.einfach = False
        x = 370
        y = 650
        d = 50
        self.button = []
        for i in range(4):
            self.button.append(Button(16 + i, 1, 1, x + i * (250 + d), y, True, USEREVENT + 19 + i))
        self.button.append(Button(BUTTON_EINFACH,1,1,x+300,y+300,True,BUTTON_EINFACH_PRESSED))

    def draw(self, alpha, wahl=False):
        self.screen.fill(COLOR[BLACK])
        self.screen.blit(self.bild, ((1920 - self.bildrect.width) / 2, (1080 - self.bildrect.height) / 2))
        if wahl:
            for i in range(5):
                self.button[i].draw(self.screen)
        self.blende.set_alpha(alpha)
        self.screen.blit(self.blende, (0, 0))
        display.flip()

    def einblenden(self):
        for i in range(255, 5, -10):
            self.draw(i)

    def begruessen(self):
        playsound(begruessung, False)

    def waehlespielerzahl(self):
        fertig = False
        mp = False
        sanz = 0
        while not fertig:
            self.draw(0, True)
            # Mausklicks abfragen
            for event in pg.event.get():
                for i in range(4):
                    if event.type == USEREVENT + 19 + i:
                        sanz = i + 1
                        playsound(spielerzahlsound[i], False)
                        fertig = True

                if event.type == BUTTON_EINFACH_PRESSED:
                    self.switcheinfachcheckstate()

                if event.type == MOUSEBUTTONUP:
                    mp = False

            mousebutton = pg.mouse.get_pressed()
            if mousebutton[0]:
                if not mp:
                    mp = True
                    self.checkselection()
        return sanz,self.einfach

    def ausblenden(self):
        for alpha in range(0, 255, 10):
            self.draw(alpha)

    def checkselection(self):
        for i in range(5):
            self.button[i].checkselection()

    def switcheinfachcheckstate(self):
        self.einfach = not self.einfach
        self.button[4].switchcheckstate(self.einfach)

