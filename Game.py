from Konstanten import *

class Game:
    def __init__(self):
        self.zoommode = ZOOMFULL
        self.Mode = SPIELRUN
        self.spielrunde = 0
        self.zugfertig = True
        self.anzahl_vergeben = 0
        self.aktspieler = None
        self.suezkanalgesperrt = False
        self.anzahlspieler = 0
        self.rate = 1
        self.einfach = False
        self.maxgeld = 10000000
        self.quiet = False

    def setmaxgeld(self,betrag):
        self.maxgeld = betrag
        print(f"Das Spielziel liegt jetzt bei {self.maxgeld} $")

    def setquietmode(self):
        self.quiet = True

    def changerate(self, newrate):
        self.rate = newrate

    def setzeanzahlspielerundModus(self, wert):
        self.anzahlspieler = wert[0]
        self.einfach = wert[1]

    def sperresuezkanal(self, modus):
        self.suezkanalgesperrt = modus

    def set_zuglaeuft(self):
        self.zugfertig = False

    def set_zugfertig(self):
        self.zugfertig = True

    def newround(self):
        self.spielrunde += 1

    def setzoommode(self, mode):
        self.zoommode = mode

    def getzoommode(self):
        return self.zoommode

    def setzemode(self, mode):
        self.Mode = mode

    def setzeaktspieler(self, spnr):
        self.aktspieler = spnr

    def setSpielmodus(self, wert):
        self.einfach = wert

    def iseinfach(self):
        return self.einfach