import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype


def execute():
    tabel_etnii = pd.read_csv("Ethnicity.csv", index_col=0)
    nan_replace(tabel_etnii)

    variabile_etnii = list(tabel_etnii.columns)[1:]
    print(variabile_etnii)

    # calcul populatie pe etnii la nivel de judet

    localitati = pd.read_excel("CoduriRomania.xlsx", index_col=0)
    t1 = tabel_etnii.merge(right=localitati, left_index=True, right_index=True)
    # print(t1)

    g1 = t1[variabile_etnii + ["County"]].groupby(by="County").agg(sum)
    assert isinstance(g1, pd.DataFrame)
    g1.to_csv("EtniiJudete.csv")

    # calcul populatie pe etnii la nivel de regiune
    judete = pd.read_excel("CoduriRomania.xlsx", sheet_name=1, index_col=0)
    t2 = g1.merge(right=judete, left_index=True, right_index=True)
    g2 = t2[variabile_etnii + ["Regiune"]].groupby(by="Regiune").agg(sum)
    assert isinstance(g2, pd.DataFrame)
    g2.to_csv("EtniiRegiuni.csv")

    # calcul populatie pe etnii la nivel de macroregiune
    regiuni = pd.read_excel("CoduriRomania.xlsx", sheet_name="Regiuni", index_col=0)
    t3 = g2.merge(right=regiuni, left_index=True, right_index=True)
    g3 = t3[variabile_etnii + ["MacroRegiune"]].groupby(by="MacroRegiune").agg(sum)
    assert isinstance(g3, pd.DataFrame)
    g3.to_csv("EtniiMacroRegiuni.csv")

    # indici de diversitate la nivel de localitate
    div_loc = tabel_etnii.apply(func=diversitate, axis=1, denumire_coloana="Localitate")
    div_loc.to_csv("DiversitateLocalitati.csv")

    # indici de diversitate la nivel de judet
    div_judet = g1.apply(func=diversitate, axis=1)
    div_judet.to_csv("DiversitateJudete.csv")

    # indici de diversitate la nivel de regiune
    div_regiune = g2.apply(func=diversitate, axis=1)
    div_regiune.to_csv("DiversitateRegiuni.csv")


def nan_replace(t):
    assert isinstance(t, pd.DataFrame)
    nume_variabile = list(t.columns)
    for v in nume_variabile:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                modulul = t[v].mode()[0]
                t[v].fillna(modulul, inplace=True)


def diversitate(t, denumire_coloana=None):
    assert isinstance(t, pd.Series)
    if denumire_coloana is not None:
        x = np.array(t.iloc[1:], dtype=float)
    else:
        x = np.array(t.values)

    suma = np.sum(x)
    proportii = x / suma

    k = proportii == 0
    proportii[k] = 1

    shannon = -np.sum(proportii * np.log2(proportii))

    proportii_ = x / suma
    d = np.sum(proportii_ * proportii_)

    simpson = 1 - d
    inv_simpson = 1 / d

    if denumire_coloana is not None:
        serie_div = pd.Series(data=[t.iloc[0], shannon, simpson, inv_simpson],
                              index=[denumire_coloana, "Shannon", "Simpson", "Inverse Simpson"])
    else:
        serie_div = pd.Series(data=[shannon, simpson, inv_simpson],
                              index=["Shannon", "Simpson", "Inverse Simpson"])

    return serie_div


if __name__ == "__main__":
    execute()