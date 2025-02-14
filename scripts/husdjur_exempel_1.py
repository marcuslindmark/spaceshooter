# Skapar klassen HusDjur
class HusDjur:
    # Konstruktor (__init__) som skapar ett husdjursobjekt med namn och ålder
    # Den tilldelar startvärden till instansvariablerna som hör till just detta objekt.
    def __init__(self, namn, ålder):    
        self.namn = namn    # Sparar djurets namn i en instansvariabel
        self.ålder = ålder  # Sparar djurets ålder i en instansvariabel

    # Metoden prata som låter HusDjuret presentera sig 
    # (låt oss anta att det är ett väldigt smart djur som kan prata)
    def prata(self):
        print(f"Hej! Jag heter {self.namn} och jag är {self.ålder} år gammal.")

# Skapar ett husdjursobjekt
mitt_husdjur = HusDjur("Fido", 3)

# Anropar metoden prata på objektet mitt_husdjur med punktnotation
mitt_husdjur.prata()
