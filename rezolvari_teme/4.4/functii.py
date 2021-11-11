import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np


def nan_replace(t):
    assert isinstance(t, pd.DataFrame)
    variabile = list(t.columns)
    for variabila in variabile:
        if any(t[variabila].isna()):
            if is_numeric_dtype(t[variabila]):
                t[variabila].fillna(t[variabila].mean(), inplace=True)
            else:
                modulul = t[variabila].mode()[0]
                t[variabila].fillna(modulul, inplace=True)


def calcul_procente(t, variabile, variabila_raport):
    p = t[variabile] * 100 / t[variabila_raport]
    return p


def vot_majoritar(t):
    k = np.argmax(t.iloc[1:]) + 1
    return pd.Series(
        data={"Localitate": t["City"],
              "Partid majoritar": t.index[k]}
    )
