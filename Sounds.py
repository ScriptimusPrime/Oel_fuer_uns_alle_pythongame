import pygame
from pygame import mixer



feld_sound = (mixer.Sound("Sounds/Felder/start.mp3"), mixer.Sound("Sounds/Felder/memo.mp3"), mixer.Sound("Sounds/Felder/aufschlussbohrung.mp3"),
              mixer.Sound("Sounds/Felder/information.mp3"), mixer.Sound("Sounds/Felder/oelfoerderung.mp3"), mixer.Sound("Sounds/Felder/urlaubsanfang.mp3"),
              mixer.Sound("Sounds/Felder/boerse.mp3"), mixer.Sound("Sounds/Felder/verkaufsangebot.mp3"), mixer.Sound("Sounds/Felder/hubschrauber.mp3"),
              mixer.Sound("Sounds/Felder/konferenzlondon.mp3"), mixer.Sound("Sounds/Felder/zurueckzurboerse.mp3"), mixer.Sound("Sounds/Felder/urlaubsende.mp3"),
              mixer.Sound("Sounds/Felder/oelquelleversiegt.mp3"), mixer.Sound("Sounds/Felder/dienstreise.mp3"), mixer.Sound("Sounds/Felder/zurboerse.mp3"))
bohrfeld_sound = (mixer.Sound("Sounds/Mitteilungen/bohrungsstart.mp3"), mixer.Sound("Sounds/Mitteilungen/bohrfeld nix.mp3"),
                  mixer.Sound("Sounds/Mitteilungen/bohrung fortschritt.mp3"), mixer.Sound("Sounds/Mitteilungen/bohrung nicht erfolgreich.mp3"),
                  mixer.Sound("Sounds/Mitteilungen/bohrmeissel gebrochen.mp3"), mixer.Sound("Sounds/Mitteilungen/bohrung erfolgreich.mp3"))
tank_voll_sound = (mixer.Sound("Sounds/Mitteilungen/tank in kuwait voll.mp3"), mixer.Sound("Sounds/Mitteilungen/tank im irak voll.mp3"),
                   mixer.Sound("Sounds/Mitteilungen/tank in qatar voll.mp3"), mixer.Sound("Sounds/Mitteilungen/tank im iran voll.mp3"),
                   mixer.Sound("Sounds/Mitteilungen/tank in trinidad voll.mp3"))
suezkanalgesperrt=mixer.Sound("Sounds/Mitteilungen/suezkanal gesperrt.mp3")
verschiffen_sound = mixer.Sound("Sounds/Mitteilungen/platz schaffen öl verschiffen.mp3")
frachtrate_sound = (mixer.Sound("Sounds/Mitteilungen/frachtrate 1.mp3"), mixer.Sound("Sounds/Mitteilungen/frachtrate 2.mp3"), mixer.Sound("Sounds/Mitteilungen/frachtrate 3.mp3"), mixer.Sound("Sounds/Mitteilungen/frachtrate 4.mp3"))
aktien_sound = (mixer.Sound("Sounds/Mitteilungen/raffinerien bonus.mp3"), mixer.Sound("Sounds/Mitteilungen/reedereien bonus.mp3"))
dividenden_sound = (mixer.Sound("Sounds/Mitteilungen/dividendenausschüttung 1.mp3"), mixer.Sound("Sounds/Mitteilungen/dividendenausschüttung 2.mp3"))
amzug_sound = (mixer.Sound("Sounds/Mitteilungen/rotistamzug.mp3"),mixer.Sound("Sounds/Mitteilungen/gelbistamzug.mp3"),
               mixer.Sound("Sounds/Mitteilungen/blauistamzug.mp3"),mixer.Sound("Sounds/Mitteilungen/grünistamzug.mp3"))
nichtgenugoel = (mixer.Sound("Sounds/Mitteilungen/kuwait27000.mp3"),mixer.Sound("Sounds/Mitteilungen/irak18000.mp3"), mixer.Sound("Sounds/Mitteilungen/qatar9000.mp3"),
                 mixer.Sound("Sounds/Mitteilungen/iran9000.mp3"),mixer.Sound("Sounds/Mitteilungen/trinidad9000.mp3"))
esgiltfrachtrate = (mixer.Sound("Sounds/Mitteilungen/Esgiltfrachtrate1.mp3"),mixer.Sound("Sounds/Mitteilungen/Esgiltfrachtrate2.mp3"),mixer.Sound("Sounds/Mitteilungen/Esgiltfrachtrate3.mp3"),mixer.Sound("Sounds/Mitteilungen/Esgiltfrachtrate4.mp3"))
begruessung = mixer.Sound("Sounds/Mitteilungen/Begrüßung.mp3")
foerderstop = mixer.Sound("Sounds/Mitteilungen/FörderstopkeinÖl.mp3")
spielerzahlsound = (mixer.Sound("Sounds/Spielerwahl/alleine.mp3"),mixer.Sound("Sounds/Spielerwahl/zuzweit.mp3"),mixer.Sound("Sounds/Spielerwahl/zudritt.mp3"),mixer.Sound("Sounds/Spielerwahl/zuviert.mp3"))
gewonnen = (mixer.Sound("Sounds/Mitteilungen/spielerrothatgewonnen.mp3"),mixer.Sound("Sounds/Mitteilungen/spielergelbhatgewonnen.mp3"),mixer.Sound("Sounds/Mitteilungen/spielerblauhatgewonnen.mp3"),mixer.Sound("Sounds/Mitteilungen/spielergrünhatgewonnen.mp3"))
verloren = (mixer.Sound("Sounds/Mitteilungen/spielerrothatverloren.mp3"),mixer.Sound("Sounds/Mitteilungen/spielergelbhatverloren.mp3"),mixer.Sound("Sounds/Mitteilungen/spielerblauhatverloren.mp3"),mixer.Sound("Sounds/Mitteilungen/spielergrünhatverloren.mp3"))