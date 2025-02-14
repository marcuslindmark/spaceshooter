# Skapar klassen HusDjur
class HusDjur:
    # Här sätts alla startvärden på instansvariablerna
    def __init__(self, namn, ålder):
        self.namn = namn
        self.ålder = ålder
        self.energi = -1  # Startvärde

    # Metoden äta låter husdjuret äta något och få mer energi
    def äta(self):
        self.energi = self.energi + 5
        print(f"{self.namn} äter och får mer energi! Energinivå: {self.energi}")

    # Metoden hoppa låter husdjuret hoppa men bara om den har tillräckligt med energi för det
    def hoppa(self):
        if (self.energi > 0):
            self.energi = self.energi - 3
            print(f"{self.namn} hoppar! Energinivå: {self.energi}")
        else:
            print(f"{self.namn} är för trött för att hoppa.")

# Skapar husdjursobjektet och interagerar med husdjuret genom metoderna
mitt_husdjur = HusDjur("Misse", 2)
mitt_husdjur.hoppa()
mitt_husdjur.äta()
mitt_husdjur.hoppa()
