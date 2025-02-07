# *** GRUNDSPELET FÖLJ DESSA STEG ***
# *** STEG 1 ***
# Skapa en skärm, en spelloop och importera en sprite för rymdskeppet
# Gör så att rymdskeppet kan röra på sig

# *** STEG 2 ***
# Lägg till en stjärnbakgrund och få den att scrolla 

# *** STEG 3 ***
# Lägg till jetstrålar bakom rymdskeppet

# *** STEG 4 ***
# Gör så att man kan skjuta i spelet


# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

# Initiera pygame
pygame.init()


# *** KONFIGURERA FÖNSTRET ***
# Skärmstorlek
SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 1000

# Skapar en skärm med angiven bredd och höjd (1024 x 768 pixlar)
skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

# Sätter en fönstertitel på spelet 
pygame.display.set_caption("Space Shooter")

# *** LADDAR IN EN BAKGRUNDSBILD ***
# Laddar en stjärnbakgrund
bakgrundsbild = pygame.image.load("assets/backgrounds/bg.png")
stjärnbild_1 = pygame.image.load("assets/backgrounds/Stars-A.png")


# *** LADDAR IN ALLA SPRITES ***

# Laddar in en ny sprite för rymdskeppet
original_rymdskeppsbild = pygame.image.load("assets/sprites/spaceShip.png")

# Skalar om rymdskeppet till halva storleken 
# Den nya spriten länkas till spelare_bild
# OBS // är operatorn för heltalsdivision 
sprite_spelare = pygame.transform.scale(original_rymdskeppsbild, (original_rymdskeppsbild.get_width() // 2, original_rymdskeppsbild.get_height() // 2))

# Laddar in en ny sprite för jetstrålen till rymdskeppet
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")

# Laddar in en ny sprite till ett skott till rymdskeppet
sprite_skott = pygame.image.load("assets/sprites/bullet.png")


# *** STÄLL IN STARTVÄRDEN PÅ VARIABLER ***
# Sätt spelarens startposition
spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200

# Sätt jetstrålens startposition
jetstråle_x = spelare_x + 13
jetstråle_y = spelare_y + 46

# Sätt spelarens hastighet när spelet börjar
spelarens_hastighet = 10

# Skapar en tom lista att fylla för alla skotten som spelaren avfyrar
skott_lista = []  # Lista för att hålla reda på alla skott

# Variabler för att kunna skapa en kort fördröjning som hindrar spelaren från att skjuta för ofta
skott_räknare = 0  # Håller koll på tiden mellan skott

# *** BAKGRUNDSRÖRELSE ***
# Bakgrundens startposition vertikalt (Y-position, den börjar från toppen av skärmen)
bakgrund_y = 0


# *** SAMTLIGA KLASSER I SPELET ***

# Denna klass hanterar det vanliga skottet som skeppet kan skjuta
class Skott:
    # Statisk variabel som håller reda på antalet skottinstanser som finns i spelet
    antal_instans = 0

    # Sätter alla instansvariabler som hör till skottet
    def __init__(self, x, y):
        self.x = x # Skottets position i x-led
        self.y = y # Skottets position i y-led
        self.hastighet = 10  # Skottets rörelsehastighet
        self.bild = sprite_skott  # Använd sprite-bilden
        Skott.antal_instans = Skott.antal_instans + 1  # Öka räknaren när ett nytt skott skapas
        
    # Metod som flyttar skottet uppåt
    def flytta(self):
        self.y = self.y - self.hastighet  # Flytta skottet uppåt

    # Metod som ritar skottet på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita skottet på skärmen

    # En specialmetod som fungerar som Pythons städare. 
    # Anropas när en instans av klassen tas bort och minnet återvinns.
    def __del__(self):
        Skott.antal_instans = Skott.antal_instans - 1  # Minska räknaren när ett skott tas bort

# *** SPELET STARTAR HÄR ***
# Spelloop
spelet_körs = True
while (spelet_körs == True):
    
    # *** RITA BAKGRUNDSBILDEN ***
    # Skapa en mörk bakgrundsbild
    skärm.blit(bakgrundsbild, (0,0))
    
    # Rita stjärnorna i bakgrunden
    skärm.blit(stjärnbild_1, (0, bakgrund_y))  # Lägg till stjärnbilden från hörnet (0, 0)
    
    # Rita en andra bakgrundsbild utanför skärmen för att skapa illusionen av kontinuerlig rörelse
    skärm.blit(stjärnbild_1, (0, bakgrund_y - SKÄRMENS_HÖJD))  # Andra bilden som ligger ovanpå den första

    # Uppdatera båda bakgrundsbildernas position
    bakgrund_y = bakgrund_y + 2  # Rör bakgrunden neråt (justera denna för att få önskad hastighet)
    
    # Om bakgrunden har rört sig för långt (längden på skärmen) så sätt tillbaka till toppen
    if bakgrund_y >= SKÄRMENS_HÖJD:
        bakgrund_y = 0


    # *** AVSLUTA SPELET ***
    # Den här koden kollar hela tiden om användaren försöker stänga spelet 
    # genom att klicka på fönstrets stängknapp. 
    for händelse in pygame.event.get():
        # Om användaren klickar på fönstrets stängningsknapp avslutas loopen
        if händelse.type == pygame.QUIT:
            spelet_körs = False
        # denna kod kollar om användaren försöker stänga spelet med en ESC-knapp
        elif händelse.type == pygame.KEYDOWN:
            if händelse.key == pygame.K_ESCAPE:  # Tryck på ESC för att avsluta helskärm
                spelet_körs = False


    # *** KONTROLLER FÖR SPELAREN ***
    # Hantera tangenttryckningar
    
    # Hämtar en lista som innehåller vilka tangenter som är nedtryckta just nu och sparar den i variabeln keys.
    keys = pygame.key.get_pressed()
    
    # Om spelaren trycker på vänster piltangent styr vänster med rymdskeppet och jetstrålen, 
    # men inte om rymdskeppet åker utanför skärmen
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x = spelare_x - spelarens_hastighet
        jetstråle_x = jetstråle_x - spelarens_hastighet
    
    # Om spelaren trycker på höger piltangent styr höger med rymdskeppet och jetstrålen, 
    # men inte om rymdskeppet åker utanför skärmen
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x = spelare_x + spelarens_hastighet
        jetstråle_x = jetstråle_x + spelarens_hastighet
    
    # Om spelaren trycker på uppåt piltangent styr uppåt med rymdskeppet och jetstrålen, 
    # men inte om rymdskeppet åker utanför skärmen
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y = spelare_y - spelarens_hastighet
        jetstråle_y = jetstråle_y - spelarens_hastighet
    
    # Om spelaren trycker på nedåt piltangent styr nedåt med rymdskeppet och jetstrålen, 
    # men inte om rymdskeppet åker utanför skärmen
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_width() - 20:
        spelare_y = spelare_y + spelarens_hastighet
        jetstråle_y = jetstråle_y + spelarens_hastighet
    
    # Om spelaren trycker på SPACE skjut en kula
    if keys[pygame.K_SPACE]:  
        # Om tillräckligt lång tid har gått får spelaren skjuta igen
        if (skott_räknare > 10):
            # Uppdaterar skottlistan med en ny instans (kopia av skottet) på den position där det avfyrades
            skott_lista.append(Skott(spelare_x + 20, spelare_y))
            
            # Nollställer räknaren
            skott_räknare = 0


    for skott in reversed(skott_lista):  # Iterera baklänges genom listan
        skott.flytta()
        skott.rita(skärm)
    
        # Ta bort skott som hamnat utanför skärmen
        if skott.y < -100:
            skott_lista.remove(skott)

        
    print(f"Antalet skott i spelet just nu: {Skott.antal_instans}")
    
    # *** RITA ALLA SPRITES PÅ SKÄRMEN ***
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    
    # Rita spelarens rymdskepp
    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
    skärm.blit(sprite_jetstråle, (jetstråle_x, jetstråle_y))

    # *** UPPDATERA ALL GRAFIK PÅ SKÄRMEN ***
    # Uppdaterar grafiken på skärmen så att spelaren ser vart alla spelfigurer flyttat någonstans
    pygame.display.update()

    # Uppdaterar skottets räknare som används för att se när spelaren får skjuta igen 
    skott_räknare = skott_räknare + 1

# Avslutar spelet
pygame.quit()