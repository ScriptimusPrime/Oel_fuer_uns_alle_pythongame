# Imports
import random
from time import *
import sys

import pygame as pg
from pygame import mixer
from pygame.locals import *

# Initializing
pg.init()
pg.mixer.init()

clock = pg.time.Clock()

mixer.set_num_channels(4)

# Fenster erstellen
screen = pg.display.set_mode((1920, 1080), FULLSCREEN)

from Konstanten import *
from Images import *
from Sounds import *
from Game import *
from Marker import *
from Button import *
from Funktionen import *
from Oelquelle import *
from Besitzkarte import *
from Titelbild import *
from Spielende import *
from Console import *


screen.fill(COLOR[BLACK])


class Tanker:
    def __init__(self, player, startland):
        self.player = player
        self.image = pg.transform.scale(tanker[player.nummer], (0.3 * tanker[player.nummer].get_width(), 0.3 * tanker[player.nummer].get_height()))

        self.pos = -1
        self.routepos = -1
        self.x = -1
        self.y = -1
        self.startland = startland
        self.starthafen = starts[startland]
        self.anzahlziele = len(ziele[startland])
        self.zielhafen = ziele[startland][random.randrange(0, self.anzahlziele)]
        self.tankerroute = -1
        self.alternativroute = -1
        self.umgeleitet = False
        self.zielerreicht = False
        self.zielhafenid = -1
        for i in range(4):
            if self.zielhafen == Zielhaefennr[i]:
                self.zielhafenid = i

        self.frachtmenge = 0
        self.kosten = []
        self.gewinn = []
        self.kostengewinndiff = 0
        self.waehleFrachtbrief()
        self.starten()

    def waehleFrachtbrief(self):
        print("Wähle Frachtbrief")
        gefunden = False
        frachtbrief = []
        while not gefunden:
            self.frachtmenge = random.randint(0, 3)
            frachtbrief = Frachtbrief[self.startland][self.zielhafenid][self.frachtmenge]
            if frachtbrief is not None:
                self.kostengewinndiff = Gewinn[self.startland][self.zielhafenid][self.frachtmenge] * 1000
                gefunden = True
        print("Frachtbrief gefunden")
        for i in range(4):
            self.kosten.append(None)
            self.gewinn.append(None)
            self.kosten[i] = frachtbrief[i] * 10000
            self.gewinn[i] = self.kosten[i] + self.kostengewinndiff
        self.player.bezahlen(self.kosten[game.rate - 1])
        self.player.reduzieretankstand(self.startland, Frachtmengen[self.frachtmenge])
        # Sprachausgabe "Du verschiffst x Tonnen Rohöl aus " + "Starthafen" . Das Ziel ist x . Deine Kosten betragen bei Frachtrate x " Betrag " Dollar
        playsound(mixer.Sound("Sounds/Verschiffen/" + str(Frachtmengen[self.frachtmenge]) + ".mp3"), False)
        playsound(mixer.Sound("Sounds/Verschiffen/" + hafentext[self.startland] + ".mp3"), False)
        playsound(mixer.Sound("Sounds/Verschiffen/" + zieltext[self.zielhafen] + ".mp3"), False)
        playsound(mixer.Sound("Sounds/Verschiffen/Kosten" + str(game.rate) + ".mp3"), False)
        playsound(mixer.Sound("Sounds/Beträge/" + str(self.kosten[game.rate - 1]) + ".mp3"), False)
        playsound(mixer.Sound("Sounds/Verschiffen/Dollar.mp3"), False)
        drawallelements(False, True)

    def finderoute(self, startpos, zielhafen, strecke):
        gefundeneroute = -1
        if strecke == NORMALROUTE:
            for i in range(8):
                rte = Route[i]
                if rte[0] == startpos and rte[-1] == zielhafen:
                    gefundeneroute = i
        if strecke == AFRIKAROUTE:
            for i in range(8, 26):
                rte = Route[i]
                if rte[0] == startpos and rte[-1] == zielhafen:
                    gefundeneroute = i
        return gefundeneroute

    def starten(self):
        self.tankerroute = self.finderoute(self.starthafen, self.zielhafen, NORMALROUTE)
        self.routepos = 0
        self.pos = Route[self.tankerroute][self.routepos]
        self.zug(0)

    def zug(self, wurf):
        if game.suezkanalgesperrt and not self.umgeleitet:
            self.umleitung()
        aktpos = self.routepos
        newpos = aktpos + wurf
        if newpos >= len(Route[self.tankerroute]):
            newpos = len(Route[self.tankerroute]) - 1
        self.routepos = newpos
        for i in range(newpos - aktpos):
            self.move(aktpos + i, aktpos + i + 1)
        self.x = Position[Route[self.tankerroute][self.routepos]][0]
        self.y = Position[Route[self.tankerroute][self.routepos]][1]
        self.pos = Route[self.tankerroute][self.routepos]
        drawallelements(True, False)
        if self.pos == Route[self.tankerroute][-1]:
            self.zielerreicht = True

    def move(self, aktpos, nextpos):
        akt_x = Position[Route[self.tankerroute][aktpos]][0]
        akt_y = Position[Route[self.tankerroute][aktpos]][1]
        next_x = Position[Route[self.tankerroute][nextpos]][0]
        next_y = Position[Route[self.tankerroute][nextpos]][1]
        steps = 10
        dx = (next_x - akt_x) / steps
        dy = (next_y - akt_y) / steps
        for i in range(1, steps):
            self.x = int(akt_x + i * dx)
            self.y = int(akt_y + i * dy)
            drawallelements(True, False)

    def umleitung(self):
        # Suezkanal ist gesperrt
        if self.starthafen == 0 and self.zielhafen in ziele[1] and self.pos < 6:
            self.tankerroute = self.finderoute(self.pos, self.zielhafen, AFRIKAROUTE)
            self.routepos = 0
            self.pos = Route[self.tankerroute][self.routepos]
        self.umgeleitet = True

    def draw(self):
        xpos = self.x - self.image.get_width()
        ypos = self.y - self.image.get_height()
        screen.blit(self.image, (int(xpos * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0]), int(ypos * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1])))


class Memo:
    def __init__(self):
        self.x = 1670
        self.y = 1469
        self.breite = 240 * ZOOMSCALE[game.zoommode]
        self.hoehe = 295 * ZOOMSCALE[game.zoommode]
        self.imageorig = image.load("Memos/1.png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        self.kartenzaehler = 0
        self.mischen()

    def mischen(self):
        pos = 0
        for i in range(len(Memokarten)):  # alle 3. Stellen auf 0 setzen
            Memokarten[i][3] = 0
        for i in range(1, len(Memokarten) + 1):  # Plätze 1 bis 16 vergeben
            freigefunden = False
            while not freigefunden:
                pos = random.randrange(0, len(Memokarten))
                if Memokarten[pos][3] == 0:
                    freigefunden = True
            Memokarten[pos][3] = i
        Memokarten.sort(key=lambda x: x[3])

    def zeigekarte(self):
        karte = Memokarten[self.kartenzaehler]
        self.breite = 240 * ZOOMSCALE[game.zoommode]
        self.hoehe = 295 * ZOOMSCALE[game.zoommode]
        self.imageorig = image.load("Memos/" + str(Memokarten[self.kartenzaehler][0]) + ".png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        drawallelements(True, False)
        self.draw()

        self.kartenzaehler += 1
        if self.kartenzaehler == len(Memokarten):
            self.kartenzaehler = 0
            self.mischen()
        return karte


    def draw(self):
        screen.blit(self.image, (self.x * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0], self.y * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1], self.breite, self.hoehe))
        pg.display.update()


class Information:
    def __init__(self):
        self.x = 2426
        self.y = 1024
        self.breite = 243 * ZOOMSCALE[game.zoommode]
        self.hoehe = 291 * ZOOMSCALE[game.zoommode]
        self.imageorig = image.load("Informationen/1.png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        self.kartenzaehler = 0
        self.mischen()

    def mischen(self):
        pos = 0
        for i in range(len(Infokarten)):  # alle 3. Stellen auf 0 setzen
            Infokarten[i][3] = 0
        for i in range(1, len(Infokarten) + 1):  # Plätze 1 bis 16 vergeben
            freigefunden = False
            while not freigefunden:
                pos = random.randrange(0, len(Infokarten))
                if Infokarten[pos][3] == 0:
                    freigefunden = True
            Infokarten[pos][3] = i
        Infokarten.sort(key=lambda x: x[3])

    def karteauswerten(self, karte):
        typ = karte[1]
        wert = karte[2]

        if typ == FRACHTRATE:
            game.changerate(wert)
            playsound(frachtrate_sound[wert - 1], False)
        if typ == SUEZGESPERRT:
            game.sperresuezkanal(True)
            playsound(suezkanalgesperrt, False)
            drawallelements(False, True)
            pg.display.flip()
        if typ == DIVIDENDEN:
            raff = 5000
            tank = 8000
            if wert == 1:
                raff = 10000
                tank = 5000
            playsound(dividenden_sound[wert], False)

            for sp in spieler:
                sp.dividendenausschuettung(raff, tank)
        if typ == AKTIEN:
            playsound(aktien_sound[wert], False)
            for sp in spieler:
                sp.aktienausschuettung(wert)
        drawallelements(False, True)

    def zeigekarte(self):
        if game.suezkanalgesperrt:  # Beim Zeigen einer neuen Infokarte wird Soez-Sperrung aufgehoben
            game.sperresuezkanal(False)
            drawallelements(False, True)
        karte = Infokarten[self.kartenzaehler]
        self.breite = 243 * ZOOMSCALE[game.zoommode]
        self.hoehe = 308 * ZOOMSCALE[game.zoommode]
        self.imageorig = image.load("Informationen/" + str(Infokarten[self.kartenzaehler][0]) + ".png")
        self.image = pg.transform.scale(self.imageorig, (self.breite, self.hoehe))
        self.draw()
        self.karteauswerten(karte)
        self.kartenzaehler += 1
        # print(self.kartenzaehler)
        if self.kartenzaehler == len(Infokarten):
            self.kartenzaehler = 0
            self.mischen()
        return karte


    def draw(self):
        screen.blit(self.image, (self.x * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0], self.y * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1], self.breite, self.hoehe))
        pg.display.flip()


class Spieler:
    def __init__(self, nummer, typ):
        self.nummer = nummer
        self.typ = typ  # HUMAN oder COMPUTER
        self.bereich = ZOOMFULL
        self.bahn = AUSSENBAHN
        # print('Spielertyp ', self.typ)
        self.imageorig = imgSpielfigur[nummer]
        self.image = pg.transform.scale(self.imageorig, (int(FIGURZOOMSCALE[self.bereich][game.zoommode] * self.imageorig.get_width()), int(FIGURZOOMSCALE[self.bereich][game.zoommode] * self.imageorig.get_height())))
        self.imagerect = self.image.get_rect()
        self.pos = 0
        self.oldpos = 0
        self.newpos = 0
        self.x = FeldPos[self.pos][0]
        self.y = FeldPos[self.pos][1]
        self.dx = 0
        self.dy = 0
        self.bohrpos = 0
        self.figur_aufbohrloch = False
        self.figur_aufspielfeld = True
        self.geld = 1000000
        self.oelquellen = []
        self.tankschiffaktien = 0
        self.raffinerieaktien = 0
        self.dienstreisestation = 0
        self.urlaubstation = 0
        self.konferenzstation = 0
        self.ontour = False
        self.onboerse = False
        self.darfprobebohrung = False
        self.darfquellekaufen = False
        self.foerderstop = False
        self.doppeltefoerderung = False
        self.probebohrung_preis = 0
        self.onboersemodus = NORMALPREIS
        self.landauswahl = False
        self.tanker = []
        self.tankeristunterwegs = False
        self.wurf = 0
        self.kannbeenden = False
        self.zahlungsunfaehig = False

    def gesamtvermoegen(self):
        vermoegen = self.geld
        for quelle in self.oelquellen:
            vermoegen += quelle.wert
            vermoegen += quelle.tankstand * 5
        vermoegen += self.tankschiffaktien * 50000
        vermoegen += self.raffinerieaktien * 80000
        return vermoegen

    def istbankrott(self):
        return self.zahlungsunfaehig

    def hatzehnmillionen(self):
        return self.gesamtvermoegen() >= 10000000

    def tankmitgroesstermenge(self, land):
        tanknr = -1
        tankmenge = 0
        for i in range(len(self.oelquellen)):
            quelle = self.oelquellen[i]
            if quelle.hafen == land:
                if quelle.tankstand > tankmenge:
                    tankmenge = quelle.tankstand
                    tanknr = i
        return tanknr, tankmenge

    def reduzieretankstand(self, land, menge):
        restmenge = menge
        while restmenge > 0:
            quelle = self.tankmitgroesstermenge(land)
            if quelle[1] >= restmenge:
                self.oelquellen[quelle[0]].reduzieretank(restmenge)
                restmenge = 0
            else:
                restmenge -= self.oelquellen[quelle[0]].tankstand
                self.oelquellen[quelle[0]].leeretank()

    def hatgenugoel(self, land):
        oelmenge = 0
        print("Land=", land)
        for quelle in self.oelquellen:
            if quelle.hafen == land:
                print("Quelle gefunden", quelle.hafen)
                oelmenge += quelle.tankstand
        print("Deine Tanks in", hafentext[land], "enthalten insgesamt", oelmenge, "Tonnen Rohöl")
        if oelmenge >= Minimumoel[land]:
            print("Das sind mehr als", Minimumoel[land])
            return True
        else:
            print("Das ist nicht genug öl. Minimum =", Minimumoel[land])
            playsound(nichtgenugoel[land], False)
            return False

    def setzealleszurueck(self):
        self.setze_nokannbeenden()
        self.setze_noprobebohrung()
        self.setze_noquellekaufen()
        self.setze_nolandauswahl()

    def setze_nokannbeenden(self):
        self.kannbeenden = False

    def setze_notonboerse(self):
        self.onboerse = False

    def setze_noprobebohrung(self):
        self.darfprobebohrung = False

    def setze_noquellekaufen(self):
        self.darfquellekaufen = False

    def setze_nolandauswahl(self):
        self.landauswahl = False

    def test(self):
        self.aktienverkaufen(EGAL, 2, HALBERPREIS)

    def spielzugstarten(self):
        # print("Spieler ",self.nummer, " zieht")
        if self.bahn == AUSSENBAHN or self.tanker or self.bereich == ZOOMBOHRUNG:  # Würfeln, wenn Spieler auf der AUssenbahn ist, oder gerade bohrt oder einen Tanker unterwegs hat
            self.wurf = self.wuerfeln()  # oder wenn er gerade auf Urlaubs/Dienstreisenspur ist, aber Tanker unterwegs sind
        if self.bereich == ZOOMBOHRUNG:
            self.bohrzug(self.wurf)  # Simulier Würfeln und Zug
        elif self.bereich == ZOOMFULL:
            if self.bahn == AUSSENBAHN:
                self.zug(self.wurf)  # Simulier Würfeln und Zug
            elif self.bahn == URLAUB:
                self.urlaubstation += 1
                self.ziehezu(self.urlaubstation, urlaubpos)
                if self.urlaubstation == len(urlaubpos) - 1:
                    # playsound(feld_sound[URLAUBSENDE], False)
                    self.reiseende(REISEENDEURLAUB)
            elif self.bahn == KONFERENZ:
                self.konferenzstation += 1
                self.ziehezu(self.konferenzstation, konferenzpos)
                if self.konferenzstation == len(konferenzpos) - 1:
                    self.reiseende(REISEENDEKONFERENZ)
            elif self.bahn == DIENSTREISE:
                self.dienstreisestation += 1
                self.ziehezu(self.dienstreisestation, dienstreisepos)
                if self.dienstreisestation == len(dienstreisepos) - 1:
                    self.reiseende(REISEENDEDIENSTREISE)
        if self.tanker:
            #warteaufklick(screen)
            spielfeld.changezoommode(ZOOMFULL)
            # print("Tanker bewegen")
            self.tankerbewegen()

        self.kannbeenden = True

    def ziehezu(self, station, liste):
        playsound(mixer.Sound("Sounds/Mitteilungen/reisestationweiter.mp3"), False)
        steps = 20
        oldpos = liste[station - 1]
        newpos = liste[station]
        # print("Zug von Pos: ", station - 1, " nach ", station)
        # print("von Koordinaten ", oldpos, " nach ", newpos)
        dx = (newpos[0] - oldpos[0]) / steps
        dy = (newpos[1] - oldpos[1]) / steps
        for i in range(steps + 1):
            self.x = int(oldpos[0] + i * dx) + deltadienstreise[self.nummer][0]
            self.y = int(oldpos[1] + i * dy) + deltadienstreise[self.nummer][1]
            drawallelements(True, False)

    def reset_werte_beim_wuerfeln(self):
        self.setze_notonboerse()  # Beim Würfeln sollen sofort wieder die +/- Symbole verschwinden
        self.setze_noprobebohrung()
        self.setze_noquellekaufen()
        self.onboersemodus = NORMALPREIS  # wenn die Boerse mit einem Würfelzug erreicht wird, ist es immer Normalpreis

    def wuerfeln(self):
        wurf = 0
        self.reset_werte_beim_wuerfeln()
        fertig = False
        mousepressed = False
        while fertig == False:
            pg.event.pump()
            mousebutton = pg.mouse.get_pressed()
            if mousebutton[0]:
                mousepressed = True
                wurf = wurf % 6 + 1
                console.changewuerfel(wurf)
                sleep(0.01)
            elif mousepressed == True:
                fertig = True
        return wurf

    def dividendenausschuettung(self, raff, tank):
        for _ in range(self.raffinerieaktien):
            self.erhalten(raff)

        for _ in range(self.tankschiffaktien):
            self.erhalten(tank)

    def aktienausschuettung(self, typ):
        x_start = 800
        y_start = 570
        x_end = 1524 + typ * 200
        y_end = 350
        steps = 25
        dx = (x_end - x_start) / steps
        dy = (y_end - y_start) / steps

        image = pg.transform.scale(Aktienimages[typ], (0.5 * Aktienimages[typ].get_width(), 0.5 * Aktienimages[typ].get_height()))
        if typ == RAFFINERIE:
            anz = self.raffinerieaktien // 2
        else:
            anz = self.tankschiffaktien // 2
        if self == spieler[game.aktspieler]:
            for _ in range(0, anz):
                for cnt in range(steps+1):
                    drawallelements(True, True, False)
                    screen.blit(image, (int(x_start + cnt * dx), int(y_start + cnt * dy)))
                    pg.display.update()
                drawallelements(False, True)

        self.aktienkaufen(typ, anz, GRATIS)

    def get_quelle(self, init=False):
        qnr = 0
        if Oelquelle.anzahl_quellen < 18:
            ok = False
            while not ok:  # erst wenn eine freie Quelle gefunden und vergeben wurde, dann ok
                if init:
                    qnr = random.randint(1, 9)
                else:
                    qnr = random.randint(1, 18)
                if not Oelquelle.quelle_vergeben[qnr]:
                    self.oelquellen.append(Oelquelle(qnr, self.nummer, screen,game))  # und dem aktuellen Spieler zugewiesen
                    ok = True
            besitzkarte.zeigekarte(qnr)
            return qnr
        else:
            print("Es sind bereits alle Ölquellen vergeben")

    def draw(self):
        breite = 0
        hoehe = 0
        self.image = pg.transform.scale(self.imageorig, (
            int(FIGURZOOMSCALE[self.bereich][game.zoommode] * ZOOMSCALE[game.zoommode] * self.imageorig.get_width()), int(FIGURZOOMSCALE[self.bereich][game.zoommode] * ZOOMSCALE[game.zoommode] * self.imageorig.get_height())))
        self.imagerect = self.image.get_rect()
        if self.bereich == ZOOMFULL:
            if self.bahn == AUSSENBAHN:
                self.imagerect.x = self.x * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0] + Deltabereich[game.zoommode][self.nummer] * ZOOMSCALE[game.zoommode]
                self.imagerect.y = self.y * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1] + Fixdy[game.zoommode] * ZOOMSCALE[game.zoommode]
            else:
                self.imagerect.x = self.x * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0]
                self.imagerect.y = self.y * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1]
        if self.bereich == ZOOMBOHRUNG:
            self.imagerect.x = self.x * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0] + Deltabohr[game.zoommode][self.nummer] * ZOOMSCALE[game.zoommode]
            self.imagerect.y = self.y * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1] + Fixdybohr[game.zoommode] * ZOOMSCALE[game.zoommode]
        if self.imagerect.x + self.imagerect.width > 1514:
            breite = 1514 - self.imagerect.x
        else:
            breite = self.imagerect.width
        if self.imagerect.y + self.imagerect.height > 1078:
            hoehe = 1078 - self.imagerect.y
        else:
            hoehe = self.imagerect.height
        if breite > 0:
            screen.blit(self.image, self.imagerect, (0, 0, breite, hoehe))

        for quelle in self.oelquellen:
            quelle.draw()

    def oelfoerderung(self):
        mitgeteilt = False
        if not self.foerderstop:  # wenn der Spieler das Föderstop-Memo hat, dann keine Förderung
            for quelle in self.oelquellen:
                quelle.foerderung(self)
                drawallelements(True)
                if quelle.istankvoll() and not mitgeteilt:
                    mitgeteilt = True
                    playsound(tank_voll_sound[quelle.hafen], False)
                    playsound(verschiffen_sound, False)
        else:
            playsound(foerderstop, False)

    def aufschlussbohrung(self):
        self.probebohrung_preis = 140000
        self.darfprobebohrung = True
        drawallelements(False, True)

    def hubschrauber(self):
        self.probebohrung_preis = 40000
        self.darfprobebohrung = True
        drawallelements(False, True)

    def bohrungdurchfuehren(self):
        self.setze_noprobebohrung()
        self.bezahlen(self.probebohrung_preis)
        self.bereich = ZOOMBOHRUNG
        self.setzeaufbohrloch()
        drawallelements(True, True)

    def quellevonbankkaufen(self):
        self.setze_noquellekaufen()
        spielfeld.changezoommode(ZOOMBESITZKARTEN)
        self.bezahlen(200000)
        nr = self.get_quelle()
        playsound(mixer.Sound("Sounds/Ölquelle/" + str(nr) + ".mp3"), False)

        spielfeld.changezoommode(ZOOMFULL)
        drawallelements(True, True)

    def verkaufsangebot(self):
        self.darfquellekaufen = True
        drawallelements(False, True)

    def landauswaehlen(self, rate):
        self.landauswahl = True
        playsound(esgiltfrachtrate[rate - 1], False)
        drawallelements(True, True)

    def tankerstarten(self, landnr):
        print("Tanker wird gestartet")
        self.landauswahl = False
        self.tanker.append(Tanker(self, landnr))  # self.nummer
        self.tankeristunterwegs = True
        print("Tanker ist unterwegs")
        drawallelements(True, False)

    def tankerbewegen(self):
        # 1. alle tanker bewegen
        for tkr in self.tanker:
            # print("ein tanker wird bewegt")
            tkr.zug(self.wurf)

            # 2. alle tanker, die das ziel erreicht haben löschen
        for i in reversed(range(len(self.tanker))):
            if self.tanker[i].zielerreicht:
                playsound(mixer.Sound("Sounds/Verschiffen/Ziel" + zieltext[self.tanker[i].zielhafen] + ".mp3"), False)
                playsound(mixer.Sound("Sounds/Verschiffen/Gewinn" + str(game.rate) + ".mp3"), False)
                playsound(mixer.Sound("Sounds/Beträge/" + str(self.tanker[i].gewinn[game.rate - 1]) + ".mp3"), False)
                playsound(mixer.Sound("Sounds/Verschiffen/Dollar.mp3"), False)

                self.erhalten(self.tanker[i].gewinn[game.rate - 1])
                self.tanker.remove(self.tanker[i])
        drawallelements(True, True)

    def oelquelleversiegt(self):
        # ermittelt die Kuwait-Quelle mit dem  geringsten Tankvolumen uund gibt sie für 200000 an die Bank zurück
        versiegt = None
        for quelle in self.oelquellen:
            if quelle.hafen == MINA_AL_AHMADI:
                if versiegt is not None:
                    if quelle.tankstand < versiegt.tankstand:
                        versiegt = quelle
                else:
                    versiegt = quelle
        if versiegt is not None:
            playsound(mixer.Sound("Sounds/Ölquelle/versiegt/" + str(versiegt.nr) + ".mp3"), False)
            #versiegt.nimmquellezurueck()
            #game.nimmquellezurueck(versiegt.nr)
            self.oelquellen.remove(versiegt)
            versiegt.loeschen()
            self.erhalten(140000)
            drawallelements(True, True)
            return True
        else:
            return False

    def memoauswerten(self, karte):  # Memos betreffen nur den Spieler selbst, also hier auswerten
        typ = karte[1]
        wert = karte[2]
        if typ == PROQUELLE:
            if self.oelquellen:  #if len(self.oelquellen) > 0:
                playsound(mixer.Sound("Sounds/Mitteilungen/" + str(wert) + ".mp3"), False)
                for _ in self.oelquellen:
                    self.bezahlen(wert)
        if typ == RUECKVERGUETUNG:
            playsound(mixer.Sound("Sounds/Mitteilungen/erhälst 40000.mp3"), False)
            self.erhalten(wert)
        if typ == EINMALKOSTEN:
            if self.oelquellen:  #if len(self.oelquellen) > 0:
                playsound(mixer.Sound("Sounds/Mitteilungen/" + str(wert) + ".mp3"), False)
                self.bezahlen(wert)
        if typ == HAFENKOSTEN:
            kuwaitgefunden = False
            irakgefunden = False
            irangefunden = False
            qatargefunden = False
            trinidadgefunden = False
            irgendwasgefunden = False
            for quelle in self.oelquellen:
                if quelle.hafen == MINA_AL_AHMADI:
                    kuwaitgefunden = True
                    irgendwasgefunden = True
                if quelle.hafen == UMM_SAID:
                    qatargefunden = True
                    irgendwasgefunden = True
                if quelle.hafen == TRIPOLI:
                    irakgefunden = True
                    irgendwasgefunden = True
                if quelle.hafen == PORT_OF_SPAIN:
                    trinidadgefunden = True
                    irgendwasgefunden = True
                if quelle.hafen == BANDAR_MASHUR:
                    irangefunden = True
                    irgendwasgefunden = True
            if irgendwasgefunden:
                playsound(mixer.Sound("Sounds/Mitteilungen/du zahlst.mp3"), False)

            if kuwaitgefunden:
                self.bezahlen(150000)
                playsound(mixer.Sound("Sounds/Mitteilungen/150000 kuwait.mp3"), False)
            if irakgefunden:
                self.bezahlen(50000)
                playsound(mixer.Sound("Sounds/Mitteilungen/50000 irak.mp3"), False)

            if irangefunden:
                self.bezahlen(30000)
                playsound(mixer.Sound("Sounds/Mitteilungen/30000 iran.mp3"), False)

            if qatargefunden:
                self.bezahlen(30000)
                playsound(mixer.Sound("Sounds/Mitteilungen/30000 katar.mp3"), False)

            if trinidadgefunden:
                self.bezahlen(30000)
                playsound(mixer.Sound("Sounds/Mitteilungen/30000 trinidad.mp3"), False)

        if typ == ZUHUBSCHRAUBER:
            # warteaufklick(screen)
            playsound(mixer.Sound("Sounds/Mitteilungen/zuHubschrauber.mp3"), False)
            spielfeld.changezoommode(self.bereich)
            if self.pos < 12:  # Start bis Hubschrauber
                self.zug(12 - self.pos)
                drawallelements(True, False)
            elif self.pos < 18:
                self.zug(18 - self.pos, False)
                self.zug(12)
                drawallelements(True, False)
            elif self.pos < 30:
                self.zug(30 - self.pos)
            else:
                self.zug(36 - self.pos)
                self.zug(12)
                drawallelements(True, False)
        if typ == ZUOELFOERDERUNG:
            playsound(mixer.Sound("Sounds/Mitteilungen/zuÖlförderung.mp3"), False)
            spielfeld.changezoommode(self.bereich)
            if self.pos < 5:  # vor dem unteren Feld
                self.zug(5 - self.pos)
            elif self.pos < 10:  # nach dem unteren Feld aber noch auf unterer Bahn
                self.zug(10 - self.pos, False)
                self.zug(13)
            elif self.pos < 23:  # auf oberer Bahn Vor Feld
                self.zug(23 - self.pos)
            elif self.pos < 28:  # auf oberer Bahn nach Feld
                self.zug(28 - self.pos, False)
                self.zug(8)
                self.zug(5)
            else:
                self.zug(36 - self.pos)
                self.zug(5)
        if typ == BOERSEHALBERPREIS:
            playsound(mixer.Sound("Sounds/Mitteilungen/zur Börse Aktien halber Preis kaufen.mp3"), False)
            spielfeld.changezoommode(self.bereich)
            if self.pos < 10:
                self.zug(10 - self.pos)
                drawallelements(True, False)
            elif self.pos < 18:
                self.zug(18 - self.pos)
            elif self.pos < 28:
                self.zug(28 - self.pos)
                drawallelements(True, False)
            else:
                self.zug(36 - self.pos)
                self.zug(10)
                drawallelements(True, False)
            self.onboersemodus = HALBERPREIS
        if typ == FOERDERSTOP:
            # print("Förderstop")
            self.foerderstop = True
            self.doppeltefoerderung = False
        if typ == DOPPELFOERDERUNG:
            self.doppeltefoerderung = True
            self.foerderstop = False
        drawallelements(False, True)
        pg.display.flip()

    def aktienkaufen(self, typ, anzahl, boersemodus):
        preisart = boersemodus
        if boersemodus == ZWANGHALBERPREIS:
            preisart = 1
        if typ == RAFFINERIE and (self.geld >= 80000 / preisart or preisart == GRATIS):
            for _ in range(anzahl):
                self.raffinerieaktien += 1
                if preisart != GRATIS:
                    self.bezahlen(80000 // preisart)
        if typ == TANKSCHIFF and (self.geld >= 50000 / preisart or preisart == GRATIS):
            for _ in range(anzahl):
                self.tankschiffaktien += 1
                if preisart != GRATIS:
                    self.bezahlen(50000 // preisart)
        drawallelements(False, True)
        pg.display.flip()

    def aktienverkaufen(self, typ, anzahl, boersemodus):
        if typ == EGAL or (typ == RAFFINERIE and self.raffinerieaktien > 0) or (typ == TANKSCHIFF and self.tankschiffaktien > 0):
            if boersemodus == ZWANGHALBERPREIS:
                preisart = 2
                typ = TANKSCHIFF
                anz = self.tankschiffaktien
                if anz < 2:  # nicht genügend Tankeraktien, also bei Raffinerieaktien schauen
                    typ = RAFFINERIE
                    anz = self.raffinerieaktien
                if anz < 2:  # auch nicht genug Raffinerieaktien
                    anz = 0
                else:
                    anz = 2
            else:
                anz = anzahl
                preisart = boersemodus
            if anz > 0:
                if typ == RAFFINERIE:
                    self.raffinerieaktien -= anz
                    self.erhalten(anz * (80000 // preisart))
                if typ == TANKSCHIFF:
                    self.tankschiffaktien -= anz
                    self.erhalten(anz * (50000 // preisart))
            drawallelements(False, True)
            pg.display.flip()

    def memo(self):
        spielfeld.changezoommode(ZOOMMEMO)
        karte = memo.zeigekarte()
        self.memoauswerten(karte)

    def information(self):
        spielfeld.changezoommode(ZOOMINFORMATION)
        information.zeigekarte()

    def urlaubsanfang(self):
        self.ontour = True
        self.urlaubstation = 1
        self.bahn = URLAUB
        self.x = urlaubpos[1][0] + deltaurlaub[self.nummer][0]
        self.y = urlaubpos[1][1] + deltaurlaub[self.nummer][1]
        self.draw()

    def reiseende(self, feldpos):
        self.ontour = False
        self.urlaubstation = 0
        self.konferenzstation = 0
        self.dienstreisestation = 0
        self.bahn = AUSSENBAHN
        self.pos = feldpos
        self.x = FeldPos[self.pos][0]
        self.y = FeldPos[self.pos][1]
        drawallelements(True, False)

    def konferenz(self):
        self.ontour = True
        self.konferenzstation = 1
        self.bahn = KONFERENZ
        self.x = konferenzpos[1][0] + deltakonferenz[self.nummer][0]
        self.y = konferenzpos[1][1] + deltakonferenz[self.nummer][1]
        drawallelements(True, False)

    def dienstreise(self):
        self.ontour = True
        self.dienstreisestation = 1
        self.bahn = DIENSTREISE
        self.x = dienstreisepos[1][0] + deltadienstreise[self.nummer][0]
        self.y = dienstreisepos[1][1] + deltadienstreise[self.nummer][1]
        drawallelements(True, False)

    def feld_auswerten(self):
        self.onboerse = False
        feld = FELD[self.pos]

        if feld == MEMO:
            playsound(feld_sound[feld], False)
            self.memo()
        if feld == INFORMATION:
            playsound(feld_sound[feld], False)
            self.information()
        if feld == AUFSCHLUSSBOHRUNG:
            if self.geld >=140000:
                if Oelquelle.anzahl_quellen < 18:
                    playsound(feld_sound[feld], False)
                    self.aufschlussbohrung()
                else:
                    playsound(mixer.Sound("Sounds/Mitteilungen/keine Ölquellen verfügbar.mp3"), False)
            drawallelements(True, True)
        if feld == OELFOERDERUNG:
            if self.oelquellen:  #if len(self.oelquellen) > 0:
                playsound(feld_sound[feld], False)
                self.oelfoerderung()
            drawallelements(True, True)
        if feld == URLAUBSANFANG:
            playsound(feld_sound[feld], False)
            self.urlaubsanfang()
            drawallelements(True, False)
        if feld == BOERSE:
            playsound(feld_sound[feld], False)
            self.onboerse = True
            drawallelements(True, True)
        if feld == VERKAUFSANGEBOT:
            if self.geld >= 200000:
                if Oelquelle.anzahl_quellen < 18:
                    playsound(feld_sound[feld], False)
                    self.verkaufsangebot()
                else:
                    playsound(mixer.Sound("Sounds/Mitteilungen/keine Ölquellen verfügbar.mp3"), False)
            drawallelements(True, True)
        if feld == HUBSCHRAUBER:
            if self.geld >= 40000:
                if Oelquelle.anzahl_quellen < 18:
                    playsound(feld_sound[feld], False)
                    self.hubschrauber()
                else:
                    playsound(mixer.Sound("Sounds/Mitteilungen/keine Ölquellen verfügbar.mp3"), False)
            drawallelements(True, True)
        if feld == KONFERENZLONDON:
            playsound(feld_sound[feld], False)
            self.konferenz()
            drawallelements(True, False)
        if feld == ZURUECKZURBOERSE:
            if self.tankschiffaktien > 1 or self.raffinerieaktien > 1:
                playsound(feld_sound[feld], False)
                self.zug(-4)
                self.aktienverkaufen(EGAL, 2, ZWANGHALBERPREIS)

        if feld == URLAUBSENDE:
            drawallelements(True, False)
        if feld == OELQUELLEVERSIEGT:
            self.oelquelleversiegt()
            drawallelements(True, True)
        if feld == DIENSTREISESTART:
            playsound(feld_sound[feld], False)
            self.dienstreise()
            drawallelements(True, False)
        if feld == ZURBOERSE:
            playsound(feld_sound[feld], False)
            self.zug(1)
            self.zug(10)
            drawallelements(True, True)
        game.set_zugfertig()
        drawallelements(False, True)

    def bohrfeld_auswerten(self):
        feld = BOHRFELD[self.bohrpos]
        playsound(bohrfeld_sound[feld], False)
        if feld == GLATTERVERLAUF:
            self.bohrzug(4)
        if feld == NICHTFUENDIG:
            self.bereich = ZOOMFULL
            self.setzeaufspielfeld()
        if feld == BOHRMEISSELGEBROCHEN:
            self.bezahlen(40000)
        if feld == FUENDIG:
            spielfeld.changezoommode(ZOOMBESITZKARTEN)
            nr = self.get_quelle()
            playsound(mixer.Sound("Sounds/Ölquelle/" + str(nr) + ".mp3"), False)

            self.bereich = ZOOMFULL
            self.setzeaufspielfeld()
        game.set_zugfertig()

    def bezahlen(self, betrag):
        self.geld -= betrag
        if self.geld < 0:
            self.zahlungsunfaehig = True
            self.geld = 0

    def erhalten(self, betrag):
        self.geld += int(betrag)

    def setzeaufbohrloch(self):
        self.bohrpos = 0
        self.x = BohrFeldPos[self.bohrpos][0]
        self.y = BohrFeldPos[self.bohrpos][1]
        self.figur_aufbohrloch = True
        self.figur_aufspielfeld = False
        playsound(bohrfeld_sound[0], False)

    def setzeaufspielfeld(self):
        # self.pos=0
        self.x = FeldPos[self.pos][0]
        self.y = FeldPos[self.pos][1]
        self.figur_aufbohrloch = False
        self.figur_aufspielfeld = True

    def zug(self, count, auswerten=True):
        self.oldpos = self.pos
        self.newpos = ((self.oldpos + count) % 36)
        if self.newpos == 0 or self.oldpos + count > 35:
            self.doppeltefoerderung = False
            self.foerderstop = False
            drawallelements(False, True)
            pg.display.flip()

        self.pos = self.newpos

        fertig = False
        while not fertig:
            # Je nach Position der Spielfigur wird sie erst in x oder y-Richtung bewegt und dann in der anderen
            if self.y == 2023 and self.x > FeldPos[self.newpos][0]:
                self.dx = -SCHRITTWEITE
                self.dy = 0
            elif self.newpos > self.oldpos and (self.y == 100 and self.x < FeldPos[self.newpos][0]):
                self.dx = SCHRITTWEITE
                self.dy = 0
            elif self.newpos < self.oldpos and (self.y == 100 and self.x > FeldPos[self.newpos][0]):
                self.dx = -SCHRITTWEITE
                self.dy = 0
            elif self.x == 140 and self.y > FeldPos[self.newpos][1]:
                self.dx = 0
                self.dy = -SCHRITTWEITE
            elif self.x == 2910 and self.y < FeldPos[self.newpos][1]:
                self.dx = 0
                self.dy = SCHRITTWEITE
            else:  # Ziel erreicht
                fertig = True
            if not fertig:
                self.x += self.dx
                self.y += self.dy
                if self.x < 140:
                    self.x = 140
                if self.x > 2910:
                    self.x = 2910
                if self.y < 100:
                    self.y = 100
                if self.y > 2023:
                    self.y = 2023
                if (abs(FeldPos[self.newpos][0] - self.x) < SCHRITTWEITE) and (abs(FeldPos[self.newpos][1] - self.y) < SCHRITTWEITE):
                    self.x = FeldPos[self.newpos][0]
                    self.y = FeldPos[self.newpos][1]
            drawallelements(True, False)

        self.x = FeldPos[self.newpos][0]
        self.y = FeldPos[self.newpos][1]
        drawallelements(True, False)

        if (self.oldpos < 5 < self.newpos) or (self.oldpos < 23 < self.newpos):
            self.oelfoerderung()
        if auswerten:
            self.feld_auswerten()

    def bohrzug(self, count):
        self.oldpos = self.bohrpos
        self.newpos = min(self.oldpos + count, 12)
        self.bohrpos = self.newpos
        self.x = BohrFeldPos[self.oldpos][0]
        self.y = BohrFeldPos[self.oldpos][1]
        fertig = False
        self.dy = SCHRITTWEITE / 5
        while not fertig:
            # Je nach Position der Spielfigur wird sie erst in x oder y-Richtung bewegt und dann in der anderen
            self.y += self.dy
            if self.y >= BohrFeldPos[self.newpos][1]:
                self.y = BohrFeldPos[self.newpos][1]
                fertig = True
            drawallelements(True, False)

        self.bohrfeld_auswerten()


class Spielfeld:
    def __init__(self):
        self.spielfeldimageorig = imgSpielfeld
        self.spielfeldimage = pg.transform.scale(self.spielfeldimageorig, (ZOOMSCALE[game.zoommode] * self.spielfeldimageorig.get_width(), ZOOMSCALE[game.zoommode] * self.spielfeldimageorig.get_height()))
        self.spielfeldimagerect = self.spielfeldimage.get_rect()
        self.ausschnitt = None

    def changezoommode(self, mode):
        akt_zoommode = game.getzoommode()
        scalediff = 0
        posxdiff = 0
        posydiff = 0
        scaletemp = 0
        xtemp = 0
        ytemp = 0
        steps = 10
        if akt_zoommode != mode:
            #self.spielfeldimageorig = imgSpielfeld
            scalediff = (ZOOMSCALE[mode] - ZOOMSCALE[akt_zoommode]) / steps
            posxdiff = (ZOOMPOSDELTA[mode][0] - ZOOMPOSDELTA[akt_zoommode][0]) / steps
            posydiff = (ZOOMPOSDELTA[mode][1] - ZOOMPOSDELTA[akt_zoommode][1]) / steps
            scaletemp = ZOOMSCALE[akt_zoommode]
            xtemp = self.spielfeldimagerect.x
            ytemp = self.spielfeldimagerect.y
            for i in range(steps + 1):
                self.spielfeldimage = pg.transform.scale(self.spielfeldimageorig, ((scaletemp + i * scalediff) * self.spielfeldimageorig.get_width(), (scaletemp + i * scalediff) * self.spielfeldimageorig.get_height()))
                self.spielfeldimagerect = self.spielfeldimage.get_rect()
                self.spielfeldimagerect.x = int(xtemp + i * posxdiff)
                self.spielfeldimagerect.y = int(ytemp + i * posydiff)
                self.ausschnitt = (0 - self.spielfeldimagerect.x, 0 - self.spielfeldimagerect.y, 1514, 1078)
                self.draw()
                pg.display.flip()
            game.setzoommode(mode)
            drawallelements(True, False)  # Update nur auf Spielfeld

    def draw(self):
        screen.blit(self.spielfeldimage, (0, 0), self.ausschnitt)  # self.spielfeldimagerect

    def drawfrachtrate(self):
        pg.draw.circle(screen, COLOR[BLACK], (int((2171 + 48 * game.rate) * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0]), int(924 * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1])),
                       ZOOMSCALE[game.zoommode] * 10, 0)
        pg.draw.circle(screen, COLOR[WHITE], (int((2171 + 48 * game.rate) * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][0]), int(924 * ZOOMSCALE[game.zoommode] + ZOOMPOSDELTA[game.zoommode][1])),
                       ZOOMSCALE[game.zoommode] * 7, 0)

    # drawallelements(False, True)
    def wechselezueinfachemFeld(self):
        self.spielfeldimageorig = imgSpielfeldeinfach
        self.spielfeldimage = pg.transform.scale(self.spielfeldimageorig, (ZOOMSCALE[game.zoommode] * self.spielfeldimageorig.get_width(), ZOOMSCALE[game.zoommode] * self.spielfeldimageorig.get_height()))
        self.spielfeldimagerect = self.spielfeldimage.get_rect()



def drawallelements(sp=True, co=True, flip=True):
    if sp:
        spielfeld.draw()
        if game.anzahl_vergeben < 18:
            besitzkarte.drawstapel()
        spielfeld.drawfrachtrate()

        for sp in spieler:
            sp.draw()
            for tkr in sp.tanker:
                tkr.draw()
    if co:
        console.draw()
    if flip:
        pg.display.flip()


def main():
    random.seed()
    # hier Spielinitialisierung
    for i in range(game.anzahlspieler):
        spieler.append(Spieler(i, HUMAN))  # Test: nur ein menschlicher Spieler
        spieler[i].get_quelle(True)

    if game.iseinfach():
        FELD[29]=7
        BOHRFELD[4]=1
        spielfeld.wechselezueinfachemFeld()
    mousepressed = False

    # ab hier läuft das Spiel
    game.setzemode(SPIELRUN)
    spielfeld.changezoommode(ZOOMFULL)

    anderreihe = 0
    spiellaeuft = True
    while spiellaeuft:
        # ab hier ein neuer Zug
        # 1. Spielfeld auf den aktuellen Spieler zoomen
        game.setzeaktspieler(anderreihe)
        spielfeld.changezoommode(spieler[anderreihe].bereich)
        spieler[game.aktspieler].setze_nokannbeenden()
        if game.Mode == SPIELRUN:
            drawallelements(True, True)
        zuggestartet = False
        zugbeendet = False

        playsound(amzug_sound[anderreihe], False)  # Spieler X ist am Zug Sound ab
        if spieler[game.aktspieler].ontour and not spieler[game.aktspieler].tanker:  # nur automatisch Urlaub weiterziehen, wenn keine Tanker unterwegs sind
            zuggestartet = True
            zugbeendet = False

            spieler[anderreihe].spielzugstarten()
            drawallelements(False, True)
            mousepressed = False
#            anderreihe = (anderreihe + 1) % game.anzahlspieler

        while not zugbeendet:  # während noch nichts passiert, Events abfragen

            for event in pg.event.get():
                if event.type == QUIT or event.type == BUTTON_CLOSE_PRESSED:
                    pg.quit()
                    sys.exit()

                if event.type == BUTTON_PLUS1_PRESSED:
                    if (spieler[game.aktspieler].onboersemodus == HALBERPREIS and spieler[game.aktspieler].geld >= 40000) or \
                            (spieler[game.aktspieler].onboersemodus != HALBERPREIS and spieler[game.aktspieler].geld >= 80000):
                        spieler[game.aktspieler].aktienkaufen(RAFFINERIE, 1, spieler[game.aktspieler].onboersemodus)

                if event.type == BUTTON_PLUS2_PRESSED:
                    if (spieler[game.aktspieler].onboersemodus == HALBERPREIS and spieler[game.aktspieler].geld >= 25000) or \
                            (spieler[game.aktspieler].onboersemodus != HALBERPREIS and spieler[game.aktspieler].geld >= 50000):
                        spieler[game.aktspieler].aktienkaufen(TANKSCHIFF, 1, spieler[game.aktspieler].onboersemodus)

                if event.type == BUTTON_MINUS1_PRESSED:
                    spieler[game.aktspieler].aktienverkaufen(RAFFINERIE, 1, spieler[game.aktspieler].onboersemodus)

                if event.type == BUTTON_MINUS2_PRESSED:
                    spieler[game.aktspieler].aktienverkaufen(TANKSCHIFF, 1, spieler[game.aktspieler].onboersemodus)

                if event.type == BUTTON_WUERFELMATTE_PRESSED:
                    if not zuggestartet:
                        spieler[game.aktspieler].setze_nolandauswahl()
                        zuggestartet = True
                        zugbeendet = False
                        spieler[anderreihe].spielzugstarten()
                        drawallelements(False, True)
                        mousepressed = False
                if event.type == BUTTON_ZUGBEENDEN_PRESSED:
                    if zuggestartet:
                        zugbeendet = True
                        if spielzuende(spieler):
                            spielende.show()
                            spiellaeuft = False

                        zuggestartet = False
                        spieler[game.aktspieler].setzealleszurueck()
                        anderreihe = (anderreihe + 1) % game.anzahlspieler

                if event.type == BUTTON_PROBEBOHRUNG_PRESSED:
                    spieler[game.aktspieler].bohrungdurchfuehren()

                if event.type == BUTTON_QUELLEKAUFEN_PRESSED:
                    spieler[game.aktspieler].quellevonbankkaufen()

                if event.type == BUTTON_TANKERSTARTEN_PRESSED:
                    spielfeld.changezoommode(ZOOMFULL)
                    spieler[game.aktspieler].landauswaehlen(game.rate)

                for i in range(5):
                    if event.type == 13 + i:
                        if spieler[game.aktspieler].hatgenugoel(i):
                            spieler[game.aktspieler].tankerstarten(i)

                if event.type == MOUSEBUTTONUP:
                    mousepressed = False

            # Mausklicks abfragen
            pg.event.pump()
            mousebutton = pg.mouse.get_pressed()
            if mousebutton[0]:
                if not mousepressed:
                    mousepressed = True
                    console.checkselection()


if __name__ == "__main__":
    titelbild = Titelbild(screen)
    titelbild.einblenden()
    titelbild.begruessen()
    while True:
        spieler = []

        game = Game()
        spielende = Spielende(screen, game, spieler)
        console = Console(screen, game, spieler)
        spielfeld = Spielfeld()
        besitzkarte = Besitzkarte(screen, game)
        memo = Memo()
        information = Information()

        wert = titelbild.waehlespielerzahl()
        game.setzeanzahlspielerundModus(wert)


        titelbild.ausblenden()
        main()
        titelbild.einblenden()

        del game
        del spielende
        del console
        del spielfeld
        del besitzkarte
        del memo
        del information
        del spieler
