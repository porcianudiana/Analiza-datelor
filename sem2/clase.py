class Entitate:
    # echivalentul unui constructor
    def __init__(self, id, nume):
        self.id = id
        self.nume = nume

    def display(self):
        print(self.id, self.nume)  # 1 Monaco


class Tara(Entitate):
    def __init__(self, id, nume, populatie, pib):
        # echivalent: super.__init__(id, nume)
        Entitate.__init__(self, id, nume)
        self.populatie = populatie
        self.pib = pib

    def display(self):
        print(self.id, self.nume, self.populatie, self.pib)

    def __str__(self):
        #return self.id + " " + self.nume + " " + self.populatie + " " + self.pib
        return "{0} {1} {2} {3}".format(self.id, self.nume, self.populatie, self.pib)

    def __lt__(self, other):
        return self.pib < other.pib


a = Tara(1, "test", 1000, 1234)
b = Tara(2, "test2", 2000, 2345)
c = Tara(3, "test3", 3000, 3456)
a.display()
lista = [a, b, c]
for each in lista:
    print(each)