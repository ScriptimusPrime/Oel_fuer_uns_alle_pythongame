from pygame import *

# Scale-Größen
ZOOMFULL = 0
ZOOMBOHRUNG = 1
ZOOMMEMO = 2
ZOOMINFORMATION = 3
ZOOMBESITZKARTEN = 4
ZOOMSCALE = (0.505, 1.25, 1.2, 1.5, 1.2)  # Spielfeldvergrößerung bei verschiedenen Zooms
ZOOMPOSDELTA = ((0, 0), (-2087, -200), (-1350, -1484), (-2986, -1300), (-300, -1482))  # Spielfeldverschiebung bei verschiedenen Zooms
FIGURZOOMSCALE = ((0.4, 0.4, 0.35, 0.4, 0.35),(0.4, 0.16, 0.35, 0.33, 0.35))

AUSSENBAHN = 0
URLAUB = 1
KONFERENZ = 2
DIENSTREISE = 3

# Individuelle Verschiebung der Figuren auf einem Spielfeld

# Verschiebungen der einzelnen Figuren zueinander, wenn Figur sich im ZOOMFULL-Modus befindet
#  Spielzoom:   ZOOMFULL f           ZOOMBOHRUNG f       ZOOMMEMO             ZOOMINFORMATION    ZOOMBESITZKARTEN
Deltabereich = ((-125, -70, -15, 40),(-125, -70, -15, 40),(-125, -70, -15, 40),(-125, -70, -15, 40),(-125, -70, -15, 40))
Fixdy =                (10,                 10,               10,                    10,                   10)

# Verschiebungen der einzelnen Figuren zueinander, wenn Figur sich im ZOOMBOHRUNG-Modus befindet
#  Spielzoom:  ZOOMFULL            ZOOMBOHRUNG f       ZOOMMEMO             ZOOMINFORMATION    ZOOMBESITZKARTEN
Deltabohr = ((-37,-25,-13,-1),(-20, -12, -4, 4),(-37,-25,-13,-1),(-37,-25,-13,-1),(-37,-25,-13,-1))
#Fixdybohr =  (        0,                0,               0,             0,              0)
Fixdybohr =  (        -75,            -18,              -75,           -55,              -75)

Fixdymarker = 2

# GameMode-Phasen
SPIELINIT = 2
SPIELRUN = 3
SPIELENDE = 4

# Spielfigurfarben
SPIELERFARBE = ("rot", "gelb", "blau", "grün")
HUMAN = 0
COMPUTER = 1

RED = 0
YELLOW = 1
BLUE = 2
GREEN = 3
BLACK = 4
GREY = 5
WHITE = 6

COLOR = ((255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0), (200, 200, 200), (255, 255, 255))

# Spielfeldtypen
START = 0
MEMO = 1
AUFSCHLUSSBOHRUNG = 2
INFORMATION = 3
OELFOERDERUNG = 4
URLAUBSANFANG = 5
BOERSE = 6
VERKAUFSANGEBOT = 7
HUBSCHRAUBER = 8
KONFERENZLONDON = 9
ZURUECKZURBOERSE = 10
URLAUBSENDE = 11
OELQUELLEVERSIEGT = 12
DIENSTREISESTART = 13
ZURBOERSE = 14

# Felder Aufschlussbohrung
ANFANG = 0
NIX = 1
GLATTERVERLAUF = 2
NICHTFUENDIG = 3
BOHRMEISSELGEBROCHEN = 4
FUENDIG = 5

# Spielermodi
STANDING = 0
MOVING = 1

# Spielbereiche
VOLLSPIELFELD = 0
BOHRSPIELFELD = 1

SCHRITTWEITE = 15

# Spielfeldreihenfolge
BOHRFELD = [0, 1, 1, 2, 3, 1, 4, 1, 1, 3, 1, 1, 5]
BohrFeldPos = ((2586, 307), (2586, 357), (2586, 407), (2586, 458), (2586, 510), (2586, 561), (2586, 611), (2586, 663), (2586, 713), (2586, 767), (2586, 817), (2586, 867), (2586, 917))
FELD = [0, 1, 2, 3, 1, 4, 5, 3, 2, 1, 6, 7, 8, 1, 2, 3, 9, 1, 6, 3, 2, 1, 10, 4, 11, 1, 2, 3, 6, 12, 8, 3, 2, 13, 3, 14]
FeldPos = ((2910, 2023), (2620, 2023), (2390, 2023), (2157, 2023), (1926, 2023), (1525, 2023), (1126, 2023), (890, 2023), (660, 2023), (430, 2023), (140, 2023),
           (140, 1757), (140, 1527), (140, 1300), (140, 1070), (140, 835), (140, 605), (140, 375), (140, 100),
           (430, 100), (660, 100), (890, 100), (1126, 100), (1525, 100), (1926, 100), (2157, 100), (2390, 100), (2620, 100), (2910, 100),
           (2910, 375), (2910, 605), (2910, 835), (2910, 1070), (2910, 1300), (2910, 1527), (2910, 1757))

# Aktienpakete
RAFFINERIE = 0
TANKSCHIFF = 1

EGAL = 2

Aktienwert = (50000, 80000)
GRATIS = 4
NORMALPREIS = 1
HALBERPREIS = 2
ZWANGHALBERPREIS = 3

# Info-Karten
FRACHTRATE = 1  # erledigt
SUEZGESPERRT = 2
AKTIEN = 3
DIVIDENDEN = 4

Infokarten = [[1, FRACHTRATE, 1, 0], [2, FRACHTRATE, 3, 0], [3, FRACHTRATE, 4, 0], [4, FRACHTRATE, 2, 0],[8, FRACHTRATE, 1, 0],
              [5, FRACHTRATE, 4, 0], [6, SUEZGESPERRT, 0, 0], [7, FRACHTRATE, 2, 0], [8, FRACHTRATE, 1, 0],[3, FRACHTRATE, 4, 0],
              [9, AKTIEN, RAFFINERIE, 0], [10, AKTIEN, TANKSCHIFF, 0], [11, FRACHTRATE, 3, 0], [12, FRACHTRATE, 2, 0], [2, FRACHTRATE, 3, 0], [3, FRACHTRATE, 4, 0],
              [13, FRACHTRATE, 2, 0], [14, DIVIDENDEN, 0, 0], [15, DIVIDENDEN, 1, 0], [14, DIVIDENDEN, 0, 0],
              [15, DIVIDENDEN, 1, 0],[16, FRACHTRATE, 3, 0],[6, SUEZGESPERRT, 0, 0]]

# Memo-Karten
PROQUELLE = 1  # erledigt
FOERDERSTOP = 2
OELTRANSPORT = 3
EINMALKOSTEN = 4  # erledigt
BOERSEHALBERPREIS = 5
FEUERANBORD = 6
ZUHUBSCHRAUBER = 7
HAFENKOSTEN = 8  # erledigt
SCHUERFKONZESSION = 9
DOPPELFOERDERUNG = 10
KOSTENBEITRANSSPORT = 11
ZUOELFOERDERUNG = 12
RUECKVERGUETUNG = 13  # erledigt

Memokarten = [[1, PROQUELLE, 40000, 0], [2, PROQUELLE, 50000, 0], [3, FOERDERSTOP, 0, 0], [4, RUECKVERGUETUNG, 40000, 0],
              [6, EINMALKOSTEN, 100000, 0], [7, BOERSEHALBERPREIS, 0, 0], [9, ZUHUBSCHRAUBER, 0, 0], [9, ZUHUBSCHRAUBER, 0, 0],[4, RUECKVERGUETUNG, 40000, 0],
              [10, HAFENKOSTEN, 0, 0], [12, DOPPELFOERDERUNG, 0, 0], [12, DOPPELFOERDERUNG, 0, 0], [13, PROQUELLE, 30000, 0], [15, ZUOELFOERDERUNG, 0, 0],
              [15, ZUOELFOERDERUNG, 0, 0], [16, PROQUELLE, 50000, 0], [7, BOERSEHALBERPREIS, 0, 0]]
# Karten ausgelassen: [5, OELTRANSPORT, 0, 0],  [11, SCHUERFKONZESSION, 0, 0], [15, ZUOELFOERDERUNG, 0, 0], [14, KOSTENBEITRANSSPORT, 0, 0][8, FEUERANBORD, 0, 0],


# Verschiffungshäfen
MINA_AL_AHMADI = 0
TRIPOLI = 1
UMM_SAID = 2
BANDAR_MASHUR = 3
PORT_OF_SPAIN = 4
min_oelstand = (27000,18000,9000,9000,9000)

# Ölquellendaten
nummer = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
leistung = (0, 9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000, 6000, 6000, 6000, 6000, 6000, 3000, 3000, 3000, 3000)
maxtank = (0, 45000, 45000, 45000, 45000, 45000, 45000, 45000, 45000, 45000, 42000, 42000, 42000, 42000, 42000, 45000, 45000, 45000, 45000)
wert = (0, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 400000, 400000, 400000, 400000, 400000, 200000, 200000, 200000, 200000)
hafen = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 4)
hafentext = ("Mina al Ahmadi", "Tripoli", "Umm Said", "Bandar Mashur", "Port of Spain")

# Abstecher
urlaubpos=((0,0),(1068,1936),(1283,1678),(1146,763),(1836,186))
konferenzpos = ((0,0),(198,606),(1116,703),(1098,196))
dienstreisepos = ((0,0),(2791,1296),(2268,1698),(2791,1706))
deltaurlaub =((-24,-70),(-14,-70),(-4,-70),(10,-70))
deltakonferenz = ((-24,-70),(-14,-70),(-4,-70),(10,-70))
deltadienstreise =((-24,-70),(-14,-70),(-4,-70),(10,-70))
REISEENDEURLAUB = 24
REISEENDEKONFERENZ = 22
REISEENDEDIENSTREISE = 35

BUTTON_PLUS = 0
BUTTON_MINUS = 1
WUERFELMATTE = 2
BUTTON_ZUGBEENDEN = 3
BUTTON_JA = 4
BUTTON_NEIN = 5
BUTTON_FERTIG = 6
BUTTON_TANKERSTARTEN = 7
BUTTON_PROBEBOHRUNG = 8
BUTTON_QUELLEKAUFEN = 9
BUTTON_KUWAIT = 10
BUTTON_IRAK = 11
BUTTON_QATAR = 12
BUTTON_IRAN = 13
BUTTON_TRINIDAD = 14
BUTTON_CLOSE = 15
BUTTON_EINSPIELER = 16
BUTTON_ZWEISPIELER = 17
BUTTON_DREISPIELER = 18
BUTTON_VIERSPIELER = 19
BUTTON_EINFACH = 20
BUTTON_ANLEITUNG = 21

BUTTON_PLUS1_PRESSED = USEREVENT + 1
BUTTON_MINUS1_PRESSED = USEREVENT + 2
BUTTON_PLUS2_PRESSED = USEREVENT + 3
BUTTON_MINUS2_PRESSED = USEREVENT + 4
BUTTON_WUERFELMATTE_PRESSED = USEREVENT + 5
BUTTON_ZUGBEENDEN_PRESSED = USEREVENT + 6
BUTTON_JA_PRESSED = USEREVENT + 7
BUTTON_NEIN_PRESSED = USEREVENT + 8
BUTTON_FERTIG_PRESSED = USEREVENT + 9
BUTTON_TANKERSTARTEN_PRESSED = USEREVENT + 10
BUTTON_PROBEBOHRUNG_PRESSED = USEREVENT + 11
BUTTON_QUELLEKAUFEN_PRESSED = USEREVENT + 12
BUTTON_KUWAIT_PRESSED = USEREVENT + 13
BUTTON_IRAK_PRESSED = USEREVENT + 14
BUTTON_QATAR_PRESSED = USEREVENT + 15
BUTTON_IRAN_PRESSED = USEREVENT + 16
BUTTON_TRINIDAD_PRESSED = USEREVENT + 17
BUTTON_CLOSE_PRESSED = USEREVENT + 18
BUTTON_EINSPIELER_PRESSED = USEREVENT + 19
BUTTON_ZWEISPIELER_PRESSED = USEREVENT + 20
BUTTON_DREISPIELER_PRESSED = USEREVENT + 21
BUTTON_VIERSPIELER_PRESSED = USEREVENT + 22
BUTTON_EINFACH_PRESSED = USEREVENT + 23
BUTTON_ANLEITUNG_PRESSED = USEREVENT + 24

DIALOG_BOHREN = 0
DIALOG_HANDELN = 1
# Minha al Hamadi nach Hamburg
Position=((1612,1016),(1752,1074),(1692,1158),(1585,1181),(1511,1119),(1463,1027),(1390,952),(1307,943),(1233,923),(1171,885),(1173,839),(1128,904),(1023,935),(924,896),(1003,811),(1111,737),(1199,695),
          (1822,1153),(1826,1256),(1862,1359),(1956,1411),(2053,1463),(2134,1536),(2198,1620),(2263,1698),
          (489,1177),(535,1106),(640,1084),(726,1020),(833,995),
          (1655,1259),(1593,1353),(1552,1452),(1514,1554),(1471,1649),(1389,1719),(1280,1678),(1187,1658),(1144,1543),(1095,1445),(1005,1385),(913,1336),(905,1230),(815,1171),(865,1076),(940,1001),
          (1469,945))
ziele = [[10,15,16,24],[10,15,16],[16,24],[15,16,24],[15]]  # Ziele von Starthäfen aus
starts = (0,46,0,0,25)
zieltext=("", "", "", "", "", "", "", "", "", "", "Lavera", "", "", "", "", "Kent", "Hamburg", "", "", "", "", "", "", "", "Kwinana")
# Häfen:
# Kuwait   - Mina al Ahmadi
# Irak     - Tripoli
# Qatar    - Umm Said
# Iran     - Bandar Mashur
# Trinidad - Port of Spain
Minimumoel = (27000,18000,9000,9000,9000)
Route=((0,1,2,3,4,5,6,7,8,9,10),                                                    # Route 0: Mina al Ahmadi/Umm Said/Bandar Mashur -> Lavera
       (0,1,2,3,4,5,6,7,8,9,11,12,13,14,15),                                        # Route 1: Mina al Ahmadi/Umm Said/Bandar Mashur -> Kent
       (0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16),                                     # Route 2: Mina al Ahmadi/Umm Said/Bandar Mashur -> Hamburg
       (0,1,17,18,19,20,21,22,23,24),                                               # Route 3: Mina al Ahmadi/Umm Said/Bandar Mashur -> Kwinana
       (46,6,7,8,9,10),                                                             # Route 4: Tripoli -> Lavera
       (46,6,7,8,9,11,12,13,14,15),                                                 # Route 5: Tripoli -> Kent
       (46,6,7,8,9,11,12,13,14,15,16),                                              # Route 6: Tripoli -> Hamburg
       (25,26,27,28,29,13,14,15),                                                   # Route 7: Port of Spain -> Kent
       (0,1,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),       # Route 8: Mina al Ahmad nach Lavera über Afrikaroute
       (0,1,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15),            # Route 9: Mina al Ahmad nach Kent über Afrikaroute
       (0,1,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16),         # Route 10: Mina al Ahmad nach Hamburg über Afrikaroute
       (1,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),         # Route 11: Mina al Ahmad nach Lavera über Afrikaroute
       (1,2,30,31,32,33,34,35,36,37,38,38,40,41,42,43,44,45,13,14,15),              # Route 12: Mina al Ahmad nach Kent über Afrikaroute
       (1,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16),           # Route 13: Mina al Ahmad nach Hamburg über Afrikaroute
       (2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),           # Route 14: Mina al Ahmad nach Lavera über Afrikaroute
       (2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15),                # Route 15: Mina al Ahmad nach Kent über Afrikaroute
       (2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16),             # Route 16: Mina al Ahmad nach Hamburg über Afrikaroute
       (3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),         # Route 17: Mina al Ahmad nach Lavera über Afrikaroute
       (3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15),              # Route 18: Mina al Ahmad nach Kent über Afrikaroute
       (3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16),           # Route 19: Mina al Ahmad nach Hamburg über Afrikaroute
       (4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),       # Route 20: Mina al Ahmad nach Lavera über Afrikaroute
       (4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15),            # Route 21: Mina al Ahmad nach Kent über Afrikaroute
       (4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16),         # Route 22: Mina al Ahmad nach Hamburg über Afrikaroute
       (5,4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,12,11,9,10),     # Route 23: Mina al Ahmad nach Lavera über Afrikaroute
       (5,4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15),          # Route 24: Mina al Ahmad nach Kent über Afrikaroute
       (5,4,3,2,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,13,14,15,16))       # Route 25: Mina al Ahmad nach Hamburg über Afrikaroute

Landbutton_pos = ((1795,440),(1795,675),(1795,790),(1795,839),(1795,888)) # Position der Auswhalbuttons auf Bohrkarte

NORMALROUTE = 0
AFRIKAROUTE = 1

# aktivekarten für Konsole
SUEZKANALGESPERRT = 0
FOERDERSTOPQUELLEN = 1
DOPPELTEFOERDERUNG = 2

#Zeile = Starthafen
#Spalte =      (       Hamburg                           ),(                 Kent                  ),(              Lavera                     ),(             Kwinana               )
# Subspalte     (6000t),( 9000t      ),(18000t    ),(27000t     )   ( 9000t   ),(18000t     ),(27000t     )   ( 9000t      ),(18000t    ),(27000t     )
Frachtbrief = (((None,None,None,(12,26,40,54))    , (None,(4,8,12,16),(8,16,25,33),(12,25,37,50)) , (None,None,None,(11,20,28,36))  , (None,(3,5,8,11),(5,11,16,22),(8,16,25,33))),
               ((None,None,(4,8,12,16),None)      , (None,(2,4,7,10),None,None)                    , (None,(1,3,4,5),(3,5,8,11),None), (None,None,None,None)),
               (((3,5,8,11),(4,8,12,16),None,None), (None,None,None,None)                          , (None,None,None,None),            (None,(3,5,8,11),None,None)),
               ((None,(4,8,12,16),None,None)      , ((3,5,8,11),None,None,None)                    , (None,None,None,None),            (None,(3,5,8,11),None,None)),
               ((None,None,None,None)             , (None,(2,4,7,10),None,None)                    , (None,None,None,None),            (None,None,None,None)))
Gewinn     =  (((None,None,None,380),(None,140,240,380),(None,None,None,360),(None,130,250,370)),
               ((None,None,310,None),(None,160,None,None),(None,170,340,None),(None,None,None,None)),
               ((100,140,None,None),(None,None,None,None),(None,None,None,None),(None,140,None,None)),
               ((None,140,None,None),(90,None,None,None),(None,None,None,None),(None,130,None,None)),
               ((None,None,None,None),(None,200,None,None),(None,None,None,None),(None,None,None,None)))
Frachtmengen = (6000,9000,18000,27000)
HAMBURG = 0
KENT = 1
LAVERA = 2
KWINANA = 3
Zielhaefennr=(16,15,10,24)

feld_pause = (0, 1.2, 3.5, 1.8, 3.3, 1, 2.8, 5, 4, 2.1, 5, 1.3, 6, 2.5, 1.7)
bohrfeld_pause = (1.6,0,3,3.2,5.3,2.1)

LARGE = 0
SMALL = 1