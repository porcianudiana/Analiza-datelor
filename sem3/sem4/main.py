import pandas as pd
import numpy as np
from scipy.stats import shapiro, kstest, norm, chi2, chisquare

def execute():
    # Obtinere date din fisier csv
    tabel = pd.read_csv("Mortalitate.csv", index_col=0)
    # print(tabel, type(tabel))
    nume_tari = list(tabel.index)
    nume_variabile = list(tabel.columns)
    # print(nume_tari)
    # print(nume_variabile)
    x = tabel.values
    # print(x)
    # print(type(x))
    n, m = x.shape
    # print(n, m)

    # Completare celule lipsa (nan)
    is_nan = np.isnan(x)
    # print(is_nan)
    # print(is_nan[3, :])
    k = np.where(is_nan)
    # print(k)
    # print(x[3, :])
    x[k] = np.nanmean(x[:, k[1]], axis=0)
    # print(x[3, :])

    # Determinare covarianta si coef de corelatie
    v = np.cov(x, rowvar=False, ddof=0)
    # print(v)
    salvare_matrice(v, nume_variabile, nume_variabile, "cov.csv")

    r = np.corrcoef(x, rowvar=False)
    # print(r)
    salvare_matrice(r, nume_variabile, nume_variabile, "r.csv")

    x_std = standardizare_centrare(x)
    salvare_matrice(x_std, nume_tari, nume_variabile, "x_std.csv")

    x_c = standardizare_centrare(x, False)
    salvare_matrice(x_c, nume_tari, nume_variabile, "x_c.csv")

    # teste de concordanta
    tabel = teste_concordanta(x)
    nume_coloane = ["s_shapiro", "p_shapiro", "s_ks", "p_ks", "s_chi2", "p_chi2"]
    salvare_matrice(tabel, nume_variabile, nume_coloane, "teste.csv")

    vector_variabile = np.array(nume_variabile)
    decizie_shapiro = tabel[:, 1] > 0.05
    print(decizie_shapiro)
    print("Variabile care urmeaza o distributie normala conform Shapiro: ", vector_variabile[decizie_shapiro])

    decizie_ks = tabel[:, 3] > 0.05
    print("Variabile care urmeaza o distributie normala conform KS: ", vector_variabile[decizie_ks])

    decizie_chi2 = tabel[:, 5] < 0.05
    print("Variabile care urmeaza o distributie normala conform chi2_test: ", vector_variabile[decizie_chi2])

    decizie_chisquare = tabel[:, 7] > 0.05
    print("Variabile care urmeaza o distributie normala conform scipy Chi2: ", vector_variabile[decizie_chisquare])


def salvare_matrice(x, nume_randuri=None, nume_coloane=None, nume_fisier="out.csv"):
    f = open(nume_fisier, "w")
    if nume_coloane is not None:
        if nume_randuri is not None:
            f.write(",")
        f.write(",".join(nume_coloane) + "\n")
    n = x.shape[0]  # np.shape(x)
    for i in range(n):
        if nume_randuri is not None:
            f.write(nume_randuri[i] + ",")
        f.write(",".join(str(v) for v in x[i, :]) + "\n")
    f.close()


def standardizare_centrare(x, scale=True):
    medii_coloane = np.mean(x, axis=0)
    x_ = x - medii_coloane  # centrarea
    if scale:  # standardizare
        abateri_coloane = np.std(x, axis=0)
        x_ /= abateri_coloane
    return x_


def teste_concordanta(x):
    assert isinstance(x, np.ndarray)
    m = x.shape[1]
    tabel = np.empty((m, 8))

    for i in range(m):
        v = x[:, i]
        tabel[i, 0:2] = shapiro(v)
        tabel[i, 2:4] = kstest(v, 'norm')
        tabel[i, 4:6] = chi2_test(v)
        tabel[i, 6:8] = chisquare(v, )

    return tabel


def chi2_test(v):
    """
    Exista 2 tipuri de teste Chi2:
    - primul tip (test of independence) verifica daca existe vreo relatie intre 2 variabile distincte
    - al doilea tip (goodness of fit) este folosit pentru a emite inferente despre distributia unei variabile

    INFERÉNȚĂ s.f. Operație logică de derivare a unui enunț din altul, prin care se admite o judecată
    (al cărei adevăr nu este verificat direct) în virtutea unei legături a ei cu alte judecăți considerate
    ca adevărate. [< fr. inférence, cf. lat. inferre – a duce].

    In cazul de fata folosim cel de-al 2-lea tip de test Chi2.

    Ce presupune testul Chi2?

    H₀: Variabila are distributia specificata (normala)
    H₁: Variabila nu are distributia specificata (normala)

    Numarul gradelor de libertate ale testlui: d.f. = (numarul de categorii -1)

    Testul compara frecventele observate (O) dintr-o populatie cu freceventele asteptate (E).
    E = probabilitatea unui eveniment * dimensiunea totala a populatiei

    :param v: vectorul de date (ndarray unidimensional cu observatiile unei variabile)
    :return: o pereche compusa din statistica testului Chi2 si p_value
    """
    # calculam lungimea vectorului de date
    len_set_date = len(v)

    # functia histogram din numpy creeaza o reprezentare grafica (histograma) a setului de date, fara a o si desena
    # bins="sturges" => determinarea latimii intervalelor din histograma folosind metoda Sturges
    #
    # Explicatie despre ce sunt si ce rol au bins:
    # https://stackoverflow.com/questions/9141732/how-does-numpy-histogram-work
    # Documentatie a functiei histogram:
    # (https://numpy.org/doc/stable/reference/generated/numpy.histogram.html)
    hist, bin_edges = np.histogram(v, bins="sturges")

    len_hist = len(hist)

    media = np.mean(v)
    std = np.std(v)

    # A normal cumulative distribution function (CDF) will return the percentage of the normal distribution
    # function that is less than or equal to the random variable specified.
    # semnatura functiei cdf e de forma cdf(x, loc, scale), unde
    # x = numele argumentului
    # loc = numele argumentului ce referntiaza media
    # scale = numele argumentului ce referentiaza abaterea medie patratica
    # default cdf(x, loc=0, scale=1)
    d = norm.cdf(bin_edges[1:], media, std) - norm.cdf(bin_edges[:len_hist], media, std)

    expected_dist = len_set_date * d
    chi_square = 0
    # formula: chi_square += (O - E) ** 2 / E
    for i in range(len_hist):
        o = hist[i]
        e = expected_dist[i]
        if e != 0:
            chi_square += ((o - e) * (o - e) / e)

    deg_freedom = len_hist-1
    p_value = chi2.cdf(chi_square, deg_freedom)

    return chi_square, p_value


if __name__ == "__main__":
    execute()















