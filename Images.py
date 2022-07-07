import pygame
from pygame import image

imgSpielfeld = image.load('Spielfeld/Spielfeld_3500.png')
imgSpielfeldeinfach = image.load('Spielfeld/Spielfeld_3500einfacher.png')

imgSpielfigur = (image.load('Spielfiguren/rotrand.png'), image.load('Spielfiguren/gelbrand.png'), image.load('Spielfiguren/blaurand.png'),
                 image.load('Spielfiguren/grünrand.png'), image.load('Spielfiguren/rot.png'), image.load('Spielfiguren/gelb.png'),
                 image.load('Spielfiguren/blau.png'), image.load('Spielfiguren/grün.png'))
imgTitelbild = image.load('Titelbild/Titelbild_1080.png')

# Geld
# Scheine = [[500000,image.load("Geld/500000.png")],[200000,image.load("Geld/200000.png")],[100000,image.load("Geld/100000.png")],[50000,image.load("Geld/50000.png")],[10000,image.load("Geld/10000.png")]]

Zahlimages = [image.load("Bedienfeld/0.png"), image.load("Bedienfeld/1.png"), image.load("Bedienfeld/2.png"), image.load("Bedienfeld/3.png"), image.load("Bedienfeld/4.png"), image.load("Bedienfeld/5.png"), image.load("Bedienfeld/6.png"),
              image.load("Bedienfeld/7.png"), image.load("Bedienfeld/8.png"), image.load("Bedienfeld/9.png")]
Tablet = image.load("Bedienfeld/tablet.png")
Dollar = image.load("Bedienfeld/dollar.png")

Aktienimages = (image.load("Bedienfeld/AktienRaffinerie.png"), image.load("Bedienfeld/AktienReederei.png"))
# AktienReederei = image.load("Bedienfeld/AktienReederei.png")
# AktienRaffinerie = image.load("Bedienfeld/AktienRaffinerie.png")
Landbutton_small = (image.load("Bedienfeld/button_kuwait.png"), image.load("Bedienfeld/button_irak.png"), image.load("Bedienfeld/button_qatar.png"), image.load("Bedienfeld/button_iran.png"), image.load("Bedienfeld/button_trinidad.png"))
Landbutton_big = (image.load("Bedienfeld/button_kuwait_big.png"), image.load("Bedienfeld/button_irak_big.png"),
                  image.load("Bedienfeld/button_qatar_big.png"), image.load("Bedienfeld/button_iran_big.png"),
                  image.load("Bedienfeld/button_trinidad_big.png"))

buttonImages = (image.load("Bedienfeld/plus.png"), image.load("Bedienfeld/minus.png"), image.load("Bedienfeld/Würfel/Würfelbrett.png"),
                image.load("Bedienfeld/button_zug-beenden.png"), image.load("Bedienfeld/button_ja.png"), image.load("Bedienfeld/button_nein.png"),
                image.load("Bedienfeld/button_fertig.png"), image.load("Bedienfeld/button_tanker-starten.png"), image.load("Bedienfeld/button_probebohrung.png"),
                image.load("Bedienfeld/button_oelquelle-kaufen.png"),
                Landbutton_small[0], Landbutton_small[1], Landbutton_small[2], Landbutton_small[3], Landbutton_small[4],
                image.load("Bedienfeld/button_close.png"),
                image.load("Titelbild/1spieler.png"), image.load("Titelbild/2spieler.png"), image.load("Titelbild/3spieler.png"), image.load("Titelbild/4spieler.png"),image.load('Bedienfeld/unchecked-d.png'))

buttonKlick = image.load("Bedienfeld/button_klick.png")

tanker = (image.load("Tanker/rot_klein.png"), image.load("Tanker/gelb_klein.png"), image.load("Tanker/blau_klein.png"), image.load("Tanker/grün_klein.png"))

aktivekarten = (image.load("Bedienfeld/suezkanalgesperrt.png"), image.load("Bedienfeld/Förderstop.png"), image.load("Bedienfeld/Doppelteförderleistung.png"))
saleimage = image.load("Bedienfeld/sale.png")
wuerfelimages = (image.load("Bedienfeld/Würfel/1.png"), image.load("Bedienfeld/Würfel/2.png"), image.load("Bedienfeld/Würfel/3.png"), image.load("Bedienfeld/Würfel/4.png"), image.load("Bedienfeld/Würfel/5.png"), image.load("Bedienfeld/Würfel/6.png"))

endeImage = image.load("Spielende/Bohrturm Nacht.png")
blendeImage = image.load("Spielende/blende.png")
