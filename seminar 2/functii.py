def medie(lista, index):
    suma = 0
    for each in lista:
        suma += int(each[index])
    return suma / len(lista)


def medie_populatie(lista):
    suma = 0
    for tara in lista:
        suma += tara.populatie
    return suma / len(lista)


def filtru_pib_capita(instanta):
    if int(instanta[3]) > 95000:
        return True
    return False


def filtru_populatie(instanta):
    if instanta.populatie > 1000000:
        return True
    return False


def filtru_interval(instanta, prag_minim, prag_maxim):
    # if instanta.populatie > prag_minim and instanta.populatie < prag_maxim:
    if prag_minim < instanta.populatie < prag_maxim:
        return True
    return False


def sortare_dupa_un_criteriu(instanta, index):
    return int(instanta[index])

