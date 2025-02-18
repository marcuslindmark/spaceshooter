# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

# Importerar random för att kunna skapa slumptal
import random


# Initiera pygame
pygame.init()


# Initiera Pygame Mixer
pygame.mixer.init()

# Ladda och spela bakgrundsmusiken (ange filnamnet)
pygame.mixer.music.load("assets/music/Mesmerizing Galaxy Loop.mp3")  # Ersätt med rätt sökväg
pygame.mixer.music.set_volume(0.5)  # Justera volym (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Spela loopen (-1 betyder oändlig loop)


# Ladda ljudeffekter
sound_liten_explosion = pygame.mixer.Sound("assets/sounds/scfi_explosion.wav")   # Explosion-ljud
sound_stor_explosion = pygame.mixer.Sound("assets/sounds/huge_explosion.wav")    # Explosion-ljud

# Justera volym om det behövs
sound_liten_explosion.set_volume(0.7)
sound_stor_explosion.set_volume(0.9)



# *** KONFIGURERA FÖNSTRET ***
# Skärmstorlek
SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 1000

# Skapar en skärm med angiven bredd och höjd
skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

# Sätter en fönstertitel på spelet 
pygame.display.set_caption("Space Shooter")

# *** LADDAR ALLA TECKENSNITT OCH SKAPAR TEXTER ***

# Ladda in en egen font
font_game_over = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 74)  
font_poäng = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 24) 

# Skapa en Game Over text
text_game_over = font_game_over.render("SPELET ÄR SLUT!", True, (255, 0, 0))  # Röd färg
text_rect = text_game_over.get_rect(center=(SKÄRMENS_BREDD // 2, SKÄRMENS_HÖJD // 2))  # Centrera texten


# *** LADDAR IN ALLA BAKGRUNDSBILDER ***
# Laddar en stjärnbakgrund
background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/Stars-A.png")


# *** LADDAR IN ALLA SPRITES ***
# Laddar in en ny sprite för rymdskeppet
original_rymdskeppsbild = pygame.image.load("assets/sprites/spaceShip.png")

# Skalar om rymdskeppet till halva storleken 
# Den nya spriten länkas till spelare_bild
# OBS // är operatorn för heltalsdivision 
sprite_rymdskepp = pygame.transform.scale(original_rymdskeppsbild, (original_rymdskeppsbild.get_width() // 2, original_rymdskeppsbild.get_height() // 2))

# Laddar in en ny sprite för jetstrålen till rymdskeppet
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")

# Laddar in en ny sprite till ett skott till rymdskeppet
sprite_skott = pygame.image.load("assets/sprites/bullet.png")

# Laddar in sprites för samtliga asteroider
sprite_asteroid_liten = pygame.image.load("assets/sprites/small-A.png")
sprite_asteroid_mellan = pygame.image.load("assets/sprites/medium-A.png")
sprite_asteroid_stor = pygame.image.load("assets/sprites/large-A.png")


# Skapar en tom lista att fylla för alla skotten som spelaren avfyrar
skott_lista = []  # Lista för att hålla reda på alla skott

# Skapar tomma listor till de olika asteroiderna 
asteroid_liten_lista = []  # Lista för att hålla reda på alla små asteroider
asteroid_mellan_lista = [] # Lista för att hålla reda på alla mellanstora asteroider
asteroid_stor_lista = []   # Lista för att hålla reda på alla stora asteroider

# Lista för alla explosioner (varje explosion är en lista med partiklar)
explosioner = []

# Variabel för att kunna skapa en kort fördröjning som hindrar spelaren från att skjuta för ofta
skott_räknare = 0  # Håller koll på tiden mellan skott

# Variabel för att skapa en fördröjning för hur ofta en asteroid får skapas
asteroid_räknare = 0  

# Startvärde på pausvaribeln för att skapa en fördröjning så att man hinner se Game Over texten.
paus = 0

# Startvärde spelarens energi
energi_kvar = 200

# *** BAKGRUNDSRÖRELSE ***
# Bakgrundens startposition vertikalt (Y-position, den börjar från toppen av skärmen)
bakgrund_y = 0

# Färger som används till explosionseffekten
SVART = (0, 0, 0)
FÄRG_LISTA = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]  # Röd, orange, gul


# *** SAMTLIGA KLASSER I SPELET ***                                  
class Gränssnitt:
    """ Klass som ritar ut allt som har med spelets gränssnitt att göra """
    def __init__(self):
        self.poäng = 0
        self.energi_kvar = 200

    def uppdatera():
        poäng = poäng + 1 

    def uppdatera_energi(self):
        self.energi_kvar = self.energi_kvar - 40

class RymdSkepp:
    """ Denna klass hanterar allt som rör spelarens rymdskepp """
    def __init__(self):
        """Alla instansvariabler för rymdskeppet"""
        self.rymdskepp_x = SKÄRMENS_BREDD // 2 - 120    # Rymdskeppets startposition x-led
        self.rymdskepp_y = SKÄRMENS_HÖJD - 200          # Rymdskeppet startposition y-led
        self.sprite_rymdskepp = sprite_rymdskepp        # Spelarens sprite/bild
        
        self.jetstråle_x = self.rymdskepp_x + 13        # Jetstrålens startposition x-led
        self.jetstråle_y = self.rymdskepp_y + 46        # Jetstrålens startposition y-led
        self.sprite_jetstråle = sprite_jetstråle        # Jetstrålen sprite/bild
        
        self.rymdskeppets_hastighet = 10                # Rymdskeppets hastighet                             
        
        self.exploderat = False                         # När spelet börjar har INTE rymdskeppet exploderat
        
        # Skapar en rektangel för rymdskeppet baserat på dess position och storlek
        self.kollisions_rektangel = pygame.Rect(self.rymdskepp_x, self.rymdskepp_y, self.sprite_rymdskepp.get_width(), self.sprite_rymdskepp.get_height())

    def flytta(self, riktning):
        """Flyttar spelaren i en viss riktning."""
        if not self.exploderat:  # Om rymdskeppet har exploderat, gör ingenting
            if riktning == "vänster":
                self.rymdskepp_x = self.rymdskepp_x - self.rymdskeppets_hastighet
                self.jetstråle_x = self.jetstråle_x - self.rymdskeppets_hastighet
            elif riktning == "höger":
                self.rymdskepp_x = self.rymdskepp_x + self.rymdskeppets_hastighet
                self.jetstråle_x = self.jetstråle_x + self.rymdskeppets_hastighet
            elif riktning == "upp":
                self.rymdskepp_y = self.rymdskepp_y - self.rymdskeppets_hastighet
                self.jetstråle_y = self.jetstråle_y - self.rymdskeppets_hastighet
            elif riktning == "ner":
                self.rymdskepp_y = self.rymdskepp_y + self.rymdskeppets_hastighet
                self.jetstråle_y = self.jetstråle_y + self.rymdskeppets_hastighet
            
            # Flytta med kollisionsrektangeln till där rymdskeppet är
            self.kollisions_rektangel.topleft = (self.rymdskepp_x, self.rymdskepp_y)

    def rita(self, skärm):
        """Ritar spelaren på skärmen."""
        if not self.exploderat:  # Om rymdskeppet har exploderat, rita inte det längre
            skärm.blit(self.sprite_rymdskepp, (self.rymdskepp_x, self.rymdskepp_y))
            skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))

            # Rita kollisionsrektangeln (endast för testning)
            # pygame.draw.rect(skärm, (0, 0, 255), self.kollisions_rektangel, 2)  # Blå rektangel med tjocklek 2
        else:
            # Ta bort kollisionsrektangeln när rymdskeppet är förstört
            self.kollisions_rektangel = pygame.Rect(0, 0, 0, 0)  

# Denna klass skapar explosionseffekten när något förstörs i spelet
class Partikel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.livstid = random.randint(20, 50)  # Hur länge partikeln lever
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig rörelse i x-led
        self.hastighet_y = random.uniform(-2, 2)  # Slumpmässig rörelse i y-led
        self.radius = random.randint(3, 6)  # Storlek på partikeln
        self.färg = random.choice(FÄRG_LISTA)  # Slumpmässig färg

    def uppdatera(self):
        self.x += self.hastighet_x  # Flytta partikeln i x-led
        self.y += self.hastighet_y  # Flytta partikeln i y-led
        self.livstid -= 1  # Minska livslängden

    def rita(self, skärm):
        if self.livstid > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius) 

# Denna klass hanterar det vanliga skottet som skeppet kan skjuta
class Skott:
    # Sätter alla instansvariabler som hör till skottet, kallas på via objektnamnet
    def __init__(self, x, y):
        self.x = x # Skottets position i x-led
        self.y = y # Skottets position i y-led
        self.hastighet = 10  # Skottets rörelsehastighet
        self.bild = sprite_skott  # Använd sprite-bilden
        
    # Metod som flyttar skottet uppåt
    def flytta(self):
        self.y = self.y - self.hastighet  # Flytta skottet uppåt

    # Metod som ritar skottet på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita skottet på skärmen




# Detta är basklassen för asteroider som de andra ärver från
class AsteroidStor:
    # Sätter alla instansvariabler för asteroiden
    def __init__(self, asteroid_x, asteroid_y):
        self.x = asteroid_x # Asteroidens position i x-led
        self.y = asteroid_y # Asteroidens position i y-led
        self.hastighet = 4  # Asteroidens rörelsehastighet
        self.bild = sprite_asteroid_stor  # Använd sprite-bilden
        self.kollisions_rektangel = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())        

        # Sätt en slumpmässig riktning en gång vid skapandet
        self.riktning = random.randint(1, 3)

    def kollidera_med_skott(self, objekt_lista):
        """Kontrollerar om en asteroid har kolliderat med ett skott"""
        for skott in objekt_lista:
            if self.kollisions_rektangel.colliderect(pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height())):
                print("Stor Asteroid träffades av skottet!")  # Skriver ut i konsolen att en träff har skett
                gränssnitts_hanteraren.poäng = gränssnitts_hanteraren.poäng + 1  # Uppdaterar spelarens poäng
                objekt_lista.remove(skott)  # Ta bort skottet
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(self.x + self.bild.get_width() // 2, self.y + self.bild.get_height() // 2) for _ in range(100)]
                explosioner.append(explosion)  # Skapa explosionseffekten
                return True  # Returnera True om kollison har skett
        return False

    # Metod som undersöker om asteroiden har kolliderat med rymdskeppet
    def kollidera_med_rymdskepp(self, rymdskepp):
        if not spelare_1.exploderat:  # Kontrollera kollision endast om skeppet inte är förstört
            # Kontrollerar om en kollision mellan asteroiden och rymdskeppet inträffat
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("Kollision upptäckt med rymdskeppet!")
                
                # Om spelaren har energi kvar gör det här:
                asteroid_stor_lista.remove(asteroid_stor)    # Ta bort asteroiden från listan
                gränssnitts_hanteraren.uppdatera_energi()
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y - 46) for _ in range(100)]  # Skapa 100 partiklar
                explosioner.append(explosion)
                
                # Om spelaren har slut på energi gör i stället detta:
                if (gränssnitts_hanteraren.energi_kvar <= 0):
                    spelare_1.exploderat = True
                    sound_stor_explosion.play()  # Spela explosionseffekten
                    explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y + 46) for _ in range(100)]  # Skapa 100 partiklar
                    explosioner.append(explosion)

    # Metod som flyttar asteroiden neråt
    def flytta(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position

    # Metod som flyttar asteroiden neråt snett åt vänster
    def flytta_snett_vänster(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x - 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position

    # Metod som flyttar asteroiden neråt snett åt höger
    def flytta_snett_höger(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x + 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position
    
    # Metod som ritar asteroiden på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita asteroiden på skärmen       


# Denna klass hanterar den mellanstora asteroiden
class AsteroidMellan:
    # Sätter alla instansvariabler för asteroiden
    def __init__(self, asteroid_mellan_x, asteroid_mellan_y):
        self.x = asteroid_mellan_x # Asteroidens position i x-led
        self.y = asteroid_mellan_y # Asteroidens position i y-led
        self.hastighet = 5  # Asteroidens rörelsehastighet
        self.bild = sprite_asteroid_mellan  # Använd sprite-bilden
        self.kollisions_rektangel = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())        

        # Sätt en slumpmässig riktning en gång vid skapandet
        self.riktning = random.randint(1, 3)

    def kollidera_med_skott(self, objekt_lista):
        """Kontrollerar om en asteroid har kolliderat med ett skott"""
        for skott in objekt_lista:
            if self.kollisions_rektangel.colliderect(pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height())):
                print("Mellanstor Asteroid träffades av skottet!")  # Skriver ut i konsolen att en träff har skett
                gränssnitts_hanteraren.poäng = gränssnitts_hanteraren.poäng + 1  # Uppdaterar spelarens poäng
                objekt_lista.remove(skott)  # Ta bort skottet
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(self.x + self.bild.get_width() // 2, self.y + self.bild.get_height() // 2) for _ in range(100)]
                explosioner.append(explosion)  # Skapa explosionseffekten
                return True  # Returnera True om kollison har skett
        return False

    # Metod som undersöker om asteroiden har kolliderat med rymdskeppet
    def kollidera_med_rymdskepp(self, rymdskepp):
        if not spelare_1.exploderat:  # Kontrollera kollision endast om skeppet inte är förstört
            # Kontrollerar om en kollision mellan asteroiden och rymdskeppet inträffat
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("Kollision upptäckt med rymdskeppet!")
                
                # Om spelaren har energi kvar gör det här:
                asteroid_mellan_lista.remove(asteroid_mellan)    # Ta bort asteroiden från listan
                gränssnitts_hanteraren.uppdatera_energi()
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y - 46) for _ in range(100)]  # Skapa 100 partiklar
                explosioner.append(explosion)
                
                # Om spelaren har slut på energi gör i stället detta:
                if (gränssnitts_hanteraren.energi_kvar <= 0):
                    spelare_1.exploderat = True
                    sound_stor_explosion.play()  # Spela explosionseffekten
                    explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y + 46) for _ in range(100)]  # Skapa 100 partiklar
                    explosioner.append(explosion)

    # Metod som flyttar asteroiden neråt
    def flytta(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position

    # Metod som flyttar asteroiden neråt snett åt vänster
    def flytta_snett_vänster(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x - 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position

    # Metod som flyttar asteroiden neråt snett åt höger
    def flytta_snett_höger(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x + 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position
    
    # Metod som ritar asteroiden på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita asteroiden på skärmen                
                

# Denna klass hanterar liten asteroid.
class AsteroidLiten:
    # Sätter alla instansvariabler för asteroiden
    def __init__(self, asteroid_liten_x, asteroid_liten_y):
        self.x = asteroid_liten_x # Asteroidens position i x-led
        self.y = asteroid_liten_y # Asteroidens position i y-led
        self.hastighet = 6  # Asteroidens rörelsehastighet
        self.bild = sprite_asteroid_liten  # Använd sprite-bilden
        
        # Sätt en slumpmässig riktning en gång vid skapandet
        self.riktning = random.randint(1, 3)
        
        self.kollisions_rektangel = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())        

    def kollidera_med_skott(self, objekt_lista):
        """Kontrollerar om en asteroid har kolliderat med ett skott"""
        for skott in objekt_lista:
            if self.kollisions_rektangel.colliderect(pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height())):
                print("Asteroiden träffades av skottet!")  # Skriver ut i konsolen att en träff har skett
                gränssnitts_hanteraren.poäng = gränssnitts_hanteraren.poäng + 1  # Uppdaterar spelarens poäng
                objekt_lista.remove(skott)  # Ta bort skottet
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(self.x + self.bild.get_width() // 2, self.y + self.bild.get_height() // 2) for _ in range(100)]
                explosioner.append(explosion)  # Skapa explosionseffekten
                return True  # Returnera True om kollison har skett
        return False

    # Metod som undersöker om asteroiden har kolliderat med rymdskeppet
    def kollidera_med_rymdskepp(self, rymdskepp):
        if not spelare_1.exploderat:  # Kontrollera kollision endast om skeppet inte är förstört
            # Kontrollerar om en kollision mellan asteroiden och rymdskeppet inträffat
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("Kollision upptäckt med rymdskeppet!")
                
                # Om spelaren har energi kvar gör det här:
                asteroid_liten_lista.remove(asteroid_liten)  # Ta bort asteroiden från listan
                gränssnitts_hanteraren.uppdatera_energi()
                sound_stor_explosion.play()  # Spela explosionseffekten
                explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y - 46) for _ in range(100)]  # Skapa 100 partiklar
                explosioner.append(explosion)
                
                # Om spelaren har slut på energi gör i stället detta:
                if (gränssnitts_hanteraren.energi_kvar <= 0):
                    spelare_1.exploderat = True
                    sound_stor_explosion.play()  # Spela explosionseffekten
                    explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y + 46) for _ in range(100)]  # Skapa 100 partiklar
                    explosioner.append(explosion)

    # Metod som flyttar asteroiden neråt
    def flytta(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position
    
    # Metod som flyttar asteroiden neråt snett åt vänster
    def flytta_snett_vänster(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x - 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position

    # Metod som flyttar asteroiden neråt snett åt höger
    def flytta_snett_höger(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.x = self.x + 1
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position


    # Metod som ritar asteroiden på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita asteroiden på skärmen
    
    # Rita kollisionsrektangeln (endast för testning)
        #pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel, 2)  # Röd rektangel med tjocklek 2    

# Skapar ett objekt av spelarens rymdskepp
spelare_1 = RymdSkepp()

# Skapar ett objekt av gränssnitts_hanteraren
gränssnitts_hanteraren = Gränssnitt()

# *** SPELET STARTAR HÄR ***
# Spelloop
spelet_körs = True
while (spelet_körs == True):
    
    # *** RITA BAKGRUNDSBILDEN ***
    # Skapa en mörk bakgrundsbild
    skärm.blit(background_mörkblå, (0,0))
    
    # Rita stjärnorna i bakgrunden
    skärm.blit(background_stjärnor, (0, bakgrund_y))  # Lägg till stjärnbilden från hörnet (0, 0)
    
    # Rita en andra bakgrundsbild utanför skärmen för att skapa illusionen av kontinuerlig rörelse
    skärm.blit(background_stjärnor, (0, bakgrund_y - SKÄRMENS_HÖJD))  # Andra bilden som ligger ovanpå den första

    # Uppdatera båda bakgrundsbildernas position
    bakgrund_y = bakgrund_y + 2  # Rör bakgrunden neråt (justera denna för att få önskad hastighet)
    
    # Om bakgrunden har rört sig för långt (längden på skärmen) så sätt tillbaka till toppen
    if (bakgrund_y >= SKÄRMENS_HÖJD):
        bakgrund_y = 0

    # *** AVSLUTA SPELET ***
    # Den här koden kollar hela tiden om användaren försöker stänga spelet 
    # genom att klicka på fönstrets stängknapp. 
    for händelse in pygame.event.get():
        # Om användaren klickar på fönstrets stängningsknapp avslutas loopen
        if (händelse.type == pygame.QUIT):
            spelet_körs = False
        # Denna kod kollar om användaren försöker stänga spelet med en ESC-knapp
        elif (händelse.type == pygame.KEYDOWN):
            if (händelse.key == pygame.K_ESCAPE):  # Tryck på ESC för att avsluta spelet
                spelet_körs = False
        

    # *** KONTROLLER FÖR SPELAREN ***
    # Hantera tangenttryckningar
    
    # Hämtar en lista som innehåller vilka tangenter som är nedtryckta just nu och sparar den i variabeln keys.
    keys = pygame.key.get_pressed()
    
    # Styra vänster men inte utanför skärmen
    if keys[pygame.K_LEFT] and spelare_1.rymdskepp_x > 0:
        spelare_1.flytta("vänster")
    
    # Styra höger men inte utanför skärmen
    if keys[pygame.K_RIGHT] and spelare_1.rymdskepp_x < SKÄRMENS_BREDD - spelare_1.sprite_rymdskepp.get_width():
        spelare_1.flytta("höger")

    # Styra uppåt men inte utanför skärmen
    if keys[pygame.K_UP] and spelare_1.rymdskepp_y > 0:
        spelare_1.flytta("upp")
        
    # Styra nedåt men inte utanför skärmen
    if keys[pygame.K_DOWN] and spelare_1.rymdskepp_y < SKÄRMENS_HÖJD - spelare_1.sprite_rymdskepp.get_width() - 20:
        spelare_1.flytta("ner")

    # Om spelaren trycker på SPACE skjut en kula
    if not spelare_1.exploderat:  # Om rymdskeppet har exploderat, gör ingenting
        if keys[pygame.K_SPACE]:  
            # Om tillräckligt lång tid har gått får spelaren skjuta igen
            if (skott_räknare > 10):
                # Uppdaterar skottlistan med en ny instans (kopia av skottet) på den position där det avfyrades
                skott_lista.append(Skott(spelare_1.rymdskepp_x + 20, spelare_1.rymdskepp_y))
                
                # Nollställer räknaren
                skott_räknare = 0

    # *** VANLIGT SKOTT ***
    # Loopar igenom skottlistan baklänges och flyttar varje instans av skotten och ritar dem på skärmen
    for skott in reversed(skott_lista):  # Iterera baklänges genom listan
        skott.flytta()
        skott.rita(skärm)
    
        # Ta bort skott som hamnat utanför skärmen
        if skott.y < -100:
            skott_lista.remove(skott)


    # *** SKAPA NYA ASTEROIDER ***
    # Om tillräckligt lång tid passerat
    if (asteroid_räknare >= 40):
        slumptal = random.randint(1, 3)
        if (slumptal == 1):
            # Skapa en ny instans av liten asteroid    
            asteroid_liten_lista.append(AsteroidLiten(random.randint(100, SKÄRMENS_BREDD - 100), -100))
        elif (slumptal == 2):
            # Skapa en ny instans av mellanstor asteroid    
            asteroid_mellan_lista.append(AsteroidMellan(random.randint(100, SKÄRMENS_BREDD - 100), -100))
        elif (slumptal == 3):
            # Skapa en ny instans av stor asteroid    
            asteroid_stor_lista.append(AsteroidStor(random.randint(100, SKÄRMENS_BREDD - 100), -100))
        
        # Återställ räknaren
        asteroid_räknare = 0    

    
    # Loopar igenom asteroidlistan baklänges och flyttar varje instans av asteroiderna och ritar dem på skärmen
    for asteroid_liten in reversed(asteroid_liten_lista):  # Iterera baklänges genom listan
        # Flyttar asteroiderna ett steg i den riktningen de för tillfället har
        
        if (asteroid_liten.riktning == 1):
            asteroid_liten.flytta_snett_vänster()
        elif (asteroid_liten.riktning == 2):
            asteroid_liten.flytta_snett_höger()
        elif (asteroid_liten.riktning == 3):
            asteroid_liten.flytta()
        # Om asteroiden kolliderar med spelarens rymdskepp
        asteroid_liten.kollidera_med_rymdskepp(spelare_1.kollisions_rektangel)
        
        # Ritar asteroiderna på den plats de för tillfället befinner sig på
        asteroid_liten.rita(skärm)
        
        # Ta bort asteroider som hamnat utanför skärmen
        if asteroid_liten.y > 1100:
            asteroid_liten_lista.remove(asteroid_liten)

    # Om asteoriden kolliderar med ett skott 
        if asteroid_liten.kollidera_med_skott(skott_lista):
            if asteroid_liten in asteroid_liten_lista:  # Kontrollera om asteroiden finns i listan
                 asteroid_liten_lista.remove(asteroid_liten)  # Ta bort asteroiden från listan

# *** MELLANSTOR ASTEROID ***
# Loopar igenom asteroidlistan baklänges och flyttar varje instans av asteroiderna och ritar dem på skärmen
    for asteroid_mellan in reversed(asteroid_mellan_lista):  # Iterera baklänges genom listan
        # Flyttar asteroiderna ett steg i den riktningen de för tillfället har
        if (asteroid_mellan.riktning == 1):
            asteroid_mellan.flytta_snett_vänster()
        elif (asteroid_mellan.riktning == 2):
            asteroid_mellan.flytta_snett_höger()
        elif (asteroid_mellan.riktning == 3):
            asteroid_mellan.flytta()
        
        # Om asteroiden kolliderar med spelarens rymdskepp
        asteroid_mellan.kollidera_med_rymdskepp(spelare_1.kollisions_rektangel)
        
        # Ritar asteroiderna på den plats de för tillfället befinner sig på
        asteroid_mellan.rita(skärm)
        
        # Ta bort asteroider som hamnat utanför skärmen
        if asteroid_mellan.y > 1100:
            asteroid_mellan_lista.remove(asteroid_mellan)

    # Om asteoriden kolliderar med ett skott 
        if asteroid_mellan.kollidera_med_skott(skott_lista):
            
            asteroid_liten_lista.append(AsteroidLiten(asteroid_mellan.x - 60, asteroid_mellan.y))
            asteroid_liten_lista.append(AsteroidLiten(asteroid_mellan.x + 60, asteroid_mellan.y))
            
            if asteroid_mellan in asteroid_mellan_lista:  # Kontrollera om asteroiden finns i listan
                asteroid_mellan_lista.remove(asteroid_mellan)  # Ta bort den från listan

# *** STOR ASTEROID ***
# Loopar igenom asteroidlistan baklänges och flyttar varje instans av asteroiderna och ritar dem på skärmen
    for asteroid_stor in reversed(asteroid_stor_lista):  # Iterera baklänges genom listan
        # Flyttar asteroiderna ett steg i den riktningen de för tillfället har
        if (asteroid_stor.riktning == 1):
            asteroid_stor.flytta_snett_vänster()
        elif (asteroid_stor.riktning == 2):
            asteroid_stor.flytta_snett_höger()
        elif (asteroid_stor.riktning == 3):
            asteroid_stor.flytta()
        
        # Om asteroiden kolliderar med spelarens rymdskepp
        asteroid_stor.kollidera_med_rymdskepp(spelare_1.kollisions_rektangel)
        
        # Ritar asteroiderna på den plats de för tillfället befinner sig på
        asteroid_stor.rita(skärm)
        
        # Ta bort asteroider som hamnat utanför skärmen
        if asteroid_stor.y > 1100:
            asteroid_stor_lista.remove(asteroid_stor)

    # Om asteoriden kolliderar med ett skott 
        if asteroid_stor.kollidera_med_skott(skott_lista):
            
            asteroid_mellan_lista.append(AsteroidMellan(asteroid_stor.x - 80, asteroid_stor.y))
            asteroid_mellan_lista.append(AsteroidMellan(asteroid_stor.x + 80, asteroid_stor.y))
            
            if asteroid_stor in asteroid_stor_lista:  # Kontrollera om asteroiden finns i listan
                asteroid_stor_lista.remove(asteroid_stor)  # Ta bort den från listan
   
    # *** RITA ALLA SPRITES PÅ SKÄRMEN ***
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    
    # Rita spelarens rymdskepp
    spelare_1.rita(skärm)

    # Om spelarens skepp exploderat läggs en kort paus in här innan spelet avslutas    
    if (spelare_1.exploderat == True):
        
        # Ritar "Game Over" texten på skärmen.
        skärm.blit(text_game_over, text_rect)  # Rita texten på skärmen
        
        paus = paus + 1
        if (paus >= 120):
            exit()
    
    # Skapa en text som visar poängen
    score_text = font_poäng.render(f"Poäng: {gränssnitts_hanteraren.poäng}", True, (255, 255, 255))  # Vit text
    skärm.blit(score_text, (10, 20))  # Rita texten i övre vänstra hörnet

    # Rita ut energibaren i gränssnittet en grön ovanpå en röd
    pygame.draw.rect(skärm, (255, 0, 0), (200, 10, 200, 40))  # Röd rektangel 
    pygame.draw.rect(skärm, (0, 255, 0), (200, 10, gränssnitts_hanteraren.energi_kvar, 40))  # Grön rektangel 


    # *** RITAR ALLA PARTIKELEFFEKTER ***
    # Uppdatera och rita explosionerna
    for explosion in explosioner:
        for partikel in explosion:
            partikel.uppdatera()
            partikel.rita(skärm)

    # Ta bort döda partiklar (de som har en livslängd på 0)
    explosioner = [[p for p in explosion if p.livstid > 0] for explosion in explosioner]
    explosioner = [e for e in explosioner if len(e) > 0]  # Ta bort tomma explosioner


    # *** UPPDATERA ALL GRAFIK PÅ SKÄRMEN ***
    # Uppdaterar grafiken på skärmen så att spelaren ser vart alla spelfigurer flyttat någonstans
    pygame.display.update()

    # Uppdaterar skottets räknare som används för att se när spelaren får skjuta igen 
    skott_räknare = skott_räknare + 1

    # Uppdaterar asteroid_litens räknare för att se när nästa asteroid ska skapas i spelet
    asteroid_räknare = asteroid_räknare + 1

# Avslutar spelet
pygame.quit()