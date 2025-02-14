class HusDjur:
    def __init__(self, namn):
        self.namn = namn
        self.energi = 10

    def äta(self):
        self.energi = self.energi + 5
        print(f"{self.namn} åt och fick mer energi! Energi: {self.energi}")

    def hoppa(self):
        if self.energi > 0:
            self.energi = self.energi - 3
            print(f"{self.namn} hoppar! Energi: {self.energi}")
        else:
            print(f"{self.namn} är för trött.")

# Skapa ett husdjur med användarens input
namn = input("Vad heter ditt husdjur? ")
mitt_husdjur = HusDjur(namn)

# Huvudloop där spelaren kan välja handlingar
while True:
    val = input("Vad vill du göra? (äta/hoppa/avsluta): ").lower()
    if val == "äta":
        mitt_husdjur.äta()
    elif val == "hoppa":
        mitt_husdjur.hoppa()
    elif val == "avsluta":
        print("Hej då!")
        break
    else:
        print("Ogiltigt val, försök igen.")
