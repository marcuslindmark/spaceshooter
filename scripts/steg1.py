# *** STEG 1 ***
# Skapa en skärm, en spelloop och importera en sprite för rymdskeppet
# Gör så att rymdskeppet kan röra på sig

# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

# Initiera pygame
pygame.init()


# *** KONFIGURERA FÖNSTRET ***
# Skärmstorlek
SKÄRMENS_BREDD = 1024
SKÄRMENS_HÖJD = 768

# Skapar en skärm med angiven bredd och höjd (1024 x 768 pixlar)
screen = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

# Sätter en fönstertitel på spelet 
pygame.display.set_caption("Space Shooter")


# *** LADDAR IN ALLA SPRITES ***
# Laddar in en ny sprite för rymdskeppet
original_bild = pygame.image.load("assets/sprites/spaceShip.png")

# Skalar om rymdskeppet till halva storleken 
# Den nya spriten länkas till spelare_bild
# OBS // är operatorn för heltalsdivision 
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

# Sätt spelarens startposition
spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 1


# *** SPELET STARTAR HÄR ***
# Spelloop
spelet_körs = True
while (spelet_körs == True):
    
    # Skapa en mörk bakgrundsbild
    screen.fill((0, 0, 30))  # Mörk bakgrund
    
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

    # Rita spelare
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    screen.blit(sprite_spelare, (spelare_x, spelare_y))

    # Uppdaterar grafiken på skärmen så att spelaren ser vart alla spelfigurer flyttat någonstans
    pygame.display.update()

# Avslutar spelet
pygame.quit()