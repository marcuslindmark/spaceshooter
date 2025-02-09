# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

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

# En lista för alla skotten
skott_lista = []

# *** LADDAR IN ALLA BAKGRUNDSBILDER ***
# Laddar en stjärnbakgrund
background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/Stars-A.png")

# *** LADDAR IN ALLA SPRITES ***
# Laddar in en ny sprite för rymdskeppet
original_bild = pygame.image.load("assets/sprites/spaceShip.png")

# Skalar om rymdskeppet till halva storleken 
# Den nya spriten länkas till sprite_spelare
# OBS // är operatorn för heltalsdivision 
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

# Laddar in en ny sprite för jetstrålen till rymdskeppet
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")

# Laddar in en ny sprite till ett skott till rymdskeppet
sprite_skott = pygame.image.load("assets/sprites/bullet.png")


# *** SAMTLIGA KLASSER I SPELET ***
# Denna klass hanterar det vanliga skottet som skeppet kan skjuta
class Skott:
    # Sätter alla instansvariabler som hör till skottet
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

# Sätt spelarens startposition
spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 10

# *** BAKGRUNDSRÖRELSE ***
# Bakgrundens Y-position (börjar från toppen av skärmen)
bakgrund_y = 0

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
    
    # Den här koden kollar hela tiden om användaren försöker stänga spelet 
    # genom att klicka på fönstrets stängknapp. 
    for event in pygame.event.get():
        # Om användaren klickar på fönstrets stängningsknapp avslutas loopen
        if event.type == pygame.QUIT:
            spelet_körs = False

    # Hantera tangenttryckningar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x = spelare_x - spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x = spelare_x + spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y = spelare_y - spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_width() + 26:
        spelare_y = spelare_y + spelarens_hastighet
    # Om spelaren trycker på SPACE skjut en kula
    if keys[pygame.K_SPACE]:          
        # Uppdaterar skottlistan med en ny instans (kopia av skottet) på den position där det avfyrades
        skott_lista.append(Skott(spelare_x + 20, spelare_y))
            



    for skott in reversed(skott_lista):  # Iterera baklänges genom listan
        skott.flytta()
        skott.rita(skärm)
    
        # Ta bort skott som hamnat utanför skärmen
        if skott.y < -100:
            skott_lista.remove(skott)
    # Rita spelare
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    skärm.blit(sprite_spelare, (spelare_x, spelare_y))

    # Uppdaterar grafiken på skärmen så att spelaren ser vart alla spelfigurer flyttat någonstans
    pygame.display.update()

# Avslutar spelet
pygame.quit()