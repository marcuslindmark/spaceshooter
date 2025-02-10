# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

# Importerar random för att kunna skapa slumptal
import random


# Initiera pygame
pygame.init()


# *** KONFIGURERA FÖNSTRET ***
# Skärmstorlek
SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 1000

# Skapar en skärm med angiven bredd och höjd
skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

# Sätter en fönstertitel på spelet 
pygame.display.set_caption("Space Shooter")

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

# Laddar in en ny sprite till en liten asteroid
sprite_asteroid_liten = pygame.image.load("assets/sprites/small-A.png")

# Skapar en tom lista att fylla för alla skotten som spelaren avfyrar
skott_lista = []  # Lista för att hålla reda på alla skott

# Skapar en tom lista att fylla med alla asteroider som spawnas
asteroid_liten_lista = []  # Lista för att hålla reda på alla asteroider

# Lista för alla explosioner (varje explosion är en lista med partiklar)
explosioner = []

# Variabel för att kunna skapa en kort fördröjning som hindrar spelaren från att skjuta för ofta
skott_räknare = 0  # Håller koll på tiden mellan skott

# Variabel för att skapa en fördröjning för hur ofta en asteroid får skapas
asteroid_liten_räknare = 0  

paus = 0

# *** BAKGRUNDSRÖRELSE ***
# Bakgrundens startposition vertikalt (Y-position, den börjar från toppen av skärmen)
bakgrund_y = 0

# Färger som används till explosionseffekten
SVART = (0, 0, 0)
FÄRG_LISTA = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]  # Röd, orange, gul


# *** SAMTLIGA KLASSER I SPELET ***
# Denna klass hanterar allt som rör spelarens rymdskepp
class RymdSkepp:
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

# Denna klass hanterar liten asteroid.
class AsteroidLiten:
    # Sätter alla instansvariabler för asteroiden
    def __init__(self, asteroid_liten_x, asteroid_liten_y):
        self.x = asteroid_liten_x # Asteroidens position i x-led
        self.y = asteroid_liten_y # Asteroidens position i y-led
        self.hastighet = 4  # Asteroidens rörelsehastighet
        self.bild = sprite_asteroid_liten  # Använd sprite-bilden
        self.kollisions_rektangel = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())        

    def kollidera_med_skott(self, objekt_lista):
        """Kontrollerar om en asteroid har kolliderat med ett skott"""
        for skott in objekt_lista:
            if self.kollisions_rektangel.colliderect(pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height())):
                print("Asteroiden träffades av skottet!")
                objekt_lista.remove(skott)  # Ta bort skottet
                explosion = [Partikel(self.x + self.bild.get_width() // 2, self.y + self.bild.get_height() // 2) for _ in range(100)]
                explosioner.append(explosion)  # Skapa explosionseffekten
                return True  # Returnera True om kollison har skett
        return False

    # Metod som undersöker om asteroiden har kolliderat med rymdskeppet
    def kollidera(self, rymdskepp):
        if not spelare_1.exploderat:  # Kontrollera kollision endast om skeppet inte är förstört
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("Kollision upptäckt med rymdskeppet!")
                spelare_1.exploderat = True
                explosion = [Partikel(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y + 46) for _ in range(100)]  # Skapa 100 partiklar
                explosioner.append(explosion)

    # Metod som flyttar asteroiden neråt
    def flytta(self):
        self.y = self.y + self.hastighet  # Flytta asteroiden neråt
        self.kollisions_rektangel.topleft = (self.x, self.y)  # Uppdatera rektangelns position
    
    # Metod som ritar asteroiden på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita asteroiden på skärmen
    
    # Rita kollisionsrektangeln (endast för testning)
        #pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel, 2)  # Röd rektangel med tjocklek 2

# Skapar ett objekt av spelarens rymdskepp
spelare_1 = RymdSkepp()

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


    # *** LITEN ASTEROID ***
    # Om tillräckligt lång tid passerat
    if (asteroid_liten_räknare >= 30):
        # Skapa en ny instans av asteroiden    
        asteroid_liten_lista.append(AsteroidLiten(random.randint(100, SKÄRMENS_BREDD - 100), -100))
        # Återställ räknaren
        asteroid_liten_räknare = 0    

    
    # Loopar igenom asteroidlistan baklänges och flyttar varje instans av asteroiderna och ritar dem på skärmen
    for asteroid_liten in reversed(asteroid_liten_lista):  # Iterera baklänges genom listan
        # Flyttar asteroiderna ett steg i den riktningen de för tillfället har
        asteroid_liten.flytta()
        
        # Om asteroiden kolliderar med spelarens rymdskepp
        asteroid_liten.kollidera(spelare_1.kollisions_rektangel)

        # Om asteoriden kolliderar med ett skott
        if asteroid_liten.kollidera_med_skott(skott_lista):
            asteroid_liten_lista.remove(asteroid_liten)  # Ta bort asteroiden från listan
        
        # Ritar asteroiderna på den plats de för tillfället befinner sig på
        asteroid_liten.rita(skärm)
        
        # Ta bort asteroider som hamnat utanför skärmen
        if asteroid_liten.y > 1100:
            asteroid_liten_lista.remove(asteroid_liten)



    # *** RITA ALLA SPRITES PÅ SKÄRMEN ***
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    
    # Rita spelarens rymdskepp
    spelare_1.rita(skärm)

    # Om spelarens skepp exploderat läggs en kort paus in här innan spelet avslutas    
    if (spelare_1.exploderat == True):
        paus = paus + 1
        if (paus >= 120):
            exit()
    
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
    asteroid_liten_räknare = asteroid_liten_räknare + 1

# Avslutar spelet
pygame.quit()