from Konstanten import *
from Marker import *


class Oelquelle:
    anzahl_quellen = 0
    quelle_vergeben = [False for _ in range(20)]

    def __init__(self, qnr, snr, screen, game):
        Oelquelle.anzahl_quellen +=1
        self.screen = screen
        self.game = game
        self.nr = qnr
        Oelquelle.quelle_vergeben[self.nr] = True
        self.leistung = leistung[qnr]
        self.wert = wert[qnr]
        self.hafen = hafen[qnr]
        self.tankstand = 0
        self.maxtankstand = maxtank[qnr]
        self.farbe = COLOR[snr]
        self.marker = Marker(self.nr, self.farbe, self.screen, self.game)

    def foerderung(self, aktspieler):
        self.tankstand += self.leistung
        if aktspieler.doppeltefoerderung:  # wenn der Spieler das Doppelte-Förderung-Memo hat, dann Leistung noch einmal draufzählen
            self.tankstand += self.leistung
        if self.tankstand >= self.maxtankstand:
            self.tankstand = self.maxtankstand
        self.marker.setze(self.tankstand)

    def istankvoll(self):
        return self.tankstand == self.maxtankstand

    def draw(self):
        self.marker.draw()

    def reduzieretank(self, menge):
        self.tankstand -= menge
        self.marker.setze(self.tankstand)

    def leeretank(self):
        self.tankstand = 0
        self.marker.setze(self.tankstand)

    def loeschen(self):
        Oelquelle.anzahl_quellen -=1
        Oelquelle.quelle_vergeben[self.nr]= False


