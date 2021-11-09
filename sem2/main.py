import functii as f
from clase import Tara

# citire din fisier
nume_fisier = "dataset.csv"
fisier = open(nume_fisier, 'r')
print(type(fisier))

linii = fisier.readlines()
for linie in linii:
    print(linie[:-1])  # fara ultimul caracter \n

# preluare date in liste
lista_tupluri = []
lista_liste = []
lista_instante = []
for linie in linii:
    if linie.startswith("ID"):
        continue
    cuvinte = linie[:-1].split(',')
    # print(type(cuvinte))

    instanta = Tara(int(cuvinte[0]), cuvinte[1], int(cuvinte[2]), int(cuvinte[3]))
    lista_instante.append(instanta)

    lista_liste.append(cuvinte)
    lista_tupluri.append(tuple(cuvinte))

print(type(lista_instante[0]))
print(type(lista_liste[0]))
print(type(lista_tupluri[0]))
print("Lista de instante:")
for each in lista_instante:
    print(each)

print("Valoarea medie a pib/capita este %s" % f.medie(lista_tupluri, 3))
print("Valoarea medie a populatiei este", f.medie_populatie(lista_instante))

# Explicatii aditionale

# list comprehension
numere = [1,2,3,4,5]
patrate = []
for each in numere:
    patrate.append(each * each)

patrate = [x * x for x in numere]
pare = [x for x in range(20) if x % 2 == 0]
litere = [l for l in "python"]
divizibile_cu_zece = [x for x in range(100) if x % 2 == 0 if x % 5 == 0]
pare_impare = ["par" if x % 2 == 0 else "impar" for x in range(10)]


# lambda functions (functii anonime)
fa = lambda a, b: a * b
print(fa(2, 5))

# filter(function, sequence)

def fun(litera):
    vocale = ['a', 'e', 'i', 'o', 'u']
    if litera in vocale:
        return True
    return False

litere = ['g','h','i','j,','o']
litere_filtrate = filter(fun, litere)
print(litere)
for each in litere_filtrate:
    print(each)


# map(function, sequence)
print("Map examples")
numbers = (1, 2, 3, 4)
result = map(lambda x: x**3, numbers)
for each in result:
    print(each)

a_sequence = [1, 2, 3, 4, 5]
b_sequence = [10, 9, 8, 7, 6]

result = list(map(lambda x, y: x+y, a_sequence, b_sequence))
print(result)

# filtrare pe date
print("Filtru pib")
filtru_pib = filter(f.filtru_pib_capita, lista_tupluri)
for each in filtru_pib:
    print(each)

print("Filtru populatie")
filtru_populatie = filter(f.filtru_populatie, lista_instante)
for each in filtru_populatie:
    print(each)

print("Filtru interval")
minim = 100000
maxim = 1000000
filtru_interval = filter(lambda x: f.filtru_interval(x, minim, maxim), lista_instante)
for each in filtru_interval:
    print(each)

print("Sortare folosind sorted()")
valori_sortate = sorted(lista_tupluri, key=lambda x: f.sortare_dupa_un_criteriu(x, 2), reverse=True)
print(valori_sortate)

valori_sortate = sorted(lista_instante, key=lambda x: x.pib)
for each in valori_sortate:
    print(each)

print("Sortare folosind sort()")
for each in lista_instante:
    print(each)
lista_instante.sort()
for each in lista_instante:
    print(each)


pib_mediu = f.medie(lista_tupluri, 3)
print("Transformari")
valori_transformate = list(map(lambda x: (x[1], x[3], str(int(x[3]) * 100 / pib_mediu) + "%"), lista_tupluri))
print(valori_transformate)

# valori_transformate = map(lambda x: (x[1], x[3], str(int(x[3]) * 100 / pib_mediu) + "%"), lista_tupluri)
# for each in valori_transformate:
#     print(each)
# for each in valori_transformate:
#     print(each)  # nu sunt printate valori, intrucat iteratorul a ajuns la finalul secventei

print("Salvare in fisier csv")
fisier_rezultat = open("raport_pib.csv", "w")
spatiu = " ___ "
fisier_rezultat.write("Nume PIB/CAPITA % din medie\n")
for each in valori_transformate:
    fisier_rezultat.write(spatiu.join(cuvant for cuvant in each))
    # fisier_rezultat.write(each[0] + " " + each[1] + " " + each[2])
    fisier_rezultat.write("\n")
fisier_rezultat.close()